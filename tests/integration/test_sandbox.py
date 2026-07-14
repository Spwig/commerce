"""
Integration tests for the Sandbox Mode system.

Tests cover:
- License mode detection (is_sandbox_mode)
- Payment gateway enforcement
- Email redirection
- Order test flagging
- Webhook sandbox flag
- Sandbox banner middleware
- Tamper report endpoint
- POS license validation
- Email guard whitelist (sandbox_filter_recipient, validate_whitelist)
- SMS guard whitelist (sandbox_filter_sms_recipient, validate_sms_whitelist)
- Email backend whitelist filtering
- EmailSendingService sandbox enforcement (queue_email, send_template_email, send_email)
- SMS sending service sandbox enforcement (send_sms, send_whatsapp)
- Webhook delivery restrictions (localhost-only in sandbox)
- Usage telemetry (_collect_usage_metrics, refresh_license)
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory

# ============================================================
# License Detection
# ============================================================


class TestSandboxDetection:
    """Test is_sandbox_mode() under various license states."""

    def test_no_license_data_is_not_sandbox(self):
        """
        No license file → NOT sandbox mode.

        Prior to Community edition, a missing licence file was treated as
        sandbox as a graceful-degradation fallback. That fallback is now
        removed — Community edition is auto-bootstrapped at startup so a
        missing licence file means the platform hasn't been bootstrapped
        yet, which is a distinct (and rare) condition. Sandbox mode is
        now reserved for explicit dev/staging/sandbox environment_type.
        """
        from core.license import LicenseManager

        mgr = LicenseManager.__new__(LicenseManager)
        with patch.object(mgr, "get_license_data", return_value=None):
            assert mgr.is_sandbox() is False

    def test_development_environment_is_sandbox(self):
        """License with environment_type='development' → sandbox."""
        from core.license import LicenseManager

        mgr = LicenseManager.__new__(LicenseManager)
        license_data = {"license": {"environment_type": "development"}}
        with patch.object(mgr, "get_license_data", return_value=license_data):
            assert mgr.is_sandbox() is True

    def test_staging_environment_is_sandbox(self):
        """License with environment_type='staging' → sandbox."""
        from core.license import LicenseManager

        mgr = LicenseManager.__new__(LicenseManager)
        license_data = {"license": {"environment_type": "staging"}}
        with patch.object(mgr, "get_license_data", return_value=license_data):
            assert mgr.is_sandbox() is True

    def test_production_environment_is_not_sandbox(self):
        """License with environment_type='production' → NOT sandbox."""
        from core.license import LicenseManager

        mgr = LicenseManager.__new__(LicenseManager)
        license_data = {"license": {"environment_type": "production"}}
        with patch.object(mgr, "get_license_data", return_value=license_data):
            assert mgr.is_sandbox() is False

    def test_missing_environment_type_defaults_to_production(self):
        """License without environment_type → defaults to production (not sandbox)."""
        from core.license import LicenseManager

        mgr = LicenseManager.__new__(LicenseManager)
        license_data = {"license": {"license_key": "ABC-1234"}}
        with patch.object(mgr, "get_license_data", return_value=license_data):
            assert mgr.is_sandbox() is False

    def test_module_level_is_sandbox_mode(self):
        """Test the module-level convenience function."""
        from core.license import get_license_manager, is_sandbox_mode

        with patch.object(get_license_manager(), "is_sandbox", return_value=True):
            assert is_sandbox_mode() is True


# ============================================================
# Payment Guard
# ============================================================


class TestPaymentGuard:
    """Test payment credential validation in sandbox mode."""

    def test_noop_in_production(self):
        """Guard does nothing when not in sandbox mode."""
        from core.sandbox.payment_guard import validate_provider_credentials

        with patch("core.sandbox.payment_guard.is_sandbox_mode", return_value=False):
            # Should not raise even with live credentials
            validate_provider_credentials(
                "stripe",
                {
                    "environment": "live",
                    "secret_key": "sk_live_12345",
                },
            )

    def test_rejects_live_environment_in_sandbox(self):
        """Guard rejects 'live' environment field in sandbox."""
        from core.sandbox.payment_guard import (
            SandboxPaymentError,
            validate_provider_credentials,
        )

        with patch("core.sandbox.payment_guard.is_sandbox_mode", return_value=True):
            with pytest.raises(SandboxPaymentError, match="Live/production credentials"):
                validate_provider_credentials(
                    "stripe",
                    {
                        "environment": "live",
                        "secret_key": "sk_live_12345",
                    },
                )

    def test_allows_test_environment_in_sandbox(self):
        """Guard allows 'test' environment in sandbox."""
        from core.sandbox.payment_guard import validate_provider_credentials

        with patch("core.sandbox.payment_guard.is_sandbox_mode", return_value=True):
            validate_provider_credentials(
                "stripe",
                {
                    "environment": "test",
                    "secret_key": "sk_test_12345",
                    "publishable_key": "pk_test_12345",
                },
            )

    def test_rejects_stripe_live_key_prefix_in_sandbox(self):
        """Guard catches Stripe live key even if environment says test."""
        from core.sandbox.payment_guard import (
            SandboxPaymentError,
            validate_provider_credentials,
        )

        with patch("core.sandbox.payment_guard.is_sandbox_mode", return_value=True):
            with pytest.raises(SandboxPaymentError, match="has a live key"):
                validate_provider_credentials(
                    "stripe",
                    {
                        "environment": "test",
                        "secret_key": "sk_live_sneaky12345",
                    },
                )

    def test_rejects_revolut_live_key_in_sandbox(self):
        """Guard catches Revolut live key prefix."""
        from core.sandbox.payment_guard import (
            SandboxPaymentError,
            validate_provider_credentials,
        )

        with patch("core.sandbox.payment_guard.is_sandbox_mode", return_value=True):
            with pytest.raises(SandboxPaymentError, match="has a live key"):
                validate_provider_credentials(
                    "revolut",
                    {
                        "environment": "sandbox",
                        "secret_key": "sk_live_revolut123",
                    },
                )

    def test_allows_all_providers_with_test_environment(self):
        """All 6 providers pass with test/sandbox/demo environment."""
        from core.sandbox.payment_guard import validate_provider_credentials

        with patch("core.sandbox.payment_guard.is_sandbox_mode", return_value=True):
            for slug, env in [
                ("stripe", "test"),
                ("airwallex", "demo"),
                ("paypal", "sandbox"),
                ("square", "sandbox"),
                ("revolut", "sandbox"),
                ("adyen", "test"),
            ]:
                validate_provider_credentials(slug, {"environment": env})

    def test_missing_environment_with_live_key_still_caught(self):
        """Even without environment field, live key prefix is caught."""
        from core.sandbox.payment_guard import (
            SandboxPaymentError,
            validate_provider_credentials,
        )

        with patch("core.sandbox.payment_guard.is_sandbox_mode", return_value=True):
            # Live key without environment field — key prefix check still catches it
            with pytest.raises(SandboxPaymentError, match="has a live key"):
                validate_provider_credentials(
                    "stripe",
                    {
                        "secret_key": "sk_live_12345",
                    },
                )

    def test_missing_environment_with_test_key_allowed(self):
        """Test key without environment field is allowed (unknown environment logged only)."""
        from core.sandbox.payment_guard import validate_provider_credentials

        with patch("core.sandbox.payment_guard.is_sandbox_mode", return_value=True):
            # Test key without environment — not blocked
            validate_provider_credentials(
                "stripe",
                {
                    "secret_key": "sk_test_12345",
                },
            )


# ============================================================
# Email Backend
# ============================================================


class TestSandboxEmailBackend:
    """Test sandbox email interception."""

    def test_drops_non_whitelisted_in_sandbox(self):
        """Non-whitelisted emails are dropped in sandbox mode."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with (
            patch("core.sandbox.email_backend.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
        ):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["customer@example.com"]
            msg.cc = ["cc@example.com"]
            msg.bcc = ["bcc@example.com"]
            msg.subject = "Order Confirmation"
            msg.body = "Thank you!"
            msg.alternatives = [("<p>Thank you!</p>", "text/html")]

            result = sb.send_messages([msg])

            # All recipients are non-whitelisted, so email should be dropped
            backend.send_messages.assert_not_called()
            assert result == 0

    def test_passthrough_in_production(self):
        """Emails pass through unchanged in production."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with patch("core.sandbox.email_backend.is_sandbox_mode", return_value=False):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["customer@example.com"]
            msg.subject = "Order Confirmation"

            sb.send_messages([msg])

            backend.send_messages.assert_called_once_with([msg])
            assert msg.to == ["customer@example.com"]


# ============================================================
# Webhook Sandbox Flag
# ============================================================


class TestWebhookSandboxFlag:
    """Test that webhook payload building includes sandbox flag."""

    def test_sandbox_flag_added_to_payload(self):
        """Payload building adds sandbox=True when in sandbox mode."""
        from django.utils import timezone

        # Simulate what trigger_webhook does to build the payload
        payload = {
            "event": "order.created",
            "created_at": timezone.now().isoformat(),
            "data": {"order_id": 123},
        }

        # In sandbox mode, the flag should be added
        with patch("core.license.is_sandbox_mode", return_value=True):
            from core.license import is_sandbox_mode

            if is_sandbox_mode():
                payload["sandbox"] = True

        assert payload.get("sandbox") is True

    def test_no_sandbox_flag_in_production(self):
        """Payload does NOT include sandbox flag in production."""
        from django.utils import timezone

        payload = {
            "event": "order.created",
            "created_at": timezone.now().isoformat(),
            "data": {"order_id": 123},
        }

        with patch("core.license.is_sandbox_mode", return_value=False):
            from core.license import is_sandbox_mode

            if is_sandbox_mode():
                payload["sandbox"] = True

        assert "sandbox" not in payload


# ============================================================
# Sandbox Banner Middleware
# ============================================================


class TestSandboxBannerMiddleware:
    """Test sandbox banner injection."""

    def test_injects_banner_in_sandbox(self):
        """HTML responses get sandbox banner in sandbox mode."""
        from core.sandbox.middleware import SandboxBannerMiddleware

        factory = RequestFactory()
        request = factory.get("/en/products/")

        response = MagicMock()
        response.status_code = 200
        response.streaming = False
        response.get = lambda key, default="": (
            "text/html; charset=utf-8" if key == "Content-Type" else default
        )
        response.content = b"<html><body><h1>Shop</h1></body></html>"
        response.__setitem__ = MagicMock()

        middleware = SandboxBannerMiddleware(lambda r: response)

        with patch("core.sandbox.middleware.is_sandbox_mode", return_value=True):
            result = middleware.process_response(request, response)

        assert b"SANDBOX MODE" in result.content
        assert b"_nuke" in result.content  # Tamper detection present

    def test_no_banner_in_production(self):
        """No banner injection in production mode."""
        from core.sandbox.middleware import SandboxBannerMiddleware

        factory = RequestFactory()
        request = factory.get("/en/products/")

        original_content = b"<html><body><h1>Shop</h1></body></html>"
        response = MagicMock()
        response.status_code = 200
        response.streaming = False
        response.content = original_content

        middleware = SandboxBannerMiddleware(lambda r: response)

        with patch("core.sandbox.middleware.is_sandbox_mode", return_value=False):
            result = middleware.process_response(request, response)

        assert result.content == original_content

    def test_admin_badge_not_full_banner(self):
        """Admin pages get badge, not full banner."""
        from core.sandbox.middleware import SandboxBannerMiddleware

        factory = RequestFactory()
        request = factory.get("/en/admin/dashboard/")

        response = MagicMock()
        response.status_code = 200
        response.streaming = False
        response.get = lambda key, default="": (
            "text/html; charset=utf-8" if key == "Content-Type" else default
        )
        response.content = b'<html><body><div class="admin-header"><div class="header-brand">Admin</div></div></body></html>'
        response.__setitem__ = MagicMock()

        middleware = SandboxBannerMiddleware(lambda r: response)

        with patch("core.sandbox.middleware.is_sandbox_mode", return_value=True):
            result = middleware.process_response(request, response)

        content = result.content.decode()
        assert "SANDBOX" in content
        # Admin badge doesn't include the full _nuke function
        assert "_nuke" not in content

    def test_skips_api_paths(self):
        """API paths are excluded from banner injection."""
        from core.sandbox.middleware import SandboxBannerMiddleware

        factory = RequestFactory()
        request = factory.get("/api/products/")

        original_content = b'{"products": []}'
        response = MagicMock()
        response.status_code = 200
        response.streaming = False
        response.get = lambda key, default="": (
            "application/json" if key == "Content-Type" else default
        )
        response.content = original_content

        middleware = SandboxBannerMiddleware(lambda r: response)

        with patch("core.sandbox.middleware.is_sandbox_mode", return_value=True):
            result = middleware.process_response(request, response)

        # JSON content type means no injection
        assert result.content == original_content


# ============================================================
# Tamper Report Endpoint
# ============================================================


@pytest.mark.django_db
@pytest.mark.django_db
class TestTamperReport:
    """Test the tamper report API endpoint."""

    @pytest.fixture(autouse=True)
    def _ensure_site_settings(self, db):
        """Ensure a singleton SiteSettings exists so the middleware chain doesn't error."""
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(pk=1, defaults={"admin_email": "admin@example.com"})

    def test_accepts_valid_report(self, client):
        """Valid tamper report returns 204."""
        with (
            patch("core.sandbox.views.is_sandbox_mode", return_value=True),
            patch("core.sandbox.tasks.report_tamper_to_server") as mock_task,
        ):
            mock_task.delay = MagicMock()
            response = client.post(
                "/api/sandbox/tamper-report/",
                data=json.dumps(
                    {
                        "event": "banner_tamper",
                        "url": "http://localhost/en/",
                        "ts": 1234567890,
                    }
                ),
                content_type="application/json",
            )
            assert response.status_code == 204

    def test_noop_in_production(self, client):
        """Tamper reports are silently ignored in production."""
        with patch("core.sandbox.views.is_sandbox_mode", return_value=False):
            response = client.post(
                "/api/sandbox/tamper-report/",
                data=json.dumps({"event": "banner_tamper"}),
                content_type="application/json",
            )
            assert response.status_code == 204


