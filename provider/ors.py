# Still waiting on PHP issues to be resolved for ORS. Using Mapbox skeleton for the time being.
from base import BaseProvider
import config
import utils
import requests

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


class ORSProvider(BaseProvider):
    """Platform object for geo-related lookups"""

    def __init__(self, provider):
        super().__init__()

    def get_address_content(self, search_text: str) -> dict:
        """Get the address' information from arbitrary provider
    
        Args:
            search_text: Address to search for
    
        Returns:
            Description of return value
    
        Raises:
            ExceptionType: When this exception is raised
        """
        url = self.get_formatted_url(search_text)
        response = requests.get(url)
        primary_feature = response.json().get("features")[0]
    
        property_context = utils.get_in(primary_feature, ["properties", "context"])
        property_coordinates = utils.get_in(primary_feature, ["properties", "coordinates"])
    
        return {
            "coordinates": {
                "accuracy": property_coordinates.get("accuracy"),
                "latitude": property_coordinates.get("latitude"),
                "longitude": property_coordinates.get("longitude"),
            },
            "address": {
                "number": utils.get_in(property_context, ["address", "address_number"]),
                "street_name": utils.get_in(property_context, ["address", "street_name"]),
                "county": utils.get_in(property_context, ["place", "name"]),
                "state": utils.get_in(property_context, ["region", "name"]),
                "state_code": utils.get_in(property_context, ["region", "region_code"]),
                "country": utils.get_in(property_context, ["country", "name"]),
                "zip": utils.get_in(property_context, ["postcode", "name"]),
            },
        }
