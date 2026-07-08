"""
Model Tests

Tests for all referral program models.
"""
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from ..models import (
    ReferralProgram,
    ReferralIdentity,
    ReferralAttribution,
    ReferralReward,
    ReferralEvent,
)
from .factories import (
    create_user,
    create_referral_program,
    create_referral_identity,
    create_referral_attribution,
    create_referral_reward,
    create_referral_event,
    create_order,
)


class ReferralProgramModelTest(TestCase):
    """Tests for ReferralProgram model."""

    def test_create_referral_program(self):
        """Test creating a referral program."""
        program = create_referral_program(name='My Program')
        self.assertEqual(program.name, 'My Program')
        self.assertEqual(program.status, 'active')

    def test_singleton_pattern(self):
        """Test that program uses singleton pattern (pk=1)."""
        program1 = create_referral_program(name='Program 1')
        self.assertEqual(program1.pk, 1)

        # Can update the existing program
        program1.name = 'Program Updated'
        program1.save()
        self.assertEqual(program1.pk, 1)
        self.assertEqual(ReferralProgram.objects.count(), 1)

        # Verify deletion is prevented
        with self.assertRaises(Exception):  # ValidationError
            program1.delete()

    def test_get_program(self):
        """Test get_program class method."""
        # Delete any existing program
        ReferralProgram.objects.all().delete()

        # get_program should create a program if none exists (get_or_create)
        program = ReferralProgram.get_program()
        self.assertIsNotNone(program)
        self.assertEqual(program.pk, 1)

        # Calling again should return the same program
        program2 = ReferralProgram.get_program()
        self.assertEqual(program, program2)

    def test_is_active(self):
        """Test is_active method."""
        program = create_referral_program(status='active')
        self.assertTrue(program.is_active())

        program.status = 'paused'
        program.save()
        self.assertFalse(program.is_active())

    def test_get_cookie_ttl_days(self):
        """Test get_cookie_ttl_days method."""
        program = create_referral_program()

        # Default from factory
        self.assertEqual(program.get_cookie_ttl_days(), 30)

        # Custom
        program.tracking_config = {'cookie_ttl_days': 60}
        program.save()
        self.assertEqual(program.get_cookie_ttl_days(), 60)


class ReferralIdentityModelTest(TestCase):
    """Tests for ReferralIdentity model."""

    def setUp(self):
        self.program = create_referral_program()

    def test_create_identity(self):
        """Test creating a referral identity."""
        user = create_user()
        identity = create_referral_identity(customer=user)

        self.assertEqual(identity.customer, user)
        self.assertIsNotNone(identity.token)
        self.assertEqual(len(identity.token), 12)

    def test_token_uniqueness(self):
        """Test that tokens are unique."""
        user1 = create_user(email='user1@example.com')
        user2 = create_user(email='user2@example.com')

        identity1 = create_referral_identity(customer=user1)
        identity2 = create_referral_identity(customer=user2)

        self.assertNotEqual(identity1.token, identity2.token)

    def test_get_referral_link(self):
        """Test get_referral_link method."""
        identity = create_referral_identity()
        link = identity.get_referral_link()

        self.assertIn(identity.token, link)
        self.assertIn('ref=', link)

    def test_conversion_rate(self):
        """Test conversion rate calculation."""
        identity = create_referral_identity()

        # No clicks yet
        self.assertEqual(identity.get_conversion_rate(), 0.0)

        # Simulate some activity
        identity.total_clicks = 100
        identity.total_conversions = 10
        identity.save()

        self.assertEqual(identity.get_conversion_rate(), 10.0)

    def test_str_representation(self):
        """Test string representation."""
        user = create_user(email='test@example.com')
        identity = create_referral_identity(customer=user)

        # String representation uses full name "Test User - {token}"
        self.assertIn('Test User', str(identity))
        self.assertIn(identity.token, str(identity))


class ReferralAttributionModelTest(TestCase):
    """Tests for ReferralAttribution model."""

    def setUp(self):
        self.program = create_referral_program()

    def test_create_attribution(self):
        """Test creating a referral attribution."""
        attribution = create_referral_attribution()

        self.assertIsNotNone(attribution.referrer_identity)
        self.assertIsNotNone(attribution.referee_customer)
        self.assertIsNotNone(attribution.first_order)
        self.assertEqual(attribution.status, 'pending')

    def test_approve_method(self):
        """Test approve method."""
        attribution = create_referral_attribution(status='pending')
        reviewer = create_user(email='admin@example.com')

        attribution.approve(reviewed_by=reviewer)

        self.assertEqual(attribution.status, 'approved')
        self.assertEqual(attribution.reviewed_by, reviewer)
        self.assertIsNotNone(attribution.reviewed_at)
        self.assertIsNotNone(attribution.approved_at)

    def test_reject_method(self):
        """Test reject method."""
        attribution = create_referral_attribution(status='pending')
        reviewer = create_user(email='admin@example.com')

        attribution.reject(reason='fraud_risk', notes='Suspicious activity', reviewed_by=reviewer)

        self.assertEqual(attribution.status, 'rejected')
        self.assertEqual(attribution.rejection_reason, 'fraud_risk')
        self.assertEqual(attribution.rejection_notes, 'Suspicious activity')
        self.assertEqual(attribution.reviewed_by, reviewer)
        self.assertIsNotNone(attribution.reviewed_at)

    def test_risk_score(self):
        """Test risk score field."""
        low_risk = create_referral_attribution(risk_score=30)
        high_risk = create_referral_attribution(risk_score=80)

        self.assertEqual(low_risk.risk_score, 30)
        self.assertEqual(high_risk.risk_score, 80)

    def test_str_representation(self):
        """Test string representation."""
        referrer = create_user(email='referrer@example.com')
        referee = create_user(email='referee@example.com')
        identity = create_referral_identity(customer=referrer)

        attribution = create_referral_attribution(
            referrer_identity=identity,
            referee_customer=referee
        )

        str_rep = str(attribution)
        # String representation uses full name "Test User → Test User (Status)"
        self.assertIn('Test User', str_rep)
        self.assertIn('→', str_rep)
        self.assertIn('Pending', str_rep)


