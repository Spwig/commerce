"""Regression: the Receipt Template admin used to 500.

The change_form's live-preview panel did
`{{ original.warehouse.pos_display_name|default:original.warehouse.name|... }}`.
On the add form `original` is None, and on the change form `warehouse` can be
None — either way the `default:` argument `original.warehouse.name` re-raises
`VariableDoesNotExist` (filter arguments propagate), 500'ing the page.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from pos_app.models import ReceiptTemplate

User = get_user_model()


def _ensure_site_settings():
    """Currency middleware needs a valid SiteSettings(pk=1) on every request."""
    from django.contrib.sites.models import Site

    from core.models import SiteSettings

    Site.objects.update_or_create(pk=1, defaults={"domain": "localhost", "name": "Test Site"})
    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "admin_email": "admin@example.com",
            "default_currency": "USD",
            "enable_multi_warehouse": False,
        },
    )


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ReceiptTemplateAdminRegressionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _ensure_site_settings()
        cls.admin = User.objects.create_superuser(
            username="rt_admin", email="rt@test.local", password="pw"
        )
        # A template with no warehouse — the case the preview panel choked on.
        cls.template = ReceiptTemplate.objects.create(name="Default receipt")

    def test_add_form_renders(self):
        self.client.force_login(self.admin)
        resp = self.client.get(
            reverse("admin:pos_app_receipttemplate_add"), SERVER_NAME="localhost"
        )
        self.assertEqual(resp.status_code, 200)

    def test_change_form_renders_without_warehouse(self):
        self.client.force_login(self.admin)
        url = reverse("admin:pos_app_receipttemplate_change", args=[self.template.pk])
        resp = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(resp.status_code, 200)
