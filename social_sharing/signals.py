"""
Social Sharing Signals

Handles automatic updates to aggregated ShareCount when shares are created/deleted.
Also integrates with loyalty badge system for awarding share-based badges.
"""

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F

from social_sharing.models import SocialShare, ShareCount

logger = logging.getLogger(__name__)


@receiver(post_save, sender=SocialShare)
def update_share_count_on_create(sender, instance, created, **kwargs):
    """
    Update aggregated share count when a share is created.

    Creates or increments ShareCount for the specific content + platform combination.
    """
    if not created:
        return  # Only process new shares

    try:
        # Get or create the ShareCount record
        share_count, created = ShareCount.objects.get_or_create(
            content_type=instance.content_type,
            object_id=instance.object_id,
            platform=instance.platform,
            defaults={'count': 0}
        )

        # Increment the count using F() expression for database-level increment
        # This avoids race conditions
        ShareCount.objects.filter(pk=share_count.pk).update(count=F('count') + 1)

        logger.debug(
            f"Incremented {instance.platform} share count for "
            f"{instance.content_type} #{instance.object_id}"
        )

    except Exception as e:
        logger.error(f"Error updating share count: {e}", exc_info=True)


@receiver(post_delete, sender=SocialShare)
def update_share_count_on_delete(sender, instance, **kwargs):
    """
    Update aggregated share count when a share is deleted.

    Decrements ShareCount for the specific content + platform combination.
    """
    try:
        # Find the ShareCount record
        share_count = ShareCount.objects.filter(
            content_type=instance.content_type,
            object_id=instance.object_id,
            platform=instance.platform
        ).first()

        if share_count:
            if share_count.count > 1:
                # Decrement the count
                ShareCount.objects.filter(pk=share_count.pk).update(count=F('count') - 1)
            else:
                # If count would be 0, delete the record
                share_count.delete()

            logger.debug(
                f"Decremented {instance.platform} share count for "
                f"{instance.content_type} #{instance.object_id}"
            )

    except Exception as e:
        logger.error(f"Error updating share count on delete: {e}", exc_info=True)


@receiver(post_save, sender=SocialShare)
def check_loyalty_badges(sender, instance, created, **kwargs):
    """
    Check and award loyalty badges when users share content.

    Integrates with the loyalty app's badge system to award badges
    based on share milestones (e.g., 5, 20, 50 shares).
    """
    if not created:
        return  # Only process new shares

    # Only check badges for logged-in users
    if not instance.user:
        logger.debug("Share by anonymous user, skipping badge check")
        return

    try:
        # Import here to avoid circular imports
        from loyalty.models import LoyaltyMember
        from loyalty.services.badge_awarding_service import BadgeAwardingService

        # Get the user's loyalty member record
        try:
            member = LoyaltyMember.objects.get(customer=instance.user, is_active=True)
        except LoyaltyMember.DoesNotExist:
            logger.debug(f"User {instance.user.id} is not a loyalty member, skipping badge check")
            return

        # Check and award social share badges
        badge_service = BadgeAwardingService()
        newly_awarded = badge_service.check_and_award_badges(
            member,
            criteria_types=['social_share']
        )

        if newly_awarded:
            logger.info(
                f"Awarded {len(newly_awarded)} social share badge(s) to member {member.id} "
                f"after sharing on {instance.platform}"
            )

    except ImportError:
        logger.debug("Loyalty app not available, skipping badge check")
    except Exception as e:
        logger.error(f"Error checking loyalty badges for share: {e}", exc_info=True)
