"""
Email System integration tests.

Tests models (CRUD, constraints, encryption, soft delete, versioning),
admin (changelist, AJAX endpoints), views (staff-only access enforcement),
tracking (open/click tracking, open redirect protection), services
(EmailSendingService), and security (auth, CSRF).
"""

import json
import uuid
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.sites.models import Site
from django.test import Client
from django.urls import reverse

from tests.factories import (
    EmailAccountFactory,
    EmailEventFactory,
    EmailOutboxFactory,
    EmailTemplateFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.email_system]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def staff_user(db):
    """Staff user for admin access."""
    return UserFactory(staff=True)


@pytest.fixture
def staff_client(staff_user):
    """Django test client authenticated as staff user."""
    client = Client()
    client.force_login(staff_user)
    return client


@pytest.fixture
def anon_client(db):
    """Unauthenticated Django test client."""
    return Client()


@pytest.fixture
def regular_user(db):
    """Non-staff user."""
    return UserFactory()


@pytest.fixture
def regular_client(regular_user):
    """Django test client authenticated as non-staff user."""
    client = Client()
    client.force_login(regular_user)
    return client


@pytest.fixture
def django_site(db):
    """Ensure Site pk=1 exists."""
    site, _ = Site.objects.update_or_create(pk=1, defaults={"domain": "testserver", "name": "Test"})
    return site


@pytest.fixture
def email_account(django_site):
    """Active non-default email account."""
    return EmailAccountFactory(site=django_site)


@pytest.fixture
def default_email_account(django_site):
    """Active default email account."""
    return EmailAccountFactory(site=django_site, default=True)


@pytest.fixture
def email_template(django_site):
    """Active email template."""
    return EmailTemplateFactory(site=django_site)


@pytest.fixture
def system_template(django_site):
    """Active system email template."""
    return EmailTemplateFactory(site=django_site, system=True)


@pytest.fixture
def outbox_entry(django_site, email_account):
    """Queued outbox entry."""
    return EmailOutboxFactory(site=django_site, account=email_account)


# ============================================================================
# 1. Models
# ============================================================================


class TestEmailAccountModel:
    """EmailAccount CRUD, constraints, and encryption."""

    def test_create_email_account(self, django_site):
        """EmailAccount can be created with valid data."""
        account = EmailAccountFactory(site=django_site, name="Primary Sender")
        account.refresh_from_db()
        assert account.name == "Primary Sender"
        assert account.is_active is True
        assert account.is_default is False
        assert account.connection_status == "unknown"
        assert account.provider_key == "builtin_smtp"

    def test_email_account_str(self, email_account):
        """__str__ includes name and email."""
        s = str(email_account)
        assert email_account.name in s
        assert email_account.from_email in s

    def test_update_email_account(self, email_account):
        """EmailAccount fields can be updated."""
        email_account.from_name = "Updated Name"
        email_account.save()
        email_account.refresh_from_db()
        assert email_account.from_name == "Updated Name"

    def test_delete_email_account(self, email_account):
        """EmailAccount can be deleted."""
        account_id = email_account.pk
        from email_system.models import EmailAccount

        email_account.delete()
        assert not EmailAccount.objects.filter(pk=account_id).exists()

    def test_unique_default_per_site(self, django_site):
        """Setting a new account as default unsets the previous default."""
        first = EmailAccountFactory(site=django_site, default=True)
        assert first.is_default is True

        second = EmailAccountFactory(site=django_site, default=True)
        first.refresh_from_db()
        assert second.is_default is True
        assert first.is_default is False

    def test_credential_encryption_roundtrip(self, django_site):
        """set_credentials / get_credentials encrypt and decrypt correctly."""
        account = EmailAccountFactory(site=django_site)
        creds = {
            "host": "smtp.example.com",
            "port": 587,
            "username": "user@example.com",
            "password": "s3cr3t!",
        }
        account.set_credentials(creds)
        account.save()
        account.refresh_from_db()

        decrypted = account.get_credentials()
        assert decrypted == creds

    def test_get_credentials_empty(self, django_site):
        """get_credentials returns empty dict when no credentials set."""
        account = EmailAccountFactory(site=django_site)
        # Set credentials to empty bytes
        account.credentials = b""
        account.save()
        account.refresh_from_db()
        assert account.get_credentials() == {}

    def test_connection_status_choices(self, email_account):
        """connection_status accepts valid choices."""
        for status in ("unknown", "connected", "error"):
            email_account.connection_status = status
            email_account.save()
            email_account.refresh_from_db()
            assert email_account.connection_status == status

    def test_ordering(self, django_site):
        """Accounts ordered by -is_default, -is_active, name."""
        from email_system.models import EmailAccount

        a = EmailAccountFactory(site=django_site, name="Bravo", is_active=True)
        b = EmailAccountFactory(site=django_site, name="Alpha", is_active=True, default=True)
        c = EmailAccountFactory(site=django_site, name="Charlie", inactive=True)

        ids = list(EmailAccount.objects.values_list("pk", flat=True))
        # Default first, then active by name, then inactive
        assert ids[0] == b.pk


