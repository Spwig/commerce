"""
POS Transactions Sync Serializer

Handles export/import of POS transaction history:
- POSShift (with nested CashMovement)
- POSPayment
- ParkedCart
"""

import logging
from decimal import Decimal

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

SHIFT_FIELDS = [
    "opening_cash",
    "closing_cash",
    "expected_cash",
    "cash_difference",
    "total_sales",
    "total_refunds",
    "total_transactions",
    "total_manual_discounts",
    "manual_discount_count",
    "notes",
]

CASH_MOVEMENT_FIELDS = [
    "movement_type",
    "amount",
    "reason",
]

PAYMENT_FIELDS = [
    "method",
    "amount",
    "amount_tendered",
    "change_given",
    "card_last_four",
    "card_reference",
    "provider_payment_id",
    "card_brand",
    "gift_card_code",
]

PARKED_CART_FIELDS = [
    "cart_data",
    "item_count",
    "total_amount",
    "customer_name",
]


class POSTransactionsSerializer(CollectionSyncSerializer):
    category_key = "pos_transactions"
    natural_key_fields = ["_terminal_name", "_started_at"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pos_app.models import POSShift

        self.model_class = POSShift

    def get_count(self):
        from pos_app.models import CashMovement, ParkedCart, POSPayment, POSShift

        return (
            POSShift.objects.count()
            + CashMovement.objects.count()
            + POSPayment.objects.count()
            + ParkedCart.objects.count()
        )

    def export(self, credential_mode="redact"):
        from pos_app.models import ParkedCart, POSPayment, POSShift

        items = []

        # Shifts with nested cash movements
        for shift in (
            POSShift.objects.select_related(
                "terminal",
                "cashier",
            )
            .prefetch_related("cash_movements", "cash_movements__performed_by")
            .all()
        ):
            data = {f: getattr(shift, f) for f in SHIFT_FIELDS}
            data["_source_pk"] = shift.pk
            data["_model"] = "POSShift"
            data["_terminal_name"] = shift.terminal.name
            data["_cashier_email"] = shift.cashier.email
            # Convert Decimals
            for df in SHIFT_FIELDS:
                val = data.get(df)
                if isinstance(val, Decimal):
                    data[df] = str(val)
            if shift.started_at:
                data["_started_at"] = shift.started_at.isoformat()
            if shift.ended_at:
                data["_ended_at"] = shift.ended_at.isoformat()

            # Nested cash movements
            data["_cash_movements"] = []
            for cm in shift.cash_movements.all().order_by("created_at"):
                cm_data = {f: getattr(cm, f) for f in CASH_MOVEMENT_FIELDS}
                cm_data["_performed_by_email"] = cm.performed_by.email
                if isinstance(cm_data.get("amount"), Decimal):
                    cm_data["amount"] = str(cm_data["amount"])
                if cm.created_at:
                    cm_data["_created_at"] = cm.created_at.isoformat()
                data["_cash_movements"].append(cm_data)

            items.append(data)

        # POS Payments
        for payment in POSPayment.objects.select_related("order", "shift").all():
            data = {f: getattr(payment, f) for f in PAYMENT_FIELDS}
            data["_source_pk"] = payment.pk
            data["_model"] = "POSPayment"
            data["_order_number"] = payment.order.order_number
            data["_shift_terminal_name"] = payment.shift.terminal.name if payment.shift else None
            data["_shift_started_at"] = (
                payment.shift.started_at.isoformat()
                if payment.shift and payment.shift.started_at
                else None
            )
            # Convert Decimals
            for df in ["amount", "amount_tendered", "change_given"]:
                val = data.get(df)
                if isinstance(val, Decimal):
                    data[df] = str(val)
            if payment.created_at:
                data["_created_at"] = payment.created_at.isoformat()
            items.append(data)

        # Parked Carts
        for cart in ParkedCart.objects.select_related("terminal", "created_by").all():
            data = {f: getattr(cart, f) for f in PARKED_CART_FIELDS}
            data["_source_pk"] = cart.pk
            data["_model"] = "ParkedCart"
            data["_terminal_name"] = cart.terminal.name
            data["_created_by_email"] = cart.created_by.email
            if isinstance(data.get("total_amount"), Decimal):
                data["total_amount"] = str(data["total_amount"])
            if cart.parked_at:
                data["_parked_at"] = cart.parked_at.isoformat()
            if cart.restored_at:
                data["_restored_at"] = cart.restored_at.isoformat()
            if cart.expires_at:
                data["_expires_at"] = cart.expires_at.isoformat()
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

        order_map = {"POSShift": 0, "POSPayment": 1, "ParkedCart": 2}
        sorted_items = sorted(items, key=lambda x: order_map.get(x.get("_model"), 99))

        for item in sorted_items:
            model_type = item.get("_model")
            try:
                with transaction.atomic():
                    if model_type == "POSShift":
                        self._import_shift(item)
                    elif model_type == "POSPayment":
                        self._import_payment(item)
                    elif model_type == "ParkedCart":
                        self._import_parked_cart(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{model_type}: {e}")

        return {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

    def _import_shift(self, item):
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime

        from pos_app.models import CashMovement, POSShift, POSTerminal

        User = get_user_model()

        terminal = POSTerminal.objects.filter(name=item["_terminal_name"]).first()
        if not terminal:
            raise ValueError(f"Terminal not found: {item['_terminal_name']}")

        cashier = User.objects.filter(email=item["_cashier_email"]).first()
        if not cashier:
            raise ValueError(f"Cashier not found: {item['_cashier_email']}")

        started_at = parse_datetime(item["_started_at"]) if item.get("_started_at") else None

        # Deduplicate by terminal + started_at
        existing = None
        if started_at:
            existing = POSShift.objects.filter(
                terminal=terminal,
                started_at=started_at,
            ).first()
        if existing:
            return

        shift = POSShift(terminal=terminal, cashier=cashier)
        for f in SHIFT_FIELDS:
            val = item.get(f)
            if val is not None:
                if f in (
                    "opening_cash",
                    "closing_cash",
                    "expected_cash",
                    "cash_difference",
                    "total_sales",
                    "total_refunds",
                    "total_manual_discounts",
                ):
                    setattr(shift, f, Decimal(str(val)))
                else:
                    setattr(shift, f, val)

        ended = item.get("_ended_at")
        if ended:
            shift.ended_at = parse_datetime(ended)

        shift.save()

        # Cash movements
        for cm_data in item.get("_cash_movements", []):
            performer = User.objects.filter(email=cm_data.get("_performed_by_email")).first()
            if not performer:
                performer = cashier

            cm = CashMovement(shift=shift, performed_by=performer)
            cm.movement_type = cm_data.get("movement_type", "in")
            cm.reason = cm_data.get("reason", "")
            amount = cm_data.get("amount")
            if amount is not None:
                cm.amount = Decimal(str(amount))
            cm.save()

    def _import_payment(self, item):
        from django.utils.dateparse import parse_datetime

        from orders.models import Order
        from pos_app.models import POSPayment, POSShift, POSTerminal

        order = Order.objects.filter(order_number=item["_order_number"]).first()
        if not order:
            raise ValueError(f"Order not found: {item['_order_number']}")

        # Deduplicate by order + method + created_at
        created_str = item.get("_created_at")
        created_at = parse_datetime(created_str) if created_str else None
        if (
            created_at
            and POSPayment.objects.filter(
                order=order,
                method=item.get("method"),
                created_at=created_at,
            ).exists()
        ):
            return

        payment = POSPayment(order=order)
        for f in PAYMENT_FIELDS:
            val = item.get(f)
            if val is not None:
                if f in ("amount", "amount_tendered", "change_given"):
                    setattr(payment, f, Decimal(str(val)))
                else:
                    setattr(payment, f, val)

        # Resolve shift
        shift_terminal = item.get("_shift_terminal_name")
        shift_started = item.get("_shift_started_at")
        if shift_terminal and shift_started:
            terminal = POSTerminal.objects.filter(name=shift_terminal).first()
            if terminal:
                started_at = parse_datetime(shift_started)
                if started_at:
                    shift = POSShift.objects.filter(
                        terminal=terminal,
                        started_at=started_at,
                    ).first()
                    if shift:
                        payment.shift = shift

        payment.save()

    def _import_parked_cart(self, item):
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime

        from pos_app.models import ParkedCart, POSTerminal

        User = get_user_model()

        terminal = POSTerminal.objects.filter(name=item["_terminal_name"]).first()
        if not terminal:
            raise ValueError(f"Terminal not found: {item['_terminal_name']}")

        creator = User.objects.filter(email=item["_created_by_email"]).first()
        if not creator:
            raise ValueError(f"User not found: {item['_created_by_email']}")

        parked_at = parse_datetime(item["_parked_at"]) if item.get("_parked_at") else None

        # Deduplicate
        if (
            parked_at
            and ParkedCart.objects.filter(
                terminal=terminal,
                parked_at=parked_at,
            ).exists()
        ):
            return

        cart = ParkedCart(terminal=terminal, created_by=creator)
        for f in PARKED_CART_FIELDS:
            val = item.get(f)
            if val is not None:
                if f == "total_amount":
                    setattr(cart, f, Decimal(str(val)))
                else:
                    setattr(cart, f, val)

        for dt_field, key in [("restored_at", "_restored_at"), ("expires_at", "_expires_at")]:
            val = item.get(key)
            if val:
                setattr(cart, dt_field, parse_datetime(val))

        cart.save()

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
