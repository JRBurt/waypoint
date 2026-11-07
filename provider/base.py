import config
import utils

validation_schema = {
    "coordinates": {
        "accuracy": str,
        "latitude": float,
        "longitude": float,
    },
    "address": {
        "number": str,  # Ironic, huh.
        "street_name": str,
        "county": str,
        "state": str,
        "state_code": str,
        "country": str,
        "zip": str,  # Supports +4 codes
    },
}


class BaseProvider:
    """Platform object for geo-related lookups"""

    def __init__(self, provider):
        self.provider_config = config.providers.get(provider, {})

        self.name = provider_config.get("name")
        self.provider_configuration_id = provider_config.get(
            "provider_configuration_id"
        )
        self.ttl_days = provider_config.get("ttl_days")
        self.base_url = provider_config.get("base_url")
        self.response_schema = validation_schema

    def request_address(self, search_text):
        raise NotImplementedError("Method not implemented.")

    def get_address_content(self, search_text):
        raise NotImplementedError("Method not implemented.")

    def get_formatted_url(self, search_text: str):
        """Format a request

        Args:
            search_text: Address/Text to search provider

        Returns:
            String, Formatted URL
        """
        return f"{self.base_url}?q={search_text}&access_token={self.access_token}"

    def get_entity_key(self, search_text):
        """Creates a hash of the standardized request and constructs the entity_id"""
        m = hashlib.sha256()
        m.update(utils.slugify(search_text).encode())
        return ":".join(["geocode", self.provider_configuration_id, m.hexdigest()[:8]])