class TestEmailTemplateModel:
    """EmailTemplate CRUD, soft delete, and versioning."""

    def test_create_template(self, django_site):
        """EmailTemplate can be created with valid data."""
        t = EmailTemplateFactory(
            site=django_site,
            template_type="order_confirmation",
            subject="Order #{{ order_number }}",
        )
        t.refresh_from_db()
        assert t.template_type == "order_confirmation"
        assert t.language_code == "en"
        assert t.is_active is True
        assert t.is_system is False
        assert t.version == 1

    def test_template_str(self, email_template):
        """__str__ shows type display and language."""
        s = str(email_template)
        assert "en" in s

    def test_soft_delete(self, email_template, staff_user):
        """delete() soft-deletes the template."""
        from email_system.models import EmailTemplate

        email_template.delete(user=staff_user)
        email_template.refresh_from_db()
        assert email_template.is_deleted is True
        assert email_template.deleted_at is not None
        assert email_template.deleted_by == staff_user
        # Default manager hides deleted templates
        assert not EmailTemplate.objects.filter(pk=email_template.pk).exists()
        # all_objects still finds it
        assert EmailTemplate.all_objects.filter(pk=email_template.pk).exists()

    def test_restore(self, email_template, staff_user):
        """restore() recovers a soft-deleted template."""
        from email_system.models import EmailTemplate

        email_template.delete(user=staff_user)
        email_template.restore()
        email_template.refresh_from_db()
        assert email_template.is_deleted is False
        assert email_template.deleted_at is None
        assert email_template.deleted_by is None
        assert EmailTemplate.objects.filter(pk=email_template.pk).exists()

    def test_hard_delete(self, email_template):
        """hard_delete() permanently removes the template."""
        from email_system.models import EmailTemplate

        pk = email_template.pk
        email_template.hard_delete()
        assert not EmailTemplate.all_objects.filter(pk=pk).exists()

    def test_clone_creates_copy(self, email_template, staff_user):
        """clone() creates a non-system copy with the same content."""
        clone = email_template.clone(user=staff_user, set_active=False)
        assert clone.pk != email_template.pk
        assert clone.template_type == email_template.template_type
        assert clone.subject == email_template.subject
        assert clone.html_content == email_template.html_content
        assert clone.is_system is False
        assert clone.created_by == staff_user

    def test_clone_with_set_active_deactivates_others(self, django_site, staff_user):
        """clone() with set_active=True deactivates other templates of same type/language."""
        original = EmailTemplateFactory(
            site=django_site, template_type="password_reset", is_active=True
        )
        clone = original.clone(user=staff_user, set_active=True)
        original.refresh_from_db()
        assert clone.is_active is True
        assert original.is_active is False

    def test_clone_with_language(self, django_site, staff_user):
        """clone() with clone_language uses translation content."""
        from email_system.models import EmailTemplateTranslation

        original = EmailTemplateFactory(
            site=django_site,
            template_type="shipping_confirmation",
            subject="Shipping Confirmation",
            language_code="en",
        )
        EmailTemplateTranslation.objects.create(
            template=original,
            language_code="es",
            subject="Confirmacion de Envio",
            html_content="<mjml><mj-body><mj-section><mj-column><mj-text>Hola</mj-text></mj-column></mj-section></mj-body></mjml>",
            text_content="Hola",
        )
        clone = original.clone(user=staff_user, clone_language="es")
        assert clone.subject == "Confirmacion de Envio"
        assert clone.language_code == "es"

    def test_create_version(self, email_template, staff_user):
        """create_version() snapshots current state and increments version."""
        original_version = email_template.version
        snapshot = email_template.create_version(user=staff_user)
        email_template.refresh_from_db()

        assert snapshot.version == original_version
        assert email_template.version == original_version + 1
        assert snapshot.is_active is False
        assert snapshot.subject == email_template.subject

    def test_get_active_template(self, django_site):
        """get_active_template returns active custom template over system."""
        from email_system.models import EmailTemplate

        system = EmailTemplateFactory(
            site=django_site,
            template_type="email_verification",
            system=True,
            is_active=True,
        )
        custom = EmailTemplateFactory(
            site=django_site,
            template_type="email_verification",
            is_active=True,
        )
        result = EmailTemplate.get_active_template("email_verification", site=django_site)
        assert result.pk == custom.pk

    def test_get_active_template_falls_back_to_english(self, django_site):
        """get_active_template falls back to English when requested language missing."""
        from email_system.models import EmailTemplate

        en_template = EmailTemplateFactory(
            site=django_site,
            template_type="refund_notification",
            language_code="en",
            is_active=True,
        )
        result = EmailTemplate.get_active_template(
            "refund_notification", site=django_site, language_code="fr"
        )
        assert result.pk == en_template.pk

    def test_get_active_template_not_found_raises(self, django_site):
        """get_active_template raises DoesNotExist when no template found."""
        from email_system.models import EmailTemplate

        with pytest.raises(EmailTemplate.DoesNotExist):
            EmailTemplate.get_active_template("nonexistent_type", site=django_site)

    def test_activate_deactivates_others(self, django_site):
        """activate() deactivates other templates of same type."""
        t1 = EmailTemplateFactory(
            site=django_site, template_type="delivery_confirmation", is_active=True
        )
        t2 = EmailTemplateFactory(
            site=django_site, template_type="delivery_confirmation", is_active=False
        )
        t2.activate()
        t1.refresh_from_db()
        assert t2.is_active is True
        assert t1.is_active is False

    def test_deactivate_restores_system_fallback(self, django_site):
        """deactivate() re-enables system template as fallback."""
        from email_system.models import EmailTemplate

        # Use a rare template_type to avoid collision with --reuse-db leftovers
        tt = "wishlist_shared_confirmation"
        # Clean up any leftover templates of this type from previous runs
        EmailTemplate.all_objects.filter(site=django_site, template_type=tt).delete()

        system = EmailTemplateFactory(
            site=django_site,
            template_type=tt,
            system=True,
            is_active=False,
        )
        custom = EmailTemplateFactory(
            site=django_site,
            template_type=tt,
            is_active=True,
        )
        custom.deactivate()
        system.refresh_from_db()
        assert custom.is_active is False
        assert system.is_active is True


