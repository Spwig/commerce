"""
Referral Email Notification Service

Handles sending email notifications for referral program events.
"""

import logging

from django.contrib.sites.models import Site

from email_system.utils.language import get_user_email_language

logger = logging.getLogger(__name__)


def send_referral_reward_email(reward, recipient_type):
    """
    Send email notification when a referral reward is issued.

    Args:
        reward (ReferralReward): The reward instance
        recipient_type (str): 'referrer' or 'referee'

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from ..models import ReferralProgram

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Get program
        ReferralProgram.get_program()

        # Determine template type
        if recipient_type == "referrer":
            template_type = "referral_reward_issued_referrer"
        elif recipient_type == "referee":
            template_type = "referral_reward_issued_referee"
        else:
            logger.error(f"Invalid recipient_type: {recipient_type}")
            return False

        # Build context
        context = {
            "customer_name": reward.customer.get_full_name() or reward.customer.email,
            "reward_amount": str(reward.amount),
            "reward_type_display": reward.get_kind_display(),
            "expires_at": reward.expires_at.strftime("%B %d, %Y") if reward.expires_at else None,
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
            "shop_url": f"https://{site.domain}",
        }

        # Add attribution details if available
        if reward.attribution:
            if recipient_type == "referrer":
                # Email to referrer - show referee name
                context["referee_name"] = (
                    reward.attribution.referee_customer.get_full_name()
                    or reward.attribution.referee_customer.email
                )
                # Add referral stats
                if reward.referrer_identity:
                    context["total_referrals"] = reward.referrer_identity.total_conversions
                    context["total_rewards_earned"] = str(
                        reward.referrer_identity.total_rewards_earned
                    )
                    context["referral_link"] = reward.referrer_identity.get_referral_link()
                    context["referral_dashboard_url"] = f"https://{site.domain}/account/referrals/"

            elif recipient_type == "referee":
                # Email to referee - show referrer name
                if reward.attribution.referrer_identity:
                    context["referrer_name"] = (
                        reward.attribution.referrer_identity.customer.get_full_name()
                        or reward.attribution.referrer_identity.customer.email
                    )
                    context["my_referral_link_url"] = f"https://{site.domain}/account/referrals/"

        # Send email using EmailSendingService (includes preference checking)
        from email_system.services.email_sender import EmailSendingService

        outbox = EmailSendingService.send_template_email(
            to_email=reward.customer.email,
            template_type=template_type,
            context=context,
            language=get_user_email_language(reward.customer),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped {template_type} email to {reward.customer.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued {template_type} email to {reward.customer.email}")
            return True
        else:
            logger.error(f"Failed to send {template_type} email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending referral reward email: {e}", exc_info=True)
        return False


def send_referral_successful_email(attribution):
    """
    Send email notification when a referral successfully signs up.

    Args:
        attribution (ReferralAttribution): The attribution instance

    Returns:
        bool: True if email sent successfully, False otherwise
    """

    try:
        # Only send if we have a referrer
        if not attribution.referrer_identity:
            return False

        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "customer_name": attribution.referrer_identity.customer.get_full_name()
            or attribution.referrer_identity.customer.email,
            "referee_name": attribution.referee_customer.get_full_name()
            or attribution.referee_customer.email,
            "referral_link": attribution.referrer_identity.get_referral_link(),
            "referral_dashboard_url": f"https://{site.domain}/account/referrals/",
            "shop_name": site.name,
        }

        # Send email using EmailSendingService (includes preference checking)
        from email_system.services.email_sender import EmailSendingService

        customer = attribution.referrer_identity.customer
        outbox = EmailSendingService.send_template_email(
            to_email=customer.email,
            template_type="referral_successful",
            context=context,
            language=get_user_email_language(customer),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped referral_successful email to {customer.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued referral_successful email to {customer.email}")
            return True
        else:
            logger.error(f"Failed to send referral_successful email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending referral successful email: {e}", exc_info=True)
        return False


def send_reward_expiring_email(reward, days_until_expiration):
    """
    Send email notification when a reward is about to expire.

    Args:
        reward (ReferralReward): The reward instance
        days_until_expiration (int): Days remaining until expiration

    Returns:
        bool: True if email sent successfully, False otherwise
    """

    try:
        # Get site
        site = Site.objects.get(pk=1)

        # Build context
        context = {
            "customer_name": reward.customer.get_full_name() or reward.customer.email,
            "reward_amount": str(reward.amount),
            "reward_type_display": reward.get_kind_display(),
            "days_until_expiration": days_until_expiration,
            "expiration_date": reward.expires_at.strftime("%B %d, %Y"),
            "shop_name": site.name,
            "shop_url": f"https://{site.domain}",
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking)
        from email_system.services.email_sender import EmailSendingService

        outbox = EmailSendingService.send_template_email(
            to_email=reward.customer.email,
            template_type="referral_reward_expiring",
            context=context,
            language=get_user_email_language(reward.customer),
        )

        # Check if email was sent or skipped
        if outbox.status == "skipped":
            logger.info(
                f"Skipped reward_expiring email to {reward.customer.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued reward_expiring email to {reward.customer.email}")
            return True
        else:
            logger.error(f"Failed to send reward_expiring email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending reward expiring email: {e}", exc_info=True)
        return False


def send_reward_expired_email(reward):
    """
    Send email notification when a referral reward has expired.

    Args:
        reward (ReferralReward): The expired reward

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        site = Site.objects.get(pk=1)

        context = {
            "customer_name": reward.customer.get_full_name() or reward.customer.email,
            "reward_amount": str(reward.amount),
            "reward_type_display": reward.get_kind_display(),
            "expired_at": reward.expires_at.strftime("%B %d, %Y") if reward.expires_at else None,
            "shop_name": site.name,
            "shop_url": f"https://{site.domain}",
            "support_email": "support@" + site.domain,
        }

        from email_system.services.email_sender import EmailSendingService

        outbox = EmailSendingService.send_template_email(
            to_email=reward.customer.email,
            template_type="referral_reward_expired",
            context=context,
            language=get_user_email_language(reward.customer),
        )

        if outbox.status == "skipped":
            logger.info(
                f"Skipped reward_expired email to {reward.customer.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued reward_expired email to {reward.customer.email}")
            return True
        else:
            logger.error(f"Failed to send reward_expired email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending reward expired email: {e}", exc_info=True)
        return False