class ReferralRewardModelTest(TestCase):
    """Tests for ReferralReward model."""

    def setUp(self):
        self.program = create_referral_program()

    def test_create_reward(self):
        """Test creating a referral reward."""
        reward = create_referral_reward(
            kind='credit',
            amount=Decimal('10.00')
        )

        self.assertEqual(reward.kind, 'credit')
        # amount is a MoneyField, compare with .amount to get Decimal value
        self.assertEqual(reward.amount.amount, Decimal('10.00'))
        self.assertEqual(str(reward.amount.currency), 'USD')
        self.assertEqual(reward.status, 'pending')

    def test_issue_method(self):
        """Test issue method."""
        reward = create_referral_reward(status='pending')

        reward.issue()

        self.assertEqual(reward.status, 'issued')
        self.assertIsNotNone(reward.issued_at)

    def test_redeem_method(self):
        """Test redeem method."""
        reward = create_referral_reward(status='issued')

        reward.redeem()

        self.assertEqual(reward.status, 'redeemed')
        self.assertIsNotNone(reward.redeemed_at)

    def test_revoke_method(self):
        """Test revoke method."""
        reward = create_referral_reward(status='issued')

        reward.revoke(reason='test_revocation')

        self.assertEqual(reward.status, 'revoked')
        self.assertIn('test_revocation', reward.revocation_reason)

    def test_expire_method(self):
        """Test expire method."""
        reward = create_referral_reward(status='issued')

        reward.expire()

        self.assertEqual(reward.status, 'expired')

    def test_is_expired(self):
        """Test is_expired method."""
        # Pending reward is not expired
        pending_reward = create_referral_reward(status='pending')
        self.assertFalse(pending_reward.is_expired())

        # Issued reward is not expired
        issued_reward = create_referral_reward(status='issued')
        self.assertFalse(issued_reward.is_expired())

        # Expired status reward
        expired_reward = create_referral_reward(status='expired')
        self.assertTrue(expired_reward.is_expired())

    def test_is_expiring_soon(self):
        """Test is_expiring_soon method."""
        # No expiration
        no_expiry = create_referral_reward(status='issued')
        self.assertFalse(no_expiry.is_expiring_soon())

        # Expires in 3 days (within 7 day threshold)
        soon_expiry = create_referral_reward(
            status='issued',
            expires_at=timezone.now() + timedelta(days=3)
        )
        self.assertTrue(soon_expiry.is_expiring_soon())

        # Expires in 30 days (not within 7 day threshold)
        far_expiry = create_referral_reward(
            status='issued',
            expires_at=timezone.now() + timedelta(days=30)
        )
        self.assertFalse(far_expiry.is_expiring_soon())

    def test_str_representation(self):
        """Test string representation."""
        user = create_user(email='user@example.com')
        reward = create_referral_reward(
            customer=user,
            amount=Decimal('10.00')
        )

        str_rep = str(reward)
        # String rep format: "{customer_name} - {kind_display} - {amount} ({status_display})"
        self.assertIn('Test User', str_rep)
        self.assertIn('10.00', str_rep)


class ReferralEventModelTest(TestCase):
    """Tests for ReferralEvent model."""

    def setUp(self):
        self.program = create_referral_program()

    def test_create_event(self):
        """Test creating a referral event."""
        event = create_referral_event(event_type='click')

        self.assertEqual(event.event_type, 'click')
        self.assertIsNotNone(event.referrer_identity)
        self.assertIsNotNone(event.program)

    def test_event_types(self):
        """Test different event types."""
        identity = create_referral_identity()

        # Valid event types: 'click', 'signup', 'order', 'approved', 'rejected', 'reward_issued', 'reward_redeemed'
        for event_type in ['click', 'signup', 'order', 'approved', 'rejected']:
            event = create_referral_event(
                referrer_identity=identity,
                event_type=event_type
            )
            self.assertEqual(event.event_type, event_type)

    def test_str_representation(self):
        """Test string representation."""
        event = create_referral_event(event_type='click')

        str_rep = str(event)
        # String format: "{event_type_display} - {referrer_name} - {date}"
        self.assertIn('Click', str_rep)  # Display value is titlecase
        self.assertIn('Test User', str_rep)
