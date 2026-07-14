"""
Subscription Provider Abstraction Layer
Supports both native provider subscriptions (Stripe, PayPal) and fallback internal billing.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Any

logger = logging.getLogger(__name__)


class SubscriptionProviderBase(ABC):
    """
    Base class for subscription payment providers.
    Defines the interface that all providers must implement.
    """

    def __init__(self, gateway):
        """
        Initialize provider with payment gateway configuration.

        Args:
            gateway: PaymentProviderAccount or legacy gateway instance
        """
        self.gateway = gateway
        # Support both PaymentProviderAccount (credentials_encrypted) and
        # legacy gateway objects (configuration)
        if hasattr(gateway, "configuration"):
            self.config = gateway.configuration
        elif hasattr(gateway, "credentials_encrypted"):
            raw = gateway.credentials_encrypted or {}
            # Decrypt credentials — the encrypted JSONField stores secret
            # values as {'value': '...', 'encrypted': True} dicts.
            from payment_providers.utils.encryption import decrypt_credentials

            try:
                self.config = decrypt_credentials(raw)
            except Exception:
                logger.error("Failed to decrypt provider credentials for %s", gateway)
                raise
        else:
            self.config = {}

    @property
    @abstractmethod
    def capabilities(self) -> dict[str, bool]:
        """
        Return provider capabilities.

        Returns:
            dict: Capabilities dictionary with keys:
                - native_subscriptions: bool - Provider manages subscriptions natively
                - tokenization: bool - Supports payment method tokenization
                - webhooks: bool - Supports webhook notifications
                - trial_periods: bool - Supports trial periods
                - prorated_billing: bool - Supports prorated charges
                - usage_based: bool - Supports usage-based billing
        """
        pass

    # ===========================
    # Customer & Token Management
    # ===========================

    @abstractmethod
    def create_customer(self, user, email: str, metadata: dict | None = None) -> dict[str, Any]:
        """
        Create a customer record in the payment provider.

        Args:
            user: Django User instance
            email: Customer email
            metadata: Optional metadata dictionary

        Returns:
            dict: {'customer_id': str, 'metadata': dict}
        """
        pass

    @abstractmethod
    def create_payment_token(
        self, customer_id: str, payment_method_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Tokenize a payment method for recurring billing.

        Args:
            customer_id: Provider's customer ID
            payment_method_data: Payment method information

        Returns:
            dict: {
                'token_id': str,
                'payment_method_type': str,
                'card_brand': str (optional),
                'card_last4': str (optional),
                'card_exp_month': int (optional),
                'card_exp_year': int (optional),
            }
        """
        pass

    @abstractmethod
    def delete_payment_token(self, token_id: str) -> bool:
        """
        Delete a tokenized payment method.

        Args:
            token_id: Provider's token ID

        Returns:
            bool: True if successful
        """
        pass

    # ===========================
    # Subscription Management (Native Providers)
    # ===========================

    def create_subscription(
        self,
        customer_id: str,
        plan_id: str,
        payment_token_id: str,
        trial_end: datetime | None = None,
        metadata: dict | None = None,
    ) -> dict[str, Any]:
        """
        Create a subscription using provider's native subscription API.
        Only called for providers with native_subscriptions=True.

        Args:
            customer_id: Provider's customer ID
            plan_id: Provider's plan ID
            payment_token_id: Provider's payment token ID
            trial_end: Trial end date (optional)
            metadata: Optional metadata

        Returns:
            dict: {
                'subscription_id': str,
                'status': str,
                'current_period_start': datetime,
                'current_period_end': datetime,
                'next_billing_date': datetime,
            }
        """
        if not self.capabilities["native_subscriptions"]:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not support native subscriptions"
            )
        return {}

    def cancel_subscription(
        self, subscription_id: str, immediately: bool = False
    ) -> dict[str, Any]:
        """
        Cancel a provider-managed subscription.
        Only called for providers with native_subscriptions=True.

        Args:
            subscription_id: Provider's subscription ID
            immediately: If True, cancel immediately; otherwise at period end

        Returns:
            dict: {'status': str, 'canceled_at': datetime}
        """
        if not self.capabilities["native_subscriptions"]:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not support native subscriptions"
            )
        return {}

    def pause_subscription(self, subscription_id: str) -> dict[str, Any]:
        """
        Pause a provider-managed subscription.
        Only called for providers with native_subscriptions=True.

        Args:
            subscription_id: Provider's subscription ID

        Returns:
            dict: {'status': str, 'paused_at': datetime}
        """
        if not self.capabilities["native_subscriptions"]:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not support native subscriptions"
            )
        return {}

    def resume_subscription(self, subscription_id: str) -> dict[str, Any]:
        """
        Resume a paused provider-managed subscription.
        Only called for providers with native_subscriptions=True.

        Args:
            subscription_id: Provider's subscription ID

        Returns:
            dict: {'status': str, 'resumed_at': datetime}
        """
        if not self.capabilities["native_subscriptions"]:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not support native subscriptions"
            )
        return {}

    def update_subscription(
        self,
        subscription_id: str,
        plan_id: str | None = None,
        payment_token_id: str | None = None,
        proration_behavior: str | None = None,
    ) -> dict[str, Any]:
        """
        Update subscription plan or payment method.
        Only called for providers with native_subscriptions=True.

        Args:
            subscription_id: Provider's subscription ID
            plan_id: New plan ID (optional)
            payment_token_id: New payment token ID (optional)
            proration_behavior: Proration handling ('create_prorations', 'none', etc.)

        Returns:
            dict: {'status': str, 'updated_at': datetime}
        """
        if not self.capabilities["native_subscriptions"]:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not support native subscriptions"
            )
        return {}

    # ===========================
    # One-time Charging (Fallback Providers)
    # ===========================

    @abstractmethod
    def charge_payment_token(
        self,
        token_id: str,
        amount: Decimal,
        currency: str,
        description: str,
        metadata: dict | None = None,
    ) -> dict[str, Any]:
        """
        Charge a tokenized payment method (for fallback billing).

        Args:
            token_id: Provider's payment token ID
            amount: Charge amount
            currency: Currency code (USD, EUR, etc.)
            description: Charge description
            metadata: Optional metadata

        Returns:
            dict: {
                'transaction_id': str,
                'status': str,  # 'succeeded', 'failed', 'pending'
                'amount': Decimal,
                'currency': str,
                'error_message': str (if failed),
                'error_code': str (if failed),
            }
        """
        pass

    # ===========================
    # Webhook Handling
    # ===========================

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify webhook signature for security.

        Args:
            payload: Raw webhook payload
            signature: Signature header value

        Returns:
            bool: True if signature is valid
        """
        # Default implementation - providers should override
        return True

    def parse_webhook_event(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Parse webhook payload into standardized event format.

        Args:
            payload: Webhook payload dictionary

        Returns:
            dict: {
                'event_type': str,  # 'subscription.created', 'payment.succeeded', etc.
                'event_id': str,
                'subscription_id': str (optional),
                'customer_id': str (optional),
                'data': dict,
            }
        """
        # Default implementation - providers should override
        return {
            "event_type": "unknown",
            "event_id": "",
            "data": payload,
        }


