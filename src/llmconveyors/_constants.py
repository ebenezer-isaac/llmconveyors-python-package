"""SDK constants and default configuration values."""

from __future__ import annotations

DEFAULT_BASE_URL = "https://api.llmconveyors.com/api/v1"

# Retry configuration
DEFAULT_MAX_RETRIES = 3
DEFAULT_TIMEOUT = 120.0  # seconds (AI operations like ATS scoring can take 30-90s)
RETRY_BASE_DELAY = 1.0  # seconds
RETRY_MAX_DELAY = 30.0  # seconds
RETRY_JITTER_MAX = 0.5  # seconds
CONCURRENT_LIMIT_DELAY = 5.0  # seconds

# SSE streaming configuration
DEFAULT_MAX_RECONNECT_ATTEMPTS = 5
SSE_SERVER_RESTART_MIN_DELAY = 5.0  # seconds
SSE_SERVER_RESTART_MAX_DELAY = 10.0  # seconds
SSE_READ_TIMEOUT = 45.0  # seconds (heartbeat is 15s, so 3x for safety)

# Polling configuration
DEFAULT_POLL_INTERVAL = 2.0  # seconds
DEFAULT_POLL_TIMEOUT = 300.0  # seconds (5 minutes)

# Authentication
API_KEY_PREFIX = "llmc_"
API_KEY_ENV_VAR = "LLMCONVEYORS_API_KEY"
