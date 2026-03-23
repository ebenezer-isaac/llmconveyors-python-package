"""Manual SSE streaming — raw event-by-event processing."""

import json

import httpx

API_KEY = "llmc_your_key_here"
BASE_URL = "https://api.llmconveyors.com/api/v1"


def stream_generation(generation_id: str):
    """Parse SSE stream manually.

    The server sends ONLY id: + data: lines. There is NO SSE event: field.
    The event type is INSIDE the JSON: {"event":"progress","data":{...}}
    """
    with httpx.stream(
        "GET",
        f"{BASE_URL}/stream/generation/{generation_id}",
        headers={"X-API-Key": API_KEY},
        timeout=45.0,
    ) as response:
        for line in response.iter_lines():
            if not line or not line.startswith("data:"):
                continue

            raw = line[5:].strip()
            if not raw:
                continue

            event = json.loads(raw)
            event_type = event["event"]
            data = event.get("data", {})

            if event_type == "progress":
                print(f"[{data['step']}] {data['percent']}%")
            elif event_type == "chunk":
                print(data["chunk"], end="", flush=True)
            elif event_type == "complete":
                if data.get("awaitingInput"):
                    print(f"\nAwaiting input: {data['interactionType']}")
                else:
                    print(f"\nDone: {len(data.get('artifacts', []))} artifacts")
                return data
            elif event_type == "error":
                raise Exception(f"[{data['code']}] {data['message']}")
            elif event_type == "log":
                print(f"  LOG [{data['level']}]: {data['content']}")


# Usage:
# 1. Start a generation via POST /agents/job-hunter/generate
# 2. Get the generationId from the response
# 3. stream_generation(generation_id)