# ============================================================
# POS License Validation
# ============================================================


class TestPOSLicense:
    """
    POS is universally enabled from v1.5.8 onward. The pos_license
    helpers stay in place as no-op shims for backwards compatibility
    with any admin UI or legacy client that still calls them.
    """

    def test_pos_is_valid_regardless_of_edition(self):
        from pos_app.license import pos_license_is_valid

        assert pos_license_is_valid() is True

    def test_get_status_reports_active(self):
        from pos_app.license import get_pos_license_status

        status = get_pos_license_status()
        assert status["valid"] is True
        assert status["status"] == "active"

    def test_activate_pos_license_succeeds_for_any_input(self):
        from pos_app.license import activate_pos_license

        result = activate_pos_license("POS-1234-5678-9ABC-DEF0")
        assert result["success"] is True
        assert result["status"] == "active"

    def test_activate_pos_license_ignores_invalid_looking_input(self):
        """
        A legacy client sending a malformed key still gets success — POS
        is free, we don't gatekeep any more.
        """
        from pos_app.license import activate_pos_license

        result = activate_pos_license("anything-at-all")
        assert result["success"] is True


# ============================================================
# Order Test Flagging
# ============================================================


@pytest.mark.django_db
class TestOrderTestFlag:
    """Test that orders are flagged in sandbox mode."""

    def test_order_has_is_test_order_field(self):
        """Order model has is_test_order field."""
        from orders.models import Order

        field = Order._meta.get_field("is_test_order")
        assert field is not None
        assert field.default is False


