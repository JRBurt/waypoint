"""
python -m config
"""

import json
import os
import utils
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

YEAR_IN_DAYS = 365

_HERE = os.path.dirname(os.path.abspath(__file__))
_SECRETS_PATH = os.path.join(_HERE, ".configs.json")

def _load_secrets() -> dict:
    if not os.path.exists(_SECRETS_PATH):
        return {}
    with open(_SECRETS_PATH) as f:
        return json.load(f)


_secrets = _load_secrets()


providers = {
    "mapbox": {
        "name": "Mapbox",
        "provider_configuration_id": "mapbox",
        "base_url": "https://api.mapbox.com/search/geocode/v6/forward",
        "access_token": utils.get_in(_secrets, ["mapbox", "token"]),
        # Mapbox's terms prohibit on-prem storage of results at all.
        # None, not 0 - this is "skip the cache layer entirely", not a TTL value.
        "ttl_seconds": None,
        "rate_limit": {"budget": 100_000, "window_seconds": YEAR_IN_DAYS * 86400 // 12},
    },
    "ors": {
        "name": "OpenRouteService",
        "provider_configuration_id": "ors",
        "base_url": "https://api.ors.com/search/geocode/v6/forward",  # confirm once they're back up
        "access_token": utils.get_in(_secrets, ["ors", "token"]),
        "ttl_seconds": YEAR_IN_DAYS * 86400,
        "rate_limit": {"budget": 2_000, "window_seconds": 86400},
    },
}


redis_config = {
    "host": os.environ.get("REDIS_HOST", "localhost"),
    "port": int(os.environ.get("REDIS_PORT", 6379)),
    "db": 0,
    "decode_responses": True,
}


def main():
    pass


if __name__ == "__main__":
    main()
