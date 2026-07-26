"""
Voucher & Gift Card System integration tests.

Tests verify the correctness of bug fixes in the voucher, gift card,
cart, checkout, and order subsystems:

1. Voucher usage tracking (current_uses increment + VoucherUsage records)
2. Voucher combination rules (non-combinable + reverse check)
3. Gift card discount recalculation on cart mutations
4. Checkout session total includes gift card discount
5. min_order_value enforcement (correct field name in orders utils/forms)
6. Gift card refund balance restoration
7. AppliedVoucher unique constraints (cart + order FKs)
8. Secure random code generation (secrets.choice)
"""

from decimal import Decimal
from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from djmoney.money import Money

from tests.factories import (
    CartFactory,
    CartItemFactory,
    CheckoutSessionFactory,
    OrderFactory,
    OrderItemFactory,
    ProductFactory,
    UserFactory,
    VoucherFactory,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.voucher_gift_card,
]


# ============================================================
# Helpers
# ============================================================


def _create_cart_with_items(user, price=Decimal("100.00"), quantity=1, site_settings=None):
    """Create a cart with one simple product at the given price."""
    cart = CartFactory(user=user)
    product = ProductFactory(price=price)
    CartItemFactory(cart=cart, product=product, quantity=quantity, unit_price=price)
    return cart


def _create_gift_card(initial_value=Decimal("50.00"), currency="USD"):
    """Create a catalog.GiftCard ready for cart application."""
    from catalog.models import GiftCard

    product = ProductFactory(product_type="gift_card", price=Money(initial_value, currency))
    gc = GiftCard.objects.create(
        product=product,
        initial_value=Money(initial_value, currency),
        current_balance=Money(initial_value, currency),
        recipient_email="recipient@test.spwig.com",
        is_active=True,
    )
    return gc


# ============================================================
# VoucherUsageTests
# ============================================================


class TestVoucherUsageTracking:
    """Tests for voucher usage increment and VoucherUsage record creation."""

    def test_voucher_current_uses_incremented_on_order_creation(self, site_settings):
        """After CheckoutService creates an order, voucher.current_uses should increase."""
        from cart.services.checkout_service import CheckoutService

        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        # Apply voucher
        voucher = VoucherFactory(
            code="USE_TRACK_1",
            discount_type="fixed",
            discount_value=Decimal("10.00"),
        )
        success, msg, discount = cart.apply_voucher("USE_TRACK_1", user)
        assert success, f"apply_voucher failed: {msg}"

        # Verify current_uses is 0 before order
        voucher.refresh_from_db()
        assert voucher.current_uses == 0

        # Create checkout session and order via service (mocking heavy dependencies)
        session = CheckoutSessionFactory(cart=cart)
        session.recalculate_totals()

        # Call _process_voucher_usage directly (the fix under test)
        order = OrderFactory(user=user, subtotal=Decimal("100.00"), total_amount=Decimal("90.00"))
        CheckoutService._process_voucher_usage(cart, order)

        # Verify current_uses incremented
        voucher.refresh_from_db()
        assert voucher.current_uses == 1

    def test_voucher_usage_record_created_on_order_creation(self, site_settings):
        """_process_voucher_usage must create a VoucherUsage record with correct fields."""
        from cart.services.checkout_service import CheckoutService
        from vouchers.models import VoucherUsage

        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("50.00"))

        voucher = VoucherFactory(
            code="USE_RECORD_1",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
        )
        cart.apply_voucher("USE_RECORD_1", user)

        order = OrderFactory(user=user, subtotal=Decimal("50.00"), total_amount=Decimal("45.00"))
        CheckoutService._process_voucher_usage(cart, order)

        # Verify VoucherUsage record
        usage = VoucherUsage.objects.filter(voucher=voucher, order=order).first()
        assert usage is not None, "VoucherUsage record not created"
        assert usage.user == user
        assert usage.discount_amount.amount > 0
        assert usage.cart_total.amount > 0

    def test_voucher_usage_incremented_atomically(self, site_settings):
        """Two concurrent usages should both increment (F-expression atomicity)."""
        from cart.services.checkout_service import CheckoutService

        user1 = UserFactory()
        user2 = UserFactory()
        cart1 = _create_cart_with_items(user1, price=Decimal("100.00"))
        cart2 = _create_cart_with_items(user2, price=Decimal("100.00"))

        voucher = VoucherFactory(
            code="ATOMIC_1",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            max_uses_total=10,
        )
        cart1.apply_voucher("ATOMIC_1", user1)
        cart2.apply_voucher("ATOMIC_1", user2)

        order1 = OrderFactory(user=user1)
        order2 = OrderFactory(user=user2)

        CheckoutService._process_voucher_usage(cart1, order1)
        CheckoutService._process_voucher_usage(cart2, order2)

        voucher.refresh_from_db()
        assert voucher.current_uses == 2

    def test_total_usage_limit_enforced(self, site_settings):
        """Voucher with max_uses_total=1 should reject second application."""
        from vouchers.models import VoucherCode

        user1 = UserFactory()
        user2 = UserFactory()

        voucher = VoucherFactory(
            code="LIMIT_TOTAL_1",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            max_uses_total=1,
            current_uses=0,
        )

        # First use succeeds
        cart1 = _create_cart_with_items(user1, price=Decimal("50.00"))
        success1, msg1, _ = cart1.apply_voucher("LIMIT_TOTAL_1", user1)
        assert success1

        # Simulate usage by incrementing counter
        VoucherCode.objects.filter(pk=voucher.pk).update(current_uses=1)
        voucher.refresh_from_db()
        assert voucher.current_uses == 1
        assert not voucher.is_valid  # max_uses_total reached

        # Second use should fail
        cart2 = _create_cart_with_items(user2, price=Decimal("50.00"))
        success2, msg2, _ = cart2.apply_voucher("LIMIT_TOTAL_1", user2)
        assert not success2

    def test_per_customer_usage_limit_enforced(self, site_settings):
        """Voucher with max_uses_per_customer=1 should reject second use by same customer."""
        from vouchers.models import VoucherUsage

        user = UserFactory()

        voucher = VoucherFactory(
            code="LIMIT_USER_1",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            max_uses_per_customer=1,
        )

        # Create a VoucherUsage record for this user (simulating prior use)
        VoucherUsage.objects.create(
            voucher=voucher,
            user=user,
            discount_amount=Money(Decimal("5.00"), "USD"),
            cart_total=Money(Decimal("50.00"), "USD"),
        )

        # Attempt to apply again -- should fail
        cart = _create_cart_with_items(user, price=Decimal("50.00"))
        success, msg, _ = cart.apply_voucher("LIMIT_USER_1", user)
        assert not success
        assert "usage limit" in str(msg).lower() or "limit" in str(msg).lower()


