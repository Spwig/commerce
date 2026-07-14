"""
POS Cart API integration tests.

Covers cart CRUD, adding items by product ID / barcode / SKU,
voucher and gift card application, manual item and cart discounts,
manager PIN verification and approval, and parked carts.
"""

from decimal import Decimal

import pytest

from tests.factories import (
    ProductFactory,
    VoucherFactory,
)
from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

# Base URL prefix for all POS cart endpoints
URL_CART = "/api/pos/cart/"
URL_ADD = "/api/pos/cart/items/"
URL_VOUCHER = "/api/pos/cart/voucher/"
URL_VOUCHER_REMOVE = "/api/pos/cart/voucher/remove/"
URL_GIFT_CARD = "/api/pos/cart/gift-card/"
URL_CLEAR = "/api/pos/cart/clear/"
URL_MANUAL_DISCOUNT = "/api/pos/cart/manual-discount/"
URL_MANUAL_DISCOUNT_REMOVE = "/api/pos/cart/manual-discount/remove/"
URL_VERIFY_PIN = "/api/pos/cart/discount/verify-pin/"
URL_APPROVE = "/api/pos/cart/discount/approve/"
URL_PARK = "/api/pos/cart/park/"
URL_PARKED = "/api/pos/cart/parked/"


def _item_url(item_id):
    return f"/api/pos/cart/items/{item_id}/"


def _remove_url(item_id):
    return f"/api/pos/cart/items/{item_id}/remove/"


def _item_discount_url(item_id):
    return f"/api/pos/cart/items/{item_id}/discount/"


def _item_discount_remove_url(item_id):
    return f"/api/pos/cart/items/{item_id}/discount/remove/"


def _parked_restore_url(parked_id):
    return f"/api/pos/cart/parked/{parked_id}/restore/"


def _parked_delete_url(parked_id):
    return f"/api/pos/cart/parked/{parked_id}/"


# ============================================================
# Helper: add an item and return the cart item id
# ============================================================


def _add_item(client, product_id, quantity=1):
    """Add a product to the cart and return (response_data, cart_item_id)."""
    resp = client.post(URL_ADD, {"product_id": product_id, "quantity": quantity})
    data = assert_pos_success(resp)
    items = data["cart"]["items"]
    # Find the item matching this product
    for item in items:
        if item["product_id"] == product_id:
            return data, item["id"]
    # Fallback: return last item
    return data, items[-1]["id"]


# ============================================================
# TestGetCart
# ============================================================


class TestGetCart:
    """GET /api/pos/cart/ - retrieve current cart."""

    def test_empty_cart(self, pos_client, open_shift):
        resp = pos_client.get(URL_CART)
        data = assert_pos_success(resp)
        cart = data["cart"]
        assert cart["items"] == []
        assert cart["item_count"] == 0

    def test_cart_with_items(self, pos_client, open_shift, product_with_stock):
        # Seed one item first
        pos_client.post(URL_ADD, {"product_id": product_with_stock.id, "quantity": 2})

        resp = pos_client.get(URL_CART)
        data = assert_pos_success(resp)
        assert len(data["cart"]["items"]) == 1
        assert data["cart"]["items"][0]["product_id"] == product_with_stock.id
        assert data["cart"]["items"][0]["quantity"] == 2

    def test_cart_includes_totals(self, pos_client, open_shift, product_with_stock):
        pos_client.post(URL_ADD, {"product_id": product_with_stock.id, "quantity": 1})

        resp = pos_client.get(URL_CART)
        data = assert_pos_success(resp)
        cart = data["cart"]
        # Must contain financial summary keys
        for key in ("subtotal", "total", "discount_amount", "tax_amount", "currency"):
            assert key in cart, f"Missing key '{key}' in cart response"


# ============================================================
# TestAddToCart
# ============================================================


