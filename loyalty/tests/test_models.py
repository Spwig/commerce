"""
Tests for loyalty app models

Tests model validation, constraints, relationships, and business logic.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyTransaction,
    LoyaltyTier,
    LoyaltyBadge,
    LoyaltyMemberBadge,
)

User = get_user_model()


class LoyaltyMemberModelTest(TestCase):
    """Test LoyaltyMember model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_loyalty_member(self):
        """Test creating a loyalty member"""
        member = LoyaltyMember.objects.create(
            customer=self.user,
        )

        self.assertEqual(member.customer, self.user)
        self.assertTrue(member.is_active)
        self.assertIsNotNone(member.uuid)
        self.assertIsNotNone(member.enrolled_at)
        self.assertIsNone(member.current_tier)

    def test_loyalty_member_str(self):
        """Test __str__ method"""
        member = LoyaltyMember.objects.create(
            customer=self.user,
        )
        expected = f"{self.user.get_full_name() or self.user.username} - Member #{member.id}"
        self.assertEqual(str(member), expected)

    def test_loyalty_member_repr(self):
        """Test __repr__ method"""
        member = LoyaltyMember.objects.create(
            customer=self.user,
        )
        self.assertIn('LoyaltyMember', repr(member))
        self.assertIn(str(member.id), repr(member))
        self.assertIn(self.user.username, repr(member))

    def test_one_member_per_customer(self):
        """Test that each customer can only have one loyalty membership"""
        LoyaltyMember.objects.create(customer=self.user)

        with self.assertRaises(IntegrityError):
            LoyaltyMember.objects.create(customer=self.user)

    def test_uuid_is_unique(self):
        """Test that UUID is unique across members"""
        member1 = LoyaltyMember.objects.create(
            customer=self.user,
        )

        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        member2 = LoyaltyMember.objects.create(
            customer=user2,
        )

        self.assertNotEqual(member1.uuid, member2.uuid)

    def test_cascade_delete_on_user_deletion(self):
        """Test that loyalty member is deleted when user is deleted"""
        member = LoyaltyMember.objects.create(customer=self.user)
        member_id = member.id

        self.user.delete()

        self.assertFalse(LoyaltyMember.objects.filter(id=member_id).exists())