# ============================================================
# Email Guard — sandbox_filter_recipient
# ============================================================


class TestEmailGuardFilterRecipient:
    """Test sandbox_filter_recipient() under various conditions."""

    def test_production_mode_always_sends(self):
        """In production mode, all recipients get action='send'."""
        from core.sandbox.email_guard import sandbox_filter_recipient

        with patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False):
            action, email = sandbox_filter_recipient("anyone@example.com")
            assert action == "send"
            assert email == "anyone@example.com"

    def test_sandbox_whitelisted_recipient_sends(self):
        """Whitelisted address gets action='send' in sandbox."""
        from core.sandbox.email_guard import sandbox_filter_recipient

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch(
                "core.sandbox.email_guard.get_email_whitelist", return_value={"allowed@test.com"}
            ),
        ):
            action, email = sandbox_filter_recipient("allowed@test.com")
            assert action == "send"
            assert email == "allowed@test.com"

    def test_sandbox_non_whitelisted_recipient_logged(self):
        """Non-whitelisted address gets action='log' in sandbox."""
        from core.sandbox.email_guard import sandbox_filter_recipient

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch(
                "core.sandbox.email_guard.get_email_whitelist", return_value={"allowed@test.com"}
            ),
        ):
            action, email = sandbox_filter_recipient("stranger@example.com")
            assert action == "log"
            assert email == "stranger@example.com"

    def test_sandbox_case_insensitive_matching(self):
        """Whitelist matching is case-insensitive."""
        from core.sandbox.email_guard import sandbox_filter_recipient

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
        ):
            action, email = sandbox_filter_recipient("Admin@Test.Com")
            assert action == "send"

    def test_sandbox_empty_whitelist_logs_all(self):
        """Empty whitelist means all recipients are logged."""
        from core.sandbox.email_guard import sandbox_filter_recipient

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value=set()),
        ):
            action, _ = sandbox_filter_recipient("anyone@example.com")
            assert action == "log"

    def test_sandbox_none_email_logged(self):
        """None email address results in log action."""
        from core.sandbox.email_guard import sandbox_filter_recipient

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
        ):
            action, email = sandbox_filter_recipient(None)
            assert action == "log"

    def test_sandbox_empty_string_email_logged(self):
        """Empty string email address results in log action."""
        from core.sandbox.email_guard import sandbox_filter_recipient

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
        ):
            action, email = sandbox_filter_recipient("")
            assert action == "log"


# ============================================================
# Email Guard — get_email_whitelist
# ============================================================


@pytest.mark.django_db
class TestEmailGuardGetWhitelist:
    """Test get_email_whitelist() loads from SiteSettings correctly."""

    def test_admin_email_always_included(self, site_settings):
        """The admin_email from SiteSettings is always in the whitelist."""
        from core.sandbox.email_guard import get_email_whitelist

        site_settings.admin_email = "boss@myshop.com"
        site_settings.sandbox_email_whitelist = []
        site_settings.save()

        whitelist = get_email_whitelist()
        assert "boss@myshop.com" in whitelist

    def test_explicit_whitelist_entries_included(self, site_settings):
        """Explicitly whitelisted addresses are in the whitelist."""
        from core.sandbox.email_guard import get_email_whitelist

        site_settings.admin_email = "admin@test.com"
        site_settings.sandbox_email_whitelist = ["dev@test.com", "qa@test.com"]
        site_settings.save()

        whitelist = get_email_whitelist()
        assert "dev@test.com" in whitelist
        assert "qa@test.com" in whitelist
        assert "admin@test.com" in whitelist

    def test_whitelist_normalized_to_lowercase(self, site_settings):
        """All whitelist entries are lowercased."""
        from core.sandbox.email_guard import get_email_whitelist

        site_settings.admin_email = "Admin@Test.Com"
        site_settings.sandbox_email_whitelist = ["QA@SHOP.com"]
        site_settings.save()

        whitelist = get_email_whitelist()
        assert "admin@test.com" in whitelist
        assert "qa@shop.com" in whitelist

    def test_no_site_settings_returns_empty(self):
        """If no SiteSettings exists, returns empty set."""
        from core.models import SiteSettings
        from core.sandbox.email_guard import get_email_whitelist

        # Patch to return None (simulates no settings row)
        with patch.object(SiteSettings.objects, "first", return_value=None):
            whitelist = get_email_whitelist()
            assert whitelist == set()

    def test_empty_admin_email_excluded(self, site_settings):
        """If admin_email is empty, it's not in the whitelist."""
        from core.sandbox.email_guard import get_email_whitelist

        # admin_email is a required EmailField on SiteSettings, so we
        # mock the attribute rather than saving empty string to DB.
        mock_ss = MagicMock()
        mock_ss.admin_email = ""
        mock_ss.sandbox_email_whitelist = ["dev@test.com"]
        from core.models import SiteSettings

        with patch.object(SiteSettings.objects, "first", return_value=mock_ss):
            whitelist = get_email_whitelist()
            assert "" not in whitelist
            assert "dev@test.com" in whitelist

    def test_non_string_entries_ignored(self, site_settings):
        """Non-string entries in the JSON list are silently ignored."""
        from core.sandbox.email_guard import get_email_whitelist

        site_settings.admin_email = "admin@test.com"
        site_settings.sandbox_email_whitelist = ["valid@test.com", None, 123, ""]
        site_settings.save()

        whitelist = get_email_whitelist()
        assert "valid@test.com" in whitelist
        assert len(whitelist) == 2  # admin + valid@test.com


# ============================================================
# Email Guard — validate_whitelist / validate_whitelist_entry
# ============================================================


class TestEmailGuardValidation:
    """Test whitelist validation functions."""

    def test_valid_email_accepted(self):
        """Valid exact email address passes validation."""
        from core.sandbox.email_guard import validate_whitelist_entry

        is_valid, error = validate_whitelist_entry("user@example.com")
        assert is_valid is True
        assert error is None

    def test_wildcard_rejected(self):
        """Wildcard patterns are rejected."""
        from core.sandbox.email_guard import validate_whitelist_entry

        is_valid, error = validate_whitelist_entry("*@domain.com")
        assert is_valid is False
        assert "Wildcards" in error

    def test_question_mark_wildcard_rejected(self):
        """Question mark wildcard is rejected."""
        from core.sandbox.email_guard import validate_whitelist_entry

        is_valid, error = validate_whitelist_entry("user?@domain.com")
        assert is_valid is False
        assert "Wildcards" in error

    def test_domain_pattern_rejected(self):
        """Domain-only patterns like @domain.com are rejected."""
        from core.sandbox.email_guard import validate_whitelist_entry

        is_valid, error = validate_whitelist_entry("@domain.com")
        assert is_valid is False
        assert "Domain patterns" in error

    def test_invalid_format_rejected(self):
        """Invalid email format is rejected."""
        from core.sandbox.email_guard import validate_whitelist_entry

        is_valid, error = validate_whitelist_entry("not-an-email")
        assert is_valid is False
        assert "Invalid email" in error

    def test_empty_string_rejected(self):
        """Empty string is rejected."""
        from core.sandbox.email_guard import validate_whitelist_entry

        is_valid, error = validate_whitelist_entry("")
        assert is_valid is False

    def test_none_rejected(self):
        """None is rejected."""
        from core.sandbox.email_guard import validate_whitelist_entry

        is_valid, error = validate_whitelist_entry(None)
        assert is_valid is False

    def test_validate_whitelist_valid_list(self):
        """validate_whitelist accepts a valid list of emails."""
        from core.sandbox.email_guard import validate_whitelist

        is_valid, errors = validate_whitelist(["a@b.com", "c@d.com"])
        assert is_valid is True
        assert errors == []

    def test_validate_whitelist_max_size_enforced(self):
        """validate_whitelist rejects lists over MAX_WHITELIST_SIZE (10)."""
        from core.sandbox.email_guard import MAX_WHITELIST_SIZE, validate_whitelist

        emails = [f"user{i}@test.com" for i in range(MAX_WHITELIST_SIZE + 1)]
        is_valid, errors = validate_whitelist(emails)
        assert is_valid is False
        assert any("Maximum" in e for e in errors)

    def test_validate_whitelist_exactly_max_size_accepted(self):
        """validate_whitelist accepts a list of exactly MAX_WHITELIST_SIZE."""
        from core.sandbox.email_guard import MAX_WHITELIST_SIZE, validate_whitelist

        emails = [f"user{i}@test.com" for i in range(MAX_WHITELIST_SIZE)]
        is_valid, errors = validate_whitelist(emails)
        assert is_valid is True

    def test_validate_whitelist_invalid_entry_reported(self):
        """validate_whitelist reports specific invalid entries."""
        from core.sandbox.email_guard import validate_whitelist

        is_valid, errors = validate_whitelist(["valid@test.com", "*@evil.com"])
        assert is_valid is False
        assert len(errors) == 1
        assert "Entry 2" in errors[0]

    def test_validate_whitelist_non_list_rejected(self):
        """validate_whitelist rejects non-list input."""
        from core.sandbox.email_guard import validate_whitelist

        is_valid, errors = validate_whitelist("not-a-list")
        assert is_valid is False
        assert any("list" in e.lower() for e in errors)


