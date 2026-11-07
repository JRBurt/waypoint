from mapbox import MapboxProvider
from ors import ORSProvider

def get_provider(provider_configuration_id):
    if provider_configuration_id=='mapbox':
        provider = MapboxProvider()
    elif provider_configuration_id=='ors':
        provider = ORSProvider()
    return provider