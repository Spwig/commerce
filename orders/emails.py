"""
Email notifications for order-related events.
Returns & RMA workflow + order status updates.
"""

import logging

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def send_return_request_confirmation(return_request):
    """
    Send confirmation email to customer when return request is created.

    Args:
        return_request: ReturnRequest instance

    Returns:
        bool: True if email queued successfully
    """
    try:
        from email_system.services.email_sender import EmailSendingService
        from email_system.utils.language import get_order_email_language

        order = return_request.order
        EmailSendingService.send_template_email(
            to_email=return_request.user.email,
            template_type="return_request_confirmation",
            context={
                "customer_name": return_request.user.get_full_name()
                or return_request.user.username,
                "order_number": order.order_number,
                "return_reason": return_request.get_reason_display(),
                "items_count": len(return_request.items_json),
                "return_status": return_request.get_status_display(),
            },
            language=get_order_email_language(order),
            enable_tracking=True,
        )
        logger.info(
            f"Return request confirmation queued for {return_request.user.email} (return {return_request.id})"
        )
        return True

    except Exception as e:
        logger.error(
            f"Failed to send return request confirmation for return {return_request.id}: {e}",
            exc_info=True,
        )
        return False


def send_return_approved_notification(return_request):
    """
    Send notification when return request is approved.

    Args:
        return_request: ReturnRequest instance
    """
    try:
        from email_system.services.email_sender import EmailSendingService
        from email_system.utils.language import get_order_email_language

        order = return_request.order
        EmailSendingService.send_template_email(
            to_email=return_request.user.email,
            template_type="return_request_approved",
            context={
                "customer_name": return_request.user.get_full_name()
                or return_request.user.username,
                "order_number": order.order_number,
                "return_label_url": return_request.return_label_url or "",
                "return_tracking_number": return_request.return_tracking_number or "",
            },
            language=get_order_email_language(order),
            enable_tracking=True,
        )
        logger.info(
            f"Return approved notification queued for {return_request.user.email} (return {return_request.id})"
        )

    except Exception as e:
        logger.error(
            f"Failed to send return approved notification for return {return_request.id}: {e}",
            exc_info=True,
        )


def send_return_rejected_notification(return_request):
    """
    Send notification when return request is rejected.

    Args:
        return_request: ReturnRequest instance (with rejection_reason set)
    """
    try:
        from email_system.services.email_sender import EmailSendingService
        from email_system.utils.language import get_order_email_language

        order = return_request.order
        EmailSendingService.send_template_email(
            to_email=return_request.user.email,
            template_type="return_request_rejected",
            context={
                "customer_name": return_request.user.get_full_name()
                or return_request.user.username,
                "order_number": order.order_number,
                "rejection_reason": return_request.rejection_reason or "",
            },
            language=get_order_email_language(order),
            enable_tracking=True,
        )
        logger.info(
            f"Return rejected notification queued for {return_request.user.email} (return {return_request.id})"
        )

    except Exception as e:
        logger.error(
            f"Failed to send return rejected notification for return {return_request.id}: {e}",
            exc_info=True,
        )


def send_return_received_notification(return_request):
    """
    Send notification to customer when return package is received at warehouse.

    Args:
        return_request: ReturnRequest instance
    """
    try:
        from email_system.services.email_sender import EmailSendingService
        from email_system.utils.language import get_order_email_language

        order = return_request.order
        EmailSendingService.send_template_email(
            to_email=return_request.user.email,
            template_type="return_received",
            context={
                "customer_name": return_request.user.get_full_name()
                or return_request.user.username,
                "order_number": order.order_number,
            },
            language=get_order_email_language(order),
            enable_tracking=True,
        )
        logger.info(
            f"Return received notification queued for {return_request.user.email} (return {return_request.id})"
        )

    except Exception as e:
        logger.error(
            f"Failed to send return received notification for return {return_request.id}: {e}",
            exc_info=True,
        )


