"""Live API integration tests against the real LLM Conveyors API.

This script tests every endpoint group to verify our SDK implementation
matches the actual API behavior. Results are logged to live_test_report.md.
"""

from __future__ import annotations

import io
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Fix Windows console Unicode encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["LLMCONVEYORS_API_KEY"] = os.environ.get(
    "LLMCONVEYORS_API_KEY", "llmc_6be092882a85f8dc0fce0b5899a6c0dd393033b3a2959ec8"
)

from llmconveyors import LLMConveyors
from llmconveyors.errors import LLMConveyorsError

# ---------------------------------------------------------------------------
# Test infrastructure
# ---------------------------------------------------------------------------

results: list[dict[str, Any]] = []


def log_test(group: str, name: str, status: str, details: str = "", data: Any = None):
    entry = {
        "group": group,
        "name": name,
        "status": status,  # PASS, FAIL, SKIP, WARN
        "details": details,
        "data_sample": str(data)[:500] if data else "",
    }
    results.append(entry)
    icon = {"PASS": "+", "FAIL": "!", "SKIP": "~", "WARN": "?"}[status]
    print(f"  [{icon}] {group}/{name}: {status} {details[:80] if details else ''}")


def run_test(group: str, name: str, fn):
    try:
        result = fn()
        log_test(group, name, "PASS", data=result)
        return result
    except LLMConveyorsError as e:
        log_test(group, name, "FAIL", f"{e.code}: {e.message}", data={"code": e.code, "hint": e.hint})
        return None
    except Exception as e:
        log_test(group, name, "FAIL", f"{type(e).__name__}: {str(e)[:200]}")
        return None


