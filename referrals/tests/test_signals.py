"""
Signal Handler Tests

Tests for automatic referral tracking via Django signals:
- User signup tracking
- Order completion and attribution
- Attribution approval handling
- Reward issuance notifications
- Order cancellation/refund handling
"""
from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.utils import timezone
from unittest.mock import Mock, patch, MagicMock

from ..models import ReferralProgram, ReferralIdentity, ReferralAttribution, ReferralReward, ReferralEvent
from ..signals import (
    track_user_signup,
    handle_order_completion,
    track_order_status_change,
    handle_attribution_approval,
    track_attribution_status_change,
    handle_reward_issuance,
    track_reward_status_change,
    handle_order_cancellation,
)
from .factories import (
    create_user,
    create_referral_program,
    create_referral_identity,
    create_referral_attribution,
    create_referral_reward,
    create_order,
)


class UserSignupSignalTest(TestCase):
    """Tests for user signup tracking signal."""

    def setUp(self):
        self.program = create_referral_program()
        self.factory = RequestFactory()

    @patch('referrals.signals.get_current_request')
    @patch('referrals.signals.track_signup')
    def test_track_user_signup_success(self, mock_track_signup, mock_get_request):
        """Test successful signup tracking."""
        # Create referrer first (before setting up mocks)
        referrer = create_user(email='referrer@example.com')
        identity = create_referral_identity(customer=referrer)

        # Now setup mocks for the new user creation
        request = self.factory.get('/')
        request.COOKIES = {'ref_token': identity.token}
        mock_get_request.return_value = request

        # Mock track_signup to return success
        mock_track_signup.return_value = (True, identity, 'Signup tracked')

        # Create new user (triggers signal)
        user = create_user(email='newuser@example.com')

        # Verify track_signup was called with the new user
        mock_track_signup.assert_called_with(user, request)

    @patch('referrals.signals.get_current_request')
    def test_track_user_signup_no_request(self, mock_get_request):
        """Test signup tracking with no request context."""
        # No request available
        mock_get_request.return_value = None

        # Create user (triggers signal)
        user = create_user(email='newuser@example.com')

        # Should not crash, just skip tracking
        self.assertIsNotNone(user)

    def test_track_user_signup_staff_user(self):
        """Test that staff users are not tracked."""
        # Create staff user
        user = create_user(email='staff@example.com', is_staff=True)

        # Should not create any events
        self.assertEqual(ReferralEvent.objects.count(), 0)

    @patch('referrals.signals.get_current_request')
    @patch('referrals.signals.track_signup')
    def test_track_user_signup_inactive_program(self, mock_track_signup, mock_get_request):
        """Test signup tracking when program is inactive."""
        # Deactivate program
        self.program.status = 'paused'
        self.program.save()

        # Setup mock request
        request = self.factory.get('/')
        mock_get_request.return_value = request

        # Create user
        user = create_user(email='newuser@example.com')

        # track_signup should not be called
        mock_track_signup.assert_not_called()


