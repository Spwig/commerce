import logging

from loyalty.models import LoyaltyMember
from loyalty.services.points_engine import points_engine

logger = logging.getLogger(__name__)


def award_order_points(order):
    """
    Convenience wrapper called by PaymentOrchestrationService after payment.

    Looks up the LoyaltyMember for the order's user and delegates to the
    PointsEngine.  Silently skips guest orders or users without a membership.
    """
    if not order.user_id:
        return None

    try:
        member = LoyaltyMember.objects.get(user=order.user)
    except LoyaltyMember.DoesNotExist:
        return None

    return points_engine.award_order_points(order, member)
