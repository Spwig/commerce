"""
Tests for SegmentEvaluator service

Tests dynamic segment evaluation and membership management.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money

from loyalty.models import (
    LoyaltyBalance,
    LoyaltyMember,
    LoyaltyRedemption,
    LoyaltyReward,
    LoyaltySegment,
    LoyaltySegmentMembership,
    LoyaltyTier,
)
from loyalty.services.segment_evaluator import SegmentEvaluator
from orders.models import Order

User = get_user_model()


class SegmentEvaluatorTestCase(TestCase):
    """Test segment evaluation and membership management"""

    def setUp(self):
        """Set up test data"""
        self.evaluator = SegmentEvaluator()

        # Create tiers
        self.bronze_tier = LoyaltyTier.objects.create(
            name="Bronze",
            slug="bronze",
            rank=10,
            min_points_earned=0,
            points_multiplier=1.0,
            is_active=True,
        )

        self.silver_tier = LoyaltyTier.objects.create(
            name="Silver",
            slug="silver",
            rank=5,
            min_points_earned=1000,
            points_multiplier=1.25,
            is_active=True,
        )

        self.gold_tier = LoyaltyTier.objects.create(
            name="Gold",
            slug="gold",
            rank=1,
            min_points_earned=5000,
            points_multiplier=1.5,
            is_active=True,
        )

        # Create test users and members
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="testpass123"
        )
        self.member1 = LoyaltyMember.objects.get(customer=self.user1)
        self.member1.current_tier = self.bronze_tier
        self.member1.save()

        self.balance1, _ = LoyaltyBalance.objects.get_or_create(
            member=self.member1,
            defaults={
                "available_points": 500,
                "pending_points": 0,
                "lifetime_earned": 500,
                "lifetime_redeemed": 0,
            },
        )
        self.balance1.available_points = 500
        self.balance1.lifetime_earned = 500
        self.balance1.save()

        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )
        self.member2 = LoyaltyMember.objects.get(customer=self.user2)
        self.member2.current_tier = self.silver_tier
        self.member2.save()

        self.balance2, _ = LoyaltyBalance.objects.get_or_create(
            member=self.member2,
            defaults={
                "available_points": 2000,
                "pending_points": 0,
                "lifetime_earned": 2000,
                "lifetime_redeemed": 0,
            },
        )
        self.balance2.available_points = 2000
        self.balance2.lifetime_earned = 2000
        self.balance2.save()

        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="testpass123"
        )
        self.member3 = LoyaltyMember.objects.get(customer=self.user3)
        self.member3.current_tier = self.gold_tier
        self.member3.save()

        self.balance3, _ = LoyaltyBalance.objects.get_or_create(
            member=self.member3,
            defaults={
                "available_points": 10000,
                "pending_points": 0,
                "lifetime_earned": 10000,
                "lifetime_redeemed": 0,
            },
        )
        self.balance3.available_points = 10000
        self.balance3.lifetime_earned = 10000
        self.balance3.save()

    def test_tier_based_segment(self):
        """Test segment filtering by tier"""
        segment = LoyaltySegment.objects.create(
            name="Gold Members",
            slug="gold-members",
            criteria_type="dynamic",
            criteria_config={"tier_id": self.gold_tier.id},
            is_active=True,
        )

        # Evaluate members
        self.assertTrue(self.evaluator.evaluate_member_for_segment(self.member3, segment))
        self.assertFalse(self.evaluator.evaluate_member_for_segment(self.member1, segment))
        self.assertFalse(self.evaluator.evaluate_member_for_segment(self.member2, segment))

        # Get qualifying members
        qualifying = self.evaluator.get_segment_members(segment)
        self.assertEqual(len(qualifying), 1)
        self.assertIn(self.member3, qualifying)

    def test_points_based_segment(self):
        """Test segment filtering by point ranges"""
        segment = LoyaltySegment.objects.create(
            name="Mid-Range Points",
            slug="mid-range-points",
            criteria_type="dynamic",
            criteria_config={"min_points": 1000, "max_points": 5000},
            is_active=True,
        )

        # Only member2 has 2000 points (between 1000 and 5000)
        self.assertFalse(
            self.evaluator.evaluate_member_for_segment(self.member1, segment)
        )  # 500 points
        self.assertTrue(
            self.evaluator.evaluate_member_for_segment(self.member2, segment)
        )  # 2000 points
        self.assertFalse(
            self.evaluator.evaluate_member_for_segment(self.member3, segment)
        )  # 10000 points

    def test_order_count_segment(self):
        """Test segment filtering by order count"""
        # Create orders
        Order.objects.create(
            user=self.user1,
            order_number="ORD-001",
            status="completed",
            subtotal=Money(100.00, "USD"),
            total_amount=Money(100.00, "USD"),
        )

        Order.objects.create(
            user=self.user2,
            order_number="ORD-002",
            status="completed",
            subtotal=Money(200.00, "USD"),
            total_amount=Money(200.00, "USD"),
        )

        Order.objects.create(
            user=self.user2,
            order_number="ORD-003",
            status="completed",
            subtotal=Money(300.00, "USD"),
            total_amount=Money(300.00, "USD"),
        )

        # Segment for members with at least 2 orders
        segment = LoyaltySegment.objects.create(
            name="Repeat Customers",
            slug="repeat-customers",
            criteria_type="dynamic",
            criteria_config={"min_orders": 2},
            is_active=True,
        )

        self.assertFalse(
            self.evaluator.evaluate_member_for_segment(self.member1, segment)
        )  # 1 order
        self.assertTrue(
            self.evaluator.evaluate_member_for_segment(self.member2, segment)
        )  # 2 orders
        self.assertFalse(
            self.evaluator.evaluate_member_for_segment(self.member3, segment)
        )  # 0 orders

    def test_total_spend_segment(self):
        """Test segment filtering by total spend"""
        # Create orders
        Order.objects.create(
            user=self.user1,
            order_number="ORD-004",
            status="completed",
            subtotal=Money(250.00, "USD"),
            total_amount=Money(250.00, "USD"),
        )

        Order.objects.create(
            user=self.user2,
            order_number="ORD-005",
            status="completed",
            subtotal=Money(600.00, "USD"),
            total_amount=Money(600.00, "USD"),
        )

        # Segment for big spenders (> $500)
        segment = LoyaltySegment.objects.create(
            name="Big Spenders",
            slug="big-spenders",
            criteria_type="dynamic",
            criteria_config={"min_spend": 500},
            is_active=True,
        )

        self.assertFalse(self.evaluator.evaluate_member_for_segment(self.member1, segment))  # $250
        self.assertTrue(self.evaluator.evaluate_member_for_segment(self.member2, segment))  # $600
        self.assertFalse(self.evaluator.evaluate_member_for_segment(self.member3, segment))  # $0

    def test_redemption_based_segment(self):
        """Test segment filtering by redemptions"""
        # Create reward
        reward = LoyaltyReward.objects.create(
            name="Test Reward",
            slug="test-reward",
            reward_type="discount",
            points_cost=100,
            is_active=True,
        )

        # Create redemption for member2
        LoyaltyRedemption.objects.create(
            member=self.member2, reward=reward, points_spent=100, status="fulfilled"
        )

        # Segment for members who have redeemed
        segment = LoyaltySegment.objects.create(
            name="Reward Redeemers",
            slug="reward-redeemers",
            criteria_type="dynamic",
            criteria_config={"has_redeemed": True},
            is_active=True,
        )

        self.assertFalse(
            self.evaluator.evaluate_member_for_segment(self.member1, segment)
        )  # No redemptions
        self.assertTrue(
            self.evaluator.evaluate_member_for_segment(self.member2, segment)
        )  # 1 redemption
        self.assertFalse(
            self.evaluator.evaluate_member_for_segment(self.member3, segment)
        )  # No redemptions

    def test_combined_rules_segment(self):
        """Test segment with multiple rules (AND logic)"""
        # Create orders for member2
        Order.objects.create(
            user=self.user2,
            order_number="ORD-006",
            status="completed",
            subtotal=Money(300.00, "USD"),
            total_amount=Money(300.00, "USD"),
        )

        # Segment: Silver tier AND 1000+ points AND at least 1 order
        segment = LoyaltySegment.objects.create(
            name="Active Silver Members",
            slug="active-silver",
            criteria_type="dynamic",
            criteria_config={"tier_id": self.silver_tier.id, "min_points": 1000, "min_orders": 1},
            is_active=True,
        )

        self.assertFalse(
            self.evaluator.evaluate_member_for_segment(self.member1, segment)
        )  # Wrong tier
        self.assertTrue(
            self.evaluator.evaluate_member_for_segment(self.member2, segment)
        )  # Matches all
        self.assertFalse(
            self.evaluator.evaluate_member_for_segment(self.member3, segment)
        )  # Wrong tier

    def test_refresh_segment_memberships(self):
        """Test refreshing segment memberships"""
        segment = LoyaltySegment.objects.create(
            name="High Points",
            slug="high-points",
            criteria_type="dynamic",
            criteria_config={"min_points": 1500},
            is_active=True,
        )

        # Initially, only member2 (2000 pts) and member3 (10000 pts) qualify
        result = self.evaluator.refresh_segment_memberships(segment)

        self.assertEqual(result["added"], 2)
        self.assertEqual(result["removed"], 0)
        self.assertEqual(result["total"], 2)

        # Verify memberships
        self.assertTrue(
            LoyaltySegmentMembership.objects.filter(segment=segment, member=self.member2).exists()
        )
        self.assertTrue(
            LoyaltySegmentMembership.objects.filter(segment=segment, member=self.member3).exists()
        )

        # Update member1's points to qualify
        self.balance1.available_points = 2000
        self.balance1.save()

        # Refresh again
        result = self.evaluator.refresh_segment_memberships(segment)

        self.assertEqual(result["added"], 1)  # member1 added
        self.assertEqual(result["removed"], 0)
        self.assertEqual(result["total"], 3)

        # Update member2's points to no longer qualify
        self.balance2.available_points = 500
        self.balance2.save()

        # Refresh again
        result = self.evaluator.refresh_segment_memberships(segment)

        self.assertEqual(result["added"], 0)
        self.assertEqual(result["removed"], 1)  # member2 removed
        self.assertEqual(result["total"], 2)

        # Verify final memberships
        self.assertTrue(
            LoyaltySegmentMembership.objects.filter(segment=segment, member=self.member1).exists()
        )
        self.assertFalse(
            LoyaltySegmentMembership.objects.filter(segment=segment, member=self.member2).exists()
        )
        self.assertTrue(
            LoyaltySegmentMembership.objects.filter(segment=segment, member=self.member3).exists()
        )

    def test_manual_segment_not_evaluated(self):
        """Test that manual segments are not auto-evaluated"""
        segment = LoyaltySegment.objects.create(
            name="Manual VIPs", slug="manual-vips", criteria_type="manual", is_active=True
        )

        # Manual segments should never qualify members automatically
        self.assertFalse(self.evaluator.evaluate_member_for_segment(self.member1, segment))
        self.assertFalse(self.evaluator.evaluate_member_for_segment(self.member2, segment))

        # Getting members should return empty for manual segments
        qualifying = self.evaluator.get_segment_members(segment)
        self.assertEqual(len(qualifying), 0)

    def test_add_member_to_segment(self):
        """Test manually adding a member to a segment"""
        segment = LoyaltySegment.objects.create(
            name="Test Segment", slug="test-segment", criteria_type="manual", is_active=True
        )

        # Add member
        membership = self.evaluator.add_member_to_segment(self.member1, segment)

        self.assertIsNotNone(membership)
        self.assertEqual(segment.member_count, 1)

        # Adding again should return None (already exists)
        membership2 = self.evaluator.add_member_to_segment(self.member1, segment)
        self.assertIsNone(membership2)
        self.assertEqual(segment.member_count, 1)

    def test_remove_member_from_segment(self):
        """Test manually removing a member from a segment"""
        segment = LoyaltySegment.objects.create(
            name="Test Segment", slug="test-segment", criteria_type="manual", is_active=True
        )

        # Add member
        self.evaluator.add_member_to_segment(self.member1, segment)

        # Remove member
        removed = self.evaluator.remove_member_from_segment(self.member1, segment)

        self.assertTrue(removed)
        self.assertEqual(segment.member_count, 0)

        # Removing again should return False (not found)
        removed2 = self.evaluator.remove_member_from_segment(self.member1, segment)
        self.assertFalse(removed2)

    def test_inactive_segment_not_evaluated(self):
        """Test that inactive segments are not evaluated"""
        segment = LoyaltySegment.objects.create(
            name="Inactive Segment",
            slug="inactive-segment",
            criteria_type="dynamic",
            criteria_config={"min_points": 0},
            is_active=False,  # Inactive
        )

        # Inactive segments should never qualify members
        self.assertFalse(self.evaluator.evaluate_member_for_segment(self.member1, segment))

    def test_empty_rules_segment(self):
        """Test segment with no rules configured"""
        segment = LoyaltySegment.objects.create(
            name="Empty Rules",
            slug="empty-rules",
            criteria_type="dynamic",
            criteria_config={},  # Empty rules
            is_active=True,
        )

        # Empty rules should not qualify anyone
        self.assertFalse(self.evaluator.evaluate_member_for_segment(self.member1, segment))

        qualifying = self.evaluator.get_segment_members(segment)
        self.assertEqual(len(qualifying), 0)
