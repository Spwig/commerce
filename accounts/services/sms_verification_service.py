"""
SMS Verification Service

Handles SMS double opt-in verification with 6-digit OTP codes for TCPA compliance.
Includes rate limiting and security features.
"""
import logging
import secrets
from datetime import timedelta
from typing import Dict
from django.utils import timezone
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


class SMSVerificationService:
    """
    Service for SMS verification with OTP codes.

    Implements TCPA-compliant SMS verification with:
    - 6-digit OTP codes
    - 15-minute TTL
    - Rate limiting (5 attempts, 60-minute cooldown)
    - Constant-time comparison for security
    """

    # Constants
    CODE_LENGTH = 6
    CODE_TTL_MINUTES = 15
    MAX_ATTEMPTS = 5
    COOLDOWN_MINUTES = 60

    @classmethod
    def generate_verification_code(cls) -> str:
        """
        Generate a secure 6-digit verification code.

        Uses secrets module for cryptographically strong randomness.

        Returns:
            str: 6-digit numeric code
        """
        # Generate 6 random digits using secrets
        code = ''.join(str(secrets.randbelow(10)) for _ in range(cls.CODE_LENGTH))
        return code

    @classmethod
    def send_verification_code(cls, user, phone_number: str) -> Dict:
        """
        Generate and send verification code via SMS.

        Args:
            user: User instance
            phone_number: Phone number to send code to

        Returns:
            Dict with success status, expiry time, and last 4 digits of phone
        """
        from accounts.models import CommunicationPreference
        from accounts.services.preference_service import PreferenceService

        try:
            # Get or create preference
            prefs, _ = PreferenceService.get_or_create_for_user(user)

            # Check cooldown (rate limiting)
            if prefs.sms_verification_sent_at:
                time_since_last = timezone.now() - prefs.sms_verification_sent_at
                cooldown_remaining = timedelta(minutes=cls.COOLDOWN_MINUTES) - time_since_last

                if cooldown_remaining.total_seconds() > 0 and prefs.sms_verification_attempts >= cls.MAX_ATTEMPTS:
                    return {
                        'success': False,
                        'error': 'Too many attempts. Please try again later.',
                        'cooldown_seconds': int(cooldown_remaining.total_seconds()),
                    }

            # Generate code
            code = cls.generate_verification_code()

            # Reset attempts if cooldown period has passed
            if prefs.sms_verification_sent_at and \
               timezone.now() - prefs.sms_verification_sent_at > timedelta(minutes=cls.COOLDOWN_MINUTES):
                prefs.sms_verification_attempts = 0

            # Store code and timestamp
            prefs.sms_verification_code = code
            prefs.sms_verification_sent_at = timezone.now()
            prefs.save(update_fields=[
                'sms_verification_code',
                'sms_verification_sent_at',
                'sms_verification_attempts',
                'updated_at'
            ])

            # Send SMS
            from sms_system.services.sms_sender import SMSSendingService

            # Use template for verification code SMS
            result = SMSSendingService.send_template_sms(
                phone=phone_number,
                template_type='verification_code',
                context={
                    'code': code,
                    'expiry_minutes': cls.CODE_TTL_MINUTES,
                },
            )

            if not result.get('success'):
                return {
                    'success': False,
                    'error': result.get('error', 'Failed to send SMS'),
                }

            expiry_time = timezone.now() + timedelta(minutes=cls.CODE_TTL_MINUTES)

            logger.info(
                f"Sent SMS verification code to {phone_number[-4:]} for user {user.id}"
            )

            return {
                'success': True,
                'expires_at': expiry_time,
                'phone_last_4': phone_number[-4:] if len(phone_number) >= 4 else phone_number,
            }

        except Exception as e:
            logger.error(f"Error sending SMS verification code: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
            }

    @classmethod
    def verify_code(cls, user, code: str, phone_number: str,
                    ip_address: str = None, user_agent: str = None) -> Dict:
        """
        Verify SMS code with security measures.

        Args:
            user: User instance
            code: 6-digit code from user
            phone_number: Phone number being verified
            ip_address: IP address for audit trail
            user_agent: User agent for audit trail

        Returns:
            Dict with success status
        """
        from accounts.models import CommunicationPreference, CustomerProfile
        from accounts.services.preference_service import PreferenceService
        from accounts.services.preference_audit_service import PreferenceAuditService

        try:
            # Get preference
            prefs, _ = PreferenceService.get_or_create_for_user(user)

            # Check if code exists
            if not prefs.sms_verification_code:
                return {
                    'success': False,
                    'error': 'No verification code found. Please request a new code.',
                }

            # Check TTL (15 minutes)
            if prefs.sms_verification_sent_at:
                time_since_sent = timezone.now() - prefs.sms_verification_sent_at
                if time_since_sent > timedelta(minutes=cls.CODE_TTL_MINUTES):
                    # Clear expired code
                    prefs.sms_verification_code = ''
                    prefs.save(update_fields=['sms_verification_code', 'updated_at'])

                    return {
                        'success': False,
                        'error': 'Verification code has expired. Please request a new code.',
                    }

            # Verify code with constant-time comparison (security best practice)
            if not secrets.compare_digest(prefs.sms_verification_code, code):
                # Increment failed attempts
                prefs.sms_verification_attempts += 1
                prefs.save(update_fields=['sms_verification_attempts', 'updated_at'])

                remaining_attempts = cls.MAX_ATTEMPTS - prefs.sms_verification_attempts

                if remaining_attempts <= 0:
                    return {
                        'success': False,
                        'error': f'Too many failed attempts. Please wait {cls.COOLDOWN_MINUTES} minutes and request a new code.',
                    }

                return {
                    'success': False,
                    'error': 'Invalid verification code.',
                    'attempts_remaining': remaining_attempts,
                }

            # Success! Mark as verified
            prefs.sms_verified = True
            prefs.sms_verified_at = timezone.now()

            # Clear verification code and reset attempts
            prefs.sms_verification_code = ''
            prefs.sms_verification_attempts = 0

            # Update consent tracking
            if ip_address:
                prefs.consent_ip = ip_address
            if user_agent:
                prefs.consent_user_agent = user_agent

            prefs.save()

            # Update phone number in CustomerProfile
            try:
                profile = CustomerProfile.objects.get(user=user)
                profile.phone = phone_number
                profile.save(update_fields=['phone', 'updated_at'])
            except CustomerProfile.DoesNotExist:
                pass

            # Create audit log
            PreferenceAuditService.log_verification(
                preference=prefs,
                channel='sms',
            )

            # Invalidate caches
            PreferenceService.invalidate_cache(user.id, 'sms')

            logger.info(f"SMS verified for user {user.id}")

            return {
                'success': True,
                'message': 'SMS number verified successfully',
            }

        except Exception as e:
            logger.error(f"Error verifying SMS code: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
            }

    @classmethod
    def resend_code(cls, user, phone_number: str) -> Dict:
        """
        Resend verification code (clears old code first).

        Args:
            user: User instance
            phone_number: Phone number to send code to

        Returns:
            Dict with success status
        """
        from accounts.services.preference_service import PreferenceService

        try:
            # Get preference
            prefs, _ = PreferenceService.get_or_create_for_user(user)

            # Clear old code
            prefs.sms_verification_code = ''
            prefs.save(update_fields=['sms_verification_code', 'updated_at'])

            # Send new code
            return cls.send_verification_code(user, phone_number)

        except Exception as e:
            logger.error(f"Error resending SMS code: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
            }
