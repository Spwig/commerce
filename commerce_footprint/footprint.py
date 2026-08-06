"""
The ``Footprint`` dataclass and its assertion helpers.

Django-free by design (see package docstring). Records hold *primitive*
snapshots — Decimals and strings, never live model instances — so an HTTP
backend reconstructing a footprint from JSON produces byte-identical objects
and the assertions below run unchanged against either backend.

Money is represented as :class:`Amount` (a Decimal + an ISO currency code)
rather than a djmoney ``Money`` so this module has no third-party dependency.
Comparisons use a 1-cent tolerance, matching ``tests/helpers.assert_totals``.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from decimal import Decimal

_MONEY_TOLERANCE = Decimal("0.01")

# Payment records that represent money actually taken from the customer via an
# external gateway (as opposed to authorises, voids, or internal tenders).
_CAPTURE_TYPES = frozenset({"charge", "capture"})
_REFUND_TYPES = frozenset({"refund"})
_COMPLETED = "completed"
# Order.payment_status values that mean money was collected at some point —
# includes the refunded states, because "refunded" means money came in and
# then went back out, which still fails "a failed payment never creates a paid
# order". Everything outside this set (unpaid / pending / failed) is
# money-never-collected.
_MONEY_COLLECTED_STATUSES = frozenset({"paid", "partially_paid", "refunded", "partially_refunded"})


def _dump(obj):
    """Recursively serialise a footprint record graph to JSON-safe primitives.

    ``Amount`` is checked before the generic dataclass branch because it *is* a
    dataclass — its ``value`` is a Decimal that must become a string, not a
    nested ``{value, currency}`` of raw Decimals JSON can't encode.
    """
    if isinstance(obj, Amount):
        return obj.as_dict()
    if is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: _dump(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, (tuple, list)):
        return [_dump(x) for x in obj]
    return obj


@dataclass(frozen=True, slots=True)
class Amount:
    """A money value: a quantised Decimal plus an ISO-4217 currency code."""

    value: Decimal
    currency: str = "USD"

    def __post_init__(self):
        # Normalise so 5 == 5.00 and string/int inputs are accepted.
        object.__setattr__(self, "value", Decimal(str(self.value)).quantize(Decimal("0.01")))

    def __add__(self, other: Amount) -> Amount:
        self._assert_same_currency(other)
        return Amount(self.value + other.value, self.currency)

    def close_to(self, other: Amount, tolerance: Decimal = _MONEY_TOLERANCE) -> bool:
        return self.currency == other.currency and abs(self.value - other.value) <= tolerance

    def _assert_same_currency(self, other: Amount) -> None:
        if self.currency != other.currency:
            raise AssertionError(
                f"currency mismatch: {self.currency} vs {other.currency} — "
                "gift cards/vouchers redeem only in the issued currency, so a "
                "cross-currency sum here is itself a bug"
            )

    def as_dict(self) -> dict:
        """JSON-safe form. ``value`` is a *string* so the Decimal survives the
        JSON round-trip exactly (a float would lose cents)."""
        return {"value": str(self.value), "currency": self.currency}

    @classmethod
    def from_dict(cls, data: dict) -> Amount:
        # __post_init__ re-quantises, so a string value is accepted as-is.
        return cls(data["value"], data["currency"])

    def __str__(self) -> str:  # pragma: no cover - display only
        return f"{self.value} {self.currency}"


@dataclass(frozen=True, slots=True)
class BookingLineRecord:
    """The booking a booking-product line reserved (from the ``Booking`` row
    linked to the order item). Empty on non-booking lines."""

    start: str = ""  # ISO datetime
    end: str = ""
    resource_id: int | None = None
    persons: tuple[tuple[str, int], ...] = ()  # (person_type, count) — hashable
    status: str = ""


@dataclass(frozen=True, slots=True)
class OrderLineRecord:
    sku: str
    name: str
    quantity: int
    unit_price: Amount
    line_total: Amount
    # Type-specific purchase details — all empty/None on a plain simple line, so
    # they don't disturb existing assertions. Collections are tuples (hashable),
    # so an OrderLineRecord stays a frozen, JSON-round-trippable value.
    variant_sku: str = ""
    is_bundle_component: bool = False
    # {slot_id: [option_ids]} as a sorted tuple of (slot, (options,)) — configurable.
    configuration: tuple[tuple[str, tuple[str, ...]], ...] = ()
    customization_token: str = ""  # customizable: the Fabric design-editor token
    # customizable (option path): sorted (option_id, value) — the CustomizationOption
    # values chosen (text engraving, dropdown, …), excluding _design/_configuration.
    customizations: tuple[tuple[str, str], ...] = ()
    gift_card_recipient: str = ""  # gift_card product: recipient email
    booking: BookingLineRecord | None = None


@dataclass(frozen=True, slots=True)
class OrderRecord:
    number: str
    email: str
    status: str
    payment_status: str
    subtotal: Amount
    tax: Amount
    shipping: Amount
    discount: Amount
    gift_card_discount: Amount
    total: Amount
    amount_paid: Amount
    amount_refunded: Amount
    lines: tuple[OrderLineRecord, ...] = ()


@dataclass(frozen=True, slots=True)
class PaymentRecord:
    reference: str  # transaction_id (internal, stable)
    transaction_type: str  # charge | authorize | capture | void | refund
    tender_type: str  # gateway | gift_card | wallet | cash | ...
    status: str  # pending | ... | completed | refunded | ...
    amount: Amount
    provider_transaction_id: str = ""


@dataclass(frozen=True, slots=True)
class IntentRecord:
    reference: str  # provider_intent_id
    status: str  # created | requires_action | processing | succeeded | ...
    amount: Amount


@dataclass(frozen=True, slots=True)
class StockMovementRecord:
    stock_item_id: int
    movement_type: str  # allocation | fulfillment | return | adjustment | ...
    quantity: int  # signed
    previous_quantity: int
    new_quantity: int
    reference_key: str | None = None


@dataclass(frozen=True, slots=True)
class GiftCardEventRecord:
    gift_card_code: str
    transaction_type: str  # issue | redemption | refund | adjustment | expiration
    amount: Amount
    balance_after: Amount


@dataclass(frozen=True, slots=True)
class VoucherUsageRecord:
    voucher_code: str
    discount_amount: Amount
    cart_total: Amount


@dataclass(frozen=True, slots=True)
class EmailRecord:
    to_email: str
    template_type: str
    subject: str
    status: str
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class WebhookRecord:
    provider_slug: str
    event_id: str
    event_type: str
    processed: bool


@dataclass(frozen=True, slots=True)
class StockStateRecord:
    """A *point-in-time snapshot* of a StockItem's counters, not a ledger row.

    The checkout path tracks allocation on ``StockItem.allocated`` /
    ``on_hand`` and writes **no** ``StockMovement`` ledger row for
    allocate/fulfill/release (only manual adjustments and admin actions do).
    So the honest oracle for "was stock deducted correctly / not twice" reads
    these counters, snapshotted per stock item the order touches. Compare two
    footprints (before/after) to get deltas.
    """

    stock_item_id: int
    on_hand: int
    allocated: int
    available: int


@dataclass(frozen=True, slots=True)
class Footprint:
    """The complete financial/operational record of one transaction.

    ``correlation`` names what the footprint was gathered around (an order
    number, for the ORM backend). ``emails`` and ``webhooks`` are correlated
    on a best-effort basis (recipient / provider ids) because neither model
    carries a hard order FK — see ``orm_backend`` for the exact basis.

    ``stock_state`` is a snapshot of counters (see ``StockStateRecord``), not a
    mutable side effect — it is deliberately excluded from
    ``side_effect_counts``; inventory correctness is asserted via before/after
    deltas, not by counting rows.
    """

    correlation: str
    orders: tuple[OrderRecord, ...] = ()
    payments: tuple[PaymentRecord, ...] = ()
    intents: tuple[IntentRecord, ...] = ()
    stock_movements: tuple[StockMovementRecord, ...] = ()
    stock_state: tuple[StockStateRecord, ...] = ()
    gift_card_events: tuple[GiftCardEventRecord, ...] = ()
    voucher_usages: tuple[VoucherUsageRecord, ...] = ()
    emails: tuple[EmailRecord, ...] = ()
    webhooks: tuple[WebhookRecord, ...] = ()

    def side_effect_counts(self) -> dict[str, int]:
        """Count of each mutable side effect — the basis for replay checks.

        ``webhooks`` is included so a replay test can *see* the duplicate
        delivery row (which legitimately grows) and pass ``ignore=("webhooks",)``
        to ``assert_same_side_effects`` — without it here, that ignore key
        would be a silent no-op. ``stock_state`` is intentionally absent (it's
        a snapshot, not a count)."""
        return {
            "orders": len(self.orders),
            "payments": len(self.payments),
            "intents": len(self.intents),
            "stock_movements": len(self.stock_movements),
            "gift_card_events": len(self.gift_card_events),
            "voucher_usages": len(self.voucher_usages),
            "emails": len(self.emails),
            "webhooks": len(self.webhooks),
        }

    def allocated_by_stock_item(self) -> dict[int, int]:
        """Currently-allocated units per stock item, from the counters."""
        return {s.stock_item_id: s.allocated for s in self.stock_state}

    def on_hand_by_stock_item(self) -> dict[int, int]:
        """Current on-hand units per stock item, from the counters."""
        return {s.stock_item_id: s.on_hand for s in self.stock_state}

    # -- JSON contract (shared by the /api/e2e/inspect endpoint and HttpBackend) --

    def to_dict(self) -> dict:
        """Serialise to a JSON-safe dict. Generic over the dataclass fields so a
        newly added field can't silently drop out of the wire form — the write
        side never drifts from the schema. ``from_dict`` is the one place that
        must be kept in step when fields change."""
        return _dump(self)

    @classmethod
    def from_dict(cls, data: dict) -> Footprint:
        """Rebuild a Footprint from :meth:`to_dict` output — byte-identical to an
        ORM-built one, so the same assertions run against either backend.

        Every top-level collection key is *required* (``to_dict`` always emits
        all of them). A payload missing one raises ``KeyError`` rather than
        yielding a silently-empty footprint — so a truncated/partial response
        from the endpoint fails loudly at the contract boundary instead of
        passing an assertion vacuously. Per-record optional fields
        (``reference_key``, ``provider_transaction_id``, ``tags``, ``lines``)
        stay lenient, matching their dataclass defaults."""
        A = Amount.from_dict
        return cls(
            correlation=data["correlation"],
            orders=tuple(
                OrderRecord(
                    number=o["number"],
                    email=o["email"],
                    status=o["status"],
                    payment_status=o["payment_status"],
                    subtotal=A(o["subtotal"]),
                    tax=A(o["tax"]),
                    shipping=A(o["shipping"]),
                    discount=A(o["discount"]),
                    gift_card_discount=A(o["gift_card_discount"]),
                    total=A(o["total"]),
                    amount_paid=A(o["amount_paid"]),
                    amount_refunded=A(o["amount_refunded"]),
                    lines=tuple(
                        OrderLineRecord(
                            sku=line["sku"],
                            name=line["name"],
                            quantity=line["quantity"],
                            unit_price=A(line["unit_price"]),
                            line_total=A(line["line_total"]),
                            variant_sku=line.get("variant_sku", ""),
                            is_bundle_component=line.get("is_bundle_component", False),
                            configuration=tuple(
                                (slot, tuple(opts)) for slot, opts in line.get("configuration", [])
                            ),
                            customization_token=line.get("customization_token", ""),
                            customizations=tuple(
                                (opt, val) for opt, val in line.get("customizations", [])
                            ),
                            gift_card_recipient=line.get("gift_card_recipient", ""),
                            booking=(
                                BookingLineRecord(
                                    start=_b.get("start", ""),
                                    end=_b.get("end", ""),
                                    resource_id=_b.get("resource_id"),
                                    persons=tuple((t, c) for t, c in _b.get("persons", [])),
                                    status=_b.get("status", ""),
                                )
                                if (_b := line.get("booking"))
                                else None
                            ),
                        )
                        for line in o.get("lines", [])
                    ),
                )
                for o in data["orders"]
            ),
            payments=tuple(
                PaymentRecord(
                    reference=p["reference"],
                    transaction_type=p["transaction_type"],
                    tender_type=p["tender_type"],
                    status=p["status"],
                    amount=A(p["amount"]),
                    provider_transaction_id=p.get("provider_transaction_id", ""),
                )
                for p in data["payments"]
            ),
            intents=tuple(
                IntentRecord(reference=i["reference"], status=i["status"], amount=A(i["amount"]))
                for i in data["intents"]
            ),
            stock_movements=tuple(
                StockMovementRecord(
                    stock_item_id=m["stock_item_id"],
                    movement_type=m["movement_type"],
                    quantity=m["quantity"],
                    previous_quantity=m["previous_quantity"],
                    new_quantity=m["new_quantity"],
                    reference_key=m.get("reference_key"),
                )
                for m in data["stock_movements"]
            ),
            stock_state=tuple(
                StockStateRecord(
                    stock_item_id=s["stock_item_id"],
                    on_hand=s["on_hand"],
                    allocated=s["allocated"],
                    available=s["available"],
                )
                for s in data["stock_state"]
            ),
            gift_card_events=tuple(
                GiftCardEventRecord(
                    gift_card_code=g["gift_card_code"],
                    transaction_type=g["transaction_type"],
                    amount=A(g["amount"]),
                    balance_after=A(g["balance_after"]),
                )
                for g in data["gift_card_events"]
            ),
            voucher_usages=tuple(
                VoucherUsageRecord(
                    voucher_code=v["voucher_code"],
                    discount_amount=A(v["discount_amount"]),
                    cart_total=A(v["cart_total"]),
                )
                for v in data["voucher_usages"]
            ),
            emails=tuple(
                EmailRecord(
                    to_email=e["to_email"],
                    template_type=e["template_type"],
                    subject=e["subject"],
                    status=e["status"],
                    tags=tuple(e.get("tags", [])),
                )
                for e in data["emails"]
            ),
            webhooks=tuple(
                WebhookRecord(
                    provider_slug=w["provider_slug"],
                    event_id=w["event_id"],
                    event_type=w["event_type"],
                    processed=w["processed"],
                )
                for w in data["webhooks"]
            ),
        )


# ---------------------------------------------------------------------------
# Assertion helpers — shared by tests/domain, tests/invariants, and (later)
# the standalone live/cert repo. Each raises AssertionError with a message
# that names the actual footprint so a failure is diagnosable on its own.
# ---------------------------------------------------------------------------


def assert_exactly_one_order(fp: Footprint) -> OrderRecord:
    """Invariant #1: a completed transaction produces exactly one order."""
    if len(fp.orders) != 1:
        raise AssertionError(
            f"expected exactly 1 order for {fp.correlation!r}, found "
            f"{len(fp.orders)}: {[o.number for o in fp.orders]}"
        )
    return fp.orders[0]


