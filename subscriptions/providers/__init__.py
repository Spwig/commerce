"""
Subscription Providers Package

All subscription providers are now component-based and auto-discovered
from their respective payment provider component directories
(components_data/integrations/payments/{slug}/current/subscription_provider.py).

The auto-discovery mechanism in provider_base._discover_component_providers()
scans ComponentRegistry for payment_provider components and dynamically imports
any subscription_provider.py modules found, triggering @register_provider
decorator registration.
"""

# Import from parent provider_base module
from subscriptions.provider_base import (
    FallbackSubscriptionProvider,
    SubscriptionProviderBase,
    get_provider,
    is_subscription_supported,
    register_provider,
)

__all__ = [
    "SubscriptionProviderBase",
    "FallbackSubscriptionProvider",
    "register_provider",
    "get_provider",
    "is_subscription_supported",
]
