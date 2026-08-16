"""
Back-in-stock notification tests.

Covers the previously declared-only `send_stock_notification` capability: the
StockItem post_save transition detector, the Celery task that sends the
`back_in_stock` email via the shared email system, idempotency, subscriber
filtering (variant / preferred warehouse), and the negative cases where nothing
should be sent.
"""

import pytest
from django.test import override_settings

from catalog.models import StockItem, StockNotification
from catalog.tasks import send_back_in_stock_notifications
from tests.factories import (
    EmailAccountFactory,
    EmailTemplateFactory,
    ProductFactory,
    StockItemFactory,
    WarehouseFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

_BACK_IN_STOCK_BODY = (
    "<mjml><mj-body><mj-section><mj-column><mj-text>"
    "{{ product_name }} is back! "
    '<a href="{{ product_url }}">buy</a>'
    "</mj-text></mj-column></mj-section></mj-body></mjml>"
)


@pytest.fixture
def seeded_email(db, django_site, site_settings):
    """Minimum for send_template_email to persist a rendered back_in_stock row:
    an active default account and an active back_in_stock template."""
    EmailAccountFactory(default=True, connected=True)
    EmailTemplateFactory(
        template_type="back_in_stock",
        subject="{{ product_name }} is back in stock",
        html_content=_BACK_IN_STOCK_BODY,
        text_content="{{ product_name }} is back in stock: {{ product_url }}",
    )
    return None


@pytest.fixture
def subscribed_product(db):
    """An out-of-stock product with a pending back-in-stock subscriber."""
    product = ProductFactory(track_inventory=True)
    warehouse = WarehouseFactory(code="WH-BIS")
    stock = StockItemFactory(product=product, warehouse=warehouse, on_hand=0, allocated=0)
    notif = StockNotification.objects.create(email="waiter@example.test", product=product)
    return {"product": product, "warehouse": warehouse, "stock": stock, "notif": notif}


# ============================================================
# The Celery task (send logic in isolation)
# ============================================================


class TestSendBackInStockTask:
    def test_task_emails_pending_subscriber_and_stamps_notified_at(
        self, seeded_email, email_outbox, subscribed_product
    ):
        stock = subscribed_product["stock"]
        StockItem.objects.filter(pk=stock.pk).update(on_hand=10)  # restock, bypass signal

        sent = send_back_in_stock_notifications(stock.pk)

        assert sent == 1
        email_outbox.assert_sent(to="waiter@example.test", template_type="back_in_stock", once=True)
        subscribed_product["notif"].refresh_from_db()
        assert subscribed_product["notif"].notified_at is not None

    def test_task_is_idempotent_no_double_send(
        self, seeded_email, email_outbox, subscribed_product
    ):
        stock = subscribed_product["stock"]
        StockItem.objects.filter(pk=stock.pk).update(on_hand=10)

        send_back_in_stock_notifications(stock.pk)
        second = send_back_in_stock_notifications(stock.pk)  # re-run

        assert second == 0
        assert email_outbox.count(to="waiter@example.test", template_type="back_in_stock") == 1

    def test_task_sends_nothing_when_still_out_of_stock(
        self, seeded_email, email_outbox, subscribed_product
    ):
        stock = subscribed_product["stock"]  # on_hand stays 0

        sent = send_back_in_stock_notifications(stock.pk)

        assert sent == 0
        assert email_outbox.count(template_type="back_in_stock") == 0

    def test_task_respects_preferred_warehouse(self, seeded_email, email_outbox, db):
        product = ProductFactory(track_inventory=True)
        wh_a = WarehouseFactory(code="WH-A")
        wh_b = WarehouseFactory(code="WH-B")
        stock_a = StockItemFactory(product=product, warehouse=wh_a, on_hand=10)
        # Subscriber only wants notifications from warehouse B.
        StockNotification.objects.create(
            email="picky@example.test", product=product, preferred_warehouse=wh_b
        )

        sent = send_back_in_stock_notifications(stock_a.pk)

        assert sent == 0
        assert email_outbox.count(to="picky@example.test") == 0

    def test_task_matches_variant_scoped_subscriber(self, seeded_email, email_outbox, db):
        from tests.factories import ProductVariantFactory

        product = ProductFactory(track_inventory=True)
        variant = ProductVariantFactory(product=product)
        wh = WarehouseFactory(code="WH-VAR")
        stock = StockItemFactory(product=product, warehouse=wh, variant=variant, on_hand=5)
        StockNotification.objects.create(
            email="variantfan@example.test", product=product, variant=variant
        )

        sent = send_back_in_stock_notifications(stock.pk)

        assert sent == 1
        email_outbox.assert_sent(to="variantfan@example.test", template_type="back_in_stock")


# ============================================================
# The signal wiring (transition detection + on_commit dispatch)
# ============================================================


class TestBackInStockSignalWiring:
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_restock_transition_dispatches_and_emails(
        self, seeded_email, email_outbox, subscribed_product, django_capture_on_commit_callbacks
    ):
        stock = subscribed_product["stock"]  # on_hand=0

        with django_capture_on_commit_callbacks(execute=True):
            stock.on_hand = 12
            stock.save(update_fields=["on_hand"])

        email_outbox.assert_sent(to="waiter@example.test", template_type="back_in_stock", once=True)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_allocation_of_in_stock_item_does_not_notify(
        self, seeded_email, email_outbox, db, django_capture_on_commit_callbacks
    ):
        """A subscriber exists and the item is in stock, but availability never
        crossed 0 -> positive, so no email (transition guard, not absence of
        subscribers)."""
        product = ProductFactory(track_inventory=True)
        wh = WarehouseFactory(code="WH-ALLOC")
        stock = StockItemFactory(product=product, warehouse=wh, on_hand=10, allocated=0)
        StockNotification.objects.create(email="insubscriber@example.test", product=product)

        with django_capture_on_commit_callbacks(execute=True):
            stock.allocate(3)  # touches only 'allocated'

        assert email_outbox.count(to="insubscriber@example.test") == 0

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_deallocation_that_restores_availability_notifies(
        self, seeded_email, email_outbox, db, django_capture_on_commit_callbacks
    ):
        """Availability is on_hand - allocated, so releasing a reservation
        (allocated falls) is a real 0 -> positive transition and must notify —
        even though on_hand didn't change."""
        product = ProductFactory(track_inventory=True)
        wh = WarehouseFactory(code="WH-DEALLOC")
        # Fully reserved: available == 0 (out of stock to shoppers).
        stock = StockItemFactory(product=product, warehouse=wh, on_hand=5, allocated=5)
        StockNotification.objects.create(email="dealloc@example.test", product=product)

        with django_capture_on_commit_callbacks(execute=True):
            stock.deallocate(2)  # available 0 -> 2, saves only 'allocated'

        email_outbox.assert_sent(
            to="dealloc@example.test", template_type="back_in_stock", once=True
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_no_email_when_no_subscribers(
        self, seeded_email, email_outbox, db, django_capture_on_commit_callbacks
    ):
        product = ProductFactory(track_inventory=True)
        wh = WarehouseFactory(code="WH-NOSUB")
        stock = StockItemFactory(product=product, warehouse=wh, on_hand=0)

        with django_capture_on_commit_callbacks(execute=True):
            stock.on_hand = 5
            stock.save(update_fields=["on_hand"])

        assert email_outbox.count(template_type="back_in_stock") == 0

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_restock_via_stock_operation_service_notifies(
        self, seeded_email, email_outbox, subscribed_product, django_capture_on_commit_callbacks
    ):
        """The new recount_stock operation is a restock path and must also fire
        the notification (proves the signal isn't coupled to one code path)."""
        from catalog.services.stock_operations import recount_stock

        stock = subscribed_product["stock"]  # on_hand=0

        with django_capture_on_commit_callbacks(execute=True):
            recount_stock(stock, 8)

        email_outbox.assert_sent(to="waiter@example.test", template_type="back_in_stock", once=True)
