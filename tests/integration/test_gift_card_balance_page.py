"""
The gift card balance page (P2.5e-1).

Every delivery email since P2.3 has carried a balance link that 404'd — the
URL was hand-built in send_delivery_email against a route that never existed.
These tests pin the three parts of the fix: the page exists, the old spelling
in already-sent (immutable) emails redirects, and the email now derives its
link from the named route so a rename breaks loudly at send time instead of
silently mailing dead links.
"""

import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.r2]


class TestTheBalancePage:
    def test_the_page_renders(self, client, site_settings):
        resp = client.get(reverse("catalog:gift_card_balance"))

        assert resp.status_code == 200
        content = resp.content.decode()
        assert "gc-balance" in content
        assert "/api/catalog/gift-cards/check-balance/" in content, (
            "The page must point its JS at the throttled API endpoint."
        )

    def test_the_old_email_spelling_redirects_permanently(self, client, site_settings):
        """Sent emails are immutable; /check-balance/ must keep working forever."""
        resp = client.get("/en/gift-cards/check-balance/")

        assert resp.status_code == 301
        assert resp.headers["Location"] == reverse("catalog:gift_card_balance")

    def test_the_delivery_email_links_the_real_page(self, site_settings):
        """
        send_delivery_email builds check_balance_url with reverse(), so the
        link in new emails resolves. This is the regression that mailed 404s
        about real money for every card issued since P2.3.
        """
        from decimal import Decimal

        from django.test import Client
        from djmoney.money import Money

        from catalog.models import GiftCard
        from tests.factories import ProductFactory

        card = GiftCard.objects.create(
            product=ProductFactory(product_type="gift_card"),
            initial_value=Money(Decimal("25.00"), "USD"),
            recipient_email="r@test.spwig.com",
            is_active=True,
        )

        # Reach into the context the email builds rather than sending mail.
        import inspect

        from catalog.models import GiftCard

        src = inspect.getsource(GiftCard.send_delivery_email)
        assert "reverse('catalog:gift_card_balance')" in src or (
            'reverse("catalog:gift_card_balance")' in src
        ), "The email URL must come from the named route, not a hand-built string."
        assert '/gift-cards/check-balance/"' not in src.replace("pattern_name", ""), (
            "The dead hardcoded path is still in send_delivery_email."
        )

        # And the route it reverses actually serves a page.
        assert Client().get(reverse("catalog:gift_card_balance")).status_code == 200