class OrderCompletionSignalTest(TestCase):
    """Tests for order completion and attribution signals."""

    def setUp(self):
        self.program = create_referral_program()
        self.factory = RequestFactory()

    @patch('referrals.signals.get_current_request')
    def test_order_completion_creates_attribution(self, mock_get_request):
        """Test that delivered order creates attribution."""
        # Setup referrer and referee
        referrer = create_user(email='referrer@example.com')
        referee = create_user(email='referee@example.com')
        identity = create_referral_identity(customer=referrer)

        # Setup mock request with referral cookie
        request = self.factory.get('/')
        request.COOKIES = {'ref_token': identity.token}
        mock_get_request.return_value = request

        # Create pending order
        order = create_order(user=referee, status='pending')

        # Change status to delivered (triggers signal)
        order.status = 'delivered'
        order.save()

        # Verify attribution was created
        self.assertEqual(ReferralAttribution.objects.count(), 1)
        attribution = ReferralAttribution.objects.first()
        self.assertEqual(attribution.referrer_identity, identity)
        self.assertEqual(attribution.referee_customer, referee)
        self.assertEqual(attribution.first_order, order)

    @patch('referrals.signals.get_current_request')
    def test_order_completion_self_referral_blocked(self, mock_get_request):
        """Test that self-referrals are blocked."""
        # Setup self-referral
        user = create_user(email='user@example.com')
        identity = create_referral_identity(customer=user)

        # Setup mock request with own referral cookie
        request = self.factory.get('/')
        request.COOKIES = {'ref_token': identity.token}
        mock_get_request.return_value = request

        # Create order
        order = create_order(user=user, status='pending')
        order.status = 'delivered'
        order.save()

        # Should NOT create attribution (self-referral)
        self.assertEqual(ReferralAttribution.objects.count(), 0)

    @patch('referrals.signals.get_current_request')
    def test_order_completion_no_cookie(self, mock_get_request):
        """Test order completion without referral cookie."""
        # Setup mock request without cookie
        request = self.factory.get('/')
        mock_get_request.return_value = request

        # Create order
        user = create_user()
        order = create_order(user=user, status='pending')
        order.status = 'delivered'
        order.save()

        # Should not create attribution
        self.assertEqual(ReferralAttribution.objects.count(), 0)

    @patch('referrals.signals.get_current_request')
    def test_order_completion_not_first_order(self, mock_get_request):
        """Test that only first order creates attribution."""
        # Setup referrer and referee
        referrer = create_user(email='referrer@example.com')
        referee = create_user(email='referee@example.com')
        identity = create_referral_identity(customer=referrer)

        # Create first order (already delivered)
        first_order = create_order(user=referee, status='delivered')

        # Setup mock request with referral cookie
        request = self.factory.get('/')
        request.COOKIES = {'ref_token': identity.token}
        mock_get_request.return_value = request

        # Create second order
        second_order = create_order(user=referee, status='pending')
        second_order.status = 'delivered'
        second_order.save()

        # Should not create attribution (not first order)
        self.assertEqual(ReferralAttribution.objects.count(), 0)

    @patch('referrals.signals.get_current_request')
    @patch('referrals.signals._create_and_issue_rewards')
    def test_order_completion_auto_approval(self, mock_create_rewards, mock_get_request):
        """Test auto-approval of low-risk attribution."""
        # Setup referrer and referee
        referrer = create_user(email='referrer@example.com')
        referee = create_user(email='referee@example.com')
        identity = create_referral_identity(customer=referrer)

        # Setup mock request
        request = self.factory.get('/')
        request.COOKIES = {'ref_token': identity.token}
        mock_get_request.return_value = request

        # Create and deliver order
        order = create_order(user=referee, status='pending')
        order.status = 'delivered'
        order.save()

        # Verify attribution was auto-approved
        attribution = ReferralAttribution.objects.first()
        self.assertEqual(attribution.status, 'approved')
        self.assertIsNotNone(attribution.approved_at)

        # Verify rewards were created
        mock_create_rewards.assert_called_once_with(attribution)

    def test_track_order_status_change(self):
        """Test that order status is tracked before save."""
        # Create order
        order = create_order(status='pending')

        # Change status
        order.status = 'delivered'
        order.save()

        # Verify previous status was tracked
        self.assertTrue(hasattr(order, '_previous_status'))


class AttributionApprovalSignalTest(TestCase):
    """Tests for attribution approval signal."""

    def setUp(self):
        self.program = create_referral_program()

    @patch('referrals.signals._create_and_issue_rewards')
    def test_manual_approval_creates_rewards(self, mock_create_rewards):
        """Test that manual approval creates rewards."""
        # Create pending attribution
        attribution = create_referral_attribution(status='pending')

        # Create admin user to simulate manual review
        admin = create_user(email='admin@example.com', is_staff=True)

        # Manually approve with reviewer
        attribution.status = 'approved'
        attribution.reviewed_by = admin
        attribution.save()

        # Verify rewards were created
        mock_create_rewards.assert_called_once_with(attribution)

    @patch('referrals.signals._create_and_issue_rewards')
    def test_rejection_does_not_create_rewards(self, mock_create_rewards):
        """Test that rejection doesn't create rewards."""
        # Create pending attribution
        attribution = create_referral_attribution(status='pending')

        # Reject
        attribution.status = 'rejected'
        attribution.rejection_reason = 'fraud_risk'
        attribution.save()

        # Should not create rewards
        mock_create_rewards.assert_not_called()

    def test_track_attribution_status_change(self):
        """Test that attribution status is tracked."""
        # Create attribution
        attribution = create_referral_attribution(status='pending')

        # Change status
        attribution.status = 'approved'
        attribution.save()

        # Verify previous status was tracked
        self.assertTrue(hasattr(attribution, '_previous_status'))


