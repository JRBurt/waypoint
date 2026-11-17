"""Cache-aside with TTL, plus stampede protection via a distributed lock.

maybe_update_and_get(provider, search_text, skip_cache=False) is the one
entrypoint. Its branches, in order:

  1. provider.ttl_seconds is None -> this provider's results can't be
     cached at all (e.g. Mapbox's storage terms). Skip Redis entirely,
     call the provider directly, every time. skip_cache is irrelevant
     here - there's nothing to bypass.
  2. skip_cache=True -> skip the initial cache read, go straight to the
     lock-protected fetch-and-refill path. Still goes through the lock,
     so N concurrent skip_cache requests for the same key don't all hit
     the provider at once, and still repopulates the cache with the
     fresh result - the bypass benefits the next normal request too,
     not just this one.
  3. Cache hit -> return it. No provider call, no lock.
  4. Cache miss -> acquire a short-lived lock on this specific key before
     calling the provider, so a hot key expiring under concurrent load
     doesn't cause every waiting request to hit the provider at once.
     Only the lock holder calls the provider and populates the cache;
     everyone else re-checks the cache once the lock is released.
"""

import json

import redis

from geocache import ratelimit


class CacheAside:

    def __init__(
        self, redis_client: redis.Redis, rate_limiter: "ratelimit.RateLimiter"
    ):
        self.redis = redis_client
        self.rate_limiter = rate_limiter

    def maybe_update_and_get(
        self, provider, search_text: str, skip_cache: bool = False
    ) -> dict:
        if provider.ttl_seconds is None:
            self.rate_limiter.check_and_increment(
                provider.provider_configuration_id, provider.rate_limit
            )
            return {
                "data": provider.get_address_content(search_text),
                "meta": {"cache": "DISABLED"},
            }

        entity_key = provider.get_entity_key(search_text)

        if not skip_cache:
            cached = self.redis.get(entity_key)
            if cached:
                return {"data": json.loads(cached), "meta": {"cache": "HIT"}}

        return self._refill(provider, entity_key, search_text, skip_cache)

    def _refill(
        self, provider, entity_key: str, search_text: str, skip_cache: bool
    ) -> dict:
        lock = self.redis.lock(f"lock:{entity_key}", timeout=10, blocking_timeout=5)
        acquired = lock.acquire(blocking=True)
        if not acquired:
            # Someone else is holding the lock past our wait window - rather
            # than pile onto the provider too, check once more for data they
            # may have just written, then give up cleanly.
            cached = self.redis.get(entity_key)
            if cached:
                return {"data": json.loads(cached), "meta": {"cache": "HIT"}}
            raise TimeoutError(f"Timed out waiting for cache fill on {entity_key}")

        try:
            if not skip_cache:
                # Another waiter may have filled it between our first GET
                # and acquiring the lock.
                cached = self.redis.get(entity_key)
                if cached:
                    return {"data": json.loads(cached), "meta": {"cache": "HIT"}}

            self.rate_limiter.check_and_increment(
                provider.provider_configuration_id, provider.rate_limit
            )
            content = provider.get_address_content(search_text)
            self.redis.set(entity_key, json.dumps(content), ex=provider.ttl_seconds)
            return {
                "data": content,
                "meta": {"cache": "BYPASS" if skip_cache else "MISS"},
            }
        finally:
            lock.release()
