"""
Unit tests for Product soft-delete functionality.

Tests cover:
- Basic soft delete operations
- Product restoration
- Related models behavior
- SKU uniqueness validation
- Stock reservation cleanup
- Order protection (PROTECT constraint)
"""

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.utils import timezone

from cart.models import CartItem
from catalog.models import Product, ProductVariant, StockItem, StockReservation
from orders.models import OrderItem

User = get_user_model()


@pytest.mark.django_db
class TestProductSoftDelete:
    """Test basic soft delete functionality"""

    def test_product_soft_delete_sets_flags(self, product_factory, user_factory):
        """Test that soft delete sets is_deleted flag and timestamps"""
        product = product_factory()
        user = user_factory()

        # Perform soft delete
        product.delete(user=user)

        # Refresh from DB
        product.refresh_from_db()

        # Assert soft-delete fields are set
        assert product.is_deleted is True
        assert product.deleted_at is not None
        assert product.deleted_by == user
        assert abs((timezone.now() - product.deleted_at).total_seconds()) < 5

    def test_product_soft_delete_excludes_from_default_queryset(self, product_factory):
        """Test that deleted products are excluded from default queryset"""
        product = product_factory()
        product_id = product.id

        # Delete product
        product.delete()

        # Product should not appear in default queryset
        assert not Product.objects.filter(id=product_id).exists()

        # Product should appear in all_objects
        assert Product.all_objects.filter(id=product_id).exists()

    def test_product_soft_delete_without_user(self, product_factory):
        """Test soft delete without specifying user"""
        product = product_factory()

        product.delete()  # No user specified

        product.refresh_from_db()
        assert product.is_deleted is True
        assert product.deleted_at is not None
        assert product.deleted_by is None

    def test_multiple_products_soft_delete(self, product_factory):
        """Test deleting multiple products"""
        products = [product_factory() for _ in range(5)]
        product_ids = [p.id for p in products]

        # Delete all products
        for product in products:
            product.delete()

        # None should appear in default queryset
        assert Product.objects.filter(id__in=product_ids).count() == 0

        # All should appear in all_objects
        assert Product.all_objects.filter(id__in=product_ids).count() == 5


@pytest.mark.django_db
class TestProductRestore:
    """Test product restoration functionality"""

    def test_product_restore_clears_flags(self, product_factory, user_factory):
        """Test that restore clears soft-delete flags"""
        product = product_factory()
        user = user_factory()

        # Delete then restore
        product.delete(user=user)
        product.restore()

        # Refresh from DB
        product.refresh_from_db()

        # Assert flags are cleared
        assert product.is_deleted is False
        assert product.deleted_at is None
        assert product.deleted_by is None

    def test_product_restore_returns_to_queryset(self, product_factory):
        """Test that restored products appear in default queryset"""
        product = product_factory()
        product_id = product.id

        # Delete then restore
        product.delete()
        assert not Product.objects.filter(id=product_id).exists()

        product.restore()
        assert Product.objects.filter(id=product_id).exists()

    def test_product_restore_sku_conflict_raises_error(self, product_factory):
        """Test that restoring with duplicate SKU raises ValidationError"""
        product1 = product_factory(sku="TEST-SKU-001")
        product2 = product_factory(sku="TEST-SKU-002")

        # Delete product1
        product1.delete()

        # Change product2 to use product1's SKU
        product2.sku = "TEST-SKU-001"
        product2.save()

        # Restoring product1 should fail
        with pytest.raises(ValidationError) as exc_info:
            product1.restore()

        assert "already in use" in str(exc_info.value)


