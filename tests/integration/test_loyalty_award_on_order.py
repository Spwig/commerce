"""Regression: loyalty points award on a paid order.

`loyalty.services.award_order_points` looked up the member with
`LoyaltyMember.objects.get(user=order.user)`, but the field is `customer`.
That raised `FieldError` (not `DoesNotExist`), so it slipped past the
wrapper's `except DoesNotExist` and surfaced in
PaymentOrchestrationService as a logged "Failed to award loyalty points" —
points were silently never awarded on paid orders.
"""

import pytest

from tests.factories import OrderFactory, UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def test_award_order_points_resolves_member_without_fielderror():
    """An enrolled customer's paid order resolves the member and does not
    raise. (Before the fix this raised FieldError on the bad query keyword.)"""
    from loyalty.models import LoyaltyMember
    from loyalty.services import award_order_points

    user = UserFactory()
    # Non-staff users are auto-enrolled by a post_save signal; reconcile
    # rather than create (the OneToOne would otherwise IntegrityError).
    LoyaltyMember.objects.get_or_create(customer=user, defaults={"is_active": True})
    order = OrderFactory(user=user)

    # Must not raise. Returns a LoyaltyTransaction when a rule grants points,
    # or None when none apply — but never crashes the award path.
    result = award_order_points(order)
    assert result is None or result.member.customer_id == user.id


def test_award_order_points_skips_guest_order():
    """A guest order (no user) is skipped cleanly, not crashed."""
    from loyalty.services import award_order_points

    order = OrderFactory(user=None, email="guest@test.spwig.com")
    assert award_order_points(order) is None