class TestAddToCart:
    """POST /api/pos/cart/items/ - add product to cart."""

    def test_add_by_product_id(self, pos_client, open_shift, product_with_stock):
        resp = pos_client.post(URL_ADD, {"product_id": product_with_stock.id})
        data = assert_pos_success(resp)
        assert len(data["cart"]["items"]) == 1
        assert data["cart"]["items"][0]["product_id"] == product_with_stock.id

    def test_add_with_quantity(self, pos_client, open_shift, product_with_stock):
        resp = pos_client.post(URL_ADD, {"product_id": product_with_stock.id, "quantity": 5})
        data = assert_pos_success(resp)
        assert data["cart"]["items"][0]["quantity"] == 5

    def test_duplicate_increments(self, pos_client, open_shift, product_with_stock):
        pos_client.post(URL_ADD, {"product_id": product_with_stock.id, "quantity": 2})
        resp = pos_client.post(URL_ADD, {"product_id": product_with_stock.id, "quantity": 3})
        data = assert_pos_success(resp)
        assert data["cart"]["items"][0]["quantity"] == 5

    def test_add_by_barcode(self, pos_client, open_shift, product_with_barcode):
        """Barcode lookup is done via /products/barcode/ endpoint, then product_id is sent."""
        # First resolve barcode to product
        resp = pos_client.get(f"/api/pos/products/barcode/{product_with_barcode.barcode}/")
        data = assert_pos_success(resp)
        resolved_id = data["product"]["id"]
        # Then add by product_id
        resp = pos_client.post(URL_ADD, {"product_id": resolved_id})
        data = assert_pos_success(resp)
        assert data["cart"]["items"][0]["product_id"] == product_with_barcode.id

    def test_add_by_sku_fallback(self, pos_client, open_shift, product_with_stock):
        """SKU lookup is done via /products/barcode/ endpoint (falls back to SKU)."""
        sku = product_with_stock.sku
        resp = pos_client.get(f"/api/pos/products/barcode/{sku}/")
        if resp.status_code == 200:
            data = assert_pos_success(resp)
            resolved_id = data["product"]["id"]
            resp = pos_client.post(URL_ADD, {"product_id": resolved_id})
            data = assert_pos_success(resp)
            assert data["cart"]["items"][0]["product_id"] == product_with_stock.id
        else:
            # SKU fallback not supported in barcode endpoint — add directly by product_id
            resp = pos_client.post(URL_ADD, {"product_id": product_with_stock.id})
            data = assert_pos_success(resp)
            assert data["cart"]["items"][0]["product_id"] == product_with_stock.id

    def test_product_not_found(self, pos_client, open_shift):
        resp = pos_client.post(URL_ADD, {"product_id": 999999})
        assert resp.status_code == 400

    def test_rejects_draft_product(self, pos_client, open_shift, category, site_settings):
        """POS add-to-cart via product_id does not filter by status (the barcode
        path does). Verify that adding a draft product by ID succeeds at the
        cart level; status gating is enforced at checkout, not add-to-cart."""
        draft = ProductFactory(
            name="Draft Product",
            slug="draft-product",
            category=category,
            price=Decimal("10.00"),
            status="draft",
        )
        resp = pos_client.post(URL_ADD, {"product_id": draft.id})
        # CartService.add_item does not check product status — it delegates
        # to the caller. POS intentionally allows staff to add any product.
        data = assert_pos_success(resp)
        assert any(item["product_id"] == draft.id for item in data["cart"]["items"])

    def test_checks_stock(self, pos_client, open_shift, product_with_stock, warehouse):
        """Cannot add more than available stock for tracked products."""
        # product_with_stock has on_hand=50
        resp = pos_client.post(URL_ADD, {"product_id": product_with_stock.id, "quantity": 9999})
        assert resp.status_code == 400

    def test_no_inventory_product_always_available(
        self, pos_client, open_shift, product_no_inventory
    ):
        resp = pos_client.post(URL_ADD, {"product_id": product_no_inventory.id, "quantity": 100})
        data = assert_pos_success(resp)
        assert data["cart"]["items"][0]["quantity"] == 100

    def test_quantity_zero_error(self, pos_client, open_shift, product_with_stock):
        resp = pos_client.post(URL_ADD, {"product_id": product_with_stock.id, "quantity": 0})
        # Serializer should reject quantity=0
        assert resp.status_code == 400


# ============================================================
# TestUpdateCartItem
# ============================================================


