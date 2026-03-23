"""B2B Sales agent — generate and poll for results."""

from llmconveyors import LLMConveyors

client = LLMConveyors()  # reads LLMCONVEYORS_API_KEY env var

# Start generation
gen = client.agents.generate("b2b-sales", {
    "companyName": "Target Corp",
    "companyWebsite": "https://target.com",
    "skipResearchCache": False,
})
print(f"Job started: {gen.job_id}")
print(f"Stream URL: {gen.stream_url}")

# Poll for completion
status = client.agents.poll("b2b-sales", gen.job_id, include="artifacts")
print(f"Status: {status.status}")

if status.status == "completed" and status.artifacts:
    print(f"Artifacts: {len(status.artifacts)}")
    for artifact in status.artifacts:
        print(f"  - {artifact.get('type', 'unknown')}")

# Hydrate the session for full data
hydration = client.sessions.hydrate(gen.session_id)
print(f"Generation logs: {len(hydration.generation_logs)}")
