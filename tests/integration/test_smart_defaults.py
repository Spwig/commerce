"""
Integration tests for Smart Defaults Service (Enhancement 5)

Tests the SmartDefaultsService engagement scoring and recommendation logic.
"""

import pytest
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

from accounts.models import CommunicationPreference
from accounts.services.smart_defaults_service import SmartDefaultsService
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.smart_defaults]


@pytest.fixture
def high_engagement_user(db):
    """Create user with high engagement (frequent orders, recent, high spend)"""
    from orders.models import Order

    user = UserFactory()

    # Create orders: 5 orders in last 90 days, total spent $2000
    for i in range(5):
        Order.objects.create(
            customer=user,
            status='completed',
            total=Decimal('400.00'),
            created_at=timezone.now() - timedelta(days=10 + i)
        )

    # Email verified and receiving marketing
    prefs = CommunicationPreference.get_or_create_for_user(user)[0]
    prefs.email_verified = True
    prefs.email_marketing = True
    prefs.save()

    return user


@pytest.fixture
def moderate_engagement_user(db):
    """Create user with moderate engagement"""
    from orders.models import Order

    user = UserFactory()

    # 2 orders in last 90 days, total spent $250
    for i in range(2):
        Order.objects.create(
            customer=user,
            status='completed',
            total=Decimal('125.00'),
            created_at=timezone.now() - timedelta(days=30 + i)
        )

    return user


@pytest.fixture
def low_engagement_user(db):
    """Create user with low engagement (1 old order, low spend)"""
    from orders.models import Order

    user = UserFactory()

    # 1 order over 180 days ago, spent $50
    Order.objects.create(
        customer=user,
        status='completed',
        total=Decimal('50.00'),
        created_at=timezone.now() - timedelta(days=200)
    )

    return user


@pytest.fixture
def new_user(db):
    """Create new user with no order history"""
    return UserFactory()


# =============================================================================
# Engagement Score Tests
# =============================================================================

def test_calculate_engagement_score_structure(high_engagement_user):
    """Test engagement score returns correct structure"""
    result = SmartDefaultsService.calculate_engagement_score(high_engagement_user)

    assert 'total_score' in result
    assert 'breakdown' in result

    # Check breakdown structure
    breakdown = result['breakdown']
    assert 'order_frequency' in breakdown
    assert 'recency' in breakdown
    assert 'customer_tier' in breakdown
    assert 'email_engagement' in breakdown


def test_calculate_engagement_score_high_engagement(high_engagement_user):
    """Test engagement score for highly engaged user"""
    result = SmartDefaultsService.calculate_engagement_score(high_engagement_user)

    # Should score highly across all dimensions
    # Order frequency: 5 orders in 90 days = 40 points (max)
    # Recency: within 30 days = 30 points (max)
    # Customer tier: $2000 spent = 20 points (VIP)
    # Email engagement: verified + opted in = 10 points
    # Total: 100 points

    assert result['total_score'] == 100.0

    breakdown = result['breakdown']
    assert breakdown['order_frequency']['score'] == 40.0
    assert breakdown['order_frequency']['orders_90d'] == 5
    assert breakdown['recency']['score'] == 30.0
    assert breakdown['customer_tier']['tier'] == 'VIP'
    assert breakdown['customer_tier']['score'] == 20.0
    assert breakdown['email_engagement']['score'] == 10.0


def test_calculate_engagement_score_moderate_engagement(moderate_engagement_user):
    """Test engagement score for moderately engaged user"""
    result = SmartDefaultsService.calculate_engagement_score(moderate_engagement_user)

    # Order frequency: 2 orders in 90 days = 20 points (50%)
    # Recency: within 90 days = 20 points (67%)
    # Customer tier: $250 spent = 10 points (Regular)
    # Email engagement: 0 (no verification)

    assert result['total_score'] == pytest.approx(50.0, abs=5)

    breakdown = result['breakdown']
    assert breakdown['order_frequency']['orders_90d'] == 2
    assert breakdown['customer_tier']['tier'] in ['Regular', 'High Value']