class TestEmailOutboxModel:
    """EmailOutbox creation and status tracking."""

    def test_create_outbox_entry(self, django_site, email_account):
        """EmailOutbox can be created with queued status."""
        entry = EmailOutboxFactory(site=django_site, account=email_account)
        entry.refresh_from_db()
        assert entry.status == "queued"
        assert entry.priority == 5
        assert entry.retry_count == 0

    def test_outbox_str(self, outbox_entry):
        """__str__ shows subject, recipient, and status."""
        s = str(outbox_entry)
        assert outbox_entry.to_email in s

    def test_status_transitions(self, outbox_entry):
        """EmailOutbox supports valid status transitions."""
        for status in ("queued", "sending", "sent", "failed", "bounced", "skipped"):
            outbox_entry.status = status
            outbox_entry.save()
            outbox_entry.refresh_from_db()
            assert outbox_entry.status == status

    def test_sent_trait(self, django_site, email_account):
        """Sent trait sets status and sent_at."""
        entry = EmailOutboxFactory(site=django_site, account=email_account, sent=True)
        assert entry.status == "sent"
        assert entry.sent_at is not None

    def test_failed_trait(self, django_site, email_account):
        """Failed trait sets status, error, and failed_at."""
        entry = EmailOutboxFactory(site=django_site, account=email_account, failed=True)
        assert entry.status == "failed"
        assert entry.error_message == "Test error"
        assert entry.failed_at is not None

    def test_skipped_trait(self, django_site, email_account):
        """Skipped trait sets status and skip_reason."""
        entry = EmailOutboxFactory(site=django_site, account=email_account, skipped=True)
        assert entry.status == "skipped"
        assert entry.skip_reason == "user_preference_disabled"


class TestEmailEventModel:
    """EmailEvent creation and relationships."""

    def test_create_event(self, django_site, email_account):
        """EmailEvent can be created for an outbox entry."""
        outbox = EmailOutboxFactory(site=django_site, account=email_account)
        event = EmailEventFactory(email=outbox, event_type="delivered")
        event.refresh_from_db()
        assert event.event_type == "delivered"
        assert event.email_id == outbox.pk

    def test_event_str(self, django_site, email_account):
        """__str__ shows event type and subject."""
        outbox = EmailOutboxFactory(site=django_site, account=email_account, subject="Welcome!")
        event = EmailEventFactory(email=outbox, event_type="opened")
        s = str(event)
        assert "Welcome!" in s

    def test_bounce_event(self, django_site, email_account):
        """Bounce events store type and reason."""
        outbox = EmailOutboxFactory(site=django_site, account=email_account)
        event = EmailEventFactory(email=outbox, bounced=True)
        assert event.event_type == "bounced"
        assert event.bounce_type == "hard"
        assert event.bounce_reason == "Mailbox not found"

    def test_click_event_with_data(self, django_site, email_account):
        """Click events store URL in event_data."""
        outbox = EmailOutboxFactory(site=django_site, account=email_account)
        event = EmailEventFactory(
            email=outbox,
            clicked=True,
            event_data={"url": "https://shop.example.com/products/42/"},
        )
        assert event.event_data["url"] == "https://shop.example.com/products/42/"

    def test_event_relationship(self, django_site, email_account):
        """Events are accessible via outbox.events reverse relation."""
        outbox = EmailOutboxFactory(site=django_site, account=email_account)
        EmailEventFactory(email=outbox, event_type="delivered")
        EmailEventFactory(email=outbox, opened=True)
        assert outbox.events.count() == 2


class TestEmailDNSCheck:
    """EmailDNSCheck model creation and properties."""

    def test_create_dns_check(self, email_account, staff_user):
        """EmailDNSCheck can be created."""
        from email_system.models import EmailDNSCheck

        check = EmailDNSCheck.objects.create(
            account=email_account,
            domain="test.spwig.com",
            spf_status="pass",
            spf_record="v=spf1 include:_spf.google.com ~all",
            dkim_status="pass",
            dmarc_status="pass",
            propagation_status="full",
            overall_status="pass",
            checked_by=staff_user,
        )
        check.refresh_from_db()
        assert check.overall_status == "pass"
        assert check.is_valid is True
        assert check.has_warnings is False

    def test_dns_check_warning(self, email_account, staff_user):
        """has_warnings returns True for warn status."""
        from email_system.models import EmailDNSCheck

        check = EmailDNSCheck.objects.create(
            account=email_account,
            domain="test.spwig.com",
            overall_status="warn",
            checked_by=staff_user,
        )
        assert check.is_valid is False
        assert check.has_warnings is True


# ============================================================================
# 2. Admin
# ============================================================================


class TestEmailAccountAdmin:
    """EmailAccount admin changelist and AJAX endpoints."""

    def test_account_changelist_loads(self, staff_client, email_account):
        """GET account changelist returns 200."""
        url = "/en/admin/email_system/emailaccount/"
        resp = staff_client.get(url)
        assert resp.status_code == 200

    def test_outbox_changelist_loads(self, staff_client, outbox_entry):
        """GET outbox changelist returns 200."""
        url = "/en/admin/email_system/emailoutbox/"
        resp = staff_client.get(url)
        assert resp.status_code == 200