def send_reward_revoked_email(reward, reason=""):
    """
    Send email notification when a referral reward has been revoked.

    Args:
        reward (ReferralReward): The revoked reward
        reason (str): Reason for revocation

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        site = Site.objects.get(pk=1)

        context = {
            "customer_name": reward.customer.get_full_name() or reward.customer.email,
            "reward_amount": str(reward.amount),
            "reward_type_display": reward.get_kind_display(),
            "revocation_reason": reason,
            "shop_name": site.name,
            "shop_url": f"https://{site.domain}",
            "support_email": "support@" + site.domain,
        }

        from email_system.services.email_sender import EmailSendingService

        outbox = EmailSendingService.send_template_email(
            to_email=reward.customer.email,
            template_type="referral_reward_revoked",
            context=context,
            language=get_user_email_language(reward.customer),
        )

        if outbox.status == "skipped":
            logger.info(
                f"Skipped reward_revoked email to {reward.customer.email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(f"Queued reward_revoked email to {reward.customer.email}")
            return True
        else:
            logger.error(f"Failed to send reward_revoked email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending reward revoked email: {e}", exc_info=True)
        return False


def send_referral_invitation_email(referrer, referee_email, personal_message=None):
    """
    Send personalized referral invitation email.

    Args:
        referrer (User): The user sending the invitation
        referee_email (str): Email address of the person being invited
        personal_message (str, optional): Personal message from referrer

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from ..models import ReferralIdentity, ReferralProgram

    try:
        # Get or create referral identity
        identity, created = ReferralIdentity.objects.get_or_create(customer=referrer)

        # Get site
        site = Site.objects.get(pk=1)

        # Get program to determine reward amount
        program = ReferralProgram.get_program()
        referee_reward = program.get_referee_reward()

        # Build context
        context = {
            "referrer_name": referrer.get_full_name() or referrer.email,
            "referral_link": identity.get_referral_link(),
            "reward_amount": str(referee_reward.get("amount", "10%")),
            "personal_message": personal_message,
            "shop_name": site.name,
            "support_email": "support@" + site.domain,
        }

        # Send email using EmailSendingService (includes preference checking for registered users)
        from email_system.services.email_sender import EmailSendingService

        outbox = EmailSendingService.send_template_email(
            to_email=referee_email,
            template_type="referral_invitation",
            context=context,
            language=get_user_email_language(referrer),
        )

        # Check if email was sent or skipped
        # Note: Referral invitations may go to non-registered users (guests)
        if outbox.status == "skipped":
            logger.info(
                f"Skipped referral_invitation email to {referee_email} - user preference disabled"
            )
            return False
        elif outbox.status in ["pending", "queued"]:
            logger.info(
                f"Queued referral_invitation email from {referrer.email} to {referee_email}"
            )
            return True
        else:
            logger.error(f"Failed to send referral_invitation email: status={outbox.status}")
            return False

    except Exception as e:
        logger.error(f"Error sending referral invitation email: {e}", exc_info=True)
        return False
