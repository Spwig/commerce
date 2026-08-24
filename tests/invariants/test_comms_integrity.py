"""
Tier-1 communication-accuracy invariants (plan invariant #11).

The customer must receive an accurate order confirmation, exactly once, and
never for a transaction that didn't actually happen. Spwig sends the
confirmation from a ``post_save`` signal on Order creation
(email_system/signals.py), wrapped in ``transaction.on_commit`` — so these
tests drive real order creation, let the on-commit hook run, and assert on the
persisted ``EmailOutbox`` row via the shared ``email_outbox`` sink.

Covers:
  - the confirmation carries the right recipient, order number, total, and link;
  - it is sent exactly once, and a later order update (e.g. payment success
    flipping payment_status) does NOT resend it;
  - if order creation rolls back, NO confirmation goes out (on_commit is the
    "suppressed when the order never completed" guarantee);
  - no payment secret / internal id leaks into the message body.

Note (surfaced, not asserted): the confirmation fires on Order creation
regardless of payment_status, and the web flow creates the order *unpaid*
before payment — so a card order that later fails payment has already been
"confirmed". Whether that is desirable is a product decision (COD/bank-transfer
orders legitimately need it), so it is flagged for discussion rather than
pinned to a specific behaviour here.
"""

from decimal import Decimal

import pytest

from tests.factories import EmailAccountFactory, EmailTemplateFactory, OrderFactory

pytestmark = [pytest.mark.django_db, pytest.mark.invariant]

# A template that actually references the vars we assert on (the factory default
# only renders {{ customer_name }}).
_CONFIRMATION_BODY = (
    "<mjml><mj-body><mj-section><mj-column><mj-text>"
    "Order {{ order_number }} total {{ order_total }} "
    '<a href="{{ order_url }}">view</a>'
    "</mj-text></mj-column></mj-section></mj-body></mjml>"
)


@pytest.fixture
def seeded_email(db, django_site, site_settings):
    """The minimum to make send_template_email persist a *rendered* row:
    an active default EmailAccount (else it raises and writes nothing) and an
    active order_confirmation template (else the row is written as 'failed')."""
    EmailAccountFactory(default=True, connected=True)
    EmailTemplateFactory(
        template_type="order_confirmation",
        subject="Your order {{ order_number }}",
        html_content=_CONFIRMATION_BODY,
        text_content="Order {{ order_number }} total {{ order_total }}",
    )
    EmailTemplateFactory(
        template_type="return_refund_processed",
        subject="Refund for order {{ order_number }}",
        html_content=(
            "<mjml><mj-body><mj-section><mj-column><mj-text>"
            "Refund of {{ refund_currency }} {{ refund_amount }} for order {{ order_number }}"
            "</mj-text></mj-column></mj-section></mj-body></mjml>"
        ),
        text_content="Refund {{ refund_currency }} {{ refund_amount }} for {{ order_number }}",
    )
    return None


def test_confirmation_email_is_accurate_and_sent_once(
    seeded_email, email_outbox, django_capture_on_commit_callbacks
):
    with django_capture_on_commit_callbacks(execute=True):
        order = OrderFactory(
            email="buyer@example.test",
            total_amount=Decimal("99.99"),
            total_amount_currency="USD",
        )

    row = email_outbox.assert_sent(
        to="buyer@example.test",
        template_type="order_confirmation",
        contains=[order.order_number, "USD 99.99"],  # total renders as "CUR amount"
        once=True,
    )
    # the order link renders (points at the localised order-confirmation page)
    assert f"/checkout/confirmation/{order.order_number}/" in row.html_body
    # #11 no-leak: the confirmation must not carry payment secrets / intent ids.
    haystack = f"{row.subject}\n{row.html_body}\n{row.text_body}".lower()
    assert "client_secret" not in haystack
    assert "pi_" not in haystack


def test_confirmation_email_not_resent_on_order_update(
    seeded_email, email_outbox, django_capture_on_commit_callbacks
):
    """The email is gated on created=True, so payment success (an update, not an
    insert) must not trigger a second confirmation."""
    with django_capture_on_commit_callbacks(execute=True):
        order = OrderFactory(email="buyer2@example.test", payment_status="unpaid")
    # assert_sent (not a status-blind count) proves a real rendered row exists,
    # so the "still 1" check below isn't satisfied by a failed/skipped row.
    row = email_outbox.assert_sent(
        to="buyer2@example.test",
        template_type="order_confirmation",
        contains=[order.order_number],
        once=True,
    )
    assert row.status not in ("failed", "skipped")

    with django_capture_on_commit_callbacks(execute=True):
        order.payment_status = "paid"
        order.save(update_fields=["payment_status"])
    assert email_outbox.count(to="buyer2@example.test", template_type="order_confirmation") == 1


def test_no_confirmation_email_when_order_creation_rolls_back(
    seeded_email, email_outbox, django_capture_on_commit_callbacks
):
    """If the order transaction rolls back, the on_commit hook never fires —
    a customer is never emailed about an order that didn't commit.

    Guard-the-guard: a committed order in the SAME block DOES get its email, so
    the rolled-back order's silence is genuine suppression, not the harness
    simply never running on_commit callbacks."""
    from django.db import transaction

    with django_capture_on_commit_callbacks(execute=True):
        OrderFactory(email="committed@example.test")  # positive control
        try:
            with transaction.atomic():
                OrderFactory(email="rolledback@example.test")
                raise RuntimeError("abort before commit")
        except RuntimeError:
            pass

    email_outbox.assert_sent(
        to="committed@example.test", template_type="order_confirmation", once=True
    )
    email_outbox.assert_none(to="rolledback@example.test")


def test_refund_processed_email_is_accurate(seeded_email, email_outbox):
    """The returns-flow refund email reaches the customer with the correct order
    number and refund amount. (create_refund itself sends no customer email —
    the refund comms are the returns flow / order.status='refunded' signal.)"""
    from decimal import Decimal

    from tests.factories import RefundFactory, ReturnRequestFactory

    order = OrderFactory(
        paid_order=True,
        delivered=True,
        total_amount=Decimal("40.00"),
        total_amount_currency="USD",
    )
    refund = RefundFactory(order=order, total_amount=Decimal("40.00"), total_amount_currency="USD")
    return_request = ReturnRequestFactory(order=order, refund=refund)

    from orders.emails import send_refund_processed_notification

    send_refund_processed_notification(return_request)  # sent synchronously

    row = email_outbox.assert_sent(
        to=return_request.user.email,
        template_type="return_refund_processed",
        contains=[order.order_number, "40.00"],
        once=True,
    )
    # Robust against the preference-skip path: a rendered transactional email,
    # not a status="skipped" row that never rendered the amount.
    assert row.status not in ("failed", "skipped")