class LoyaltyBalanceModelTest(TestCase):
    """Test LoyaltyBalance model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.member = LoyaltyMember.objects.create(customer=self.user)

    def test_create_loyalty_balance(self):
        """Test creating a loyalty balance"""
        balance = LoyaltyBalance.objects.create(
            member=self.member,
            available_points=100,
            pending_points=50,
            lifetime_earned=150,
            lifetime_redeemed=0,
            lifetime_expired=0,
        )

        self.assertEqual(balance.member, self.member)
        self.assertEqual(balance.available_points, 100)
        self.assertEqual(balance.pending_points, 50)
        self.assertEqual(balance.lifetime_earned, 150)

    def test_balance_str(self):
        """Test __str__ method"""
        balance = LoyaltyBalance.objects.create(
            member=self.member,
            available_points=100,
        )
        self.assertIn('100 points', str(balance))

    def test_balance_repr(self):
        """Test __repr__ method"""
        balance = LoyaltyBalance.objects.create(
            member=self.member,
            available_points=100,
        )
        self.assertIn('LoyaltyBalance', repr(balance))
        self.assertIn('available=100', repr(balance))

    def test_total_points_property(self):
        """Test total_points property calculation"""
        balance = LoyaltyBalance.objects.create(
            member=self.member,
            available_points=100,
            pending_points=50,
        )
        self.assertEqual(balance.total_points, 150)

    def test_one_balance_per_member(self):
        """Test that each member can only have one balance"""
        LoyaltyBalance.objects.create(member=self.member)

        with self.assertRaises(IntegrityError):
            LoyaltyBalance.objects.create(member=self.member)

    def test_cascade_delete_on_member_deletion(self):
        """Test that balance is deleted when member is deleted"""
        balance = LoyaltyBalance.objects.create(member=self.member)
        member_id = self.member.id

        self.member.delete()

        # Check balance doesn't exist by checking if we can query with the old member ID
        # Since balance uses member as primary key, it should also be deleted
        self.assertEqual(LoyaltyBalance.objects.count(), 0)

    def test_negative_points_validation(self):
        """Test that negative points are validated"""
        balance = LoyaltyBalance.objects.create(
            member=self.member,
            available_points=-10,  # This should be caught by validator
        )

        with self.assertRaises(ValidationError):
            balance.full_clean()


class LoyaltyTransactionModelTest(TestCase):
    """Test LoyaltyTransaction model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
        )
        self.member = LoyaltyMember.objects.create(customer=self.user)

    def test_create_earn_transaction(self):
        """Test creating an earn transaction"""
        transaction = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=100,
            description='Earned 100 points from order #1234',
            reason='Order #1234',
            related_object_type='order',
            related_object_id='1234',
        )

        self.assertEqual(transaction.member, self.member)
        self.assertEqual(transaction.transaction_type, LoyaltyTransaction.TYPE_EARN)
        self.assertEqual(transaction.points, 100)
        self.assertEqual(transaction.status, LoyaltyTransaction.STATUS_AVAILABLE)
        self.assertIsNotNone(transaction.uuid)

    def test_create_redeem_transaction(self):
        """Test creating a redeem transaction"""
        transaction = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_REDEEM,
            points=-50,
            description='Redeemed 50 points for discount',
            status=LoyaltyTransaction.STATUS_REDEEMED,
        )

        self.assertEqual(transaction.transaction_type, LoyaltyTransaction.TYPE_REDEEM)
        self.assertEqual(transaction.points, -50)
        self.assertEqual(transaction.status, LoyaltyTransaction.STATUS_REDEEMED)

    def test_transaction_str(self):
        """Test __str__ method"""
        transaction = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=100,
            description='Test transaction',
        )
        self.assertIn('earn', str(transaction))
        self.assertIn('100 points', str(transaction))

    def test_transaction_immutability(self):
        """Test that transactions cannot be updated after creation"""
        transaction = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=100,
            description='Test transaction',
        )

        # Try to update the transaction
        transaction.points = 200

        with self.assertRaises(ValueError) as context:
            transaction.save()

        self.assertIn('immutable', str(context.exception).lower())

    def test_transaction_with_expiration(self):
        """Test creating transaction with expiration date"""
        expires_at = timezone.now() + timedelta(days=365)

        transaction = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=100,
            description='Points expire in 1 year',
            expires_at=expires_at,
        )

        self.assertIsNotNone(transaction.expires_at)
        self.assertEqual(transaction.expires_at, expires_at)

    def test_reversal_transaction(self):
        """Test creating a reversal transaction"""
        original = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=100,
            description='Original transaction',
        )

        reversal = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_REVOKE,
            points=-100,
            description='Reversal of original transaction',
            reversal_of=original,
        )

        self.assertEqual(reversal.reversal_of, original)
        self.assertEqual(reversal.transaction_type, LoyaltyTransaction.TYPE_REVOKE)

    def test_admin_adjustment_transaction(self):
        """Test creating an admin adjustment transaction"""
        transaction = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_ADJUSTMENT,
            points=50,
            description='Manual adjustment by admin',
            created_by=self.admin_user,
            admin_note='Goodwill gesture for customer complaint',
        )

        self.assertEqual(transaction.created_by, self.admin_user)
        self.assertIn('Goodwill', transaction.admin_note)

    def test_protect_on_member_deletion(self):
        """Test that transactions are protected when member is deleted"""
        LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=100,
            description='Test transaction',
        )

        # Attempting to delete member with transactions should fail
        with self.assertRaises(Exception):  # Protected foreign key
            self.member.delete()


class LoyaltyTierModelTest(TestCase):
    """Test LoyaltyTier model"""

    def test_create_tier(self):
        """Test creating a loyalty tier"""
        tier = LoyaltyTier.objects.create(
            name='Gold',
            slug='gold',
            description='Gold tier benefits',
            icon='fa-medal',
            color='#FFD700',
            rank=2,
            min_spend=Decimal('500.00'),
            min_orders=10,
            min_points_earned=1000,
            points_multiplier=Decimal('1.5'),
            has_free_shipping=True,
        )

        self.assertEqual(tier.name, 'Gold')
        self.assertEqual(tier.slug, 'gold')
        self.assertEqual(tier.rank, 2)
        self.assertEqual(tier.points_multiplier, Decimal('1.5'))
        self.assertTrue(tier.has_free_shipping)

    def test_tier_str(self):
        """Test __str__ method"""
        tier = LoyaltyTier.objects.create(
            name='Silver',
            slug='silver',
            rank=3,
        )
        self.assertEqual(str(tier), 'Silver (Rank 3)')

    def test_tier_ordering(self):
        """Test that tiers are ordered by rank"""
        bronze = LoyaltyTier.objects.create(name='Bronze', slug='bronze', rank=4)
        platinum = LoyaltyTier.objects.create(name='Platinum', slug='platinum', rank=1)
        gold = LoyaltyTier.objects.create(name='Gold', slug='gold', rank=2)

        tiers = list(LoyaltyTier.objects.all())
        self.assertEqual(tiers[0], platinum)
        self.assertEqual(tiers[1], gold)
        self.assertEqual(tiers[2], bronze)

    def test_unique_rank(self):
        """Test that rank must be unique"""
        LoyaltyTier.objects.create(name='Gold', slug='gold', rank=1)

        with self.assertRaises(IntegrityError):
            LoyaltyTier.objects.create(name='Silver', slug='silver', rank=1)

    def test_unique_slug(self):
        """Test that slug must be unique"""
        LoyaltyTier.objects.create(name='Gold', slug='gold-tier', rank=1)

        with self.assertRaises(IntegrityError):
            LoyaltyTier.objects.create(name='Gold Plus', slug='gold-tier', rank=2)


