"""
Server-side enforcement + security tests for form_builder.

Covers the remediation of the capability-scan gaps (spam protection and
conditional logic never enforced server-side) plus the security-audit findings:
field validation, whitelist storage, honeypot/reCAPTCHA, file-upload lockdown,
partial-save IDOR, webhook SSRF, and CSV formula injection.
"""

from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from form_builder.models import Form, FormConditionalRule, FormField, FormResponse

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


@pytest.fixture(autouse=True)
def _clear_throttle_cache():
    """Reset the DRF throttle cache between tests so the form-submit rate limit
    doesn't accumulate across the suite and 429."""
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def api_client():
    return APIClient()


def _form(**kwargs):
    defaults = {"name": "F", "slug": "f", "title": "F", "is_active": True}
    defaults.update(kwargs)
    return Form.objects.create(**defaults)


def _field(form, **kwargs):
    defaults = {"field_type": "text", "label": "L", "is_required": False, "order": 0}
    defaults.update(kwargs)
    return FormField.objects.create(form=form, **defaults)


def _submit_url(form):
    return f"/api/form-builder/forms/{form.slug}/submit/"


# ============================================================
# Server-side field validation + whitelist (#3)
# ============================================================


class TestSubmissionValidation:
    def test_valid_submission_stores_only_known_fields(self, api_client):
        form = _form()
        _field(form, field_name="email", field_type="email", is_required=True)
        resp = api_client.post(
            _submit_url(form),
            {"email": "a@b.com", "evil_key": "<script>", "website": ""},
        )
        assert resp.status_code == 200
        fr = FormResponse.objects.get(form=form)
        assert fr.data == {"email": "a@b.com"}  # arbitrary key dropped

    def test_missing_required_field_rejected(self, api_client):
        form = _form()
        _field(form, field_name="email", field_type="email", is_required=True)
        resp = api_client.post(_submit_url(form), {})
        assert resp.status_code == 400
        assert "email" in resp.data["errors"]

    def test_invalid_email_rejected(self, api_client):
        form = _form()
        _field(form, field_name="email", field_type="email", is_required=True)
        resp = api_client.post(_submit_url(form), {"email": "not-an-email"})
        assert resp.status_code == 400

    def test_value_outside_select_choices_rejected(self, api_client):
        form = _form()
        _field(
            form,
            field_name="color",
            field_type="select",
            is_required=True,
            options=[{"value": "red", "label": "Red"}, {"value": "blue", "label": "Blue"}],
        )
        ok = api_client.post(_submit_url(form), {"color": "red"})
        assert ok.status_code == 200
        bad = api_client.post(_submit_url(form), {"color": "green"})
        assert bad.status_code == 400

    def test_max_length_enforced(self, api_client):
        form = _form()
        _field(form, field_name="code", field_type="text", is_required=True, max_length=5)
        resp = api_client.post(_submit_url(form), {"code": "toolongvalue"})
        assert resp.status_code == 400


