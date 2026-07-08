"""
Celery Task Tests

Tests for background tasks: reward expiry, attribution management, and stats aggregation.
"""
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from ..tasks import (
    send_reward_expiry_reminders,
    expire_old_rewards,
    expire_old_attributions,
    update_referrer_stats,
    fraud_check_batch_process,
    cleanup_old_events,
    process_attribution,
)
from ..models import ReferralAttribution, ReferralReward, ReferralEvent
from .factories import (
    create_referral_program,
    create_referral_identity,
    create_referral_attribution,
    create_referral_reward,
    create_referral_event,
    create_user,
)


class RewardExpiryRemindersTaskTest(TestCase):
    """Tests for send_reward_expiry_reminders task."""

    def setUp(self):
        self.program = create_referral_program()

    @patch('referrals.services.email_notifications.send_reward_expiring_email')
    def test_sends_reminders_for_expiring_rewards(self, mock_send_email):
        """Test that reminders are sent for rewards expiring in 7 days."""
        # Mock email sending
        mock_send_email.return_value = True

        # Create reward expiring in 7 days
        seven_days_later = timezone.now() + timedelta(days=7)
        reward = create_referral_reward(
            status='issued',
            expires_at=seven_days_later
        )

        # Run task
        result = send_reward_expiry_reminders()

        # Verify result
        self.assertEqual(result['sent'], 1)
        self.assertEqual(result['failed'], 0)
        mock_send_email.assert_called_once()

    @patch('referrals.services.email_notifications.send_reward_expiring_email')
    def test_skips_rewards_not_expiring_soon(self, mock_send_email):
        """Test that rewards not expiring in 7 days are skipped."""
        # Create reward expiring in 10 days
        ten_days_later = timezone.now() + timedelta(days=10)
        create_referral_reward(
            status='issued',
            expires_at=ten_days_later
        )

        # Run task
        result = send_reward_expiry_reminders()

        # Should not send any emails
        self.assertEqual(result['sent'], 0)
        mock_send_email.assert_not_called()

    def test_handles_inactive_program(self):
        """Test that task skips when program is inactive."""
        self.program.status = 'paused'
        self.program.save()

        result = send_reward_expiry_reminders()

        self.assertEqual(result['sent'], 0)
        self.assertIn('not active', result['message'])


class ExpireOldRewardsTaskTest(TestCase):
    """Tests for expire_old_rewards task."""

    def setUp(self):
        self.program = create_referral_program()

    def test_expires_old_rewards(self):
        """Test that expired rewards are marked as expired."""
        # Create reward that expired yesterday
        yesterday = timezone.now() - timedelta(days=1)
        reward = create_referral_reward(
            status='issued',
            expires_at=yesterday
        )

        # Run task
        result = expire_old_rewards()

        # Verify reward was expired
        self.assertEqual(result['expired'], 1)
        reward.refresh_from_db()
        self.assertEqual(reward.status, 'expired')

    def test_skips_non_expired_rewards(self):
        """Test that non-expired rewards are not affected."""
        # Create reward expiring tomorrow
        tomorrow = timezone.now() + timedelta(days=1)
        reward = create_referral_reward(
            status='issued',
            expires_at=tomorrow
        )

        # Run task
        result = expire_old_rewards()

        # Should not expire
        self.assertEqual(result['expired'], 0)
        reward.refresh_from_db()
        self.assertEqual(reward.status, 'issued')


