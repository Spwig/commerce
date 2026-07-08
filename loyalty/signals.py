"""
Loyalty Program Signal Handlers

Listens to order and user events to automatically award loyalty points.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import logging

from orders.models import Order
from loyalty.models import LoyaltyMember
from loyalty.services.points_engine import points_engine
from loyalty.services.badge_awarding_service import BadgeAwardingService

User = get_user_model()
logger = logging.getLogger(__name__)
badge_service = BadgeAwardingService()


@receiver(post_save, sender=Order)
def award_points_on_order(sender, instance, created, **kwargs):
    """
    Award loyalty points when an order is placed or updated.

    Points are awarded when:
    - Order status changes to 'processing' or 'delivered'
    - Order is not cancelled or refunded
    """
    order = instance

    # Only award points for certain statuses
    if order.status not in ['processing', 'delivered']:
        logger.debug(f"Order {order.order_number} status is {order.status}, not awarding points")
        return

    # Guest orders have no user - skip loyalty points
    if not order.user:
        logger.debug(f"Order {order.order_number} is a guest order, not awarding points")
        return

    # Check if customer is a loyalty member
    try:
        member = LoyaltyMember.objects.get(customer=order.user, is_active=True)
    except LoyaltyMember.DoesNotExist:
        logger.debug(f"User {order.user.id} is not a loyalty member")
        return

    # Check if points already awarded for this order
    from loyalty.models import LoyaltyTransaction
    existing = LoyaltyTransaction.objects.filter(
        member=member,
        related_object_type='order',
        related_object_id=str(order.id),
        transaction_type=LoyaltyTransaction.TYPE_EARN,
    ).exists()

    if existing:
        logger.debug(f"Points already awarded for order {order.order_number}")
        return

    # Award points
    try:
        transaction = points_engine.award_order_points(order, member)
        if transaction:
            logger.info(f"Awarded {transaction.points} points for order {order.order_number}")
        else:
            logger.info(f"No points awarded for order {order.order_number}")
    except Exception as e:
        logger.error(f"Error awarding points for order {order.order_number}: {e}", exc_info=True)

    # Check and award eligible badges
    try:
        criteria_to_check = [
            'first_purchase', 'order_count', 'total_spend',
            'early_morning_orders', 'late_night_orders', 'weekend_orders',
            'quick_return', 'single_order_value', 'items_per_order', 'orders_per_month'
        ]
        newly_awarded = badge_service.check_and_award_badges(member, criteria_to_check)
        if newly_awarded:
            logger.info(f"Auto-awarded {len(newly_awarded)} badges to member {member.id} after order")
    except Exception as e:
        logger.error(f"Error checking badges for order {order.order_number}: {e}", exc_info=True)


@receiver(pre_save, sender=Order)
def revoke_points_on_cancellation(sender, instance, **kwargs):
    """
    Revoke loyalty points when an order is cancelled or refunded.
    """
    if not instance.pk:
        return  # New order, nothing to revoke

    try:
        old_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    # Check if status changed to cancelled or refunded
    if old_order.status == instance.status:
        return  # Status didn't change

    if instance.status not in ['cancelled', 'refunded']:
        return  # Not a cancellation/refund

    # Check if customer is a loyalty member
    try:
        member = LoyaltyMember.objects.get(customer=instance.user, is_active=True)
    except LoyaltyMember.DoesNotExist:
        return

    # Find original earn transaction
    from loyalty.models import LoyaltyTransaction
    original_txn = LoyaltyTransaction.objects.filter(
        member=member,
        related_object_type='order',
        related_object_id=str(instance.id),
        transaction_type=LoyaltyTransaction.TYPE_EARN,
    ).first()

    if not original_txn:
        logger.debug(f"No points transaction found for order {instance.order_number}")
        return

    # Check if already revoked
    existing_revoke = LoyaltyTransaction.objects.filter(
        reversal_of=original_txn,
    ).exists()

    if existing_revoke:
        logger.debug(f"Points already revoked for order {instance.order_number}")
        return

    # Create reversal transaction
    try:
        from loyalty.services.ledger_service import ledger_service
        ledger_service.create_reversal(
            original_transaction=original_txn,
            reason=f"Order {instance.order_number} {instance.status}",
            admin_user=None,
        )
        logger.info(f"Revoked {original_txn.points} points for order {instance.order_number}")
    except Exception as e:
        logger.error(f"Error revoking points for order {instance.order_number}: {e}", exc_info=True)


@receiver(post_save, sender=User)
def create_loyalty_member_on_signup(sender, instance, created, **kwargs):
    """
    Automatically enroll new users in loyalty program and award signup bonus.
    """
    if not created:
        return  # Only for new users

    user = instance

    # Skip staff/superuser accounts
    if user.is_staff or user.is_superuser:
        return

    # Create loyalty member
    try:
        member, member_created = LoyaltyMember.objects.get_or_create(
            customer=user,
            defaults={'is_active': True}
        )

        if member_created:
            logger.info(f"Created loyalty member for user {user.id}")

            # Award signup bonus
            try:
                transaction = points_engine.award_action_points(
                    member=member,
                    action_type='signup',
                    metadata={
                        'description': 'Welcome to our loyalty program!',
                        'object_type': 'user',
                        'object_id': str(user.id),
                    }
                )
                if transaction:
                    logger.info(f"Awarded signup bonus of {transaction.points} points to user {user.id}")
            except Exception as e:
                logger.error(f"Error awarding signup bonus for user {user.id}: {e}", exc_info=True)

            # Check and award program join badges
            try:
                newly_awarded = badge_service.check_and_award_badges(member, ['program_join'])
                if newly_awarded:
                    logger.info(f"Auto-awarded {len(newly_awarded)} signup badges to member {member.id}")
            except Exception as e:
                logger.error(f"Error checking badges for new member {member.id}: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Error creating loyalty member for user {user.id}: {e}", exc_info=True)


# ============================================================================
# CAMPAIGN TRIGGER HANDLERS
# ============================================================================


@receiver(post_save, sender=Order)
def trigger_campaigns_on_order(sender, instance, created, **kwargs):
    """
    Trigger campaigns when order events occur.

    Events:
    - order_placed: When order is created
    - order_refunded: When order is refunded
    - order_cancelled: When order is cancelled
    """
    from loyalty.services.campaign_orchestrator import CampaignOrchestrator
    from loyalty.models import LoyaltyCampaign

    order = instance

    # Guest orders have no user - skip campaign triggers
    if not order.user:
        logger.debug(f"Order {order.order_number} is a guest order, skipping campaigns")
        return

    # Get loyalty member
    try:
        member = LoyaltyMember.objects.select_related('customer', 'balance', 'current_tier').get(
            customer=order.user,
            is_active=True
        )
    except LoyaltyMember.DoesNotExist:
        logger.debug(f"User {order.user.id} is not a loyalty member")
        return

    orchestrator = CampaignOrchestrator()

    # Build context
    context = {
        'order_id': order.id,
        'order_number': order.order_number,
        'order_total': float(order.total_amount.amount),
        'order_count': Order.objects.filter(user=order.user, status='completed').count(),
    }

    # Add order items context
    try:
        items = order.items.select_related('product', 'product__category')
        context['product_ids'] = list(items.values_list('product_id', flat=True))
        context['category_ids'] = list(
            items.filter(product__category__isnull=False).values_list('product__category_id', flat=True).distinct()
        )
    except Exception as e:
        logger.warning(f"Could not extract order items data: {e}")

    # Determine event based on order status
    if created:
        # New order - trigger order_placed
        event = LoyaltyCampaign.EVENT_ORDER_PLACED
        logger.debug(f"Triggering order_placed campaigns for order {order.order_number}")
    elif instance.status == 'refunded':
        # Order refunded
        event = LoyaltyCampaign.EVENT_ORDER_REFUNDED
        logger.debug(f"Triggering order_refunded campaigns for order {order.order_number}")
    elif instance.status == 'cancelled':
        # Order cancelled
        event = LoyaltyCampaign.EVENT_ORDER_CANCELLED
        logger.debug(f"Triggering order_cancelled campaigns for order {order.order_number}")
    else:
        # Status change but not a trigger event
        return

    # Trigger campaigns
    try:
        result = orchestrator.trigger_event(event, member, context)
        logger.info(f"Triggered {result['triggered']} campaigns for event '{event}' on order {order.order_number}")
    except Exception as e:
        logger.error(f"Error triggering campaigns for order {order.order_number}: {e}", exc_info=True)


@receiver(post_save, sender=User)
def trigger_campaigns_on_signup(sender, instance, created, **kwargs):
    """
    Trigger customer_signup campaigns when new user is created.
    """
    if not created:
        return

    from loyalty.services.campaign_orchestrator import CampaignOrchestrator
    from loyalty.models import LoyaltyCampaign

    user = instance

    # Skip staff/superuser accounts
    if user.is_staff or user.is_superuser:
        return

    # Get loyalty member (should be created by create_loyalty_member_on_signup)
    try:
        member = LoyaltyMember.objects.select_related('customer', 'balance').get(
            customer=user,
            is_active=True
        )
    except LoyaltyMember.DoesNotExist:
        logger.debug(f"User {user.id} is not yet a loyalty member")
        return

    orchestrator = CampaignOrchestrator()

    context = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
    }

    try:
        result = orchestrator.trigger_event(LoyaltyCampaign.EVENT_CUSTOMER_SIGNUP, member, context)
        logger.info(f"Triggered {result['triggered']} customer_signup campaigns for user {user.id}")
    except Exception as e:
        logger.error(f"Error triggering signup campaigns for user {user.id}: {e}", exc_info=True)


@receiver(post_save, sender='loyalty.LoyaltyMember')
def trigger_campaigns_on_tier_change(sender, instance, created, **kwargs):
    """
    Trigger tier promotion/demotion campaigns when member's tier changes.
    """
    if created:
        return  # New member, not a tier change

    from loyalty.services.campaign_orchestrator import CampaignOrchestrator
    from loyalty.models import LoyaltyCampaign

    member = instance

    # Check if tier actually changed
    if not hasattr(member, '_old_tier_id'):
        # Store current tier for next save
        try:
            current_member = LoyaltyMember.objects.get(pk=member.pk)
            member._old_tier_id = current_member.current_tier_id
        except LoyaltyMember.DoesNotExist:
            pass
        return

    old_tier_id = getattr(member, '_old_tier_id', None)
    new_tier_id = member.current_tier_id

    if old_tier_id == new_tier_id:
        return  # Tier didn't change

    # Determine if promotion or demotion
    from loyalty.models import LoyaltyTier

    try:
        old_tier = LoyaltyTier.objects.get(id=old_tier_id) if old_tier_id else None
        new_tier = member.current_tier

        # Lower rank = higher tier
        if old_tier and new_tier:
            if new_tier.rank < old_tier.rank:
                event = LoyaltyCampaign.EVENT_TIER_PROMOTED
            else:
                event = LoyaltyCampaign.EVENT_TIER_DEMOTED
        elif new_tier and not old_tier:
            event = LoyaltyCampaign.EVENT_TIER_PROMOTED
        else:
            return  # No tier to no tier, or new tier removed

        orchestrator = CampaignOrchestrator()

        context = {
            'old_tier_id': old_tier_id,
            'old_tier_name': old_tier.name if old_tier else None,
            'new_tier_id': new_tier_id,
            'new_tier_name': new_tier.name if new_tier else None,
        }

        result = orchestrator.trigger_event(event, member, context)
        logger.info(f"Triggered {result['triggered']} {event} campaigns for member {member.id}")

    except Exception as e:
        logger.error(f"Error triggering tier change campaigns for member {member.id}: {e}", exc_info=True)


# Store tier ID before save for tier change detection
@receiver(pre_save, sender='loyalty.LoyaltyMember')
def store_previous_tier(sender, instance, **kwargs):
    """Store previous tier ID for comparison after save"""
    if instance.pk:
        try:
            old_member = LoyaltyMember.objects.get(pk=instance.pk)
            instance._old_tier_id = old_member.current_tier_id
        except LoyaltyMember.DoesNotExist:
            pass


# ============================================================================
# BADGE AWARDING TRIGGERS
# ============================================================================


@receiver(post_save, sender='catalog.ProductReview')
def check_review_badges(sender, instance, created, **kwargs):
    """
    Check and award review-based badges when a review is created or approved.
    """
    review = instance

    # Only check when review is approved
    if not review.is_approved:
        return

    # Get loyalty member
    try:
        member = LoyaltyMember.objects.get(customer=review.user, is_active=True)
    except LoyaltyMember.DoesNotExist:
        logger.debug(f"User {review.user.id} is not a loyalty member")
        return

    # Check and award eligible review badges
    try:
        criteria_to_check = ['review_count']
        newly_awarded = badge_service.check_and_award_badges(member, criteria_to_check)
        if newly_awarded:
            logger.info(f"Auto-awarded {len(newly_awarded)} review badges to member {member.id}")
    except Exception as e:
        logger.error(f"Error checking review badges for member {member.id}: {e}", exc_info=True)


@receiver(post_save, sender='cart.WishlistItem')
def check_wishlist_badges(sender, instance, created, **kwargs):
    """
    Check and award wishlist-based badges when items are added to wishlist.
    """
    wishlist_item = instance

    # Only check on creation
    if not created:
        return

    # Get user from wishlist
    user = wishlist_item.wishlist.user

    # Get loyalty member
    try:
        member = LoyaltyMember.objects.get(customer=user, is_active=True)
    except LoyaltyMember.DoesNotExist:
        logger.debug(f"User {user.id} is not a loyalty member")
        return

    # Check and award eligible wishlist badges
    try:
        criteria_to_check = ['wishlist_items']
        newly_awarded = badge_service.check_and_award_badges(member, criteria_to_check)
        if newly_awarded:
            logger.info(f"Auto-awarded {len(newly_awarded)} wishlist badges to member {member.id}")
    except Exception as e:
        logger.error(f"Error checking wishlist badges for member {member.id}: {e}", exc_info=True)
