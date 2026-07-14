"""
Campaign Action Executor Service

Executes individual campaign actions (award points, send email, issue rewards, etc.).
Integrates with existing loyalty services for action processing.
"""

import logging

from django.db import transaction
from django.utils import timezone

from email_system.utils.language import get_user_email_language
from loyalty.models import LoyaltyBadge, LoyaltyMember, LoyaltyReward

logger = logging.getLogger(__name__)


class CampaignActionExecutor:
    """
    Executes campaign actions.

    Supported actions:
    - award_points: Award bonus points
    - send_email: Send email template
    - issue_reward: Issue a reward redemption
    - award_badge: Award a badge
    - move_segment: Move member to different segment
    """

    def execute_action(self, action: dict, member: LoyaltyMember, context: dict) -> dict:
        """
        Execute a single campaign action.

        Args:
            action: Action configuration dict
            member: LoyaltyMember instance
            context: Execution context

        Returns:
            dict: Action result with success flag and details
        """
        action_type = action.get("type")

        if not action_type:
            logger.error("Action missing 'type' field")
            return {"success": False, "error": "Missing action type"}

        logger.info(f"Executing action '{action_type}' for member {member.id}")

        # Route to appropriate handler
        handlers = {
            "award_points": self._award_points,
            "send_email": self._send_email,
            "issue_reward": self._issue_reward,
            "award_badge": self._award_badge,
            "move_segment": self._move_segment,
        }

        handler = handlers.get(action_type)
        if not handler:
            logger.error(f"Unknown action type: {action_type}")
            return {"success": False, "error": f"Unknown action type: {action_type}"}

        try:
            result = handler(action, member, context)
            logger.info(f"Action '{action_type}' completed successfully")
            return result
        except Exception as e:
            logger.error(f"Action '{action_type}' failed: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e)}

    @transaction.atomic
    def _award_points(self, action: dict, member: LoyaltyMember, context: dict) -> dict:
        """
        Award bonus points to member.

        Action config:
            {
                "type": "award_points",
                "points": 500,
                "reason": "Birthday bonus"
            }

        Args:
            action: Action configuration
            member: LoyaltyMember instance
            context: Execution context

        Returns:
            dict: Result with transaction_id
        """
        from loyalty.models import LoyaltyTransaction
        from loyalty.services.tiering_service import TieringService

        points = action.get("points", 0)
        reason = action.get("reason", "Campaign bonus")

        if points <= 0:
            return {"success": False, "error": "Points must be positive"}

        # Create bonus transaction directly
        campaign_name = context.get("campaign_name", "Campaign")
        description = f"Earned {points} points from {campaign_name}"
        if reason:
            description += f" - {reason}"

        txn = LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_BONUS,
            points=points,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description=description,
            reason=reason,
            related_object_type="campaign",
            related_object_id=str(context.get("campaign_id", "")),
        )

        # Update balance
        balance = member.balance
        balance.available_points += points
        balance.lifetime_earned += points
        balance.save(update_fields=["available_points", "lifetime_earned"])

        # Evaluate tier eligibility after points change
        tiering_service = TieringService()
        tier_result = tiering_service.evaluate_and_update_tier(
            member, trigger_event=f"campaign_points_awarded:{campaign_name}"
        )

        if tier_result["changed"]:
            logger.info(
                f"Member {member.id} tier {tier_result['action']}: "
                f"{tier_result['new_tier'].name if tier_result['new_tier'] else 'No Tier'}"
            )

        logger.info(f"Awarded {points} campaign bonus points to member {member.id}")

        return {
            "success": True,
            "action": "award_points",
            "points": points,
            "transaction_id": txn.id,
            "new_balance": member.balance.available_points,
        }

    def _send_email(self, action: dict, member: LoyaltyMember, context: dict) -> dict:
        """
        Send email template to member.

        Action config:
            {
                "type": "send_email",
                "template": "loyalty_birthday_campaign",
                "delay_hours": 0
            }

        Args:
            action: Action configuration
            member: LoyaltyMember instance
            context: Execution context

        Returns:
            dict: Result with outbox_id
        """
        from email_system.services.email_sender import EmailSendingService

        template_type = action.get("template")
        action.get("delay_hours", 0)

        if not template_type:
            return {"success": False, "error": "Missing email template"}

        # Build email context
        email_context = {
            **context,
            "customer_name": member.customer.get_full_name() or member.customer.username,
            "customer_first_name": member.customer.first_name,
            "points_balance": member.balance.available_points,
            "tier_name": member.current_tier.name if member.current_tier else "Member",
            "member_id": member.id,
            "dashboard_url": "/loyalty/account/dashboard/",
        }

        # Add action-specific context
        if action.get("points"):
            email_context["points_awarded"] = action["points"]
        if action.get("reward_id"):
            email_context["reward_id"] = action["reward_id"]

        # Send email
        try:
            outbox = EmailSendingService.send_template_email(
                to_email=member.customer.email,
                template_type=template_type,
                context=email_context,
                language=get_user_email_language(member.customer),
                enable_tracking=True,
            )

            return {
                "success": True,
                "action": "send_email",
                "template": template_type,
                "outbox_id": str(outbox.id),
                "recipient": member.customer.email,
            }
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return {"success": False, "error": f"Email sending failed: {str(e)}"}

    @transaction.atomic
    def _issue_reward(self, action: dict, member: LoyaltyMember, context: dict) -> dict:
        """
        Issue a reward to member (automatic redemption).

        Action config:
            {
                "type": "issue_reward",
                "reward_id": 123
            }

        Args:
            action: Action configuration
            member: LoyaltyMember instance
            context: Execution context

        Returns:
            dict: Result with redemption details
        """
        from loyalty.services.redemption_engine import RedemptionEngine

        reward_id = action.get("reward_id")
        if not reward_id:
            return {"success": False, "error": "Missing reward_id"}

        try:
            reward = LoyaltyReward.objects.get(id=reward_id, is_active=True)
        except LoyaltyReward.DoesNotExist:
            return {"success": False, "error": f"Reward {reward_id} not found"}

        engine = RedemptionEngine()

        try:
            redemption = engine.redeem_reward(
                member=member,
                reward=reward,
                notes=f"Campaign reward: {context.get('campaign_name', 'Unknown')}",
            )

            # Auto-confirm campaign rewards
            engine.confirm_redemption(redemption)

            return {
                "success": True,
                "action": "issue_reward",
                "reward_id": reward.id,
                "reward_name": reward.name,
                "redemption_id": redemption.id,
                "redemption_code": redemption.redemption_code,
            }
        except Exception as e:
            logger.error(f"Failed to issue reward: {str(e)}")
            return {"success": False, "error": f"Reward issuance failed: {str(e)}"}

    @transaction.atomic
    def _award_badge(self, action: dict, member: LoyaltyMember, context: dict) -> dict:
        """
        Award a badge to member.

        Action config:
            {
                "type": "award_badge",
                "badge_id": 456,
                "bonus_points": 100
            }

        Args:
            action: Action configuration
            member: LoyaltyMember instance
            context: Execution context

        Returns:
            dict: Result with badge details
        """
        from loyalty.models import LoyaltyMemberBadge

        badge_id = action.get("badge_id")
        bonus_points = action.get("bonus_points", 0)

        if not badge_id:
            return {"success": False, "error": "Missing badge_id"}

        try:
            badge = LoyaltyBadge.objects.get(id=badge_id, is_active=True)
        except LoyaltyBadge.DoesNotExist:
            return {"success": False, "error": f"Badge {badge_id} not found"}

        # Check if member already has this badge
        if LoyaltyMemberBadge.objects.filter(member=member, badge=badge).exists():
            return {"success": False, "error": "Member already has this badge"}

        # Award badge
        member_badge = LoyaltyMemberBadge.objects.create(
            member=member, badge=badge, earned_at=timezone.now()
        )

        # Award bonus points if specified
        points_transaction_id = None
        if bonus_points > 0:
            from loyalty.services.points_engine import PointsEngine

            engine = PointsEngine()
            transaction = engine.award_bonus_points(
                member=member,
                points=bonus_points,
                reason=f"Badge earned: {badge.name}",
                related_object_type="badge",
                related_object_id=str(badge.id),
            )
            points_transaction_id = transaction.id

        return {
            "success": True,
            "action": "award_badge",
            "badge_id": badge.id,
            "badge_name": badge.name,
            "member_badge_id": member_badge.id,
            "bonus_points": bonus_points,
            "points_transaction_id": points_transaction_id,
        }

    @transaction.atomic
    def _move_segment(self, action: dict, member: LoyaltyMember, context: dict) -> dict:
        """
        Move member to a different segment.

        Action config:
            {
                "type": "move_segment",
                "segment_id": 789,
                "remove_from_others": true
            }

        Args:
            action: Action configuration
            member: LoyaltyMember instance
            context: Execution context

        Returns:
            dict: Result with segment details
        """
        from loyalty.models import LoyaltySegment, LoyaltySegmentMembership

        segment_id = action.get("segment_id")
        remove_from_others = action.get("remove_from_others", False)

        if not segment_id:
            return {"success": False, "error": "Missing segment_id"}

        try:
            segment = LoyaltySegment.objects.get(id=segment_id, is_active=True)
        except LoyaltySegment.DoesNotExist:
            return {"success": False, "error": f"Segment {segment_id} not found"}

        # Only applicable for manual segments
        if segment.criteria_type != LoyaltySegment.TYPE_MANUAL:
            return {"success": False, "error": "Can only move to manual segments"}

        # Remove from other segments if specified
        if remove_from_others:
            removed_count = (
                LoyaltySegmentMembership.objects.filter(member=member)
                .exclude(segment=segment)
                .delete()[0]
            )
            logger.info(f"Removed member {member.id} from {removed_count} segments")

        # Add to target segment (if not already)
        membership, created = LoyaltySegmentMembership.objects.get_or_create(
            segment=segment,
            member=member,
            defaults={"assigned_by": None},  # Automated assignment
        )

        if created:
            # Update segment member count
            segment.member_count = segment.memberships.count()
            segment.save(update_fields=["member_count"])

        return {
            "success": True,
            "action": "move_segment",
            "segment_id": segment.id,
            "segment_name": segment.name,
            "membership_created": created,
        }
