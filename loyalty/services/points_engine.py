"""
Points Engine Service

Calculates and awards loyalty points based on rules, orders, and actions.
Handles rule evaluation, point calculation, and transaction creation.
"""

import logging
from datetime import timedelta

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from loyalty.models import (
    LoyaltyBalance,
    LoyaltyMember,
    LoyaltyRule,
    LoyaltyTransaction,
)
from loyalty.services.tiering_service import TieringService

logger = logging.getLogger(__name__)


class PointsEngine:
    """
    Core engine for calculating and awarding loyalty points.

    Handles:
    - Rule evaluation with priority ordering
    - Points calculation based on order details
    - Transaction creation and balance updates
    - Cap enforcement (per order, per day, per member)
    """

    def calculate_order_points(self, order, member: LoyaltyMember) -> dict:
        """
        Calculate points for an order based on applicable rules.

        Args:
            order: Order model instance
            member: LoyaltyMember instance

        Returns:
            Dict with points breakdown and applicable rules
        """
        # Get active rules applicable to this member's tier
        rules = self._get_applicable_rules(member)

        if not rules:
            logger.info(f"No applicable rules for member {member.id}")
            return {"total_points": 0, "rules_applied": [], "message": "No applicable rules found"}

        total_points = 0
        rules_applied = []
        matched_rules = []

        # Evaluate rules by priority
        for rule in rules:
            points = self._evaluate_rule(rule, order, member)

            if points > 0:
                # Apply tier multiplier if member has a tier
                if member.current_tier:
                    points = int(points * float(member.current_tier.points_multiplier))

                total_points += points
                matched_rules.append(rule)
                rules_applied.append(
                    {
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "points": points,
                    }
                )

                # Stop if rule is exclusive
                if rule.is_exclusive:
                    logger.info(f"Exclusive rule {rule.id} matched, stopping evaluation")
                    break

        # Apply per-order caps — only from rules that actually produced points, so
        # an unrelated rule's low cap can't clip a valid award.
        for rule in matched_rules:
            if rule.max_points_per_order and total_points > rule.max_points_per_order:
                logger.info(f"Capping points from {total_points} to {rule.max_points_per_order}")
                total_points = rule.max_points_per_order
                break

        return {
            "total_points": total_points,
            "rules_applied": rules_applied,
            "matched_rules": matched_rules,
            "message": f"Calculated {total_points} points from {len(rules_applied)} rule(s)",
        }

    def award_order_points(
        self, order, member: LoyaltyMember, admin_user=None
    ) -> LoyaltyTransaction | None:
        """
        Award points for an order and create transaction.

        Args:
            order: Order model instance
            member: LoyaltyMember instance
            admin_user: Optional admin user for audit

        Returns:
            LoyaltyTransaction instance or None if no points awarded
        """
        # Calculate points
        result = self.calculate_order_points(order, member)
        points = result["total_points"]

        if points <= 0:
            logger.info(f"No points to award for order {order.order_number}")
            return None

        # Check caps against only the rules that produced this award
        matched_rules = result["matched_rules"]

        # Check per-day cap
        if not self._check_daily_cap(member, points, matched_rules):
            logger.warning(f"Daily cap reached for member {member.id}")
            return None

        # Check per-member cap
        if not self._check_member_cap(member, points, matched_rules):
            logger.warning(f"Member cap reached for member {member.id}")
            return None

        # Determine if points should be pending
        rules_applied = result["rules_applied"]
        pending_days = 0
        expires_days = None

        if rules_applied:
            # Use the first rule's settings
            first_rule = LoyaltyRule.objects.get(id=rules_applied[0]["rule_id"])
            pending_days = first_rule.points_pending_days
            expires_days = first_rule.points_expire_days

        # Calculate expiration date
        expires_at = None
        if expires_days:
            expires_at = timezone.now() + timedelta(days=expires_days)

        # Determine status
        status = (
            LoyaltyTransaction.STATUS_PENDING
            if pending_days > 0
            else LoyaltyTransaction.STATUS_AVAILABLE
        )

        # Create transaction
        description = f"Earned {points} points from order #{order.order_number}"
        if len(rules_applied) > 0:
            rule_names = ", ".join([r["rule_name"] for r in rules_applied])
            description += f" ({rule_names})"

        with transaction.atomic():
            # Create transaction
            txn = LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_EARN,
                points=points,
                status=status,
                description=description,
                reason=f"Order #{order.order_number}",
                related_object_type="order",
                related_object_id=str(order.id),
                expires_at=expires_at,
                created_by=admin_user,
            )

            # Update balance
            self._update_balance(member, txn)

            # Evaluate tier eligibility after points change
            tiering_service = TieringService()
            tier_result = tiering_service.evaluate_and_update_tier(
                member, trigger_event=f"order_points_awarded:{order.order_number}"
            )

            if tier_result["changed"]:
                action = tier_result["action"]
                new_tier_name = (
                    tier_result["new_tier"].name if tier_result["new_tier"] else "No Tier"
                )
                logger.info(f"Member {member.id} tier {action}: {new_tier_name}")

            logger.info(
                f"Awarded {points} points to member {member.id} for order {order.order_number}"
            )

        return txn

    def award_action_points(
        self, member: LoyaltyMember, action_type: str, metadata: dict = None, admin_user=None
    ) -> LoyaltyTransaction | None:
        """
        Award points for an action (signup, review, etc.).

        Args:
            member: LoyaltyMember instance
            action_type: Type of action (signup, review, social_share, etc.)
            metadata: Optional dict with action details
            admin_user: Optional admin user for audit

        Returns:
            LoyaltyTransaction instance or None if no points awarded
        """
        metadata = metadata or {}

        # Find applicable action-based rules
        rules = LoyaltyRule.objects.filter(
            rule_type=LoyaltyRule.TYPE_ACTION_BASED,
            action_type=action_type,
            is_active=True,
        ).order_by("priority")

        # Filter by tier if applicable
        if member.current_tier:
            rules = [r for r in rules if r.applies_to_tier(member.current_tier)]

        # Filter by date
        rules = [r for r in rules if r.is_currently_active()]

        if not rules:
            logger.info(f"No rules found for action {action_type}")
            return None

        # Use first applicable rule
        rule = rules[0]
        points = int(rule.points_rate)

        # Apply tier multiplier
        if member.current_tier:
            points = int(points * float(member.current_tier.points_multiplier))

        # Check caps against only the rule that produced this award
        if not self._check_daily_cap(member, points, [rule]):
            logger.warning(f"Daily cap reached for member {member.id}")
            return None

        if not self._check_member_cap(member, points, [rule]):
            logger.warning(f"Member cap reached for member {member.id}")
            return None

        # Calculate expiration
        expires_at = None
        if rule.points_expire_days:
            expires_at = timezone.now() + timedelta(days=rule.points_expire_days)

        # Determine status
        status = (
            LoyaltyTransaction.STATUS_PENDING
            if rule.points_pending_days > 0
            else LoyaltyTransaction.STATUS_AVAILABLE
        )

        # Create transaction
        description = f"Earned {points} points for {rule.get_action_type_display()}"
        if metadata:
            description += f" ({metadata.get('description', '')})"

        with transaction.atomic():
            txn = LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_EARN,
                points=points,
                status=status,
                description=description,
                reason=f"Action: {action_type}",
                related_object_type=metadata.get("object_type", ""),
                related_object_id=metadata.get("object_id", ""),
                expires_at=expires_at,
                created_by=admin_user,
            )

            # Update balance
            self._update_balance(member, txn)

            # Evaluate tier eligibility after points change
            tiering_service = TieringService()
            tier_result = tiering_service.evaluate_and_update_tier(
                member, trigger_event=f"action_points_awarded:{action_type}"
            )

            if tier_result["changed"]:
                action_name = tier_result["action"]
                new_tier_name = (
                    tier_result["new_tier"].name if tier_result["new_tier"] else "No Tier"
                )
                logger.info(f"Member {member.id} tier {action_name}: {new_tier_name}")

            logger.info(f"Awarded {points} points to member {member.id} for action {action_type}")

        return txn

    def award_bonus_points(
        self, member: LoyaltyMember, points: int, description: str = "", admin_user=None
    ) -> LoyaltyTransaction | None:
        """
        Award bonus points directly (e.g., for badges, promotions, manual gifts).

        Unlike award_action_points, this doesn't require a LoyaltyRule - points
        are awarded directly as specified. Use this for badge rewards, referral
        bonuses, or other direct point grants.

        Args:
            member: LoyaltyMember instance
            points: Number of points to award
            description: Description for the transaction
            admin_user: Optional admin user for audit

        Returns:
            LoyaltyTransaction instance
        """
        if points <= 0:
            logger.warning(f"Attempted to award {points} bonus points - must be positive")
            return None

        with transaction.atomic():
            txn = LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_BONUS,
                points=points,
                status=LoyaltyTransaction.STATUS_AVAILABLE,
                description=description or f"Bonus: {points} points",
                reason="bonus_award",
                created_by=admin_user,
            )

            # Update balance
            self._update_balance(member, txn)

            # Evaluate tier eligibility after points change
            tiering_service = TieringService()
            tier_result = tiering_service.evaluate_and_update_tier(
                member, trigger_event="bonus_points_awarded"
            )

            if tier_result["changed"]:
                action_name = tier_result["action"]
                new_tier_name = (
                    tier_result["new_tier"].name if tier_result["new_tier"] else "No Tier"
                )
                logger.info(f"Member {member.id} tier {action_name}: {new_tier_name}")

            logger.info(f"Awarded {points} bonus points to member {member.id}: {description}")

        return txn

    def _get_applicable_rules(self, member: LoyaltyMember) -> list[LoyaltyRule]:
        """Get rules applicable to this member, ordered by priority."""
        rules = LoyaltyRule.objects.filter(
            rule_type__in=[LoyaltyRule.TYPE_SPEND_BASED, LoyaltyRule.TYPE_ITEM_BASED],
            is_active=True,
        ).order_by("priority")

        # Filter by tier
        if member.current_tier:
            rules = [r for r in rules if r.applies_to_tier(member.current_tier)]
        else:
            rules = [r for r in rules if not r.allowed_tiers.exists()]

        # Filter by date
        rules = [r for r in rules if r.is_currently_active()]

        return list(rules)

    def _evaluate_rule(self, rule: LoyaltyRule, order, member: LoyaltyMember) -> int:
        """Evaluate a single rule against an order."""
        # Gift card lines never earn.
        #
        # Buying stored value is not spending: the customer earns when they
        # spend the card on goods, and counting the purchase too pays points
        # twice for one pound passing through the store. Excluded from the
        # minimum-order gate as well as the calculation, or a basket only
        # qualifies because of a gift card it will not earn on.
        earning_base = self._earning_base(order)

        # Check minimum order amount
        if earning_base < rule.min_order_amount:
            return 0

        # Calculate points based on rule type
        if rule.rule_type == LoyaltyRule.TYPE_SPEND_BASED:
            # Points = floor(earning base * rate). Multiply the Decimals directly;
            # going via binary float can drop exact products just below an integer
            # and under-award by one point. int() truncates toward zero (== floor
            # for the non-negative earning base).
            points = int(earning_base * rule.points_rate)
            return points

        elif rule.rule_type == LoyaltyRule.TYPE_ITEM_BASED:
            # Calculate points per qualifying item
            total_points = 0
            for item in order.items.select_related("product", "product__brand").all():
                # Gift cards never earn (see _earning_base) — skip before scoping.
                if getattr(item.product, "product_type", None) == "gift_card":
                    continue
                if self._item_matches_scope(rule, item):
                    total_points += int(rule.points_rate) * item.quantity
            return total_points

        return 0

    def _earning_base(self, order):
        """
        The part of an order that can earn points.

        ``order.subtotal`` includes gift card lines; this subtracts them. Falls
        back to the subtotal when the order has no item rows loaded, so a
        points award never silently becomes zero because of a query shape.
        """
        from decimal import Decimal

        subtotal = order.subtotal.amount
        gift_card_total = Decimal("0")
        for item in order.items.select_related("product").all():
            if getattr(item.product, "product_type", None) == "gift_card":
                gift_card_total += item.total_price.amount

        if gift_card_total <= 0:
            return subtotal
        return max(subtotal - gift_card_total, Decimal("0"))

    def _item_matches_scope(self, rule: LoyaltyRule, item) -> bool:
        """Check if an order item matches the rule's scope filters."""
        if rule.scope == LoyaltyRule.SCOPE_ALL:
            return True

        scope_filters = rule.scope_filters or {}

        if rule.scope == LoyaltyRule.SCOPE_PRODUCT:
            product_ids = scope_filters.get("product_ids", [])
            return not product_ids or item.product_id in product_ids

        if rule.scope == LoyaltyRule.SCOPE_CATEGORY:
            category_ids = scope_filters.get("category_ids", [])
            return not category_ids or item.product.category_id in category_ids

        if rule.scope == LoyaltyRule.SCOPE_BRAND:
            brand_ids = scope_filters.get("brand_ids", [])
            return not brand_ids or (item.product.brand_id and item.product.brand_id in brand_ids)

        return False

    def _check_daily_cap(
        self, member: LoyaltyMember, points: int, rules: list[LoyaltyRule]
    ) -> bool:
        """Check if awarding points would exceed daily cap.

        Only enforces caps belonging to the rules that produced this award; an
        unrelated active rule must not block a valid award.
        """
        caps = [r.max_points_per_day for r in rules if r.max_points_per_day]
        if not caps:
            return True

        # Check today's points for this member
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_points = (
            LoyaltyTransaction.objects.filter(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_EARN,
                created_at__gte=today_start,
            ).aggregate(total=Sum("points"))["total"]
            or 0
        )

        # Check against the strictest cap among the matched rules
        return (today_points + points) <= min(caps)

    def _check_member_cap(
        self, member: LoyaltyMember, points: int, rules: list[LoyaltyRule]
    ) -> bool:
        """Check if awarding points would exceed member lifetime cap.

        Only enforces caps belonging to the rules that produced this award; an
        unrelated active rule must not block a valid award.
        """
        caps = [r.max_points_per_member for r in rules if r.max_points_per_member]
        if not caps:
            return True

        # Get member's lifetime earned
        balance = LoyaltyBalance.objects.filter(member=member).first()
        if not balance:
            return True

        lifetime_earned = balance.lifetime_earned

        # Check against the strictest cap among the matched rules
        return (lifetime_earned + points) <= min(caps)

    def _update_balance(self, member: LoyaltyMember, transaction: LoyaltyTransaction):
        """Update member's balance based on transaction."""
        # Lock the balance row for the read-modify-write so concurrent awards for
        # the same member cannot both read the same values and lose an update
        # (the sibling redemption_engine locks its rows the same way). Runs inside
        # the caller's atomic block; get_or_create can still race on first award,
        # so retry the locked read once if a concurrent create won.
        try:
            balance = LoyaltyBalance.objects.select_for_update().get(member=member)
        except LoyaltyBalance.DoesNotExist:
            LoyaltyBalance.objects.get_or_create(member=member)
            balance = LoyaltyBalance.objects.select_for_update().get(member=member)

        if transaction.transaction_type in (
            LoyaltyTransaction.TYPE_EARN,
            LoyaltyTransaction.TYPE_BONUS,
        ):
            # Add to lifetime earned
            balance.lifetime_earned += transaction.points

            # Add to appropriate balance field. Bonus awards are always available,
            # so they fall through to available_points here.
            if transaction.status == LoyaltyTransaction.STATUS_PENDING:
                balance.pending_points += transaction.points
            else:
                balance.available_points += transaction.points

            # Update last earned timestamp
            balance.last_earned_at = timezone.now()

        elif transaction.transaction_type == LoyaltyTransaction.TYPE_BONUS:
            # Bonus points count as earned and are immediately available.
            # Mirrors LedgerService.reconcile_balance so the cached balance
            # agrees with the authoritative ledger.
            balance.lifetime_earned += transaction.points
            balance.available_points += transaction.points
            balance.last_earned_at = timezone.now()

        elif transaction.transaction_type == LoyaltyTransaction.TYPE_REDEEM:
            balance.available_points += transaction.points

            # Signed, not abs(): a redemption carries negative points and its
            # refund (LedgerService.refund_redemption) carries positive points
            # on the same type, so the pair must net to zero rather than count
            # the refund as a second redemption. Identical to the previous
            # abs() behaviour for redemption rows, which are always negative.
            # Kept in step with LedgerService.reconcile_balance deliberately —
            # the two must agree or the cached balance drifts from the ledger.
            balance.lifetime_redeemed -= transaction.points

            # Only a real redemption moves this; a refund is not a redemption.
            if transaction.points < 0:
                balance.last_redeemed_at = timezone.now()

        elif transaction.transaction_type == LoyaltyTransaction.TYPE_EXPIRE:
            # Subtract from available points
            balance.available_points += transaction.points  # points are negative
            balance.lifetime_expired += abs(transaction.points)

        elif transaction.transaction_type == LoyaltyTransaction.TYPE_REVOKE:
            # Reverse previous award
            balance.available_points += transaction.points  # points are negative

        balance.save()


# Singleton instance
points_engine = PointsEngine()
