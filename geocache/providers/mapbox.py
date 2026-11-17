from .base import BaseProvider
from geocache import utils


class MapboxProvider(BaseProvider):

    def __init__(self):
        super().__init__("mapbox")

    def get_formatted_url(self, search_text: str) -> str:
        return f"{self.base_url}?q={search_text}&access_token={self.access_token}"

    def parse_response(self, payload: dict) -> dict:
        primary_feature = payload.get("features")[0]
        context = utils.get_in(primary_feature, ["properties", "context"])
        coordinates = utils.get_in(primary_feature, ["properties", "coordinates"])

        return {
            "coordinates": {
                "accuracy": coordinates.get("accuracy"),
                "latitude": coordinates.get("latitude"),
                "longitude": coordinates.get("longitude"),
            },
            "address": {
                "number": utils.get_in(context, ["address", "address_number"]),
                "street_name": utils.get_in(context, ["address", "street_name"]),
                "county": utils.get_in(context, ["place", "name"]),
                "state": utils.get_in(context, ["region", "name"]),
                "state_code": utils.get_in(context, ["region", "region_code"]),
                "country": utils.get_in(context, ["country", "name"]),
                "zip": utils.get_in(context, ["postcode", "name"]),
            },
        }