def assert_no_paid_order(fp: Footprint) -> None:
    """Invariant #2: a failed/abandoned transaction leaves no paid order."""
    paid = [o for o in fp.orders if o.payment_status in _MONEY_COLLECTED_STATUSES]
    if paid:
        raise AssertionError(
            f"expected no paid order for {fp.correlation!r}, but "
            f"{[o.number for o in paid]} are {[o.payment_status for o in paid]}"
        )
    captured = total_captured(fp)
    if captured is not None and captured.value > 0:
        raise AssertionError(
            f"expected no gateway capture for {fp.correlation!r}, but captured {captured}"
        )


def total_captured(fp: Footprint, tender: str = "gateway") -> Amount | None:
    """Sum of *completed* gateway charges/captures (what the customer was
    actually charged). Returns ``None`` when there are no such payments."""
    caps = [
        p
        for p in fp.payments
        if p.tender_type == tender
        and p.transaction_type in _CAPTURE_TYPES
        and p.status == _COMPLETED
    ]
    if not caps:
        return None
    out = caps[0].amount
    for p in caps[1:]:
        out = out + p.amount
    return out


def total_refunded(fp: Footprint) -> Amount | None:
    """Sum of *completed* refund payment records."""
    refunds = [
        p for p in fp.payments if p.transaction_type in _REFUND_TYPES and p.status == _COMPLETED
    ]
    if not refunds:
        return None
    out = refunds[0].amount
    for p in refunds[1:]:
        out = out + p.amount
    return out


