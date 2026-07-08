"""
Order Service - Business logic for order operations
"""
from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from typing import Tuple, Optional, List, Dict, Any
from decimal import Decimal
from ..models import Order, OrderItem


class OrderService:
    """Service class for order operations"""

    # Order statuses that allow cancellation
    CANCELABLE_STATUSES = ['pending', 'processing']

    # Order statuses that are considered "completed"
    COMPLETED_STATUSES = ['delivered']

    # Time window for cancellation (in hours)
    CANCELLATION_WINDOW_HOURS = 24

    @staticmethod
    def get_order_history(
        user,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> QuerySet:
        """
        Get order history for user

        Args:
            user: User instance
            status: Filter by order status (optional)
            limit: Limit number of results (optional)

        Returns:
            QuerySet of Order objects
        """
        queryset = Order.objects.filter(user=user).select_related(
            'user'
        ).prefetch_related(
            'items__product',
            'items__variant'
        )

        if status:
            queryset = queryset.filter(status=status)

        if limit:
            queryset = queryset[:limit]

        return queryset

    @staticmethod
    def get_order_detail(order_number: str, user) -> Optional[Order]:
        """
        Get detailed order information

        Args:
            order_number: Order number
            user: User instance (for permission check)

        Returns:
            Order instance or None
        """
        try:
            order = Order.objects.select_related('user').prefetch_related(
                'items__product',
                'items__variant'
            ).get(order_number=order_number)

            # Check permission - user must own the order or be staff
            if order.user != user and not user.is_staff:
                return None

            return order

        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_order_statistics(user) -> Dict[str, Any]:
        """
        Get order statistics for user

        Args:
            user: User instance

        Returns:
            Dict with order statistics
        """
        orders = Order.objects.filter(user=user)

        total_orders = orders.count()
        total_spent = sum(
            float(order.total_amount) for order in orders
        )

        # Get status breakdown
        status_counts = {}
        for status, _ in Order.STATUS_CHOICES:
            count = orders.filter(status=status).count()
            if count > 0:
                status_counts[status] = count

        # Get recent orders
        recent_orders = orders.order_by('-created_at')[:5]

        # Calculate average order value
        avg_order_value = total_spent / total_orders if total_orders > 0 else 0

        return {
            'total_orders': total_orders,
            'total_spent': total_spent,
            'average_order_value': avg_order_value,
            'status_breakdown': status_counts,
            'recent_orders': [
                {
                    'order_number': order.order_number,
                    'total_amount': float(order.total_amount),
                    'status': order.status,
                    'created_at': order.created_at.isoformat()
                }
                for order in recent_orders
            ]
        }

    @staticmethod
    @transaction.atomic
    def cancel_order(
        order: Order,
        user,
        reason: str = "",
        restore_stock: bool = True
    ) -> Tuple[bool, str]:
        """
        Cancel an order

        Args:
            order: Order instance
            user: User requesting cancellation (for permission check)
            reason: Cancellation reason (optional)
            restore_stock: Whether to restore product stock (default: True)

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check permission
        if order.user != user and not user.is_staff:
            return False, _("You don't have permission to cancel this order")

        # Check if order can be cancelled
        if order.status not in OrderService.CANCELABLE_STATUSES:
            return False, _("Order cannot be cancelled in current status: {status}").format(
                status=order.get_status_display()
            )

        # Check cancellation time window (only for customers, not staff)
        if not user.is_staff:
            time_since_order = timezone.now() - order.created_at
            if time_since_order > timedelta(hours=OrderService.CANCELLATION_WINDOW_HOURS):
                return False, _("Cancellation window has expired. Please contact support.")

        # Restore stock if requested - use multi-location inventory system
        if restore_stock:
            from catalog.services import fulfillment_service
            import logging
            logger = logging.getLogger(__name__)

            for item in order.items.all():
                # If stock was allocated but not yet fulfilled, release it
                if item.stock_allocated and not item.stock_fulfilled and item.warehouse:
                    try:
                        fulfillment_service.release_stock(
                            order_item=item,
                            warehouse=item.warehouse
                        )
                        # Mark as no longer allocated
                        item.stock_allocated = False
                        item.save(update_fields=['stock_allocated'])
                        logger.info(
                            f"Released stock for {item.sku} at {item.warehouse.code} "
                            f"(Order: {order.order_number})"
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to release stock for {item.sku} at {item.warehouse.code}: {e}"
                        )
                        # Continue with cancellation even if stock release fails
                elif item.stock_fulfilled:
                    # Stock already fulfilled (shipped) - cannot automatically restore
                    # This would need manual inventory adjustment
                    logger.warning(
                        f"Cannot auto-restore stock for {item.sku} - already fulfilled/shipped. "
                        f"Manual inventory adjustment may be required."
                    )
                elif not item.warehouse:
                    # No warehouse assigned - this shouldn't happen in multi-location inventory
                    # Log a warning but continue with cancellation
                    logger.warning(
                        f"Order item {item.id} has no warehouse assigned. "
                        f"Cannot restore stock for {item.sku}. Manual adjustment may be required."
                    )

        # Update order status
        old_status = order.status
        order.status = 'cancelled'

        # Store cancellation reason in notes
        if reason:
            cancellation_note = f"\n\n[Cancelled by {user.username} on {timezone.now()}]\nReason: {reason}"
            order.notes += cancellation_note

        order.save()

        return True, _("Order cancelled successfully")

    @staticmethod
    @transaction.atomic
    def reorder(order: Order, user) -> Tuple[bool, str, Optional['Cart']]:
        """
        Create a new cart from a previous order

        Args:
            order: Order instance to reorder
            user: User instance (for permission check)

        Returns:
            Tuple of (success: bool, message: str, cart: Cart or None)
        """
        from cart.models import Cart, CartItem
        from cart.services import CartService

        # Check permission
        if order.user != user and not user.is_staff:
            return False, _("You don't have permission to reorder this order"), None

        # Get or create cart for user
        cart = CartService.get_or_create_cart(user=user)

        items_added = 0
        items_unavailable = []

        for order_item in order.items.all():
            # Check if product still exists and is available
            if not order_item.product:
                items_unavailable.append(order_item.product_name)
                continue

            # Check if variant still exists (if applicable)
            variant = order_item.variant
            if order_item.variant_name and not variant:
                items_unavailable.append(f"{order_item.product_name} - {order_item.variant_name}")
                continue

            # Check stock availability using multi-location inventory
            product = order_item.product
            if product.track_inventory:
                from catalog.services import fulfillment_service

                # Check stock availability in user's region
                region = None
                if user and hasattr(user, 'sales_region'):
                    region = user.sales_region

                availability = fulfillment_service.check_stock_availability(
                    product=product,
                    quantity=order_item.quantity,
                    region=region,
                    variant=variant
                )

                if not availability['available']:
                    if variant:
                        items_unavailable.append(f"{order_item.product_name} - {order_item.variant_name} (out of stock)")
                    else:
                        items_unavailable.append(f"{order_item.product_name} (out of stock)")
                    continue

            # Add item to cart
            success, message, cart_item = CartService.add_item(
                cart=cart,
                product_id=order_item.product.id,
                quantity=order_item.quantity,
                variant_id=variant.id if variant else None,
                customizations=order_item.customizations
            )

            if success:
                items_added += 1
            else:
                items_unavailable.append(f"{order_item.product_name} ({message})")

        # Prepare response message
        if items_added == 0:
            return False, _("No items could be added to cart"), None

        message = _("{count} items added to cart").format(count=items_added)
        if items_unavailable:
            message += ". " + _("Unavailable items: {items}").format(
                items=", ".join(items_unavailable)
            )

        return True, message, cart

    @staticmethod
    @transaction.atomic
    def update_order_status(
        order: Order,
        new_status: str,
        user,
        tracking_number: str = "",
        notes: str = ""
    ) -> Tuple[bool, str]:
        """
        Update order status (staff only)

        Args:
            order: Order instance
            new_status: New status value
            user: User making the update (must be staff)
            tracking_number: Tracking number (optional)
            notes: Status update notes (optional)

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check permission - must be staff
        if not user.is_staff:
            return False, _("Only staff can update order status")

        # Validate status
        valid_statuses = [status[0] for status in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return False, _("Invalid order status")

        old_status = order.status
        order.status = new_status

        # Update tracking number if provided
        if tracking_number:
            order.tracking_number = tracking_number

        # Add status update note
        if notes:
            status_note = f"\n\n[Status updated by {user.username} on {timezone.now()}]\n{old_status} → {new_status}\n{notes}"
            order.notes += status_note

        order.save()

        return True, _("Order status updated successfully")

    @staticmethod
    def get_tracking_info(order: Order, user) -> Optional[Dict[str, Any]]:
        """
        Get order tracking information

        Args:
            order: Order instance
            user: User instance (for permission check)

        Returns:
            Dict with tracking info or None
        """
        # Check permission
        if order.user != user and not user.is_staff:
            return None

        # Calculate estimated delivery (placeholder - should integrate with shipping provider)
        estimated_delivery = None
        if order.status == 'shipped' and order.tracking_number:
            # This is a placeholder - real implementation would call shipping API
            estimated_delivery = (timezone.now() + timedelta(days=3)).date().isoformat()

        return {
            'order_number': order.order_number,
            'status': order.status,
            'status_display': order.get_status_display(),
            'tracking_number': order.tracking_number,
            'estimated_delivery': estimated_delivery,
            'shipping_address': {
                'name': order.shipping_name,
                'address1': order.shipping_address1,
                'address2': order.shipping_address2,
                'city': order.shipping_city,
                'state': order.shipping_state,
                'postal_code': order.shipping_postal_code,
                'country': order.shipping_country
            },
            'timeline': [
                {
                    'status': 'pending',
                    'date': order.created_at.isoformat(),
                    'completed': True
                },
                {
                    'status': 'processing',
                    'date': order.updated_at.isoformat() if order.status != 'pending' else None,
                    'completed': order.status not in ['pending']
                },
                {
                    'status': 'shipped',
                    'date': order.updated_at.isoformat() if order.status in ['shipped', 'delivered'] else None,
                    'completed': order.status in ['shipped', 'delivered']
                },
                {
                    'status': 'delivered',
                    'date': order.updated_at.isoformat() if order.status == 'delivered' else None,
                    'completed': order.status == 'delivered'
                }
            ]
        }

    @staticmethod
    def can_cancel_order(order: Order, user) -> Tuple[bool, str]:
        """
        Check if order can be cancelled

        Args:
            order: Order instance
            user: User instance

        Returns:
            Tuple of (can_cancel: bool, reason: str)
        """
        # Check permission
        if order.user != user and not user.is_staff:
            return False, _("You don't have permission to cancel this order")

        # Check status
        if order.status not in OrderService.CANCELABLE_STATUSES:
            return False, _("Order cannot be cancelled in current status")

        # Check time window (only for customers)
        if not user.is_staff:
            time_since_order = timezone.now() - order.created_at
            if time_since_order > timedelta(hours=OrderService.CANCELLATION_WINDOW_HOURS):
                return False, _("Cancellation window has expired")

        return True, _("Order can be cancelled")