class TestConditionalEnforcement:
    def test_conditional_require_field_enforced_server_side(self, api_client):
        form = _form()
        contact = _field(
            form,
            field_name="contact_me",
            field_type="select",
            options=[{"value": "yes"}, {"value": "no"}],
        )
        phone = _field(form, field_name="phone", field_type="text", order=1)
        # If contact_me == yes, phone becomes required.
        FormConditionalRule.objects.create(
            form=form,
            source_field=contact,
            operator="equals",
            value={"value": "yes"},
            action="require_field",
            target_field=phone,
        )
        # yes without phone -> rejected
        bad = api_client.post(_submit_url(form), {"contact_me": "yes"})
        assert bad.status_code == 400
        assert "phone" in bad.data["errors"]
        # no without phone -> accepted
        ok = api_client.post(_submit_url(form), {"contact_me": "no"})
        assert ok.status_code == 200

    def test_conditionally_hidden_field_not_required_and_not_stored(self, api_client):
        form = _form()
        trigger = _field(
            form,
            field_name="has_company",
            field_type="select",
            options=[{"value": "yes"}, {"value": "no"}],
        )
        company = _field(form, field_name="company", field_type="text", is_required=True, order=1)
        # If has_company == no, hide (and drop) the otherwise-required company field.
        FormConditionalRule.objects.create(
            form=form,
            source_field=trigger,
            operator="equals",
            value={"value": "no"},
            action="hide_field",
            target_field=company,
        )
        resp = api_client.post(_submit_url(form), {"has_company": "no"})
        assert resp.status_code == 200
        fr = FormResponse.objects.get(form=form)
        assert "company" not in fr.data

    def test_conflicting_rules_resolve_like_the_client(self, api_client):
        """On a conflicting pair the server must reach the same state as the
        storefront JS (descending priority, last-wins → lowest priority wins).
        Here unrequire (priority 5) applies after require (priority 10)."""
        form = _form()
        src = _field(
            form, field_name="x", field_type="select", options=[{"value": "yes"}, {"value": "no"}]
        )
        phone = _field(form, field_name="phone", field_type="text", order=1)
        FormConditionalRule.objects.create(
            form=form,
            source_field=src,
            operator="equals",
            value={"value": "yes"},
            action="require_field",
            target_field=phone,
            priority=10,
        )
        FormConditionalRule.objects.create(
            form=form,
            source_field=src,
            operator="equals",
            value={"value": "yes"},
            action="unrequire_field",
            target_field=phone,
            priority=5,
        )
        # unrequire wins -> phone not required -> accepted without phone
        resp = api_client.post(_submit_url(form), {"x": "yes"})
        assert resp.status_code == 200

    def test_show_and_hide_conflict_stays_hidden_like_client(self, api_client):
        """The client's show_field is a no-op, so hide wins on a conflict — the
        server must match (never require a field the browser hid)."""
        form = _form()
        src = _field(
            form, field_name="x", field_type="select", options=[{"value": "yes"}, {"value": "no"}]
        )
        secret = _field(form, field_name="secret", field_type="text", is_required=True, order=1)
        FormConditionalRule.objects.create(
            form=form,
            source_field=src,
            operator="equals",
            value={"value": "yes"},
            action="hide_field",
            target_field=secret,
            priority=5,
        )
        FormConditionalRule.objects.create(
            form=form,
            source_field=src,
            operator="equals",
            value={"value": "yes"},
            action="show_field",
            target_field=secret,
            priority=10,
        )
        resp = api_client.post(_submit_url(form), {"x": "yes"})  # no 'secret'
        assert resp.status_code == 200
        assert "secret" not in FormResponse.objects.get(form=form).data

    def test_set_value_chains_into_later_rule(self, api_client):
        """A later rule keying off a set_value target must see the set value
        (matches the client mutating formValues mid-loop)."""
        form = _form()
        trigger = _field(
            form,
            field_name="trigger",
            field_type="select",
            options=[{"value": "yes"}, {"value": "no"}],
        )
        derived = _field(form, field_name="derived", field_type="text", order=1)
        extra = _field(form, field_name="extra", field_type="text", order=2)
        # A (pri 10): trigger==yes -> set derived="X"
        FormConditionalRule.objects.create(
            form=form,
            source_field=trigger,
            operator="equals",
            value={"value": "yes"},
            action="set_value",
            target_field=derived,
            action_value={"value": "X"},
            priority=10,
        )
        # B (pri 5): derived==X -> require extra
        FormConditionalRule.objects.create(
            form=form,
            source_field=derived,
            operator="equals",
            value={"value": "X"},
            action="require_field",
            target_field=extra,
            priority=5,
        )
        resp = api_client.post(_submit_url(form), {"trigger": "yes"})  # no extra
        assert resp.status_code == 400
        assert "extra" in resp.data["errors"]

    def test_pinned_adapter_preserves_non_default_port_in_host(self):
        import requests

        from form_builder.actions.webhook import _PinnedIPAdapter

        req = requests.PreparedRequest()
        req.prepare(method="POST", url="https://hooks.example:8443/p", data=b"{}")
        adapter = _PinnedIPAdapter("hooks.example", "93.184.216.34")
        with patch("requests.adapters.HTTPAdapter.send", return_value="ok") as sup:
            adapter.send(req)
        assert sup.call_args[0][0].headers["Host"] == "hooks.example:8443"


# ============================================================
# Spam protection (#2)
# ============================================================


