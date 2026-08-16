"""
Issue AP2 Checkout Mandates for agent-placed orders.

A Checkout Mandate is the merchant's signed attestation of what an order was
authorised to charge — the AP2 `merchant_authorization`. It is issued with the
merchant's OWN ECDSA (AP2) key, so a payment network can verify it against the
JWKS the store already publishes at `/.well-known/ucp`.

Design boundaries (same discipline as the rest of `agentic/`):

- The attested amount is `amount_due` — the gateway leg. Agent orders are
  gateway-only, so that equals the order total.
- No key material or signing logic lives here; it delegates to
  `agentic.identity.sdjwt` (SD-JWT) and `agentic.identity.keys` (the stored
  AP2 key). If no active AP2 key exists, the store simply does not issue a
  mandate — the `ap2_mandate` capability is off in that case anyway.
- The issued mandate is persisted as durable dispute evidence (`Mandate`).
"""

from __future__ import annotations

import hashlib
import logging

from django.utils import timezone

from agentic.domain import jcs
from agentic.identity import sdjwt

logger = logging.getLogger(__name__)

# SD-JWT verifiable-credential types for the two AP2 mandate kinds Spwig issues.
# The Checkout (Cart) Mandate attests WHAT was authorised to be bought; the
# Payment Mandate attests the payment leg (amount, method, agent presence) for
# the payment network / issuer. Both are signed with the merchant's AP2 key.
VCT_CHECKOUT = "https://spwig.com/ap2/checkout-mandate/v1"
VCT_PAYMENT = "https://spwig.com/ap2/payment-mandate/v1"


def _active_ap2_key():
    from agentic.models import AgentKey

    return AgentKey.objects.filter(
        purpose=AgentKey.PURPOSE_AP2, status=AgentKey.STATUS_ACTIVE
    ).first()


def _merchant_iss() -> str:
    """Stable issuer identifier — the store's default site URL."""
    try:
        from core.models import SiteSettings

        settings = SiteSettings.objects.filter(pk=1).first()
        url = getattr(settings, "default_url", "") or getattr(settings, "site_url", "")
        if url:
            return url.rstrip("/")
    except Exception:
        logger.warning("mandate: could not resolve merchant iss", exc_info=True)
    return "urn:spwig:merchant"


def _money_claim(money) -> dict:
    """UCP-shaped money: integer minor units + ISO currency (JCS-safe: no float)."""
    from agentic.services.catalog_service import money_to_ucp

    return money_to_ucp(money) or {"amount": 0, "currency": str(money.currency)}


def build_checkout_mandate_payload(order, *, ucp_checkout_id: str = "") -> dict:
    """
    The claim set a Checkout Mandate attests for a placed order.

    Split into always-disclosed checkout terms (amount, currency, order ref,
    line-item digest) and selectively-disclosable buyer contact — a verifier
    can confirm the charge without the store having to expose the buyer's email
    unless the buyer's own agent chooses to.
    """
    amount = _money_claim(order.total_amount)
    lines = [
        {
            "product": str(oi.product_id) if oi.product_id else "",
            "quantity": oi.quantity,
            "total": _money_claim(oi.total_price),
        }
        for oi in order.items.all().order_by("id")
    ]
    line_digest = hashlib.sha256(jcs.canonicalize(lines)).hexdigest()

    always = {
        "mandate_type": "checkout",
        "order_ref": str(order.id),
        "order_number": getattr(order, "order_number", "") or str(order.id),
        "ucp_checkout_id": ucp_checkout_id,
        "amount_due": amount,
        "currency": amount["currency"],
        "line_items_sha256": line_digest,
    }
    sd = {
        "buyer_email": order.email or "",
        "buyer_name": order.billing_name or order.shipping_name or "",
    }
    return {"always": always, "sd": sd}


def _issue_mandate(order, *, mandate_type, vct, always_claims, sd_claims, ucp_checkout_id, agent):
    """
    Sign one AP2 mandate for ``order`` and persist it. Shared by both kinds.

    Returns the created ``Mandate``, or None when the store has no active AP2
    key. Never raises into the checkout path — a mandate is additional
    attestation, not a gate on the order that already placed and paid.
    """
    from agentic.identity.keys import load_private_key
    from agentic.models import Mandate

    key = _active_ap2_key()
    if key is None:
        return None

    try:
        private_key = load_private_key(key)

        now = timezone.now()
        exp = now + timezone.timedelta(days=Mandate.RETENTION_DAYS)
        iat = int(now.timestamp())

        sd_jwt = sdjwt.issue_sd_jwt(
            always_claims=always_claims,
            sd_claims=sd_claims,
            private_key=private_key,
            kid=key.kid,
            iss=_merchant_iss(),
            iat=iat,
            exp=int(exp.timestamp()),
            vct=vct,
        )
        payload_sha = hashlib.sha256(jcs.canonicalize(always_claims)).hexdigest()

        return Mandate.objects.create(
            mandate_type=mandate_type,
            order=order,
            agent=agent,
            ucp_checkout_id=ucp_checkout_id,
            kid=key.kid,
            alg=key.alg,
            attested_amount=order.total_amount,
            sd_jwt=sd_jwt,
            payload_sha256=payload_sha,
            issued_at=now,
            expires_at=exp,
        )
    except Exception:
        logger.exception("mandate: failed to issue %s mandate for order %s", mandate_type, order.pk)
        return None


