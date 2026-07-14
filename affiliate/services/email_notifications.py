"""
Affiliate Email Notification Service

Handles sending email notifications for affiliate program events.
"""

import logging

from django.contrib.sites.models import Site
from django.utils import timezone

from email_system.utils.language import get_user_email_language

logger = logging.getLogger(__name__)


# ============================================================================
# AFFILIATE ACCOUNT STATUS EMAILS
# ============================================================================


def send_affiliate_approved_email(affiliate):
    """
    Send email notification when affiliate account is approved.

    Args:
        affiliate (Affiliate): The affiliate instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": affiliate.user.get_full_name() or affiliate.user.email,
            "affiliate_code": affiliate.affiliate_code,
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "shop_url": f"https://{site.domain}",
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=affiliate.user.email,
            template_type="affiliate_account_approved",
            context=context,
            language=get_user_email_language(affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_account_approved email to {affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued affiliate_account_approved email to {affiliate.user.email}")
            return True
        else:
            logger.error(f"Failed to send affiliate_account_approved email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending affiliate approved email: {e}", exc_info=True)
        return False


def send_affiliate_rejected_email(affiliate):
    """
    Send email notification when affiliate account is rejected.

    Args:
        affiliate (Affiliate): The affiliate instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": affiliate.user.get_full_name() or affiliate.user.email,
            "shop_name": site.name,
            "shop_url": f"https://{site.domain}",
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=affiliate.user.email,
            template_type="affiliate_account_rejected",
            context=context,
            language=get_user_email_language(affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_account_rejected email to {affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued affiliate_account_rejected email to {affiliate.user.email}")
            return True
        else:
            logger.error(f"Failed to send affiliate_account_rejected email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending affiliate rejected email: {e}", exc_info=True)
        return False


def send_affiliate_suspended_email(affiliate):
    """
    Send email notification when affiliate account is suspended.

    Args:
        affiliate (Affiliate): The affiliate instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": affiliate.user.get_full_name() or affiliate.user.email,
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=affiliate.user.email,
            template_type="affiliate_account_suspended",
            context=context,
            language=get_user_email_language(affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_account_suspended email to {affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued affiliate_account_suspended email to {affiliate.user.email}")
            return True
        else:
            logger.error(
                f"Failed to send affiliate_account_suspended email: status={outbox.status}"
            )
            return False

    except Exception as e:
        logger.error(f"Error sending affiliate suspended email: {e}", exc_info=True)
        return False


def send_affiliate_activated_email(affiliate):
    """
    Send email notification when affiliate account is reactivated.

    Args:
        affiliate (Affiliate): The affiliate instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": affiliate.user.get_full_name() or affiliate.user.email,
            "affiliate_code": affiliate.affiliate_code,
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "shop_url": f"https://{site.domain}",
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=affiliate.user.email,
            template_type="affiliate_account_activated",
            context=context,
            language=get_user_email_language(affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_account_activated email to {affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued affiliate_account_activated email to {affiliate.user.email}")
            return True
        else:
            logger.error(
                f"Failed to send affiliate_account_activated email: status={outbox.status}"
            )
            return False

    except Exception as e:
        logger.error(f"Error sending affiliate activated email: {e}", exc_info=True)
        return False


# ============================================================================
# PROGRAM MEMBERSHIP EMAILS
# ============================================================================


def send_program_membership_approved_email(membership):
    """
    Send email notification when program membership is approved.

    Args:
        membership (AffiliateProgramMembership): The membership instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": membership.affiliate.user.get_full_name()
            or membership.affiliate.user.email,
            "program_name": membership.program.name,
            "program_description": membership.program.description,
            "commission_rate": str(membership.program.commission_value),
            "commission_type": membership.program.get_commission_type_display(),
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=membership.affiliate.user.email,
            template_type="affiliate_program_approved",
            context=context,
            language=get_user_email_language(membership.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_program_approved email to {membership.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(
                f"Queued affiliate_program_approved email to {membership.affiliate.user.email}"
            )
            return True
        else:
            logger.error(f"Failed to send affiliate_program_approved email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending program membership approved email: {e}", exc_info=True)
        return False


def send_program_membership_rejected_email(membership):
    """
    Send email notification when program membership is rejected.

    Args:
        membership (AffiliateProgramMembership): The membership instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": membership.affiliate.user.get_full_name()
            or membership.affiliate.user.email,
            "program_name": membership.program.name,
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=membership.affiliate.user.email,
            template_type="affiliate_program_rejected",
            context=context,
            language=get_user_email_language(membership.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_program_rejected email to {membership.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(
                f"Queued affiliate_program_rejected email to {membership.affiliate.user.email}"
            )
            return True
        else:
            logger.error(f"Failed to send affiliate_program_rejected email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending program membership rejected email: {e}", exc_info=True)
        return False


# ============================================================================
# COMMISSION EMAILS
# ============================================================================


def send_commission_earned_email(commission):
    """
    Send email notification when new commission is created.

    Args:
        commission (Commission): The commission instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": commission.affiliate.user.get_full_name()
            or commission.affiliate.user.email,
            "commission_amount": str(commission.amount),
            "order_number": commission.order.order_number,
            "order_total": str(commission.order.total_amount),
            "commission_rate": str(commission.program.commission_value),
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Add balance summary
        balance = commission.affiliate.get_balance_summary()
        context["outstanding_balance"] = str(balance["outstanding_balance"])
        context["total_earned"] = str(balance["total_earned"])

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=commission.affiliate.user.email,
            template_type="affiliate_commission_earned",
            context=context,
            language=get_user_email_language(commission.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_commission_earned email to {commission.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(
                f"Queued affiliate_commission_earned email to {commission.affiliate.user.email}"
            )
            return True
        else:
            logger.error(
                f"Failed to send affiliate_commission_earned email: status={outbox.status}"
            )
            return False

    except Exception as e:
        logger.error(f"Error sending commission earned email: {e}", exc_info=True)
        return False


def send_commission_approved_email(commission):
    """
    Send email notification when commission is approved.

    Args:
        commission (Commission): The commission instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": commission.affiliate.user.get_full_name()
            or commission.affiliate.user.email,
            "commission_amount": str(commission.amount),
            "order_number": commission.order.order_number,
            "approved_date": commission.approved_at.strftime("%B %d, %Y")
            if commission.approved_at
            else timezone.now().strftime("%B %d, %Y"),
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Add balance summary
        balance = commission.affiliate.get_balance_summary()
        context["outstanding_balance"] = str(balance["outstanding_balance"])
        context["minimum_payout"] = str(commission.program.minimum_payout)

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=commission.affiliate.user.email,
            template_type="affiliate_commission_approved",
            context=context,
            language=get_user_email_language(commission.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_commission_approved email to {commission.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(
                f"Queued affiliate_commission_approved email to {commission.affiliate.user.email}"
            )
            return True
        else:
            logger.error(
                f"Failed to send affiliate_commission_approved email: status={outbox.status}"
            )
            return False

    except Exception as e:
        logger.error(f"Error sending commission approved email: {e}", exc_info=True)
        return False


def send_commission_rejected_email(commission):
    """
    Send email notification when commission is rejected.

    Args:
        commission (Commission): The commission instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": commission.affiliate.user.get_full_name()
            or commission.affiliate.user.email,
            "commission_amount": str(commission.amount),
            "order_number": commission.order.order_number,
            "rejection_reason": commission.notes or "No reason provided",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=commission.affiliate.user.email,
            template_type="affiliate_commission_rejected",
            context=context,
            language=get_user_email_language(commission.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_commission_rejected email to {commission.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(
                f"Queued affiliate_commission_rejected email to {commission.affiliate.user.email}"
            )
            return True
        else:
            logger.error(
                f"Failed to send affiliate_commission_rejected email: status={outbox.status}"
            )
            return False

    except Exception as e:
        logger.error(f"Error sending commission rejected email: {e}", exc_info=True)
        return False


def send_commission_reversed_email(commission):
    """
    Send email notification when commission is reversed on refund.

    Args:
        commission (Commission): The commission instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": commission.affiliate.user.get_full_name()
            or commission.affiliate.user.email,
            "commission_amount": str(commission.amount),
            "order_number": commission.order.order_number,
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=commission.affiliate.user.email,
            template_type="affiliate_commission_reversed",
            context=context,
            language=get_user_email_language(commission.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_commission_reversed email to {commission.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(
                f"Queued affiliate_commission_reversed email to {commission.affiliate.user.email}"
            )
            return True
        else:
            logger.error(
                f"Failed to send affiliate_commission_reversed email: status={outbox.status}"
            )
            return False

    except Exception as e:
        logger.error(f"Error sending commission reversed email: {e}", exc_info=True)
        return False


# ============================================================================
# PAYOUT EMAILS
# ============================================================================


def send_payout_processing_email(payout):
    """
    Send email notification when payout starts processing.

    Args:
        payout (Payout): The payout instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": payout.affiliate.user.get_full_name() or payout.affiliate.user.email,
            "payout_amount": str(payout.amount),
            "payout_method": payout.get_method_display()
            if hasattr(payout, "get_method_display")
            else payout.method,
            "payout_id": str(payout.id),
            "payment_details": payout.affiliate.payment_email,
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=payout.affiliate.user.email,
            template_type="affiliate_payout_processing",
            context=context,
            language=get_user_email_language(payout.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_payout_processing email to {payout.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(
                f"Queued affiliate_payout_processing email to {payout.affiliate.user.email}"
            )
            return True
        else:
            logger.error(
                f"Failed to send affiliate_payout_processing email: status={outbox.status}"
            )
            return False

    except Exception as e:
        logger.error(f"Error sending payout processing email: {e}", exc_info=True)
        return False


def send_payout_completed_email(payout):
    """
    Send email notification when payout is completed.

    Args:
        payout (Payout): The payout instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": payout.affiliate.user.get_full_name() or payout.affiliate.user.email,
            "payout_amount": str(payout.amount),
            "payout_method": payout.get_method_display()
            if hasattr(payout, "get_method_display")
            else payout.method,
            "payout_id": str(payout.id),
            "payment_details": payout.affiliate.payment_email,
            "reference_number": payout.reference or payout.provider_reference or "N/A",
            "completed_date": payout.completed_at.strftime("%B %d, %Y")
            if payout.completed_at
            else timezone.now().strftime("%B %d, %Y"),
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Add balance summary
        balance = payout.affiliate.get_balance_summary()
        context["outstanding_balance"] = str(balance["outstanding_balance"])

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=payout.affiliate.user.email,
            template_type="affiliate_payout_completed",
            context=context,
            language=get_user_email_language(payout.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_payout_completed email to {payout.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued affiliate_payout_completed email to {payout.affiliate.user.email}")
            return True
        else:
            logger.error(f"Failed to send affiliate_payout_completed email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending payout completed email: {e}", exc_info=True)
        return False


def send_payout_failed_email(payout):
    """
    Send email notification when payout fails.

    Args:
        payout (Payout): The payout instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": payout.affiliate.user.get_full_name() or payout.affiliate.user.email,
            "payout_amount": str(payout.amount),
            "payout_method": payout.get_method_display()
            if hasattr(payout, "get_method_display")
            else payout.method,
            "payout_id": str(payout.id),
            "failure_reason": payout.notes or "Payment processor error",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=payout.affiliate.user.email,
            template_type="affiliate_payout_failed",
            context=context,
            language=get_user_email_language(payout.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_payout_failed email to {payout.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued affiliate_payout_failed email to {payout.affiliate.user.email}")
            return True
        else:
            logger.error(f"Failed to send affiliate_payout_failed email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending payout failed email: {e}", exc_info=True)
        return False


def send_payout_cancelled_email(payout):
    """
    Send email notification when payout is cancelled.

    Args:
        payout (Payout): The payout instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from email_system.services.email_sender import EmailSendingService

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "affiliate_name": payout.affiliate.user.get_full_name() or payout.affiliate.user.email,
            "payout_amount": str(payout.amount),
            "payout_id": str(payout.id),
            "cancellation_reason": payout.notes or "Cancelled by merchant",
            "portal_url": f"https://{site.domain}/affiliate/dashboard/",
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        outbox = EmailSendingService.send_template_email(
            to_email=payout.affiliate.user.email,
            template_type="affiliate_payout_cancelled",
            context=context,
            language=get_user_email_language(payout.affiliate.user),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped affiliate_payout_cancelled email to {payout.affiliate.user.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued affiliate_payout_cancelled email to {payout.affiliate.user.email}")
            return True
        else:
            logger.error(f"Failed to send affiliate_payout_cancelled email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending payout cancelled email: {e}", exc_info=True)
        return False
