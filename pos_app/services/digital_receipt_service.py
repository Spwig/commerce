"""
Digital Receipt Service for POS Orders.

Handles sending receipts via email, SMS, and WhatsApp to customers
after POS transactions.
"""
import logging
import secrets
from decimal import Decimal
from typing import Optional, Dict, Any

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from core.models import SiteSettings
from core.utils.currency_helpers import format_money
from orders.models import Order

logger = logging.getLogger(__name__)


class DigitalReceiptService:
    """Service for sending digital receipts via email/SMS/WhatsApp."""

    # Token length for receipt URLs (32 bytes = 64 hex chars)
    TOKEN_LENGTH = 32

    def generate_receipt_token(self) -> str:
        """Generate a unique, URL-safe token for receipt access."""
        return secrets.token_urlsafe(self.TOKEN_LENGTH)

    def get_receipt_url(self, order: Order, request=None) -> str:
        """
        Generate a public URL for viewing the receipt.

        Args:
            order: Order instance
            request: Optional HTTP request for building absolute URL

        Returns:
            Full URL to view receipt
        """
        # Ensure order has a receipt token
        if not order.receipt_token:
            order.receipt_token = self.generate_receipt_token()
            order.save(update_fields=['receipt_token'])

        # Build the URL path
        receipt_path = reverse('public_receipt', kwargs={'token': order.receipt_token})

        if request:
            return request.build_absolute_uri(receipt_path)

        # Fallback to site settings domain
        site_settings = SiteSettings.get_settings()
        domain = site_settings.site_url if site_settings else ''
        if domain:
            return f"{domain.rstrip('/')}{receipt_path}"

        return receipt_path

    def build_email_context(self, order: Order, request=None) -> Dict[str, Any]:
        """
        Build context dictionary for the POS receipt email template.

        Args:
            order: Order instance with related data
            request: Optional HTTP request

        Returns:
            Dict with all template variables
        """
        site_settings = SiteSettings.get_settings()
        currency = str(order.total_amount.currency)

        # Store info
        store_name = site_settings.site_name if site_settings else 'Store'
        store_address_parts = []
        if site_settings:
            for part in [
                getattr(site_settings, 'address_line_1', ''),
                getattr(site_settings, 'city', ''),
                getattr(site_settings, 'state_province', ''),
                getattr(site_settings, 'postal_code', ''),
                getattr(site_settings, 'country', ''),
            ]:
                if part:
                    store_address_parts.append(str(part))
        store_address = ', '.join(store_address_parts)
        store_phone = str(getattr(site_settings, 'phone_number', '')) if site_settings else ''

        # Store logo URL
        store_logo_url = ''
        if site_settings and site_settings.site_logo:
            try:
                logo = site_settings.site_logo
                if logo.file:
                    if request:
                        store_logo_url = request.build_absolute_uri(logo.file.url)
                    else:
                        domain = site_settings.site_url if site_settings else ''
                        if domain:
                            store_logo_url = f"{domain.rstrip('/')}{logo.file.url}"
            except Exception as e:
                logger.warning(f"Could not get store logo URL: {e}")

        # Get receipt template settings if available
        receipt_template = None
        try:
            from pos_app.models import ReceiptTemplate
            warehouse = order.pos_terminal.warehouse if order.pos_terminal else None
            if warehouse:
                receipt_template = ReceiptTemplate.objects.filter(warehouse=warehouse).first()
            if not receipt_template:
                receipt_template = ReceiptTemplate.objects.filter(warehouse__isnull=True).first()
        except Exception:
            pass

        # Order items
        items = []
        for item in order.items.all():
            unit_price = item.unit_price.amount if hasattr(item.unit_price, 'amount') else Decimal(str(item.unit_price))
            line_total = item.total_price.amount if hasattr(item.total_price, 'amount') else Decimal(str(item.total_price))

            items.append({
                'name': f"{item.product_name}{' - ' + item.variant_name if item.variant_name else ''}",
                'product_name': item.product_name,
                'variant_name': item.variant_name or '',
                'sku': item.sku,
                'quantity': item.quantity,
                'unit_price': format_money(unit_price, currency),
                'line_total': format_money(line_total, currency),
            })

        # Payments
        payments = []
        total_change = Decimal('0')

        for p in order.pos_payments.all():
            change = Decimal('0')
            if p.change_given:
                change = p.change_given.amount if hasattr(p.change_given, 'amount') else Decimal(str(p.change_given))
                total_change += change

            amount = p.amount.amount if hasattr(p.amount, 'amount') else Decimal(str(p.amount))

            payments.append({
                'method': p.get_method_display(),
                'amount': format_money(amount, currency),
                'card_last4': p.card_last_four or '',
            })

        # Totals
        subtotal = order.subtotal.amount if hasattr(order.subtotal, 'amount') else Decimal(str(order.subtotal))
        tax_amount = order.tax_amount.amount if hasattr(order.tax_amount, 'amount') else Decimal('0')
        discount_amount = order.discount_amount.amount if hasattr(order.discount_amount, 'amount') else Decimal('0')
        total = order.total_amount.amount if hasattr(order.total_amount, 'amount') else Decimal(str(order.total_amount))

        # Loyalty points earned (if applicable)
        loyalty_points_earned = None
        try:
            from loyalty.models import PointsTransaction
            points_transaction = PointsTransaction.objects.filter(
                order=order,
                transaction_type='earned',
            ).first()
            if points_transaction:
                loyalty_points_earned = points_transaction.points
        except Exception:
            pass

        # Shop URL for assets
        shop_url = site_settings.site_url.rstrip('/') if site_settings and site_settings.site_url else ''

        # Build context
        context = {
            # Store info
            'store_name': receipt_template.get_effective_header() if receipt_template else store_name,
            'store_address': receipt_template.get_effective_address() if receipt_template else store_address,
            'store_phone': receipt_template.get_effective_phone() if receipt_template else store_phone,
            'store_logo_url': store_logo_url,
            'shop_url': shop_url,

            # Order details
            'order_number': order.order_number,
            'order_date': order.created_at.strftime('%b %d, %Y at %I:%M %p'),
            'cashier_name': order.cashier.get_full_name() if order.cashier else '',
            'terminal_name': order.pos_terminal.name if order.pos_terminal else '',

            # Items
            'items': items,

            # Totals
            'subtotal': format_money(subtotal, currency),
            'discount_amount': format_money(discount_amount, currency) if discount_amount else None,
            'tax_amount': format_money(tax_amount, currency) if tax_amount else None,
            'total': format_money(total, currency),
            'currency': currency,

            # Payments
            'payments': payments,
            'change_given': format_money(total_change, currency) if total_change else None,

            # Loyalty
            'loyalty_points_earned': loyalty_points_earned,

            # Footer
            'return_policy': receipt_template.return_policy if receipt_template else '',
            'receipt_url': self.get_receipt_url(order, request),
        }

        return context

    def send_email_receipt(
        self,
        order: Order,
        email: Optional[str] = None,
        request=None,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send receipt email for a POS order.

        Args:
            order: Order instance
            email: Email address (uses order.email if not provided)
            request: Optional HTTP request for building URLs
            language: Language code for template (optional)

        Returns:
            Dict with success status and details
        """
        from email_system.services.email_sender import EmailSendingService

        # Determine recipient email
        recipient_email = email or order.email
        if not recipient_email:
            return {
                'success': False,
                'error': 'NO_EMAIL',
                'message': 'No email address provided',
            }

        # Build context
        try:
            context = self.build_email_context(order, request)
        except Exception as e:
            logger.error(f"Failed to build email context for order {order.pk}: {e}", exc_info=True)
            return {
                'success': False,
                'error': 'CONTEXT_ERROR',
                'message': str(e),
            }

        # Send via email system
        try:
            outbox = EmailSendingService.send_template_email(
                to_email=recipient_email,
                template_type='pos_receipt',
                context=context,
                language=language,
            )

            # Update order tracking
            order.receipt_email_sent_at = timezone.now()
            if not order.email:
                order.email = recipient_email
            order.save(update_fields=['receipt_email_sent_at', 'email'])

            logger.info(f"Queued POS receipt email for order {order.order_number} to {recipient_email}")

            return {
                'success': True,
                'outbox_id': outbox.id,
                'email': recipient_email,
            }

        except Exception as e:
            logger.error(f"Failed to send receipt email for order {order.pk}: {e}", exc_info=True)
            return {
                'success': False,
                'error': 'SEND_ERROR',
                'message': str(e),
            }

    def build_sms_message(self, order: Order, request=None) -> str:
        """
        Build short SMS message for receipt notification.

        Args:
            order: Order instance
            request: Optional HTTP request

        Returns:
            SMS message text
        """
        site_settings = SiteSettings.get_settings()
        store_name = site_settings.site_name if site_settings else 'Store'
        currency = str(order.total_amount.currency)
        total = order.total_amount.amount if hasattr(order.total_amount, 'amount') else Decimal(str(order.total_amount))

        receipt_url = self.get_receipt_url(order, request)

        # Keep it short for SMS (160 char limit)
        message = (
            f"Thanks for shopping at {store_name}! "
            f"Order #{order.order_number}, Total: {format_money(total, currency)}. "
            f"View receipt: {receipt_url}"
        )

        return message

    def send_sms_receipt(
        self,
        order: Order,
        phone: Optional[str] = None,
        request=None,
    ) -> Dict[str, Any]:
        """
        Send receipt via SMS.

        Args:
            order: Order instance
            phone: Phone number (uses order.phone if not provided)
            request: Optional HTTP request for building URLs

        Returns:
            Dict with success status and details
        """
        # Determine recipient phone
        recipient_phone = phone or order.phone
        if not recipient_phone:
            return {
                'success': False,
                'error': 'NO_PHONE',
                'message': 'No phone number provided',
            }

        # Build message
        try:
            message = self.build_sms_message(order, request)
        except Exception as e:
            logger.error(f"Failed to build SMS message for order {order.pk}: {e}", exc_info=True)
            return {
                'success': False,
                'error': 'MESSAGE_ERROR',
                'message': str(e),
            }

        # Send via SMS system
        try:
            from sms_system.services.sms_sender import SMSSendingService

            sms_service = SMSSendingService()
            result = sms_service.send_sms(
                phone=recipient_phone,
                message=message,
            )

            if result.get('success'):
                # Update order tracking
                order.receipt_sms_sent_at = timezone.now()
                if not order.phone:
                    order.phone = recipient_phone
                order.save(update_fields=['receipt_sms_sent_at', 'phone'])

                logger.info(f"Sent POS receipt SMS for order {order.order_number} to {recipient_phone}")

            return result

        except ImportError:
            logger.warning("SMS system not available")
            return {
                'success': False,
                'error': 'SMS_NOT_CONFIGURED',
                'message': 'SMS sending is not configured',
            }
        except Exception as e:
            logger.error(f"Failed to send receipt SMS for order {order.pk}: {e}", exc_info=True)
            return {
                'success': False,
                'error': 'SEND_ERROR',
                'message': str(e),
            }

    def send_whatsapp_receipt(
        self,
        order: Order,
        phone: Optional[str] = None,
        request=None,
    ) -> Dict[str, Any]:
        """
        Send receipt via WhatsApp.

        Args:
            order: Order instance
            phone: Phone number (uses order.phone if not provided)
            request: Optional HTTP request for building URLs

        Returns:
            Dict with success status and details
        """
        # Determine recipient phone
        recipient_phone = phone or order.phone
        if not recipient_phone:
            return {
                'success': False,
                'error': 'NO_PHONE',
                'message': 'No phone number provided',
            }

        # Build context for WhatsApp template
        site_settings = SiteSettings.get_settings()
        store_name = site_settings.site_name if site_settings else 'Store'
        currency = str(order.total_amount.currency)
        total = order.total_amount.amount if hasattr(order.total_amount, 'amount') else Decimal(str(order.total_amount))
        receipt_url = self.get_receipt_url(order, request)

        # Send via SMS system (WhatsApp provider)
        try:
            from sms_system.services.sms_sender import SMSSendingService

            sms_service = SMSSendingService()
            result = sms_service.send_whatsapp(
                phone=recipient_phone,
                template_name='pos_receipt',
                template_params={
                    '1': store_name,
                    '2': order.order_number,
                    '3': format_money(total, currency),
                    '4': receipt_url,
                },
            )

            if result.get('success'):
                # Update order tracking (use SMS field for now)
                order.receipt_sms_sent_at = timezone.now()
                if not order.phone:
                    order.phone = recipient_phone
                order.save(update_fields=['receipt_sms_sent_at', 'phone'])

                logger.info(f"Sent POS receipt WhatsApp for order {order.order_number} to {recipient_phone}")

            return result

        except ImportError:
            logger.warning("SMS/WhatsApp system not available")
            return {
                'success': False,
                'error': 'WHATSAPP_NOT_CONFIGURED',
                'message': 'WhatsApp sending is not configured',
            }
        except Exception as e:
            logger.error(f"Failed to send receipt WhatsApp for order {order.pk}: {e}", exc_info=True)
            return {
                'success': False,
                'error': 'SEND_ERROR',
                'message': str(e),
            }


# Singleton instance
digital_receipt_service = DigitalReceiptService()