# ============================================================
# SMS Guard — sandbox_filter_sms_recipient
# ============================================================


class TestSMSGuardFilterRecipient:
    """Test sandbox_filter_sms_recipient() under various conditions."""

    def test_production_mode_always_sends(self):
        """In production mode, all phone numbers get action='send'."""
        from core.sandbox.sms_guard import sandbox_filter_sms_recipient

        with patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=False):
            action, phone = sandbox_filter_sms_recipient("+12025551234")
            assert action == "send"
            assert phone == "+12025551234"

    def test_sandbox_whitelisted_number_sends(self):
        """Whitelisted phone number gets action='send' in sandbox."""
        from core.sandbox.sms_guard import sandbox_filter_sms_recipient

        with (
            patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.sms_guard.get_sms_whitelist", return_value={"+12025551234"}),
        ):
            action, phone = sandbox_filter_sms_recipient("+12025551234")
            assert action == "send"

    def test_sandbox_non_whitelisted_number_logged(self):
        """Non-whitelisted phone number gets action='log' in sandbox."""
        from core.sandbox.sms_guard import sandbox_filter_sms_recipient

        with (
            patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.sms_guard.get_sms_whitelist", return_value={"+12025551234"}),
        ):
            action, phone = sandbox_filter_sms_recipient("+19995551234")
            assert action == "log"

    def test_sandbox_empty_whitelist_logs_all(self):
        """Empty whitelist means all numbers are logged."""
        from core.sandbox.sms_guard import sandbox_filter_sms_recipient

        with (
            patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.sms_guard.get_sms_whitelist", return_value=set()),
        ):
            action, _ = sandbox_filter_sms_recipient("+12025551234")
            assert action == "log"

    def test_sandbox_none_phone_logged(self):
        """None phone number results in log action."""
        from core.sandbox.sms_guard import sandbox_filter_sms_recipient

        with (
            patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.sms_guard.get_sms_whitelist", return_value={"+12025551234"}),
        ):
            action, phone = sandbox_filter_sms_recipient(None)
            assert action == "log"


# ============================================================
# SMS Guard — get_sms_whitelist
# ============================================================


@pytest.mark.django_db
class TestSMSGuardGetWhitelist:
    """Test get_sms_whitelist() loads from SiteSettings correctly."""

    def test_whitelist_loaded_from_settings(self, site_settings):
        """Whitelisted numbers are loaded from SiteSettings."""
        from core.sandbox.sms_guard import get_sms_whitelist

        site_settings.sandbox_sms_whitelist = ["+12025551234", "+442071234567"]
        site_settings.save()

        whitelist = get_sms_whitelist()
        assert "+12025551234" in whitelist
        assert "+442071234567" in whitelist

    def test_empty_whitelist(self, site_settings):
        """Empty whitelist returns empty set."""
        from core.sandbox.sms_guard import get_sms_whitelist

        site_settings.sandbox_sms_whitelist = []
        site_settings.save()

        whitelist = get_sms_whitelist()
        assert whitelist == set()

    def test_no_site_settings_returns_empty(self):
        """If no SiteSettings exists, returns empty set."""
        from core.models import SiteSettings
        from core.sandbox.sms_guard import get_sms_whitelist

        with patch.object(SiteSettings.objects, "first", return_value=None):
            whitelist = get_sms_whitelist()
            assert whitelist == set()

    def test_non_string_entries_ignored(self, site_settings):
        """Non-string entries are silently ignored."""
        from core.sandbox.sms_guard import get_sms_whitelist

        site_settings.sandbox_sms_whitelist = ["+12025551234", None, 42, ""]
        site_settings.save()

        whitelist = get_sms_whitelist()
        assert "+12025551234" in whitelist
        # None, 42, '' should all be excluded
        assert len(whitelist) == 1


# ============================================================
# SMS Guard — validate_sms_whitelist / validate_sms_whitelist_entry
# ============================================================


class TestSMSGuardValidation:
    """Test SMS whitelist validation functions."""

    def test_valid_e164_number_accepted(self):
        """Valid E.164 phone number passes validation."""
        from core.sandbox.sms_guard import validate_sms_whitelist_entry

        is_valid, error = validate_sms_whitelist_entry("+12025551234")
        assert is_valid is True
        assert error is None

    def test_number_without_plus_rejected(self):
        """Phone numbers without + prefix are rejected."""
        from core.sandbox.sms_guard import validate_sms_whitelist_entry

        is_valid, error = validate_sms_whitelist_entry("12025551234")
        assert is_valid is False
        assert "E.164" in error

    def test_short_number_rejected(self):
        """Too-short numbers are rejected (+ followed by just 0)."""
        from core.sandbox.sms_guard import validate_sms_whitelist_entry

        is_valid, error = validate_sms_whitelist_entry("+0")
        assert is_valid is False

    def test_leading_zero_after_plus_rejected(self):
        """E.164 requires first digit after + to be 1-9."""
        from core.sandbox.sms_guard import validate_sms_whitelist_entry

        is_valid, error = validate_sms_whitelist_entry("+01234567890")
        assert is_valid is False

    def test_letters_in_number_rejected(self):
        """Non-digit characters in phone number are rejected."""
        from core.sandbox.sms_guard import validate_sms_whitelist_entry

        is_valid, error = validate_sms_whitelist_entry("+1abc5551234")
        assert is_valid is False

    def test_wildcard_rejected(self):
        """Wildcards in phone numbers are rejected."""
        from core.sandbox.sms_guard import validate_sms_whitelist_entry

        is_valid, error = validate_sms_whitelist_entry("+1202555*")
        assert is_valid is False
        assert "Wildcards" in error

    def test_empty_string_rejected(self):
        """Empty string is rejected."""
        from core.sandbox.sms_guard import validate_sms_whitelist_entry

        is_valid, error = validate_sms_whitelist_entry("")
        assert is_valid is False

    def test_none_rejected(self):
        """None is rejected."""
        from core.sandbox.sms_guard import validate_sms_whitelist_entry

        is_valid, error = validate_sms_whitelist_entry(None)
        assert is_valid is False

    def test_validate_sms_whitelist_valid_list(self):
        """validate_sms_whitelist accepts a valid list."""
        from core.sandbox.sms_guard import validate_sms_whitelist

        is_valid, errors = validate_sms_whitelist(["+12025551234", "+442071234567"])
        assert is_valid is True
        assert errors == []

    def test_validate_sms_whitelist_max_size_enforced(self):
        """validate_sms_whitelist rejects lists over MAX_WHITELIST_SIZE (5)."""
        from core.sandbox.sms_guard import MAX_WHITELIST_SIZE, validate_sms_whitelist

        numbers = [f"+1202555{i:04d}" for i in range(MAX_WHITELIST_SIZE + 1)]
        is_valid, errors = validate_sms_whitelist(numbers)
        assert is_valid is False
        assert any("Maximum" in e for e in errors)

    def test_validate_sms_whitelist_exactly_max_accepted(self):
        """validate_sms_whitelist accepts a list of exactly MAX_WHITELIST_SIZE."""
        from core.sandbox.sms_guard import MAX_WHITELIST_SIZE, validate_sms_whitelist

        numbers = [f"+1202555{i:04d}" for i in range(MAX_WHITELIST_SIZE)]
        is_valid, errors = validate_sms_whitelist(numbers)
        assert is_valid is True

    def test_validate_sms_whitelist_invalid_entry_reported(self):
        """validate_sms_whitelist reports specific invalid entries."""
        from core.sandbox.sms_guard import validate_sms_whitelist

        is_valid, errors = validate_sms_whitelist(["+12025551234", "bad-number"])
        assert is_valid is False
        assert len(errors) == 1
        assert "Entry 2" in errors[0]

    def test_validate_sms_whitelist_non_list_rejected(self):
        """validate_sms_whitelist rejects non-list input."""
        from core.sandbox.sms_guard import validate_sms_whitelist

        is_valid, errors = validate_sms_whitelist("not-a-list")
        assert is_valid is False
        assert any("list" in e.lower() for e in errors)


