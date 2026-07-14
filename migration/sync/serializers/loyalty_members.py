"""
Loyalty Program Members Sync Serializer

Handles export/import of loyalty member data:
- LoyaltyMember (with nested LoyaltyBalance)
- LoyaltyTransaction (immutable ledger)
- LoyaltyRedemption
- LoyaltyMemberBadge
- LoyaltyCampaignExecution
- LoyaltySegmentMembership
"""

import logging

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

MEMBER_FIELDS = ["is_active"]

BALANCE_FIELDS = [
    "available_points",
    "pending_points",
    "lifetime_earned",
    "lifetime_redeemed",
    "lifetime_expired",
]

TRANSACTION_FIELDS = [
    "transaction_type",
    "points",
    "status",
    "description",
    "reason",
    "related_object_type",
    "related_object_id",
    "admin_note",
]

REDEMPTION_FIELDS = [
    "redemption_code",
    "points_spent",
    "status",
    "cancellation_reason",
    "admin_note",
]


class LoyaltyMembersSerializer(CollectionSyncSerializer):
    category_key = "loyalty_members"
    natural_key_fields = ["_user_email"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from loyalty.models import LoyaltyMember

        self.model_class = LoyaltyMember

    def get_count(self):
        from loyalty.models import (
            LoyaltyBalance,
            LoyaltyMember,
            LoyaltyMemberBadge,
            LoyaltyRedemption,
            LoyaltyTransaction,
        )

        return (
            LoyaltyMember.objects.count()
            + LoyaltyBalance.objects.count()
            + LoyaltyTransaction.objects.count()
            + LoyaltyRedemption.objects.count()
            + LoyaltyMemberBadge.objects.count()
        )

    def export(self, credential_mode="redact"):
        from loyalty.models import LoyaltyMember

        items = []
        for member in (
            LoyaltyMember.objects.select_related(
                "customer",
                "current_tier",
                "balance",
            )
            .prefetch_related(
                "transactions",
                "redemptions",
                "redemptions__reward",
                "badges_earned",
                "badges_earned__badge",
            )
            .all()
        ):
            data = {f: getattr(member, f) for f in MEMBER_FIELDS}
            data["_source_pk"] = member.pk
            data["_model"] = "LoyaltyMember"
            data["_user_email"] = member.customer.email
            data["_tier_slug"] = member.current_tier.slug if member.current_tier else None

            if member.enrolled_at:
                data["_enrolled_at"] = member.enrolled_at.isoformat()

            # Balance (OneToOne)
            if hasattr(member, "balance"):
                bal = member.balance
                data["_balance"] = {f: getattr(bal, f) for f in BALANCE_FIELDS}

            # Transactions
            data["_transactions"] = []
            for tx in member.transactions.all().order_by("created_at"):
                tx_data = {f: getattr(tx, f) for f in TRANSACTION_FIELDS}
                if tx.created_at:
                    tx_data["_created_at"] = tx.created_at.isoformat()
                if tx.expires_at:
                    tx_data["_expires_at"] = tx.expires_at.isoformat()
                data["_transactions"].append(tx_data)

            # Redemptions
            data["_redemptions"] = []
            for red in member.redemptions.all().order_by("created_at"):
                r_data = {f: getattr(red, f) for f in REDEMPTION_FIELDS}
                r_data["_reward_slug"] = red.reward.slug if red.reward else None
                r_data["_order_number"] = red.order.order_number if red.order else None
                if red.created_at:
                    r_data["_created_at"] = red.created_at.isoformat()
                data["_redemptions"].append(r_data)

            # Badges
            data["_badges"] = []
            for mb in member.badges_earned.all():
                data["_badges"].append(
                    {
                        "_badge_slug": mb.badge.slug,
                        "_earned_at": mb.earned_at.isoformat() if mb.earned_at else None,
                    }
                )

            items.append(data)

        return {
            "category": self.category_key,
            "sync_type": "collection",
            "items": items,
            "total": len(items),
        }

    def import_data(self, data, dry_run=False, sync_mode="additive"):
        if dry_run:
            return self.generate_diff(data)

        items = data.get("items", [])
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        for item in items:
            try:
                with transaction.atomic():
                    self._import_member(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"LoyaltyMember '{item.get('_user_email', '?')}': {e}")

        return {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

    def _import_member(self, item):
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime

        from loyalty.models import (
            LoyaltyBadge,
            LoyaltyBalance,
            LoyaltyMember,
            LoyaltyMemberBadge,
            LoyaltyRedemption,
            LoyaltyReward,
            LoyaltyTier,
            LoyaltyTransaction,
        )

        User = get_user_model()

        user = User.objects.filter(email=item["_user_email"]).first()
        if not user:
            raise ValueError(f"User not found: {item['_user_email']}")

        existing = LoyaltyMember.objects.filter(customer=user).first()
        member = existing or LoyaltyMember(customer=user)

        for f in MEMBER_FIELDS:
            if f in item:
                setattr(member, f, item[f])

        tier_slug = item.get("_tier_slug")
        if tier_slug:
            member.current_tier = LoyaltyTier.objects.filter(slug=tier_slug).first()

        enrolled = item.get("_enrolled_at")
        if enrolled:
            parsed = parse_datetime(enrolled)
            if parsed:
                member.enrolled_at = parsed

        member.save()

        # Balance
        bal_data = item.get("_balance")
        if bal_data:
            bal, _ = LoyaltyBalance.objects.get_or_create(member=member)
            for f in BALANCE_FIELDS:
                if f in bal_data:
                    setattr(bal, f, bal_data[f])
            bal.save()

        # Transactions (append-only)
        for tx_data in item.get("_transactions", []):
            created_str = tx_data.get("_created_at")
            created_at = parse_datetime(created_str) if created_str else None

            if created_at:
                exists = LoyaltyTransaction.objects.filter(
                    member=member,
                    transaction_type=tx_data.get("transaction_type"),
                    created_at=created_at,
                ).exists()
                if exists:
                    continue

            tx = LoyaltyTransaction(member=member)
            for f in TRANSACTION_FIELDS:
                if f in tx_data:
                    setattr(tx, f, tx_data[f])
            expires = tx_data.get("_expires_at")
            if expires:
                tx.expires_at = parse_datetime(expires)
            tx.save()

        # Redemptions
        for r_data in item.get("_redemptions", []):
            existing_red = LoyaltyRedemption.objects.filter(
                redemption_code=r_data["redemption_code"],
            ).first()
            if existing_red:
                continue

            red = LoyaltyRedemption(member=member)
            for f in REDEMPTION_FIELDS:
                if f in r_data:
                    setattr(red, f, r_data[f])

            reward_slug = r_data.get("_reward_slug")
            if reward_slug:
                red.reward = LoyaltyReward.objects.filter(slug=reward_slug).first()

            from orders.models import Order

            order_num = r_data.get("_order_number")
            if order_num:
                red.order = Order.objects.filter(order_number=order_num).first()

            red.save()

        # Badges
        for b_data in item.get("_badges", []):
            badge_slug = b_data.get("_badge_slug")
            if badge_slug:
                badge = LoyaltyBadge.objects.filter(slug=badge_slug).first()
                if badge:
                    LoyaltyMemberBadge.objects.get_or_create(
                        member=member,
                        badge=badge,
                    )

    def generate_diff(self, remote_data):
        from django.contrib.auth import get_user_model

        from loyalty.models import LoyaltyMember

        User = get_user_model()

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            user = User.objects.filter(email=item.get("_user_email")).first()
            name = item.get("_user_email", "?")
            if user:
                existing = LoyaltyMember.objects.filter(customer=user).first()
                if existing:
                    changes.append(
                        {"type": "modify", "model": "LoyaltyMember", "name": name, "changes": []}
                    )
                else:
                    changes.append(
                        {"type": "add", "model": "LoyaltyMember", "name": name, "fields": {}}
                    )
            else:
                changes.append(
                    {"type": "add", "model": "LoyaltyMember", "name": name, "fields": {}}
                )

        adds = sum(1 for c in changes if c["type"] == "add")
        mods = sum(1 for c in changes if c["type"] == "modify")
        parts = []
        if adds:
            parts.append(f"{adds} addition(s)")
        if mods:
            parts.append(f"{mods} modification(s)")

        return {
            "changes": changes,
            "warnings": [],
            "summary": ", ".join(parts) if parts else "No changes",
        }

    def snapshot_current(self):
        return self.export(credential_mode="skip")

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {"restored": result.get("synced", 0), "errors": result.get("errors", [])}
        except Exception as e:
            return {"restored": 0, "errors": [str(e)]}
