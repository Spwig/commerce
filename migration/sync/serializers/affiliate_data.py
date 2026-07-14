"""
Affiliate Data Sync Serializer

Handles export/import of affiliate member data:
- Affiliate (profile)
- AffiliateProgramMembership (through model)
- Link (tracking links)
- Commission (earnings ledger)
- Payout (disbursements)
"""

import logging
from decimal import Decimal

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

AFFILIATE_FIELDS = [
    "affiliate_code",
    "company_name",
    "website",
    "payment_email",
    "payment_method",
    "bank_account_holder",
    "bank_account_number",
    "bank_routing_code",
    "bank_swift_code",
    "bank_country",
    "bank_currency",
    "status",
]

MEMBERSHIP_FIELDS = ["status", "notes"]

LINK_FIELDS = [
    "link_code",
    "destination_url",
    "label",
    "is_active",
]

COMMISSION_FIELDS = [
    "amount",
    "currency",
    "amount_base",
    "base_currency",
    "exchange_rate_used",
    "status",
    "notes",
]

PAYOUT_FIELDS = [
    "amount",
    "method",
    "status",
    "reference",
    "notes",
    "provider_reference",
    "provider_response",
    "currency",
    "amount_base",
    "base_currency",
]


class AffiliateDataSerializer(CollectionSyncSerializer):
    category_key = "affiliate_data"
    natural_key_fields = ["_user_email"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from affiliate.models import Affiliate

        self.model_class = Affiliate

    def get_count(self):
        from affiliate.models import (
            Affiliate,
            AffiliateProgramMembership,
            Commission,
            Link,
            Payout,
        )

        return (
            Affiliate.objects.count()
            + AffiliateProgramMembership.objects.count()
            + Link.objects.count()
            + Commission.objects.count()
            + Payout.objects.count()
        )

    def export(self, credential_mode="redact"):
        from affiliate.models import Affiliate

        items = []
        for aff in (
            Affiliate.objects.select_related("user")
            .prefetch_related(
                "affiliateprogrammembership_set",
                "affiliateprogrammembership_set__program",
                "links",
                "links__program",
                "commissions",
                "commissions__program",
                "commissions__order",
                "payouts",
            )
            .all()
        ):
            data = {f: getattr(aff, f) for f in AFFILIATE_FIELDS}
            data["_source_pk"] = aff.pk
            data["_model"] = "Affiliate"
            data["_user_email"] = aff.user.email

            if aff.created_at:
                data["_created_at"] = aff.created_at.isoformat()

            # Program memberships
            data["_memberships"] = []
            for m in aff.affiliateprogrammembership_set.all():
                m_data = {f: getattr(m, f) for f in MEMBERSHIP_FIELDS}
                m_data["_program_slug"] = m.program.slug
                if m.applied_at:
                    m_data["_applied_at"] = m.applied_at.isoformat()
                if m.approved_at:
                    m_data["_approved_at"] = m.approved_at.isoformat()
                data["_memberships"].append(m_data)

            # Links
            data["_links"] = []
            for link in aff.links.all():
                l_data = {f: getattr(link, f) for f in LINK_FIELDS}
                l_data["_program_slug"] = link.program.slug
                if link.created_at:
                    l_data["_created_at"] = link.created_at.isoformat()
                data["_links"].append(l_data)

            # Commissions
            data["_commissions"] = []
            for comm in aff.commissions.all().order_by("created_at"):
                c_data = {f: getattr(comm, f) for f in COMMISSION_FIELDS}
                c_data["_program_slug"] = comm.program.slug
                c_data["_order_number"] = comm.order.order_number if comm.order else None
                # Convert Decimals to string
                for df in ["amount", "amount_base", "exchange_rate_used"]:
                    val = c_data.get(df)
                    if val is not None:
                        c_data[df] = str(val)
                if comm.created_at:
                    c_data["_created_at"] = comm.created_at.isoformat()
                if comm.approved_at:
                    c_data["_approved_at"] = comm.approved_at.isoformat()
                if comm.paid_at:
                    c_data["_paid_at"] = comm.paid_at.isoformat()
                data["_commissions"].append(c_data)

            # Payouts
            data["_payouts"] = []
            for payout in aff.payouts.all().order_by("created_at"):
                p_data = {f: getattr(payout, f) for f in PAYOUT_FIELDS}
                # Convert Decimals to string
                for df in ["amount", "amount_base"]:
                    val = p_data.get(df)
                    if val is not None:
                        p_data[df] = str(val)
                # Commission link_codes for this payout
                p_data["_commission_order_numbers"] = [
                    c.order.order_number for c in payout.commissions.all() if c.order
                ]
                if payout.created_at:
                    p_data["_created_at"] = payout.created_at.isoformat()
                if payout.processed_at:
                    p_data["_processed_at"] = payout.processed_at.isoformat()
                if payout.completed_at:
                    p_data["_completed_at"] = payout.completed_at.isoformat()
                data["_payouts"].append(p_data)

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
                    self._import_affiliate(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Affiliate '{item.get('_user_email', '?')}': {e}")

        return {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

    def _import_affiliate(self, item):
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime

        from affiliate.models import (
            Affiliate,
            AffiliateProgramMembership,
            Commission,
            Link,
            Payout,
            Program,
        )

        User = get_user_model()

        user = User.objects.filter(email=item["_user_email"]).first()
        if not user:
            raise ValueError(f"User not found: {item['_user_email']}")

        existing = Affiliate.objects.filter(user=user).first()
        aff = existing or Affiliate(user=user)

        for f in AFFILIATE_FIELDS:
            if f in item:
                setattr(aff, f, item[f])

        created_str = item.get("_created_at")
        if created_str:
            parsed = parse_datetime(created_str)
            if parsed:
                aff.created_at = parsed

        aff.save()

        # Memberships
        for m_data in item.get("_memberships", []):
            program = Program.objects.filter(slug=m_data["_program_slug"]).first()
            if not program:
                continue
            mem, created = AffiliateProgramMembership.objects.get_or_create(
                affiliate=aff,
                program=program,
            )
            for f in MEMBERSHIP_FIELDS:
                if f in m_data:
                    setattr(mem, f, m_data[f])
            applied = m_data.get("_applied_at")
            if applied:
                mem.applied_at = parse_datetime(applied)
            approved = m_data.get("_approved_at")
            if approved:
                mem.approved_at = parse_datetime(approved)
            mem.save()

        # Links
        for l_data in item.get("_links", []):
            program = Program.objects.filter(slug=l_data.get("_program_slug")).first()
            if not program:
                continue
            existing_link = Link.objects.filter(link_code=l_data["link_code"]).first()
            link = existing_link or Link(affiliate=aff, program=program)
            for f in LINK_FIELDS:
                if f in l_data:
                    setattr(link, f, l_data[f])
            link.save()

        # Commissions (append-only)
        for c_data in item.get("_commissions", []):
            order_number = c_data.get("_order_number")
            if not order_number:
                continue

            from orders.models import Order

            order = Order.objects.filter(order_number=order_number).first()
            if not order:
                continue

            program = Program.objects.filter(slug=c_data.get("_program_slug")).first()
            if not program:
                continue

            # Deduplicate by affiliate + order
            if Commission.objects.filter(affiliate=aff, order=order).exists():
                continue

            comm = Commission(affiliate=aff, program=program, order=order)
            for f in ["status", "currency", "base_currency", "notes"]:
                if f in c_data:
                    setattr(comm, f, c_data[f])
            for df in ["amount", "amount_base", "exchange_rate_used"]:
                val = c_data.get(df)
                if val is not None:
                    setattr(comm, df, Decimal(str(val)))
            for dt_field, key in [("approved_at", "_approved_at"), ("paid_at", "_paid_at")]:
                val = c_data.get(key)
                if val:
                    setattr(comm, dt_field, parse_datetime(val))
            comm.save()

        # Payouts (append-only)
        for p_data in item.get("_payouts", []):
            created_str = p_data.get("_created_at")
            created_at = parse_datetime(created_str) if created_str else None

            # Deduplicate by affiliate + created_at
            if (
                created_at
                and Payout.objects.filter(
                    affiliate=aff,
                    created_at=created_at,
                ).exists()
            ):
                continue

            payout = Payout(affiliate=aff)
            for f in [
                "method",
                "status",
                "reference",
                "notes",
                "provider_reference",
                "provider_response",
                "currency",
                "base_currency",
            ]:
                if f in p_data:
                    setattr(payout, f, p_data[f])
            for df in ["amount", "amount_base"]:
                val = p_data.get(df)
                if val is not None:
                    setattr(payout, df, Decimal(str(val)))
            for dt_field, key in [
                ("processed_at", "_processed_at"),
                ("completed_at", "_completed_at"),
            ]:
                val = p_data.get(key)
                if val:
                    setattr(payout, dt_field, parse_datetime(val))
            payout.save()

            # Re-link commissions by order number
            for order_num in p_data.get("_commission_order_numbers", []):
                comm = Commission.objects.filter(
                    affiliate=aff,
                    order__order_number=order_num,
                ).first()
                if comm:
                    payout.commissions.add(comm)

    def generate_diff(self, remote_data):
        from django.contrib.auth import get_user_model

        from affiliate.models import Affiliate

        User = get_user_model()

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            user = User.objects.filter(email=item.get("_user_email")).first()
            name = item.get("_user_email", "?")
            if user:
                existing = Affiliate.objects.filter(user=user).first()
                if existing:
                    changes.append(
                        {"type": "modify", "model": "Affiliate", "name": name, "changes": []}
                    )
                else:
                    changes.append(
                        {"type": "add", "model": "Affiliate", "name": name, "fields": {}}
                    )
            else:
                changes.append({"type": "add", "model": "Affiliate", "name": name, "fields": {}})

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