def assert_charged_equals(fp: Footprint, expected: Amount) -> None:
    """Invariant #3: the amount actually captured equals the authoritative
    server-side figure the test computed independently."""
    captured = total_captured(fp)
    if captured is None:
        raise AssertionError(
            f"expected a gateway capture of {expected} for {fp.correlation!r}, "
            "but no completed gateway charge/capture exists"
        )
    if not captured.close_to(expected):
        raise AssertionError(f"captured {captured} != expected {expected} for {fp.correlation!r}")


def net_ledger_movement_by_stock_item(
    fp: Footprint, *, movement_type: str | None = None
) -> dict[int, int]:
    """Net **signed** quantity of ledger movements per stock item.

    Reads ``StockMovement`` rows and sums their signed ``quantity`` (NOT
    ``abs()`` — a +2 then a -2 nets to 0, as it should). Optionally filter by
    ``movement_type``.

    IMPORTANT: the storefront checkout path (allocate/fulfill/release in
    ``catalog.services.fulfillment``) writes **no** ledger rows — it mutates
    the ``StockItem`` counters directly. Only manual adjustments, admin
    actions and imports hit this ledger. So for the "no double deduction"
    invariant on a *checkout*, assert on ``Footprint.allocated_by_stock_item``
    (the counters); use this helper for flows that genuinely write movements
    (stock adjustments, admin fulfilment).
    """
    out: dict[int, int] = {}
    for m in fp.stock_movements:
        if movement_type is not None and m.movement_type != movement_type:
            continue
        out[m.stock_item_id] = out.get(m.stock_item_id, 0) + m.quantity
    return out


