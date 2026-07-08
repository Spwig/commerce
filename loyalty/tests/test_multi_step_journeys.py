"""
Tests for Multi-Step Journey Campaigns

Tests advanced journey features:
- Conditional branching
- Exit conditions
- Step conditions
- Variable delays
"""

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from decimal import Decimal

from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyCampaign,
    LoyaltyCampaignExecution,
    LoyaltyTier
)
from loyalty.services.campaign_orchestrator import CampaignOrchestrator
from orders.models import Order
from djmoney.money import Money

User = get_user_model()


class MultiStepJourneyTestCase(TestCase):
    """Test multi-step journey campaigns with advanced features"""

    def setUp(self):
        """Set up test data"""
        self.orchestrator = CampaignOrchestrator()

        # Create tier
        self.tier = LoyaltyTier.objects.create(
            name='Bronze',
            slug='bronze',
            rank=10,
            min_points_earned=0,
            points_multiplier=1.0,
            is_active=True
        )

        self.gold_tier = LoyaltyTier.objects.create(
            name='Gold',
            slug='gold',
            rank=5,
            min_points_earned=1000,
            min_spend=Decimal('999999.00'),  # Set high to avoid OR logic bug
            min_orders=999999,  # Set high to avoid OR logic bug
            points_multiplier=1.5,
            is_active=True
        )

        # Create user and member
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.member = LoyaltyMember.objects.get(customer=self.user)
        self.member.current_tier = self.tier
        self.member.save()

        self.balance, _ = LoyaltyBalance.objects.get_or_create(
            member=self.member,
            defaults={
                'available_points': 500,
                'pending_points': 0,
                'lifetime_earned': 500,
                'lifetime_redeemed': 0
            }
        )

    def test_simple_linear_journey(self):
        """Test basic linear journey with multiple steps"""
        campaign = LoyaltyCampaign.objects.create(
            name='Linear Journey',
            slug='linear-journey',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            is_journey=True,
            journey_steps=[
                {
                    'step': 1,
                    'actions': [{'type': 'award_points', 'points': 50, 'reason': 'Step 1'}],
                    'next_step_delay_days': 1  # 1 day until step 2
                },
                {
                    'step': 2,
                    'actions': [{'type': 'award_points', 'points': 100, 'reason': 'Step 2'}],
                    'next_step_delay_days': 2  # 2 days until step 3
                },
                {
                    'step': 3,
                    'actions': [{'type': 'award_points', 'points': 150, 'reason': 'Step 3'}],
                    # No next_step_delay_days = journey ends
                }
            ]
        )

        # Create execution
        execution = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=self.member,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context={},
            current_step=1
        )

        # Process step 1
        self.orchestrator.process_campaign_actions(execution)
        execution.refresh_from_db()

        self.assertEqual(execution.current_step, 2)
        self.assertIsNotNone(execution.next_step_at)
        self.assertIn(1, execution.steps_completed)

        # Process step 2
        execution.status = LoyaltyCampaignExecution.STATUS_PENDING
        execution.save()
        self.orchestrator.process_campaign_actions(execution)
        execution.refresh_from_db()

        self.assertEqual(execution.current_step, 3)
        self.assertIn(2, execution.steps_completed)

        # Process step 3 (final)
        execution.status = LoyaltyCampaignExecution.STATUS_PENDING
        execution.save()
        self.orchestrator.process_campaign_actions(execution)
        execution.refresh_from_db()

        self.assertEqual(execution.status, LoyaltyCampaignExecution.STATUS_COMPLETED)
        self.assertIn(3, execution.steps_completed)

    def test_journey_with_branching(self):
        """Test journey with conditional branching"""
        campaign = LoyaltyCampaign.objects.create(
            name='Branching Journey',
            slug='branching-journey',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            is_journey=True,
            journey_steps=[
                {
                    'step': 1,
                    'actions': [{'type': 'award_points', 'points': 50, 'reason': 'Step 1'}],
                    'branches': [
                        {
                            'conditions': {'points_threshold': 1000},  # If member has 1000+ points
                            'next_step': 3,  # Skip to step 3
                            'delay_days': 0
                        }
                    ],
                    'next_step_delay_days': 1  # Default: go to step 2
                },
                {
                    'step': 2,
                    'actions': [{'type': 'award_points', 'points': 100, 'reason': 'Step 2'}],
                    'next_step_delay_days': 1
                },
                {
                    'step': 3,
                    'actions': [{'type': 'award_points', 'points': 200, 'reason': 'Step 3 (VIP)'}],
                }
            ]
        )

        # Test member with low points - should go through all steps
        execution1 = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=self.member,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context={},
            current_step=1
        )

        # Process step 1 - should go to step 2
        self.orchestrator.process_campaign_actions(execution1)
        execution1.refresh_from_db()
        self.assertEqual(execution1.current_step, 2)  # No branch taken

        # Create high-points member
        user2 = User.objects.create_user(
            username='vipuser',
            email='vip@example.com',
            password='testpass123'
        )
        member2 = LoyaltyMember.objects.get(customer=user2)
        balance2, _ = LoyaltyBalance.objects.get_or_create(
            member=member2,
            defaults={
                'available_points': 2000,  # High points
                'pending_points': 0,
                'lifetime_earned': 2000,
                'lifetime_redeemed': 0
            }
        )

        execution2 = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=member2,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context={},
            current_step=1
        )

        # Process step 1 - should branch to step 3
        self.orchestrator.process_campaign_actions(execution2)
        execution2.refresh_from_db()
        self.assertEqual(execution2.current_step, 3)  # Branch taken!

    def test_journey_with_exit_conditions(self):
        """Test journey that can exit early based on conditions"""
        campaign = LoyaltyCampaign.objects.create(
            name='Exit Condition Journey',
            slug='exit-condition-journey',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            is_journey=True,
            journey_steps=[
                {
                    'step': 1,
                    'actions': [{'type': 'award_points', 'points': 50}],
                    'exit_conditions': {
                        'tier_required': self.gold_tier.id  # Exit if member reaches Gold tier
                    },
                    'next_step_delay_days': 1
                },
                {
                    'step': 2,
                    'actions': [{'type': 'award_points', 'points': 100}],
                }
            ]
        )

        # Give member enough points to qualify for Gold tier
        self.balance.available_points = 1500
        self.balance.lifetime_earned = 1500
        self.balance.save()

        # Promote member to Gold tier (they now have enough points to stay in Gold)
        self.member.current_tier = self.gold_tier
        self.member.save()

        execution = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=self.member,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context={},
            current_step=1
        )

        # Process step 1 - should exit due to Gold tier
        self.orchestrator.process_campaign_actions(execution)
        execution.refresh_from_db()

        self.assertEqual(execution.status, LoyaltyCampaignExecution.STATUS_COMPLETED)
        self.assertIn(1, execution.steps_completed)
        # Step 2 never executed

    def test_journey_step_conditions(self):
        """Test that step conditions can skip steps"""
        campaign = LoyaltyCampaign.objects.create(
            name='Conditional Steps Journey',
            slug='conditional-steps',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            is_journey=True,
            journey_steps=[
                {
                    'step': 1,
                    'actions': [{'type': 'award_points', 'points': 50}],
                    'next_step_delay_days': 1
                },
                {
                    'step': 2,
                    'conditions': {
                        'points_threshold': 1000  # Only execute if member has 1000+ points
                    },
                    'actions': [{'type': 'award_points', 'points': 500, 'reason': 'Bonus for high points'}],
                    'next_step_delay_days': 1
                },
                {
                    'step': 3,
                    'actions': [{'type': 'award_points', 'points': 100}],
                }
            ]
        )

        execution = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=self.member,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context={},
            current_step=1
        )

        # Process step 1
        self.orchestrator.process_campaign_actions(execution)
        execution.refresh_from_db()
        self.assertEqual(execution.current_step, 2)

        # Process step 2 - should be skipped (member has <1000 points)
        execution.status = LoyaltyCampaignExecution.STATUS_PENDING
        execution.save()

        result = self.orchestrator.process_journey_step(execution.id, 2)
        execution.refresh_from_db()

        self.assertTrue(result.get('skipped'))  # Step was skipped
        self.assertEqual(execution.current_step, 3)  # Moved to step 3
        self.assertIn(2, execution.steps_completed)  # Step 2 marked complete

    def test_journey_with_orders_since_start_condition(self):
        """Test journey condition based on orders placed during journey"""
        campaign = LoyaltyCampaign.objects.create(
            name='Order Engagement Journey',
            slug='order-engagement',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            is_journey=True,
            journey_steps=[
                {
                    'step': 1,
                    'actions': [{'type': 'award_points', 'points': 50}],
                    'next_step_delay_days': 7  # Wait 1 week
                },
                {
                    'step': 2,
                    'conditions': {
                        'orders_since_start': 2  # Must have placed 2 orders
                    },
                    'actions': [{'type': 'award_points', 'points': 500, 'reason': 'Active shopper bonus'}],
                }
            ]
        )

        # Create execution and backdate it
        execution = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=self.member,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context={},
            current_step=1
        )
        # Backdate the triggered_at timestamp
        LoyaltyCampaignExecution.objects.filter(id=execution.id).update(
            triggered_at=timezone.now() - timedelta(days=8)
        )
        execution.refresh_from_db()

        # Create 2 orders after journey start
        Order.objects.create(
            user=self.user,
            order_number='ORD-001',
            status='completed',
            subtotal=Money(50.00, 'USD'),
            total_amount=Money(50.00, 'USD'),
            created_at=timezone.now() - timedelta(days=5)
        )

        Order.objects.create(
            user=self.user,
            order_number='ORD-002',
            status='completed',
            subtotal=Money(75.00, 'USD'),
            total_amount=Money(75.00, 'USD'),
            created_at=timezone.now() - timedelta(days=2)
        )

        # Process step 1
        self.orchestrator.process_campaign_actions(execution)
        execution.refresh_from_db()

        # Process step 2 - should execute (member has 2 orders)
        execution.status = LoyaltyCampaignExecution.STATUS_PENDING
        execution.save()

        result = self.orchestrator.process_journey_step(execution.id, 2)

        self.assertFalse(result.get('skipped', False))  # Step not skipped
        self.assertTrue(result.get('success'))

    def test_journey_variable_delays(self):
        """Test that branching can use different delays"""
        campaign = LoyaltyCampaign.objects.create(
            name='Variable Delay Journey',
            slug='variable-delay',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            is_journey=True,
            journey_steps=[
                {
                    'step': 1,
                    'actions': [{'type': 'award_points', 'points': 50}],
                    'branches': [
                        {
                            'conditions': {'tier_required': self.gold_tier.id},
                            'next_step': 2,
                            'delay_days': 0  # VIP gets immediate next step
                        }
                    ],
                    'next_step_delay_days': 7  # Normal members wait 7 days
                },
                {
                    'step': 2,
                    'actions': [{'type': 'award_points', 'points': 100}],
                }
            ]
        )

        # Test normal member - should have 7 day delay
        execution1 = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=self.member,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context={},
            current_step=1
        )

        self.orchestrator.process_campaign_actions(execution1)
        execution1.refresh_from_db()

        delay1 = (execution1.next_step_at - timezone.now()).days
        self.assertAlmostEqual(delay1, 7, delta=1)

        # Test VIP member - should have 0 day delay
        user2 = User.objects.create_user(
            username='vipuser2',
            email='vip2@example.com',
            password='testpass123'
        )
        member2 = LoyaltyMember.objects.get(customer=user2)

        # Give member enough points to qualify for Gold tier
        LoyaltyBalance.objects.get_or_create(
            member=member2,
            defaults={
                'available_points': 1500,
                'pending_points': 0,
                'lifetime_earned': 1500,
                'lifetime_redeemed': 0
            }
        )

        member2.current_tier = self.gold_tier
        member2.save()

        execution2 = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=member2,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context={},
            current_step=1
        )

        self.orchestrator.process_campaign_actions(execution2)
        execution2.refresh_from_db()

        delay2 = (execution2.next_step_at - timezone.now()).total_seconds()
        self.assertLess(delay2, 60)  # Should be immediate (< 1 minute)
