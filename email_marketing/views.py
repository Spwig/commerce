"""Public storefront views for the Campaign Studio.

The tokenised unsubscribe endpoint, plus the storefront newsletter signup +
double opt-in confirmation. All are intentionally unauthenticated (visitors and
email-link recipients) and must exist before any anonymous marketing is sent, so
a lead always has a working opt-in and opt-out.

Unsubscribe: GET renders a confirmation page and does NOT change state — so inbox
link scanners and prefetchers can't trigger accidental unsubscribes. The opt-out
happens on POST, which is CSRF-exempt to support RFC 8058 one-click
List-Unsubscribe-Post. The token is a 256-bit capability, so no CSRF forgery is
possible against a specific victim; the response is identical whether or not the
token matches, so the endpoint cannot be used to enumerate subscribers.

Subscribe: CSRF-protected (both callers supply a token), rate-limited, and
non-enumerating — the response depends only on the merchant's double opt-in
policy, never on whether the address was already known.
"""

import json
import logging

from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.html import escape
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django_ratelimit.decorators import ratelimit

from .models import Subscriber

logger = logging.getLogger("email_marketing")


def _page(title: str, body_html: str, status: int = 200) -> HttpResponse:
    """Minimal, CSP-safe HTML response (no inline styles or scripts)."""
    return HttpResponse(
        f"<!doctype html><html><head><meta charset='utf-8'>"
        f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{escape(title)}</title></head><body>{body_html}</body></html>",
        status=status,
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def unsubscribe(request, token):
    """Unsubscribe a subscriber via their unique token.

    GET → confirmation page (no state change). POST → perform the opt-out. The
    response never reveals whether the token matched.
    """
    if request.method == "GET":
        heading = escape(_("Unsubscribe"))
        prompt = escape(_("Click the button below to stop receiving marketing emails from us."))
        button = escape(_("Unsubscribe"))
        return _page(
            _("Unsubscribe"),
            f"<h1>{heading}</h1><p>{prompt}</p>"
            f"<form method='post'><button type='submit'>{button}</button></form>",
        )

    subscriber = Subscriber.objects.filter(unsubscribe_token=token).first()
    if subscriber and subscriber.status != Subscriber.STATUS_UNSUBSCRIBED:
        subscriber.status = Subscriber.STATUS_UNSUBSCRIBED
        subscriber.marketing_opt_in = False
        subscriber.save(update_fields=["status", "marketing_opt_in", "updated_at"])

        # If linked to a customer account, also turn off their marketing consent
        # so the two systems stay in agreement.
        if subscriber.user_id:
            try:
                from accounts.services.preference_service import PreferenceService

                PreferenceService.unsubscribe_all(
                    subscriber.user,
                    reason="campaign_unsubscribe_link",
                    request=request,
                )
            except Exception as exc:  # noqa: BLE001 — best-effort mirror
                logger.warning("Could not mirror unsubscribe to preferences: %s", exc)

        logger.info("Subscriber %s unsubscribed at %s", subscriber.id, timezone.now())

    body = escape(
        _("You have been unsubscribed. You will no longer receive marketing emails from us.")
    )
    return _page(_("Unsubscribed"), f"<h1>{escape(_('Unsubscribed'))}</h1><p>{body}</p>")


def _wants_json(request) -> bool:
    """True when the caller is the AJAX widget (JSON) rather than a plain form."""
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return True
    content_type = request.META.get("CONTENT_TYPE", "")
    if content_type.startswith("application/json"):
        return True
    return "application/json" in request.headers.get("Accept", "")


def _extract_email(request) -> str:
    """Pull the email from a JSON body (widget) or urlencoded form (element)."""
    content_type = request.META.get("CONTENT_TYPE", "")
    if content_type.startswith("application/json"):
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except (ValueError, UnicodeDecodeError):
            return ""
        return (payload.get("email") or "").strip()
    return (request.POST.get("email") or "").strip()


def _honeypot_tripped(request) -> bool:
    """A filled hidden 'company' field means a bot — silently drop it."""
    if request.META.get("CONTENT_TYPE", "").startswith("application/json"):
        return False
    return bool((request.POST.get("company") or "").strip())


def _subscribe_response(request, *, ok: bool, message: str, status: int = 200):
    if _wants_json(request):
        payload = (
            {"success": ok, "message": message} if ok else {"success": False, "error": message}
        )
        return JsonResponse(payload, status=status)
    heading = _("Newsletter") if ok else _("Something went wrong")
    return _page(heading, f"<h1>{escape(heading)}</h1><p>{escape(message)}</p>", status=status)


@require_POST
@ratelimit(key="ip", rate="10/m", method="POST", block=True)
def subscribe(request):
    """Opt a storefront visitor into the merchant's marketing list.

    Serves both the page-builder newsletter element (plain form POST) and the
    footer/header widget (JSON AJAX). The response is non-enumerating: it reflects
    only the merchant's double opt-in policy, never whether the address existed.
    """
    from .services.subscriptions import (
        OUTCOME_CONFIRM_SENT,
        OUTCOME_SUBSCRIBED,
        subscribe_email,
    )

    if _honeypot_tripped(request):
        # Pretend success without doing anything.
        return _subscribe_response(
            request, ok=True, message=_("Please check your email to confirm your subscription.")
        )

    email = _extract_email(request)
    if not email:
        return _subscribe_response(
            request, ok=False, message=_("Please enter a valid email address."), status=400
        )

    try:
        outcome = subscribe_email(email, request=request)
    except ValidationError:
        return _subscribe_response(
            request, ok=False, message=_("Please enter a valid email address."), status=400
        )

    # Message keyed on merchant policy, not on the individual outcome, so an
    # already-subscribed address is indistinguishable from a fresh one.
    if outcome in (OUTCOME_CONFIRM_SENT,) or (
        outcome != OUTCOME_SUBSCRIBED and Subscriber._double_opt_in_required()
    ):
        message = _("Please check your email to confirm your subscription.")
    else:
        message = _("Thanks for subscribing!")
    return _subscribe_response(request, ok=True, message=message)


@require_http_methods(["GET"])
def confirm(request, token):
    """Complete a double opt-in from the emailed confirmation link."""
    from .services.subscriptions import confirm_subscription

    subscriber = confirm_subscription(token)
    if subscriber is not None:
        heading = _("Subscription confirmed")
        body = _("Thanks for confirming — you're now subscribed to our updates.")
        return _page(heading, f"<h1>{escape(heading)}</h1><p>{escape(body)}</p>")

    heading = _("Link expired")
    body = _("This confirmation link is invalid or has already been used.")
    return _page(heading, f"<h1>{escape(heading)}</h1><p>{escape(body)}</p>", status=404)
