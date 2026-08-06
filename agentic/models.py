"""
Agentic commerce settings.

Single-row settings model, following the SearchSettings / BlogSettings /
AffiliateSettings singleton pattern (pk=1, get_settings()). The master switch
defaults OFF: a self-hosted merchant upgrading Spwig must never wake up exposed
to agent traffic on a minor upgrade. Turning it on is a deliberate opt-in, which
is also the near-universal industry default (WooCommerce ships its agentic path
off and hidden; Google gates per-product).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import uuid

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class AgenticSettings(models.Model):
    """Merchant-facing on/off and coarse policy for agentic commerce."""

    # --- Master control -----------------------------------------------------
    is_enabled = models.BooleanField(
        _("Agentic commerce enabled"),
        default=False,
        help_text=_(
            "Master switch. When off, the store exposes no agentic surface at "
            "all — discovery, catalog, and checkout endpoints return 404."
        ),
    )
    # A fast, separate emergency stop, distinct from the configuration toggle
    # above: "stop everything now" is a different action from "reconfigure the
    # feature", and a merchant must be able to hit it without unpicking config.
    kill_switch_engaged = models.BooleanField(
        _("Emergency stop engaged"),
        default=False,
        help_text=_(
            "Immediately halts all agent activity while leaving configuration "
            "intact. Use in a pinch; clear it to resume."
        ),
    )

    # --- Protocol surfaces --------------------------------------------------
    ucp_enabled = models.BooleanField(_("UCP enabled"), default=True)
    acp_enabled = models.BooleanField(_("ACP enabled"), default=False)
    mcp_storefront_enabled = models.BooleanField(_("Storefront MCP enabled"), default=True)

    # --- Access posture -----------------------------------------------------
    # Read (discovery/browse) is lower-stakes than checkout; a merchant can be
    # discoverable without being purchasable. Checkout defaults closed.
    allow_unverified_read = models.BooleanField(_("Allow unverified read"), default=True)
    allow_unverified_checkout = models.BooleanField(_("Allow unverified checkout"), default=False)

    # --- Merchant presentation (falls back to SiteSettings when blank) -------
    merchant_display_name = models.CharField(_("Display name"), max_length=255, blank=True)
    support_url = models.URLField(_("Support URL"), max_length=2048, blank=True)
    terms_url = models.URLField(_("Terms URL"), max_length=2048, blank=True)
    privacy_url = models.URLField(_("Privacy URL"), max_length=2048, blank=True)
    return_policy_url = models.URLField(_("Return policy URL"), max_length=2048, blank=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Agentic Commerce Settings")
        verbose_name_plural = _("Agentic Commerce Settings")

    def __str__(self):
        # str() forces the lazy translation to a real string — Django's admin
        # (and any str() caller) rejects a bare gettext_lazy proxy here.
        return str(_("Agentic Commerce Settings"))

    def save(self, *args, **kwargs):
        # Enforce the singleton — there is only ever one row.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls) -> AgenticSettings:
        """Get or create the singleton settings row."""
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj


class AgentKey(models.Model):
    """
    One of the merchant's OWN signing keys (distinct from a calling agent's).

    Two purposes, two crypto policies, enforced by a database constraint rather
    than a comment: transport keys are Ed25519/OKP (Web Bot Auth interop), AP2
    mandate keys are ECDSA/EC (AP2 v0.2 forbids Ed25519 for the checkout JWT).
    See agentic/identity/keys.py for generation and the RFC 7638 kid.
    """

    PURPOSE_TRANSPORT = "transport"
    PURPOSE_AP2 = "ap2_mandate"
    PURPOSE_CHOICES = [
        (PURPOSE_TRANSPORT, _("Transport signing (Web Bot Auth)")),
        (PURPOSE_AP2, _("AP2 mandate signing")),
    ]

    STATUS_ACTIVE = "active"
    STATUS_ROTATING = "rotating"
    STATUS_RETIRED = "retired"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _("Active")),
        (STATUS_ROTATING, _("Rotating (published, not yet signing)")),
        (STATUS_RETIRED, _("Retired")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purpose = models.CharField(_("Purpose"), max_length=16, choices=PURPOSE_CHOICES)
    kty = models.CharField(_("Key type"), max_length=8)  # "OKP" | "EC"
    alg = models.CharField(_("Algorithm"), max_length=16)  # "EdDSA" | "ES256"
    crv = models.CharField(_("Curve"), max_length=16)  # "Ed25519" | "P-256"
    # RFC 7638 JWK SHA-256 Thumbprint, computed at creation, never user-set.
    kid = models.CharField(_("Key ID"), max_length=64, unique=True)
    public_jwk = models.JSONField(_("Public JWK"), default=dict)
    # Fernet-encrypted PKCS#8 PEM. BinaryField: this is ciphertext, not text.
    private_key_encrypted = models.BinaryField(_("Encrypted private key"))
    status = models.CharField(
        _("Status"), max_length=12, choices=STATUS_CHOICES, default=STATUS_ACTIVE, db_index=True
    )
    activated_at = models.DateTimeField(_("Activated at"), null=True, blank=True)
    retire_after = models.DateTimeField(
        _("Retire after"),
        null=True,
        blank=True,
        help_text=_("A retired key stays published in the JWKS until this time."),
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Agent Signing Key")
        verbose_name_plural = _("Agent Signing Keys")
        indexes = [models.Index(fields=["purpose", "status"])]
        constraints = [
            # The two key policies, made structurally impossible to mix up.
            # Pins the WHOLE crypto tuple, not just kty: a row can only be one
            # of exactly two shapes — transport = OKP/EdDSA/Ed25519, or
            # ap2_mandate = EC/ES256/P-256. AP2 forbids Ed25519 for the checkout
            # JWT, so this is a security invariant, not a preference, and the
            # full-tuple form stops a future direct create() from persisting,
            # say, an AP2 key that claims ES256 but carries an Ed25519 curve.
            models.CheckConstraint(
                name="agentic_agentkey_crypto_policy",
                condition=(
                    models.Q(purpose="transport", kty="OKP", alg="EdDSA", crv="Ed25519")
                    | models.Q(purpose="ap2_mandate", kty="EC", alg="ES256", crv="P-256")
                ),
            ),
        ]

    # JWK members that carry private material and must never appear in the
    # stored public_jwk (EC/OKP `d`, RSA private members, symmetric `k`).
    _PRIVATE_JWK_MEMBERS = frozenset({"d", "p", "q", "dp", "dq", "qi", "k"})

    def clean(self):
        """
        Keep the stored JWK honest about the declared key.

        The DB constraint pins the metadata columns (purpose/kty/alg/crv); this
        guards the material those columns describe: the public_jwk must carry no
        private component, and any kty/crv it does declare must match the row.
        A row could otherwise claim EC/ES256 while carrying Ed25519 JWK bytes,
        and then advertise ap2_mandate for a key that violates AP2's Ed25519 ban.
        """
        from django.core.exceptions import ValidationError

        jwk = self.public_jwk or {}
        leaked = self._PRIVATE_JWK_MEMBERS & set(jwk)
        if leaked:
            raise ValidationError(
                {"public_jwk": f"public_jwk must not contain private members: {sorted(leaked)}"}
            )
        if jwk.get("kty") not in (None, self.kty):
            raise ValidationError({"public_jwk": "public_jwk kty disagrees with the key row"})
        if jwk.get("crv") not in (None, self.crv):
            raise ValidationError({"public_jwk": "public_jwk crv disagrees with the key row"})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.purpose} key {self.kid[:12]}… ({self.status})"


class AgentIdentity(models.Model):
    """
    A CALLING agent — one that signs its requests to this store. Distinct from
    AgentKey (the merchant's own keys): this is the counterparty's identity,
    established by verifying an RFC 9421 HTTP Message Signature.

    Trust-on-first-use: a validly-signed but unknown agent is the COMMON case,
    so seeing one for the first time creates a row here (with a `capped`
    AgentPolicy), it does not reject. The durable identity is the pairing of the
    `Signature-Agent` directory host with the RFC 7638 key thumbprint that
    signed — the *claimed* fields (name/logo/homepage) are attacker-controlled
    and only ever shown marked "as stated by the assistant".
    """

    TRUST_CAPPED = "capped"
    TRUST_VERIFIED = "verified"
    TRUST_BLOCKED = "blocked"
    TRUST_CHOICES = [
        # `capped` — signature verified, limits applied (the safe default).
        (TRUST_CAPPED, _("Capped (verified, limited)")),
        # `verified` — merchant has removed the limits (a deliberate promotion).
        (TRUST_VERIFIED, _("Verified (limits removed)")),
        # `blocked` — merchant has cut this agent off.
        (TRUST_BLOCKED, _("Blocked")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # --- Verified identity (durable, cryptographic) -------------------------
    # The Signature-Agent directory host, e.g. "agent.example.com". The only
    # part of the identity that is both durable and attacker-resistant.
    directory = models.CharField(_("Directory host"), max_length=255, db_index=True)
    # RFC 7638 JWK SHA-256 Thumbprint of the key that signed.
    key_thumbprint = models.CharField(_("Key thumbprint"), max_length=64, db_index=True)
    algorithm = models.CharField(_("Algorithm"), max_length=32)  # RFC 9421 alg id
    # The resolved public key (cached from the agent's directory JWKS).
    public_jwk = models.JSONField(_("Public JWK"), default=dict)

    # --- Claimed presentation (UNTRUSTED — display only, never a gate) -------
    claimed_name = models.CharField(_("Claimed name"), max_length=255, blank=True)
    claimed_logo_url = models.URLField(_("Claimed logo URL"), max_length=2048, blank=True)
    claimed_homepage = models.URLField(_("Claimed homepage"), max_length=2048, blank=True)

    # --- Trust posture ------------------------------------------------------
    trust_state = models.CharField(
        _("Trust state"),
        max_length=12,
        choices=TRUST_CHOICES,
        default=TRUST_CAPPED,
        db_index=True,
    )
    blocked_reason = models.TextField(_("Blocked reason"), blank=True)
    blocked_at = models.DateTimeField(_("Blocked at"), null=True, blank=True)

    first_seen_at = models.DateTimeField(_("First seen"), auto_now_add=True)
    last_seen_at = models.DateTimeField(_("Last seen"), auto_now=True)
    request_count = models.PositiveBigIntegerField(_("Requests seen"), default=0)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Agent Identity")
        verbose_name_plural = _("Agent Identities")
        constraints = [
            # One identity per (directory, key) pairing — the durable identity.
            models.UniqueConstraint(
                fields=["directory", "key_thumbprint"],
                name="agentic_agentidentity_directory_key",
            ),
        ]
        indexes = [models.Index(fields=["trust_state", "directory"])]

    def __str__(self):
        label = self.claimed_name or self.directory
        return f"{label} <{self.directory}> ({self.trust_state})"

    @property
    def is_blocked(self) -> bool:
        return self.trust_state == self.TRUST_BLOCKED


class AgentPolicy(models.Model):
    """
    What a calling agent is allowed to do. One per AgentIdentity.

    The default is deliberately `capped`: order-value and daily caps set, and
    the higher-risk tenders/goods switched off. A merchant lifts these by
    promoting the agent (which nulls the caps) — never auto-promoted. Nothing
    here is ENFORCED until checkout (Phase 4); this phase only records identity
    and holds the policy the checkout path will read.
    """

    agent = models.OneToOneField(
        AgentIdentity,
        on_delete=models.CASCADE,
        related_name="policy",
        verbose_name=_("Agent"),
    )

    # Caps. NULL means "no cap" (a promoted/verified agent). A capped agent has
    # concrete amounts, populated from store defaults at trust-on-first-use.
    max_order_amount = MoneyField(
        _("Max order value"),
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
    )
    daily_spend_cap = MoneyField(
        _("Daily spend cap"),
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
    )

    # Higher-risk capabilities, off by default under `capped`.
    allow_discount_codes = models.BooleanField(_("Allow discount codes"), default=False)
    allow_gift_cards = models.BooleanField(_("Allow gift cards"), default=False)
    allow_digital_goods = models.BooleanField(_("Allow digital goods"), default=False)

    rate_limit_per_minute = models.PositiveIntegerField(_("Rate limit (per minute)"), default=60)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Agent Policy")
        verbose_name_plural = _("Agent Policies")

    def __str__(self):
        return f"Policy for {self.agent_id}"


class AgentEvent(models.Model):
    """
    A deliberately SEPARATE, append-only, hash-chained audit log for agent
    activity.

    This is not redundant with AdminAPIAuditLog — that log is mutable,
    unchained, admin-user-scoped, and hard-deletes at 90 days
    (admin_api/models.py). Card-scheme dispute windows outlast that, and an
    agent's request is not an admin user's action. So: rows here cannot be
    updated or deleted (both raise), and each row carries the SHA-256 of the
    previous row, so any excision or edit is detectable. If someone proposes
    "consolidating" the two logs, this docstring is why they should not.
    """

    EVENT_SIG_VERIFIED = "sig_verified"
    EVENT_SIG_FAILED = "sig_failed"
    EVENT_AGENT_SEEN = "agent_seen"
    EVENT_AGENT_BLOCKED = "agent_blocked"
    EVENT_AGENT_UNBLOCKED = "agent_unblocked"
    EVENT_POLICY_CHANGED = "policy_changed"
    EVENT_CHOICES = [
        (EVENT_SIG_VERIFIED, _("Signature verified")),
        (EVENT_SIG_FAILED, _("Signature verification failed")),
        (EVENT_AGENT_SEEN, _("Agent seen (first use)")),
        (EVENT_AGENT_BLOCKED, _("Agent blocked")),
        (EVENT_AGENT_UNBLOCKED, _("Agent unblocked")),
        (EVENT_POLICY_CHANGED, _("Policy changed")),
    ]

    _GENESIS_HASH = "0" * 64

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Monotonic position in the chain. Assigned under a lock in append().
    chain_index = models.PositiveBigIntegerField(_("Chain index"), unique=True, editable=False)

    # The agent may be null: a failed-signature event has no established
    # identity, but we still record the attempt (with its denormalized origin).
    agent = models.ForeignKey(
        AgentIdentity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        verbose_name=_("Agent"),
    )
    event_type = models.CharField(
        _("Event type"), max_length=24, choices=EVENT_CHOICES, db_index=True
    )
    # Denormalized origin so an event survives its agent row being nulled.
    directory = models.CharField(_("Directory host"), max_length=255, blank=True)
    key_thumbprint = models.CharField(_("Key thumbprint"), max_length=64, blank=True)
    # Structured, secret-free context (method, path, failure reason, …).
    detail = models.JSONField(_("Detail"), default=dict)

    created_at = models.DateTimeField(_("Created at"), db_index=True)
    prev_hash = models.CharField(_("Previous hash"), max_length=64, editable=False)
    entry_hash = models.CharField(_("Entry hash"), max_length=64, unique=True, editable=False)

    class Meta:
        verbose_name = _("Agent Event")
        verbose_name_plural = _("Agent Events")
        ordering = ["chain_index"]
        indexes = [models.Index(fields=["event_type", "created_at"])]

    def __str__(self):
        return f"#{self.chain_index} {self.event_type} @ {self.created_at:%Y-%m-%d %H:%M:%S}"

    # --- Append-only enforcement -------------------------------------------
    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValueError("AgentEvent is append-only; existing rows cannot be modified.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("AgentEvent is append-only; rows cannot be deleted.")

    @staticmethod
    def _payload(event_type, directory, key_thumbprint, detail, created_at) -> dict:
        """
        The integrity-covered content of one event.

        Deliberately EXCLUDES the agent FK: `agent` is `SET_NULL`, so it can
        change after the row is written (if the identity is later deleted) and
        must not be part of the hash, or deleting an agent would break the whole
        downstream chain. The origin is captured durably by the denormalized
        `directory` / `key_thumbprint`, which are copied at append time and
        never mutate.
        """
        return {
            "event_type": event_type,
            "directory": directory,
            "key_thumbprint": key_thumbprint,
            "detail": detail,
            "created_at": created_at.isoformat(),
        }

    @staticmethod
    def _chain_key() -> bytes:
        """HMAC key for the chain, derived from SECRET_KEY (domain-separated)."""
        from django.conf import settings

        return hashlib.sha256(b"agentic-event-chain:" + settings.SECRET_KEY.encode()).digest()

    @classmethod
    def _compute_hash(cls, chain_index: int, prev_hash: str, payload: dict) -> str:
        # KEYED with SECRET_KEY (HMAC), not a bare SHA-256: an attacker who
        # reaches the database cannot recompute a consistent chain over forged
        # rows without also holding the secret, so the chain is tamper-evident
        # rather than merely tamper-detectable-by-anyone. Caveat: rotating
        # SECRET_KEY invalidates verify_chain() for pre-rotation rows (same
        # trade-off as the Fernet-encrypted signing keys).
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        material = f"{chain_index}\n{prev_hash}\n{canonical}".encode()
        return hmac.new(cls._chain_key(), material, hashlib.sha256).hexdigest()

    @classmethod
    def append(
        cls,
        event_type: str,
        *,
        agent: AgentIdentity | None = None,
        directory: str = "",
        key_thumbprint: str = "",
        detail: dict | None = None,
    ) -> AgentEvent:
        """
        Append one row to the chain, atomically.

        The AgenticSettings singleton row is locked for the duration, which
        serialises concurrent appends so two events can never claim the same
        chain_index or fork the hash chain.
        """
        detail = detail or {}
        with transaction.atomic():
            # Lock the singleton as the chain mutex — one writer at a time.
            AgenticSettings.objects.select_for_update().get_or_create(pk=1)
            last = cls.objects.order_by("-chain_index").first()
            prev_hash = last.entry_hash if last else cls._GENESIS_HASH
            chain_index = (last.chain_index + 1) if last else 1
            now = timezone.now()
            resolved_directory = directory or (agent.directory if agent else "")
            resolved_kid = key_thumbprint or (agent.key_thumbprint if agent else "")
            payload = cls._payload(event_type, resolved_directory, resolved_kid, detail, now)
            entry_hash = cls._compute_hash(chain_index, prev_hash, payload)
            return cls.objects.create(
                chain_index=chain_index,
                agent=agent,
                event_type=event_type,
                directory=resolved_directory,
                key_thumbprint=resolved_kid,
                detail=detail,
                created_at=now,
                prev_hash=prev_hash,
                entry_hash=entry_hash,
            )

    @classmethod
    def verify_chain(cls) -> bool:
        """Recompute every link; return True iff the chain is intact."""
        prev_hash = cls._GENESIS_HASH
        for ev in cls.objects.order_by("chain_index"):
            payload = cls._payload(
                ev.event_type, ev.directory, ev.key_thumbprint, ev.detail, ev.created_at
            )
            expected = cls._compute_hash(ev.chain_index, prev_hash, payload)
            if ev.prev_hash != prev_hash or ev.entry_hash != expected:
                return False
            prev_hash = ev.entry_hash
        return True


class Mandate(models.Model):
    """
    An AP2 payment/checkout mandate the store issued (an SD-JWT).

    This is durable evidence: it attests, under the merchant's own signature,
    exactly what an agent-placed order was authorised to charge. It therefore
    lives in its own model with a long retention and a `delete()` that raises —
    a card-scheme dispute can arrive well over a year later, and the mandate is
    the artifact that settles it. The stored `attested_amount` is the gateway
    leg (`amount_due`); agent orders are gateway-only, which keeps that figure
    equal to the order total and the attestation honest.
    """

    # AP2 v0.2 keeps mandates recoverable for disputes; 540 days comfortably
    # outlasts card-scheme windows (unlike AdminAPIAuditLog's 90-day purge).
    RETENTION_DAYS = 540

    TYPE_CHECKOUT = "checkout"
    TYPE_PAYMENT = "payment"
    TYPE_CHOICES = [
        (TYPE_CHECKOUT, _("Checkout mandate")),
        (TYPE_PAYMENT, _("Payment mandate")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mandate_type = models.CharField(
        _("Type"), max_length=16, choices=TYPE_CHOICES, default=TYPE_CHECKOUT
    )
    # Where it came from. Both nullable so the mandate outlives its order/agent.
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agentic_mandates",
        verbose_name=_("Order"),
    )
    agent = models.ForeignKey(
        AgentIdentity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mandates",
        verbose_name=_("Agent"),
    )
    ucp_checkout_id = models.CharField(
        _("UCP checkout id"), max_length=64, blank=True, db_index=True
    )

    # The signing key + algorithm (the AP2 ECDSA key's RFC 7638 thumbprint).
    kid = models.CharField(_("Key ID"), max_length=64)
    alg = models.CharField(_("Algorithm"), max_length=8)  # ES256 | ES384 | ES512

    attested_amount = MoneyField(
        _("Attested amount"), max_digits=12, decimal_places=2, default_currency="USD"
    )
    # The signed SD-JWT and the SHA-256 of the canonical (JCS) mandate payload,
    # so the exact attested content is verifiable without re-parsing the JWT.
    sd_jwt = models.TextField(_("SD-JWT"))
    payload_sha256 = models.CharField(_("Payload SHA-256"), max_length=64)

    issued_at = models.DateTimeField(_("Issued at"))
    expires_at = models.DateTimeField(_("Expires at"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Agent Mandate")
        verbose_name_plural = _("Agent Mandates")
        ordering = ["-issued_at"]
        indexes = [models.Index(fields=["mandate_type", "issued_at"])]

    def __str__(self):
        return f"{self.mandate_type} mandate {str(self.id)[:8]} ({self.attested_amount})"

    def delete(self, *args, **kwargs):
        # Evidence: mandates are never deleted through the ORM/admin. A retention
        # sweep, if ever built, must be a deliberate, separate, audited path.
        raise ValueError("Mandates are retained evidence and cannot be deleted.")
