"""
Tests for SMS Verification functionality.

Tests the SMSVerificationService for TCPA-compliant SMS double opt-in
with 6-digit OTP codes, rate limiting, and security features.
"""
import pytest
import secrets
from datetime import timedelta
from unittest.mock import Mock, patch
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from accounts.models import CommunicationPreference, PreferenceChangeLog
from accounts.services.sms_verification_service import SMSVerificationService
from accounts.services.preference_service import PreferenceService
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.unit, pytest.mark.sms_verification]


class TestSMSCodeGeneration:
    """Test SMS verification code generation."""

    def test_code_length(self, db):
        """Test that generated code is exactly 6 digits."""
        code = SMSVerificationService.generate_verification_code()
        assert len(code) == 6

    def test_code_is_numeric(self, db):
        """Test that code contains only digits."""
        code = SMSVerificationService.generate_verification_code()
        assert code.isdigit()

    def test_code_uniqueness(self, db):
        """Test that multiple codes are different (randomness check)."""
        codes = [SMSVerificationService.generate_verification_code() for _ in range(100)]
        # Should have at least 90 unique codes out of 100
        assert len(set(codes)) >= 90

    def test_code_uses_secrets_module(self, db):
        """Test that code generation uses cryptographically secure randomness."""
        with patch('secrets.randbelow') as mock_randbelow:
            mock_randbelow.return_value = 5
            code = SMSVerificationService.generate_verification_code()
            # Should call randbelow 6 times (once per digit)
            assert mock_randbelow.call_count == 6
            # Should return "555555" when randbelow always returns 5
            assert code == "555555"


class TestSendVerificationCode:
    """Test sending SMS verification codes."""

    @patch('sms_system.services.sms_sender.SMSSendingService.send_template_sms')
    def test_send_code_success(self, mock_send_sms, db):
        """Test successful code sending."""
        user = UserFactory()
        phone_number = "+1234567890"

        # Mock SMS service to return success
        mock_send_sms.return_value = {'success': True}

        result = SMSVerificationService.send_verification_code(user, phone_number)

        assert result['success'] is True
        assert 'expires_at' in result
        assert result['phone_last_4'] == '7890'

        # Verify code was stored
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]
        assert len(prefs.sms_verification_code) == 6
        assert prefs.sms_verification_sent_at is not None

        # Verify SMS was sent with correct template
        mock_send_sms.assert_called_once()
        call_kwargs = mock_send_sms.call_args[1]
        assert call_kwargs['phone'] == phone_number
        assert call_kwargs['template_type'] == 'verification_code'
        assert 'code' in call_kwargs['context']
        assert call_kwargs['context']['expiry_minutes'] == 15

    @patch('sms_system.services.sms_sender.SMSSendingService.send_template_sms')
    def test_send_code_rate_limiting(self, mock_send_sms, db):
        """Test rate limiting after max attempts."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up state: 5 failed attempts, sent 30 minutes ago
        prefs.sms_verification_attempts = 5
        prefs.sms_verification_sent_at = timezone.now() - timedelta(minutes=30)
        prefs.save()

        mock_send_sms.return_value = {'success': True}

        result = SMSVerificationService.send_verification_code(user, phone_number)

        assert result['success'] is False
        assert 'Too many attempts' in result['error']
        assert 'cooldown_seconds' in result
        # Should have ~30 minutes remaining (60 - 30)
        assert result['cooldown_seconds'] > 1500  # ~30 minutes in seconds

        # SMS should not have been sent
        mock_send_sms.assert_not_called()

    @patch('sms_system.services.sms_sender.SMSSendingService.send_template_sms')
    def test_send_code_cooldown_expired(self, mock_send_sms, db):
        """Test that cooldown resets after 60 minutes."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up state: 5 failed attempts, sent 61 minutes ago (cooldown expired)
        prefs.sms_verification_attempts = 5
        prefs.sms_verification_sent_at = timezone.now() - timedelta(minutes=61)
        prefs.save()

        mock_send_sms.return_value = {'success': True}

        result = SMSVerificationService.send_verification_code(user, phone_number)

        # Should succeed because cooldown has expired
        assert result['success'] is True

        # Attempts should be reset
        prefs.refresh_from_db()
        assert prefs.sms_verification_attempts == 0

    @patch('sms_system.services.sms_sender.SMSSendingService.send_template_sms')
    def test_send_code_sms_failure(self, mock_send_sms, db):
        """Test handling of SMS sending failure."""
        user = UserFactory()
        phone_number = "+1234567890"

        # Mock SMS service to return failure
        mock_send_sms.return_value = {'success': False, 'error': 'Invalid phone number'}

        result = SMSVerificationService.send_verification_code(user, phone_number)

        assert result['success'] is False
        assert 'Invalid phone number' in result['error']

    def test_send_code_exception_handling(self, db):
        """Test that exceptions are caught and logged."""
        user = UserFactory()
        phone_number = "+1234567890"

        # Cause an exception by passing invalid data
        with patch('accounts.models.CommunicationPreference.objects.get_or_create') as mock_get:
            mock_get.side_effect = Exception("Database error")

            result = SMSVerificationService.send_verification_code(user, phone_number)

            assert result['success'] is False
            assert 'error' in result


