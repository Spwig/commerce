"""
Preference service for managing customer communication preferences.

Centralized service layer for checking permissions, updating preferences,
and handling verification workflows for email and SMS communications.
"""

import logging

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.utils import timezone

from accounts.constants import (
    TRANSACTIONAL_EMAIL_TYPES,
    get_message_type_category,
    is_locked_message_type,
)
from accounts.models import CommunicationPreference
from accounts.services.preference_audit_service import PreferenceAuditService

User = get_user_model()
logger = logging.getLogger(__name__)


class PreferenceService:
    """
    Centralized service for preference management.

    Provides methods for:
    - Creating/retrieving user preferences
    - Checking email/SMS permissions
    - Updating preferences with validation
    - Sending verification emails
    - Cache management for performance
    """

    # Cache TTL for preference checks (5 minutes)
    CACHE_TTL = 300

    @staticmethod
    def get_or_create_for_user(user) -> tuple[CommunicationPreference, bool]:
        """
        Get or create preferences for user with defaults.

        Args:
            user: User instance

        Returns:
            Tuple of (CommunicationPreference, created)
        """
        return CommunicationPreference.get_or_create_for_user(user)

    @classmethod
    def check_email_permission(cls, user, message_type: str) -> bool:
        """
        Check if user should receive email for given message type.

        This method implements the permission logic with caching for performance.

        Args:
            user: User instance
            message_type: Email type key (e.g., 'order_confirmation', 'newsletter')

        Returns:
            bool: True if email should be sent

        Examples:
            >>> PreferenceService.check_email_permission(user, 'order_confirmation')
            True  # Transactional always allowed
            >>> PreferenceService.check_email_permission(user, 'newsletter')
            False  # Requires opt-in + verification
        """
        # Check cache first for performance
        cache_key = f"email_pref:{user.id}:{message_type}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        try:
            prefs = CommunicationPreference.objects.get(user=user)
            result = prefs.should_send_email(message_type)

            # Cache the result
            cache.set(cache_key, result, cls.CACHE_TTL)
            return result

        except CommunicationPreference.DoesNotExist:
            # No preferences set - allow transactional only
            is_allowed = message_type in TRANSACTIONAL_EMAIL_TYPES
            cache.set(cache_key, is_allowed, cls.CACHE_TTL)
            return is_allowed

    @classmethod
    def check_sms_permission(cls, user, message_type: str) -> bool:
        """
        Check if user should receive SMS for given message type.

        All SMS requires explicit opt-in (TCPA compliance).

        Args:
            user: User instance
            message_type: SMS type key

        Returns:
            bool: True if SMS should be sent
        """
        # Check cache first
        cache_key = f"sms_pref:{user.id}:{message_type}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        try:
            prefs = CommunicationPreference.objects.get(user=user)
            result = prefs.should_send_sms(message_type)

            # Cache the result
            cache.set(cache_key, result, cls.CACHE_TTL)
            return result

        except CommunicationPreference.DoesNotExist:
            # No SMS without explicit consent
            cache.set(cache_key, False, cls.CACHE_TTL)
            return False

    @classmethod
    def update_preference(
        cls,
        user,
        channel: str,
        message_type: str,
        enabled: bool,
        frequency: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        request=None,
        source: str = "user",
    ) -> dict:
        """
        Update a single preference with validation and audit trail.

        Args:
            user: User instance
            channel: 'email' or 'sms'
            message_type: Message type key
            enabled: Whether to enable or disable
            frequency: Optional frequency setting (immediate, daily, weekly, monthly)
            ip_address: IP address for audit trail
            user_agent: User agent for audit trail
            request: HttpRequest object (optional)
            source: Change source ('user', 'admin', 'api', etc.)

        Returns:
            Dict with success status and any errors
        """
        try:
            prefs, created = cls.get_or_create_for_user(user)

            # Don't allow disabling locked (transactional) preferences
            if not enabled and is_locked_message_type(message_type):
                return {
                    "success": False,
                    "error": "Cannot disable required transactional communications",
                }

            # Capture old state for audit trail
            old_value = {}
            action = f"{channel}.{message_type}"

            # Determine category
            category, app = get_message_type_category(message_type)

            if channel == "email":
                if category == "marketing":
                    old_value["email_marketing"] = prefs.email_marketing
                    prefs.email_marketing = enabled
                    action = f"email_marketing.{message_type}"
                elif category == "app_specific" and app:
                    # Capture old app preference state
                    old_value[f"app_preferences.{app}"] = prefs.app_preferences.get(app, {}).copy()

                    # Update app-specific preference
                    if app not in prefs.app_preferences:
                        prefs.app_preferences[app] = (
                            CommunicationPreference.get_default_app_preferences()[app]
                        )

                    # Extract preference key from message type
                    pref_key = message_type.replace(f"{app}_", "")
                    prefs.app_preferences[app][pref_key] = enabled

                    # Update frequency if provided
                    if frequency:
                        prefs.app_preferences[app]["frequency"] = frequency

                    action = f"app.{app}.{pref_key}"

            elif channel == "sms":
                if category == "transactional":
                    old_value["sms_transactional"] = prefs.sms_transactional
                    prefs.sms_transactional = enabled
                    action = f"sms_transactional.{message_type}"
                elif category == "marketing":
                    old_value["sms_marketing"] = prefs.sms_marketing
                    prefs.sms_marketing = enabled
                    action = f"sms_marketing.{message_type}"

            # Update consent tracking if enabling marketing
            if enabled and category in ["marketing", "app_specific"]:
                if ip_address:
                    prefs.consent_ip = ip_address
                if user_agent:
                    prefs.consent_user_agent = user_agent
                prefs.consent_source = "preference_center"

            prefs.save()

            # Create new state for audit trail
            new_value = {}
            if channel == "email":
                if category == "marketing":
                    new_value["email_marketing"] = prefs.email_marketing
                elif category == "app_specific" and app:
                    new_value[f"app_preferences.{app}"] = prefs.app_preferences.get(app, {}).copy()
            elif channel == "sms":
                if category == "transactional":
                    new_value["sms_transactional"] = prefs.sms_transactional
                elif category == "marketing":
                    new_value["sms_marketing"] = prefs.sms_marketing

            # Log change to audit trail
            PreferenceAuditService.log_change(
                preference=prefs,
                action=action,
                old_value=old_value,
                new_value=new_value,
                request=request,
                source=source,
                ip_address=ip_address,
                user_agent=user_agent,
            )

            # Invalidate cache
            cls.invalidate_cache(user.id, channel, message_type)

            logger.info(
                f"Updated preference for user {user.id}: {channel}/{message_type} = {enabled}"
            )

            return {"success": True}

        except Exception as e:
            logger.error(f"Error updating preference: {e}")
            return {"success": False, "error": str(e)}

    @classmethod
    def invalidate_cache(cls, user_id: int, channel: str = None, message_type: str = None):
        """
        Invalidate cached preference checks.

        Args:
            user_id: User ID
            channel: Optional channel filter ('email' or 'sms')
            message_type: Optional message type filter
        """
        if channel and message_type:
            # Invalidate specific cache key
            cache_key = f"{channel}_pref:{user_id}:{message_type}"
            cache.delete(cache_key)
        else:
            # Build explicit key list from known message types and delete them
            from accounts.constants import ALL_EMAIL_TYPES, ALL_SMS_TYPES

            keys = []
            if channel != "sms":
                keys.extend(f"email_pref:{user_id}:{mt}" for mt in ALL_EMAIL_TYPES)
            if channel != "email":
                keys.extend(f"sms_pref:{user_id}:{mt}" for mt in ALL_SMS_TYPES)

            if keys:
                cache.delete_many(keys)

    @classmethod
    def send_verification_email(cls, user) -> dict:
        """
        Send double opt-in verification email for marketing communications.

        Args:
            user: User instance

        Returns:
            Dict with success status and verification token
        """
        import secrets

        try:
            prefs, _ = cls.get_or_create_for_user(user)

            # Generate verification token
            token = secrets.token_urlsafe(32)

            # Store in cache (expires in 24 hours)
            cache_key = f"email_verify:{token}"
            cache.set(
                cache_key,
                {
                    "user_id": user.id,
                    "timestamp": timezone.now().isoformat(),
                },
                timeout=86400,
            )

            # Import email service
            from email_system.services.email_sender import EmailSendingService

            # Send verification email
            site = Site.objects.get_current()
            verification_url = f"https://{site.domain}/accounts/verify-email/{token}/"

            EmailSendingService.send_template_email(
                to_email=user.email,
                template_type="email_verification",
                context={
                    "verification_url": verification_url,
                    "user": user,
                },
                language=prefs.language_code,
            )

            logger.info(f"Sent verification email to {user.email}")

            return {
                "success": True,
                "token": token,
                "expires_at": timezone.now() + timezone.timedelta(hours=24),
            }

        except Exception as e:
            logger.error(f"Error sending verification email: {e}")
            return {"success": False, "error": str(e)}

    @classmethod
    def verify_email(
        cls,
        token: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        request=None,
    ) -> dict:
        """
        Verify email address from token.

        Args:
            token: Verification token from email link
            ip_address: IP address for audit trail
            user_agent: User agent for audit trail
            request: HttpRequest object (optional)

        Returns:
            Dict with success status
        """
        cache_key = f"email_verify:{token}"
        data = cache.get(cache_key)

        if not data:
            return {"success": False, "error": "Invalid or expired token"}

        try:
            user = User.objects.get(id=data["user_id"])
            prefs, _ = cls.get_or_create_for_user(user)

            # Mark as verified
            prefs.email_verified = True
            prefs.email_verified_at = timezone.now()

            # Update consent tracking
            if ip_address:
                prefs.consent_ip = ip_address
            if user_agent:
                prefs.consent_user_agent = user_agent

            prefs.save()

            # Log verification to audit trail
            PreferenceAuditService.log_verification(
                preference=prefs,
                channel="email",
                request=request,
            )

            # Delete token
            cache.delete(cache_key)

            # Invalidate caches
            cls.invalidate_cache(user.id, "email")

            logger.info(f"Email verified for user {user.id}")

            return {"success": True, "user": user}

        except User.DoesNotExist:
            return {"success": False, "error": "User not found"}
        except Exception as e:
            logger.error(f"Error verifying email: {e}")
            return {"success": False, "error": str(e)}

    @classmethod
    def bulk_update_preferences(cls, user, updates: list) -> dict:
        """
        Update multiple preferences at once.

        Args:
            user: User instance
            updates: List of dicts with {channel, message_type, enabled, frequency}

        Returns:
            Dict with success status and any errors
        """
        errors = []

        for update in updates:
            result = cls.update_preference(
                user=user,
                channel=update.get("channel"),
                message_type=update.get("message_type"),
                enabled=update.get("enabled"),
                frequency=update.get("frequency"),
            )

            if not result["success"]:
                errors.append(
                    {"message_type": update.get("message_type"), "error": result.get("error")}
                )

        if errors:
            return {"success": False, "errors": errors}

        return {"success": True}

    @classmethod
    def unsubscribe_all(cls, user, reason: str = "", request=None) -> dict:
        """
        Unsubscribe from all non-transactional communications.

        Args:
            user: User instance
            reason: Optional reason for unsubscribing
            request: HttpRequest object (optional)

        Returns:
            Dict with success status
        """
        try:
            prefs, _ = cls.get_or_create_for_user(user)

            # Disable all marketing
            prefs.email_marketing = False
            prefs.sms_marketing = False

            # Disable all app preferences
            for app in prefs.app_preferences:
                prefs.app_preferences[app]["enabled"] = False

            prefs.save()

            # Log unsubscribe to audit trail
            PreferenceAuditService.log_unsubscribe_all(
                preference=prefs,
                reason=reason,
                request=request,
            )

            # Invalidate all caches for this user
            cls.invalidate_cache(user.id)

            logger.info(f"User {user.id} unsubscribed from all communications. Reason: {reason}")

            return {"success": True}

        except Exception as e:
            logger.error(f"Error unsubscribing user: {e}")
            return {"success": False, "error": str(e)}
