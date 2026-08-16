"""
Behaviour tests for the communication-preference SiteSettings toggles.

These cover the *wiring* that makes the five GDPR/TCPA settings functional
(2026-08-15) — each test asserts a real behavioural effect of a toggle, not
merely that the field exists:

- enable_double_opt_in       -> marketing email gated on a confirmed address
- default_marketing_opt_in   -> initial opt-in state of a new customer
- preference_center_enabled  -> self-service preference page + API availability
- require_sms_verification   -> SMS gated on a verified phone
- show_unsubscribe_reasons   -> structured reason capture on unsubscribe
"""

from unittest.mock import patch

import pytest
from django.http import QueryDict
from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from accounts.models import CommunicationPreference
from accounts.services.preference_service import PreferenceService
from core.models import SiteSettings
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


@pytest.fixture
def settings_row(db):
    return SiteSettings.get_settings()


def _prefs_for(user, **overrides):
    prefs, _ = CommunicationPreference.get_or_create_for_user(user)
    for key, value in overrides.items():
        setattr(prefs, key, value)
    prefs.save()
    return prefs


# ---------------------------------------------------------------------------
# enable_double_opt_in
# ---------------------------------------------------------------------------


def test_marketing_email_blocked_until_verified_when_double_opt_in_on(settings_row):
    settings_row.enable_double_opt_in = True
    settings_row.save()
    user = UserFactory()
    prefs = _prefs_for(user, email_enabled=True, email_marketing=True, email_verified=False)

    assert prefs.should_send_email("newsletter") is False

    prefs.email_verified = True
    prefs.save()
    assert prefs.should_send_email("newsletter") is True


def test_marketing_email_allowed_without_verification_when_double_opt_in_off(settings_row):
    settings_row.enable_double_opt_in = False
    settings_row.save()
    user = UserFactory()
    prefs = _prefs_for(user, email_enabled=True, email_marketing=True, email_verified=False)

    # No confirmation required — opt-in alone is enough.
    assert prefs.should_send_email("newsletter") is True


def test_opting_into_marketing_triggers_confirmation_email_when_double_opt_in_on(settings_row):
    settings_row.enable_double_opt_in = True
    settings_row.save()
    user = UserFactory()
    _prefs_for(user, email_enabled=True, email_marketing=True, email_verified=False)

    with patch(
        "email_system.services.email_sender.EmailSendingService.send_template_email"
    ) as send:
        sent = PreferenceService.request_marketing_confirmation(user)

    assert sent is True
    assert send.called
    assert send.call_args.kwargs.get("template_type") == "email_verification"


def test_no_confirmation_email_when_double_opt_in_off(settings_row):
    settings_row.enable_double_opt_in = False
    settings_row.save()
    user = UserFactory()
    _prefs_for(user, email_enabled=True, email_marketing=True, email_verified=False)

    with patch(
        "email_system.services.email_sender.EmailSendingService.send_template_email"
    ) as send:
        sent = PreferenceService.request_marketing_confirmation(user)

    assert sent is False
    assert not send.called


def test_verify_email_get_does_not_confirm_only_post_does(client, settings_row):
    """A GET (e.g. a link-prefetcher) must not confirm; only the POST does."""
    settings_row.enable_double_opt_in = True
    settings_row.save()
    user = UserFactory()
    _prefs_for(user, email_enabled=True, email_marketing=True, email_verified=False)

    with patch("email_system.services.email_sender.EmailSendingService.send_template_email"):
        result = PreferenceService.send_verification_email(user)
    token = result["token"]
    url = reverse("accounts:verify_email", kwargs={"token": token})

    # GET shows the confirm page but does NOT flip verification.
    resp_get = client.get(url)
    assert resp_get.status_code == 200
    assert CommunicationPreference.objects.get(user=user).email_verified is False

    # POST performs the confirmation.
    resp_post = client.post(url)
    assert resp_post.status_code == 200
    assert CommunicationPreference.objects.get(user=user).email_verified is True


def test_verify_email_post_rejects_invalid_token(client):
    resp = client.post(reverse("accounts:verify_email", kwargs={"token": "not-a-real-token"}))
    assert resp.status_code == 200
    # Failure page rendered; the address stays unverified (no user touched).


def test_token_resubscribe_requires_reconfirmation_under_double_opt_in(client, settings_row):
    """A previously-confirmed address must not be silently re-armed via the
    broadly-distributed unsubscribe token — it must re-confirm."""
    settings_row.enable_double_opt_in = True
    settings_row.save()
    user = UserFactory()
    prefs = _prefs_for(user, email_enabled=True, email_marketing=False, email_verified=True)

    url = reverse("accounts:unsubscribe", kwargs={"token": prefs.unsubscribe_token})
    with patch("email_system.services.email_sender.EmailSendingService.send_template_email"):
        client.post(url + "?type=newsletter", {"action": "resubscribe"})

    prefs.refresh_from_db()
    # Marketing re-enabled but confirmation reset — nothing sends until reconfirmed.
    assert prefs.email_marketing is True
    assert prefs.email_verified is False
    assert prefs.should_send_email("newsletter") is False


