import hashlib

from geocache import config
from geocache import utils

validation_schema = {
    "coordinates": {
        "accuracy": str,
        "latitude": float,
        "longitude": float,
    },
    "address": {
        "number": str,
        "street_name": str,
        "county": str,
        "state": str,
        "state_code": str,
        "country": str,
        "zip": str,
    },
}


class BaseProvider:
    """Shared config-loading and key-derivation for a geocoding provider.

    Subclasses call super().__init__(provider_configuration_id) and only
    override what's genuinely provider-specific: get_formatted_url and
    parse_response.
    """

    response_schema = validation_schema

    def __init__(self, provider_configuration_id: str):
        self.provider_config = config.providers.get(provider_configuration_id, {})
        self.name = self.provider_config.get("name")
        self.provider_configuration_id = provider_configuration_id
        self.ttl_seconds = self.provider_config.get("ttl_seconds")
        self.base_url = self.provider_config.get("base_url")
        self.access_token = self.provider_config.get("access_token")
        self.rate_limit = self.provider_config.get("rate_limit")

    def get_formatted_url(self, search_text: str) -> str:
        raise NotImplementedError

    def parse_response(self, payload: dict) -> dict:
        raise NotImplementedError

    def get_address_content(self, search_text: str) -> dict:
        import requests

        url = self.get_formatted_url(search_text)
        response = requests.get(url)
        response.raise_for_status()
        return self.parse_response(response.json())

    def get_entity_key(self, search_text: str) -> str:
        """Hash of the standardized request, namespaced by provider."""
        m = hashlib.sha256()
        m.update(utils.slugify(search_text).encode())
        return ":".join(["geocode", self.provider_configuration_id, m.hexdigest()[:8]])
