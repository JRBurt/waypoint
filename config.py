"""
python -m config
"""
import json
import utils


def get_tokens():
    with open('.configs.json', 'r') as json_configs:
        data = json.load(json_configs)
    mapbox_token = utils.get_in(data, ['mapbox', 'token'])
    ors_token = utils.get_in(data, ['ors', 'token'])


YEAR_IN_DAYS = 365

providers = {
    "mapbox": {
        "name": "Mapbox",
        "provider_configuration_id": "mapbox",
        "ttl_days": 0,
        "base_url": "https://api.mapbox.com/search/geocode/v6/forward",
        "access_token": mapbox_token
    },
    "ors": {
        "name": "OpenRouteService",
        "provider_configuration_id": "ors",
        "ttl_days": 1 * YEAR_IN_DAYS,
        "base_url": "https://api.ors.com/search/geocode/v6/forward", # Get correct url once they're back up.
        "access_token": ors_token
    }
}