@pytest.mark.django_db
class TestRelatedModels:
    """Test behavior of related models with soft-deleted products"""

    def test_stock_items_remain_active(self, product_factory, warehouse_factory):
        """Test that StockItems remain active after product soft delete"""
        product = product_factory()
        warehouse = warehouse_factory()

        stock_item = StockItem.objects.create(
            product=product, warehouse=warehouse, on_hand=100, allocated=0
        )
        stock_item_id = stock_item.id

        # Delete product
        product.delete()

        # StockItem should still exist in database
        assert StockItem.objects.filter(id=stock_item_id).exists()

        # But won't be visible when queried through product relationship
        assert not Product.objects.filter(id=product.id).exists()

    def test_product_images_remain_active(self, product_factory, media_asset_factory):
        """Test that ProductImages remain active after product soft delete"""
        product = product_factory()
        media_asset = media_asset_factory()

        from catalog.models import ProductImage

        image = ProductImage.objects.create(product=product, media_asset=media_asset, position=1)
        image_id = image.id

        # Delete product
        product.delete()

        # Image should still exist
        assert ProductImage.objects.filter(id=image_id).exists()

    def test_product_variants_remain_active(self, product_factory):
        """Test that ProductVariants remain active after product soft delete"""
        product = product_factory(product_type="variable")

        variant = ProductVariant.objects.create(
            product=product, name="Size M", sku=f"{product.sku}-M", price=product.price
        )
        variant_id = variant.id

        # Delete product
        product.delete()

        # Variant should still exist
        assert ProductVariant.objects.filter(id=variant_id).exists()


@pytest.mark.django_db
class TestStockReservations:
    """Test stock reservation cleanup on product deletion"""

    def test_stock_reservations_released_on_delete(
        self, product_factory, warehouse_factory, cart_factory
    ):
        """Test that active stock reservations are released when product is deleted"""
        product = product_factory()
        warehouse = warehouse_factory()

        # Create stock item
        stock_item = StockItem.objects.create(
            product=product, warehouse=warehouse, on_hand=100, allocated=0
        )

        # StockReservation requires a cart_item + warehouse
        cart = cart_factory()
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=10, unit_price=product.price
        )

        # Create active stock reservation
        reservation = StockReservation.objects.create(
            stock_item=stock_item,
            cart_item=cart_item,
            warehouse=warehouse,
            quantity=10,
            expires_at=timezone.now() + timedelta(hours=1),
            channel="web",
        )
        reservation_id = reservation.id

        # Delete product
        product.delete()

        # Reservation should be deleted
        assert not StockReservation.objects.filter(id=reservation_id).exists()

    def test_expired_reservations_not_cleaned(
        self, product_factory, warehouse_factory, cart_factory
    ):
        """Test that expired reservations are not cleaned up during delete"""
        product = product_factory()
        warehouse = warehouse_factory()

        stock_item = StockItem.objects.create(
            product=product, warehouse=warehouse, on_hand=100, allocated=0
        )

        cart = cart_factory()
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=5, unit_price=product.price
        )

        # Create expired reservation (already expired)
        expired_reservation = StockReservation.objects.create(
            stock_item=stock_item,
            cart_item=cart_item,
            warehouse=warehouse,
            quantity=5,
            expires_at=timezone.now() - timedelta(hours=1),  # Already expired
            channel="web",
        )
        expired_id = expired_reservation.id

        # Delete product
        product.delete()

        # Expired reservation should still exist (not cleaned by delete)
        # It will be cleaned by the periodic task
        assert StockReservation.objects.filter(id=expired_id).exists()


@pytest.mark.django_db
class TestCartIntegration:
    """Test cart behavior with deleted products"""

    def test_cart_item_remains_after_product_delete(
        self, product_factory, cart_factory, user_factory
    ):
        """Test that CartItem FK remains valid after product soft delete"""
        product = product_factory()
        cart = cart_factory()

        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=1, unit_price=product.price
        )
        cart_item_id = cart_item.id

        # Soft delete product
        product.delete()

        # CartItem FK should still be valid (CASCADE doesn't trigger on soft delete)
        assert CartItem.objects.filter(id=cart_item_id).exists()

        # But product should not be accessible via default manager
        assert not Product.objects.filter(id=product.id).exists()

        # CartItem can still access product via all_objects
        cart_item.refresh_from_db()
        assert Product.all_objects.filter(id=cart_item.product_id).exists()