class TestSpamProtection:
    def test_filled_honeypot_is_silently_dropped(self, api_client):
        form = _form(spam_protection="honeypot")
        _field(form, field_name="email", field_type="email", is_required=True)
        resp = api_client.post(
            _submit_url(form), {"email": "a@b.com", "website": "http://spam.example"}
        )
        assert resp.status_code == 200  # benign success
        assert FormResponse.objects.filter(form=form).count() == 0  # nothing stored

    def test_recaptcha_failure_rejected(self, api_client):
        form = _form(spam_protection="recaptcha", recaptcha_secret_key="secret")
        _field(form, field_name="email", field_type="email", is_required=True)
        with patch("form_builder.validation.verify_recaptcha", return_value=False):
            resp = api_client.post(
                _submit_url(form), {"email": "a@b.com", "g-recaptcha-response": "tok"}
            )
        assert resp.status_code == 400
        assert FormResponse.objects.filter(form=form).count() == 0

    def test_recaptcha_success_accepted(self, api_client):
        form = _form(spam_protection="recaptcha", recaptcha_secret_key="secret")
        _field(form, field_name="email", field_type="email", is_required=True)
        with patch("form_builder.validation.verify_recaptcha", return_value=True):
            resp = api_client.post(
                _submit_url(form), {"email": "a@b.com", "g-recaptcha-response": "tok"}
            )
        assert resp.status_code == 200
        assert FormResponse.objects.filter(form=form).count() == 1

    def test_recaptcha_form_without_token_falls_back_to_honeypot(self, api_client):
        """Frontend isn't wired for reCAPTCHA yet, so a tokenless legit
        submission must still succeed (via honeypot), not be rejected."""
        form = _form(spam_protection="recaptcha", recaptcha_secret_key="secret")
        _field(form, field_name="email", field_type="email", is_required=True)
        resp = api_client.post(_submit_url(form), {"email": "a@b.com"})  # no token
        assert resp.status_code == 200
        assert FormResponse.objects.filter(form=form).count() == 1

    def test_real_website_field_is_not_treated_as_honeypot(self, api_client):
        """A form with a legitimately-named 'website' field must accept it — the
        honeypot only applies when 'website' is an undeclared decoy."""
        form = _form(spam_protection="honeypot")
        _field(form, field_name="website", field_type="url", is_required=True)
        resp = api_client.post(_submit_url(form), {"website": "https://real.example"})
        assert resp.status_code == 200
        fr = FormResponse.objects.get(form=form)
        assert fr.data["website"] == "https://real.example"

    def test_disabled_spam_protection_skips_honeypot(self, api_client):
        form = _form(spam_protection="none")
        _field(form, field_name="email", field_type="email", is_required=True)
        resp = api_client.post(_submit_url(form), {"email": "a@b.com", "website": "anything"})
        assert resp.status_code == 200
        assert FormResponse.objects.filter(form=form).count() == 1

    def test_recaptcha_form_without_token_still_catches_honeypot(self, api_client):
        form = _form(spam_protection="recaptcha", recaptcha_secret_key="secret")
        _field(form, field_name="email", field_type="email", is_required=True)
        resp = api_client.post(_submit_url(form), {"email": "a@b.com", "website": "spam"})
        assert resp.status_code == 200  # benign
        assert FormResponse.objects.filter(form=form).count() == 0


# ============================================================
# File upload lockdown (#1)
# ============================================================


class TestUploadSecurity:
    def test_dangerous_extension_rejected_even_if_whitelisted(self):
        from form_builder.upload_security import UploadRejected, validate_upload

        f = SimpleUploadedFile("evil.svg", b"<svg onload=alert(1)>", content_type="image/svg+xml")
        with pytest.raises(UploadRejected):
            validate_upload(f, ["svg"])  # merchant allowed it; hard denylist still wins

    def test_empty_allowed_types_uses_safe_default(self):
        from form_builder.upload_security import UploadRejected, validate_upload

        exe = SimpleUploadedFile("payload.exe", b"MZ\x90\x00", content_type="application/x-dosexec")
        with pytest.raises(UploadRejected):
            validate_upload(exe, [])  # not in the safe default allowlist

    def test_content_extension_mismatch_rejected(self):
        from form_builder.upload_security import UploadRejected, validate_upload

        fake_png = SimpleUploadedFile(
            "a.png", b"<html><body>x</body></html>", content_type="image/png"
        )
        with pytest.raises(UploadRejected):
            validate_upload(fake_png, ["png"])

    def test_safe_document_accepted(self):
        from form_builder.upload_security import validate_upload

        txt = SimpleUploadedFile("notes.txt", b"just some text", content_type="text/plain")
        assert validate_upload(txt, []) == "txt"

    def test_stored_name_is_not_traversable(self):
        from form_builder.upload_security import safe_stored_name

        name = safe_stored_name("my-form", "../../../etc/passwd", "txt")
        assert ".." not in name
        assert name.startswith("my-form/")
        assert name.endswith(".txt")

    def test_sniff_failure_fails_closed_for_content_checked_type(self):
        """If content sniffing is unavailable, a content-checked extension
        (image/pdf/media) must be rejected rather than trusted on extension."""
        from form_builder import upload_security

        png = SimpleUploadedFile("a.png", b"<html>x</html>", content_type="image/png")
        with patch("magic.from_buffer", side_effect=RuntimeError("libmagic missing")):
            with pytest.raises(upload_security.UploadRejected):
                upload_security.validate_upload(png, ["png"])