def send_inspection_reminder_to_staff(return_request):
    """
    Send inspection reminder to all active staff members when a return is received.

    Args:
        return_request: ReturnRequest instance
    """
    try:
        from django.contrib.auth import get_user_model
        from django.contrib.sites.models import Site

        from email_system.services.email_sender import EmailSendingService

        User = get_user_model()
        staff_emails = list(
            User.objects.filter(is_staff=True, is_active=True)
            .exclude(email="")
            .values_list("email", flat=True)
        )

        if not staff_emails:
            logger.warning(
                f"No staff emails found for inspection reminder (return {return_request.id})"
            )
            return

        try:
            site = Site.objects.get_current()
            site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
        except Exception:
            site_url = getattr(settings, "SITE_URL", "http://localhost:8000")

        order = return_request.order
        context = {
            "order_number": order.order_number,
            "received_at": (return_request.received_at or timezone.now()).strftime("%B %d, %Y"),
            "items_count": len(return_request.items_json) if return_request.items_json else 0,
            "admin_url": f"{site_url}/en/admin/orders/returnrequest/{return_request.id}/change/",
        }

        for staff_email in staff_emails:
            try:
                EmailSendingService.send_template_email(
                    to_email=staff_email,
                    template_type="admin_return_inspection_reminder",
                    context=context,
                    language="en",
                    enable_tracking=False,
                )
            except Exception as e:
                logger.error(
                    f"Failed to send inspection reminder to {staff_email}: {e}", exc_info=True
                )

        logger.info(
            f"Inspection reminder queued for {len(staff_emails)} staff member(s) (return {return_request.id})"
        )

    except Exception as e:
        logger.error(
            f"Failed to send inspection reminders for return {return_request.id}: {e}",
            exc_info=True,
        )


def send_refund_processed_notification(return_request):
    """
    Send notification when refund is processed after return inspection.

    Args:
        return_request: ReturnRequest instance with linked refund
    """
    try:
        from email_system.services.email_sender import EmailSendingService
        from email_system.utils.language import get_order_email_language

        if not return_request.refund:
            logger.warning(
                f"Cannot send refund notification for return {return_request.id} - no refund linked"
            )
            return

        order = return_request.order
        refund = return_request.refund

        restocking_fee = ""
        restocking_fee_currency = ""
        if return_request.restocking_fee and return_request.restocking_fee.amount > 0:
            restocking_fee = str(return_request.restocking_fee.amount)
            restocking_fee_currency = str(return_request.restocking_fee.currency)

        EmailSendingService.send_template_email(
            to_email=return_request.user.email,
            template_type="return_refund_processed",
            context={
                "customer_name": return_request.user.get_full_name()
                or return_request.user.username,
                "order_number": order.order_number,
                "refund_amount": str(refund.total_amount.amount),
                "refund_currency": str(refund.total_amount.currency),
                "restocking_fee": restocking_fee,
                "restocking_fee_currency": restocking_fee_currency,
            },
            language=get_order_email_language(order),
            enable_tracking=True,
        )
        logger.info(
            f"Refund processed notification queued for {return_request.user.email} (return {return_request.id})"
        )

    except Exception as e:
        logger.error(
            f"Failed to send refund processed notification for return {return_request.id}: {e}",
            exc_info=True,
        )


def send_order_status_update(order, old_status):
    """
    Send generic order status update notification to customer.

    Args:
        order: Order instance (already saved with new status)
        old_status: The previous status string before the change
    """
    try:
        from django.contrib.sites.models import Site

        from email_system.services.email_sender import EmailSendingService
        from email_system.utils.language import get_order_email_language

        try:
            site = Site.objects.get_current()
            site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
        except Exception:
            site_url = getattr(settings, "SITE_URL", "http://localhost:8000")

        status_display_map = dict(order.STATUS_CHOICES)

        EmailSendingService.send_template_email(
            to_email=order.email,
            template_type="order_status_update",
            context={
                "customer_name": order.shipping_name,
                "order_number": order.order_number,
                "old_status_display": str(status_display_map.get(old_status, old_status)),
                "new_status_display": str(status_display_map.get(order.status, order.status)),
                "order_url": f"{site_url}/orders/{order.order_number}/",
            },
            language=get_order_email_language(order),
            enable_tracking=True,
        )
        logger.info(
            f"Order status update notification queued for {order.email} (order {order.order_number})"
        )

    except Exception as e:
        logger.error(
            f"Failed to send order status update email for order {order.order_number}: {e}",
            exc_info=True,
        )
