"""
python -m server

GET /geocode?provider=mapbox&q=900+Washington+Ave,+Golden,+CO
GET /geocode?provider=mapbox&q=...&skip_cache=1   (force a fresh provider call)
GET /route?...   (not implemented - placeholder for the routing endpoint)

ThreadingHTTPServer, not plain HTTPServer: a single-threaded server would
serialize every request, which would silently defeat any test meant to
exercise the stampede lock under real concurrency.
"""

import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

import redis

import cache
import config
import providers
import ratelimit

logger = logging.getLogger(__name__)

redis_client = redis.Redis(**config.redis_config)
rate_limiter = ratelimit.RateLimiter(redis_client)
cache_aside = cache.CacheAside(redis_client, rate_limiter)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/geocode":
            self._handle_geocode(params)
        elif parsed.path == "/route":
            self._respond(501, {"error": "not implemented"})
        else:
            self._respond(404, {"error": "not found"})

    def _handle_geocode(self, params):
        provider_id = params.get("provider", [None])[0]
        search_text = params.get("q", [None])[0]
        skip_cache = params.get("skip_cache", ["0"])[0].lower() in ("1", "true", "yes")

        if not provider_id or not search_text:
            self._respond(400, {"error": "provider and q are required"})
            return

        try:
            provider = providers.get_provider(provider_id)
        except ValueError as e:
            self._respond(400, {"error": str(e)})
            return

        try:
            result = cache_aside.maybe_update_and_get(provider, search_text, skip_cache)
        except ratelimit.RateLimitExceeded as e:
            self._respond(429, {"error": str(e)})
            return

        self._respond(200, result)

    def _respond(self, status: int, body: dict):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        logger.info("%s - %s", self.address_string(), fmt % args)


def main():
    server = ThreadingHTTPServer(("0.0.0.0", 8080), Handler)
    logger.info("waypoint listening on http://localhost:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()
