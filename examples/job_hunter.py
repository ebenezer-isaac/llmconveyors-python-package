"""Job Hunter agent — full workflow with streaming and phased interaction."""

from llmconveyors import LLMConveyors

client = LLMConveyors()  # reads LLMCONVEYORS_API_KEY env var


def on_progress(event):
    print(f"[{event.step}] {event.percent}%")


def on_chunk(event):
    print(event.chunk, end="", flush=True)


def interaction_handler(interaction_type, interaction_data):
    """Handle contact selection for phased execution."""
    print(f"\nAwaiting input: {interaction_type}")
    candidates = interaction_data.get("candidates", [])
    for i, c in enumerate(candidates):
        print(f"  {i}: {c.get('name', 'Unknown')} - {c.get('title', '')}")

    # Auto-select recommended target
    return {
        "selectedTargetId": interaction_data.get("recommendedTargetId"),
        "selectedCcId": interaction_data.get("recommendedCcId"),
    }


result = client.agents.run(
    "job-hunter",
    {
        "companyName": "Acme Corp",
        "jobTitle": "Senior Engineer",
        "companyWebsite": "https://acme.com",
        "contactEmail": "hiring@acme.com",
        "genericEmail": "info@acme.com",
        "jobSourceUrl": "https://acme.com/careers/senior-engineer",
        "jobDescription": "We are looking for a senior engineer...",
    },
    on_progress=on_progress,
    on_chunk=on_chunk,
    interaction_handler=interaction_handler,
)

print(f"\nSuccess: {result.success}")
print(f"Artifacts: {len(result.artifacts)}")
for artifact in result.artifacts:
    print(f"  - {artifact.get('type', 'unknown')}")