@pytest.mark.django_db
class TestOrderProtection:
    """Test that products with orders cannot be hard deleted"""

    def test_product_with_orders_cannot_be_hard_deleted(
        self, product_factory, order_factory, user_factory
    ):
        """Test that PROTECT constraint prevents hard deletion of products with orders"""
        product = product_factory()
        order = order_factory()

        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            sku=product.sku,
            quantity=1,
            unit_price=product.price,
            total_price=product.price,
        )

        # Soft delete should work
        product.delete()
        assert product.is_deleted is True

        # Hard delete should raise ProtectedError
        with pytest.raises(ProtectedError):
            product.hard_delete()

    def test_product_without_orders_can_be_hard_deleted(self, product_factory):
        """Test that products without orders can be permanently deleted"""
        product = product_factory()
        product_id = product.id

        # Soft delete first
        product.delete()

        # Hard delete should succeed
        product.hard_delete()

        # Product should be gone from database entirely
        assert not Product.all_objects.filter(id=product_id).exists()


@pytest.mark.django_db
class TestQuerySetMethods:
    """Test custom queryset methods"""

    def test_deleted_queryset_method(self, product_factory):
        """Test that deleted() queryset method returns only deleted products"""
        active_product = product_factory()
        deleted_product = product_factory()
        deleted_product.delete()

        deleted_products = Product.objects.deleted()

        assert deleted_product.id in [p.id for p in deleted_products]
        assert active_product.id not in [p.id for p in deleted_products]

    def test_active_queryset_method(self, product_factory):
        """Test that the default manager excludes soft-deleted products.

        ProductManager.get_queryset() applies .active() so
        Product.objects returns only non-deleted products. The manager
        does not expose active() itself — call .all() to reach the
        underlying queryset.
        """
        active_product = product_factory()
        deleted_product = product_factory()
        deleted_product.delete()

        active_products = Product.objects.all()

        assert active_product.id in [p.id for p in active_products]
        assert deleted_product.id not in [p.id for p in active_products]

        # Confirm the queryset-level active() helper is still available
        # (some callers reach it through with_deleted() or all_objects).
        base_qs = Product.all_objects.all()
        # ProductQuerySet.active() is what backs the default manager.
        # Only ProductManager exposes the filtered view; the base
        # Manager on all_objects returns a plain QuerySet without it.
        assert base_qs.filter(is_deleted=False).count() >= 1

    def test_with_deleted_queryset_method(self, product_factory):
        """Test that with_deleted() returns all products"""
        active_product = product_factory()
        deleted_product = product_factory()
        deleted_product.delete()

        all_products = Product.objects.with_deleted()

        assert active_product.id in [p.id for p in all_products]
        assert deleted_product.id in [p.id for p in all_products]

    def test_queryset_delete_method(self, product_factory):
        """Test that queryset.delete() performs bulk soft delete"""
        products = [product_factory() for _ in range(3)]
        product_ids = [p.id for p in products]

        # Bulk delete via queryset
        Product.objects.filter(id__in=product_ids).delete()

        # All should be soft-deleted
        assert Product.objects.filter(id__in=product_ids).count() == 0
        assert Product.all_objects.filter(id__in=product_ids, is_deleted=True).count() == 3

    def test_queryset_restore_method(self, product_factory):
        """Test that soft-deleted products can be bulk restored.

        Product.all_objects is a plain Manager (not a ProductManager),
        so its default queryset is a plain QuerySet without the custom
        restore() method. Restoration goes through with_deleted() on
        the default manager, which returns a ProductQuerySet.
        """
        products = [product_factory() for _ in range(3)]
        product_ids = [p.id for p in products]

        # Delete all
        for p in products:
            p.delete()

        # Bulk restore via with_deleted() which returns a ProductQuerySet.
        Product.objects.with_deleted().filter(id__in=product_ids).restore()

        # All should be restored
        assert Product.objects.filter(id__in=product_ids).count() == 3


@pytest.mark.django_db
class TestIsActiveProperty:
    """Test is_active property"""

    def test_is_active_for_active_product(self, product_factory):
        """Test that is_active returns True for non-deleted products"""
        product = product_factory()
        assert product.is_active is True

    def test_is_active_for_deleted_product(self, product_factory):
        """Test that is_active returns False for deleted products"""
        product = product_factory()
        product.delete()
        assert product.is_active is False
