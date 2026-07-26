"""
Drop cart.AppliedGiftCard — gift cards are a payment tender, not a discount.

The model capped a card against the cart's **pre-tax subtotal** and stored the
result in a field literally named ``discount_amount``. A $200 card against a
$100 + $10 tax + $10 shipping order therefore covered only $100, charged the
customer the remaining $20, and stranded $100 of balance. It also booked the
customer's own prepaid money as a revenue discount, and on POS — where the cart
apply and the checkout tender were both reachable in one sale — it handed over
goods the card never paid for while the balance stayed on the card.

Replaced by ``PaymentTransaction`` rows with ``tender_type='gift_card'``, held
at checkout against ``CheckoutSession.amount_due`` and captured on payment
confirmation. See ``catalog.services.gift_card_tender_service``.

**Irreversible.** ``DeleteModel`` drops the table and its rows. Any live rows
are session-scoped and pre-commitment — no money has moved at that point, since
balance was only ever debited at order creation — so a customer mid-checkout
simply re-keys the code on the payment step. The count is logged first so an
upgrade that discards rows says so rather than doing it silently.

``Order.gift_card_discount`` is deliberately **not** dropped: historical orders
must keep reading back correctly, and restating them would need ``amount_paid``
and the ``_base`` columns too.
"""

import logging

from django.db import migrations

logger = logging.getLogger(__name__)


def log_discarded_rows(apps, schema_editor):
    """Record how many in-flight cart applications this upgrade throws away."""
    AppliedGiftCard = apps.get_model("cart", "AppliedGiftCard")
    count = AppliedGiftCard.objects.count()
    if count:
        logger.warning(
            "Discarding %d cart_appliedgiftcard row(s): gift cards are now tendered "
            "at checkout. No balance was debited by these rows — affected customers "
            "re-enter their code on the payment step.",
            count,
        )
    else:
        logger.info("No cart_appliedgiftcard rows to discard.")


def noop_reverse(apps, schema_editor):
    """Nothing to undo — the log emitted no state."""


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0006_consolidate_duplicate_carts"),
    ]

    operations = [
        migrations.RunPython(log_discarded_rows, noop_reverse),
        migrations.DeleteModel(
            name="AppliedGiftCard",
        ),
    ]
