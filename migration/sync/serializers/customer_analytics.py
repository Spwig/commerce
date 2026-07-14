"""
Customer Analytics & History Sync Serializer

Handles export/import of customer analytics data:
- CustomerNote
- AbandonedCart (with MoneyField)
- CustomerCohort (with nested CohortMetrics)
- PreferenceChangeLog
"""

import logging
from decimal import Decimal

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

CUSTOMER_NOTE_FIELDS = [
    "note_type",
    "title",
    "content",
    "requires_follow_up",
    "completed",
    "is_internal",
]

ABANDONED_CART_FIELDS = [
    "estimated_reason",
    "total_items",
    "recovery_emails_sent",
    "recovered",
]

COHORT_FIELDS = [
    "cohort_date",
    "acquisition_channel",
    "first_product_category",
    "customer_count",
]

COHORT_METRICS_FIELDS = [
    "months_since_acquisition",
    "active_customers",
    "cumulative_orders",
    "retention_rate",
]
COHORT_METRICS_MONEY_FIELDS = ["cumulative_revenue", "average_ltv"]

PREFERENCE_LOG_FIELDS = [
    "action",
    "old_value",
    "new_value",
    "ip_address",
    "user_agent",
    "source",
    "notes",
]


def _serialize_money(data, instance, field_name):
    val = getattr(instance, field_name, None)
    if val is not None:
        data[f"_{field_name}_amount"] = str(val.amount) if hasattr(val, "amount") else str(val)
        data[f"_{field_name}_currency"] = (
            str(val.currency)
            if hasattr(val, "currency")
            else getattr(instance, f"{field_name}_currency", None)
        )
    else:
        data[f"_{field_name}_amount"] = None
        data[f"_{field_name}_currency"] = None


def _deserialize_money(instance, item, field_name):
    amount = item.get(f"_{field_name}_amount")
    currency = item.get(f"_{field_name}_currency")
    if amount is not None:
        setattr(instance, field_name, Decimal(str(amount)))
    if currency:
        setattr(instance, f"{field_name}_currency", currency)