class ExpireOldAttributionsTaskTest(TestCase):
    """Tests for expire_old_attributions task."""

    def setUp(self):
        self.program = create_referral_program()
        # Set review period to 30 days
        self.program.fraud_policy = {'attribution_review_period_days': 30}
        self.program.save()

    def test_expires_old_pending_attributions(self):
        """Test that old pending attributions are expired."""
        # Create attribution that's 31 days old
        attribution = create_referral_attribution(status='pending')
        attribution.created_at = timezone.now() - timedelta(days=31)
        attribution.save()

        # Run task
        result = expire_old_attributions()

        # Verify attribution was expired
        self.assertEqual(result['expired'], 1)
        attribution.refresh_from_db()
        self.assertEqual(attribution.status, 'rejected')
        self.assertIn('expired', attribution.rejection_notes.lower())

    def test_skips_recent_attributions(self):
        """Test that recent attributions are not expired."""
        # Create attribution that's 20 days old
        attribution = create_referral_attribution(status='pending')
        attribution.created_at = timezone.now() - timedelta(days=20)
        attribution.save()

        # Run task
        result = expire_old_attributions()

        # Should not expire
        self.assertEqual(result['expired'], 0)
        attribution.refresh_from_db()
        self.assertEqual(attribution.status, 'pending')


class UpdateReferrerStatsTaskTest(TestCase):
    """Tests for update_referrer_stats task."""

    def setUp(self):
        self.program = create_referral_program()

    def test_updates_referrer_stats(self):
        """Test that referrer stats are updated correctly."""
        # Create referrer with approved attributions
        referrer = create_user(email='referrer@example.com')
        identity = create_referral_identity(customer=referrer)

        # Create 3 approved attributions
        attributions = []
        for i in range(3):
            referee = create_user(email=f'referee{i}@example.com')
            attr = create_referral_attribution(
                program=self.program,
                referrer_identity=identity,
                referee_customer=referee,
                status='approved'
            )
            attributions.append(attr)

        # Create rewards for each attribution
        for attribution in attributions:
            create_referral_reward(
                attribution=attribution,
                program=self.program,
                recipient_type='referrer',
                status='issued',
                amount=Decimal('10.00')
            )

        # Run task
        result = update_referrer_stats()

        # Verify stats were updated
        self.assertEqual(result['updated'], 1)
        identity.refresh_from_db()
        self.assertEqual(identity.total_conversions, 3)
        self.assertEqual(identity.total_rewards_earned, 30.0)

    def test_skips_unchanged_stats(self):
        """Test that identities with unchanged stats are skipped."""
        # Create identity with no activity
        create_referral_identity()

        # Run task twice
        result1 = update_referrer_stats()
        result2 = update_referrer_stats()

        # Second run should update 0 (stats unchanged)
        self.assertEqual(result2['updated'], 0)


class FraudCheckBatchProcessTaskTest(TestCase):
    """Tests for fraud_check_batch_process task."""

    def setUp(self):
        self.program = create_referral_program()

    @patch('referrals.services.validation.validate_attribution')
    def test_re_evaluates_high_risk_attributions(self, mock_validate):
        """Test that high-risk attributions are re-evaluated."""
        # Mock validation to return lower risk
        mock_validate.return_value = (True, {}, 20)

        # Create high-risk attribution from 25 hours ago
        attribution = create_referral_attribution(
            program=self.program,
            status='pending',
            risk_score=80
        )
        attribution.created_at = timezone.now() - timedelta(hours=25)
        attribution.save()

        # Run task
        result = fraud_check_batch_process()

        # Verify attribution was processed
        self.assertEqual(result['processed'], 1)
        mock_validate.assert_called_once()

    @patch('referrals.services.validation.validate_attribution')
    def test_auto_rejects_very_high_risk(self, mock_validate):
        """Test that very high risk attributions are auto-rejected."""
        # Mock validation to return very high risk
        mock_validate.return_value = (False, {}, 95)

        # Create high-risk attribution
        attribution = create_referral_attribution(
            program=self.program,
            status='pending',
            risk_score=80
        )
        attribution.created_at = timezone.now() - timedelta(hours=25)
        attribution.save()

        # Run task
        result = fraud_check_batch_process()

        # Verify attribution was auto-rejected
        self.assertEqual(result['auto_rejected'], 1)
        attribution.refresh_from_db()
        self.assertEqual(attribution.status, 'rejected')

    def test_skips_recent_attributions(self):
        """Test that recent high-risk attributions are skipped."""
        # Create high-risk attribution from 12 hours ago
        attribution = create_referral_attribution(
            program=self.program,
            status='pending',
            risk_score=80
        )
        attribution.created_at = timezone.now() - timedelta(hours=12)
        attribution.save()

        # Run task
        result = fraud_check_batch_process()

        # Should not process (too recent)
        self.assertEqual(result['processed'], 0)