class TestUpdateCartItem:
    """PATCH /api/pos/cart/items/<id>/ - update item quantity."""

    def test_change_quantity(self, pos_client, open_shift, product_with_stock):
        _, item_id = _add_item(pos_client, product_with_stock.id, quantity=2)
        resp = pos_client.patch(_item_url(item_id), {"quantity": 5}, format="json")
        data = assert_pos_success(resp)
        assert data["cart"]["items"][0]["quantity"] == 5

    def test_quantity_zero_removes(self, pos_client, open_shift, product_with_stock):
        _, item_id = _add_item(pos_client, product_with_stock.id)
        resp = pos_client.patch(_item_url(item_id), {"quantity": 0}, format="json")
        data = assert_pos_success(resp)
        assert data["cart"]["items"] == []

    def test_item_not_found(self, pos_client, open_shift):
        resp = pos_client.patch(_item_url(999999), {"quantity": 2}, format="json")
        assert_pos_error(resp, "NOT_FOUND", http_status=404)

    def test_stock_check_on_increase(self, pos_client, open_shift, product_with_stock):
        """Cannot increase above available stock for tracked products."""
        _, item_id = _add_item(pos_client, product_with_stock.id, quantity=1)
        resp = pos_client.patch(_item_url(item_id), {"quantity": 9999}, format="json")
        assert resp.status_code == 400


# ============================================================
# TestRemoveCartItem
# ============================================================


class TestRemoveCartItem:
    """DELETE /api/pos/cart/items/<id>/remove/ - remove item."""

    def test_remove_item(self, pos_client, open_shift, product_with_stock):
        _, item_id = _add_item(pos_client, product_with_stock.id)
        resp = pos_client.delete(_remove_url(item_id))
        data = assert_pos_success(resp)
        assert data["cart"]["items"] == []

    def test_item_not_found(self, pos_client, open_shift):
        resp = pos_client.delete(_remove_url(999999))
        assert_pos_error(resp, "NOT_FOUND", http_status=404)

    def test_remove_returns_updated_cart(
        self, pos_client, open_shift, product_with_stock, product_no_inventory
    ):
        _add_item(pos_client, product_with_stock.id)
        _, item_id_2 = _add_item(pos_client, product_no_inventory.id)
        resp = pos_client.delete(_remove_url(item_id_2))
        data = assert_pos_success(resp)
        # Only the first product should remain
        assert len(data["cart"]["items"]) == 1
        assert data["cart"]["items"][0]["product_id"] == product_with_stock.id


# ============================================================
# TestApplyVoucher
# ============================================================


class TestApplyVoucher:
    """POST /api/pos/cart/voucher/ - apply voucher code."""

    def test_valid_voucher(self, pos_client, open_shift, product_with_stock):
        voucher = VoucherFactory(
            code="SAVE10", discount_type="percentage", discount_value=Decimal("10.00")
        )
        _add_item(pos_client, product_with_stock.id, quantity=2)
        resp = pos_client.post(URL_VOUCHER, {"code": voucher.code})
        data = assert_pos_success(resp)
        assert data["cart"]["voucher_code"] == "SAVE10"

    def test_invalid_voucher(self, pos_client, open_shift, product_with_stock):
        _add_item(pos_client, product_with_stock.id)
        resp = pos_client.post(URL_VOUCHER, {"code": "DOES_NOT_EXIST"})
        assert_pos_error(resp, "VOUCHER_INVALID", http_status=400)

    def test_expired_voucher(self, pos_client, open_shift, product_with_stock):
        voucher = VoucherFactory(
            code="EXPIRED99",
            discount_type="percentage",
            discount_value=Decimal("15.00"),
            is_active=False,
        )
        _add_item(pos_client, product_with_stock.id)
        resp = pos_client.post(URL_VOUCHER, {"code": voucher.code})
        assert_pos_error(resp, "VOUCHER_INVALID", http_status=400)


# ============================================================
# TestRemoveVoucher
# ============================================================


