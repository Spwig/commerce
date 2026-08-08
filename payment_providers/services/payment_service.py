"""
Payment Service - payment amount validation.

Historically this module also carried create_payment_intent / authorize_payment
/ capture_payment / get_payment_status / cancel_payment methods, but they were
dead **and** broken: each constructed its provider with
``provider_class(provider_account)`` — handing the account model to a
constructor whose contract is ``__init__(self, credentials: dict, ...)``, which
raised ``TypeError`` inside ``_select_credentials`` — and several called
provider methods that no provider implements (e.g. ``authorize_payment``). They
had no callers; the live charge/authorize/capture/cancel path is
``PaymentOrchestrationService``, which builds providers correctly via
``PaymentProviderAccount.get_provider_instance()``. The broken methods were
removed rather than repaired so nothing grows a caller against a dead contract.

``validate_payment_amount`` is a pure guard with no provider dependency and is
kept here (referenced from the cart/checkout services).
"""

from decimal import Decimal

from django.utils.translation import gettext_lazy as _


class PaymentService:
    """
    Payment-amount validation helpers.
    """

    @staticmethod
    def validate_payment_amount(amount: Decimal, currency: str = "USD") -> tuple[bool, str]:
        """
        Validate a payment amount is positive and within the allowed ceiling.

        Args:
            amount: Payment amount
            currency: Currency code

        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if amount <= 0:
            return False, _("Payment amount must be greater than zero")

        # Check for reasonable maximum (e.g., $1,000,000)
        if amount > Decimal("1000000.00"):
            return False, _("Payment amount exceeds maximum allowed")

        return True, ""