def test_calculate_engagement_score_low_engagement(low_engagement_user):
    """Test engagement score for low engagement user"""
    result = SmartDefaultsService.calculate_engagement_score(low_engagement_user)

    # Should score low across dimensions
    # Order frequency: 0 orders in 90 days = 10 points (25%)
    # Recency: over 180 days = 5.1 points (17%)
    # Customer tier: $50 spent = 5 points (New)
    # Email engagement: 0

    assert result['total_score'] < 30.0

    breakdown = result['breakdown']
    assert breakdown['order_frequency']['orders_90d'] == 0
    assert breakdown['customer_tier']['tier'] == 'New'
    assert breakdown['recency']['days_since_last_order'] > 180


def test_calculate_engagement_score_new_user(new_user):
    """Test engagement score for brand new user with no orders"""
    result = SmartDefaultsService.calculate_engagement_score(new_user)

    # Should have minimal score
    # Order frequency: 0 = 10 points
    # Recency: no orders = 0 points
    # Customer tier: $0 = 5 points
    # Email: 0

    assert result['total_score'] == pytest.approx(15.0, abs=2)

    breakdown = result['breakdown']
    assert breakdown['order_frequency']['orders_90d'] == 0
    assert breakdown['recency']['days_since_last_order'] is None
    assert breakdown['customer_tier']['total_spent'] == 0.0


# =============================================================================
# Frequency Recommendation Tests
# =============================================================================

def test_get_recommended_frequency_high_engagement(high_engagement_user):
    """Test frequency recommendation for high engagement (≥80 score)"""
    result = SmartDefaultsService.get_recommended_frequency(high_engagement_user)

    assert result['frequency'] == 'immediate'
    assert 'High engagement' in result['reasoning']
    assert result['engagement_score'] >= 80
    assert 'breakdown' in result


def test_get_recommended_frequency_moderate_engagement(moderate_engagement_user):
    """Test frequency recommendation for moderate engagement (50-79 score)"""
    result = SmartDefaultsService.get_recommended_frequency(moderate_engagement_user)

    assert result['frequency'] == 'weekly'
    assert 'Moderate engagement' in result['reasoning']
    assert 50 <= result['engagement_score'] < 80


def test_get_recommended_frequency_low_engagement(low_engagement_user):
    """Test frequency recommendation for low engagement (<50 score)"""
    result = SmartDefaultsService.get_recommended_frequency(low_engagement_user)

    assert result['frequency'] == 'monthly'
    assert 'Lower engagement' in result['reasoning']
    assert result['engagement_score'] < 50


# =============================================================================
# App Recommendation Tests
# =============================================================================

def test_get_app_recommendations_structure(high_engagement_user):
    """Test app recommendations returns all apps"""
    result = SmartDefaultsService.get_app_recommendations(high_engagement_user)

    assert 'blog' in result
    assert 'loyalty' in result
    assert 'referrals' in result
    assert 'affiliate' in result

    # Each app should have recommended and reason
    for app, data in result.items():
        assert 'recommended' in data
        assert 'reason' in data


def test_get_app_recommendations_blog_threshold():
    """Test blog recommendation threshold (≥2 orders)"""
    from orders.models import Order

    # User with 1 order - should NOT recommend blog
    user1 = UserFactory()
    Order.objects.create(customer=user1, status='completed', total=Decimal('50.00'))

    result1 = SmartDefaultsService.get_app_recommendations(user1)
    assert result1['blog']['recommended'] is False

    # User with 2 orders - SHOULD recommend blog
    user2 = UserFactory()
    for i in range(2):
        Order.objects.create(customer=user2, status='completed', total=Decimal('50.00'))

    result2 = SmartDefaultsService.get_app_recommendations(user2)
    assert result2['blog']['recommended'] is True


def test_get_app_recommendations_loyalty_threshold():
    """Test loyalty recommendation threshold (≥$100 spent)"""
    from orders.models import Order

    # User spent $99 - should NOT recommend
    user1 = UserFactory()
    Order.objects.create(customer=user1, status='completed', total=Decimal('99.00'))

    result1 = SmartDefaultsService.get_app_recommendations(user1)
    assert result1['loyalty']['recommended'] is False

    # User spent $100 - SHOULD recommend
    user2 = UserFactory()
    Order.objects.create(customer=user2, status='completed', total=Decimal('100.00'))

    result2 = SmartDefaultsService.get_app_recommendations(user2)
    assert result2['loyalty']['recommended'] is True