class TestVerifyCode:
    """Test SMS code verification."""

    def test_verify_code_success(self, db):
        """Test successful code verification."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up verification code
        code = "123456"
        prefs.sms_verification_code = code
        prefs.sms_verification_sent_at = timezone.now()
        prefs.sms_verification_attempts = 2
        prefs.save()

        # Verify code
        result = SMSVerificationService.verify_code(
            user=user,
            code=code,
            phone_number=phone_number,
            ip_address="192.168.1.1",
            user_agent="TestBrowser/1.0"
        )

        assert result['success'] is True
        assert 'verified successfully' in result['message']

        # Check preference was updated
        prefs.refresh_from_db()
        assert prefs.sms_verified is True
        assert prefs.sms_verified_at is not None
        assert prefs.sms_verification_code == ''
        assert prefs.sms_verification_attempts == 0
        assert prefs.consent_ip == "192.168.1.1"
        assert prefs.consent_user_agent == "TestBrowser/1.0"

        # Check audit log was created
        logs = PreferenceChangeLog.objects.filter(
            user=user,
            action='sms_verified'
        )
        assert logs.count() == 1

    def test_verify_code_invalid(self, db):
        """Test verification with wrong code."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up verification code
        prefs.sms_verification_code = "123456"
        prefs.sms_verification_sent_at = timezone.now()
        prefs.sms_verification_attempts = 0
        prefs.save()

        # Try wrong code
        result = SMSVerificationService.verify_code(
            user=user,
            code="999999",
            phone_number=phone_number
        )

        assert result['success'] is False
        assert 'Invalid verification code' in result['error']
        assert result['attempts_remaining'] == 4

        # Check attempts were incremented
        prefs.refresh_from_db()
        assert prefs.sms_verification_attempts == 1
        assert prefs.sms_verified is False

    def test_verify_code_expired(self, db):
        """Test verification with expired code (>15 minutes)."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up expired code (sent 20 minutes ago)
        prefs.sms_verification_code = "123456"
        prefs.sms_verification_sent_at = timezone.now() - timedelta(minutes=20)
        prefs.save()

        result = SMSVerificationService.verify_code(
            user=user,
            code="123456",
            phone_number=phone_number
        )

        assert result['success'] is False
        assert 'expired' in result['error']

        # Code should be cleared
        prefs.refresh_from_db()
        assert prefs.sms_verification_code == ''

    def test_verify_code_no_code_exists(self, db):
        """Test verification when no code was sent."""
        user = UserFactory()
        phone_number = "+1234567890"

        result = SMSVerificationService.verify_code(
            user=user,
            code="123456",
            phone_number=phone_number
        )

        assert result['success'] is False
        assert 'No verification code found' in result['error']

    def test_verify_code_too_many_attempts(self, db):
        """Test verification after max attempts reached."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up code with 4 failed attempts
        prefs.sms_verification_code = "123456"
        prefs.sms_verification_sent_at = timezone.now()
        prefs.sms_verification_attempts = 4
        prefs.save()

        # Try wrong code (5th attempt)
        result = SMSVerificationService.verify_code(
            user=user,
            code="999999",
            phone_number=phone_number
        )

        assert result['success'] is False
        assert 'Too many failed attempts' in result['error']
        assert '60 minutes' in result['error']

    def test_verify_code_constant_time_comparison(self, db):
        """Test that constant-time comparison is used for security."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        prefs.sms_verification_code = "123456"
        prefs.sms_verification_sent_at = timezone.now()
        prefs.save()

        with patch('secrets.compare_digest') as mock_compare:
            mock_compare.return_value = False

            SMSVerificationService.verify_code(
                user=user,
                code="123456",
                phone_number=phone_number
            )

            # Verify secrets.compare_digest was called
            mock_compare.assert_called_once()

    def test_verify_code_updates_customer_profile(self, db):
        """Test that successful verification updates CustomerProfile phone."""
        from accounts.models import CustomerProfile

        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Create CustomerProfile
        profile = CustomerProfile.objects.create(user=user)

        # Set up verification code
        prefs.sms_verification_code = "123456"
        prefs.sms_verification_sent_at = timezone.now()
        prefs.save()

        # Verify code
        SMSVerificationService.verify_code(
            user=user,
            code="123456",
            phone_number=phone_number
        )

        # Check phone was updated
        profile.refresh_from_db()
        assert profile.phone == phone_number

    def test_verify_code_no_customer_profile(self, db):
        """Test verification succeeds even without CustomerProfile."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up verification code
        prefs.sms_verification_code = "123456"
        prefs.sms_verification_sent_at = timezone.now()
        prefs.save()

        # Verify code (should not crash despite missing CustomerProfile)
        result = SMSVerificationService.verify_code(
            user=user,
            code="123456",
            phone_number=phone_number
        )

        assert result['success'] is True