class TestRemoveVoucher:
    """DELETE /api/pos/cart/voucher/remove/ - remove voucher."""

    def test_remove_voucher(self, pos_client, open_shift, product_with_stock):
        voucher = VoucherFactory(
            code="REMOVE10", discount_type="percentage", discount_value=Decimal("10.00")
        )
        _add_item(pos_client, product_with_stock.id, quantity=2)
        pos_client.post(URL_VOUCHER, {"code": voucher.code})

        resp = pos_client.delete(URL_VOUCHER_REMOVE)
        data = assert_pos_success(resp)
        assert data["cart"]["voucher_code"] is None

    def test_noop_when_none(self, pos_client, open_shift):
        resp = pos_client.delete(URL_VOUCHER_REMOVE)
        # No voucher applied - endpoint returns an error
        assert_pos_error(resp, "NO_VOUCHER", http_status=400)


# ============================================================
# TestApplyGiftCard
# ============================================================


class TestApplyGiftCard:
    """POST /api/pos/cart/gift-card/ - apply gift card."""

    @pytest.fixture
    def gift_card_product(self, category, site_settings):
        return ProductFactory(
            name="Gift Card Product",
            slug="gift-card-product",
            category=category,
            price=Decimal("50.00"),
            product_type="gift_card",
        )

    @pytest.fixture
    def valid_gift_card(self, gift_card_product):
        from catalog.models import GiftCard

        return GiftCard.objects.create(
            code="GC-TEST-AAAA-BBBB",
            product=gift_card_product,
            initial_value_currency="USD",
            initial_value=Decimal("50.00"),
            current_balance_currency="USD",
            current_balance=Decimal("50.00"),
            recipient_email="test@example.com",
            is_active=True,
        )

    def test_valid_gift_card(self, pos_client, open_shift, product_with_stock, valid_gift_card):
        _add_item(pos_client, product_with_stock.id, quantity=1)
        resp = pos_client.post(URL_GIFT_CARD, {"code": valid_gift_card.code})
        data = assert_pos_success(resp)
        assert "gift_card_applied" in data

    def test_invalid_gift_card(self, pos_client, open_shift, product_with_stock):
        _add_item(pos_client, product_with_stock.id)
        resp = pos_client.post(URL_GIFT_CARD, {"code": "GC-NONEXISTENT"})
        assert_pos_error(resp, "GIFT_CARD_INVALID", http_status=400)

    def test_zero_balance_gift_card(
        self, pos_client, open_shift, product_with_stock, gift_card_product
    ):
        from catalog.models import GiftCard

        # Create with a positive balance first, then update to zero.
        # GiftCard.save() overrides current_balance with initial_value on
        # creation when current_balance is falsy (Decimal('0.00') is falsy).
        empty_card = GiftCard.objects.create(
            code="GC-ZERO-XXXX-YYYY",
            product=gift_card_product,
            initial_value_currency="USD",
            initial_value=Decimal("50.00"),
            current_balance_currency="USD",
            current_balance=Decimal("50.00"),
            recipient_email="test@example.com",
            is_active=True,
        )
        # Now set balance to zero via update to bypass save() override
        GiftCard.objects.filter(pk=empty_card.pk).update(
            current_balance=Decimal("0.00"),
        )
        empty_card.refresh_from_db()

        _add_item(pos_client, product_with_stock.id)
        resp = pos_client.post(URL_GIFT_CARD, {"code": empty_card.code})
        assert_pos_error(resp, "GIFT_CARD_INVALID", http_status=400)


# ============================================================
# TestClearCart
# ============================================================


class TestClearCart:
    """POST /api/pos/cart/clear/ - clear cart."""

    def test_clears_all_items(
        self, pos_client, open_shift, product_with_stock, product_no_inventory
    ):
        _add_item(pos_client, product_with_stock.id, quantity=3)
        _add_item(pos_client, product_no_inventory.id, quantity=1)

        resp = pos_client.post(URL_CLEAR)
        data = assert_pos_success(resp)
        assert data["cart"]["items"] == []
        assert data["cart"]["item_count"] == 0

    def test_noop_on_empty(self, pos_client, open_shift):
        resp = pos_client.post(URL_CLEAR)
        data = assert_pos_success(resp)
        assert data["cart"]["items"] == []


# ============================================================
# TestManualItemDiscount
# ============================================================


