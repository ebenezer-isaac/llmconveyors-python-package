"""Comprehensive E2E live test — every endpoint, full I/O logging, artifact retrieval."""

from __future__ import annotations

import io
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Fix Windows console encoding
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

# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

report_lines: list[str] = []
test_num = 0
passed = 0
failed = 0
skipped = 0


def section(title: str):
    report_lines.append(f"\n## {title}\n")
    print(f"\n{'='*60}\n  {title}\n{'='*60}")


def test(
    name: str,
    endpoint: str,
    method: str,
    input_data: Any,
    fn,
    *,
    skip: bool = False,
    expect_error: str | None = None,
):
    global test_num, passed, failed, skipped
    test_num += 1

    if skip:
        skipped += 1
        report_lines.append(f"\n### Test {test_num}: {name}\n")
        report_lines.append(f"- **Endpoint:** `{method} {endpoint}`\n")
        report_lines.append(f"- **Status:** SKIPPED\n")
        print(f"  [{test_num}] SKIP {name}")
        return None

    report_lines.append(f"\n### Test {test_num}: {name}\n")
    report_lines.append(f"- **Endpoint:** `{method} {endpoint}`\n")

    # Log input
    if input_data is not None:
        input_str = json.dumps(input_data, indent=2, default=str)
        report_lines.append(f"- **Input:**\n```json\n{input_str}\n```\n")

    try:
        start = time.monotonic()
        result = fn()
        elapsed = time.monotonic() - start

        if expect_error:
            # Expected an error but got success — that's a failure
            failed += 1
            report_lines.append(f"- **Status:** FAIL (expected error `{expect_error}` but succeeded)\n")
            print(f"  [{test_num}] FAIL {name}: expected error {expect_error}")
            return result

        # Serialize output
        if hasattr(result, "model_dump"):
            output = result.model_dump(by_alias=True)
        elif isinstance(result, list) and result and hasattr(result[0], "model_dump"):
            output = [r.model_dump(by_alias=True) for r in result[:3]]
            if len(result) > 3:
                output.append(f"... +{len(result)-3} more")
        elif isinstance(result, (dict, list, str, int, float, bool)):
            output = result
        elif result is None:
            output = "null (204 No Content)"
        else:
            output = str(result)[:2000]

        output_str = json.dumps(output, indent=2, default=str)
        # Truncate very long outputs
        if len(output_str) > 3000:
            output_str = output_str[:3000] + "\n... (truncated)"

        report_lines.append(f"- **Status:** PASS ({elapsed:.1f}s)\n")
        report_lines.append(f"- **Output:**\n```json\n{output_str}\n```\n")
        passed += 1
        print(f"  [{test_num}] PASS {name} ({elapsed:.1f}s)")
        return result

    except LLMConveyorsError as e:
        if expect_error and e.code == expect_error:
            # Got the expected error — this is a PASS
            passed += 1
            report_lines.append(f"- **Status:** PASS (expected error)\n")
            report_lines.append(f"- **Error Code:** `{e.code}` (expected)\n")
            report_lines.append(f"- **Error Message:** {e.message}\n")
            if e.hint:
                report_lines.append(f"- **Hint:** {e.hint}\n")
            report_lines.append(f"- **SDK handled correctly:** Raised `{type(e).__name__}`\n")
            print(f"  [{test_num}] PASS {name}: [{e.code}] {e.message} (expected)")
            return None

        failed += 1
        report_lines.append("- **Status:** FAIL\n")
        report_lines.append(f"- **Error Code:** `{e.code}`\n")
        report_lines.append(f"- **Error Message:** {e.message}\n")
        if e.hint:
            report_lines.append(f"- **Hint:** {e.hint}\n")
        print(f"  [{test_num}] FAIL {name}: [{e.code}] {e.message}")
        return None

    except Exception as e:
        failed += 1
        report_lines.append("- **Status:** FAIL\n")
        report_lines.append(f"- **Error:** `{type(e).__name__}: {e}`\n")
        print(f"  [{test_num}] FAIL {name}: {type(e).__name__}: {e}")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    report_lines.append("# LLM Conveyors SDK - Comprehensive E2E Test Report\n")
    report_lines.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
    report_lines.append(f"**SDK Version:** 0.1.0\n")
    report_lines.append(f"**Base URL:** https://api.llmconveyors.com/api/v1\n")

    client = LLMConveyors()

    # ===================================================================
    # HEALTH
    # ===================================================================
    section("1. Health Endpoints")

    test("Health check", "/health", "GET", None,
         lambda: client.health.check())

    test("Readiness", "/health/ready", "GET", None,
         lambda: client.health.ready())

    test("Liveness", "/health/live", "GET", None,
         lambda: client.health.live())

    # ===================================================================
    # SETTINGS
    # ===================================================================
    section("2. Settings Endpoints")

    profile = test("Get profile", "/settings/profile", "GET", None,
                   lambda: client.settings.get_profile())

    test("Get preferences", "/settings/preferences", "GET", None,
         lambda: client.settings.get_preferences())

    test("Get usage summary", "/settings/usage-summary", "GET",
         {"offset": 0, "limit": 50},
         lambda: client.settings.get_usage_summary())

    test("Get usage logs", "/settings/usage-logs", "GET",
         {"offset": 0, "limit": 5},
         lambda: client.settings.get_usage_logs(limit=5))

    test("List API keys", "/settings/platform-api-keys", "GET", None,
         lambda: client.settings.list_api_keys())

    test("Get BYO key status", "/settings/api-key", "GET", None,
         lambda: client.settings.get_byo_key())

    test("Get webhook secret", "/settings/webhook-secret", "GET", None,
         lambda: client.settings.get_webhook_secret())

    # ===================================================================
    # SESSIONS
    # ===================================================================
    section("3. Sessions Endpoints")

    test("Session init", "/sessions/init", "GET", None,
         lambda: client.sessions.init())

    sessions_list = test("List sessions", "/sessions", "GET", None,
                         lambda: client.sessions.list())

    create_body: dict[str, Any] = {}
    new_session = test("Create session", "/sessions", "POST", create_body,
                       lambda: client.sessions.create())

    sid = new_session.id if new_session else None

    if sid:
        test("Get session", f"/sessions/{sid}", "GET", None,
             lambda: client.sessions.get(sid))

        test("Hydrate session", f"/sessions/{sid}/hydrate", "GET", None,
             lambda: client.sessions.hydrate(sid))

        log_body = {"role": "user", "content": "Test log entry from SDK E2E test"}
        test("Append log", f"/sessions/{sid}/log", "POST", log_body,
             lambda: client.sessions.log(sid, log_body))

        test("Delete session", f"/sessions/{sid}", "DELETE", None,
             lambda: client.sessions.delete(sid))
    else:
        report_lines.append("\n> Skipping session get/hydrate/log/delete — create failed\n")

    # ===================================================================
    # RESUME
    # ===================================================================
    section("4. Resume Endpoints")

    test("List themes", "/resume/themes", "GET", None,
         lambda: client.resume.themes())

    # ===================================================================
    # AGENT MANIFESTS
    # ===================================================================
    section("5. Agent Manifests")

    test("Job Hunter manifest", "/agents/job-hunter/manifest", "GET", None,
         lambda: client.agents.get_manifest("job-hunter"))

    test("B2B Sales manifest", "/agents/b2b-sales/manifest", "GET", None,
         lambda: client.agents.get_manifest("b2b-sales"))

    # ===================================================================
    # SHARES
    # ===================================================================
    section("6. Shares Endpoints")

    test("List shares (stats)", "/shares/stats", "GET", None,
         lambda: client.shares.get_stats())

    # ===================================================================
    # REFERRAL
    # ===================================================================
    section("7. Referral Endpoints")

    test("Get referral stats", "/referral/stats", "GET", None,
         lambda: client.referral.get_stats())

    test("Get referral code", "/referral/code", "GET", None,
         lambda: client.referral.get_code())

    # ===================================================================
    # PRIVACY
    # ===================================================================
    section("8. Privacy Endpoints")

    test("List consents", "/privacy/consents", "GET", None,
         lambda: client.privacy.list_consents())

    # ===================================================================
    # ATS SCORING
    # ===================================================================
    section("9. ATS Scoring")

    ats_input = {
        "resumeText": (
            "John Doe\nSenior Software Engineer | 10 Years Experience\n\n"
            "SKILLS: Python, TypeScript, React, Node.js, AWS, Docker, Kubernetes, "
            "PostgreSQL, MongoDB, Redis, GraphQL, REST APIs, CI/CD, Terraform\n\n"
            "EXPERIENCE:\n"
            "Staff Engineer at Amazon Web Services (2020-2026)\n"
            "- Led team of 8 engineers building real-time data pipelines\n"
            "- Reduced infrastructure costs by 40% through Kubernetes optimization\n"
            "- Designed microservices architecture serving 10M+ daily requests\n\n"
            "Senior Engineer at Stripe (2018-2020)\n"
            "- Built payment processing APIs handling $1B+ annual volume\n"
            "- Implemented automated testing reducing bugs by 60%\n\n"
            "EDUCATION: MS Computer Science, MIT (2016)\nBS Computer Science, Stanford (2014)"
        ),
        "jobDescription": (
            "Senior Software Engineer - AI Platform\n\n"
            "We're looking for an experienced engineer to build AI-powered tools. "
            "Requirements:\n"
            "- 5+ years experience with Python and TypeScript\n"
            "- Experience with cloud services (AWS/GCP) and containerization\n"
            "- Strong understanding of distributed systems and microservices\n"
            "- Experience with ML/AI infrastructure is a plus\n"
            "- Familiarity with CI/CD pipelines and infrastructure as code"
        ),
        "jobTitle": "Senior Software Engineer",
    }

    ats_result = test("Score resume", "/ats/score", "POST", ats_input,
                      lambda: client.ats.score(ats_input))

    # ===================================================================
    # UPLOAD — Job Text
    # ===================================================================
    section("10. Upload Endpoints")

    job_text_input = {
        "text": (
            "Senior Software Engineer - AI Platform at Anthropic\n\n"
            "About the role:\n"
            "We're building the next generation of AI safety tools. "
            "You'll work on infrastructure powering Claude.\n\n"
            "Requirements:\n"
            "- 5+ years Python/TypeScript\n"
            "- Cloud infrastructure experience\n"
            "- Strong systems design skills\n\n"
            "Location: San Francisco\n"
            "Email: careers@anthropic.com"
        ),
    }

    job_text_result = test("Upload job text", "/upload/job-text", "POST",
                           job_text_input,
                           lambda: client.upload.job_text(job_text_input))

    # ===================================================================
    # JOB HUNTER — FULL WORKFLOW
    # ===================================================================
    section("11. Job Hunter — Full Generate + Stream Workflow")

    generate_input = {
        "companyName": "Anthropic",
        "jobTitle": "Senior Software Engineer",
        "companyWebsite": "https://anthropic.com",
        "contactEmail": "careers@anthropic.com",
        "genericEmail": "hello@anthropic.com",
        "jobSourceUrl": "https://anthropic.com/careers",
        "jobDescription": (
            "Senior Software Engineer for AI safety research tools. "
            "5+ years Python/TypeScript, distributed systems, ML infrastructure."
        ),
        "autoSelectContacts": True,
        "skipResearchCache": True,
    }

    gen = test("Generate (job-hunter)", "/agents/job-hunter/generate", "POST",
               generate_input,
               lambda: client.agents.generate("job-hunter", generate_input))

    # Stream events
    if gen:
        report_lines.append(f"\n### Test {test_num + 1}: SSE Stream\n")
        report_lines.append(f"- **Endpoint:** `GET /stream/generation/{gen.generation_id}`\n")
        report_lines.append("- **Events received:**\n\n```\n")

        event_log: list[str] = []
        event_counts: dict[str, int] = {}
        final_complete = None
        stream_start = time.monotonic()

        print(f"\n  Streaming generation {gen.generation_id}...")
        try:
            for event in client.stream.generation(
                gen.generation_id,
                include_heartbeats=True,
                include_logs=True,
            ):
                etype = type(event).__name__
                event_counts[etype] = event_counts.get(etype, 0) + 1

                if etype == "ProgressEvent":
                    line = f"[{event.step}] {event.percent}%"
                    if event.message:
                        line += f" - {event.message}"
                    event_log.append(line)
                    print(f"    {line}")
                elif etype == "ChunkEvent":
                    event_log.append(f"[chunk #{event.index}] {event.chunk[:80]}...")
                elif etype == "LogEvent":
                    line = f"[log:{event.level}] {event.content[:100]}"
                    event_log.append(line)
                    print(f"    {line}")
                elif etype == "HeartbeatEvent":
                    event_log.append("[heartbeat]")
                elif etype == "CompleteEvent":
                    final_complete = event
                    event_log.append(
                        f"[COMPLETE] success={event.success}, "
                        f"artifacts={len(event.artifacts)}, "
                        f"awaitingInput={event.awaiting_input}"
                    )
                    print(f"    [COMPLETE] {len(event.artifacts)} artifacts")
                    break

                if sum(event_counts.values()) > 500:
                    event_log.append("[SAFETY CUTOFF at 500 events]")
                    break

        except LLMConveyorsError as e:
            event_log.append(f"[STREAM ERROR] {e.code}: {e.message}")
            print(f"    STREAM ERROR: {e.code}: {e.message}")
        except Exception as e:
            event_log.append(f"[ERROR] {type(e).__name__}: {e}")
            print(f"    ERROR: {e}")

        stream_elapsed = time.monotonic() - stream_start

        for line in event_log:
            report_lines.append(f"{line}\n")
        report_lines.append("```\n")
        report_lines.append(f"- **Duration:** {stream_elapsed:.1f}s\n")
        report_lines.append(f"- **Event counts:** {json.dumps(event_counts)}\n")
        report_lines.append(f"- **Status:** {'PASS' if final_complete else 'FAIL'}\n")

        test_num_holder = [test_num + 1]
        if final_complete:
            global passed
            passed += 1
        else:
            global failed
            failed += 1
        test_num_holder[0]  # just to use it

        # ---------------------------------------------------------------
        # STATUS POLLING
        # ---------------------------------------------------------------
        section("12. Status Polling + Artifact Retrieval")

        status = test("Get status (with artifacts)", f"/agents/job-hunter/status/{gen.job_id}",
                      "GET", {"include": "logs,artifacts"},
                      lambda: client.agents.get_status("job-hunter", gen.job_id, include="logs,artifacts"))

        # ---------------------------------------------------------------
        # ARTIFACT RETRIEVAL
        # ---------------------------------------------------------------
        if final_complete and final_complete.artifacts:
            report_lines.append(f"\n### Artifacts from generation\n")
            report_lines.append(f"- **Count:** {len(final_complete.artifacts)}\n")
            report_lines.append("- **Details:**\n\n```json\n")
            for i, artifact in enumerate(final_complete.artifacts):
                art_str = json.dumps(artifact, indent=2, default=str)
                if len(art_str) > 1500:
                    art_str = art_str[:1500] + "\n  ... (truncated)"
                report_lines.append(f"Artifact {i+1}:\n{art_str}\n\n")
            report_lines.append("```\n")

        # ---------------------------------------------------------------
        # SESSION HYDRATE (with generation data)
        # ---------------------------------------------------------------
        hydration = test("Hydrate generation session",
                         f"/sessions/{gen.session_id}/hydrate", "GET", None,
                         lambda: client.sessions.hydrate(gen.session_id))

        if hydration:
            report_lines.append(f"\n**Hydration details:**\n")
            report_lines.append(f"- Artifacts: {len(hydration.artifacts)}\n")
            report_lines.append(f"- Generation logs: {len(hydration.generation_logs)}\n")
            report_lines.append(f"- CV versions: {len(hydration.cv_versions)}\n")
            report_lines.append(f"- Cover letter versions: {len(hydration.cover_letter_versions)}\n")
            report_lines.append(f"- Cold email versions: {len(hydration.cold_email_versions)}\n")
            report_lines.append(f"- ATS versions: {len(hydration.ats_versions)}\n")

        # ---------------------------------------------------------------
        # DOWNLOAD ARTIFACTS
        # ---------------------------------------------------------------
        if hydration and hydration.artifacts:
            section("13. Artifact Download")
            for i, art in enumerate(hydration.artifacts[:5]):
                if isinstance(art, dict):
                    key = art.get("storageKey") or art.get("key") or art.get("path", "")
                    art_type = art.get("type", "unknown")
                    if key:
                        dl = test(f"Download artifact ({art_type})",
                                  f"/sessions/{gen.session_id}/download?key={key}", "GET",
                                  {"key": key},
                                  lambda k=key: client.sessions.download(gen.session_id, k))
                        if dl:
                            size = len(dl) if isinstance(dl, (bytes, str)) else 0
                            report_lines.append(f"- **Size:** {size} bytes\n")
                            if isinstance(dl, bytes) and size > 0:
                                report_lines.append(f"- **First 200 bytes:** `{dl[:200]}`\n")

        # ---------------------------------------------------------------
        # CONTENT
        # ---------------------------------------------------------------
        section("14. Content Endpoints")

        test("Delete generation", f"/content/generations/{gen.generation_id}",
             "DELETE", {"sessionId": gen.session_id},
             lambda: client.content.delete_generation(gen.generation_id, session_id=gen.session_id))

        # Cleanup
        try:
            client.sessions.delete(gen.session_id)
            report_lines.append(f"\n> Cleaned up session {gen.session_id}\n")
        except Exception:
            pass

    # ===================================================================
    # DOCUMENTS
    # ===================================================================
    section("15. Documents Endpoint")
    test("Download (invalid path raises FORBIDDEN)", "/documents/download", "GET",
         {"path": "nonexistent"},
         lambda: client.documents.download("nonexistent"),
         expect_error="FORBIDDEN")

    # ===================================================================
    # LOGGING
    # ===================================================================
    section("16. Logging Endpoint")
    # Valid log: only level + message (extra fields rejected by strict schema)
    log_input = {"level": "info", "message": "SDK E2E test log"}
    test("Send log", "/log", "POST", log_input,
         lambda: client.logging.send(log_input))

    # Test that invalid schema is correctly caught
    bad_log = {"level": "info", "message": "test", "context": "extra_field"}
    test("Send log (invalid extra field raises VALIDATION_ERROR)", "/log", "POST",
         bad_log,
         lambda: client.logging.send(bad_log),
         expect_error="VALIDATION_ERROR")

    # ===================================================================
    # AUTH (API keys are explicitly forbidden — session auth only)
    # ===================================================================
    section("17. Auth Endpoints")
    test("Export data (API key raises FORBIDDEN — session auth required)",
         "/auth/export", "GET", None,
         lambda: client.auth.export_data(),
         expect_error="FORBIDDEN")

    # ===================================================================
    # SUMMARY
    # ===================================================================
    total = passed + failed + skipped
    report_lines.insert(4, f"\n## Summary\n\n")
    report_lines.insert(5, f"| Metric | Value |\n|--------|-------|\n")
    report_lines.insert(6, f"| Total tests | {total} |\n")
    report_lines.insert(7, f"| Passed | {passed} |\n")
    report_lines.insert(8, f"| Failed | {failed} |\n")
    report_lines.insert(9, f"| Skipped | {skipped} |\n")
    report_lines.insert(10, f"| Pass rate | {passed/total*100:.0f}% |\n\n")

    print(f"\n{'='*60}")
    print(f"  TOTAL: {passed} PASS / {failed} FAIL / {skipped} SKIP ({total} tests)")
    print(f"{'='*60}")

    # Write report
    report_path = Path(__file__).parent.parent / "E2E_TEST_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\nReport: {report_path}")
    client.close()
    return failed


if __name__ == "__main__":
    sys.exit(main())