def assert_no_duplicate_reference_keys(fp: Footprint) -> None:
    """Invariant #4/#6 support: no two stock movements share an idempotency
    ``reference_key`` — a duplicate means a retry deducted twice."""
    seen: set[str] = set()
    for m in fp.stock_movements:
        if not m.reference_key:
            continue
        if m.reference_key in seen:
            raise AssertionError(
                f"duplicate stock-movement reference_key {m.reference_key!r} for "
                f"{fp.correlation!r} — a retried operation deducted stock twice"
            )
        seen.add(m.reference_key)


def assert_refund_reconciles(fp: Footprint) -> None:
    """Invariant #8: the order's recorded ``amount_refunded`` equals the sum of
    completed refund payment records."""
    order = assert_exactly_one_order(fp)
    ledger = total_refunded(fp) or Amount(Decimal("0"), order.amount_refunded.currency)
    if not order.amount_refunded.close_to(ledger):
        raise AssertionError(
            f"order {order.number} records amount_refunded={order.amount_refunded} but "
            f"refund transactions sum to {ledger}"
        )


def count_emails(fp: Footprint, *, template_type: str | None = None, to: str | None = None) -> int:
    """Count emails in the footprint, optionally filtered by template/recipient."""
    return sum(
        1
        for e in fp.emails
        if (template_type is None or e.template_type == template_type)
        and (to is None or e.to_email == to)
    )


