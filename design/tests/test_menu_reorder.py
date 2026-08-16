"""Menu reorder endpoint — parent-hierarchy validation.

The drag-and-drop reorder endpoint persists ``parent_id`` for a batch of items.
It must refuse a parent that is the item itself, lives in another menu, or would
form a cycle — otherwise a malformed hierarchy reaches the DB (data integrity;
the nav renderer is separately hardened against pathological trees).
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from design.header_footer_models import Menu, MenuItem
from design.menu_api_views import MenuItemsReorderAPIView

User = get_user_model()


class ParentValidationUnitTests(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name="M", slug="m")
        self.other = Menu.objects.create(name="O", slug="o")
        self.a = MenuItem.objects.create(menu=self.menu, item_type="link", title="A", url="/a/")
        self.b = MenuItem.objects.create(menu=self.menu, item_type="link", title="B", url="/b/")
        self.c = MenuItem.objects.create(
            menu=self.menu, parent=self.b, item_type="link", title="C", url="/c/"
        )
        self.foreign = MenuItem.objects.create(
            menu=self.other, item_type="link", title="F", url="/f/"
        )

    def _valid(self, item, parent_id):
        return MenuItemsReorderAPIView._parent_is_valid(item, parent_id)

    def test_self_parent_rejected(self):
        self.assertFalse(self._valid(self.a, self.a.pk))

    def test_foreign_menu_parent_rejected(self):
        self.assertFalse(self._valid(self.a, self.foreign.pk))

    def test_missing_parent_rejected(self):
        self.assertFalse(self._valid(self.a, 999999))

    def test_normal_parent_allowed(self):
        self.assertTrue(self._valid(self.a, self.b.pk))

    def test_cycle_rejected(self):
        # B already has child C; making B a child of C would form B -> C -> B
        self.assertFalse(self._valid(self.b, self.c.pk))


class ReorderEndpointTests(TestCase):
    def setUp(self):
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "admin_email": "admin@example.com",
                "default_currency": "USD",
                "enable_multi_warehouse": False,
            },
        )
        self.staff = User.objects.create_user("staff", "s@e.com", "pw", is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(self.staff)
        self.menu = Menu.objects.create(name="M", slug="m")
        self.a = MenuItem.objects.create(menu=self.menu, item_type="link", title="A", url="/a/")

    def _post(self, items):
        return self.client.post(reverse("menu_api:items_reorder"), {"items": items}, format="json")

    def test_self_parent_is_coerced_to_root(self):
        resp = self._post([{"id": self.a.pk, "order": 0, "parent_id": self.a.pk}])
        self.assertEqual(resp.status_code, 200)
        self.a.refresh_from_db()
        # the self-parent was rejected — the item stays at the root, not looped
        self.assertIsNone(self.a.parent_id)

    def test_valid_parent_persists(self):
        parent = MenuItem.objects.create(menu=self.menu, item_type="link", title="P", url="/p/")
        resp = self._post([{"id": self.a.pk, "order": 1, "parent_id": parent.pk}])
        self.assertEqual(resp.status_code, 200)
        self.a.refresh_from_db()
        self.assertEqual(self.a.parent_id, parent.pk)
