"""
R1 coverage: gift card sale gate + public balance endpoint hardening.

Two independent R1 changes, both about gift cards:

1. **Sales are gated off.** ``GiftCardService.create_gift_cards_for_order`` is
   reachable only from ``CheckoutService.process_payment_completion``, which has
   no callers — so paying for a gift card produced no card and sent no email.
   ``CartService.add_item`` now refuses ``product_type="gift_card"`` unless
   ``SPWIG_ENABLE_GIFT_CARD_SALES`` is on. P2.3 removes the gate.

2. **The balance endpoint no longer works as an oracle.** It is deliberately
   public (a gift card is a bearer instrument and the recipient usually has no
   account), which makes it an enumeration surface on stored value. Every
   failure mode now returns an identical 404, and both anonymous *and*
   authenticated callers are throttled — ``throttle_classes`` **replaces**
   ``DEFAULT_THROTTLE_CLASSES``, so naming only the anonymous class would have
   left authenticated callers unthrottled.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R1)
"""

from decimal import Decimal

import pytest
from django.core.cache import cache
from django.urls import reverse
from djmoney.money import Money
from rest_framework.test import APIClient

from tests.factories import CartFactory, CartItemFactory, ProductFactory, UserFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.r1,
]


@pytest.fixture(autouse=True)
def _clear_throttle_cache():
    """
    DRF caches throttle counters. With ``--reuse-db`` — and across repeated
    local runs — a stale counter turns a real assertion into a spurious 429,
    or exhausts the budget before the test that means to exhaust it.
    """
    cache.clear()
    yield
    cache.clear()


def _gift_card(initial_value="50.00", **kwargs):
    from catalog.models import GiftCard

    product = kwargs.pop("product", None) or ProductFactory(product_type="gift_card")
    defaults = {
        "product": product,
        "initial_value": Money(Decimal(initial_value), "USD"),
        "is_active": True,
    }
    defaults.update(kwargs)
    return GiftCard.objects.create(**defaults)


# ============================================================
# 6. Gift card sales (live as of P2.3)
# ============================================================


class TestGiftCardSalesAreLive:
    """
    Sales are on. Through R1 and P2.2 they were refused outright, because
    paying produced no card and sent no email. P2.3 added the issuance
    receiver, so the refusal is gone and validation replaces it.
    """

    def test_a_gift_card_with_recipient_details_can_be_bought(self, site_settings):
        from cart.services.cart_service import CartService

        cart = CartFactory(user=UserFactory())
        product = ProductFactory(product_type="gift_card", price=Decimal("50.00"))

        success, message, item = CartService.add_item(
            cart,
            product.id,
            quantity=1,
            gift_card_data={"recipient_email": "recipient@test.spwig.com"},
        )

        assert success is True, f"Gift card sales should be live: {message}"
        assert item is not None
        assert item.gift_card_data["recipient_email"] == "recipient@test.spwig.com"

    def test_a_gift_card_without_a_recipient_is_refused(self, site_settings):
        """
        Not a leftover of the old gate — a different rule.

        A card with nowhere to send it cannot be delivered, and the issuance
        service refuses to mint one rather than quietly mailing the gift to the
        buyer instead of the person it was bought for.
        """
        from cart.services.cart_service import CartService

        cart = CartFactory(user=UserFactory())
        product = ProductFactory(product_type="gift_card")

        success, message, item = CartService.add_item(cart, product.id, quantity=1)

        assert success is False
        assert item is None
        assert cart.items.count() == 0
        assert "recipient" in str(message).lower() or "email" in str(message).lower(), (
            f"Refused for the wrong reason: {message}"
        )

    def test_two_cards_for_two_recipients_stay_two_lines(self, site_settings):
        """
        Merging would give one recipient both cards and the other nothing.

        They match on (product, variant, customizations) — customizations is
        empty for both — so the ordinary merge path would fold them together.
        """
        from cart.services.cart_service import CartService

        cart = CartFactory(user=UserFactory())
        product = ProductFactory(product_type="gift_card", price=Decimal("25.00"))

        CartService.add_item(
            cart, product.id, quantity=1, gift_card_data={"recipient_email": "alice@test.spwig.com"}
        )
        CartService.add_item(
            cart, product.id, quantity=1, gift_card_data={"recipient_email": "bob@test.spwig.com"}
        )

        assert cart.items.count() == 2
        assert {i.gift_card_data["recipient_email"] for i in cart.items.all()} == {
            "alice@test.spwig.com",
            "bob@test.spwig.com",
        }

    def test_a_gift_card_is_not_shipped_or_stocked(self, site_settings):
        """
        Both of these blocked the sale outright once the gate came off:
        requires_shipping demanded an address and postage for an emailed code,
        and track_inventory failed every add with "Insufficient stock" — no
        merchant can create a StockItem for a gift card, the inline is hidden.

        ProductFactory defaults track_inventory False, so it is set explicitly
        here or this passes vacuously forever.
        """
        product = ProductFactory(product_type="gift_card", track_inventory=True)
        product.refresh_from_db()

        assert product.is_digital is True
        assert product.requires_shipping is False
        assert product.track_inventory is False

    def test_markup_in_the_message_is_refused(self, site_settings):
        """The message is interpolated into an email sent to a third party."""
        from cart.services.cart_service import CartService

        cart = CartFactory(user=UserFactory())
        product = ProductFactory(product_type="gift_card")

        success, _message, _item = CartService.add_item(
            cart,
            product.id,
            gift_card_data={
                "recipient_email": "recipient@test.spwig.com",
                "message": "<script>alert(1)</script>",
            },
        )

        assert success is False
        assert cart.items.count() == 0


