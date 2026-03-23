# LLM Conveyors Python SDK

Official Python SDK for the [LLM Conveyors](https://llmconveyors.com) AI Agent Platform API.

## Installation

```bash
pip install llmconveyors
```

## Quick Start

```python
from llmconveyors import LLMConveyors

# Uses LLMCONVEYORS_API_KEY env var, or pass api_key= directly
client = LLMConveyors(api_key="llmc_...")

# Generate with streaming
result = client.agents.run(
    "job-hunter",
    {
        "companyName": "Acme Corp",
        "jobTitle": "Senior Engineer",
        "companyWebsite": "https://acme.com",
        "contactEmail": "hiring@acme.com",
        "genericEmail": "info@acme.com",
        "jobSourceUrl": "https://acme.com/careers",
    },
    on_progress=lambda e: print(f"[{e.step}] {e.percent}%"),
)

print(f"Success: {result.success}, Artifacts: {len(result.artifacts)}")
```

## Async Usage

```python
import asyncio
from llmconveyors import AsyncLLMConveyors

async def main():
    async with AsyncLLMConveyors() as client:
        result = await client.agents.run(
            "b2b-sales",
            {
                "companyName": "Target Corp",
                "companyWebsite": "https://target.com",
                "skipResearchCache": False,
            },
        )
        print(result.artifacts)

asyncio.run(main())
```

## Features

- **Sync + Async clients** with identical APIs
- **15 resource namespaces**: agents, stream, sessions, upload, resume, ats, settings, privacy, auth, documents, logging, health, content, shares, referral
- **SSE streaming** via generators (sync) and async generators
- **High-level `run()` method** — generate + stream + interact in one call
- **`poll()` method** for non-streaming environments
- **Typed exceptions** for all 17 API error codes
- **Automatic retry** with exponential backoff and jitter
- **Webhook verification** with HMAC-SHA256 and constant-time comparison
- **Pydantic v2 models** for all request/response types

## Webhook Verification

```python
from llmconveyors import construct_event

event = construct_event(
    payload=request.body,  # raw bytes
    sig_header=request.headers["X-Webhook-Signature"],
    secret="your_webhook_secret",
)
```

## Documentation

- [API Docs](https://llmconveyors.com/docs)
- [SDK Guide](https://llmconveyors.com/docs/sdk)
- [Examples](examples/)

## License

MIT
