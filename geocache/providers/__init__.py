from .mapbox import MapboxProvider
from .ors import OrsProvider

_REGISTRY = {
    "mapbox": MapboxProvider,
    "ors": OrsProvider,
}


def get_provider(provider_configuration_id: str):
    try:
        provider_cls = _REGISTRY[provider_configuration_id]
    except KeyError:
        raise ValueError(f"Unknown provider: {provider_configuration_id!r}")
    return provider_cls()