# ============================================================
# Partial-save IDOR (#4)
# ============================================================


class TestPartialSaveIDOR:
    def test_other_session_cannot_overwrite_draft(self):
        form = _form(save_partial_responses=True)
        _field(form, field_name="email", field_type="email")
        url = f"/api/form-builder/forms/{form.slug}/partial/"

        attacker = APIClient()
        owner = APIClient()
        created = owner.post(
            url, {"data": {"email": "owner@b.com"}, "current_step": 1}, format="json"
        )
        assert created.status_code == 200
        rid = created.data["response_id"]

        # Attacker (different session) tries to overwrite the owner's draft.
        resp = attacker.post(
            url, {"response_id": rid, "data": {"email": "hacked@b.com"}}, format="json"
        )
        assert resp.status_code == 404
        FormResponse.objects.get(pk=rid).refresh_from_db()
        assert FormResponse.objects.get(pk=rid).data["email"] == "owner@b.com"


# ============================================================
# Webhook SSRF (#7) + CSV injection (#6) — unit
# ============================================================


class TestWebhookSSRF:
    def test_blocks_link_local_metadata(self):
        from form_builder.actions.webhook import validate_webhook_url

        ok, _ = validate_webhook_url("http://169.254.169.254/latest/meta-data/")
        assert ok is False

    def test_blocks_loopback(self):
        from form_builder.actions.webhook import validate_webhook_url

        ok, _ = validate_webhook_url("http://127.0.0.1:8000/internal")
        assert ok is False

    def test_blocks_non_http_scheme(self):
        from form_builder.actions.webhook import validate_webhook_url

        ok, _ = validate_webhook_url("file:///etc/passwd")
        assert ok is False

    def test_blocks_carrier_grade_nat_range(self):
        """100.64.0.0/10 is shared/non-global and reaches internal infra."""
        from form_builder.actions import webhook

        assert webhook._addr_is_public("100.64.1.1") is False

    def test_allows_public_host(self):
        from form_builder.actions import webhook

        with patch.object(
            webhook.socket, "getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 0))]
        ):
            ok, _ = webhook.validate_webhook_url("https://example.com/hook")
        assert ok is True

    def test_mixed_public_private_resolution_is_rejected(self):
        """A host resolving to both a public and a private IP is an SSRF dodge."""
        from form_builder.actions import webhook

        with patch.object(
            webhook.socket,
            "getaddrinfo",
            return_value=[
                (2, 1, 6, "", ("93.184.216.34", 0)),
                (2, 1, 6, "", ("169.254.169.254", 0)),
            ],
        ):
            assert webhook.resolve_public_ip("rebind.example") is None

    def test_pinned_adapter_connects_to_ip_keeps_host(self):
        """The pinning adapter rewrites the connection to the validated IP while
        preserving the Host header (SNI stays on the hostname) — closes the
        DNS-rebinding TOCTOU."""
        import requests

        from form_builder.actions.webhook import _PinnedIPAdapter

        req = requests.PreparedRequest()
        req.prepare(method="POST", url="https://example.com/hook", data=b"{}")
        adapter = _PinnedIPAdapter("example.com", "93.184.216.34")
        with patch("requests.adapters.HTTPAdapter.send", return_value="ok") as sup:
            adapter.send(req)
        sent = sup.call_args[0][0]
        assert "93.184.216.34" in sent.url
        assert sent.headers["Host"] == "example.com"

    def test_http_adapter_omits_tls_pool_kwargs(self):
        """Plain-HTTP webhooks must not receive HTTPS-only pool kwargs
        (server_hostname/assert_hostname) — urllib3 would raise TypeError."""
        from form_builder.actions.webhook import _PinnedIPAdapter

        http = _PinnedIPAdapter("example.com", "93.184.216.34", is_https=False)
        http.init_poolmanager(1, 1)  # must not raise
        assert "server_hostname" not in http.poolmanager.connection_pool_kw
        https = _PinnedIPAdapter("example.com", "93.184.216.34", is_https=True)
        https.init_poolmanager(1, 1)
        assert "server_hostname" in https.poolmanager.connection_pool_kw