def assert_same_side_effects(
    before: Footprint, after: Footprint, *, ignore: tuple[str, ...] = ()
) -> None:
    """Invariant #6: replaying a duplicate event produces no new side effects.

    Compare the side-effect counts of a footprint taken before a duplicate
    webhook/redelivery against one taken after. Only an **increase** is a
    double-effect bug — a decrease (e.g. a cleanup) is not what this invariant
    guards, so it is not flagged. ``ignore`` skips categories a test knows
    legitimately grow (e.g. ``webhooks`` — the duplicate delivery *is*
    recorded as a row, it just must not act twice)."""
    b, a = before.side_effect_counts(), after.side_effect_counts()
    grown = {k: (b[k], a[k]) for k in b if k not in ignore and a[k] > b[k]}
    if grown:
        raise AssertionError(
            f"replay created new side effects for {after.correlation!r} "
            "(a duplicate event acted twice): "
            + ", ".join(f"{k} {v0}->{v1}" for k, (v0, v1) in grown.items())
        )


# ---------------------------------------------------------------------------
# Line-level assertions — prove the RIGHT thing was bought, not just that a line
# exists. Shared by both tiers (ORM in-repo, HTTP from the cert host).
# ---------------------------------------------------------------------------


def line_by_sku(fp: Footprint, sku: str) -> OrderLineRecord:
    """The single order line with this sku (across the footprint's one order)."""
    lines = [line for o in fp.orders for line in o.lines if line.sku == sku]
    if len(lines) != 1:
        raise AssertionError(
            f"expected exactly 1 line with sku {sku!r} for {fp.correlation!r}, "
            f"found {len(lines)}: {[(o.number, [line.sku for line in o.lines]) for o in fp.orders]}"
        )
    return lines[0]