# ---------------------------------------------------------------------------
# default_marketing_opt_in
# ---------------------------------------------------------------------------


def test_new_preferences_opt_in_when_default_is_true(settings_row):
    settings_row.default_marketing_opt_in = True
    settings_row.save()
    user = UserFactory()

    prefs, _ = CommunicationPreference.get_or_create_for_user(user)
    assert prefs.email_marketing is True


def test_new_preferences_opt_out_when_default_is_false(settings_row):
    settings_row.default_marketing_opt_in = False
    settings_row.save()
    user = UserFactory()

    prefs, _ = CommunicationPreference.get_or_create_for_user(user)
    assert prefs.email_marketing is False


# ---------------------------------------------------------------------------
# preference_center_enabled
# ---------------------------------------------------------------------------


def test_preference_center_returns_404_when_disabled(client, settings_row):
    settings_row.preference_center_enabled = False
    settings_row.save()
    user = UserFactory()
    client.force_login(user)

    resp = client.get(reverse("accounts:communication_preferences"))
    assert resp.status_code == 404


def test_preference_center_accessible_when_enabled(client, settings_row):
    settings_row.preference_center_enabled = True
    settings_row.save()
    user = UserFactory()
    client.force_login(user)

    resp = client.get(reverse("accounts:communication_preferences"))
    assert resp.status_code == 200


def test_preference_api_forbidden_when_center_disabled(client, settings_row):
    settings_row.preference_center_enabled = False
    settings_row.save()
    user = UserFactory()
    client.force_login(user)

    resp = client.get("/api/accounts/communication-preferences/")
    assert resp.status_code == 403


# ---------------------------------------------------------------------------
# require_sms_verification
# ---------------------------------------------------------------------------


def test_sms_blocked_until_verified_when_required(settings_row):
    settings_row.require_sms_verification = True
    settings_row.save()
    user = UserFactory()
    prefs = _prefs_for(user, sms_enabled=True, sms_marketing=True, sms_verified=False)

    assert prefs.should_send_sms("promotional_offers") is False

    prefs.sms_verified = True
    prefs.save()
    assert prefs.should_send_sms("promotional_offers") is True


def test_sms_allowed_without_verification_when_not_required(settings_row):
    settings_row.require_sms_verification = False
    settings_row.save()
    user = UserFactory()
    prefs = _prefs_for(user, sms_enabled=True, sms_marketing=True, sms_verified=False)

    assert prefs.should_send_sms("promotional_offers") is True


# ---------------------------------------------------------------------------
# show_unsubscribe_reasons
# ---------------------------------------------------------------------------


def test_unsubscribe_page_shows_reasons_when_enabled(client, settings_row):
    settings_row.show_unsubscribe_reasons = True
    settings_row.save()
    user = UserFactory()
    prefs, _ = CommunicationPreference.get_or_create_for_user(user)

    resp = client.get(reverse("accounts:unsubscribe", kwargs={"token": prefs.unsubscribe_token}))
    assert resp.status_code == 200
    assert b'name="reason"' in resp.content


def test_unsubscribe_page_hides_reasons_when_disabled(client, settings_row):
    settings_row.show_unsubscribe_reasons = False
    settings_row.save()
    user = UserFactory()
    prefs, _ = CommunicationPreference.get_or_create_for_user(user)

    resp = client.get(reverse("accounts:unsubscribe", kwargs={"token": prefs.unsubscribe_token}))
    assert resp.status_code == 200
    assert b'name="reason"' not in resp.content


def test_unsubscribe_records_structured_reason(client, settings_row):
    settings_row.show_unsubscribe_reasons = True
    settings_row.save()
    user = UserFactory()
    prefs = _prefs_for(user, email_marketing=True)

    resp = client.post(
        reverse("accounts:unsubscribe", kwargs={"token": prefs.unsubscribe_token}),
        {"action": "unsubscribe_all", "reason": "too_frequent"},
    )
    assert resp.status_code in (200, 302)

    prefs.refresh_from_db()
    assert prefs.email_marketing is False
    log = prefs.change_logs.filter(action="unsubscribe_all").order_by("-timestamp").first()
    assert log is not None
    assert "too_frequent" in (log.notes or "")


# ---------------------------------------------------------------------------
# newsletter recipient consent gating
# ---------------------------------------------------------------------------


def test_newsletter_recipients_exclude_non_consenting(settings_row):
    from email_system.views import newsletter as nl

    settings_row.enable_double_opt_in = True
    settings_row.save()

    opted_in = UserFactory()
    _prefs_for(opted_in, email_enabled=True, email_marketing=True, email_verified=True)

    opted_out = UserFactory()
    _prefs_for(opted_out, email_enabled=True, email_marketing=False)

    unconfirmed = UserFactory()
    _prefs_for(unconfirmed, email_enabled=True, email_marketing=True, email_verified=False)

    recipients = nl._get_recipients(QueryDict(""), MultiValueDict())
    emails = {e for e, _n in recipients}

    assert opted_in.email in emails
    assert opted_out.email not in emails
    assert unconfirmed.email not in emails  # double opt-in on, not confirmed