class FallbackSubscriptionProvider(SubscriptionProviderBase):
    """
    Base class for providers that don't have native subscription support.
    Uses internal Celery-based billing engine.
    """

    @property
    def capabilities(self) -> dict[str, bool]:
        return {
            "native_subscriptions": False,  # Uses fallback engine
            "tokenization": True,
            "webhooks": True,
            "trial_periods": True,  # Handled by internal engine
            "prorated_billing": False,
            "usage_based": False,
        }

    def create_subscription(self, *args, **kwargs):
        """Fallback providers don't create provider-side subscriptions"""
        raise NotImplementedError(
            f"{self.__class__.__name__} uses fallback billing engine. "
            "Subscriptions are managed internally, not by the provider."
        )

    def cancel_subscription(self, *args, **kwargs):
        """Fallback providers don't manage provider-side subscriptions"""
        raise NotImplementedError(f"{self.__class__.__name__} uses fallback billing engine.")

    def pause_subscription(self, *args, **kwargs):
        """Fallback providers don't manage provider-side subscriptions"""
        raise NotImplementedError(f"{self.__class__.__name__} uses fallback billing engine.")

    def resume_subscription(self, *args, **kwargs):
        """Fallback providers don't manage provider-side subscriptions"""
        raise NotImplementedError(f"{self.__class__.__name__} uses fallback billing engine.")

    def update_subscription(self, *args, **kwargs):
        """Fallback providers don't manage provider-side subscriptions"""
        raise NotImplementedError(f"{self.__class__.__name__} uses fallback billing engine.")


# ===========================
# Provider Registry
# ===========================

_PROVIDER_REGISTRY: dict[str, type] = {}
_COMPONENT_PROVIDERS_DISCOVERED: bool = False