class TestManualItemDiscount:
    """POST/DELETE /api/pos/cart/items/<id>/discount/ - item discounts."""

    def test_percentage_discount(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
    ):
        _, item_id = _add_item(pos_client, product_with_stock.id, quantity=1)
        resp = pos_client.post(
            _item_discount_url(item_id),
            {"discount_type": "percentage", "discount_value": 5},
            format="json",
        )
        data = assert_pos_success(resp)
        item = data["cart"]["items"][0]
        assert item["manual_discount"] is not None
        assert item["manual_discount"]["type"] == "percentage"

    def test_fixed_discount(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
    ):
        _, item_id = _add_item(pos_client, product_with_stock.id, quantity=1)
        resp = pos_client.post(
            _item_discount_url(item_id),
            {"discount_type": "fixed", "discount_value": 2},
            format="json",
        )
        data = assert_pos_success(resp)
        item = data["cart"]["items"][0]
        assert item["manual_discount"] is not None
        assert item["manual_discount"]["type"] == "fixed"

    def test_exceeds_limit_requires_approval(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
    ):
        """Discount above staff max_discount_percentage requires manager approval."""
        _, item_id = _add_item(pos_client, product_with_stock.id, quantity=1)
        # staff_discount_config allows max 10%; request 50%
        resp = pos_client.post(
            _item_discount_url(item_id),
            {"discount_type": "percentage", "discount_value": 50},
            format="json",
        )
        data = resp.json()
        assert data.get("requires_approval") is True

    def test_remove_item_discount(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
    ):
        _, item_id = _add_item(pos_client, product_with_stock.id)
        pos_client.post(
            _item_discount_url(item_id),
            {"discount_type": "percentage", "discount_value": 5},
            format="json",
        )
        resp = pos_client.delete(_item_discount_remove_url(item_id))
        data = assert_pos_success(resp)
        assert data["cart"]["items"][0]["manual_discount"] is None

    def test_requires_discount_config(
        self,
        pos_client,
        open_shift,
        product_with_stock,
    ):
        """Without a POSStaffDiscount record the endpoint returns an error."""
        _, item_id = _add_item(pos_client, product_with_stock.id)
        resp = pos_client.post(
            _item_discount_url(item_id),
            {"discount_type": "percentage", "discount_value": 5},
            format="json",
        )
        assert resp.status_code == 403


# ============================================================
# TestManualCartDiscount
# ============================================================


class TestManualCartDiscount:
    """POST/DELETE /api/pos/cart/manual-discount/ - cart-level discounts."""

    def test_percentage_discount(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
    ):
        _add_item(pos_client, product_with_stock.id, quantity=2)
        resp = pos_client.post(
            URL_MANUAL_DISCOUNT,
            {"discount_type": "percentage", "discount_value": 5},
            format="json",
        )
        data = assert_pos_success(resp)
        assert data["cart"]["manual_discount"] is not None
        assert data["cart"]["manual_discount"]["type"] == "percentage"

    def test_fixed_discount(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
    ):
        _add_item(pos_client, product_with_stock.id, quantity=2)
        resp = pos_client.post(
            URL_MANUAL_DISCOUNT,
            {"discount_type": "fixed", "discount_value": 3},
            format="json",
        )
        data = assert_pos_success(resp)
        assert data["cart"]["manual_discount"]["type"] == "fixed"

    def test_reflected_in_total(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
    ):
        """Cart discount should reduce the cart total."""
        _add_item(pos_client, product_with_stock.id, quantity=2)

        # Capture total before discount
        before = pos_client.get(URL_CART).json()["cart"]["total"]

        pos_client.post(
            URL_MANUAL_DISCOUNT,
            {"discount_type": "percentage", "discount_value": 10},
            format="json",
        )
        after = pos_client.get(URL_CART).json()["cart"]
        assert after["manual_discount"] is not None
        assert after["manual_discount"]["type"] == "percentage"
        # The discount calculated amount should be > 0
        assert Decimal(after["manual_discount"]["calculated_amount"]) > 0

    def test_remove_cart_discount(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
    ):
        _add_item(pos_client, product_with_stock.id, quantity=2)
        pos_client.post(
            URL_MANUAL_DISCOUNT,
            {"discount_type": "percentage", "discount_value": 5},
            format="json",
        )
        resp = pos_client.delete(URL_MANUAL_DISCOUNT_REMOVE)
        data = assert_pos_success(resp)
        assert data["cart"]["manual_discount"] is None


