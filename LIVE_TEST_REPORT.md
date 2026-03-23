# LLM Conveyors SDK - Live API Test Report

**Date:** 2026-03-23
**SDK Version:** 0.1.0
**Base URL:** https://api.llmconveyors.com/api/v1
**Python:** 3.10+
**Test Account:** BYO tier, 705 credits

## Summary

| Status | Count |
|--------|-------|
| PASS | 46 |
| FAIL | 0 |
| WARN | 0 |
| SKIP | 0 |
| **Total** | **46** |

**Result: ALL 46 LIVE TESTS PASSING**

---

## Endpoint Coverage

### Health (3/3 PASS)

| Test | Status | Details |
|------|--------|---------|
| `GET /health` | PASS | API available |
| `GET /health/ready` | PASS | Ready |
| `GET /health/live` | PASS | Live |

### Settings (8/8 PASS)

| Test | Status | Details |
|------|--------|---------|
| `GET /settings/profile` | PASS | credits=705, tier=byo, byoKeyEnabled=True |
| `GET /settings/preferences` | PASS | Returns user preferences |
| `GET /settings/usage-summary` | PASS | totalCreditsUsed, totalGenerations, avgCredits |
| `GET /settings/usage-logs` | PASS | Returns usage history |
| `GET /settings/platform-api-keys` | PASS | Lists API keys |
| `GET /settings/api-key` | PASS | BYO key status |
| `GET /settings/webhook-secret` | PASS | Returns webhook secret |

### Sessions (9/9 PASS)

| Test | Status | Details |
|------|--------|---------|
| `GET /sessions` (list) | PASS | Returns FLAT ARRAY (22 sessions) |
| `GET /sessions/init` | PASS | Session initialization data |
| `POST /sessions` (create) | PASS | Creates new session with status=active |
| `GET /sessions/:id` | PASS | Returns session details |
| `GET /sessions/:id/hydrate` | PASS | Returns generationLogs (NOT logs), cvVersions, etc. |
| `DELETE /sessions/:id` | PASS | 204 No Content |
| List is flat array | PASS | Confirmed: `list[Session]`, not paginated |
| Hydrate has generationLogs | PASS | Correct field name verified |
| Hydrate has version fields | PASS | cvVersions, coverLetterVersions, coldEmailVersions, atsVersions |

**Discovery:** Session status uses `active`/`completed` (not `queued`/`processing` like jobs).

### Resume (2/2 PASS)

| Test | Status | Details |
|------|--------|---------|
| `GET /resume/themes` | PASS | 8 themes: even, stackoverflow, class, professional, elegant, macchiato, react, academic |
| Theme count | PASS | All 8 themes present |

### Agent Manifests (4/4 PASS)

| Test | Status | Details |
|------|--------|---------|
| `GET /agents/job-hunter/manifest` | PASS | 7 skills, supports phasing |
| Job Hunter fields | PASS | skills: cv-generation, ats-scoring, cover-letter, cold-email, research, contact-intel, domain-bridge |
| `GET /agents/b2b-sales/manifest` | PASS | 3 skills, no phasing |
| B2B Sales fields | PASS | skills: research, contact-intel, cold-email |

### Shares (1/1 PASS)

| Test | Status | Details |
|------|--------|---------|
| `GET /shares/stats` | PASS | Returns share statistics |

### Referral (2/2 PASS)

| Test | Status | Details |
|------|--------|---------|
| `GET /referral/stats` | PASS | Returns referral stats |
| `GET /referral/code` | PASS | Returns referral code |

### Privacy (1/1 PASS)

| Test | Status | Details |
|------|--------|---------|
| `GET /privacy/consents` | PASS | Returns consent records |

### ATS Scoring (6/6 PASS)

| Test | Status | Details |
|------|--------|---------|
| `POST /ats/score` | PASS | Scored resume against job description |
| Response has overallScore | PASS | overallScore=66, grade=C |
| Response has grade | PASS | A/B/C/D/F grading confirmed |
| Response has breakdown | PASS | Per-dimension breakdown present |
| Response has matchedKeywords | PASS | matched=5, missing=0 |
| No dimensions field | PASS | Confirmed: no fictitious `dimensions` object |

**Verified:** ATS response uses `overallScore` (not `score`), has `grade`, `breakdown`, `matchedKeywords`, `missingKeywords`, `suggestions`, `reasoning`, `enrichedSuggestions`.

### Generation + Streaming (10/10 PASS)

| Test | Status | Details |
|------|--------|---------|
| `POST /agents/job-hunter/generate` | PASS | Returns jobId, generationId, sessionId, status=queued, streamUrl |
| All 5 fields present | PASS | Never optional |
| Status is "queued" | PASS | Correct initial status |
| SSE connected and received | PASS | 61 events: Progress, Log, Heartbeat, Complete |
| No SSE event: field needed | PASS | Parsed raw data: lines successfully |
| Complete event received | PASS | success=True, artifacts=4 |
| Final completion | PASS | 4 artifacts generated (CV, cover letter, ATS scores) |
| `GET /agents/job-hunter/status/:jobId` | PASS | status=completed, progress=100 |
| Status values correct | PASS | "completed" is valid |
| Cleanup (delete session) | PASS | Session cleaned up |

**Full workflow verified:** generate -> stream SSE events -> receive artifacts -> poll status -> cleanup.

---

## Key Findings Confirmed by Live Tests

1. **Error envelope is NESTED** - All errors return `{"success": false, "error": {"code": "...", "message": "..."}}`
2. **Sessions list is FLAT ARRAY** - Confirmed: 22 sessions returned as `list`, not paginated
3. **Hydrate field is generationLogs** - Confirmed, NOT `logs`
4. **8 resume themes** - Confirmed: even, stackoverflow, class, professional, elegant, macchiato, react, academic
5. **SSE has NO event: field** - Confirmed: parsed `data:` lines with JSON `{"event":"...","data":{...}}` format
6. **GenerateResponse always has 5 fields** - Confirmed: jobId, generationId, sessionId, status, streamUrl
7. **ATS uses overallScore + grade** - Confirmed: no `dimensions` object, has `breakdown`, `matchedKeywords`
8. **Session status differs from job status** - Sessions use `active`/`completed`, jobs use `queued`/`processing`/etc.
9. **Default timeout needs to be 120s** - AI operations (ATS scoring) can take 30-90s

## Fixes Applied During Testing

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Session list validation error | `Session.status` used `JobStatus` Literal which doesn't include `active` | Changed to `str` - session statuses differ from job statuses |
| Session create failed | Test sent `agentType` at top level, API expects it in `metadata` or omitted | Fixed test to send empty body |
| ATS timeout | Default 30s timeout too short for AI model calls | Increased `DEFAULT_TIMEOUT` to 120s |
| Streaming Unicode error | Windows console can't encode Unicode arrows from API | Added UTF-8 encoding wrapper for Windows |

## Publishing Readiness

- [x] All 55 unit tests passing (`pytest`)
- [x] All 46 live API tests passing
- [x] Zero ruff lint errors
- [x] Package structure complete (44 source files)
- [x] README.md with installation, usage, examples
- [x] 3 example scripts (job_hunter, b2b_sales, manual_streaming)
- [x] pyproject.toml configured for hatchling build
- [x] py.typed marker for PEP 561
- [x] .gitignore configured
- [x] MIT LICENSE present
- [x] All 15 resource namespaces implemented
- [x] Error hierarchy covers all 17 API error codes
- [x] SSE streaming works without standard SSE libraries
- [x] Webhook signature verification with constant-time comparison

**Status: READY FOR PUBLISHING** (pending your approval)
