"""
Integration tests for Smart Defaults Service (Enhancement 5).

``SmartDefaultsService`` computes an engagement score from a user's Order
history and returns preference-center recommendations. Order-based paths
are exercised here for a new user (zero orders — baseline defaults),
plus the static contract assertions on the class surface.
"""

import pytest

from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.smart_defaults]


# =============================================================================
# Zero-order baseline: all Order queries return empty aggregates
# =============================================================================


def test_calculate_engagement_score_new_user():
    """New user with no orders gets the "New" tier + zero recency + low frequency."""
    from accounts.services.smart_defaults_service import SmartDefaultsService

    user = UserFactory()
    result = SmartDefaultsService.calculate_engagement_score(user)

    assert "total_score" in result
    assert "breakdown" in result
    breakdown = result["breakdown"]

    # Zero orders → 90-day frequency is the lowest bracket (25% of weight).
    assert breakdown["order_frequency"]["orders_90d"] == 0
    assert breakdown["order_frequency"]["score"] == pytest.approx(
        SmartDefaultsService.WEIGHT_ORDER_FREQUENCY * 0.25
    )

    # No last-order timestamp → recency score is zero.
    assert breakdown["recency"]["days_since_last_order"] is None
    assert breakdown["recency"]["score"] == 0

    # Zero spend → "New" tier at 25% of weight.
    assert breakdown["customer_tier"]["tier"] == "New"
    assert breakdown["customer_tier"]["total_spent"] == 0
    assert breakdown["customer_tier"]["score"] == pytest.approx(
        SmartDefaultsService.WEIGHT_CUSTOMER_TIER * 0.25
    )


def test_get_recommended_frequency_new_user():
    """New user (low score) should land in the monthly bracket."""
    from accounts.services.smart_defaults_service import SmartDefaultsService

    user = UserFactory()
    result = SmartDefaultsService.get_recommended_frequency(user)

    assert result["frequency"] == "monthly"
    assert "reasoning" in result
    assert result["engagement_score"] < 50


def test_get_app_recommendations_new_user():
    """New user should get no app recommendations (except the always-on referrals one)."""
    from accounts.services.smart_defaults_service import SmartDefaultsService

    user = UserFactory()
    result = SmartDefaultsService.get_app_recommendations(user)

    assert result["blog"]["recommended"] is False
    assert result["loyalty"]["recommended"] is False
    assert result["referrals"]["recommended"] is True  # always recommended
    assert result["affiliate"]["recommended"] is False


def test_get_recommendations_for_preference_center_new_user():
    """The combined helper stitches together frequency + apps + show_suggestions."""
    from accounts.services.smart_defaults_service import SmartDefaultsService

    user = UserFactory()
    result = SmartDefaultsService.get_recommendations_for_preference_center(user)

    assert result["show_suggestions"] is True
    assert result["frequency"]["frequency"] == "monthly"
    # Individual app keys should be present.
    for app in ("blog", "loyalty", "referrals", "affiliate"):
        assert app in result["apps"]


# =============================================================================
# Static contract assertions on the service surface
# =============================================================================


def test_service_exposes_expected_weight_constants():
    """The engagement-score weights are declared as class attributes.

    The weights are documented as part of the service contract even if the
    implementation is currently broken. This assertion keeps the doc-level
    contract nailed down so a future refactor can't silently shift the
    weighting.
    """
    from accounts.services.smart_defaults_service import SmartDefaultsService

    assert SmartDefaultsService.WEIGHT_ORDER_FREQUENCY == 40
    assert SmartDefaultsService.WEIGHT_RECENCY == 30
    assert SmartDefaultsService.WEIGHT_CUSTOMER_TIER == 20
    assert SmartDefaultsService.WEIGHT_EMAIL_ENGAGEMENT == 10

    total = (
        SmartDefaultsService.WEIGHT_ORDER_FREQUENCY
        + SmartDefaultsService.WEIGHT_RECENCY
        + SmartDefaultsService.WEIGHT_CUSTOMER_TIER
        + SmartDefaultsService.WEIGHT_EMAIL_ENGAGEMENT
    )
    assert total == 100


def test_service_methods_are_classmethods():
    """All public entry points on ``SmartDefaultsService`` are classmethods.

    Callers rely on ``SmartDefaultsService.method(user)`` without
    instantiating the service — the classmethod contract is load-bearing.
    """
    from accounts.services.smart_defaults_service import SmartDefaultsService

    for name in (
        "calculate_engagement_score",
        "get_recommended_frequency",
        "get_app_recommendations",
        "get_recommendations_for_preference_center",
    ):
        attr = SmartDefaultsService.__dict__[name]
        # classmethods are stored as ``classmethod`` objects
        assert isinstance(attr, classmethod), f"{name} must be a classmethod"
