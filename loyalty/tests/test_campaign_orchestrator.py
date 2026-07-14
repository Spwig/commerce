"""
Unit tests for Campaign Orchestrator Service
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from loyalty.models import (
    LoyaltyBalance,
    LoyaltyCampaign,
    LoyaltyCampaignExecution,
    LoyaltyMember,
    LoyaltyTier,
)
from loyalty.services.campaign_orchestrator import CampaignOrchestrator

User = get_user_model()


class CampaignOrchestratorTestCase(TestCase):
    """Test campaign orchestration logic"""

    def setUp(self):
        """Set up test data"""
        # Create test user (member is auto-created by signal)
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", first_name="Test", last_name="User"
        )

        # Get the auto-created member
        self.member = LoyaltyMember.objects.get(customer=self.user)

        # Ensure balance exists (get_or_create to be safe)
        self.balance, _ = LoyaltyBalance.objects.get_or_create(
            member=self.member,
            defaults={
                "available_points": 0,
                "pending_points": 0,
                "lifetime_earned": 0,
                "lifetime_redeemed": 0,
            },
        )

        # Create test tier
        self.tier = LoyaltyTier.objects.create(
            name="Bronze",
            slug="bronze",
            rank=10,
            min_points_earned=0,
            points_multiplier=1.0,
            is_active=True,
        )

        self.member.current_tier = self.tier
        self.member.save()

        # Create orchestrator
        self.orchestrator = CampaignOrchestrator()

    def test_trigger_event_creates_execution(self):
        """Test that triggering an event creates campaign execution"""
        # Create test campaign
        campaign = LoyaltyCampaign.objects.create(
            name="Test Campaign",
            slug="test-campaign",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            actions=[{"type": "award_points", "points": 100, "reason": "Test bonus"}],
        )

        # Trigger event
        result = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            member=self.member,
            context={"order_id": 123, "order_total": 99.99},
        )

        # Verify result
        self.assertEqual(result["triggered"], 1)
        self.assertEqual(result["skipped"], 0)

        # Verify execution created
        execution = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign, member=self.member
        ).first()
        self.assertIsNotNone(execution)
        self.assertEqual(execution.status, LoyaltyCampaignExecution.STATUS_PENDING)

    def test_trigger_conditions_min_order_amount(self):
        """Test trigger conditions with minimum order amount"""
        campaign = LoyaltyCampaign.objects.create(
            name="High Value Order Campaign",
            slug="high-value-order",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            trigger_conditions={"min_order_amount": 100.00},
            actions=[{"type": "award_points", "points": 500}],
        )

        # Test with order below minimum
        result_low = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            member=self.member,
            context={"order_total": 50.00},
        )
        self.assertEqual(result_low["triggered"], 0)
        self.assertEqual(result_low["skipped"], 1)

        # Test with order above minimum
        result_high = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            member=self.member,
            context={"order_total": 150.00},
        )
        self.assertEqual(result_high["triggered"], 1)

    def test_campaign_cooldown_period(self):
        """Test campaign cooldown prevents repeated triggers"""
        campaign = LoyaltyCampaign.objects.create(
            name="Cooldown Test Campaign",
            slug="cooldown-test",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            cooldown_days=7,
            actions=[{"type": "award_points", "points": 100}],
        )

        # First trigger - should succeed
        result1 = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result1["triggered"], 1)

        # Second trigger immediately - should be blocked by cooldown
        result2 = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result2["triggered"], 0)
        self.assertEqual(result2["skipped"], 1)

    def test_max_triggers_per_member(self):
        """Test max triggers per member limit"""
        campaign = LoyaltyCampaign.objects.create(
            name="Limited Trigger Campaign",
            slug="limited-trigger",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            max_triggers_per_member=2,
            actions=[{"type": "award_points", "points": 100}],
        )

        # Trigger 1 - should succeed
        result1 = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result1["triggered"], 1)

        # Trigger 2 - should succeed (now have 2 total)
        result2 = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result2["triggered"], 1)

        # Verify we now have 2 executions
        execution_count = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign, member=self.member
        ).count()
        self.assertEqual(execution_count, 2)

        # Trigger 3 - should be blocked (max 2 reached)
        result3 = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result3["triggered"], 0)

    def test_campaign_date_range(self):
        """Test campaign only triggers within date range"""
        # Campaign with future start date
        future_campaign = LoyaltyCampaign.objects.create(
            name="Future Campaign",
            slug="future-campaign",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            start_date=timezone.now() + timedelta(days=7),
            actions=[{"type": "award_points", "points": 100}],
        )

        result = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result["triggered"], 0)

        # Campaign with past end date
        past_campaign = LoyaltyCampaign.objects.create(
            name="Past Campaign",
            slug="past-campaign",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            end_date=timezone.now() - timedelta(days=7),
            actions=[{"type": "award_points", "points": 100}],
        )

        result = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result["triggered"], 0)

    def test_tier_targeting(self):
        """Test campaign targeting specific tiers"""
        # Create Gold tier
        gold_tier = LoyaltyTier.objects.create(
            name="Gold",
            slug="gold",
            rank=5,
            min_points_earned=1000,
            points_multiplier=1.5,
            is_active=True,
        )

        # Create campaign targeting Gold tier only
        campaign = LoyaltyCampaign.objects.create(
            name="Gold Tier Campaign",
            slug="gold-tier-campaign",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=False,
            actions=[{"type": "award_points", "points": 500}],
        )
        campaign.target_tiers.add(gold_tier)

        # Trigger for Bronze member - should be skipped
        result_bronze = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result_bronze["triggered"], 0)

        # Upgrade member to Gold
        self.member.current_tier = gold_tier
        self.member.save()

        # Trigger for Gold member - should succeed
        result_gold = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED, member=self.member, context={}
        )
        self.assertEqual(result_gold["triggered"], 1)

    def test_journey_step_scheduling(self):
        """Test multi-step journey scheduling"""
        campaign = LoyaltyCampaign.objects.create(
            name="Journey Campaign",
            slug="journey-campaign",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            is_journey=True,
            journey_steps=[
                {
                    "step": 1,
                    "actions": [{"type": "send_email", "template": "welcome"}],
                    "next_step_delay_days": 3,
                },
                {
                    "step": 2,
                    "actions": [{"type": "award_points", "points": 100}],
                    "next_step_delay_days": 7,
                },
                {
                    "step": 3,
                    "actions": [{"type": "send_email", "template": "followup"}],
                    "next_step_delay_days": None,
                },
            ],
        )

        # Trigger campaign
        result = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP, member=self.member, context={}
        )
        self.assertEqual(result["triggered"], 1)

        # Verify execution created with journey tracking
        execution = LoyaltyCampaignExecution.objects.get(campaign=campaign, member=self.member)
        self.assertEqual(execution.current_step, 1)
        self.assertIsNone(execution.next_step_at)  # Will be set after processing

    def test_evaluate_trigger_conditions_category_ids(self):
        """Test trigger condition evaluation with category IDs"""
        campaign = LoyaltyCampaign.objects.create(
            name="Category Campaign",
            slug="category-campaign",
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            trigger_conditions={"category_ids": [1, 2, 3]},
            actions=[{"type": "award_points", "points": 200}],
        )

        # Context with matching category
        result_match = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            member=self.member,
            context={"category_ids": [2, 5]},
        )
        self.assertEqual(result_match["triggered"], 1)

        # Context without matching category
        result_no_match = self.orchestrator.trigger_event(
            event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            member=self.member,
            context={"category_ids": [7, 8]},
        )
        self.assertEqual(result_no_match["triggered"], 0)