def test_get_app_recommendations_referrals_always():
    """Test referrals always recommended (win-win program)"""
    # Even new user should have referrals recommended
    user = UserFactory()

    result = SmartDefaultsService.get_app_recommendations(user)

    assert result['referrals']['recommended'] is True
    assert 'Win-win' in result['referrals']['reason']


def test_get_app_recommendations_affiliate_threshold():
    """Test affiliate recommendation (≥$500 spent AND ≥5 orders)"""
    from orders.models import Order

    # User with $500 but only 4 orders - should NOT recommend
    user1 = UserFactory()
    for i in range(4):
        Order.objects.create(customer=user1, status='completed', total=Decimal('125.00'))

    result1 = SmartDefaultsService.get_app_recommendations(user1)
    assert result1['affiliate']['recommended'] is False

    # User with $600 and 5 orders - SHOULD recommend
    user2 = UserFactory()
    for i in range(5):
        Order.objects.create(customer=user2, status='completed', total=Decimal('120.00'))

    result2 = SmartDefaultsService.get_app_recommendations(user2)
    assert result2['affiliate']['recommended'] is True


# =============================================================================
# Complete Recommendations Tests
# =============================================================================

def test_get_recommendations_for_preference_center_structure(high_engagement_user):
    """Test complete recommendations structure"""
    result = SmartDefaultsService.get_recommendations_for_preference_center(high_engagement_user)

    assert 'frequency' in result
    assert 'apps' in result
    assert 'show_suggestions' in result

    # Frequency should have complete data
    assert 'frequency' in result['frequency']
    assert 'reasoning' in result['frequency']
    assert 'engagement_score' in result['frequency']

    # Apps should have all 4 apps
    assert len(result['apps']) == 4


def test_get_recommendations_for_preference_center_show_suggestions():
    """Test show_suggestions flag"""
    user = UserFactory()

    result = SmartDefaultsService.get_recommendations_for_preference_center(user)

    # Should always show suggestions
    assert result['show_suggestions'] is True


def test_get_recommendations_for_preference_center_integration(high_engagement_user):
    """Test recommendations work end-to-end with real data"""
    result = SmartDefaultsService.get_recommendations_for_preference_center(high_engagement_user)

    # High engagement user should get immediate frequency
    assert result['frequency']['frequency'] == 'immediate'

    # Should recommend all apps (has 5 orders, $2000 spent)
    assert result['apps']['blog']['recommended'] is True
    assert result['apps']['loyalty']['recommended'] is True
    assert result['apps']['referrals']['recommended'] is True
    assert result['apps']['affiliate']['recommended'] is True


def test_recommendations_consistent_across_calls(moderate_engagement_user):
    """Test recommendations are consistent when called multiple times"""
    result1 = SmartDefaultsService.get_recommendations_for_preference_center(moderate_engagement_user)
    result2 = SmartDefaultsService.get_recommendations_for_preference_center(moderate_engagement_user)

    # Should get same frequency recommendation
    assert result1['frequency']['frequency'] == result2['frequency']['frequency']

    # Should get same app recommendations
    for app in ['blog', 'loyalty', 'referrals', 'affiliate']:
        assert result1['apps'][app]['recommended'] == result2['apps'][app]['recommended']


# =============================================================================
# Edge Cases
# =============================================================================

def test_engagement_score_handles_incomplete_data():
    """Test engagement scoring handles missing data gracefully"""
    user = UserFactory()
    # No orders, no preferences

    result = SmartDefaultsService.calculate_engagement_score(user)

    # Should not crash
    assert isinstance(result['total_score'], (int, float))
    assert result['total_score'] >= 0


def test_app_recommendations_with_only_pending_orders():
    """Test app recommendations ignore non-completed orders"""
    from orders.models import Order

    user = UserFactory()

    # Create pending orders (should not count)
    for i in range(5):
        Order.objects.create(customer=user, status='pending', total=Decimal('100.00'))

    result = SmartDefaultsService.get_app_recommendations(user)

    # Should not recommend blog (no completed orders)
    assert result['blog']['recommended'] is False
