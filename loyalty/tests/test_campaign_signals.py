"""
Integration tests for campaign signal handlers

Tests that campaigns are automatically triggered when real events occur.
"""

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal

from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyCampaign,
    LoyaltyCampaignExecution,
    LoyaltyTier
)
from orders.models import Order
from catalog.models import Product, Category
from djmoney.money import Money

User = get_user_model()


class CampaignSignalIntegrationTestCase(TestCase):
    """Test campaign triggering via Django signals"""

    def setUp(self):
        """Set up test data"""
        # Create test tier
        self.tier = LoyaltyTier.objects.create(
            name='Bronze',
            slug='bronze',
            rank=10,
            min_points_earned=0,
            points_multiplier=1.0,
            is_active=True
        )

        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            is_active=True
        )

        # Create test product
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=Money(50.00, 'USD'),
            category=self.category,
            status='published'
        )

    def test_order_placed_triggers_campaign(self):
        """Test that creating an order triggers order_placed campaigns"""
        # Create user (this automatically creates LoyaltyMember via signal)
        user = User.objects.create_user(
            username='testcustomer',
            email='customer@example.com',
            password='testpass123'
        )

        # Get the auto-created member
        member = LoyaltyMember.objects.get(customer=user)
        member.current_tier = self.tier
        member.save()

        # Ensure balance exists
        LoyaltyBalance.objects.get_or_create(
            member=member,
            defaults={
                'available_points': 0,
                'pending_points': 0,
                'lifetime_earned': 0,
                'lifetime_redeemed': 0
            }
        )

        # Create campaign for order_placed event
        campaign = LoyaltyCampaign.objects.create(
            name='First Order Campaign',
            slug='first-order-campaign',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            trigger_conditions={'min_order_amount': 25.00},
            actions=[
                {'type': 'award_points', 'points': 100, 'reason': 'First order bonus'}
            ]
        )

        # Create order (this should trigger the campaign)
        order = Order.objects.create(
            user=user,
            order_number='TEST-001',
            status='pending',
            subtotal=Money(50.00, 'USD'),
            total_amount=Money(50.00, 'USD')
        )

        # Verify execution was created
        executions = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign,
            member=member
        )
        self.assertEqual(executions.count(), 1)

        execution = executions.first()
        self.assertEqual(execution.status, LoyaltyCampaignExecution.STATUS_PENDING)
        self.assertEqual(execution.trigger_context['order_id'], order.id)
        self.assertEqual(execution.trigger_context['order_number'], order.order_number)

    def test_order_below_minimum_skips_campaign(self):
        """Test that orders below minimum amount don't trigger campaigns"""
        # Create user
        user = User.objects.create_user(
            username='testcustomer2',
            email='customer2@example.com',
            password='testpass123'
        )

        member = LoyaltyMember.objects.get(customer=user)
        member.current_tier = self.tier
        member.save()

        # Create campaign with high minimum
        campaign = LoyaltyCampaign.objects.create(
            name='High Value Order Campaign',
            slug='high-value-order',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            trigger_conditions={'min_order_amount': 100.00},
            actions=[{'type': 'award_points', 'points': 500}]
        )

        # Create small order
        order = Order.objects.create(
            user=user,
            order_number='TEST-002',
            status='pending',
            subtotal=Money(25.00, 'USD'),
            total_amount=Money(25.00, 'USD')
        )

        # Verify NO execution was created
        executions = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign,
            member=member
        )
        self.assertEqual(executions.count(), 0)

    def test_customer_signup_triggers_campaign(self):
        """Test that creating a new user triggers signup campaigns"""
        # Create campaign for customer_signup event
        campaign = LoyaltyCampaign.objects.create(
            name='Welcome Campaign',
            slug='welcome-campaign',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            actions=[
                {'type': 'award_points', 'points': 50, 'reason': 'Welcome bonus'},
                {'type': 'send_email', 'template': 'loyalty_welcome'}
            ]
        )

        # Create new user (this should trigger both member creation AND signup campaign)
        user = User.objects.create_user(
            username='newcustomer',
            email='newcustomer@example.com',
            password='testpass123'
        )

        # Get the auto-created member
        member = LoyaltyMember.objects.get(customer=user)

        # Verify execution was created
        executions = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign,
            member=member
        )
        self.assertEqual(executions.count(), 1)

        execution = executions.first()
        self.assertEqual(execution.status, LoyaltyCampaignExecution.STATUS_PENDING)
        self.assertEqual(execution.trigger_context['user_id'], user.id)
        self.assertEqual(execution.trigger_context['email'], user.email)

    def test_tier_promotion_triggers_campaign(self):
        """Test that tier upgrades trigger tier_promoted campaigns"""
        # Create user and member
        user = User.objects.create_user(
            username='testcustomer3',
            email='customer3@example.com',
            password='testpass123'
        )

        member = LoyaltyMember.objects.get(customer=user)
        member.current_tier = self.tier
        member.save()

        # Create Gold tier
        gold_tier = LoyaltyTier.objects.create(
            name='Gold',
            slug='gold',
            rank=5,
            min_points_earned=1000,
            points_multiplier=1.5,
            is_active=True
        )

        # Create campaign for tier promotion
        campaign = LoyaltyCampaign.objects.create(
            name='Tier Promotion Celebration',
            slug='tier-promotion',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_TIER_PROMOTED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            actions=[
                {'type': 'award_points', 'points': 200, 'reason': 'Tier promotion bonus'}
            ]
        )

        # Promote member to Gold tier
        member.current_tier = gold_tier
        member.save()

        # Verify execution was created
        executions = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign,
            member=member
        )
        self.assertEqual(executions.count(), 1)

        execution = executions.first()
        self.assertEqual(execution.status, LoyaltyCampaignExecution.STATUS_PENDING)
        self.assertEqual(execution.trigger_context['new_tier_id'], gold_tier.id)
        self.assertEqual(execution.trigger_context['new_tier_name'], 'Gold')
        self.assertEqual(execution.trigger_context['old_tier_id'], self.tier.id)
        self.assertEqual(execution.trigger_context['old_tier_name'], 'Bronze')

    def test_multiple_campaigns_trigger_for_same_event(self):
        """Test that multiple campaigns can trigger for the same event"""
        # Create user
        user = User.objects.create_user(
            username='testcustomer4',
            email='customer4@example.com',
            password='testpass123'
        )

        member = LoyaltyMember.objects.get(customer=user)
        member.current_tier = self.tier
        member.save()

        # Create multiple campaigns for order_placed
        campaign1 = LoyaltyCampaign.objects.create(
            name='Campaign 1',
            slug='campaign-1',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            actions=[{'type': 'award_points', 'points': 50}]
        )

        campaign2 = LoyaltyCampaign.objects.create(
            name='Campaign 2',
            slug='campaign-2',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            actions=[{'type': 'award_points', 'points': 75}]
        )

        # Create order
        order = Order.objects.create(
            user=user,
            order_number='TEST-003',
            status='pending',
            subtotal=Money(100.00, 'USD'),
            total_amount=Money(100.00, 'USD')
        )

        # Verify both campaigns created executions
        execution1 = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign1,
            member=member
        ).first()
        self.assertIsNotNone(execution1)

        execution2 = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign2,
            member=member
        ).first()
        self.assertIsNotNone(execution2)

    def test_inactive_campaign_does_not_trigger(self):
        """Test that inactive campaigns don't trigger"""
        # Create user
        user = User.objects.create_user(
            username='testcustomer5',
            email='customer5@example.com',
            password='testpass123'
        )

        member = LoyaltyMember.objects.get(customer=user)

        # Create inactive campaign
        campaign = LoyaltyCampaign.objects.create(
            name='Inactive Campaign',
            slug='inactive-campaign',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=False,  # Inactive
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=True,
            actions=[{'type': 'award_points', 'points': 100}]
        )

        # Create order
        order = Order.objects.create(
            user=user,
            order_number='TEST-004',
            status='pending',
            subtotal=Money(50.00, 'USD'),
            total_amount=Money(50.00, 'USD')
        )

        # Verify NO execution was created
        executions = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign,
            member=member
        )
        self.assertEqual(executions.count(), 0)

    def test_tier_targeting_filters_members(self):
        """Test that campaigns target only specified tiers"""
        # Create Gold tier
        gold_tier = LoyaltyTier.objects.create(
            name='Gold',
            slug='gold',
            rank=5,
            min_points_earned=1000,
            points_multiplier=1.5,
            is_active=True
        )

        # Create Bronze member
        bronze_user = User.objects.create_user(
            username='bronzemember',
            email='bronze@example.com',
            password='testpass123'
        )
        bronze_member = LoyaltyMember.objects.get(customer=bronze_user)
        bronze_member.current_tier = self.tier
        bronze_member.save()

        # Create Gold member
        gold_user = User.objects.create_user(
            username='goldmember',
            email='gold@example.com',
            password='testpass123'
        )
        gold_member = LoyaltyMember.objects.get(customer=gold_user)
        gold_member.current_tier = gold_tier
        gold_member.save()

        # Create campaign targeting only Gold tier
        campaign = LoyaltyCampaign.objects.create(
            name='Gold Only Campaign',
            slug='gold-only',
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=LoyaltyCampaign.EVENT_ORDER_PLACED,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE,
            target_all_members=False,
            actions=[{'type': 'award_points', 'points': 200}]
        )
        campaign.target_tiers.add(gold_tier)

        # Create order for Bronze member
        bronze_order = Order.objects.create(
            user=bronze_user,
            order_number='BRONZE-001',
            status='pending',
            subtotal=Money(50.00, 'USD'),
            total_amount=Money(50.00, 'USD')
        )

        # Create order for Gold member
        gold_order = Order.objects.create(
            user=gold_user,
            order_number='GOLD-001',
            status='pending',
            subtotal=Money(50.00, 'USD'),
            total_amount=Money(50.00, 'USD')
        )

        # Verify only Gold member got execution
        bronze_executions = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign,
            member=bronze_member
        )
        self.assertEqual(bronze_executions.count(), 0)

        gold_executions = LoyaltyCampaignExecution.objects.filter(
            campaign=campaign,
            member=gold_member
        )
        self.assertEqual(gold_executions.count(), 1)