class LoyaltyBadgeModelTest(TestCase):
    """Test LoyaltyBadge model"""

    def test_create_badge(self):
        """Test creating a loyalty badge"""
        badge = LoyaltyBadge.objects.create(
            name='First Purchase',
            slug='first-purchase',
            description='Awarded on first purchase',
            icon='fa-star',
            criteria_type='first_purchase',
            criteria_value=1,
            points_reward=50,
        )

        self.assertEqual(badge.name, 'First Purchase')
        self.assertEqual(badge.slug, 'first-purchase')
        self.assertEqual(badge.criteria_type, 'first_purchase')
        self.assertEqual(badge.points_reward, 50)

    def test_badge_str(self):
        """Test __str__ method"""
        badge = LoyaltyBadge.objects.create(
            name='Social Butterfly',
            slug='social-butterfly',
            description='Shared 5 times',
            icon='fa-share',
            criteria_type='social_share',
            criteria_value=5,
        )
        self.assertEqual(str(badge), 'Social Butterfly')

    def test_badge_ordering(self):
        """Test that badges are ordered by display_order then name"""
        badge1 = LoyaltyBadge.objects.create(
            name='Zeta Badge',
            slug='zeta',
            description='Test',
            icon='fa-star',
            criteria_type='test',
            display_order=2,
        )
        badge2 = LoyaltyBadge.objects.create(
            name='Alpha Badge',
            slug='alpha',
            description='Test',
            icon='fa-star',
            criteria_type='test',
            display_order=1,
        )

        badges = list(LoyaltyBadge.objects.all())
        self.assertEqual(badges[0], badge2)  # Alpha, display_order 1
        self.assertEqual(badges[1], badge1)  # Zeta, display_order 2


class LoyaltyMemberBadgeModelTest(TestCase):
    """Test LoyaltyMemberBadge model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.member = LoyaltyMember.objects.create(customer=self.user)
        self.badge = LoyaltyBadge.objects.create(
            name='Test Badge',
            slug='test-badge',
            description='Test badge',
            icon='fa-trophy',
            criteria_type='test',
        )

    def test_create_member_badge(self):
        """Test awarding a badge to a member"""
        member_badge = LoyaltyMemberBadge.objects.create(
            member=self.member,
            badge=self.badge,
        )

        self.assertEqual(member_badge.member, self.member)
        self.assertEqual(member_badge.badge, self.badge)
        self.assertIsNotNone(member_badge.earned_at)

    def test_member_badge_str(self):
        """Test __str__ method"""
        member_badge = LoyaltyMemberBadge.objects.create(
            member=self.member,
            badge=self.badge,
        )
        self.assertIn('Test Badge', str(member_badge))

    def test_unique_badge_per_member(self):
        """Test that a member cannot earn the same badge twice"""
        LoyaltyMemberBadge.objects.create(
            member=self.member,
            badge=self.badge,
        )

        with self.assertRaises(IntegrityError):
            LoyaltyMemberBadge.objects.create(
                member=self.member,
                badge=self.badge,
            )

    def test_member_badge_with_transaction(self):
        """Test awarding badge with points transaction"""
        transaction = LoyaltyTransaction.objects.create(
            member=self.member,
            transaction_type=LoyaltyTransaction.TYPE_BONUS,
            points=50,
            description='Badge reward',
        )

        member_badge = LoyaltyMemberBadge.objects.create(
            member=self.member,
            badge=self.badge,
            transaction=transaction,
        )

        self.assertEqual(member_badge.transaction, transaction)

    def test_cascade_delete_on_member_deletion(self):
        """Test that badges are deleted when member is deleted"""
        member_badge = LoyaltyMemberBadge.objects.create(
            member=self.member,
            badge=self.badge,
        )
        member_badge_id = member_badge.id

        self.member.delete()

        self.assertFalse(LoyaltyMemberBadge.objects.filter(id=member_badge_id).exists())

    def test_cascade_delete_on_badge_deletion(self):
        """Test that member badges are deleted when badge is deleted"""
        member_badge = LoyaltyMemberBadge.objects.create(
            member=self.member,
            badge=self.badge,
        )
        member_badge_id = member_badge.id

        self.badge.delete()

        self.assertFalse(LoyaltyMemberBadge.objects.filter(id=member_badge_id).exists())