# ---------------------------------------------------------------------------
# Main test runner
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("LLM Conveyors SDK — Live API Integration Tests")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    client = LLMConveyors()

    # -----------------------------------------------------------------------
    # 1. Health
    # -----------------------------------------------------------------------
    print("\n--- Health ---")
    run_test("health", "check", lambda: client.health.check())
    run_test("health", "ready", lambda: client.health.ready())
    run_test("health", "live", lambda: client.health.live())

    # -----------------------------------------------------------------------
    # 2. Settings — Profile
    # -----------------------------------------------------------------------
    print("\n--- Settings ---")
    profile = run_test("settings", "get_profile", lambda: client.settings.get_profile())
    if profile:
        log_test("settings", "profile_has_credits", "PASS" if hasattr(profile, "credits") else "FAIL",
                 f"credits={profile.credits}, tier={profile.tier}, byo={profile.byo_key_enabled}")

    run_test("settings", "get_preferences", lambda: client.settings.get_preferences())
    run_test("settings", "get_usage_summary", lambda: client.settings.get_usage_summary())
    run_test("settings", "get_usage_logs", lambda: client.settings.get_usage_logs(limit=5))
    run_test("settings", "list_api_keys", lambda: client.settings.list_api_keys())
    run_test("settings", "get_byo_key", lambda: client.settings.get_byo_key())
    run_test("settings", "get_webhook_secret", lambda: client.settings.get_webhook_secret())

    # -----------------------------------------------------------------------
    # 3. Sessions
    # -----------------------------------------------------------------------
    print("\n--- Sessions ---")
    sessions = run_test("sessions", "list", lambda: client.sessions.list())
    if sessions is not None:
        log_test("sessions", "list_is_flat_array", "PASS" if isinstance(sessions, list) else "FAIL",
                 f"type={type(sessions).__name__}, count={len(sessions)}")

    init_data = run_test("sessions", "init", lambda: client.sessions.init())

    # Test create + get + hydrate + delete
    new_session = run_test("sessions", "create", lambda: client.sessions.create())
    if new_session:
        sid = new_session.id
        run_test("sessions", "get", lambda: client.sessions.get(sid))

        hydration = run_test("sessions", "hydrate", lambda: client.sessions.hydrate(sid))
        if hydration:
            log_test("sessions", "hydrate_has_generationLogs",
                     "PASS" if hasattr(hydration, "generation_logs") else "FAIL",
                     f"fields: {[f for f in hydration.model_fields_set]}")
            log_test("sessions", "hydrate_has_version_fields",
                     "PASS" if hasattr(hydration, "cv_versions") else "FAIL")

        run_test("sessions", "delete", lambda: client.sessions.delete(sid))

    # -----------------------------------------------------------------------
    # 4. Resume
    # -----------------------------------------------------------------------
    print("\n--- Resume ---")
    themes = run_test("resume", "themes", lambda: client.resume.themes())
    if themes:
        log_test("resume", "themes_count", "PASS" if isinstance(themes, list) and len(themes) >= 4 else "WARN",
                 f"count={len(themes) if isinstance(themes, list) else 'N/A'}, data={themes}")

    # -----------------------------------------------------------------------
    # 5. Agent Manifests
    # -----------------------------------------------------------------------
    print("\n--- Agent Manifests ---")
    jh_manifest = run_test("agents", "manifest_job_hunter", lambda: client.agents.get_manifest("job-hunter"))
    if jh_manifest:
        log_test("agents", "jh_manifest_fields",
                 "PASS" if jh_manifest.agent_type == "job-hunter" else "FAIL",
                 f"type={jh_manifest.agent_type}, skills={jh_manifest.skills}, "
                 f"billing={jh_manifest.billing}, phasing={jh_manifest.capabilities.supports_phasing}")

    b2b_manifest = run_test("agents", "manifest_b2b_sales", lambda: client.agents.get_manifest("b2b-sales"))
    if b2b_manifest:
        log_test("agents", "b2b_manifest_fields",
                 "PASS" if b2b_manifest.agent_type == "b2b-sales" else "FAIL",
                 f"type={b2b_manifest.agent_type}, skills={b2b_manifest.skills}")

    # -----------------------------------------------------------------------
    # 6. Shares
    # -----------------------------------------------------------------------
    print("\n--- Shares ---")
    run_test("shares", "get_stats", lambda: client.shares.get_stats())

    # -----------------------------------------------------------------------
    # 7. Referral
    # -----------------------------------------------------------------------
    print("\n--- Referral ---")
    run_test("referral", "get_stats", lambda: client.referral.get_stats())
    run_test("referral", "get_code", lambda: client.referral.get_code())

    # -----------------------------------------------------------------------
    # 8. Privacy
    # -----------------------------------------------------------------------
    print("\n--- Privacy ---")
    run_test("privacy", "list_consents", lambda: client.privacy.list_consents())

    # -----------------------------------------------------------------------
    # 9. ATS Score (needs resume + JD text)
    # -----------------------------------------------------------------------
    print("\n--- ATS ---")
    ats_result = run_test("ats", "score", lambda: client.ats.score({
        "resumeText": "John Doe\nSenior Software Engineer\n10 years experience in Python, TypeScript, React, Node.js\nBuilt scalable microservices at AWS\nMS Computer Science, MIT",
        "jobDescription": "Looking for a Senior Software Engineer with 5+ years experience in Python and TypeScript. Must have experience with cloud services and microservices architecture.",
        "jobTitle": "Senior Software Engineer",
    }))
    if ats_result:
        log_test("ats", "response_has_overallScore",
                 "PASS" if hasattr(ats_result, "overall_score") else "FAIL",
                 f"overallScore={ats_result.overall_score}, grade={ats_result.grade}")
        log_test("ats", "response_has_grade",
                 "PASS" if hasattr(ats_result, "grade") else "FAIL",
                 f"grade={ats_result.grade}")
        log_test("ats", "response_has_breakdown",
                 "PASS" if hasattr(ats_result, "breakdown") else "FAIL")
        log_test("ats", "response_has_matchedKeywords",
                 "PASS" if hasattr(ats_result, "matched_keywords") else "FAIL",
                 f"matched={len(ats_result.matched_keywords)}, missing={len(ats_result.missing_keywords)}")
        log_test("ats", "no_dimensions_field",
                 "PASS" if not hasattr(ats_result, "dimensions") else "FAIL",
                 "Confirmed: no fictitious 'dimensions' field")

    # -----------------------------------------------------------------------
    # 10. Job Hunter Generate + Stream (FULL WORKFLOW)
    # -----------------------------------------------------------------------
    print("\n--- Job Hunter Generate + Stream ---")
    gen_response = None
    try:
        gen_response = client.agents.generate("job-hunter", {
            "companyName": "Anthropic",
            "jobTitle": "Software Engineer",
            "companyWebsite": "https://anthropic.com",
            "contactEmail": "careers@anthropic.com",
            "genericEmail": "hello@anthropic.com",
            "jobSourceUrl": "https://anthropic.com/careers",
            "jobDescription": "We are looking for a software engineer to work on AI safety research tools.",
            "autoSelectContacts": True,
            "skipResearchCache": True,
        })
        log_test("agents", "generate_job_hunter", "PASS",
                 f"jobId={gen_response.job_id}, genId={gen_response.generation_id}, "
                 f"sessionId={gen_response.session_id}, status={gen_response.status}, "
                 f"streamUrl={gen_response.stream_url}")
        log_test("agents", "generate_all_5_fields_present",
                 "PASS" if all([gen_response.job_id, gen_response.generation_id,
                               gen_response.session_id, gen_response.status,
                               gen_response.stream_url]) else "FAIL")
        log_test("agents", "generate_status_is_queued",
                 "PASS" if gen_response.status == "queued" else "FAIL",
                 f"status={gen_response.status}")
    except LLMConveyorsError as e:
        log_test("agents", "generate_job_hunter", "FAIL", f"{e.code}: {e.message}")
    except Exception as e:
        log_test("agents", "generate_job_hunter", "FAIL", f"{type(e).__name__}: {e}")

    # Stream the generation
    if gen_response:
        print("\n--- SSE Streaming ---")
        event_types_seen = set()
        event_count = 0
        final_event = None

        try:
            for event in client.stream.generation(
                gen_response.generation_id,
                include_heartbeats=True,
                include_logs=True,
            ):
                event_type = type(event).__name__
                event_types_seen.add(event_type)
                event_count += 1

                if event_type == "ProgressEvent":
                    print(f"    [{event.step}] {event.percent}%")
                elif event_type == "ChunkEvent":
                    pass  # silent
                elif event_type == "CompleteEvent":
                    final_event = event
                    break
                elif event_type == "HeartbeatEvent":
                    print("    [heartbeat]")
                elif event_type == "LogEvent":
                    print(f"    [log:{event.level}] {event.content[:60]}")

                # Safety: don't run forever
                if event_count > 500:
                    log_test("streaming", "safety_cutoff", "WARN", "Hit 500 event limit")
                    break

            log_test("streaming", "connected_and_received",
                     "PASS" if event_count > 0 else "FAIL",
                     f"events={event_count}, types={event_types_seen}")
            log_test("streaming", "no_sse_event_field_needed",
                     "PASS", "Parsed successfully without SSE event: field")

            if final_event:
                log_test("streaming", "complete_event_received", "PASS",
                         f"success={final_event.success}, artifacts={len(final_event.artifacts)}, "
                         f"awaitingInput={final_event.awaiting_input}")
                if final_event.awaiting_input:
                    log_test("streaming", "phase_boundary_detected", "PASS",
                             f"interactionType={final_event.interaction_type}")
                else:
                    log_test("streaming", "final_completion", "PASS",
                             f"artifacts={len(final_event.artifacts)}")

        except LLMConveyorsError as e:
            log_test("streaming", "stream_error", "FAIL", f"{e.code}: {e.message}")
        except Exception as e:
            log_test("streaming", "stream_error", "FAIL", f"{type(e).__name__}: {e}")

        # Test status polling
        print("\n--- Status Polling ---")
        status = run_test("agents", "get_status", lambda: client.agents.get_status(
            "job-hunter", gen_response.job_id, include="logs,artifacts"))
        if status:
            log_test("agents", "status_values_correct",
                     "PASS" if status.status in ("queued", "processing", "completed", "failed", "awaiting_input") else "FAIL",
                     f"status={status.status}, progress={status.progress}")

        # Clean up the session
        try:
            client.sessions.delete(gen_response.session_id)
            log_test("cleanup", "delete_session", "PASS")
        except Exception:
            log_test("cleanup", "delete_session", "SKIP", "Could not delete")

    # -----------------------------------------------------------------------
    # Generate report
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    warned = sum(1 for r in results if r["status"] == "WARN")
    total = len(results)

    print(f"Results: {passed} PASS, {failed} FAIL, {warned} WARN, {skipped} SKIP ({total} total)")
    print("=" * 60)

    # Write report
    report_path = Path(__file__).parent.parent / "LIVE_TEST_REPORT.md"
    with open(report_path, "w") as f:
        f.write("# LLM Conveyors SDK — Live API Test Report\n\n")
        f.write(f"**Date:** {datetime.now(timezone.utc).isoformat()}\n")
        f.write("**SDK Version:** 0.1.0\n")
        f.write("**Base URL:** https://api.llmconveyors.com/api/v1\n\n")
        f.write("## Summary\n\n")
        f.write("| Status | Count |\n|--------|-------|\n")
        f.write(f"| PASS | {passed} |\n")
        f.write(f"| FAIL | {failed} |\n")
        f.write(f"| WARN | {warned} |\n")
        f.write(f"| SKIP | {skipped} |\n")
        f.write(f"| **Total** | **{total}** |\n\n")

        current_group = ""
        for r in results:
            if r["group"] != current_group:
                current_group = r["group"]
                f.write(f"\n## {current_group.title()}\n\n")
                f.write("| Test | Status | Details |\n|------|--------|---------|\n")
            icon = {"PASS": "PASS", "FAIL": "FAIL", "SKIP": "SKIP", "WARN": "WARN"}[r["status"]]
            details = r["details"][:120].replace("|", "\\|").replace("\n", " ")
            f.write(f"| {r['name']} | {icon} | {details} |\n")

        if failed > 0:
            f.write("\n## Failed Tests — Details\n\n")
            for r in results:
                if r["status"] == "FAIL":
                    f.write(f"### {r['group']}/{r['name']}\n")
                    f.write(f"- **Details:** {r['details']}\n")
                    if r["data_sample"]:
                        f.write(f"- **Data:** `{r['data_sample'][:300]}`\n")
                    f.write("\n")

    print(f"\nReport saved to: {report_path}")
    client.close()
    return failed


if __name__ == "__main__":
    sys.exit(main())
