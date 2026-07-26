"""
Test helpers for the ``vouchers`` app.

Deliberately thin. ``tests/factories.py`` already ships a ``VoucherFactory``
(percentage / 10.00 / cart scope) and these tests use it for the common case.
What it does not offer is convenient construction of the *restriction* and
*usage* rows, or of vouchers whose validity window and usage limits are the
subject under test — that is what lives here.

Every helper takes explicit values. Nothing is randomised: a characterisation
suite that cannot be reproduced byte-for-byte is not characterising anything.
"""

from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from djmoney.money import Money

from vouchers.models import VoucherCode, VoucherRestriction, VoucherUsage


def make_voucher(code, **kwargs):
    """
    Create a ``VoucherCode`` with sane, explicit defaults.

    Defaults to a 10% cart-scoped voucher that is currently valid.
    """
    defaults = {
        "name": f"Voucher {code}",
        "discount_type": "percentage",
        "discount_value": Decimal("10.00"),
        "application_scope": "cart",
        "is_active": True,
    }
    defaults.update(kwargs)
    return VoucherCode.objects.create(code=code, **defaults)


def make_percentage_voucher(code, percent=Decimal("10.00"), max_discount=None, **kwargs):
    """Percentage voucher, optionally capped by ``max_discount`` (``Money``)."""
    return make_voucher(
        code,
        discount_type="percentage",
        discount_value=Decimal(percent),
        max_discount_amount=max_discount,
        **kwargs,
    )


def make_fixed_voucher(code, amount=Decimal("10.00"), **kwargs):
    """Fixed-amount voucher worth ``amount`` off."""
    return make_voucher(
        code,
        discount_type="fixed",
        discount_value=Decimal(amount),
        **kwargs,
    )


def make_expired_voucher(code, days_ago=1, **kwargs):
    """Voucher whose ``end_date`` is in the past."""
    now = timezone.now()
    return make_voucher(
        code,
        start_date=now - timedelta(days=days_ago + 30),
        end_date=now - timedelta(days=days_ago),
        **kwargs,
    )


def make_future_voucher(code, days_ahead=1, **kwargs):
    """Voucher whose ``start_date`` has not arrived yet."""
    return make_voucher(code, start_date=timezone.now() + timedelta(days=days_ahead), **kwargs)


def make_restriction(voucher, restriction_type, restriction_value, is_inclusive=True):
    """Attach a ``VoucherRestriction`` to ``voucher``."""
    return VoucherRestriction.objects.create(
        voucher=voucher,
        restriction_type=restriction_type,
        restriction_value=restriction_value,
        is_inclusive=is_inclusive,
    )


def record_usage(voucher, user=None, discount=Decimal("5.00"), cart_total=Decimal("50.00")):
    """
    Record a ``VoucherUsage`` row.

    Note this writes the ledger row only — it does **not** touch
    ``voucher.current_uses``. The two are incremented independently by
    ``CheckoutService``, and ``can_be_used_by_customer`` reads the ledger
    while ``is_valid`` reads the counter. Keeping them separate here is what
    lets the tests pin which check consults which.
    """
    return VoucherUsage.objects.create(
        voucher=voucher,
        user=user,
        discount_amount=Money(Decimal(discount), "USD"),
        cart_total=Money(Decimal(cart_total), "USD"),
    )
