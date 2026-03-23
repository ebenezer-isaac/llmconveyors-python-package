"""Extended E2E: B2B Sales workflow + Resume upload/parse + all remaining endpoints."""

from __future__ import annotations

import io
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Load from .env file if not already set
if "LLMCONVEYORS_API_KEY" not in os.environ:
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("LLMCONVEYORS_API_KEY="):
                os.environ["LLMCONVEYORS_API_KEY"] = line.split("=", 1)[1].strip()

from llmconveyors import LLMConveyors
from llmconveyors.errors import LLMConveyorsError

report: list[str] = []
passed = 0
failed = 0
test_num = 0


def log(msg: str):
    report.append(msg)
    print(msg)


def t(name: str, fn, *, expect_error: str | None = None) -> Any:
    global test_num, passed, failed
    test_num += 1
    try:
        result = fn()
        if expect_error:
            failed += 1
            log(f"  [{test_num}] FAIL {name}: expected error {expect_error} but succeeded")
            return result
        passed += 1
        # Summarize
        if hasattr(result, "model_dump"):
            summary = json.dumps(result.model_dump(by_alias=True), default=str)[:300]
        elif isinstance(result, list):
            summary = f"list[{len(result)}]"
        elif isinstance(result, (bytes,)):
            summary = f"bytes[{len(result)}]"
        elif result is None:
            summary = "204 No Content"
        else:
            summary = str(result)[:300]
        log(f"  [{test_num}] PASS {name}: {summary}")
        report.append(f"```\n{json.dumps(result.model_dump(by_alias=True) if hasattr(result, 'model_dump') else result, indent=2, default=str)[:2000]}\n```\n" if result else "")
        return result
    except LLMConveyorsError as e:
        if expect_error and e.code == expect_error:
            passed += 1
            log(f"  [{test_num}] PASS {name}: [{e.code}] {e.message} (expected)")
            return None
        failed += 1
        log(f"  [{test_num}] FAIL {name}: [{e.code}] {e.message}")
        return None
    except Exception as e:
        failed += 1
        log(f"  [{test_num}] FAIL {name}: {type(e).__name__}: {str(e)[:200]}")
        return None


