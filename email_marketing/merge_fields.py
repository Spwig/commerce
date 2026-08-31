"""Personalization merge fields for campaigns.

Merchants insert allowlisted tokens like ``[[first_name]]`` into block text. At
send time each token is resolved per recipient by a plain string substitution —
NOT the Django template engine — so there is no SSTI surface, and resolved
values are HTML-escaped (body) or newline-stripped (subject header). Unknown
tokens resolve to empty. The ``[[ ]]`` delimiter is deliberately not Django
template syntax, so it survives the serializer's SSTI neutralisation untouched.
"""

import logging
import re

from django.utils.html import escape

logger = logging.getLogger("email_marketing")

# [[ field ]] — lowercase/underscore keys only.
_TOKEN_RE = re.compile(r"\[\[\s*([a-z_]+)\s*\]\]")


def _first_name(sub):
    # Prefer the linked account's name; fall back to the subscriber's own
    # (set for imported / storefront-signup contacts with no account).
    if sub.user_id and sub.user.first_name:
        return sub.user.first_name
    return sub.first_name or ""


def _last_name(sub):
    if sub.user_id and sub.user.last_name:
        return sub.user.last_name
    return sub.last_name or ""


def _store_name(sub):
    from core.models import SiteSettings

    return SiteSettings.get_settings().site_name or ""


def _unsubscribe_url(sub):
    from django.contrib.sites.models import Site

    return f"https://{Site.objects.get_current().domain}/marketing/unsubscribe/{sub.unsubscribe_token}/"


def _loyalty_points(sub):
    if not sub.user_id:
        return ""
    points = sub.user.loyalty_member.balance.available_points
    return str(points)


# key -> {label, resolver(subscriber), sample}. Order defines the UI list order.
MERGE_FIELDS = {
    "first_name": {"label": "First name", "resolver": _first_name, "sample": "Alex"},
    "last_name": {"label": "Last name", "resolver": _last_name, "sample": "Rivera"},
    "email": {"label": "Email", "resolver": lambda s: s.email, "sample": "alex@example.com"},
    "store_name": {"label": "Store name", "resolver": _store_name, "sample": "Your Store"},
    "loyalty_points": {"label": "Loyalty points", "resolver": _loyalty_points, "sample": "250"},
    "unsubscribe_url": {
        "label": "Unsubscribe link",
        "resolver": _unsubscribe_url,
        "sample": "https://example.com/unsubscribe",
    },
}


def available_merge_fields() -> list[dict]:
    """[{key, label}] for the builder's merge-field inserter."""
    return [{"key": key, "label": field["label"]} for key, field in MERGE_FIELDS.items()]


def _resolve(key: str, subscriber) -> str:
    field = MERGE_FIELDS.get(key)
    if not field:
        return ""
    try:
        value = field["resolver"](subscriber)
    except Exception:  # noqa: BLE001 — a missing relation must never break a send
        return ""
    return "" if value is None else str(value)


def resolve_merge_fields(text: str, subscriber, *, html: bool = True) -> str:
    """Replace ``[[field]]`` tokens with this subscriber's values.

    ``html=True`` HTML-escapes each value (body context); ``html=False`` strips
    newlines instead (subject/header context, to prevent header injection).
    """
    if not text:
        return text

    def repl(match):
        value = _resolve(match.group(1), subscriber)
        if html:
            return escape(value)
        return value.replace("\r", " ").replace("\n", " ")

    return _TOKEN_RE.sub(repl, text)


def resolve_preview(text: str) -> str:
    """Replace tokens with highlighted sample values for the builder canvas."""
    if not text:
        return text

    def repl(match):
        field = MERGE_FIELDS.get(match.group(1))
        if not field:
            return ""
        return f'<span class="em-merge">{escape(field["sample"])}</span>'

    return _TOKEN_RE.sub(repl, text)
