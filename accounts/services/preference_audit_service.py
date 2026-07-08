"""
Preference Audit Service

Handles audit logging for communication preference changes with GDPR Article 7
compliance (proof of consent).
"""
import logging
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


class PreferenceAuditService:
    """
    Service for creating audit logs of preference changes.

    Follows the pattern from admin_api/services/audit_service.py with
    try/except wrappers to never fail the main operation.
    """

    @classmethod
    def log_change(cls, preference, action, old_value, new_value, request=None,
                   source='user', notes='', ip_address=None, user_agent=None):
        """
        Log a preference change with full context.

        Args:
            preference: CommunicationPreference instance
            action: Action description (e.g., "email_marketing.enable")
            old_value: Dict of old state
            new_value: Dict of new state
            request: HttpRequest object (optional)
            source: Change source ('user', 'admin', 'api', etc.)
            notes: Additional context
            ip_address: Override IP address (if request not provided)
            user_agent: Override user agent (if request not provided)

        Returns:
            PreferenceChangeLog instance or None if logging failed
        """
        from ..models import PreferenceChangeLog

        try:
            # Extract IP and user agent from request if provided
            if request:
                ip_address = ip_address or cls._get_client_ip(request)
                user_agent = user_agent or request.META.get('HTTP_USER_AGENT', '')

            # Ensure user_agent has a default value
            if user_agent is None:
                user_agent = ''

            # Create audit log
            log_entry = PreferenceChangeLog.objects.create(
                user=preference.user,
                preference=preference,
                action=action,
                old_value=old_value,
                new_value=new_value,
                ip_address=ip_address,
                user_agent=user_agent,
                source=source,
                notes=notes,
            )

            logger.info(
                f"Preference change logged: user={preference.user.email}, "
                f"action={action}, source={source}"
            )

            return log_entry

        except Exception as e:
            # Never fail the main operation because of logging issues
            extra_data = {
                'action': action,
                'source': source,
            }
            # Only add user email if preference is not None
            if preference and hasattr(preference, 'user'):
                extra_data['user'] = preference.user.email

            logger.error(
                f"Failed to log preference change: {e}",
                exc_info=True,
                extra=extra_data
            )
            return None

    @classmethod
    def log_verification(cls, preference, channel, request=None):
        """
        Log email or SMS verification completion.

        Args:
            preference: CommunicationPreference instance
            channel: 'email' or 'sms'
            request: HttpRequest object (optional)

        Returns:
            PreferenceChangeLog instance or None
        """
        action = f"{channel}_verified"
        old_value = {f"{channel}_verified": False}
        new_value = {f"{channel}_verified": True}

        return cls.log_change(
            preference=preference,
            action=action,
            old_value=old_value,
            new_value=new_value,
            request=request,
            source='verification',
            notes=f'{channel.upper()} verification completed'
        )

    @classmethod
    def log_bulk_update(cls, preference, changes, request=None, source='user'):
        """
        Log multiple preference changes in a single entry.

        Args:
            preference: CommunicationPreference instance
            changes: Dict of field changes {field: {'old': value, 'new': value}}
            request: HttpRequest object (optional)
            source: Change source

        Returns:
            PreferenceChangeLog instance or None
        """
        # Build action description
        field_names = list(changes.keys())
        if len(field_names) == 1:
            action = f"bulk_update.{field_names[0]}"
        else:
            action = f"bulk_update.{len(field_names)}_fields"

        # Extract old and new values
        old_value = {field: change['old'] for field, change in changes.items()}
        new_value = {field: change['new'] for field, change in changes.items()}

        return cls.log_change(
            preference=preference,
            action=action,
            old_value=old_value,
            new_value=new_value,
            request=request,
            source=source,
            notes=f"Updated {len(field_names)} fields: {', '.join(field_names)}"
        )

    @classmethod
    def log_unsubscribe_all(cls, preference, reason, request=None):
        """
        Log unsubscribe all marketing communications action.

        Args:
            preference: CommunicationPreference instance
            reason: Unsubscribe reason (optional)
            request: HttpRequest object (optional)

        Returns:
            PreferenceChangeLog instance or None
        """
        old_value = {
            'email_marketing': True,
            'sms_marketing': True,
            'app_preferences': preference.app_preferences.copy()
        }

        new_value = {
            'email_marketing': False,
            'sms_marketing': False,
            'app_preferences': {}  # All apps disabled
        }

        notes = 'Unsubscribed from all marketing communications'
        if reason:
            notes += f' - Reason: {reason}'

        return cls.log_change(
            preference=preference,
            action='unsubscribe_all',
            old_value=old_value,
            new_value=new_value,
            request=request,
            source='unsubscribe',
            notes=notes
        )

    @classmethod
    def _get_client_ip(cls, request):
        """
        Extract client IP address from request.

        Handles proxy headers (X-Forwarded-For) for accurate IP tracking.

        Args:
            request: HttpRequest object

        Returns:
            str: IP address or None
        """
        # Check X-Forwarded-For header first (proxy support)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Take the first IP (client IP)
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Fallback to REMOTE_ADDR
            ip = request.META.get('REMOTE_ADDR')

        return ip
