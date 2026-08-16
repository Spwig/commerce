"""
Regression tests for admin UI wiring that was previously broken/missing.

Covers three separate fixes:

1. StockDisplaySettings.__str__ returns a real str (was a lazy gettext proxy),
   so its admin change form no longer 500s.
2. The Product admin change form renders the region-availability controls:
   the ``region_restriction_mode`` select and the ProductRegionVisibility
   inline management form (exactly once).
3. The Stock Items changelist exposes the Django admin action framework
   (bulk-action select, checkboxes) and its stock actions dispatch to their
   confirmation screens.
"""

import json
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from djmoney.money import Money

from catalog.models import (
    Category,
    Product,
    ProductRegionVisibility,
    SalesRegion,
    StockDisplaySettings,
    StockItem,
    Warehouse,
)

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
class StockDisplaySettingsAdminRegressionTest(TestCase):
    """StockDisplaySettings admin change form must not 500.

    Root cause was ``__str__`` returning a lazy ``gettext`` proxy instead of a
    concrete ``str``, which blew up admin rendering of the change form.
    """

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_str_returns_concrete_str(self):
        settings_obj = StockDisplaySettings.get_settings()
        rendered = str(settings_obj)
        # A lazy gettext proxy is NOT an instance of ``str``; a real string is.
        self.assertIsInstance(rendered, str)
        self.assertEqual(rendered, "Stock Display Settings")
        # __proxy__ objects have this attribute; a real str does not.
        self.assertFalse(hasattr(settings_obj.__str__(), "_delegate_text"))

    def test_change_form_returns_200(self):
        settings_obj = StockDisplaySettings.get_settings()
        url = reverse("admin:catalog_stockdisplaysettings_change", args=[settings_obj.pk])
        response = self.client.get(url, SERVER_NAME="localhost")
        # Previously 500 because __str__ returned a lazy proxy.
        self.assertEqual(response.status_code, 200)


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ProductRegionAvailabilityChangeFormTest(TestCase):
    """Product change form renders region-availability controls exactly once."""

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

        self.category = Category.objects.create(name="Cat", slug="cat")
        self.region_a = SalesRegion.objects.create(
            name="Region A", code="RA", countries=["NZ"], default_currency="NZD"
        )
        self.region_b = SalesRegion.objects.create(
            name="Region B", code="RB", countries=["SG"], default_currency="SGD"
        )
        self.product = Product.objects.create(
            name="Region Restricted Product",
            slug="region-restricted-product",
            sku="RRP-001",
            price=Money(100, "USD"),
            category=self.category,
            region_restriction_mode="only_in",
        )
        # Two region-visibility rows so the inline has real initial forms.
        ProductRegionVisibility.objects.create(
            product=self.product, region=self.region_a, is_visible=True
        )
        ProductRegionVisibility.objects.create(
            product=self.product, region=self.region_b, is_visible=False
        )

    def test_change_form_renders_region_restriction_mode_field(self):
        url = reverse("admin:catalog_product_change", args=[self.product.pk])
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        # The region_restriction_mode select must be present.
        self.assertIn("id_region_restriction_mode", content)

    def test_region_visibility_inline_rendered_exactly_once(self):
        url = reverse("admin:catalog_product_change", args=[self.product.pk])
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        # The inline management form is the tell that the inline rendered.
        # Regression 1: it rendered zero times (wrong verbose_name string).
        # Regression 2: it must not double-render.
        self.assertEqual(
            content.count('name="region_visibility-TOTAL_FORMS"'),
            1,
            "ProductRegionVisibility inline management form should render exactly once",
        )
        # And the two initial rows should be reflected in the management form.
        self.assertIn('name="region_visibility-INITIAL_FORMS"', content)


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ProductChangeFormInlineWiringTest(TestCase):
    """EVERY product type's change form must render every inline admin.py declares.

    Regression: on 1.7.2 the custom product change_form template rendered the
    declared ``region_restriction_mode`` field and ``region_visibility`` inline
    ZERO times, so every save failed with "region_restriction_mode: This field is
    required" and "region_visibility-TOTAL_FORMS ... ManagementForm data is
    missing" (a model default does not rescue a *required, unrendered* form field,
    and the inline ManagementForm is structural). Fixed in 36a869f8a (1.7.3 line).

    The controls live in the shared "General" tab, so the bug hit every product
    type — a merchant happened to hit it on a booking product. Each specialist
    type also splices its own inlines into ``get_inlines`` (booking adds five,
    configurable two, bundle/digital/customization one), any of which a custom
    template can silently drop. This asserts the general invariant for ALL of
    them: every declared inline renders its ManagementForm, and the region
    controls render, so a save can never fail on a missing management form.
    """

    # product_type -> extra kwargs needed to construct that type
    TYPE_KWARGS = {
        "simple": {},
        "variable": {},
        "digital": {"is_digital": True},
        "gift_card": {},
        "bundle": {},
        "configurable": {},  # 3D configurator
        "customizable": {"allow_customization": True},
        "booking": {},
    }

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)
        self.category = Category.objects.create(name="Cat", slug="cat")
        SalesRegion.objects.create(
            name="Region A", code="RA", countries=["NZ"], default_currency="NZD"
        )

    def _make(self, product_type, extra):
        return Product.objects.create(
            name=f"{product_type} product",
            slug=f"{product_type}-product",
            sku=f"{product_type[:3].upper()}-1",
            price=Money(100, "USD"),
            category=self.category,
            product_type=product_type,
            **extra,
        )

    def _declared_inline_prefixes(self, product):
        """The formset prefix of every inline admin.py declares for this product."""
        from types import SimpleNamespace

        from django.contrib import admin as djadmin
        from django.test import RequestFactory

        req = RequestFactory().get("/")
        req.user = self.admin_user
        # a custom formfield_for_manytomany reads resolver_match on the change view
        req.resolver_match = SimpleNamespace(kwargs={"object_id": str(product.pk)})
        product_admin = djadmin.site._registry[Product]
        prefixes = []
        for inline_cls in product_admin.get_inlines(req, product):
            inline = inline_cls(Product, djadmin.site)
            prefixes.append(inline.get_formset(req, product).get_default_prefix())
        return prefixes

    def test_all_product_types_render_region_controls_and_every_inline(self):
        for product_type, extra in self.TYPE_KWARGS.items():
            with self.subTest(product_type=product_type):
                product = self._make(product_type, extra)
                url = reverse("admin:catalog_product_change", args=[product.pk])
                content = self.client.get(url, SERVER_NAME="localhost").content.decode("utf-8")

                # the region-availability field + inline management form must render
                self.assertIn(
                    "id_region_restriction_mode",
                    content,
                    f"{product_type}: region_restriction_mode select missing",
                )
                self.assertEqual(
                    content.count('name="region_visibility-TOTAL_FORMS"'),
                    1,
                    f"{product_type}: region_visibility management form should render once",
                )

                # no declared inline may be silently dropped by the custom template
                missing = [
                    pfx
                    for pfx in self._declared_inline_prefixes(product)
                    if f'name="{pfx}-TOTAL_FORMS"' not in content
                ]
                self.assertEqual(
                    missing,
                    [],
                    f"{product_type}: declared inline(s) not rendered → save would fail "
                    f"on their ManagementForm: {missing}",
                )


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class StockItemChangelistBulkActionsTest(TestCase):
    """Stock Items changelist exposes and dispatches the admin action framework."""

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

        self.category = Category.objects.create(name="Cat", slug="cat")
        self.region = SalesRegion.objects.create(
            name="Region A", code="RA", countries=["NZ"], default_currency="NZD"
        )
        self.warehouse = self._make_warehouse("Main", "WH-1")
        # Second active warehouse so transfer has a valid destination choice.
        self.warehouse2 = self._make_warehouse("Overflow", "WH-2")

        self.product_a = Product.objects.create(
            name="Prod A",
            slug="prod-a",
            sku="PA-1",
            price=Money(10, "USD"),
            category=self.category,
        )
        self.product_b = Product.objects.create(
            name="Prod B",
            slug="prod-b",
            sku="PB-1",
            price=Money(20, "USD"),
            category=self.category,
        )
        self.item_a = StockItem.objects.create(
            product=self.product_a, warehouse=self.warehouse, on_hand=50
        )
        self.item_b = StockItem.objects.create(
            product=self.product_b, warehouse=self.warehouse, on_hand=30
        )

    def _make_warehouse(self, name, code):
        return Warehouse.objects.create(
            name=name,
            code=code,
            region=self.region,
            address_line1="1 Test St",
            city="Auckland",
            postal_code="1010",
            country="NZ",
            is_active=True,
        )

    def test_changelist_exposes_action_form(self):
        url = reverse("admin:catalog_stockitem_changelist")
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn('id="changelist-form"', content)
        # The action <select> from Django's action_form.
        self.assertIn('name="action"', content)
        # Per-row checkboxes for selecting items.
        self.assertIn('name="_selected_action"', content)
        # The three wired-up stock action labels.
        self.assertIn("Transfer stock to warehouse", content)
        self.assertIn("Record damaged/lost stock", content)
        self.assertIn("Recount stock (physical count)", content)

    def test_transfer_action_dispatches_to_confirmation(self):
        url = reverse("admin:catalog_stockitem_changelist")
        response = self.client.post(
            url,
            {
                "action": "transfer_stock_action",
                "_selected_action": [self.item_a.pk, self.item_b.pk],
                "index": "0",
            },
            SERVER_NAME="localhost",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("stock-adjustment-container", content)
        # TransferForm renders a destination ModelChoiceField.
        self.assertIn("id_destination", content)

    def test_recount_action_dispatches_to_confirmation(self):
        url = reverse("admin:catalog_stockitem_changelist")
        response = self.client.post(
            url,
            {
                "action": "recount_stock_action",
                "_selected_action": [self.item_a.pk, self.item_b.pk],
                "index": "0",
            },
            SERVER_NAME="localhost",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("stock-adjustment-container", content)
        # RecountForm renders a counted_quantity IntegerField.
        self.assertIn("id_counted_quantity", content)


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ProductCustomsBulkActionsTest(TestCase):
    """The customs/international-shipping bulk actions are reachable from the UI.

    Regression: ``mark_international_ready`` and ``export_customs_data`` were
    declared as Django admin actions but the custom Product change list does not
    render the actions dropdown, so they were unreachable. They are now surfaced
    through the change-list toolbar and handled by ``bulk_action_view``.
    """

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

        self.category = Category.objects.create(name="Cat", slug="cat")
        # Ready for international shipping: has HS code, origin and customs price.
        self.ready = Product.objects.create(
            name="Ready Product",
            slug="ready-product",
            sku="RDY-1",
            price=Money(10, "USD"),
            category=self.category,
            hs_code="6109.10",
            country_of_origin="NZ",
            unit_price_for_customs=Decimal("9.50"),
        )
        # Not ready: missing all customs fields.
        self.not_ready = Product.objects.create(
            name="Incomplete Product",
            slug="incomplete-product",
            sku="INC-1",
            price=Money(20, "USD"),
            category=self.category,
        )

    def _bulk_action(self, action, product_ids):
        url = reverse("admin:catalog_product_bulk_action")
        return self.client.post(
            url,
            data=json.dumps({"action": action, "product_ids": product_ids}),
            content_type="application/json",
            SERVER_NAME="localhost",
        )

    def test_changelist_toolbar_offers_customs_actions(self):
        url = reverse("admin:catalog_product_changelist")
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn('value="export_customs"', content)
        self.assertIn('value="international_ready"', content)

    def test_international_readiness_reports_ready_and_missing(self):
        response = self._bulk_action("international_ready", [self.ready.pk, self.not_ready.pk])
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        # One ready, one not ready, and the missing fields are named.
        self.assertIn("1 ready", payload["message"])
        self.assertIn("1 not ready", payload["message"])
        self.assertIn("hs_code", payload["message"])

    def test_export_customs_returns_csv_with_customs_columns(self):
        response = self._bulk_action("export_customs", [self.ready.pk])
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertIn('filename="product_customs_data.csv"', response["Content-Disposition"])
        body = response.content.decode("utf-8")
        self.assertIn("HS Code", body)
        self.assertIn("6109.10", body)

    def test_customs_export_neutralizes_formula_injection(self):
        # A product name that opens with a formula trigger must be exported as
        # inert text (apostrophe-prefixed), not an executable spreadsheet formula.
        evil = Product.objects.create(
            name="=cmd|'/c calc'!A1",
            slug="evil-product",
            sku="+SUM(A1:A9)",
            price=Money(5, "USD"),
            category=self.category,
            hs_code="6109.10",
            country_of_origin="NZ",
            unit_price_for_customs=Decimal("5.00"),
        )
        response = self._bulk_action("export_customs", [evil.pk])
        self.assertEqual(response.status_code, 200)
        body = response.content.decode("utf-8")
        self.assertIn("'=cmd", body)
        self.assertIn("'+SUM", body)
        # The raw, unescaped formula must not appear as a cell start.
        self.assertNotIn(",=cmd", body)