# ============================================================
# VoucherCombinationTests
# ============================================================


class TestVoucherCombinationRules:
    """Tests for non-combinable voucher enforcement (including reverse check)."""

    def test_non_combinable_voucher_rejects_second_voucher(self, site_settings):
        """When a non-combinable voucher is applied first, a second voucher should be rejected."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        # First voucher: non-combinable
        VoucherFactory(
            code="EXCLUSIVE_1",
            discount_type="fixed",
            discount_value=Decimal("10.00"),
            cannot_combine_with_other_vouchers=True,
        )
        success1, _, _ = cart.apply_voucher("EXCLUSIVE_1", user)
        assert success1

        # Second voucher: regular
        VoucherFactory(
            code="REGULAR_1",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
        )
        success2, msg2, _ = cart.apply_voucher("REGULAR_1", user)
        assert not success2
        assert "cannot be combined" in msg2.lower() or "combine" in msg2.lower()

    def test_regular_voucher_then_non_combinable_rejected(self, site_settings):
        """A non-combinable voucher should be rejected when a regular voucher already exists."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        # Apply regular voucher first
        VoucherFactory(
            code="REGULAR_2",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
        )
        success1, _, _ = cart.apply_voucher("REGULAR_2", user)
        assert success1

        # Attempt to add non-combinable -- should fail
        VoucherFactory(
            code="EXCLUSIVE_2",
            discount_type="fixed",
            discount_value=Decimal("10.00"),
            cannot_combine_with_other_vouchers=True,
        )
        success2, msg2, _ = cart.apply_voucher("EXCLUSIVE_2", user)
        assert not success2
        assert "cannot be combined" in msg2.lower() or "combine" in msg2.lower()

    def test_reverse_combination_check_non_combinable_exists(self, site_settings):
        """Bug fix: when cart has a non-combinable voucher, ANY new voucher should be blocked
        even if the new voucher itself is combinable."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("200.00"))

        # Non-combinable voucher in cart
        VoucherFactory(
            code="NOCOMBINE",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            cannot_combine_with_other_vouchers=True,
        )
        success1, _, _ = cart.apply_voucher("NOCOMBINE", user)
        assert success1

        # New combinable voucher should be rejected (reverse check)
        VoucherFactory(
            code="COMBINABLE",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            cannot_combine_with_other_vouchers=False,
        )
        success2, msg2, _ = cart.apply_voucher("COMBINABLE", user)
        assert not success2
        assert "cannot be combined" in msg2.lower() or "combine" in msg2.lower()

    def test_combinable_vouchers_can_stack(self, site_settings):
        """Multiple combinable vouchers should work together."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        VoucherFactory(code="COMBO_A", discount_type="fixed", discount_value=Decimal("5.00"))
        VoucherFactory(code="COMBO_B", discount_type="fixed", discount_value=Decimal("3.00"))

        success1, _, _ = cart.apply_voucher("COMBO_A", user)
        assert success1

        success2, _, _ = cart.apply_voucher("COMBO_B", user)
        assert success2

        # Both applied
        assert cart.applied_vouchers.count() == 2

    def test_same_voucher_cannot_be_applied_twice(self, site_settings):
        """Applying the same voucher code twice should fail."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        VoucherFactory(code="DUP_V", discount_type="fixed", discount_value=Decimal("5.00"))

        success1, _, _ = cart.apply_voucher("DUP_V", user)
        assert success1

        success2, msg2, _ = cart.apply_voucher("DUP_V", user)
        assert not success2
        assert "already" in msg2.lower()


# ============================================================
# CheckoutSessionTests
# ============================================================


# ============================================================
# MinOrderValueTests
# ============================================================


class TestMinOrderValue:
    """Tests for min_order_value enforcement (fixed field name bug)."""

    def test_min_order_value_enforced_in_cart_apply_voucher(self, site_settings):
        """Cart.apply_voucher should reject voucher when cart total < min_order_value."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("30.00"))

        voucher = VoucherFactory(
            code="MIN_ORDER_V",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            min_order_value=Money(Decimal("50.00"), "USD"),
        )

        success, msg, _ = cart.apply_voucher("MIN_ORDER_V", user)
        assert not success
        assert "minimum" in msg.lower() or "min" in msg.lower()

    def test_min_order_value_passes_when_met(self, site_settings):
        """Cart.apply_voucher should succeed when cart total >= min_order_value."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("75.00"))

        VoucherFactory(
            code="MIN_ORDER_PASS",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            min_order_value=Money(Decimal("50.00"), "USD"),
        )

        success, msg, _ = cart.apply_voucher("MIN_ORDER_PASS", user)
        assert success, f"Voucher should have been accepted: {msg}"

    def test_min_order_value_enforced_in_admin_voucher_form(self, site_settings):
        """OrderVoucherApplicationForm should reject voucher when order subtotal < min_order_value."""
        from orders.forms import OrderVoucherApplicationForm

        user = UserFactory()
        order = OrderFactory(
            user=user,
            subtotal=Decimal("30.00"),
            total_amount=Decimal("30.00"),
        )

        VoucherFactory(
            code="FORM_MIN_V",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            min_order_value=Money(Decimal("50.00"), "USD"),
        )

        form = OrderVoucherApplicationForm(
            data={"voucher_code": "FORM_MIN_V"},
            order=order,
        )
        assert not form.is_valid()
        assert "voucher_code" in form.errors
        error_text = str(form.errors["voucher_code"]).lower()
        assert "minimum" in error_text

    def test_min_order_value_in_apply_voucher_to_order(self, site_settings):
        """orders.utils.apply_voucher_to_order should reject when below min_order_value."""
        from orders.utils import apply_voucher_to_order

        user = UserFactory()
        order = OrderFactory(
            user=user,
            subtotal=Decimal("25.00"),
            total_amount=Decimal("25.00"),
        )

        VoucherFactory(
            code="UTIL_MIN_V",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            min_order_value=Money(Decimal("50.00"), "USD"),
        )

        with pytest.raises(ValidationError) as exc_info:
            apply_voucher_to_order(order, "UTIL_MIN_V")
        assert "minimum" in str(exc_info.value).lower()


# ============================================================
# GiftCardRefundTests
# ============================================================


class TestGiftCardRefund:
    """
    Automatic balance restoration is DISABLED as of P2.3.

    These tests used to assert that refunding an order restored the full
    original redemption to any gift card used to pay for it. That behaviour was
    wrong in a way that cost real money: it restored the WHOLE redemption
    regardless of how much was actually refunded, so refunding 20 of a 200
    order paid entirely by gift card gave the customer 200 back on the card AND
    the 20. It also wrote no PaymentTransaction refund row, so the tender ledger
    and the gift card ledger disagreed afterwards.

    It survived only because it was unreachable — `order_item` was never
    populated, because issuance had never run. P2.3 makes issuance real, which
    would have brought this to life too.

    Tender-aware refunds are P2.4 (TenderRefundAllocator). Until then the
    service logs loudly and a human adjusts the card from the admin: refusing
    is better than a partly-correct restore that silently over-credits.
    """

    def test_balance_is_not_silently_restored(self, site_settings):
        from catalog.models import GiftCardTransaction
        from catalog.services.gift_card_service import GiftCardService

        gc = _create_gift_card(initial_value=Decimal("200.00"))
        order = OrderFactory(payment_status="paid")
        gc.redeem(amount=Money(Decimal("200.00"), "USD"), order=order)
        gc.refresh_from_db()
        assert gc.current_balance.amount == Decimal("0.00")

        GiftCardService.process_gift_card_refund(order)

        gc.refresh_from_db()
        assert gc.current_balance.amount == Decimal("0.00"), (
            "The card was auto-restored. That path over-credits on a partial "
            "refund and is disabled until P2.4 routes refunds through the "
            "tender rail."
        )
        assert not GiftCardTransaction.objects.filter(
            gift_card=gc, order=order, transaction_type="refund", amount__gt=0
        ).exists()

    def test_a_purchased_card_is_deactivated_and_zeroed_together(self, site_settings):
        """
        Part 1 still runs, and its ledger row and balance must agree.

        It used to write a -initial_value ledger row while leaving
        current_balance at full face value, so reconciliation
        (balance == initial - redemptions + refunds + adjustments) failed on
        every refunded card.
        """
        from catalog.models import GiftCard, GiftCardTransaction
        from catalog.services.gift_card_service import GiftCardService

        product = ProductFactory(product_type="gift_card", price=Decimal("50.00"))
        order = OrderFactory(payment_status="paid")
        order_item = OrderItemFactory(
            order=order,
            product=product,
            quantity=1,
            unit_price=Money(Decimal("50.00"), "USD"),
            total_price=Money(Decimal("50.00"), "USD"),
            gift_card_data={"recipient_email": "recipient@test.spwig.com"},
        )
        GiftCardService.create_gift_cards_for_order(order)
        card = GiftCard.objects.get(order_item=order_item)

        GiftCardService.process_gift_card_refund(order)

        card.refresh_from_db()
        assert card.is_active is False
        assert card.current_balance.amount == Decimal("0.00")

        row = GiftCardTransaction.objects.get(
            gift_card=card, order=order, transaction_type="refund"
        )
        assert row.balance_after == card.current_balance, (
            "Ledger and balance disagree — reconciliation would fail."
        )


# ============================================================
# AppliedVoucherModelTests
# ============================================================


class TestAppliedVoucherModel:
    """Tests for AppliedVoucher model including order FK and unique constraints."""

    def test_applied_voucher_with_cart_fk(self, site_settings):
        """AppliedVoucher can be created with a cart FK."""
        from vouchers.models import AppliedVoucher

        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("50.00"))
        voucher = VoucherFactory(code="AV_CART_FK")

        av = AppliedVoucher.objects.create(
            cart=cart,
            voucher=voucher,
            discount_amount=Money(Decimal("5.00"), "USD"),
        )
        assert av.pk is not None
        assert av.cart == cart
        assert av.order is None

    def test_applied_voucher_with_order_fk(self, site_settings):
        """Bug fix: AppliedVoucher can be created with an order FK."""
        from vouchers.models import AppliedVoucher

        user = UserFactory()
        order = OrderFactory(user=user)
        voucher = VoucherFactory(code="AV_ORDER_FK")

        av = AppliedVoucher.objects.create(
            order=order,
            voucher=voucher,
            discount_amount=Money(Decimal("10.00"), "USD"),
        )
        assert av.pk is not None
        assert av.order == order
        assert av.cart is None

    def test_applied_voucher_with_both_cart_and_order(self, site_settings):
        """AppliedVoucher can reference both a cart and an order."""
        from vouchers.models import AppliedVoucher

        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("50.00"))
        order = OrderFactory(user=user)
        voucher = VoucherFactory(code="AV_BOTH_FK")

        av = AppliedVoucher.objects.create(
            cart=cart,
            order=order,
            voucher=voucher,
            discount_amount=Money(Decimal("5.00"), "USD"),
        )
        assert av.cart == cart
        assert av.order == order

    def test_applied_voucher_unique_per_cart(self, site_settings):
        """Same voucher cannot be applied twice to the same cart (DB constraint)."""
        from vouchers.models import AppliedVoucher

        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))
        voucher = VoucherFactory(code="UNIQUE_CART_V")

        AppliedVoucher.objects.create(
            cart=cart,
            voucher=voucher,
            discount_amount=Money(Decimal("5.00"), "USD"),
        )

        with pytest.raises(IntegrityError), transaction.atomic():
            AppliedVoucher.objects.create(
                cart=cart,
                voucher=voucher,
                discount_amount=Money(Decimal("5.00"), "USD"),
            )

    def test_applied_voucher_unique_per_order(self, site_settings):
        """Same voucher cannot be applied twice to the same order (DB constraint)."""
        from vouchers.models import AppliedVoucher

        user = UserFactory()
        order = OrderFactory(user=user)
        voucher = VoucherFactory(code="UNIQUE_ORDER_V")

        AppliedVoucher.objects.create(
            order=order,
            voucher=voucher,
            discount_amount=Money(Decimal("5.00"), "USD"),
        )

        with pytest.raises(IntegrityError), transaction.atomic():
            AppliedVoucher.objects.create(
                order=order,
                voucher=voucher,
                discount_amount=Money(Decimal("5.00"), "USD"),
            )

    def test_same_voucher_different_carts_allowed(self, site_settings):
        """Same voucher applied to different carts should be allowed."""
        from vouchers.models import AppliedVoucher

        user1 = UserFactory()
        user2 = UserFactory()
        cart1 = _create_cart_with_items(user1, price=Decimal("100.00"))
        cart2 = _create_cart_with_items(user2, price=Decimal("100.00"))
        voucher = VoucherFactory(code="SAME_V_DIFF_CART")

        av1 = AppliedVoucher.objects.create(
            cart=cart1,
            voucher=voucher,
            discount_amount=Money(Decimal("5.00"), "USD"),
        )
        av2 = AppliedVoucher.objects.create(
            cart=cart2,
            voucher=voucher,
            discount_amount=Money(Decimal("5.00"), "USD"),
        )
        assert av1.pk != av2.pk


# ============================================================
# SecureRandomCodeTests
# ============================================================


class TestSecureRandomCodeGeneration:
    """Tests for voucher code generation using secrets.choice (not random.choice)."""

    def test_voucher_code_uses_secrets_module(self):
        """Voucher code generation should use secrets.choice, not random.choice."""
        from vouchers.models import VoucherCode

        # Patch random.choice to fail if called
        with patch("random.choice", side_effect=AssertionError("random.choice should not be used")):
            code = VoucherCode().generate_unique_code()
            assert code is not None
            assert len(code) == 8

    def test_generated_code_is_alphanumeric_uppercase(self):
        """Generated codes should be uppercase alphanumeric."""
        from vouchers.models import VoucherCode

        for _ in range(10):
            code = VoucherCode().generate_unique_code()
            assert code.isalnum()
            assert code == code.upper()
            assert len(code) == 8

    def test_generated_code_is_unique(self):
        """Generated codes should be unique even after many generations."""
        from vouchers.models import VoucherCode

        codes = set()
        for _ in range(50):
            code = VoucherCode().generate_unique_code()
            codes.add(code)

        # All should be unique (practically impossible to collide with 36^8 space)
        assert len(codes) == 50


# ============================================================
# CartService Integration Tests
# ============================================================


# ============================================================
# Edge Cases
# ============================================================


class TestEdgeCases:
    """Edge cases for voucher and gift card system."""

    def test_inactive_voucher_rejected(self, site_settings):
        """An inactive voucher should not be applicable."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        VoucherFactory(code="INACTIVE_V", is_active=False)

        success, msg, _ = cart.apply_voucher("INACTIVE_V", user)
        assert not success

    def test_expired_voucher_rejected(self, site_settings):
        """An expired voucher should not be applicable."""
        from datetime import timedelta

        from django.utils import timezone

        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        VoucherFactory(
            code="EXPIRED_V",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            start_date=timezone.now() - timedelta(days=10),
            end_date=timezone.now() - timedelta(days=1),
        )

        success, msg, _ = cart.apply_voucher("EXPIRED_V", user)
        assert not success

    def test_nonexistent_voucher_code_rejected(self, site_settings):
        """Applying a non-existent voucher code should fail gracefully."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        success, msg, _ = cart.apply_voucher("DOESNOTEXIST", user)
        assert not success
        assert "invalid" in msg.lower()

    def test_gift_card_for_gift_card_product_rejected(self, site_settings):
        """
        A gift card cannot buy another gift card.

        Enforced by GiftCardTenderService.authorize_for_session since P2.2f
        deleted Cart.apply_gift_card, which used to hold the rule.
        """
        from catalog.services.gift_card_tender_service import (
            GiftCardTenderError,
            GiftCardTenderService,
        )

        user = UserFactory()
        cart = CartFactory(user=user)
        gc_product = ProductFactory(product_type="gift_card", price=Decimal("50.00"))
        CartItemFactory(cart=cart, product=gc_product, quantity=1, unit_price=Decimal("50.00"))
        session = CheckoutSessionFactory(cart=cart)

        gc = _create_gift_card(initial_value=Decimal("50.00"))
        with pytest.raises(GiftCardTenderError, match="cannot be used to buy another gift card"):
            GiftCardTenderService.authorize_for_session(session, gc.code)

    def test_zero_discount_voucher_rejected(self, site_settings):
        """A voucher that calculates to $0 discount should be rejected."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("100.00"))

        # 0% discount = $0
        VoucherFactory(
            code="ZERO_DISC",
            discount_type="percentage",
            discount_value=Decimal("0.01"),  # Very small percentage
        )

        # This might or might not be zero depending on rounding -- let's test with 0
        # Use a voucher that targets products not in cart
        VoucherFactory(
            code="WRONG_SCOPE",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
            application_scope="products",
        )
        # No eligible_products configured, so eligible amount = 0
        success, msg, _ = cart.apply_voucher("WRONG_SCOPE", user)
        assert not success

    def test_voucher_discount_does_not_exceed_cart_total(self, site_settings):
        """Fixed discount larger than cart total should be capped."""
        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("10.00"))

        VoucherFactory(
            code="BIG_FIXED",
            discount_type="fixed",
            discount_value=Decimal("50.00"),
        )

        success, msg, discount = cart.apply_voucher("BIG_FIXED", user)
        assert success
        # Discount should be capped at cart total ($10)
        assert Decimal(str(discount.amount)) == Decimal("10.00")

    def test_fully_redeemed_gift_card_rejected(self, site_settings):
        """A gift card with $0 balance should be rejected."""
        from catalog.models import GiftCard

        user = UserFactory()
        cart = _create_cart_with_items(user, price=Decimal("50.00"))

        # Create GC with positive balance first (save() overrides 0 balance on creation)
        gc = _create_gift_card(initial_value=Decimal("25.00"))
        # Drain balance via DB update to bypass save() guard
        GiftCard.objects.filter(pk=gc.pk).update(
            current_balance=Decimal("0.00"),
            current_balance_currency="USD",
        )
        gc.refresh_from_db()
        assert gc.current_balance.amount == Decimal("0.00"), "Setup: GC balance must be $0"

        from catalog.services.gift_card_tender_service import (
            GiftCardTenderError,
            GiftCardTenderService,
            InsufficientGiftCardBalance,
        )

        session = CheckoutSessionFactory(cart=cart)
        # `is_valid` may reject a drained card outright, otherwise the available
        # balance check does — either is a correct refusal.
        with pytest.raises((GiftCardTenderError, InsufficientGiftCardBalance)):
            GiftCardTenderService.authorize_for_session(session, gc.code)

    def test_process_voucher_usage_for_guest_user(self, site_settings):
        """_process_voucher_usage should handle guest (unauthenticated) users."""
        from cart.services.checkout_service import CheckoutService
        from vouchers.models import VoucherUsage

        # Create a guest-like cart (user with guest prefix)
        guest = UserFactory(username="guest_test123")
        cart = _create_cart_with_items(guest, price=Decimal("50.00"))

        voucher = VoucherFactory(
            code="GUEST_V",
            discount_type="fixed",
            discount_value=Decimal("5.00"),
        )
        cart.apply_voucher("GUEST_V")

        order = OrderFactory(user=guest)
        CheckoutService._process_voucher_usage(cart, order)

        usage = VoucherUsage.objects.filter(voucher=voucher, order=order).first()
        assert usage is not None
        # Guest user should be recorded
        assert usage.user == guest