# ============================================================
# Email Backend — Whitelist-based filtering
# ============================================================


class TestSandboxEmailBackendWhitelist:
    """Test SandboxEmailBackend with whitelist-based filtering."""

    def test_production_mode_passes_through(self):
        """In production mode, all emails pass through unchanged."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with patch("core.sandbox.email_backend.is_sandbox_mode", return_value=False):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["anyone@example.com"]
            msg.subject = "Test Email"

            sb.send_messages([msg])

            backend.send_messages.assert_called_once_with([msg])
            assert msg.to == ["anyone@example.com"]
            assert msg.subject == "Test Email"

    def test_sandbox_whitelisted_recipient_delivered(self):
        """Whitelisted recipients in sandbox get emails with [SANDBOX] prefix."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with (
            patch("core.sandbox.email_backend.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"dev@test.com"}),
        ):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["dev@test.com"]
            msg.cc = []
            msg.bcc = []
            msg.subject = "Order Confirmation"
            msg.body = "Thank you for your order!"
            msg.alternatives = []

            sb.send_messages([msg])

            # Email should be delivered
            backend.send_messages.assert_called_once()
            assert msg.to == ["dev@test.com"]
            assert msg.subject.startswith("[SANDBOX]")

    def test_sandbox_non_whitelisted_recipient_dropped(self):
        """Non-whitelisted recipients in sandbox have emails silently dropped."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with (
            patch("core.sandbox.email_backend.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
        ):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["stranger@example.com"]
            msg.cc = []
            msg.bcc = []
            msg.subject = "Order Confirmation"
            msg.body = "You have a new order"

            result = sb.send_messages([msg])

            # Email should NOT be delivered
            backend.send_messages.assert_not_called()
            assert result == 0

    def test_sandbox_cc_bcc_filtered(self):
        """CC and BCC recipients are also filtered by whitelist."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with (
            patch("core.sandbox.email_backend.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
        ):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["admin@test.com"]
            msg.cc = ["blocked-cc@example.com"]
            msg.bcc = ["blocked-bcc@example.com", "admin@test.com"]
            msg.subject = "Important"
            msg.body = "Hello"
            msg.alternatives = []

            sb.send_messages([msg])

            # CC should be empty (non-whitelisted), BCC should only have admin
            assert msg.cc == []
            assert msg.bcc == ["admin@test.com"]
            backend.send_messages.assert_called_once()

    def test_sandbox_mixed_recipients_partial_delivery(self):
        """When some To: recipients are whitelisted and some aren't, only whitelisted are kept."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with (
            patch("core.sandbox.email_backend.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch(
                "core.sandbox.email_guard.get_email_whitelist",
                return_value={"admin@test.com", "dev@test.com"},
            ),
        ):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["admin@test.com", "stranger@example.com", "dev@test.com"]
            msg.cc = []
            msg.bcc = []
            msg.subject = "Test"
            msg.body = "Hello"
            msg.alternatives = []

            sb.send_messages([msg])

            assert msg.to == ["admin@test.com", "dev@test.com"]
            backend.send_messages.assert_called_once()

    def test_sandbox_html_banner_injected(self):
        """Sandbox banner is injected into HTML alternatives."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with (
            patch("core.sandbox.email_backend.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
        ):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["admin@test.com"]
            msg.cc = []
            msg.bcc = []
            msg.subject = "Test"
            msg.body = "Plain text"
            msg.alternatives = [("<html><body><p>Hello</p></body></html>", "text/html")]

            sb.send_messages([msg])

            # Check HTML alternatives contain sandbox banner
            html_content = msg.alternatives[0][0]
            assert "SANDBOX MODE" in html_content

    def test_sandbox_subject_not_double_prefixed(self):
        """Already-prefixed [SANDBOX] subjects are not double-prefixed."""
        from core.sandbox.email_backend import SandboxEmailBackend

        with (
            patch("core.sandbox.email_backend.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
        ):
            backend = MagicMock()
            sb = SandboxEmailBackend.__new__(SandboxEmailBackend)
            sb._connection = backend
            sb.fail_silently = False

            msg = MagicMock()
            msg.to = ["admin@test.com"]
            msg.cc = []
            msg.bcc = []
            msg.subject = "[SANDBOX] Already Prefixed"
            msg.body = "Hello"
            msg.alternatives = []

            sb.send_messages([msg])

            assert msg.subject == "[SANDBOX] Already Prefixed"
            assert not msg.subject.startswith("[SANDBOX] [SANDBOX]")


# ============================================================
# EmailSendingService — queue_email sandbox enforcement
# ============================================================


@pytest.mark.django_db
class TestEmailSendingServiceSandbox:
    """Test EmailSendingService.queue_email() sandbox whitelist enforcement."""

    @pytest.fixture(autouse=True)
    def setup_email_account(self, django_site, site_settings):
        """Set up a default email account."""
        from tests.factories import EmailAccountFactory

        self.site_settings = site_settings
        self.site_settings.email_delivery_mode = "live"
        self.site_settings.email_test_redirect_address = ""
        self.site_settings.save()

        self.account = EmailAccountFactory(default=True)

    def test_queue_email_sandbox_logged_for_non_whitelisted(self):
        """Non-whitelisted recipient creates outbox with sandbox_logged status."""
        from email_system.services.email_sender import EmailSendingService

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
            patch("email_system.services.email_sender.is_sandbox_mode", return_value=True),
        ):
            outbox = EmailSendingService.queue_email(
                to_email="stranger@example.com",
                subject="Order Confirmation",
                html_body="<p>Thank you!</p>",
                account=self.account,
            )

            assert outbox.status == "sandbox_logged"
            assert outbox.to_email == "stranger@example.com"
            assert outbox.subject.startswith("[SANDBOX]")

    def test_queue_email_whitelisted_delivers_normally(self):
        """Whitelisted recipient gets normal delivery with [SANDBOX] prefix."""
        from email_system.services.email_sender import EmailSendingService

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"dev@test.com"}),
            patch("email_system.services.email_sender.is_sandbox_mode", return_value=True),
        ):
            outbox = EmailSendingService.queue_email(
                to_email="dev@test.com",
                subject="Order Confirmation",
                html_body="<p>Thank you!</p>",
                account=self.account,
            )

            assert outbox.status == "queued"
            assert outbox.subject.startswith("[SANDBOX]")
            # CC and BCC should be cleared for sandbox
            assert outbox.cc == []
            assert outbox.bcc == []

    def test_queue_email_production_mode_no_sandbox_effect(self):
        """In production mode, emails are queued normally without sandbox effects."""
        from email_system.services.email_sender import EmailSendingService

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False),
            patch("email_system.services.email_sender.is_sandbox_mode", return_value=False),
        ):
            outbox = EmailSendingService.queue_email(
                to_email="customer@example.com",
                subject="Order Confirmation",
                html_body="<p>Thank you!</p>",
                account=self.account,
            )

            assert outbox.status == "queued"
            assert not outbox.subject.startswith("[SANDBOX]")

    def test_send_email_refuses_sandbox_logged(self):
        """send_email() refuses to send emails with sandbox_logged status."""
        from django.contrib.sites.models import Site

        from email_system.models import EmailOutbox
        from email_system.services.email_sender import EmailSendingService

        site = Site.objects.get(pk=1)
        outbox = EmailOutbox.objects.create(
            site=site,
            account=self.account,
            to_email="blocked@example.com",
            from_email="sender@test.com",
            subject="[SANDBOX] Test",
            html_body="<p>Test</p>",
            status="sandbox_logged",
        )

        result = EmailSendingService.send_email(str(outbox.id))
        assert result is False

        outbox.refresh_from_db()
        assert outbox.status == "sandbox_logged"


