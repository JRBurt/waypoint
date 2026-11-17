"""Token-bucket rate limiting, shared across every caller of Waypoint.

Simplified to a fixed-window counter (INCR + EXPIRE) rather than a true
leaky/token bucket - matches what the handoff describes ("budget per
provider... visible across however many clients are calling Waypoint") and
is the smallest thing that gets the shared-state property right. A real
token bucket (continuous refill) would be a reasonable later upgrade if
bursty traffic near the window boundary turns out to matter.
"""

import redis


class RateLimitExceeded(Exception):
    pass


class RateLimiter:

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def check_and_increment(self, provider_configuration_id: str, rate_limit: dict) -> None:
        if not rate_limit:
            return

        budget = rate_limit["budget"]
        window_seconds = rate_limit["window_seconds"]
        key = f"ratelimit:{provider_configuration_id}"

        current = self.redis.incr(key)
        if current == 1:
            self.redis.expire(key, window_seconds)

        if current > budget:
            raise RateLimitExceeded(
                f"{provider_configuration_id} exceeded budget of {budget} "
                f"per {window_seconds}s window"
            )
