"""Regression tests for the Page admin "add" action.

Clicking "Add page" in the change list hits ``PageAdmin.add_view``, which
auto-creates a draft page and redirects to the visual builder instead of
showing the default add form. The draft's title was passed as a
``gettext_lazy`` proxy, which is written verbatim into
``PageVersion.content_snapshot`` (a JSONField) by ``create_snapshot()``. A
lazy ``__proxy__`` is not JSON serializable, so the insert 500'd. These tests
lock in that the add action succeeds and persists a JSON-serializable title.
"""

import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from page_builder.models import Page, PageVersion


class PageAdminAddViewTests(TestCase):
    def setUp(self):
        # Seed the SiteSettings singleton so admin/context-processor lookups
        # during the request don't fail validation on the blank admin_email.
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "admin_email": "admin@example.com",
                "default_currency": "USD",
                "enable_multi_warehouse": False,
            },
        )
        self.user = get_user_model().objects.create_superuser("admin", "admin@example.com", "x")
        self.client.force_login(self.user)

    def test_add_view_creates_draft_and_redirects_to_builder(self):
        """Add action auto-creates a draft page and redirects, never 500s."""
        before = Page.objects.count()
        resp = self.client.get(reverse("admin:page_builder_page_add"))

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Page.objects.count(), before + 1)

        page = Page.objects.latest("created_at")
        self.assertEqual(page.status, "draft")
        self.assertIn(f"/builder/{page.pk}/", resp["Location"])

    def test_draft_title_is_json_serializable(self):
        """The initial version snapshot must not carry a lazy proxy title."""
        self.client.get(reverse("admin:page_builder_page_add"))
        page = Page.objects.latest("created_at")

        # A concrete str, not a gettext_lazy __proxy__.
        self.assertIsInstance(page.title, str)

        version = PageVersion.objects.filter(page=page).latest("version_number")
        # Round-trips cleanly; a lazy proxy would raise TypeError here.
        json.dumps(version.content_snapshot)
        self.assertEqual(version.content_snapshot["page"]["title"], page.title)

    def test_snapshot_failure_leaves_no_orphaned_page(self):
        """A failure while snapshotting must roll the page insert back too."""
        from unittest.mock import patch

        before = Page.objects.count()
        with (
            patch.object(PageVersion, "create_snapshot", side_effect=RuntimeError("boom")),
            self.assertRaises(RuntimeError),
        ):
            self.client.get(reverse("admin:page_builder_page_add"))

        # add_view wraps creation in transaction.atomic(), so the orphaned
        # draft page must not survive the failed snapshot.
        self.assertEqual(Page.objects.count(), before)
