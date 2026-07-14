"""
SMS Provider Registry.

Provides access to SMS provider implementations.
Uses component-based provider discovery from components_data/integrations/sms/
"""

from .base import SMSProviderBase
from .loader import SMSProviderLoader
from .registry import SMSProviderRegistry


def get_provider_class(provider_key: str):
    """
    Get provider class for a given key.

    Uses the component-based registry to discover providers.

    Args:
        provider_key: Provider identifier (e.g., 'twilio', 'twilio_whatsapp')

    Returns:
        Provider class or None if not found
    """
    return SMSProviderRegistry.get_provider_class(provider_key)


def get_provider_choices():
    """
    Get choices tuple for provider selection fields.

    Returns:
        List of tuples: [(provider_key, provider_name), ...]
    """
    providers = SMSProviderRegistry.list_providers()
    return [(p["key"], p["name"]) for p in providers]


__all__ = [
    "SMSProviderBase",
    "SMSProviderLoader",
    "SMSProviderRegistry",
    "get_provider_class",
    "get_provider_choices",
]
