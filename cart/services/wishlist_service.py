"""
Wishlist Service - Business logic for wishlist operations
"""
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from typing import Tuple, Optional
from ..models import Wishlist, WishlistItem
from catalog.models import Product, ProductVariant


class WishlistService:
    """Service class for wishlist operations"""

    @staticmethod
    def get_or_create_default_wishlist(user) -> Wishlist:
        """
        Get or create default wishlist for user

        Args:
            user: User instance

        Returns:
            Wishlist instance
        """
        wishlist, created = Wishlist.objects.get_or_create(
            user=user,
            name=_("My Wishlist"),
            defaults={'name': _("My Wishlist")}
        )
        return wishlist

    @staticmethod
    @transaction.atomic
    def add_item(
        wishlist: Wishlist,
        product_id: int,
        variant_id: Optional[int] = None,
        notes: str = "",
        priority: str = "medium",
        notify_when_available: bool = False,
        notify_when_on_sale: bool = False
    ) -> Tuple[bool, str, Optional[WishlistItem]]:
        """
        Add item to wishlist

        Args:
            wishlist: Wishlist instance
            product_id: Product ID
            variant_id: Product variant ID (optional)
            notes: Item notes
            priority: Priority level (low, medium, high)
            notify_when_available: Notify when back in stock
            notify_when_on_sale: Notify when on sale

        Returns:
            Tuple of (success: bool, message: str, wishlist_item: WishlistItem)
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return False, _("Product not found"), None

        variant = None
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product)
            except ProductVariant.DoesNotExist:
                return False, _("Product variant not found"), None

        # Check if item already exists
        existing_item = WishlistItem.objects.filter(
            wishlist=wishlist,
            product=product,
            variant=variant
        ).first()

        if existing_item:
            # Update existing item
            existing_item.notes = notes
            existing_item.priority = priority
            existing_item.notify_when_available = notify_when_available
            existing_item.notify_when_on_sale = notify_when_on_sale
            existing_item.save()
            return True, _("Wishlist item updated"), existing_item

        # Create new item
        wishlist_item = WishlistItem.objects.create(
            wishlist=wishlist,
            product=product,
            variant=variant,
            notes=notes,
            priority=priority,
            notify_when_available=notify_when_available,
            notify_when_on_sale=notify_when_on_sale
        )

        return True, _("Item added to wishlist"), wishlist_item

    @staticmethod
    @transaction.atomic
    def remove_item(wishlist_item: WishlistItem) -> Tuple[bool, str]:
        """
        Remove item from wishlist

        Args:
            wishlist_item: WishlistItem instance

        Returns:
            Tuple of (success: bool, message: str)
        """
        wishlist_item.delete()
        return True, _("Item removed from wishlist")

    @staticmethod
    @transaction.atomic
    def move_to_cart(wishlist_item: WishlistItem, cart, quantity: int = 1) -> Tuple[bool, str]:
        """
        Move wishlist item to cart

        Args:
            wishlist_item: WishlistItem instance
            cart: Cart instance
            quantity: Quantity to add to cart

        Returns:
            Tuple of (success: bool, message: str)
        """
        from .cart_service import CartService

        success, message, cart_item = CartService.add_item(
            cart=cart,
            product_id=wishlist_item.product.id,
            quantity=quantity,
            variant_id=wishlist_item.variant.id if wishlist_item.variant else None
        )

        if success:
            wishlist_item.delete()
            return True, _("Item moved to cart")

        return False, message

    @staticmethod
    @transaction.atomic
    def clear_wishlist(wishlist: Wishlist) -> Tuple[bool, str]:
        """
        Clear all items from wishlist

        Args:
            wishlist: Wishlist instance

        Returns:
            Tuple of (success: bool, message: str)
        """
        wishlist.items.all().delete()
        return True, _("Wishlist cleared")

    @staticmethod
    def create_wishlist(user, name: str, is_public: bool = False) -> Tuple[bool, str, Optional[Wishlist]]:
        """
        Create new wishlist for user

        Args:
            user: User instance
            name: Wishlist name
            is_public: Whether wishlist is publicly shareable

        Returns:
            Tuple of (success: bool, message: str, wishlist: Wishlist)
        """
        # Check if wishlist with same name already exists
        if Wishlist.objects.filter(user=user, name=name).exists():
            return False, _("Wishlist with this name already exists"), None

        wishlist = Wishlist.objects.create(
            user=user,
            name=name,
            is_public=is_public
        )

        # Generate share slug if public
        if is_public:
            import uuid
            wishlist.share_slug = str(uuid.uuid4())[:8]
            wishlist.save(update_fields=['share_slug'])

        return True, _("Wishlist created"), wishlist

    @staticmethod
    def get_public_wishlist(share_slug: str) -> Optional[Wishlist]:
        """
        Get public wishlist by share slug

        Args:
            share_slug: Wishlist share slug

        Returns:
            Wishlist instance or None
        """
        try:
            return Wishlist.objects.get(share_slug=share_slug, is_public=True)
        except Wishlist.DoesNotExist:
            return None
