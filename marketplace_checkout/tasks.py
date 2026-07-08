"""
Marketplace Checkout Celery Tasks

Handles async retry of entitlement grants that fail during payment processing.
Only active on spwig.com (SPWIG_IS_HQ=True).
"""

import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def retry_grant_entitlement(self, order_id):
    """
    Retry granting a marketplace component entitlement.

    Called when the initial grant fails during payment finalization.
    Retries up to 5 times with 60-second intervals.
    On success, clears the failure flag from order metadata.
    """
    from orders.models import Order
    from marketplace_checkout.services import grant_component_entitlement

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.error(f"Entitlement retry: order {order_id} not found")
        return

    try:
        grant_component_entitlement(order)
        # Clear failure flag on success
        order.metadata.pop('entitlement_grant_failed', None)
        order.metadata.pop('entitlement_grant_error', None)
        order.save(update_fields=['metadata'])
        logger.info(
            f"Entitlement retry succeeded for order {order.order_number} "
            f"(attempt {self.request.retries + 1})"
        )
    except Exception as e:
        logger.error(
            f"Entitlement retry {self.request.retries + 1} failed "
            f"for order {order.order_number}: {e}"
        )
        raise self.retry(exc=e)