class TestCsvInjection:
    @pytest.mark.parametrize("payload", ["=cmd|calc", "+1", "-1+1", "@SUM(A1)", "\n=IMPORTXML(1)"])
    def test_formula_cells_are_neutralised(self, payload):
        from form_builder.views import csv_safe_cell

        assert csv_safe_cell(payload) == "'" + payload

    def test_plain_values_unchanged(self):
        from form_builder.views import csv_safe_cell

        assert csv_safe_cell("hello") == "hello"


class TestReCaptchaSecretEncryption:
    """The reCAPTCHA secret is encrypted at rest (EncryptedCharField)."""

    def test_secret_is_encrypted_in_db_and_transparent_via_orm(self):
        from django.db import connection

        form = _form(spam_protection="recaptcha")
        form.recaptcha_secret_key = "super-secret-value"
        form.save()

        with connection.cursor() as cur:
            cur.execute("SELECT recaptcha_secret_key FROM form_builder_form WHERE id=%s", [form.id])
            raw = cur.fetchone()[0]
        # Stored ciphertext is prefixed and does NOT contain the plaintext.
        assert raw.startswith("fbenc:")
        assert "super-secret-value" not in raw
        # ORM read decrypts transparently.
        assert Form.objects.get(id=form.id).recaptcha_secret_key == "super-secret-value"

    def test_legacy_plaintext_is_still_readable(self):
        from django.db import connection

        form = _form(spam_protection="recaptcha")
        # Simulate a pre-encryption row by writing plaintext via raw SQL
        # (bypasses the field's get_prep_value).
        with connection.cursor() as cur:
            cur.execute(
                "UPDATE form_builder_form SET recaptcha_secret_key=%s WHERE id=%s",
                ["legacy-plaintext", form.id],
            )
        assert Form.objects.get(id=form.id).recaptcha_secret_key == "legacy-plaintext"

    def test_blank_secret_stays_blank(self):
        form = _form(spam_protection="honeypot")
        form.recaptcha_secret_key = ""
        form.save()
        from django.db import connection

        with connection.cursor() as cur:
            cur.execute("SELECT recaptcha_secret_key FROM form_builder_form WHERE id=%s", [form.id])
            assert cur.fetchone()[0] == ""


class TestRecaptchaWiring:
    """The v3 site key reaches the front-end island; the secret never does; and
    the storefront honeypot field name is enforced server-side."""

    def test_form_data_exposes_site_key_not_secret(self):
        import json

        from form_builder.templatetags.form_builder_tags import get_form_data

        form = _form(
            spam_protection="recaptcha",
            recaptcha_site_key="SITE-KEY-PUBLIC",
            recaptcha_secret_key="SECRET-KEY-PRIVATE",
        )
        _field(form, field_name="email", field_type="email")
        data = get_form_data({}, form.slug)
        assert data["recaptcha_site_key"] == "SITE-KEY-PUBLIC"
        # The secret must never be serialised to the client island.
        assert "SECRET-KEY-PRIVATE" not in json.dumps(data)

    def test_form_data_omits_site_key_when_not_recaptcha(self):
        from form_builder.templatetags.form_builder_tags import get_form_data

        form = _form(spam_protection="honeypot", recaptcha_site_key="SITE-KEY")
        data = get_form_data({}, form.slug)
        assert data["recaptcha_site_key"] == ""

    def test_storefront_honeypot_field_is_enforced(self, api_client):
        """The page-builder element renders the honeypot as `fb_hp_field`; a
        scripted bot that fills it must be dropped server-side."""
        form = _form(spam_protection="honeypot")
        _field(form, field_name="email", field_type="email", is_required=True)
        resp = api_client.post(_submit_url(form), {"email": "a@b.com", "fb_hp_field": "i-am-a-bot"})
        assert resp.status_code == 200  # benign
        assert FormResponse.objects.filter(form=form).count() == 0