class TestEmailAccountAJAXEndpoints:
    """AJAX endpoints for email account management."""

    def _ajax_post(self, client, url, data=None):
        """Helper for AJAX POST requests with CSRF."""
        kwargs = {
            "content_type": "application/json",
            "HTTP_X_REQUESTED_WITH": "XMLHttpRequest",
        }
        body = json.dumps(data) if data else ""
        return client.post(url, body, **kwargs)

    def test_toggle_active(self, staff_client, email_account):
        """Toggle account active/inactive."""
        url = f"/en/admin/email-system/accounts/{email_account.pk}/toggle-active/"
        resp = self._ajax_post(staff_client, url)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        email_account.refresh_from_db()
        assert email_account.is_active is False

    def test_toggle_active_twice(self, staff_client, email_account):
        """Toggling twice restores original state."""
        url = f"/en/admin/email-system/accounts/{email_account.pk}/toggle-active/"
        self._ajax_post(staff_client, url)
        self._ajax_post(staff_client, url)
        email_account.refresh_from_db()
        assert email_account.is_active is True

    def test_set_default(self, staff_client, email_account, django_site):
        """Set an account as default."""
        url = f"/en/admin/email-system/accounts/{email_account.pk}/set-default/"
        resp = self._ajax_post(staff_client, url)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        email_account.refresh_from_db()
        assert email_account.is_default is True

    def test_set_default_inactive_fails(self, staff_client, django_site):
        """Cannot set inactive account as default."""
        account = EmailAccountFactory(site=django_site, inactive=True)
        url = f"/en/admin/email-system/accounts/{account.pk}/set-default/"
        resp = self._ajax_post(staff_client, url)
        assert resp.status_code == 400
        assert resp.json()["success"] is False

    def test_test_connection(self, staff_client, email_account):
        """Test connection endpoint calls provider healthcheck."""
        mock_provider = MagicMock()
        mock_provider.healthcheck.return_value = {"success": True, "message": "OK"}

        with patch.object(type(email_account), "get_provider_instance", return_value=mock_provider):
            url = f"/en/admin/email-system/accounts/{email_account.pk}/test-connection/"
            resp = self._ajax_post(staff_client, url)
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True

        email_account.refresh_from_db()
        assert email_account.connection_status == "connected"

    def test_delete_account(self, staff_client, email_account):
        """Delete a non-default account."""
        from email_system.models import EmailAccount

        pk = email_account.pk
        url = f"/en/admin/email-system/accounts/{pk}/delete/"
        resp = self._ajax_post(staff_client, url)
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert not EmailAccount.objects.filter(pk=pk).exists()

    def test_cannot_delete_default_account(self, staff_client, default_email_account):
        """Default account cannot be deleted."""
        url = f"/en/admin/email-system/accounts/{default_email_account.pk}/delete/"
        resp = self._ajax_post(staff_client, url)
        assert resp.status_code == 400
        assert resp.json()["success"] is False

    def test_delete_nonexistent_account(self, staff_client):
        """Deleting nonexistent account returns 404."""
        fake_id = uuid.uuid4()
        url = f"/en/admin/email-system/accounts/{fake_id}/delete/"
        resp = self._ajax_post(staff_client, url)
        assert resp.status_code == 404

    def test_bulk_enable(self, staff_client, django_site):
        """Bulk enable action activates multiple accounts."""
        a1 = EmailAccountFactory(site=django_site, inactive=True)
        a2 = EmailAccountFactory(site=django_site, inactive=True)
        url = "/en/admin/email-system/accounts/bulk-action/"
        resp = self._ajax_post(
            staff_client,
            url,
            {
                "action": "enable",
                "account_ids": [str(a1.pk), str(a2.pk)],
            },
        )
        assert resp.status_code == 200
        a1.refresh_from_db()
        a2.refresh_from_db()
        assert a1.is_active is True
        assert a2.is_active is True

    def test_bulk_disable(self, staff_client, django_site):
        """Bulk disable action deactivates multiple accounts."""
        a1 = EmailAccountFactory(site=django_site)
        a2 = EmailAccountFactory(site=django_site)
        url = "/en/admin/email-system/accounts/bulk-action/"
        resp = self._ajax_post(
            staff_client,
            url,
            {
                "action": "disable",
                "account_ids": [str(a1.pk), str(a2.pk)],
            },
        )
        assert resp.status_code == 200
        a1.refresh_from_db()
        a2.refresh_from_db()
        assert a1.is_active is False
        assert a2.is_active is False

    def test_bulk_delete_blocks_default(self, staff_client, default_email_account, django_site):
        """Bulk delete blocks if selection includes default account."""
        other = EmailAccountFactory(site=django_site)
        url = "/en/admin/email-system/accounts/bulk-action/"
        resp = self._ajax_post(
            staff_client,
            url,
            {
                "action": "delete",
                "account_ids": [str(default_email_account.pk), str(other.pk)],
            },
        )
        assert resp.status_code == 400
        assert resp.json()["success"] is False

    def test_bulk_action_unknown_action(self, staff_client, email_account):
        """Unknown bulk action returns 400."""
        url = "/en/admin/email-system/accounts/bulk-action/"
        resp = self._ajax_post(
            staff_client,
            url,
            {
                "action": "fly_to_moon",
                "account_ids": [str(email_account.pk)],
            },
        )
        assert resp.status_code == 400

    def test_bulk_action_empty_selection(self, staff_client):
        """Bulk action with no account_ids returns 400."""
        url = "/en/admin/email-system/accounts/bulk-action/"
        resp = self._ajax_post(
            staff_client,
            url,
            {
                "action": "enable",
                "account_ids": [],
            },
        )
        assert resp.status_code == 400


