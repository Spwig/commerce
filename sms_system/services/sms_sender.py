"""
SMS Sending Service.

Handles queuing and sending SMS/WhatsApp messages through configured providers.
"""
import logging
from typing import Dict, Any, Optional

from django.utils import timezone

logger = logging.getLogger(__name__)


class SMSSendingService:
    """Service for sending SMS and WhatsApp messages."""

    def __init__(self):
        self._providers = {}

    def _get_provider(self, account):
        """Get provider instance for an account."""
        from sms_system.providers import get_provider_class

        cache_key = f"{account.provider_key}_{account.pk}"
        if cache_key not in self._providers:
            provider_class = get_provider_class(account.provider_key)
            if provider_class:
                self._providers[cache_key] = provider_class(account)
            else:
                raise ValueError(f"Unknown provider: {account.provider_key}")

        return self._providers[cache_key]

    def send_sms(
        self,
        phone: str,
        message: str,
        account=None,
        message_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an SMS message.

        Args:
            phone: Recipient phone number (E.164 format preferred)
            message: Message text
            account: Optional SMSProviderAccount (uses default if not provided)
            message_type: Optional message type for preference checking (e.g., 'order_shipped')

        Returns:
            Dict with success status and details
        """
        from sms_system.models import SMSProviderAccount, SMSOutbox

        # Check communication preferences if message_type provided
        if message_type:
            from accounts.services.preference_service import PreferenceService
            from accounts.models import CustomerProfile
            from django.contrib.auth import get_user_model

            User = get_user_model()

            try:
                # Try to find user by phone number
                profile = CustomerProfile.objects.filter(phone=phone).first()
                if profile:
                    user = profile.user

                    # Check if user should receive this SMS type
                    if not PreferenceService.check_sms_permission(user, message_type):
                        logger.info(
                            f"Skipping SMS to {phone} - preference disabled for {message_type}"
                        )

                        # Create skipped outbox entry for tracking
                        outbox = SMSOutbox.objects.create(
                            account=account or SMSProviderAccount.get_default_sms_account(),
                            message_type='sms',
                            phone=phone,
                            message=message,
                            status='skipped',
                            skip_reason='user_preference_disabled',
                        )

                        return {
                            'success': False,
                            'outbox_id': outbox.pk,
                            'skipped': True,
                            'reason': 'user_preference_disabled',
                        }

            except Exception as e:
                # If lookup fails, continue with sending (guest user)
                logger.debug(f"Could not check SMS preferences for {phone}: {e}")
                pass

        # Get account
        if not account:
            account = SMSProviderAccount.get_default_sms_account()

        if not account:
            logger.error("No SMS account configured")
            return {
                'success': False,
                'error': 'NO_ACCOUNT',
                'message': 'No SMS provider account configured',
            }

        # Sandbox mode: enforce SMS whitelist
        from core.sandbox.sms_guard import sandbox_filter_sms_recipient
        action, phone = sandbox_filter_sms_recipient(phone)
        if action == 'log':
            outbox = SMSOutbox.objects.create(
                account=account,
                message_type='sms',
                phone=phone,
                message=f'[SANDBOX] {message}',
                status='sandbox_logged',
            )
            logger.info(
                f"[SANDBOX] SMS to {phone} sandbox-logged "
                f"(not whitelisted), outbox_id={outbox.pk}"
            )
            return {
                'success': False,
                'outbox_id': outbox.pk,
                'skipped': True,
                'reason': 'sandbox_not_whitelisted',
            }

        # Create outbox entry
        outbox = SMSOutbox.objects.create(
            account=account,
            message_type='sms',
            phone=phone,
            message=message,
            status='pending',
        )

        # Send via provider
        try:
            provider = self._get_provider(account)
            result = provider.send_sms(phone, message)

            if result.get('success'):
                outbox.mark_sent(result.get('message_id', ''))
                logger.info(f"SMS sent to {phone}, message_id={result.get('message_id')}")
                return {
                    'success': True,
                    'outbox_id': outbox.pk,
                    'message_id': result.get('message_id'),
                }
            else:
                outbox.mark_failed(result.get('error', 'Unknown error'))
                return {
                    'success': False,
                    'outbox_id': outbox.pk,
                    'error': result.get('error'),
                }

        except Exception as e:
            logger.error(f"Failed to send SMS to {phone}: {e}", exc_info=True)
            outbox.mark_failed(str(e))
            return {
                'success': False,
                'outbox_id': outbox.pk,
                'error': str(e),
            }

    def send_whatsapp(
        self,
        phone: str,
        template_name: str,
        template_params: Dict[str, str],
        account=None,
    ) -> Dict[str, Any]:
        """
        Send a WhatsApp template message.

        Args:
            phone: Recipient phone number (E.164 format)
            template_name: WhatsApp template name (pre-approved by Meta)
            template_params: Template parameter values (e.g., {'1': 'value1', '2': 'value2'})
            account: Optional SMSProviderAccount (uses default WhatsApp if not provided)

        Returns:
            Dict with success status and details
        """
        from sms_system.models import SMSProviderAccount, SMSOutbox

        # Get account
        if not account:
            account = SMSProviderAccount.get_default_whatsapp_account()

        if not account:
            logger.error("No WhatsApp account configured")
            return {
                'success': False,
                'error': 'NO_ACCOUNT',
                'message': 'No WhatsApp provider account configured',
            }

        # Sandbox mode: enforce SMS whitelist (applies to WhatsApp too)
        from core.sandbox.sms_guard import sandbox_filter_sms_recipient
        action, phone = sandbox_filter_sms_recipient(phone)
        if action == 'log':
            message_preview = f"[SANDBOX] [Template: {template_name}] {template_params}"
            outbox = SMSOutbox.objects.create(
                account=account,
                message_type='whatsapp',
                phone=phone,
                message=message_preview,
                status='sandbox_logged',
            )
            logger.info(
                f"[SANDBOX] WhatsApp to {phone} sandbox-logged "
                f"(not whitelisted), outbox_id={outbox.pk}"
            )
            return {
                'success': False,
                'outbox_id': outbox.pk,
                'skipped': True,
                'reason': 'sandbox_not_whitelisted',
            }

        # Build message preview for logging
        message_preview = f"[Template: {template_name}] {template_params}"

        # Create outbox entry
        outbox = SMSOutbox.objects.create(
            account=account,
            message_type='whatsapp',
            phone=phone,
            message=message_preview,
            status='pending',
        )

        # Send via provider
        try:
            provider = self._get_provider(account)
            result = provider.send_whatsapp(phone, template_name, template_params)

            if result.get('success'):
                outbox.mark_sent(result.get('message_id', ''))
                logger.info(f"WhatsApp sent to {phone}, message_id={result.get('message_id')}")
                return {
                    'success': True,
                    'outbox_id': outbox.pk,
                    'message_id': result.get('message_id'),
                }
            else:
                outbox.mark_failed(result.get('error', 'Unknown error'))
                return {
                    'success': False,
                    'outbox_id': outbox.pk,
                    'error': result.get('error'),
                }

        except Exception as e:
            logger.error(f"Failed to send WhatsApp to {phone}: {e}", exc_info=True)
            outbox.mark_failed(str(e))
            return {
                'success': False,
                'outbox_id': outbox.pk,
                'error': str(e),
            }

    def send_template_sms(
        self,
        phone: str,
        template_type: str,
        context: Dict[str, Any],
        account=None,
    ) -> Dict[str, Any]:
        """
        Send SMS using a template.

        Args:
            phone: Recipient phone number
            template_type: Template type (e.g., 'pos_receipt')
            context: Template context variables
            account: Optional SMSProviderAccount

        Returns:
            Dict with success status and details
        """
        from sms_system.models import SMSTemplate

        # Get template
        try:
            template = SMSTemplate.objects.get(
                template_type=template_type,
                is_active=True,
            )
        except SMSTemplate.DoesNotExist:
            logger.error(f"SMS template not found: {template_type}")
            return {
                'success': False,
                'error': 'TEMPLATE_NOT_FOUND',
                'message': f'SMS template not found: {template_type}',
            }

        # Render message
        message = template.render(context)

        # Send with message_type for preference checking
        return self.send_sms(phone, message, account, message_type=template_type)

    def test_connection(self, account) -> Dict[str, Any]:
        """
        Test connection to an SMS provider.

        Args:
            account: SMSProviderAccount to test

        Returns:
            Dict with success status and message
        """
        try:
            provider = self._get_provider(account)
            result = provider.test_connection()

            # Update account status
            account.connection_status = 'success' if result.get('success') else 'failed'
            account.last_checked = timezone.now()
            account.save(update_fields=['connection_status', 'last_checked'])

            return result

        except Exception as e:
            logger.error(f"Connection test failed for {account}: {e}")
            account.connection_status = 'failed'
            account.last_checked = timezone.now()
            account.save(update_fields=['connection_status', 'last_checked'])

            return {
                'success': False,
                'message': str(e),
            }