class RewardIssuanceSignalTest(TestCase):
    """Tests for reward issuance signal."""

    def setUp(self):
        self.program = create_referral_program()

    @patch('referrals.signals.send_referral_reward_email')
    def test_reward_issuance_sends_email(self, mock_send_email):
        """Test that reward issuance sends email."""
        # Create pending reward
        reward = create_referral_reward(status='pending', recipient_type='referrer')

        # Mock email success
        mock_send_email.return_value = True

        # Issue reward
        reward.status = 'issued'
        reward.save()

        # Verify email was sent
        mock_send_email.assert_called_once_with(reward, 'referrer')

    @patch('referrals.signals.send_referral_reward_email')
    def test_reward_redemption_no_email(self, mock_send_email):
        """Test that reward redemption doesn't send email."""
        # Create issued reward
        reward = create_referral_reward(status='issued')

        # Redeem reward
        reward.status = 'redeemed'
        reward.save()

        # Should not send email
        mock_send_email.assert_not_called()

    def test_track_reward_status_change(self):
        """Test that reward status is tracked."""
        # Create reward
        reward = create_referral_reward(status='pending')

        # Change status
        reward.status = 'issued'
        reward.save()

        # Verify previous status was tracked
        self.assertTrue(hasattr(reward, '_previous_status'))


class OrderCancellationSignalTest(TestCase):
    """Tests for order cancellation/refund signal."""

    def setUp(self):
        self.program = create_referral_program()

    def test_order_cancellation_rejects_attribution(self):
        """Test that order cancellation rejects attribution."""
        # Create approved attribution with delivered order
        attribution = create_referral_attribution(status='approved')
        order = attribution.first_order
        order.status = 'delivered'
        order.save()

        # Cancel order
        order.status = 'cancelled'
        order.save()

        # Verify attribution was rejected
        attribution.refresh_from_db()
        self.assertEqual(attribution.status, 'rejected')
        self.assertEqual(attribution.rejection_reason, 'order_cancelled')

    def test_order_refund_rejects_attribution(self):
        """Test that order refund rejects attribution."""
        # Create approved attribution with delivered order
        attribution = create_referral_attribution(status='approved')
        order = attribution.first_order
        order.status = 'delivered'
        order.save()

        # Refund order
        order.status = 'refunded'
        order.save()

        # Verify attribution was rejected
        attribution.refresh_from_db()
        self.assertEqual(attribution.status, 'rejected')
        self.assertEqual(attribution.rejection_reason, 'order_refunded')

    @patch('referrals.services.rewards.revoke_reward')
    def test_order_cancellation_revokes_rewards(self, mock_revoke_reward):
        """Test that order cancellation revokes issued rewards."""
        # Create approved attribution with rewards
        attribution = create_referral_attribution(status='approved')
        reward = create_referral_reward(
            attribution=attribution,
            status='issued'
        )

        # Mock revoke_reward success
        mock_revoke_reward.return_value = True

        # Get order and mark as delivered
        order = attribution.first_order
        order.status = 'delivered'
        order.save()

        # Cancel order
        order.status = 'cancelled'
        order.save()

        # Verify reward was revoked
        mock_revoke_reward.assert_called_once()
        call_args = mock_revoke_reward.call_args
        self.assertEqual(call_args[0][0], reward)
        self.assertIn('cancelled', call_args[1]['reason'])

    def test_already_rejected_attribution_not_processed(self):
        """Test that already rejected attribution is not re-processed."""
        # Create rejected attribution
        attribution = create_referral_attribution(status='rejected')
        order = attribution.first_order
        order.status = 'delivered'
        order.save()

        # Store initial rejection reason
        initial_reason = attribution.rejection_reason

        # Cancel order
        order.status = 'cancelled'
        order.save()

        # Verify attribution status unchanged
        attribution.refresh_from_db()
        self.assertEqual(attribution.status, 'rejected')
        self.assertEqual(attribution.rejection_reason, initial_reason)