class CustomerAnalyticsSerializer(CollectionSyncSerializer):
    category_key = "customer_analytics"
    natural_key_fields = ["_user_email"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from customers.models import CustomerNote

        self.model_class = CustomerNote

    def get_count(self):
        from accounts.models import PreferenceChangeLog
        from customers.models import AbandonedCart, CohortMetrics, CustomerCohort, CustomerNote

        return (
            CustomerNote.objects.count()
            + AbandonedCart.objects.count()
            + CustomerCohort.objects.count()
            + CohortMetrics.objects.count()
            + PreferenceChangeLog.objects.count()
        )

    def export(self, credential_mode="redact"):
        from accounts.models import PreferenceChangeLog
        from customers.models import AbandonedCart, CustomerCohort, CustomerNote

        items = []

        # Customer Notes
        for note in CustomerNote.objects.select_related("customer", "created_by").all():
            data = {f: getattr(note, f) for f in CUSTOMER_NOTE_FIELDS}
            data["_source_pk"] = note.pk
            data["_model"] = "CustomerNote"
            data["_user_email"] = note.customer.email
            data["_created_by_email"] = note.created_by.email if note.created_by else None
            if note.created_at:
                data["_created_at"] = note.created_at.isoformat()
            if note.follow_up_date:
                data["_follow_up_date"] = note.follow_up_date.isoformat()
            items.append(data)

        # Abandoned Carts
        for ac in AbandonedCart.objects.select_related("user", "recovery_order").all():
            data = {f: getattr(ac, f) for f in ABANDONED_CART_FIELDS}
            data["_source_pk"] = ac.pk
            data["_model"] = "AbandonedCart"
            data["_user_email"] = ac.user.email
            _serialize_money(data, ac, "total_value")
            if ac.abandoned_at:
                data["_abandoned_at"] = ac.abandoned_at.isoformat()
            if ac.recovery_order:
                data["_recovery_order_number"] = ac.recovery_order.order_number
            items.append(data)

        # Cohorts with nested metrics
        for cohort in CustomerCohort.objects.prefetch_related("metrics").all():
            data = {f: getattr(cohort, f) for f in COHORT_FIELDS}
            data["_source_pk"] = cohort.pk
            data["_model"] = "CustomerCohort"
            if hasattr(data.get("cohort_date"), "isoformat"):
                data["cohort_date"] = data["cohort_date"].isoformat()

            data["_metrics"] = []
            for m in cohort.metrics.all().order_by("months_since_acquisition"):
                m_data = {f: getattr(m, f) for f in COHORT_METRICS_FIELDS}
                for mf in COHORT_METRICS_MONEY_FIELDS:
                    _serialize_money(m_data, m, mf)
                data["_metrics"].append(m_data)

            items.append(data)

        # Preference Change Logs
        for log in PreferenceChangeLog.objects.select_related("user").all()[:10000]:
            data = {f: getattr(log, f) for f in PREFERENCE_LOG_FIELDS}
            data["_source_pk"] = log.pk
            data["_model"] = "PreferenceChangeLog"
            data["_user_email"] = log.user.email
            if log.timestamp:
                data["_timestamp"] = log.timestamp.isoformat()
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
            model_type = item.get("_model")
            try:
                with transaction.atomic():
                    if model_type == "CustomerNote":
                        self._import_note(item)
                    elif model_type == "AbandonedCart":
                        self._import_abandoned_cart(item)
                    elif model_type == "CustomerCohort":
                        self._import_cohort(item)
                    elif model_type == "PreferenceChangeLog":
                        self._import_pref_log(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{model_type}: {e}")

        return {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

    def _import_note(self, item):
        from django.contrib.auth import get_user_model

        from customers.models import CustomerNote

        User = get_user_model()

        customer = User.objects.filter(email=item["_user_email"]).first()
        if not customer:
            return

        note = CustomerNote(customer=customer)
        for f in CUSTOMER_NOTE_FIELDS:
            if f in item:
                setattr(note, f, item[f])

        created_by_email = item.get("_created_by_email")
        if created_by_email:
            note.created_by = User.objects.filter(email=created_by_email).first()

        from django.utils.dateparse import parse_date

        fup = item.get("_follow_up_date")
        if fup:
            note.follow_up_date = parse_date(fup)

        note.save()

    def _import_abandoned_cart(self, item):
        # AbandonedCart requires a Cart FK — skip import as carts are ephemeral
        logger.info("Skipping AbandonedCart import (cart FK is ephemeral)")

    def _import_cohort(self, item):
        from django.utils.dateparse import parse_date

        from customers.models import CohortMetrics, CustomerCohort

        cohort_date = (
            parse_date(item["cohort_date"])
            if isinstance(item["cohort_date"], str)
            else item["cohort_date"]
        )

        existing = CustomerCohort.objects.filter(
            cohort_date=cohort_date,
            acquisition_channel=item["acquisition_channel"],
            first_product_category=item.get("first_product_category", ""),
        ).first()
        cohort = existing or CustomerCohort()

        for f in COHORT_FIELDS:
            if f in item:
                val = item[f]
                if f == "cohort_date" and isinstance(val, str):
                    val = parse_date(val)
                setattr(cohort, f, val)
        cohort.save()

        # Replace metrics
        if existing:
            cohort.metrics.all().delete()

        for m_data in item.get("_metrics", []):
            m = CohortMetrics(cohort=cohort)
            for f in COHORT_METRICS_FIELDS:
                if f in m_data:
                    setattr(m, f, m_data[f])
            for mf in COHORT_METRICS_MONEY_FIELDS:
                _deserialize_money(m, m_data, mf)
            m.save()

    def _import_pref_log(self, item):
        from django.contrib.auth import get_user_model

        from accounts.models import PreferenceChangeLog

        User = get_user_model()

        user = User.objects.filter(email=item["_user_email"]).first()
        if not user:
            return

        log = PreferenceChangeLog(user=user)
        for f in PREFERENCE_LOG_FIELDS:
            if f in item:
                setattr(log, f, item[f])

        # preference FK is hard to resolve portably — skip if not found
        log.save()

    def generate_diff(self, remote_data):
        items = remote_data.get("items", [])
        model_counts = {}
        for item in items:
            mt = item.get("_model", "?")
            model_counts[mt] = model_counts.get(mt, 0) + 1

        parts = [f"{count} {model}(s)" for model, count in model_counts.items()]

        return {
            "changes": [],
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
