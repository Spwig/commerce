"""
Server-side validation and spam enforcement for public form submissions.

The storefront JS validates fields, evaluates conditional rules, and shows a
honeypot/reCAPTCHA — but a scripted POST bypasses all of it. This module is the
authoritative server-side gate: it whitelists known fields, enforces each
field's type/length/regex/choice constraints, applies conditional rules
(required / hidden / set-value) using the same ``ConditionalRule.evaluate``
the client mirrors, and performs the honeypot + reCAPTCHA checks.
"""

from __future__ import annotations

import logging
import re

from django.core.validators import EmailValidator, URLValidator
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

# Fixed honeypot field name rendered into every form (see form_render.html).
# Honeypot decoy field names rendered by the two front-ends: the storefront
# page-builder element uses `fb_hp_field`; the standalone/preview page uses
# `website`. The server checks both so a scripted bot that fills the visible
# decoy is caught regardless of which front-end rendered the form.
HONEYPOT_FIELDS = ("fb_hp_field", "website")

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


def _allowed_option_values(field) -> list[str]:
    """Allowed submitted values for a choice field, handling both option shapes
    (list of {"value","label"} dicts, or a bare list of strings)."""
    values: list[str] = []
    for opt in field.options or []:
        if isinstance(opt, dict):
            values.append(str(opt.get("value", opt.get("label", ""))))
        else:
            values.append(str(opt))
    return values


def compute_effective_fields(form, submitted: dict) -> dict[str, dict]:
    """Apply active conditional rules to the submitted data (single pass).

    Returns ``{field_name: {"required": bool, "hidden": bool, "forced": value|None}}``
    for every field, starting from the field's static ``is_required`` and folding
    in each matching rule's effect. Rules are applied low-priority-first so a
    higher-priority rule wins. This mirrors what the client enforced
    interactively, re-checked against the finally-submitted values.
    """
    effective = {
        f.field_name: {"required": f.is_required, "hidden": False, "forced": None}
        for f in form.fields.all()
    }
    # Mirror the storefront JS EXACTLY (dynamic_form.js `executeRuleAction`) so
    # the server is never stricter than the browser (which would reject a valid
    # submission). It sorts descending by priority and applies last-wins, and:
    #   hide_field   -> add to hidden (monotonic; show_field is a NO-OP there,
    #                   so once any matching rule hides a field it stays hidden)
    #   require_field / unrequire_field -> last-wins required override
    #   set_value    -> force the value
    #   show_field / show_step / hide_step / skip_to_step -> no field-validation
    #                   effect client-side, so none here either.
    rules = (
        form.rules.filter(is_active=True)
        .select_related("source_field", "target_field")
        .order_by("-priority", "id")
    )
    # The client mutates its live values as set_value fires (dynamic_form.js sets
    # formValues[target]), so a later rule can key off a set value. Evaluate
    # against a working copy that set_value updates, to match that chaining.
    values = dict(submitted)
    for rule in rules:
        if not rule.source_field:
            continue
        src_value = values.get(rule.source_field.field_name)
        if not rule.evaluate(src_value):
            continue
        action = rule.action
        target = rule.target_field.field_name if rule.target_field else None
        if target not in effective:
            continue
        if action == "require_field":
            effective[target]["required"] = True
        elif action == "unrequire_field":
            effective[target]["required"] = False
        elif action == "hide_field":
            effective[target]["hidden"] = True  # monotonic; show_field is a no-op
        elif action == "set_value":
            av = rule.action_value
            forced = av.get("value") if isinstance(av, dict) else av
            effective[target]["forced"] = forced
            values[target] = forced  # mirror the client's mid-loop mutation
    return effective


def _validate_value(field, value) -> str | None:
    """Validate a single non-empty value against the field's constraints.
    Returns an error message, or None if valid."""
    ftype = field.field_type
    svalue = value if isinstance(value, str) else str(value)
    custom_msg = field.validation_message or None

    # Length
    if field.min_length and len(svalue) < field.min_length:
        return custom_msg or _("Must be at least %(n)d characters.") % {"n": field.min_length}
    if field.max_length and len(svalue) > field.max_length:
        return custom_msg or _("Must be at most %(n)d characters.") % {"n": field.max_length}

    # Type-specific
    if ftype == "email":
        try:
            EmailValidator()(svalue)
        except Exception:
            return custom_msg or _("Enter a valid email address.")
    elif ftype == "url":
        try:
            URLValidator()(svalue)
        except Exception:
            return custom_msg or _("Enter a valid URL.")
    elif ftype in ("number", "rating_stars", "rating_nps", "rating_likert"):
        try:
            num = float(svalue)
        except (ValueError, TypeError):
            return custom_msg or _("Enter a valid number.")
        if field.min_value is not None and num < float(field.min_value):
            return custom_msg or _("Must be at least %(v)s.") % {"v": field.min_value}
        if field.max_value is not None and num > float(field.max_value):
            return custom_msg or _("Must be at most %(v)s.") % {"v": field.max_value}

    # Choice membership
    if ftype in ("select", "radio"):
        allowed = _allowed_option_values(field)
        if allowed and svalue not in allowed:
            return custom_msg or _("Select a valid choice.")
    elif ftype in ("checkbox_group",):
        allowed = _allowed_option_values(field)
        submitted_vals = value if isinstance(value, list) else [svalue]
        if allowed and any(str(v) not in allowed for v in submitted_vals):
            return custom_msg or _("Select valid choices.")

    # Custom regex
    if field.validation_regex:
        try:
            if not re.fullmatch(field.validation_regex, svalue):
                return custom_msg or _("Value does not match the required format.")
        except re.error:
            logger.warning("form_builder: invalid validation_regex on field %s", field.pk)

    return None


