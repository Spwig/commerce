"""
Audit Service for Admin API

Provides centralized audit logging for all admin API operations.
"""
import logging
from typing import Optional, Any
from django.http import HttpRequest

logger = logging.getLogger(__name__)


def get_client_ip(request: Optional[HttpRequest]) -> Optional[str]:
    """Extract client IP address from request."""
    if not request:
        return None

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class AuditService:
    """
    Service for creating audit log entries for admin API operations.

    Usage:
        AuditService.log(
            user=request.user,
            action='order.update_status',
            resource_type='order',
            resource_id=order.order_number,
            old_value={'status': 'pending'},
            new_value={'status': 'processing'},
            request=request
        )
    """

    @classmethod
    def log(
        cls,
        user,
        action: str,
        resource_type: str,
        resource_id: str,
        old_value: Optional[dict] = None,
        new_value: Optional[dict] = None,
        request: Optional[HttpRequest] = None,
        success: bool = True,
        error_message: str = ''
    ):
        """
        Create an audit log entry for an admin operation.

        Args:
            user: The user who performed the action
            action: Action identifier (e.g., 'order.update_status')
            resource_type: Type of resource (e.g., 'order', 'product')
            resource_id: ID of the affected resource
            old_value: Previous state (optional)
            new_value: New state (optional)
            request: HTTP request object (optional, for IP/device extraction)
            success: Whether the operation succeeded
            error_message: Error details if operation failed
        """
        from admin_api.models import AdminAPIAuditLog

        try:
            log_entry = AdminAPIAuditLog.objects.create(
                user=user,
                action=action,
                resource_type=resource_type,
                resource_id=str(resource_id),
                old_value=old_value or {},
                new_value=new_value or {},
                ip_address=get_client_ip(request),
                device_id=request.headers.get('X-Device-ID', '') if request else '',
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500] if request else '',
                success=success,
                error_message=error_message
            )
            return log_entry
        except Exception as e:
            # Log the error but don't fail the main operation
            logger.error(f"Failed to create audit log: {e}", exc_info=True)
            return None

    @classmethod
    def log_order_status_change(
        cls,
        user,
        order,
        old_status: str,
        new_status: str,
        request: Optional[HttpRequest] = None,
        tracking_number: str = '',
        notes: str = ''
    ):
        """Log an order status change."""
        old_value = {'status': old_status}
        new_value = {'status': new_status}

        if tracking_number:
            new_value['tracking_number'] = tracking_number
        if notes:
            new_value['notes'] = notes

        return cls.log(
            user=user,
            action='order.update_status',
            resource_type='order',
            resource_id=order.order_number,
            old_value=old_value,
            new_value=new_value,
            request=request
        )

    @classmethod
    def log_tracking_update(
        cls,
        user,
        order,
        old_tracking: str,
        new_tracking: str,
        carrier: str = '',
        request: Optional[HttpRequest] = None
    ):
        """Log a tracking number update."""
        old_value = {'tracking_number': old_tracking or ''}
        new_value = {'tracking_number': new_tracking}

        if carrier:
            new_value['carrier'] = carrier

        return cls.log(
            user=user,
            action='order.update_tracking',
            resource_type='order',
            resource_id=order.order_number,
            old_value=old_value,
            new_value=new_value,
            request=request
        )

    @classmethod
    def log_stock_adjustment(
        cls,
        user,
        product,
        warehouse_name: str,
        old_quantity: int,
        new_quantity: int,
        reason: str = '',
        request: Optional[HttpRequest] = None
    ):
        """Log a stock quantity adjustment."""
        return cls.log(
            user=user,
            action='product.adjust_stock',
            resource_type='product',
            resource_id=str(product.id),
            old_value={
                'quantity': old_quantity,
                'warehouse': warehouse_name
            },
            new_value={
                'quantity': new_quantity,
                'warehouse': warehouse_name,
                'reason': reason
            },
            request=request
        )

    @classmethod
    def log_product_status_change(
        cls,
        user,
        product,
        old_status: str,
        new_status: str,
        request: Optional[HttpRequest] = None
    ):
        """Log a product status change."""
        return cls.log(
            user=user,
            action='product.update_status',
            resource_type='product',
            resource_id=str(product.id),
            old_value={'status': old_status},
            new_value={'status': new_status},
            request=request
        )

    @classmethod
    def log_login(
        cls,
        user,
        device_id: str,
        device_name: str = '',
        request: Optional[HttpRequest] = None,
        success: bool = True,
        error_message: str = ''
    ):
        """Log a login attempt."""
        return cls.log(
            user=user,
            action='auth.login',
            resource_type='user',
            resource_id=str(user.id) if user else 'unknown',
            old_value={},
            new_value={
                'device_id': device_id,
                'device_name': device_name
            },
            request=request,
            success=success,
            error_message=error_message
        )

    @classmethod
    def log_logout(
        cls,
        user,
        device_id: str = '',
        logout_all: bool = False,
        request: Optional[HttpRequest] = None
    ):
        """Log a logout action."""
        return cls.log(
            user=user,
            action='auth.logout' if not logout_all else 'auth.logout_all',
            resource_type='user',
            resource_id=str(user.id),
            old_value={},
            new_value={
                'device_id': device_id,
                'logout_all': logout_all
            },
            request=request
        )

    # --- Catalog management audit methods ---

    @classmethod
    def log_product_create(cls, user, product, request=None):
        """Log a product creation."""
        return cls.log(
            user=user,
            action='product.create',
            resource_type='product',
            resource_id=str(product.id),
            new_value={
                'name': product.name,
                'sku': product.sku,
                'status': product.status,
                'product_type': product.product_type,
            },
            request=request
        )

    @classmethod
    def log_product_update(cls, user, product, old_values, new_values, request=None):
        """Log a product update with changed fields."""
        return cls.log(
            user=user,
            action='product.update',
            resource_type='product',
            resource_id=str(product.id),
            old_value=old_values,
            new_value=new_values,
            request=request
        )

    @classmethod
    def log_product_delete(cls, user, product, request=None):
        """Log a product deletion (soft delete)."""
        return cls.log(
            user=user,
            action='product.delete',
            resource_type='product',
            resource_id=str(product.id),
            old_value={'name': product.name, 'sku': product.sku},
            request=request
        )

    @classmethod
    def log_category_change(cls, user, action_suffix, category, old_value=None, new_value=None, request=None):
        """Log a category create/update/delete."""
        return cls.log(
            user=user,
            action=f'category.{action_suffix}',
            resource_type='category',
            resource_id=str(category.id),
            old_value=old_value or {},
            new_value=new_value or {},
            request=request
        )

    @classmethod
    def log_brand_change(cls, user, action_suffix, brand, old_value=None, new_value=None, request=None):
        """Log a brand create/update/delete."""
        return cls.log(
            user=user,
            action=f'brand.{action_suffix}',
            resource_type='brand',
            resource_id=str(brand.id),
            old_value=old_value or {},
            new_value=new_value or {},
            request=request
        )

    @classmethod
    def log_variant_change(cls, user, action_suffix, variant, old_value=None, new_value=None, request=None):
        """Log a variant create/update/delete."""
        return cls.log(
            user=user,
            action=f'variant.{action_suffix}',
            resource_type='variant',
            resource_id=str(variant.id),
            old_value=old_value or {},
            new_value=new_value or {},
            request=request
        )

    @classmethod
    def log_bulk_operation(cls, user, action, resource_type, created_count, error_count, request=None):
        """Log a bulk create/update operation."""
        return cls.log(
            user=user,
            action=action,
            resource_type=resource_type,
            resource_id='bulk',
            new_value={
                'created_count': created_count,
                'error_count': error_count,
            },
            request=request
        )