def main():
    log(f"# Extended E2E — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
    client = LLMConveyors()

    # =================================================================
    # B2B SALES — FULL WORKFLOW
    # =================================================================
    log("\n## B2B Sales — Full Generate + Stream + Artifacts\n")

    b2b_input = {
        "companyName": "Notion",
        "companyWebsite": "https://notion.so",
        "skipResearchCache": True,
        "senderName": "Ebenezer Isaac",
    }

    gen = t("B2B Generate", lambda: client.agents.generate("b2b-sales", b2b_input))

    if gen:
        log(f"\n### SSE Stream for B2B Sales\n")
        event_counts: dict[str, int] = {}
        final = None
        stream_start = time.monotonic()

        try:
            for event in client.stream.generation(
                gen.generation_id, include_heartbeats=True, include_logs=True
            ):
                etype = type(event).__name__
                event_counts[etype] = event_counts.get(etype, 0) + 1

                if etype == "ProgressEvent":
                    log(f"    [{event.step}] {event.percent}%{(' - ' + event.message) if event.message else ''}")
                elif etype == "LogEvent":
                    log(f"    [log:{event.level}] {event.content[:80]}")
                elif etype == "CompleteEvent":
                    final = event
                    log(f"    [COMPLETE] success={event.success}, artifacts={len(event.artifacts)}")
                    break
                if sum(event_counts.values()) > 500:
                    break
        except LLMConveyorsError as e:
            log(f"    [STREAM ERROR] {e.code}: {e.message}")
        except Exception as e:
            log(f"    [ERROR] {e}")

        elapsed = time.monotonic() - stream_start
        log(f"\n**Stream duration:** {elapsed:.0f}s | **Events:** {json.dumps(event_counts)}")

        if final:
            global passed
            passed += 1
            log(f"\n### B2B Artifacts ({len(final.artifacts)})\n")
            for i, art in enumerate(final.artifacts):
                art_type = art.get("type", "?")
                log(f"**Artifact {i+1}: {art_type}**")
                payload = art.get("payload", {})
                if isinstance(payload, dict):
                    content = payload.get("content", "")
                    if content:
                        log(f"```\n{content[:1500]}\n```\n")
        else:
            global failed
            failed += 1
            log("FAIL: No complete event received")

        # Status
        t("B2B Status", lambda: client.agents.get_status("b2b-sales", gen.job_id, include="artifacts"))

        # Hydrate
        hydration = t("B2B Hydrate", lambda: client.sessions.hydrate(gen.session_id))
        if hydration:
            log(f"  Artifacts: {len(hydration.artifacts)}, GenLogs: {len(hydration.generation_logs)}, "
                f"ColdEmailVersions: {len(hydration.cold_email_versions)}")

        # Download artifacts
        if hydration and hydration.artifacts:
            for art in hydration.artifacts[:3]:
                if isinstance(art, dict):
                    key = art.get("storageKey") or art.get("key", "")
                    if key:
                        dl = t(f"B2B Download ({art.get('type', '?')})",
                               lambda k=key: client.sessions.download(gen.session_id, k))
                        if dl:
                            size = len(dl) if isinstance(dl, (bytes, str, dict)) else 0
                            log(f"    Downloaded: {size} bytes/chars")

        # =============================================================
        # SHARES CREATE (must happen BEFORE session delete)
        # =============================================================
        log("\n## Shares\n")

        if gen:
            # B2B sales has no ATS artifacts, so share create correctly returns NOT_FOUND
            # This validates the SDK correctly handles the error
            share = t("Create share (B2B has no ATS — expects NOT_FOUND)", lambda: client.shares.create({
                "sessionId": gen.session_id,
                "generationId": gen.generation_id,
            }), expect_error="NOT_FOUND")

        # Cleanup
        try:
            client.sessions.delete(gen.session_id)
            log(f"  Cleaned up session {gen.session_id}")
        except Exception:
            pass

    # =================================================================
    # RESUME UPLOAD + PARSE
    # =================================================================
    log("\n## Resume Upload + Parse\n")

    # Create a simple text resume for testing
    resume_text = """EBENEZER ISAAC
Senior Software Engineer | Python, TypeScript, React
London, UK | ebnezr.isaac@gmail.com | +44 75010 53232

EXPERIENCE:
Application Developer, IBM (2023-2025)
- Developed static analysis tools reducing bug triage time by 70%
- Built Python automation preventing P1 incidents

Full Stack Developer, Jatpoint (2025-2026)
- Led Phase 2 platform overhaul on AWS
- Engineered real-time radar chart visualization

EDUCATION:
MSc Systems Engineering for IoT, UCL (2025-2026)
BEng Computer Science, VTU (2019-2023)

SKILLS: Python, TypeScript, React, Node.js, AWS, Docker, MongoDB, PostgreSQL
"""

    # Write temp file
    temp_resume = Path(__file__).parent / "temp_resume.txt"
    temp_resume.write_text(resume_text)

    t("Upload resume (file)", lambda: client.upload.resume(str(temp_resume)))

    t("Parse resume (file)", lambda: client.resume.parse(str(temp_resume)))

    temp_resume.unlink(missing_ok=True)

    # =================================================================
    # RESUME VALIDATE + RENDER + PREVIEW
    # =================================================================
    log("\n## Resume Validate + Render + Preview\n")

    sample_resume = {
        "basics": {
            "name": "Test User",
            "label": "Software Engineer",
            "email": "test@example.com",
            "summary": "Experienced engineer",
            "location": {"city": "London", "countryCode": "UK"},
            "profiles": [],
        },
        "work": [{
            "name": "Acme Corp",
            "position": "Engineer",
            "startDate": "2020-01-01",
            "summary": "Built things",
            "highlights": ["Led team of 5"],
        }],
        "education": [{
            "institution": "MIT",
            "area": "Computer Science",
            "studyType": "BS",
            "startDate": "2016-01-01",
            "endDate": "2020-01-01",
        }],
        "skills": [{"name": "Python", "keywords": ["Django", "FastAPI"]}],
    }

    t("Validate resume", lambda: client.resume.validate(sample_resume))

    t("Render resume (PDF)", lambda: client.resume.render({
        "resume": sample_resume, "theme": "even", "format": "pdf"
    }))

    t("Preview resume (HTML)", lambda: client.resume.preview(sample_resume, "even"))

    # =================================================================
    # MASTER RESUME CRUD
    # =================================================================
    log("\n## Master Resume CRUD\n")

    master = t("Create master resume", lambda: client.resume.create_master({
        "label": "SDK E2E Test Resume",
        "rawText": resume_text,
        "isDefault": False,
    }))

    if master:
        t("List masters", lambda: client.resume.list_masters())
        t("Get master", lambda: client.resume.get_master(master.id))
        t("Update master", lambda: client.resume.update_master(master.id, {"label": "Updated Label"}))
        t("Delete master", lambda: client.resume.delete_master(master.id))

    # =================================================================
    # CONTENT SAVE
    # =================================================================
    log("\n## Content Save\n")

    t("Save content (original_cv)", lambda: client.content.save({
        "docType": "original_cv",
        "content": "Test resume content from SDK E2E test",
    }))

    # (Shares tested above, before session cleanup)

    # =================================================================
    # SUMMARY
    # =================================================================
    total = passed + failed
    log(f"\n{'='*60}")
    log(f"  TOTAL: {passed} PASS / {failed} FAIL ({total} tests)")
    log(f"{'='*60}")

    report_path = Path(__file__).parent.parent / "E2E_FULL_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    log(f"\nReport: {report_path}")

    client.close()
    return failed


if __name__ == "__main__":
    sys.exit(main())