class TestResendCode:
    """Test resending SMS verification codes."""

    @patch('sms_system.services.sms_sender.SMSSendingService.send_template_sms')
    def test_resend_clears_old_code(self, mock_send_sms, db):
        """Test that resend clears the old code before sending new one."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up old code
        old_code = "111111"
        prefs.sms_verification_code = old_code
        prefs.save()

        mock_send_sms.return_value = {'success': True}

        result = SMSVerificationService.resend_code(user, phone_number)

        assert result['success'] is True

        # Verify new code is different
        prefs.refresh_from_db()
        assert prefs.sms_verification_code != old_code
        assert len(prefs.sms_verification_code) == 6

    @patch('sms_system.services.sms_sender.SMSSendingService.send_template_sms')
    def test_resend_respects_rate_limiting(self, mock_send_sms, db):
        """Test that resend still respects rate limiting."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up rate limit state
        prefs.sms_verification_attempts = 5
        prefs.sms_verification_sent_at = timezone.now() - timedelta(minutes=30)
        prefs.save()

        mock_send_sms.return_value = {'success': True}

        result = SMSVerificationService.resend_code(user, phone_number)

        # Should still be blocked by rate limit
        assert result['success'] is False
        assert 'Too many attempts' in result['error']


class TestCacheInvalidation:
    """Test that SMS verification invalidates preference cache."""

    def test_verify_invalidates_cache(self, db):
        """Test that successful verification invalidates cache."""
        user = UserFactory()
        phone_number = "+1234567890"
        prefs = CommunicationPreference.get_or_create_for_user(user)[0]

        # Set up verification code
        prefs.sms_verification_code = "123456"
        prefs.sms_verification_sent_at = timezone.now()
        prefs.save()

        # Prime the cache
        PreferenceService.check_sms_permission(user, 'test_message')

        # Verify code
        with patch('accounts.services.preference_service.PreferenceService.invalidate_cache') as mock_invalidate:
            SMSVerificationService.verify_code(
                user=user,
                code="123456",
                phone_number=phone_number
            )

            # Should invalidate SMS cache
            mock_invalidate.assert_called_once_with(user.id, 'sms')


class TestPhoneNumberFormatting:
    """Test phone number formatting in results."""

    @patch('sms_system.services.sms_sender.SMSSendingService.send_template_sms')
    def test_phone_last_4_digits(self, mock_send_sms, db):
        """Test that last 4 digits are extracted correctly."""
        user = UserFactory()
        mock_send_sms.return_value = {'success': True}

        result = SMSVerificationService.send_verification_code(user, "+1234567890")
        assert result['phone_last_4'] == '7890'

    @patch('sms_system.services.sms_sender.SMSSendingService.send_template_sms')
    def test_phone_last_4_short_number(self, mock_send_sms, db):
        """Test handling of short phone numbers."""
        user = UserFactory()
        mock_send_sms.return_value = {'success': True}

        result = SMSVerificationService.send_verification_code(user, "123")
        # Should return full number if less than 4 digits
        assert result['phone_last_4'] == '123'


class TestExceptionHandling:
    """Test error handling and logging."""

    def test_verify_code_exception_handling(self, db):
        """Test that exceptions are caught in verify_code."""
        user = UserFactory()

        # Cause exception by corrupting preference
        with patch('accounts.models.CommunicationPreference.objects') as mock_objects:
            mock_objects.get_or_create.side_effect = Exception("Database error")

            result = SMSVerificationService.verify_code(
                user=user,
                code="123456",
                phone_number="+1234567890"
            )

            assert result['success'] is False
            assert 'error' in result

    def test_resend_code_exception_handling(self, db):
        """Test that exceptions are caught in resend_code."""
        user = UserFactory()

        with patch('accounts.services.preference_service.PreferenceService.get_or_create_for_user') as mock_get:
            mock_get.side_effect = Exception("Database error")

            result = SMSVerificationService.resend_code(user, "+1234567890")

            assert result['success'] is False
            assert 'error' in result