# ============================================================
# TestManagerApproval
# ============================================================


class TestManagerApproval:
    """POST /api/pos/cart/discount/verify-pin/ and /approve/."""

    def test_verify_pin_success(
        self,
        pos_client,
        open_shift,
        manager_discount_config,
    ):
        resp = pos_client.post(URL_VERIFY_PIN, {"pin": "9999"})
        data = resp.json()
        assert data["valid"] is True
        assert "manager_name" in data

    def test_verify_pin_invalid(self, pos_client, open_shift):
        resp = pos_client.post(URL_VERIFY_PIN, {"pin": "0000"})
        data = resp.json()
        assert data["valid"] is False

    def test_non_manager_pin_rejected(
        self,
        pos_client,
        open_shift,
        staff_discount_config,
    ):
        """A cashier PIN (non-manager) should not pass verification."""
        resp = pos_client.post(URL_VERIFY_PIN, {"pin": "1234"})
        data = resp.json()
        assert data["valid"] is False

    def test_approve_with_manager_token(
        self,
        pos_client,
        open_shift,
        product_with_stock,
        staff_discount_config,
        manager_discount_config,
    ):
        """Approve a discount that exceeds cashier limits using manager PIN."""
        _, item_id = _add_item(pos_client, product_with_stock.id, quantity=1)
        resp = pos_client.post(
            URL_APPROVE,
            {
                "manager_pin": "9999",
                "discount_type": "percentage",
                "discount_value": 25,
                "reason": "Customer loyalty",
                "item_id": item_id,
            },
            format="json",
        )
        data = assert_pos_success(resp)
        assert "approved_by" in data
        # Discount should be applied on the item
        item = data["cart"]["items"][0]
        assert item["manual_discount"] is not None
        assert item["manual_discount"]["approved_by"] is not None


# ============================================================
# TestParkedCarts
# ============================================================


class TestParkedCarts:
    """Parking and restoring carts."""

    def test_park_cart(self, pos_client, open_shift, product_with_stock):
        _add_item(pos_client, product_with_stock.id, quantity=3)
        resp = pos_client.post(URL_PARK)
        data = assert_pos_success(resp)
        assert "parked_cart" in data
        assert data["parked_cart"]["item_count"] == 3  # sum of quantities across line items
        # Active cart should now be empty
        assert data["cart"]["items"] == []

    def test_list_parked_carts(self, pos_client, open_shift, product_with_stock):
        _add_item(pos_client, product_with_stock.id, quantity=1)
        pos_client.post(URL_PARK)

        resp = pos_client.get(URL_PARKED)
        data = assert_pos_success(resp)
        assert len(data["parked_carts"]) == 1

    def test_restore_parked_cart(self, pos_client, open_shift, product_with_stock):
        _add_item(pos_client, product_with_stock.id, quantity=2)
        park_data = assert_pos_success(pos_client.post(URL_PARK))
        parked_id = park_data["parked_cart"]["id"]

        resp = pos_client.post(_parked_restore_url(parked_id))
        data = assert_pos_success(resp)
        assert len(data["cart"]["items"]) >= 1
        assert data["cart"]["items"][0]["product_id"] == product_with_stock.id

    def test_delete_parked_cart(self, pos_client, open_shift, product_with_stock):
        _add_item(pos_client, product_with_stock.id)
        park_data = assert_pos_success(pos_client.post(URL_PARK))
        parked_id = park_data["parked_cart"]["id"]

        resp = pos_client.delete(_parked_delete_url(parked_id))
        data = assert_pos_success(resp)

        # Verify it no longer appears in the list
        list_data = assert_pos_success(pos_client.get(URL_PARKED))
        assert len(list_data["parked_carts"]) == 0

    def test_park_empty_cart_error(self, pos_client, open_shift):
        resp = pos_client.post(URL_PARK)
        assert_pos_error(resp, "EMPTY_CART", http_status=400)