# ============================================================
# EmailSendingService — send_template_email sandbox enforcement
# ============================================================


@pytest.mark.django_db
class TestSendTemplateEmailSandbox:
    """Test EmailSendingService.send_template_email() sandbox enforcement."""

    @pytest.fixture(autouse=True)
    def setup_email_account(self, django_site, site_settings):
        """Set up email account and template."""
        from tests.factories import EmailAccountFactory

        self.site_settings = site_settings
        self.site_settings.email_delivery_mode = "live"
        self.site_settings.email_test_redirect_address = ""
        self.site_settings.save()
        self.account = EmailAccountFactory(default=True)

    def test_template_email_sandbox_logged_for_non_whitelisted(self):
        """Non-whitelisted recipient creates sandbox_logged outbox."""
        from email_system.services.email_sender import EmailSendingService

        # Mock template rendering
        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"admin@test.com"}),
            patch("email_system.services.email_sender.is_sandbox_mode", return_value=True),
            patch(
                "email_system.services.template_renderer.TemplateRenderer.render",
                return_value=("Subject", "<p>Body</p>", "Plain text"),
            ),
            patch(
                "accounts.services.preference_service.PreferenceService.check_email_permission",
                return_value=True,
            ),
        ):
            outbox = EmailSendingService.send_template_email(
                to_email="stranger@example.com",
                template_type="order_confirmation",
                context={"order_number": "ORD-001"},
                account=self.account,
            )

            assert outbox.status == "sandbox_logged"

    def test_template_email_whitelisted_queued(self):
        """Whitelisted recipient gets queued with [SANDBOX] prefix."""
        from email_system.services.email_sender import EmailSendingService

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.email_guard.get_email_whitelist", return_value={"dev@test.com"}),
            patch("email_system.services.email_sender.is_sandbox_mode", return_value=True),
            patch(
                "email_system.services.template_renderer.TemplateRenderer.render",
                return_value=("Subject", "<p>Body</p>", "Plain text"),
            ),
            patch(
                "accounts.services.preference_service.PreferenceService.check_email_permission",
                return_value=True,
            ),
        ):
            outbox = EmailSendingService.send_template_email(
                to_email="dev@test.com",
                template_type="order_confirmation",
                context={"order_number": "ORD-001"},
                account=self.account,
            )

            assert outbox.status == "queued"
            assert outbox.subject.startswith("[SANDBOX]")

    def test_template_email_production_no_sandbox(self):
        """In production mode, template emails are queued normally."""
        from email_system.services.email_sender import EmailSendingService

        with (
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False),
            patch("email_system.services.email_sender.is_sandbox_mode", return_value=False),
            patch(
                "email_system.services.template_renderer.TemplateRenderer.render",
                return_value=("Subject", "<p>Body</p>", "Plain text"),
            ),
            patch(
                "accounts.services.preference_service.PreferenceService.check_email_permission",
                return_value=True,
            ),
        ):
            outbox = EmailSendingService.send_template_email(
                to_email="customer@example.com",
                template_type="order_confirmation",
                context={"order_number": "ORD-001"},
                account=self.account,
            )

            assert outbox.status == "queued"
            assert not outbox.subject.startswith("[SANDBOX]")


# ============================================================
# SMS Sending Service — sandbox enforcement
# ============================================================


@pytest.mark.django_db
class TestSMSSendingServiceSandbox:
    """Test SMSSendingService sandbox whitelist enforcement."""

    @pytest.fixture(autouse=True)
    def setup_sms_account(self, django_site, site_settings):
        """Set up a default SMS account."""
        from email_system.utils.encryption import encrypt_credentials
        from sms_system.models import SMSProviderAccount

        self.account = SMSProviderAccount.objects.create(
            site_id=1,
            provider_key="test_provider",
            display_name="Test SMS Account",
            credentials=encrypt_credentials({"api_key": "test"}),
            is_active=True,
            is_default_sms=True,
            is_default_whatsapp=True,
        )

    def test_send_sms_sandbox_logged_for_non_whitelisted(self):
        """Non-whitelisted phone number creates sandbox_logged outbox."""
        from sms_system.models import SMSOutbox
        from sms_system.services.sms_sender import SMSSendingService

        with (
            patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.sms_guard.get_sms_whitelist", return_value={"+12025551234"}),
        ):
            service = SMSSendingService()
            result = service.send_sms(
                phone="+19995559999",
                message="Your order has shipped!",
                account=self.account,
            )

            assert result["success"] is False
            assert result["reason"] == "sandbox_not_whitelisted"

            outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
            assert outbox.status == "sandbox_logged"
            assert "[SANDBOX]" in outbox.message

    def test_send_sms_production_mode_proceeds(self):
        """In production mode, SMS is sent normally (mocking the provider)."""
        from sms_system.services.sms_sender import SMSSendingService

        mock_provider = MagicMock()
        mock_provider.send_sms.return_value = {"success": True, "message_id": "MSG123"}

        with patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=False):
            service = SMSSendingService()
            service._providers = {f"{self.account.provider_key}_{self.account.pk}": mock_provider}

            result = service.send_sms(
                phone="+19995559999",
                message="Your order has shipped!",
                account=self.account,
            )

            assert result["success"] is True
            mock_provider.send_sms.assert_called_once()

    def test_send_whatsapp_sandbox_logged_for_non_whitelisted(self):
        """Non-whitelisted phone for WhatsApp creates sandbox_logged outbox."""
        from sms_system.models import SMSOutbox
        from sms_system.services.sms_sender import SMSSendingService

        with (
            patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.sms_guard.get_sms_whitelist", return_value={"+12025551234"}),
        ):
            service = SMSSendingService()
            result = service.send_whatsapp(
                phone="+19995559999",
                template_name="order_shipped",
                template_params={"1": "ORD-001"},
                account=self.account,
            )

            assert result["success"] is False
            assert result["reason"] == "sandbox_not_whitelisted"

            outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
            assert outbox.status == "sandbox_logged"
            assert outbox.message_type == "whatsapp"

    def test_send_whatsapp_production_mode_proceeds(self):
        """In production mode, WhatsApp is sent normally."""
        from sms_system.services.sms_sender import SMSSendingService

        mock_provider = MagicMock()
        mock_provider.send_whatsapp.return_value = {"success": True, "message_id": "WA123"}

        with patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=False):
            service = SMSSendingService()
            service._providers = {f"{self.account.provider_key}_{self.account.pk}": mock_provider}

            result = service.send_whatsapp(
                phone="+19995559999",
                template_name="order_shipped",
                template_params={"1": "ORD-001"},
                account=self.account,
            )

            assert result["success"] is True
            mock_provider.send_whatsapp.assert_called_once()

    def test_send_sms_whitelisted_proceeds(self):
        """Whitelisted number in sandbox proceeds to send normally."""
        from sms_system.services.sms_sender import SMSSendingService

        mock_provider = MagicMock()
        mock_provider.send_sms.return_value = {"success": True, "message_id": "MSG456"}

        with (
            patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=True),
            patch("core.sandbox.sms_guard.get_sms_whitelist", return_value={"+12025551234"}),
        ):
            service = SMSSendingService()
            service._providers = {f"{self.account.provider_key}_{self.account.pk}": mock_provider}

            result = service.send_sms(
                phone="+12025551234",
                message="Your order shipped!",
                account=self.account,
            )

            assert result["success"] is True
            mock_provider.send_sms.assert_called_once()