def _resolve_gateway_name(gateway_or_account) -> str:
    """
    Resolve the provider name from either a PaymentProviderAccount or legacy gateway.

    Args:
        gateway_or_account: PaymentProviderAccount (has component.slug) or
                           legacy gateway (has .name)

    Returns:
        str: Provider name for registry lookup
    """
    if hasattr(gateway_or_account, "component"):
        return gateway_or_account.component.slug
    if hasattr(gateway_or_account, "name"):
        return gateway_or_account.name
    return str(gateway_or_account)


def register_provider(gateway_name: str):
    """
    Decorator to register a subscription provider.

    Usage:
        @register_provider('stripe')
        class StripeSubscriptionProvider(SubscriptionProviderBase):
            ...
    """

    def decorator(provider_class):
        _PROVIDER_REGISTRY[gateway_name] = provider_class
        return provider_class

    return decorator


def _discover_component_providers() -> None:
    """
    Discover subscription providers from payment provider components.

    Scans ComponentRegistry for payment_provider components that have a
    subscription_provider.py module in their component directory.
    Dynamically imports these to trigger @register_provider registration.

    This keeps provider-specific subscription logic in the component
    package where it can be updated via the upgrade server independently.
    """
    global _COMPONENT_PROVIDERS_DISCOVERED
    if _COMPONENT_PROVIDERS_DISCOVERED:
        return
    _COMPONENT_PROVIDERS_DISCOVERED = True

    try:
        from component_updates.integration_paths import INTEGRATIONS_DIR

        components_dir = INTEGRATIONS_DIR / "payment_provider"

        if not components_dir.exists():
            return

        try:
            from component_updates.models import ComponentRegistry

            provider_components = ComponentRegistry.objects.filter(
                component_type="payment_provider"
            ).exclude(current_version__isnull=True)
        except Exception:
            # Fall back to scanning filesystem if DB isn't ready
            provider_components = None

        if provider_components is not None:
            for component in provider_components:
                _load_component_subscription_provider(
                    components_dir / component.slug / "current", component.slug
                )
        else:
            # Filesystem fallback: scan component directories
            for slug_dir in components_dir.iterdir():
                if not slug_dir.is_dir():
                    continue
                current_dir = slug_dir / "current"
                if current_dir.exists():
                    _load_component_subscription_provider(current_dir, slug_dir.name)

    except Exception as e:
        logger.debug(f"Component subscription provider discovery skipped: {e}")


def _load_component_subscription_provider(component_dir, slug: str) -> None:
    """
    Load a subscription_provider.py from a component directory if it exists.

    Args:
        component_dir: Path to the component version directory
        slug: Component slug for logging
    """
    import importlib.util
    import sys
    from pathlib import Path

    component_dir = Path(component_dir)
    sp_file = component_dir / "subscription_provider.py"

    if not sp_file.exists():
        return

    # Already registered? Skip.
    if slug in _PROVIDER_REGISTRY:
        return

    module_name = f"subscription_provider_{slug}"

    try:
        spec = importlib.util.spec_from_file_location(module_name, sp_file)
        if spec is None or spec.loader is None:
            logger.warning(f"Could not load subscription provider spec from {sp_file}")
            return

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        logger.info(f"Loaded subscription provider from component: {slug}")

    except Exception as e:
        logger.error(f"Failed to load subscription provider for {slug}: {e}")


def _ensure_discovered() -> None:
    """Ensure both built-in and component providers are registered."""
    if not _COMPONENT_PROVIDERS_DISCOVERED:
        _discover_component_providers()


def get_provider(gateway) -> SubscriptionProviderBase:
    """
    Get subscription provider instance for a payment gateway.

    Args:
        gateway: PaymentProviderAccount or legacy gateway instance

    Returns:
        SubscriptionProviderBase: Provider instance

    Raises:
        ValueError: If gateway is not supported for subscriptions
    """
    _ensure_discovered()

    name = _resolve_gateway_name(gateway)
    provider_class = _PROVIDER_REGISTRY.get(name)

    if not provider_class:
        raise ValueError(
            f"No subscription provider found for gateway: {name}. "
            f"Available providers: {list(_PROVIDER_REGISTRY.keys())}"
        )

    return provider_class(gateway)


def is_subscription_supported(gateway) -> bool:
    """
    Check if a payment gateway supports subscriptions.

    Args:
        gateway: PaymentProviderAccount or legacy gateway instance

    Returns:
        bool: True if subscriptions are supported
    """
    _ensure_discovered()

    name = _resolve_gateway_name(gateway)
    return name in _PROVIDER_REGISTRY
