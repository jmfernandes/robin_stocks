"""
Configuration for recurring investments example scripts.

This file contains rate limiting and retry settings for the recurring investments
example scripts. The core robin_stocks library now supports built-in rate limiting
via enable_rate_limiting(), which this config uses.
"""

# Core rate limiting (uses robin_stocks built-in rate limiting)
# Set to True to enable automatic rate limiting in all API calls
ENABLE_CORE_RATE_LIMITING = True
CORE_RATE_LIMIT_DELAY = 5.0  # Seconds between API calls (conservative for safety)

# Retry logic settings (for handling rate limit errors and server errors)
MAX_RETRIES = 3  # Maximum retry attempts for rate-limited requests
INITIAL_RETRY_DELAY = 10  # Initial retry delay (seconds) - exponential backoff starts here

# API timeout settings
API_TIMEOUT = 30  # Seconds to wait for API response

# Rate limit error codes that should trigger retry
RETRYABLE_ERROR_CODES = ['429', '502', '503', '504']  # Rate limit, Bad Gateway, Service Unavailable, Gateway Timeout

# Legacy setting for backward compatibility (used by scripts that haven't migrated yet)
DELAY_BETWEEN_REQUESTS = CORE_RATE_LIMIT_DELAY