def issue_checkout_mandate(order, *, ucp_checkout_id: str = "", agent=None):
    """
    Issue, sign, and persist a Checkout Mandate for ``order``.

    The merchant's signed attestation of what the order was authorised to buy and
    be charged (the AP2 ``merchant_authorization``). Returns the created
    ``Mandate``, or None when the store has no active AP2 key.
    """
    from agentic.models import Mandate

    claims = build_checkout_mandate_payload(order, ucp_checkout_id=ucp_checkout_id)
    return _issue_mandate(
        order,
        mandate_type=Mandate.TYPE_CHECKOUT,
        vct=VCT_CHECKOUT,
        always_claims=claims["always"],
        sd_claims=claims["sd"],
        ucp_checkout_id=ucp_checkout_id,
        agent=agent,
    )


def build_payment_mandate_payload(
    order, *, ucp_checkout_id: str = "", payment_method_label: str = ""
) -> dict:
    """
    The claim set an AP2 Payment Mandate attests for a paid order.

    Distinct from the checkout mandate: this attests the payment leg the payment
    network / issuer cares about — the amount actually charged, the (non-secret)
    payment-method label, and the presence signal (agent-initiated, no human at
    checkout). It carries no selectively-disclosed claims and never any card data.
    """
    amount = _money_claim(order.total_amount)
    always = {
        "mandate_type": "payment",
        "order_ref": str(order.id),
        "order_number": getattr(order, "order_number", "") or str(order.id),
        "ucp_checkout_id": ucp_checkout_id,
        "amount": amount,
        "currency": amount["currency"],
        # Agent orders are placed headlessly: the human is not present at the
        # moment of payment. This presence signal is exactly what an issuer's
        # risk engine reads off an AP2 payment mandate.
        "presence": "agent",
        "human_present": False,
        "payment_method": payment_method_label or "",
    }
    return {"always": always, "sd": {}}


def issue_payment_mandate(
    order, *, ucp_checkout_id: str = "", agent=None, payment_method_label: str = ""
):
    """
    Issue, sign, and persist an AP2 Payment Mandate for a paid ``order``.

    The merchant's signed attestation of the payment leg (amount charged, method
    label, agent-presence) for the payment network / issuer. Returns the created
    ``Mandate``, or None when the store has no active AP2 key. Never raises into
    the checkout path.
    """
    from agentic.models import Mandate

    claims = build_payment_mandate_payload(
        order, ucp_checkout_id=ucp_checkout_id, payment_method_label=payment_method_label
    )
    return _issue_mandate(
        order,
        mandate_type=Mandate.TYPE_PAYMENT,
        vct=VCT_PAYMENT,
        always_claims=claims["always"],
        sd_claims=claims["sd"],
        ucp_checkout_id=ucp_checkout_id,
        agent=agent,
    )


def checkout_mandate_for_checkout(ucp_checkout_id: str):
    """The most recent Checkout Mandate issued for a UCP checkout id, or None."""
    from agentic.models import Mandate

    return (
        Mandate.objects.filter(ucp_checkout_id=ucp_checkout_id, mandate_type=Mandate.TYPE_CHECKOUT)
        .order_by("-issued_at")
        .first()
    )


def payment_mandate_for_checkout(ucp_checkout_id: str):
    """The most recent Payment Mandate issued for a UCP checkout id, or None."""
    from agentic.models import Mandate

    return (
        Mandate.objects.filter(ucp_checkout_id=ucp_checkout_id, mandate_type=Mandate.TYPE_PAYMENT)
        .order_by("-issued_at")
        .first()
    )


def mandate_for_checkout(ucp_checkout_id: str):
    """
    The Checkout Mandate for a UCP checkout id, or None.

    Back-compat alias for `checkout_mandate_for_checkout`: the `/mandate/`
    endpoint has always returned the checkout mandate, and adding payment
    mandates must not change what it resolves.
    """
    return checkout_mandate_for_checkout(ucp_checkout_id)