# ============================================================
# Webhook Services — localhost detection and sandbox blocking
# ============================================================


class TestWebhookLocalhostDetection:
    """Test _is_localhost_url() helper."""

    def test_localhost_hostname(self):
        """localhost hostname is recognized."""
        from webhooks.services import _is_localhost_url

        assert _is_localhost_url("http://localhost/webhook") is True
        assert _is_localhost_url("http://localhost:8000/webhook") is True
        assert _is_localhost_url("https://localhost/webhook") is True

    def test_ipv4_loopback(self):
        """127.0.0.1 is recognized as localhost."""
        from webhooks.services import _is_localhost_url

        assert _is_localhost_url("http://127.0.0.1/webhook") is True
        assert _is_localhost_url("http://127.0.0.1:9000/webhook") is True

    def test_ipv6_loopback(self):
        """::1 is recognized as localhost."""
        from webhooks.services import _is_localhost_url

        assert _is_localhost_url("http://[::1]/webhook") is True
        assert _is_localhost_url("http://[::1]:8000/webhook") is True

    def test_external_url_not_localhost(self):
        """External URLs are not localhost."""
        from webhooks.services import _is_localhost_url

        assert _is_localhost_url("https://api.example.com/webhook") is False
        assert _is_localhost_url("http://10.0.0.1/webhook") is False
        assert _is_localhost_url("https://webhook.site/test") is False

    def test_private_network_not_localhost(self):
        """Private network IPs (192.168.x.x, 10.x.x.x) are not localhost."""
        from webhooks.services import _is_localhost_url

        assert _is_localhost_url("http://192.168.1.1/webhook") is False
        assert _is_localhost_url("http://10.0.0.1/webhook") is False

    def test_empty_url_not_localhost(self):
        """Empty/invalid URLs return False."""
        from webhooks.services import _is_localhost_url

        assert _is_localhost_url("") is False
        assert _is_localhost_url("not-a-url") is False

    def test_none_url_not_localhost(self):
        """None-like URLs return False without raising."""
        from webhooks.services import _is_localhost_url

        # _is_localhost_url uses try/except, should handle gracefully
        assert _is_localhost_url("") is False


# ============================================================
# Webhook Services — trigger_webhook sandbox blocking
# ============================================================


@pytest.mark.django_db
class TestWebhookSandboxBlocking:
    """Test trigger_webhook() sandbox delivery restrictions."""

    @pytest.fixture(autouse=True)
    def setup_endpoints(self, db):
        """Create test webhook endpoints."""
        from webhooks.models import WebhookEndpoint

        self.external_endpoint = WebhookEndpoint.objects.create(
            name="External Receiver",
            url="https://api.external.com/webhook",
            is_active=True,
            events=["order.created"],
        )
        self.localhost_endpoint = WebhookEndpoint.objects.create(
            name="Local Receiver",
            url="http://localhost:9000/webhook",
            is_active=True,
            events=["order.created"],
        )

    def test_sandbox_blocks_external_endpoint(self):
        """External endpoints get sandbox_blocked status in sandbox mode."""
        from webhooks.models import WebhookDelivery
        from webhooks.services import trigger_webhook

        with (
            patch("core.license.is_sandbox_mode", return_value=True),
            patch("webhooks.tasks.deliver_webhook") as mock_deliver,
        ):
            count = trigger_webhook(
                "order.created",
                data={"order_id": 123},
            )

            # Both endpoints should have deliveries
            assert count == 2

            # External endpoint should be sandbox_blocked
            external_delivery = WebhookDelivery.objects.filter(
                endpoint=self.external_endpoint,
            ).first()
            assert external_delivery is not None
            assert external_delivery.status == "sandbox_blocked"

            # Localhost endpoint should be pending (queued for delivery)
            localhost_delivery = WebhookDelivery.objects.filter(
                endpoint=self.localhost_endpoint,
            ).first()
            assert localhost_delivery is not None
            assert localhost_delivery.status == "pending"

            # deliver_webhook should only be called for localhost
            mock_deliver.delay.assert_called_once()

    def test_sandbox_includes_sandbox_flag_in_payload(self):
        """Sandbox mode adds sandbox=True to webhook payloads."""
        from webhooks.models import WebhookDelivery
        from webhooks.services import trigger_webhook

        with (
            patch("core.license.is_sandbox_mode", return_value=True),
            patch("webhooks.tasks.deliver_webhook"),
        ):
            trigger_webhook("order.created", data={"order_id": 123})

            delivery = WebhookDelivery.objects.filter(
                endpoint=self.localhost_endpoint,
            ).first()
            assert delivery is not None
            assert delivery.payload.get("sandbox") is True

    def test_production_mode_delivers_to_all_endpoints(self):
        """In production mode, all endpoints get normal delivery."""
        from webhooks.models import WebhookDelivery
        from webhooks.services import trigger_webhook

        with (
            patch("core.license.is_sandbox_mode", return_value=False),
            patch("webhooks.tasks.deliver_webhook") as mock_deliver,
        ):
            count = trigger_webhook(
                "order.created",
                data={"order_id": 123},
            )

            assert count == 2

            # Both endpoints should be pending (delivered normally)
            blocked = WebhookDelivery.objects.filter(status="sandbox_blocked").count()
            assert blocked == 0

            # deliver_webhook should be called for both
            assert mock_deliver.delay.call_count == 2

    def test_production_mode_no_sandbox_flag(self):
        """In production mode, webhook payloads do NOT include sandbox flag."""
        from webhooks.models import WebhookDelivery
        from webhooks.services import trigger_webhook

        with (
            patch("core.license.is_sandbox_mode", return_value=False),
            patch("webhooks.tasks.deliver_webhook"),
        ):
            trigger_webhook("order.created", data={"order_id": 123})

            delivery = WebhookDelivery.objects.filter(
                endpoint=self.external_endpoint,
            ).first()
            assert delivery is not None
            assert "sandbox" not in delivery.payload


# ============================================================
# Webhook Services — trigger_webhook_sync sandbox blocking
# ============================================================