class TestIssuanceIsActuallyWired:
    """
    The orphaned entry point is what caused this whole phase.

    ``GiftCardService.create_gift_cards_for_order`` was correct code that
    nothing called — reachable only from ``process_payment_completion``, which
    had zero callers — so merchants could sell gift cards and customers
    received nothing. Every unit test of the service passed throughout.

    So assert the WIRING, not the service: that a receiver is registered
    against Order's post_save. A service test cannot catch this failure mode.
    """

    def test_the_issuance_receiver_is_registered_for_order_post_save(self):
        from django.db.models.signals import post_save

        found = set()
        for entry in post_save.receivers:
            ref = entry[1]
            fn = ref() if callable(ref) else ref
            if fn is not None:
                found.add(getattr(fn, "__name__", ""))

        assert "issue_gift_cards_on_payment_confirmed" in found, (
            "No issuance receiver is registered on Order.post_save. Gift cards "
            "will be sold and never minted — the exact failure P2.3 exists to "
            "fix, and one that every service-level test still passes through."
        )

    def test_the_sales_flag_is_gone(self):
        """
        The flag was a stopgap while issuance did not exist. Leaving a dead
        setting around invites someone to 'turn sales off' with it and be
        surprised when nothing changes.
        """
        from django.conf import settings as django_settings

        assert not hasattr(django_settings, "SPWIG_ENABLE_GIFT_CARD_SALES"), (
            "SPWIG_ENABLE_GIFT_CARD_SALES still exists but no longer gates anything."
        )


class TestNonGiftCardProductsAreUnaffected:
    """The gate must be scoped to ``product_type="gift_card"`` and nothing else."""

    # "bundle" is deliberately absent: an unconfigured bundle is refused by
    # `check_hard_dependencies` with "Bundle has no components configured",
    # which has nothing to do with the gift card gate and would make this test
    # fail for the wrong reason.
    @pytest.mark.parametrize("product_type", ["simple", "variable", "digital"])
    def test_other_product_types_still_add(self, site_settings, product_type):
        from cart.services.cart_service import CartService

        cart = CartFactory(user=UserFactory())
        product = ProductFactory(product_type=product_type)

        success, message, item = CartService.add_item(cart, product.id, quantity=1)

        assert success is True, f"{product_type} product was refused: {message}"
        assert item is not None
        assert cart.items.count() == 1

    def test_a_cart_containing_other_items_is_untouched_by_the_refusal(self, site_settings):
        from cart.services.cart_service import CartService

        cart = CartFactory(user=UserFactory())
        ordinary = ProductFactory(product_type="simple")
        CartItemFactory(cart=cart, product=ordinary)
        gift_card_product = ProductFactory(product_type="gift_card")

        CartService.add_item(cart, gift_card_product.id)

        assert cart.items.count() == 1
        assert cart.items.first().product_id == ordinary.id


