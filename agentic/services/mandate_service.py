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

# SD-JWT verifiable-credential type for a Spwig checkout mandate.
VCT_CHECKOUT = "https://spwig.com/ap2/checkout-mandate/v1"


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


def issue_checkout_mandate(order, *, ucp_checkout_id: str = "", agent=None):
    """
    Issue, sign, and persist a Checkout Mandate for ``order``.

    Returns the created ``Mandate``, or None when the store has no active AP2
    key (in which case it doesn't advertise ap2_mandate either). Never raises
    into the checkout path — a mandate is additional attestation, not a gate on
    the order that already placed and paid.
    """
    from agentic.identity.keys import load_private_key
    from agentic.models import Mandate

    key = _active_ap2_key()
    if key is None:
        return None

    try:
        claims = build_checkout_mandate_payload(order, ucp_checkout_id=ucp_checkout_id)
        private_key = load_private_key(key)

        now = timezone.now()
        exp = now + timezone.timedelta(days=Mandate.RETENTION_DAYS)
        iat = int(now.timestamp())

        sd_jwt = sdjwt.issue_sd_jwt(
            always_claims=claims["always"],
            sd_claims=claims["sd"],
            private_key=private_key,
            kid=key.kid,
            iss=_merchant_iss(),
            iat=iat,
            exp=int(exp.timestamp()),
            vct=VCT_CHECKOUT,
        )
        payload_sha = hashlib.sha256(jcs.canonicalize(claims["always"])).hexdigest()

        return Mandate.objects.create(
            mandate_type=Mandate.TYPE_CHECKOUT,
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
        logger.exception("mandate: failed to issue checkout mandate for order %s", order.pk)
        return None


def mandate_for_checkout(ucp_checkout_id: str):
    """The most recent mandate issued for a UCP checkout id, or None."""
    from agentic.models import Mandate

    return Mandate.objects.filter(ucp_checkout_id=ucp_checkout_id).order_by("-issued_at").first()