def validate_submission(form, data: dict) -> tuple[dict, dict]:
    """Validate a submission against the form definition.

    Returns ``(clean_data, errors)``. ``clean_data`` contains ONLY values for the
    form's declared, non-hidden fields (whitelist), with conditional set-values
    forced. ``errors`` maps field_name -> message; empty means valid.
    """
    effective = compute_effective_fields(form, data)
    clean_data: dict = {}
    errors: dict = {}

    for field in form.fields.all():
        # Non-input/display fields never carry submitted data.
        if field.field_type in ("heading", "paragraph", "divider"):
            continue
        state = effective.get(field.field_name, {"required": field.is_required, "hidden": False})

        # A conditionally-hidden field is neither required nor stored.
        if state.get("hidden"):
            continue

        # Server-forced value (conditional set_value) wins.
        if state.get("forced") is not None:
            clean_data[field.field_name] = state["forced"]
            continue

        raw = data.get(field.field_name)
        is_empty = raw is None or raw == "" or raw == []

        if is_empty:
            if state.get("required"):
                errors[field.field_name] = _("%(label)s is required") % {
                    "label": field.translated_label
                }
            continue

        msg = _validate_value(field, raw)
        if msg:
            errors[field.field_name] = msg
        else:
            clean_data[field.field_name] = raw

    return clean_data, errors


# ── Spam protection ─────────────────────────────────────────────────────────


def honeypot_triggered(data, declared_names=frozenset()) -> bool:
    """True when a hidden honeypot decoy carries a value (bot fill). A decoy
    name that is also a real declared field is skipped (not a honeypot)."""
    for name in HONEYPOT_FIELDS:
        if name in declared_names:
            continue
        value = data.get(name)
        if value and str(value).strip():
            return True
    return False


def verify_recaptcha(secret_key: str, token: str, remote_ip: str | None = None) -> bool:
    """Verify a reCAPTCHA token against Google's siteverify. Fail-closed."""
    if not secret_key or not token:
        return False
    import requests

    payload = {"secret": secret_key, "response": token}
    if remote_ip:
        payload["remoteip"] = remote_ip
    try:
        resp = requests.post(RECAPTCHA_VERIFY_URL, data=payload, timeout=10)
        resp.raise_for_status()
        return bool(resp.json().get("success"))
    except Exception:
        logger.warning("form_builder: reCAPTCHA verification failed", exc_info=True)
        return False


def check_spam(form, request) -> str | None:
    """Run the form's configured spam protection. Returns an error string to
    reject with, or None when the submission passes.

    reCAPTCHA note: the storefront does not yet render a reCAPTCHA widget (that
    needs Google's external script, which the platform CSP currently disallows),
    so legitimate submissions arrive without a token. To avoid rejecting every
    real submission, we verify the token *when one is present* (fail-closed —
    ready for when the widget is wired) and otherwise fall back to the honeypot
    so reCAPTCHA-configured forms still get server-side spam protection today.
    """
    protection = getattr(form, "spam_protection", "honeypot")
    if protection == "recaptcha":
        token = request.data.get("g-recaptcha-response") or request.data.get("recaptcha_token")
        if token:
            remote_ip = request.META.get("REMOTE_ADDR")
            if not verify_recaptcha(form.recaptcha_secret_key, token, remote_ip):
                return "recaptcha_failed"
            return None
        # No token (frontend not wired) — fall back to honeypot rather than break.
    elif protection != "honeypot":
        return None  # spam protection disabled/unknown — no server-side check

    # A decoy name that collides with a real declared field (e.g. a URL field
    # named "website") is not treated as a honeypot.
    declared_names = set(form.fields.values_list("field_name", flat=True))
    if honeypot_triggered(request.data, declared_names):
        return "spam_detected"
    return None