# ============================================================
# 7. Public gift card balance endpoint
# ============================================================


BALANCE_URL_NAME = "catalog_api:gift-card-check-balance"


class TestBalanceEndpointHappyPath:
    def test_a_valid_code_returns_the_balance(self, site_settings):
        card = _gift_card(initial_value="75.00")
        client = APIClient()

        response = client.post(reverse(BALANCE_URL_NAME), {"code": card.code}, format="json")

        assert response.status_code == 200
        assert response.data["code"] == card.code
        assert response.data["current_balance"]["amount"] == "75.00"
        assert response.data["current_balance"]["currency"] == "USD"
        assert response.data["is_active"] is True

    def test_the_response_reports_validity_and_redemption(self, site_settings):
        card = _gift_card(initial_value="100.00")
        client = APIClient()

        response = client.post(reverse(BALANCE_URL_NAME), {"code": card.code}, format="json")

        assert response.status_code == 200
        assert set(response.data) >= {
            "code",
            "current_balance",
            "initial_value",
            "is_active",
            "is_expired",
            "is_valid",
            "expires_at",
            "redemption_percentage",
        }


class TestBalanceEndpointIsNotAnOracle:
    """
    Every failure mode must be indistinguishable. If "no such code" differs
    from "malformed" or "disabled", enumeration gets cheap.
    """

    def _post(self, client, payload):
        return client.post(reverse(BALANCE_URL_NAME), payload, format="json")

    def test_missing_code_returns_404(self, site_settings):
        response = self._post(APIClient(), {})

        assert response.status_code == 404

    def test_empty_code_returns_404(self, site_settings):
        response = self._post(APIClient(), {"code": ""})

        assert response.status_code == 404

    def test_whitespace_only_code_returns_404(self, site_settings):
        response = self._post(APIClient(), {"code": "   "})

        assert response.status_code == 404

    def test_non_string_code_returns_404(self, site_settings):
        response = self._post(APIClient(), {"code": 12345})

        assert response.status_code == 404

    def test_list_code_returns_404(self, site_settings):
        response = self._post(APIClient(), {"code": ["GC-AAAA-BBBB-CCCC"]})

        assert response.status_code == 404

    def test_unknown_code_returns_404(self, site_settings):
        response = self._post(APIClient(), {"code": "GC-ZZZZ-ZZZZ-ZZZZ"})

        assert response.status_code == 404

    def test_every_failure_mode_returns_an_identical_response(self, site_settings):
        """
        The point of the test: statuses *and* bodies must match exactly, so a
        caller learns nothing from the difference.
        """
        client = APIClient()
        payloads = [
            {},
            {"code": ""},
            {"code": "   "},
            {"code": 12345},
            {"code": ["GC-AAAA-BBBB-CCCC"]},
            {"code": "GC-ZZZZ-ZZZZ-ZZZZ"},
            {"code": "not-even-a-code-shape"},
        ]

        responses = []
        for payload in payloads:
            cache.clear()  # keep the throttle out of this assertion
            response = self._post(client, payload)
            responses.append((response.status_code, response.data))

        first_status, first_body = responses[0]
        assert first_status == 404
        for status_code, body in responses[1:]:
            assert status_code == first_status
            assert body == first_body, (
                f"Response body differs between failure modes: {body!r} vs "
                f"{first_body!r}. That difference is an enumeration oracle."
            )

    def test_disabled_by_settings_is_indistinguishable_from_unknown(self, site_settings):
        card = _gift_card(initial_value="50.00")
        client = APIClient()

        unknown = self._post(client, {"code": "GC-ZZZZ-ZZZZ-ZZZZ"})
        unknown_result = (unknown.status_code, unknown.data)

        # `SiteSettings.get_settings()` re-reads pk=1 on every call, so saving
        # here is enough — there is no cache to invalidate.
        site_settings.public_gift_card_balance_enabled = False
        site_settings.save()
        cache.clear()

        disabled = self._post(client, {"code": card.code})

        assert (disabled.status_code, disabled.data) == unknown_result, (
            "A disabled endpoint answers differently from an unknown code, so "
            "a caller can tell a real code from a fake one."
        )