class TestEmailOutboxFilter:
    """AJAX filter endpoint for outbox."""

    def test_filter_outbox(self, staff_client, outbox_entry):
        """GET filter endpoint returns HTML and count."""
        url = "/en/admin/email-system/outbox/filter/"
        resp = staff_client.get(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "html" in data
        assert "count" in data
        assert data["count"] >= 1

    def test_filter_outbox_by_status(self, staff_client, django_site, email_account):
        """Filter by status returns only matching emails."""
        EmailOutboxFactory(site=django_site, account=email_account, status="queued")
        EmailOutboxFactory(site=django_site, account=email_account, sent=True)
        url = "/en/admin/email-system/outbox/filter/?status=sent"
        resp = staff_client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_outbox_non_ajax_rejected(self, staff_client, outbox_entry):
        """Non-AJAX request to filter endpoint returns 400."""
        url = "/en/admin/email-system/outbox/filter/"
        resp = staff_client.get(url)
        assert resp.status_code == 400


# ============================================================================
# 3. Views (staff-only access enforcement)
# ============================================================================


class TestViewStaffAccess:
    """All email system views require staff authentication."""

    @pytest.fixture(autouse=True)
    def _setup_template(self, email_template):
        """Provide a template for URL generation."""
        self.template = email_template

    STAFF_VIEWS = [
        "email_system:template_list",
        "email_system:newsletter_list",
        "email_system:translation_manager",
    ]

    STAFF_VIEWS_WITH_TEMPLATE_ID = [
        "email_system:template_edit",
        "email_system:template_preview",
    ]

    def test_anon_redirect_to_login(self, anon_client):
        """Anonymous users are redirected to admin login."""
        for url_name in self.STAFF_VIEWS:
            url = reverse(url_name)
            resp = anon_client.get(url)
            assert resp.status_code == 302, f"{url_name} did not redirect anon user"
            assert "/admin/" in resp.url or "/login/" in resp.url

    def test_anon_redirect_template_views(self, anon_client):
        """Anonymous users redirected from template-specific views."""
        for url_name in self.STAFF_VIEWS_WITH_TEMPLATE_ID:
            url = reverse(url_name, args=[self.template.pk])
            resp = anon_client.get(url)
            assert resp.status_code == 302, f"{url_name} did not redirect anon user"

    def test_regular_user_redirect(self, regular_client):
        """Non-staff users are redirected to admin login."""
        for url_name in self.STAFF_VIEWS:
            url = reverse(url_name)
            resp = regular_client.get(url)
            assert resp.status_code == 302, f"{url_name} did not redirect non-staff user"

    def test_wizard_step1_requires_staff(self, anon_client):
        """Wizard step 1 requires staff authentication."""
        url = reverse("email_system:wizard_step1")
        resp = anon_client.get(url)
        assert resp.status_code == 302

    def test_provider_browse_requires_staff(self, anon_client):
        """Provider browse view requires staff authentication."""
        url = reverse("email_system:provider_browse")
        resp = anon_client.get(url)
        assert resp.status_code == 302


class TestAdminAJAXSecurity:
    """AJAX endpoints require staff authentication."""

    AJAX_URLS = [
        "/en/admin/email-system/outbox/filter/",
    ]

    def _make_account_urls(self, account_id):
        return [
            f"/en/admin/email-system/accounts/{account_id}/toggle-active/",
            f"/en/admin/email-system/accounts/{account_id}/set-default/",
            f"/en/admin/email-system/accounts/{account_id}/test-connection/",
            f"/en/admin/email-system/accounts/{account_id}/delete/",
        ]

    def test_anon_ajax_get_redirected(self, anon_client):
        """Anonymous AJAX GET requests redirected to login."""
        for url in self.AJAX_URLS:
            resp = anon_client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            assert resp.status_code == 302, f"{url} did not redirect anon"

    def test_anon_ajax_post_redirected(self, anon_client, email_account):
        """Anonymous AJAX POST requests redirected to login."""
        for url in self._make_account_urls(email_account.pk):
            resp = anon_client.post(
                url,
                "{}",
                content_type="application/json",
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            )
            assert resp.status_code == 302, f"{url} did not redirect anon"

    def test_regular_user_ajax_redirected(self, regular_client, email_account):
        """Non-staff AJAX POST requests redirected to login."""
        for url in self._make_account_urls(email_account.pk):
            resp = regular_client.post(
                url,
                "{}",
                content_type="application/json",
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            )
            assert resp.status_code == 302, f"{url} did not redirect non-staff"

    def test_bulk_action_requires_staff(self, anon_client):
        """Bulk action endpoint requires staff."""
        url = "/en/admin/email-system/accounts/bulk-action/"
        resp = anon_client.post(
            url,
            json.dumps({"action": "enable", "account_ids": []}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert resp.status_code == 302


# ============================================================================
# 4. Tracking
# ============================================================================


class TestTrackOpen:
    """Track open endpoint returns pixel and records event."""

    def test_track_open_returns_gif_pixel(self, anon_client, outbox_entry):
        """GET track/open returns 1x1 transparent GIF."""
        from email_system.services.tracking_service import TrackingService

        ts = TrackingService()
        tracking_id = ts._generate_tracking_id(str(outbox_entry.pk))

        url = f"/email/track/open/{tracking_id}/"
        resp = anon_client.get(url)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "image/gif"
        assert resp["Cache-Control"] == "no-cache, no-store, must-revalidate"
        # 1x1 GIF is 43 bytes
        assert len(resp.content) == 43

    def test_track_open_creates_event(self, anon_client, outbox_entry):
        """Track open creates an EmailEvent record."""
        from email_system.models import EmailEvent
        from email_system.services.tracking_service import TrackingService

        ts = TrackingService()
        tracking_id = ts._generate_tracking_id(str(outbox_entry.pk))

        url = f"/email/track/open/{tracking_id}/"
        anon_client.get(url)

        event = EmailEvent.objects.filter(email=outbox_entry, event_type="opened").first()
        assert event is not None

    def test_track_open_deduplication(self, anon_client, outbox_entry):
        """Multiple opens do not create duplicate events."""
        from email_system.models import EmailEvent
        from email_system.services.tracking_service import TrackingService

        ts = TrackingService()
        tracking_id = ts._generate_tracking_id(str(outbox_entry.pk))

        url = f"/email/track/open/{tracking_id}/"
        anon_client.get(url)
        anon_client.get(url)

        count = EmailEvent.objects.filter(email=outbox_entry, event_type="opened").count()
        assert count == 1

    def test_track_open_invalid_id_returns_pixel(self, anon_client):
        """Invalid tracking ID still returns pixel (graceful degradation)."""
        url = "/email/track/open/invalid-tracking-id/"
        resp = anon_client.get(url)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "image/gif"

    def test_track_open_no_language_prefix(self, anon_client, outbox_entry):
        """Tracking URLs work without /en/ language prefix."""
        from email_system.services.tracking_service import TrackingService

        ts = TrackingService()
        tracking_id = ts._generate_tracking_id(str(outbox_entry.pk))

        # Verify it works at /email/track/open/ (no /en/ prefix)
        url = f"/email/track/open/{tracking_id}/"
        assert not url.startswith("/en/")
        resp = anon_client.get(url)
        assert resp.status_code == 200


class TestTrackClick:
    """Track click endpoint redirects and records event."""

    def _get_tracking_id(self, outbox_entry):
        from email_system.services.tracking_service import TrackingService

        ts = TrackingService()
        return ts._generate_tracking_id(str(outbox_entry.pk))

    def test_track_click_redirects(self, anon_client, outbox_entry):
        """Click tracking redirects to original URL."""
        tracking_id = self._get_tracking_id(outbox_entry)
        dest = "https://shop.example.com/products/42/"
        url = f"/email/track/click/{tracking_id}/?url={dest}"
        resp = anon_client.get(url)
        assert resp.status_code == 302
        assert resp["Location"] == dest

    def test_track_click_creates_event(self, anon_client, outbox_entry):
        """Click tracking creates an EmailEvent record."""
        from email_system.models import EmailEvent

        tracking_id = self._get_tracking_id(outbox_entry)
        dest = "https://shop.example.com/sale/"
        url = f"/email/track/click/{tracking_id}/?url={dest}"
        anon_client.get(url)

        event = EmailEvent.objects.filter(email=outbox_entry, event_type="clicked").first()
        assert event is not None
        assert event.event_data["url"] == dest

    def test_track_click_missing_url_404(self, anon_client, outbox_entry):
        """Missing url parameter returns 404."""
        tracking_id = self._get_tracking_id(outbox_entry)
        url = f"/email/track/click/{tracking_id}/"
        resp = anon_client.get(url)
        assert resp.status_code == 404

    def test_track_click_blocks_javascript_urls(self, anon_client, outbox_entry):
        """javascript: URLs are rejected (XSS protection)."""
        tracking_id = self._get_tracking_id(outbox_entry)
        url = f"/email/track/click/{tracking_id}/?url=javascript:alert(1)"
        resp = anon_client.get(url)
        assert resp.status_code == 404

    def test_track_click_blocks_data_urls(self, anon_client, outbox_entry):
        """data: URLs are rejected."""
        tracking_id = self._get_tracking_id(outbox_entry)
        url = f"/email/track/click/{tracking_id}/?url=data:text/html,<h1>evil</h1>"
        resp = anon_client.get(url)
        assert resp.status_code == 404

    def test_track_click_allows_http(self, anon_client, outbox_entry):
        """http:// URLs are allowed (external partner links)."""
        tracking_id = self._get_tracking_id(outbox_entry)
        dest = "http://partner.example.com/offer/"
        url = f"/email/track/click/{tracking_id}/?url={dest}"
        resp = anon_client.get(url)
        assert resp.status_code == 302
        assert resp["Location"] == dest

    def test_track_click_no_language_prefix(self, anon_client, outbox_entry):
        """Click tracking URLs work without /en/ language prefix."""
        tracking_id = self._get_tracking_id(outbox_entry)
        dest = "https://shop.example.com/"
        url = f"/email/track/click/{tracking_id}/?url={dest}"
        assert not url.startswith("/en/")
        resp = anon_client.get(url)
        assert resp.status_code == 302


# ============================================================================
# 5. Services (EmailSendingService)
# ============================================================================


class TestEmailSendingService:
    """EmailSendingService queue and send logic."""

    def test_queue_email_creates_outbox(self, default_email_account, django_site):
        """queue_email creates an EmailOutbox with status 'queued'.

        Also patch the guard module because `is_sandbox_mode` is imported into it
        at module load; patching only core.license.is_sandbox_mode is not enough.
        """
        from email_system.models import EmailOutbox
        from email_system.services.email_sender import EmailSendingService

        with (
            patch("core.license.is_sandbox_mode", return_value=False),
            patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False),
            patch("email_system.services.email_sender.is_sandbox_mode", return_value=False),
        ):
            outbox = EmailSendingService.queue_email(
                to_email="customer@example.com",
                subject="Your Order",
                html_body="<p>Thanks!</p>",
                account=default_email_account,
                site=django_site,
            )

        assert isinstance(outbox, EmailOutbox)
        assert outbox.status == "queued"
        assert outbox.to_email == "customer@example.com"
        assert outbox.subject == "Your Order"
        assert outbox.from_email == default_email_account.from_email

    def test_queue_email_uses_default_account(self, default_email_account, django_site):
        """queue_email uses default account when none specified."""
        from email_system.services.email_sender import EmailSendingService

        with patch("core.license.is_sandbox_mode", return_value=False):
            outbox = EmailSendingService.queue_email(
                to_email="test@example.com",
                subject="Test",
                html_body="<p>Test</p>",
                site=django_site,
            )

        assert outbox.account_id == default_email_account.pk

    def test_queue_email_no_account_raises(self, django_site):
        """queue_email raises ValueError when no active account exists."""
        from email_system.models import EmailAccount
        from email_system.services.email_sender import EmailSendingService

        # Clear all accounts for this site to ensure no fallback exists
        EmailAccount.objects.filter(site=django_site).delete()

        with patch("core.license.is_sandbox_mode", return_value=False):
            with pytest.raises(ValueError, match="No active email account"):
                EmailSendingService.queue_email(
                    to_email="test@example.com",
                    subject="Test",
                    html_body="<p>Test</p>",
                    site=django_site,
                )

    def test_queue_email_with_priority(self, default_email_account, django_site):
        """queue_email respects custom priority."""
        from email_system.services.email_sender import EmailSendingService

        with patch("core.license.is_sandbox_mode", return_value=False):
            outbox = EmailSendingService.queue_email(
                to_email="test@example.com",
                subject="Urgent",
                html_body="<p>Important</p>",
                account=default_email_account,
                site=django_site,
                priority=1,
            )

        assert outbox.priority == 1

    def test_queue_email_preference_check_skips_marketing(self, default_email_account, django_site):
        """Marketing email is skipped when user preference is disabled."""
        from email_system.services.email_sender import EmailSendingService

        user = UserFactory(email="prefuser@test.com")

        with (
            patch("core.license.is_sandbox_mode", return_value=False),
            patch(
                "accounts.services.preference_service.PreferenceService.check_email_permission",
                return_value=False,
            ),
        ):
            outbox = EmailSendingService.queue_email(
                to_email="prefuser@test.com",
                subject="Newsletter",
                html_body="<p>Sale!</p>",
                template_type="newsletter",
                account=default_email_account,
                site=django_site,
            )

        assert outbox.status == "skipped"
        assert outbox.skip_reason == "user_preference_disabled"

    def test_queue_email_transactional_always_sends(self, default_email_account, django_site):
        """Transactional email sends regardless of marketing preferences."""
        from email_system.services.email_sender import EmailSendingService

        user = UserFactory(email="txn@test.com")

        with (
            patch("core.license.is_sandbox_mode", return_value=False),
            patch(
                "accounts.services.preference_service.PreferenceService.check_email_permission",
                return_value=True,
            ),
        ):
            outbox = EmailSendingService.queue_email(
                to_email="txn@test.com",
                subject="Order Confirmed",
                html_body="<p>Order details</p>",
                template_type="order_confirmation",
                account=default_email_account,
                site=django_site,
            )

        assert outbox.status == "queued"

    def test_get_default_account(self, default_email_account, django_site):
        """get_default_account returns the default active account."""
        from email_system.services.email_sender import EmailSendingService

        account = EmailSendingService.get_default_account(site=django_site)
        assert account is not None
        assert account.pk == default_email_account.pk

    def test_get_default_account_falls_back(self, django_site):
        """get_default_account falls back to any active account when no default."""
        from email_system.models import EmailAccount
        from email_system.services.email_sender import EmailSendingService

        # Clear all accounts for this site to isolate the test
        EmailAccount.objects.filter(site=django_site).delete()
        fallback = EmailAccountFactory(site=django_site, is_default=False)
        account = EmailSendingService.get_default_account(site=django_site)
        assert account is not None
        assert account.pk == fallback.pk

    def test_get_default_account_none(self, django_site):
        """get_default_account returns None when no active accounts exist."""
        from email_system.models import EmailAccount
        from email_system.services.email_sender import EmailSendingService

        # Clear all accounts for this site to isolate the test
        EmailAccount.objects.filter(site=django_site).delete()
        account = EmailSendingService.get_default_account(site=django_site)
        assert account is None


# ============================================================================
# 6. Encryption utilities
# ============================================================================


class TestEncryptionUtils:
    """Encryption roundtrip and redaction."""

    def test_encrypt_decrypt_roundtrip(self):
        """encrypt_credentials / decrypt_credentials are inverse operations."""
        from email_system.utils.encryption import decrypt_credentials, encrypt_credentials

        creds = {"api_key": "sk-12345", "region": "us-east-1"}
        encrypted = encrypt_credentials(creds)
        assert isinstance(encrypted, bytes)
        decrypted = decrypt_credentials(encrypted)
        assert decrypted == creds

    def test_redact_credentials(self):
        """redact_credentials masks sensitive fields."""
        from email_system.utils.encryption import redact_credentials

        creds = {"api_key": "abcdefghijk", "host": "smtp.example.com"}
        redacted = redact_credentials(creds)
        assert redacted["api_key"] == "abc***ijk"
        assert redacted["host"] == "smtp.example.com"

    def test_redact_short_secret(self):
        """Short secrets are fully masked."""
        from email_system.utils.encryption import redact_credentials

        creds = {"password": "123"}
        redacted = redact_credentials(creds)
        assert redacted["password"] == "***"


# ============================================================================
# 7. URL Resolution
# ============================================================================


class TestURLResolution:
    """Verify URL names resolve correctly."""

    def test_tracking_open_url(self):
        """email_tracking:track_open resolves without language prefix."""
        url = reverse("email_tracking:track_open", args=["test-tracking-id"])
        assert url == "/email/track/open/test-tracking-id/"
        assert not url.startswith("/en/")

    def test_tracking_click_url(self):
        """email_tracking:track_click resolves without language prefix."""
        url = reverse("email_tracking:track_click", args=["test-tracking-id"])
        assert url == "/email/track/click/test-tracking-id/"
        assert not url.startswith("/en/")

    def test_template_list_url(self):
        """email_system:template_list resolves with language prefix."""
        url = reverse("email_system:template_list")
        assert "/admin/email-system/templates/" in url

    def test_newsletter_list_url(self):
        """email_system:newsletter_list resolves with language prefix."""
        url = reverse("email_system:newsletter_list")
        assert "/admin/email-system/newsletters/" in url

    def test_wizard_step1_url(self):
        """email_system:wizard_step1 resolves with language prefix."""
        url = reverse("email_system:wizard_step1")
        assert "/admin/email-system/wizard/step1/" in url

    def test_provider_browse_url(self):
        """email_system:provider_browse resolves with language prefix."""
        url = reverse("email_system:provider_browse")
        assert "/admin/email-system/providers/browse/" in url

    def test_translation_manager_url(self):
        """email_system:translation_manager resolves with language prefix."""
        url = reverse("email_system:translation_manager")
        assert "/admin/email-system/translations/" in url


# ============================================================================
# 8. TrackingService unit tests
# ============================================================================


class TestTrackingService:
    """TrackingService ID generation and parsing."""

    def test_generate_tracking_id_format(self):
        """Generated tracking ID has correct format: uuid-token."""
        from email_system.services.tracking_service import TrackingService

        ts = TrackingService()
        outbox_id = str(uuid.uuid4())
        tracking_id = ts._generate_tracking_id(outbox_id)
        # UUID (36 chars) + '-' + 16 hex chars = 53 chars
        assert len(tracking_id) == 53
        assert tracking_id.startswith(outbox_id)

    def test_parse_tracking_id(self):
        """parse_tracking_id extracts outbox UUID from tracking ID."""
        from email_system.services.tracking_service import TrackingService

        ts = TrackingService()
        outbox_id = str(uuid.uuid4())
        tracking_id = ts._generate_tracking_id(outbox_id)
        parsed = ts.parse_tracking_id(tracking_id)
        assert parsed == outbox_id

    def test_parse_tracking_id_invalid(self):
        """parse_tracking_id returns None for invalid tracking IDs."""
        from email_system.services.tracking_service import TrackingService

        ts = TrackingService()
        assert ts.parse_tracking_id("too-short") is None
        assert ts.parse_tracking_id("") is None


# ============================================================================
# 9. EmailTemplateTranslation model
# ============================================================================


class TestEmailTemplateTranslation:
    """EmailTemplateTranslation model."""

    def test_create_translation(self, email_template):
        """Translation can be created for a template."""
        from email_system.models import EmailTemplateTranslation

        t = EmailTemplateTranslation.objects.create(
            template=email_template,
            language_code="es",
            subject="Asunto de Prueba",
            html_content="<mjml><mj-body><mj-section><mj-column><mj-text>Hola</mj-text></mj-column></mj-section></mj-body></mjml>",
            text_content="Hola",
        )
        t.refresh_from_db()
        assert t.language_code == "es"
        assert t.template_id == email_template.pk

    def test_translation_unique_per_language(self, email_template):
        """Only one translation per language per template."""
        from django.db import IntegrityError, transaction

        from email_system.models import EmailTemplateTranslation

        EmailTemplateTranslation.objects.create(
            template=email_template,
            language_code="fr",
            subject="Sujet",
            html_content="<mjml><mj-body><mj-section><mj-column><mj-text>Bonjour</mj-text></mj-column></mj-section></mj-body></mjml>",
            text_content="Bonjour",
        )
        with pytest.raises(IntegrityError), transaction.atomic():
            EmailTemplateTranslation.objects.create(
                template=email_template,
                language_code="fr",
                subject="Sujet 2",
                html_content="<mjml><mj-body><mj-section><mj-column><mj-text>Bonjour 2</mj-text></mj-column></mj-section></mj-body></mjml>",
                text_content="Bonjour 2",
            )

    def test_is_outdated(self, email_template):
        """is_outdated returns True when template version exceeds translation version."""
        from email_system.models import EmailTemplateTranslation

        t = EmailTemplateTranslation.objects.create(
            template=email_template,
            language_code="de",
            subject="Betreff",
            html_content="<mjml><mj-body><mj-section><mj-column><mj-text>Hallo</mj-text></mj-column></mj-section></mj-body></mjml>",
            text_content="Hallo",
            base_template_version=1,
        )
        assert t.is_outdated() is False

        # Bump template version
        email_template.version = 2
        email_template.save(update_fields=["version"])
        assert t.is_outdated() is True

    def test_translation_str(self, email_template):
        """__str__ shows template type and language display."""
        from email_system.models import EmailTemplateTranslation

        t = EmailTemplateTranslation.objects.create(
            template=email_template,
            language_code="ja",
            subject="Test",
            html_content="<mjml><mj-body><mj-section><mj-column><mj-text>Test</mj-text></mj-column></mj-section></mj-body></mjml>",
            text_content="Test",
        )
        s = str(t)
        assert "Japanese" in s

    def test_clone_includes_translations(self, django_site, staff_user):
        """clone() without clone_language copies all translations."""
        from email_system.models import EmailTemplateTranslation

        original = EmailTemplateFactory(site=django_site, template_type="payment_confirmation")
        EmailTemplateTranslation.objects.create(
            template=original,
            language_code="es",
            subject="S",
            html_content="<mjml><mj-body><mj-section><mj-column><mj-text>H</mj-text></mj-column></mj-section></mj-body></mjml>",
            text_content="T",
        )
        EmailTemplateTranslation.objects.create(
            template=original,
            language_code="fr",
            subject="S",
            html_content="<mjml><mj-body><mj-section><mj-column><mj-text>H</mj-text></mj-column></mj-section></mj-body></mjml>",
            text_content="T",
        )
        clone = original.clone(user=staff_user, set_active=False)
        assert clone.translations.count() == 2


# ============================================================================
# 10. CSRF enforcement
# ============================================================================


class TestCSRFEnforcement:
    """POST endpoints enforce CSRF."""

    def test_toggle_active_rejects_no_csrf(self, email_account):
        """POST without CSRF token is rejected."""
        from django.test import Client

        client = Client(enforce_csrf_checks=True)
        user = UserFactory(staff=True)
        client.force_login(user)

        url = f"/en/admin/email-system/accounts/{email_account.pk}/toggle-active/"
        resp = client.post(
            url,
            "{}",
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert resp.status_code == 403