class CleanupOldEventsTaskTest(TestCase):
    """Tests for cleanup_old_events task."""

    def setUp(self):
        self.program = create_referral_program()

    def test_deletes_old_view_events(self):
        """Test that old view/share events are deleted."""
        # Create old view event (91 days ago)
        identity = create_referral_identity()
        event = create_referral_event(
            referrer_identity=identity,
            event_type='view'
        )
        event.created_at = timezone.now() - timedelta(days=91)
        event.save()

        # Run task
        result = cleanup_old_events()

        # Verify event was deleted
        self.assertEqual(result['deleted'], 1)
        self.assertEqual(ReferralEvent.objects.filter(id=event.id).count(), 0)

    def test_keeps_important_events(self):
        """Test that important events (click, signup, order) are kept."""
        # Create old click event
        identity = create_referral_identity()
        event = create_referral_event(
            referrer_identity=identity,
            event_type='click'
        )
        event.created_at = timezone.now() - timedelta(days=91)
        event.save()

        # Run task
        result = cleanup_old_events()

        # Event should still exist
        self.assertEqual(result['deleted'], 0)
        self.assertEqual(ReferralEvent.objects.filter(id=event.id).count(), 1)

    def test_keeps_recent_events(self):
        """Test that recent events are kept."""
        # Create recent view event
        identity = create_referral_identity()
        event = create_referral_event(
            referrer_identity=identity,
            event_type='view'
        )

        # Run task
        result = cleanup_old_events()

        # Should not delete recent events
        self.assertEqual(result['deleted'], 0)


class ProcessAttributionTaskTest(TestCase):
    """Tests for process_attribution task."""

    def setUp(self):
        self.program = create_referral_program()

    @patch('referrals.services.validation.validate_attribution')
    @patch('referrals.services.rewards.create_rewards')
    @patch('referrals.services.rewards.issue_reward')
    def test_processes_approved_attribution(self, mock_issue, mock_create, mock_validate):
        """Test that approved attribution is processed."""
        # Mock validation and rewards
        mock_validate.return_value = (True, {}, 25)
        referrer_reward = create_referral_reward(status='pending')
        referee_reward = create_referral_reward(status='pending')
        mock_create.return_value = (referrer_reward, referee_reward)
        mock_issue.return_value = True

        # Create approved attribution
        attribution = create_referral_attribution(
            program=self.program,
            status='approved'
        )

        # Run task
        result = process_attribution(attribution.id)

        # Verify processing
        self.assertTrue(result['success'])
        self.assertEqual(result['attribution_id'], attribution.id)
        mock_validate.assert_called_once()
        mock_create.assert_called_once()

    @patch('referrals.services.validation.validate_attribution')
    def test_handles_pending_attribution(self, mock_validate):
        """Test that pending attribution is validated but not processed."""
        # Mock validation
        mock_validate.return_value = (True, {}, 25)

        # Create pending attribution
        attribution = create_referral_attribution(
            program=self.program,
            status='pending'
        )

        # Run task
        result = process_attribution(attribution.id)

        # Should validate but not create rewards
        self.assertFalse(result['success'])
        self.assertIn('not approved', result['error'])

    def test_handles_nonexistent_attribution(self):
        """Test that task handles nonexistent attribution gracefully."""
        # Run task with invalid ID
        result = process_attribution(9999)

        # Should return error
        self.assertFalse(result['success'])
        self.assertIn('not found', result['error'])