class TestBalanceEndpointCanBeDisabled:
    def test_disabled_setting_returns_404_for_a_real_card(self, site_settings):
        card = _gift_card(initial_value="50.00")
        site_settings.public_gift_card_balance_enabled = False
        site_settings.save()

        response = APIClient().post(reverse(BALANCE_URL_NAME), {"code": card.code}, format="json")

        assert response.status_code == 404

    def test_enabled_setting_returns_200_for_the_same_card(self, site_settings):
        card = _gift_card(initial_value="50.00")
        site_settings.public_gift_card_balance_enabled = True
        site_settings.save()

        response = APIClient().post(reverse(BALANCE_URL_NAME), {"code": card.code}, format="json")

        assert response.status_code == 200


class TestBalanceEndpointThrottling:
    """
    ``gift_card_balance_anon`` is 10/hour and ``gift_card_balance_user`` 30/hour.
    Both are declared because ``throttle_classes`` replaces the defaults rather
    than adding to them.
    """

    def test_anonymous_callers_are_throttled(self, site_settings):
        client = APIClient()
        url = reverse(BALANCE_URL_NAME)

        statuses = [
            client.post(url, {"code": "GC-ZZZZ-ZZZZ-ZZZZ"}, format="json").status_code
            for _ in range(12)
        ]

        assert 429 in statuses, (
            "An anonymous caller made 12 balance lookups without being "
            "throttled — the endpoint is a free stored-value enumeration "
            "oracle."
        )
        assert statuses[:10] == [404] * 10, (
            f"Throttling kicked in earlier than the 10/hour budget: {statuses}"
        )
        assert statuses[10] == 429

    def test_authenticated_callers_are_also_throttled(self, site_settings):
        """Authenticating must not be a way to buy a laxer limit."""
        client = APIClient()
        client.force_authenticate(user=UserFactory())
        url = reverse(BALANCE_URL_NAME)

        statuses = [
            client.post(url, {"code": "GC-ZZZZ-ZZZZ-ZZZZ"}, format="json").status_code
            for _ in range(32)
        ]

        assert 429 in statuses, (
            "An authenticated caller was never throttled. `throttle_classes` "
            "replaces DEFAULT_THROTTLE_CLASSES, so omitting the user variant "
            "leaves logged-in callers entirely unlimited on this oracle."
        )

    def test_the_configured_rates_are_present(self):
        from django.conf import settings as django_settings

        rates = django_settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]

        assert rates["gift_card_balance_anon"] == "10/hour"
        assert rates["gift_card_balance_user"] == "30/hour"

    def test_both_throttle_classes_are_attached_to_the_view(self):
        """
        Guards the specific mistake the docstring warns about: dropping the
        user throttle would leave authenticated callers unlimited.
        """
        from catalog.api_views import check_gift_card_balance
        from core.api.throttling import (
            GiftCardBalanceAnonThrottle,
            GiftCardBalanceUserThrottle,
        )

        attached = set(check_gift_card_balance.cls.throttle_classes)

        assert GiftCardBalanceAnonThrottle in attached
        assert GiftCardBalanceUserThrottle in attached
