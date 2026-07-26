"""
The agentic settings admin: a merchant can toggle the feature in the UI.

Smoke-level, but it proves the singleton admin registers, the changelist
redirects to the one editable row, and the master switch / kill switch render.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


@pytest.fixture
def superuser():
    return get_user_model().objects.create_superuser(
        username="agentic_admin",
        email="agentic_admin@test.spwig.com",
        password="pw-12345!",
    )


class TestAgenticSettingsAdmin:
    def test_changelist_redirects_to_the_singleton_change_form(self, superuser):
        c = Client()
        c.force_login(superuser)
        resp = c.get("/en/admin/agentic/agenticsettings/")

        assert resp.status_code == 200
        body = resp.content.decode("utf-8", "ignore")
        # The master switch and the emergency stop are both editable here.
        assert "is_enabled" in body
        assert "kill_switch_engaged" in body
        # And the admin chrome carries the sidebar link into this page.
        assert "AI Shopping" in body

    def test_a_merchant_can_turn_it_on(self, superuser):
        from agentic.models import AgenticSettings

        # The merchant loads the page first (which creates the singleton row),
        # then submits — mirror that so the POST targets an existing object.
        AgenticSettings.get_settings()

        c = Client()
        c.force_login(superuser)
        # Post the full change form with is_enabled ticked. Unchecked booleans
        # are simply omitted (that's how HTML checkboxes work).
        resp = c.post(
            "/en/admin/agentic/agenticsettings/1/change/",
            data={
                "is_enabled": "on",
                "ucp_enabled": "on",
                "mcp_storefront_enabled": "on",
                "allow_unverified_read": "on",
                "merchant_display_name": "",
                "support_url": "",
                "terms_url": "",
                "privacy_url": "",
                "return_policy_url": "",
                "_save": "Save",
            },
            follow=True,
        )
        assert resp.status_code == 200
        # No form errors re-rendered.
        assert b"errornote" not in resp.content
        assert AgenticSettings.get_settings().is_enabled is True

    def test_singleton_cannot_be_deleted(self, superuser):
        from agentic.admin import AgenticSettingsAdmin

        admin = AgenticSettingsAdmin(
            model=__import__("agentic.models", fromlist=["AgenticSettings"]).AgenticSettings,
            admin_site=None,
        )
        assert admin.has_delete_permission(request=None) is False