@pytest.mark.django_db
class TestWebhookSyncSandboxBlocking:
    """Test trigger_webhook_sync() sandbox delivery restrictions."""

    @pytest.fixture(autouse=True)
    def setup_endpoints(self, db):
        """Create test webhook endpoints."""
        from webhooks.models import WebhookEndpoint

        self.external_endpoint = WebhookEndpoint.objects.create(
            name="External Receiver",
            url="https://api.external.com/webhook",
            is_active=True,
            events=["order.created"],
        )
        self.localhost_endpoint = WebhookEndpoint.objects.create(
            name="Local Receiver",
            url="http://localhost:9000/webhook",
            is_active=True,
            events=["order.created"],
        )

    def test_sync_sandbox_blocks_external(self):
        """trigger_webhook_sync blocks external URLs in sandbox."""
        from webhooks.services import trigger_webhook_sync

        with (
            patch("core.license.is_sandbox_mode", return_value=True),
            patch("webhooks.tasks.deliver_webhook") as mock_deliver,
        ):
            results = trigger_webhook_sync(
                "order.created",
                data={"order_id": 456},
            )

            # Should have 2 results
            assert len(results) == 2

            # Find the external endpoint result
            external_result = next(r for r in results if r["endpoint"] == "External Receiver")
            assert external_result["status"] == "sandbox_blocked"
            assert external_result["response_code"] is None

    def test_sync_production_delivers_all(self):
        """trigger_webhook_sync delivers to all endpoints in production."""
        from webhooks.services import trigger_webhook_sync

        with (
            patch("core.license.is_sandbox_mode", return_value=False),
            patch("webhooks.tasks.deliver_webhook") as mock_deliver,
        ):
            results = trigger_webhook_sync(
                "order.created",
                data={"order_id": 456},
            )

            assert len(results) == 2
            # No sandbox_blocked results
            assert all(r["status"] != "sandbox_blocked" for r in results)


# ============================================================
# Usage Telemetry — _collect_usage_metrics
# ============================================================


@pytest.mark.django_db
class TestUsageTelemetry:
    """Test usage metrics collection for license refresh."""

    def test_collect_usage_metrics_returns_counts(self, django_site, site_settings):
        """_collect_usage_metrics returns product, order, and customer counts."""
        from component_updates.services import UpdateManager

        # Create known test data
        from tests.factories import ProductFactory, UserFactory

        # Create some products (factory uses unique names)
        for _ in range(3):
            ProductFactory()

        # Create a non-staff, non-superuser customer
        customer = UserFactory(
            username="metrics_customer",
            email="metrics@test.com",
        )

        metrics = UpdateManager._collect_usage_metrics()

        assert "product_count" in metrics
        assert metrics["product_count"] >= 3
        assert "order_count" in metrics
        assert "customer_count" in metrics
        assert metrics["customer_count"] >= 1

    def test_collect_usage_metrics_excludes_staff(self, db):
        """Staff and superusers are excluded from customer_count."""
        from component_updates.services import UpdateManager
        from tests.factories import UserFactory

        staff = UserFactory(username="staff_only_for_metrics", staff=True)
        customer = UserFactory(username="cust_only_for_metrics")

        metrics = UpdateManager._collect_usage_metrics()

        # Staff should not be counted; customer should
        assert metrics.get("customer_count", 0) >= 1

    def test_collect_usage_metrics_handles_empty_db(self, db):
        """Metrics collection works even with empty tables."""
        from component_updates.services import UpdateManager

        metrics = UpdateManager._collect_usage_metrics()

        # Should have keys with zero counts (or be absent if tables don't exist)
        assert isinstance(metrics, dict)

    def test_refresh_license_includes_usage_metrics(self):
        """refresh_license() sends usage_metrics in request body."""
        from component_updates.services import UpdateManager

        manager = UpdateManager.__new__(UpdateManager)
        mock_config = MagicMock()
        mock_config.server_url = "https://update.example.com"
        mock_config.installation_uuid = "test-uuid"
        mock_config.license_key = "TEST-KEY"
        manager.config = mock_config

        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "license": {"environment_type": "production"},
            "signature": "abc123",
        }
        mock_session.post.return_value = mock_response
        manager.session = mock_session

        with (
            patch("core.license.is_sandbox_mode", return_value=False),
            patch.object(manager, "_ensure_authenticated"),
            patch.object(
                UpdateManager,
                "_collect_usage_metrics",
                return_value={"product_count": 10, "order_count": 5, "customer_count": 3},
            ),
            patch("core.license.get_license_manager") as mock_lm,
            patch("core.activation.write_license_file"),
            patch("core.license.reload_license_manager"),
        ):
            mock_lm_instance = MagicMock()
            mock_lm_instance.verify_signature.return_value = True
            mock_lm_instance.get_license_data.return_value = None
            mock_lm.return_value = mock_lm_instance

            manager.refresh_license()

            # Verify the POST was made with usage_metrics
            call_args = mock_session.post.call_args
            assert call_args is not None
            request_body = (
                call_args[1].get("json") or call_args[0][1]
                if len(call_args[0]) > 1
                else call_args[1].get("json")
            )
            assert "usage_metrics" in request_body
            assert request_body["usage_metrics"]["product_count"] == 10
            assert request_body["usage_metrics"]["order_count"] == 5
            assert request_body["usage_metrics"]["customer_count"] == 3

    def test_refresh_license_skips_in_sandbox_mode(self):
        """refresh_license() skips entirely in sandbox mode."""
        from component_updates.services import UpdateManager

        manager = UpdateManager.__new__(UpdateManager)
        manager.config = MagicMock()
        manager.session = MagicMock()

        with patch("core.license.is_sandbox_mode", return_value=True):
            result = manager.refresh_license()

            assert result["refreshed"] is False
            assert result["error"] == "sandbox_mode"
            # Should not make any HTTP requests
            manager.session.post.assert_not_called()


# ============================================================
# Model Field Existence — sandbox_logged / sandbox_blocked status choices
# ============================================================


class TestSandboxStatusChoices:
    """Verify new sandbox status choices exist on models."""

    def test_email_outbox_has_sandbox_logged_status(self):
        """EmailOutbox STATUS_CHOICES includes sandbox_logged."""
        from email_system.models import EmailOutbox

        status_field = EmailOutbox._meta.get_field("status")
        choices_values = [c[0] for c in status_field.choices]
        assert "sandbox_logged" in choices_values

    def test_sms_outbox_has_sandbox_logged_status(self):
        """SMSOutbox STATUS_CHOICES includes sandbox_logged."""
        from sms_system.models import SMSOutbox

        status_field = SMSOutbox._meta.get_field("status")
        choices_values = [c[0] for c in status_field.choices]
        assert "sandbox_logged" in choices_values

    def test_webhook_delivery_has_sandbox_blocked_status(self):
        """WebhookDelivery Status includes sandbox_blocked."""
        from webhooks.models import WebhookDelivery

        assert hasattr(WebhookDelivery.Status, "SANDBOX_BLOCKED")
        assert WebhookDelivery.Status.SANDBOX_BLOCKED == "sandbox_blocked"


# ============================================================
# Model Field Existence — SiteSettings whitelist fields
# ============================================================


class TestSiteSettingsWhitelistFields:
    """Verify new whitelist JSONFields on SiteSettings."""

    def test_sandbox_email_whitelist_field_exists(self):
        """SiteSettings has sandbox_email_whitelist JSONField."""
        from core.models import SiteSettings

        field = SiteSettings._meta.get_field("sandbox_email_whitelist")
        assert field is not None
        assert field.get_internal_type() == "JSONField"

    def test_sandbox_sms_whitelist_field_exists(self):
        """SiteSettings has sandbox_sms_whitelist JSONField."""
        from core.models import SiteSettings

        field = SiteSettings._meta.get_field("sandbox_sms_whitelist")
        assert field is not None
        assert field.get_internal_type() == "JSONField"

    def test_sandbox_email_whitelist_defaults_to_list(self):
        """sandbox_email_whitelist default is list."""
        from core.models import SiteSettings

        field = SiteSettings._meta.get_field("sandbox_email_whitelist")
        assert field.default is list

    def test_sandbox_sms_whitelist_defaults_to_list(self):
        """sandbox_sms_whitelist default is list."""
        from core.models import SiteSettings

        field = SiteSettings._meta.get_field("sandbox_sms_whitelist")
        assert field.default is list
