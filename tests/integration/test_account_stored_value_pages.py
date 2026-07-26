"""
/account/gift-cards/ and /account/wallet/ (P2.5e-3/4).

The security property worth a test on its own: the gift card list shows the
buyer LAST-FOUR ONLY, never the full code. P2.4 settled that the RECIPIENT is
the entitled party of a gift card; the buyer may have given it away, and
re-showing them the code would silently re-arm them as a bearer of someone
else's money.
"""

from decimal import Decimal

import pytest
from django.urls import reverse
from djmoney.money import Money

from catalog.models import GiftCard
from tests.factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory
from wallet.services import WalletService

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.r2]


def _bought_card(user, code="GC-SECR-ETCO-DE99"):
    product = ProductFactory(product_type="gift_card")
    order = OrderFactory(user=user, payment_status="paid")
    item = OrderItemFactory(order=order, product=product)
    return GiftCard.objects.create(
        code=code,
        product=product,
        order_item=item,
        initial_value=Money(Decimal("50.00"), "USD"),
        recipient_email="recipient@test.spwig.com",
        is_active=True,
    )


class TestGiftCardList:
    def test_requires_login(self, client, site_settings):
        resp = client.get(reverse("accounts:gift_card_list"))
        assert resp.status_code == 302
        assert "login" in resp.headers["Location"]

    def test_shows_bought_cards_masked_never_the_full_code(self, client, site_settings):
        user = UserFactory()
        card = _bought_card(user)
        client.force_login(user)

        content = client.get(reverse("accounts:gift_card_list")).content.decode()

        assert card.code[-4:] in content, "The last four identify the card."
        assert card.code not in content, (
            "FULL CODE LEAKED to the buyer. The recipient is the entitled "
            "party; the buyer may have gifted the card away."
        )
        assert "recipient@test.spwig.com" in content

    def test_other_customers_cards_never_appear(self, client, site_settings):
        owner = UserFactory()
        _bought_card(owner, code="GC-MINE-MINE-0001")
        other = UserFactory()
        client.force_login(other)

        content = client.get(reverse("accounts:gift_card_list")).content.decode()

        assert "0001" not in content
        assert "not purchased any gift cards" in content


class TestWalletPage:
    def test_requires_login(self, client, site_settings):
        resp = client.get(reverse("accounts:wallet_detail"))
        assert resp.status_code == 302

    def test_shows_balance_and_history(self, client, site_settings):
        user = UserFactory()
        WalletService.credit(user, Decimal("30.00"), "USD", "manual", "goodwill credit")
        client.force_login(user)

        content = client.get(reverse("accounts:wallet_detail")).content.decode()

        assert "30.00" in content
        assert "goodwill credit" in content

    def test_no_wallet_renders_the_empty_state_without_creating_one(self, client, site_settings):
        from wallet.models import CustomerWallet

        user = UserFactory()
        client.force_login(user)

        content = client.get(reverse("accounts:wallet_detail")).content.decode()

        assert "no store credit yet" in content
        assert not CustomerWallet.objects.filter(customer=user).exists(), (
            "A page view created a ledger."
        )
