"""
Regression test: the Ship-To Selector widget is available in the widget library.

The header/footer builder's widget-library API groups active widgets by type.
The ``create_default_widgets`` management command was extended to seed a
``ship_to`` widget, so a fresh install exposes it in the builder. This verifies
both the seeded command output and the API grouping surface the widget.
"""

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from design.header_footer_models import Widget

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
class ShipToWidgetLibraryTest(TestCase):
    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        self.url = reverse("hf_api:widget_library")

    def test_create_default_widgets_seeds_ship_to(self):
        call_command("create_default_widgets")
        self.assertTrue(
            Widget.objects.filter(widget_type="ship_to", is_active=True).exists(),
            "create_default_widgets should seed an active ship_to widget",
        )

    def test_library_api_groups_ship_to_widget(self):
        Widget.objects.create(
            name="Ship-To Selector",
            widget_type="ship_to",
            config={"button_style": "outline", "show_label": True},
            is_active=True,
        )
        response = self.client.get(self.url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)

        grouped = response.data["widgets"]
        self.assertIn("ship_to", grouped)
        ship_to_widgets = grouped["ship_to"]
        self.assertEqual(len(ship_to_widgets), 1)
        self.assertEqual(ship_to_widgets[0]["type"], "ship_to")
        self.assertEqual(ship_to_widgets[0]["type_display"], "Ship-To Selector")

    def test_library_api_requires_admin(self):
        anon = APIClient()
        response = anon.get(self.url, SERVER_NAME="localhost")
        self.assertIn(response.status_code, (401, 403))