def assert_line_variant(fp: Footprint, sku: str, variant_sku: str) -> None:
    """The line for ``sku`` bought exactly the variant ``variant_sku`` (variable)."""
    line = line_by_sku(fp, sku)
    if line.variant_sku != variant_sku:
        raise AssertionError(
            f"line {sku!r} bought variant {line.variant_sku!r}, expected {variant_sku!r}"
        )


def assert_line_configuration(fp: Footprint, sku: str, expected: dict[str, list[str]]) -> None:
    """The configurable line recorded exactly ``expected`` (slot -> option ids)."""
    line = line_by_sku(fp, sku)
    got = {slot: list(opts) for slot, opts in line.configuration}
    want = {str(slot): [str(o) for o in opts] for slot, opts in expected.items()}
    if got != want:
        raise AssertionError(f"line {sku!r} configuration {got} != expected {want}")


def assert_line_customized(fp: Footprint, sku: str) -> None:
    """The customizable line carries a design token (Fabric design-editor path)."""
    line = line_by_sku(fp, sku)
    if not line.customization_token:
        raise AssertionError(f"line {sku!r} has no customization/design token")


def assert_line_customization(
    fp: Footprint, sku: str, value: str, *, option: str | None = None
) -> None:
    """The customizable line recorded a CustomizationOption value (text/dropdown
    path). Asserts ``value`` appears among the line's customizations — optionally
    for a specific ``option`` id."""
    line = line_by_sku(fp, sku)
    pairs = [(o, v) for o, v in line.customizations if option is None or o == str(option)]
    if not any(v == value for _, v in pairs):
        raise AssertionError(
            f"line {sku!r} customization value {value!r} not found in {line.customizations}"
        )


def assert_line_gift_card_recipient(fp: Footprint, sku: str, recipient: str) -> None:
    """The gift-card *product* line recorded the recipient email it was bought for."""
    line = line_by_sku(fp, sku)
    if line.gift_card_recipient != recipient:
        raise AssertionError(
            f"line {sku!r} gift-card recipient {line.gift_card_recipient!r}, expected {recipient!r}"
        )


def assert_line_booking(
    fp: Footprint, sku: str, *, resource_id: int | None = None, status: str | None = None
) -> BookingLineRecord:
    """The booking line reserved a slot; optionally assert resource/status. Returns
    the BookingLineRecord so a caller can check start/end/persons."""
    line = line_by_sku(fp, sku)
    if line.booking is None:
        raise AssertionError(f"line {sku!r} has no booking reservation")
    b = line.booking
    if not (b.start and b.end):
        raise AssertionError(f"line {sku!r} booking has no start/end: {b}")
    if resource_id is not None and b.resource_id != resource_id:
        raise AssertionError(
            f"line {sku!r} booking resource {b.resource_id}, expected {resource_id}"
        )
    if status is not None and b.status != status:
        raise AssertionError(f"line {sku!r} booking status {b.status!r}, expected {status!r}")
    return b


def assert_bundle_components(fp: Footprint, parent_sku: str, component_skus: set[str]) -> None:
    """A bundle purchase produced the parent line plus its component lines."""
    order = assert_exactly_one_order(fp)
    skus = {line.sku for line in order.lines}
    if parent_sku not in skus:
        raise AssertionError(f"bundle parent {parent_sku!r} not in order lines {skus}")
    missing = component_skus - skus
    if missing:
        raise AssertionError(
            f"bundle {parent_sku!r} missing component lines {missing} (have {skus})"
        )
    components = [line for line in order.lines if line.is_bundle_component]
    if not components:
        raise AssertionError(f"no lines flagged is_bundle_component for bundle {parent_sku!r}")
