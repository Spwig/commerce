"""Regression: the custom Product change form must render (and therefore
submit) the pre-order / shipping / tags / page-template fields.

Before the fix these fields were declared in the admin fieldsets but not
rendered by the custom change_form template. ProductForm bound every model
field, so each merchant save omitted them from the POST and the bound form
reset them — is_preorder/requires_shipping flipped to False,
tags/preferred_shipping_package/pre-order dates were cleared. requires_shipping
is checkout-critical (cart filters on it), so this was silent data loss.

The fix renders the merchant-facing fields and moves everything that must not
be form-managed into ProductForm.Meta.exclude. These tests drive a real admin
save (harvesting the rendered form) to assert the rendered values survive, and
guard the form ↔ template relationship against future drift.
"""

import re
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from djmoney.money import Money

import catalog
from catalog.admin import ProductForm
from catalog.models import Category, Product, ProductTag
from shipping.models import ShippingPackage

CHANGE_FORM_TEMPLATE = (
    Path(catalog.__file__).parent / "templates/admin/catalog/product/change_form.html"
)

User = get_user_model()

TARGET_FIELDS = [
    "tags",
    "is_preorder",
    "preorder_release_date",
    "preorder_message",
    "preferred_shipping_package",
    "page_template",
    "requires_shipping",
    "out_of_stock_action_override",
]

# Fields ProductForm.Meta.exclude keeps out of the bound form so a no-op save
# can never reset them. A representative sample used by the guard test.
EXCLUDED_SAMPLE = [
    "sales_count",
    "views_count",
    "is_deleted",
    "css_classes",
    "product_sections",
    "external_id",
    "agent_visible",
    "barcode",
]


def _ensure_site_settings():
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
class ProductChangeFormSurfacesFieldsTest(TestCase):
    def setUp(self):
        _ensure_site_settings()
        self.admin = User.objects.create_superuser("admin", "a@t.com", "pw123456")
        self.client = Client()
        self.client.force_login(self.admin)
        self.category = Category.objects.create(name="Cat", slug="cat")
        self.tag = ProductTag.objects.create(name="Summer", slug="summer")
        self.pkg = ShippingPackage.objects.create(
            name="Box A", length=10, width=10, height=10, max_weight=5
        )
        self.product = Product.objects.create(
            name="Preorder Widget",
            slug="preorder-widget",
            sku="PW-1",
            price=Money(20, "USD"),
            category=self.category,
            product_type="simple",
            requires_shipping=True,
            is_preorder=True,
            preorder_release_date=date(2027, 3, 1),
            preorder_message="Ships March 2027",
            page_template="classic",
            preferred_shipping_package=self.pkg,
            out_of_stock_action_override="hide",
        )
        self.product.tags.add(self.tag)

    def _harvest(self, html):
        """Approximate the browser's POST from every rendered input on the page."""
        soup = BeautifulSoup(html, "html.parser")
        data = {}

        def add(name, value):
            if name in data:
                if isinstance(data[name], list):
                    data[name].append(value)
                else:
                    data[name] = [data[name], value]
            else:
                data[name] = value

        for inp in soup.find_all("input"):
            name = inp.get("name")
            if not name:
                continue
            itype = (inp.get("type") or "text").lower()
            if itype in ("checkbox", "radio"):
                if inp.has_attr("checked"):
                    add(name, inp.get("value", "on"))
            elif itype in ("submit", "button", "file"):
                continue
            else:
                add(name, inp.get("value", ""))
        for sel in soup.find_all("select"):
            name = sel.get("name")
            if not name:
                continue
            opts = sel.find_all("option")
            selected = [o for o in opts if o.has_attr("selected")]
            if not selected and opts and not sel.has_attr("multiple"):
                selected = [opts[0]]
            for o in selected:
                add(name, o.get("value", ""))
        for ta in soup.find_all("textarea"):
            name = ta.get("name")
            if name:
                add(name, ta.text or "")
        return data

    def test_all_target_fields_are_rendered(self):
        url = reverse("admin:catalog_product_change", args=[self.product.pk])
        html = self.client.get(url, SERVER_NAME="localhost").content.decode()
        for field in TARGET_FIELDS:
            self.assertIn(
                f'name="{field}"',
                html,
                f"{field} is not rendered in the product change form",
            )

    def test_save_preserves_fields(self):
        url = reverse("admin:catalog_product_change", args=[self.product.pk])
        html = self.client.get(url, SERVER_NAME="localhost").content.decode()
        data = self._harvest(html)
        data["name"] = "Preorder Widget EDITED"

        resp = self.client.post(url, data, SERVER_NAME="localhost")
        self.assertEqual(resp.status_code, 302, "product save should succeed")

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Preorder Widget EDITED")
        # None of these may be reset by an unrelated edit.
        self.assertTrue(self.product.is_preorder)
        self.assertEqual(self.product.preorder_release_date, date(2027, 3, 1))
        self.assertEqual(self.product.preorder_message, "Ships March 2027")
        self.assertEqual(self.product.page_template, "classic")
        self.assertTrue(self.product.requires_shipping)
        self.assertEqual(self.product.preferred_shipping_package_id, self.pkg.pk)
        self.assertEqual(self.product.out_of_stock_action_override, "hide")
        self.assertEqual(list(self.product.tags.values_list("slug", flat=True)), ["summer"])


class ProductChangeFormDriftGuard(TestCase):
    """Fail loudly when a Product form field is neither rendered in
    change_form.html nor explicitly accounted for.

    The custom change form hand-picks each field with
    ``{{ adminform.form.<name> }}``. Any bound field the template does not
    render is omitted from every POST and therefore silently reset to empty on
    save (this is the bug that wiped is_preorder, requires_shipping, tags,
    etc.). ProductForm now uses ``exclude`` rather than ``fields="__all__"`` so
    internal/system/design fields are not bound at all and cannot be reset.

    This guard keeps that honest: add a model field and — unless you also add it
    to ProductForm.exclude — it is bound by default; if you then forget to
    render it AND forget to list it here, this test fails. When it does, render
    the field in change_form.html (preferred — it becomes editable and cannot
    be reset) or add it to ProductForm.exclude.
    """

    # name -> reason. The only fields that are bound but intentionally not
    # rendered via adminform.form.<name>. Everything else that must not be
    # form-managed is handled by ProductForm.Meta.exclude, not parked here.
    ACCOUNTED_FOR = {
        # Written by the translatable-field widgets, not a field of its own:
        "translations": "TranslatableFieldWidget writes it via the translatable fields",
        # Managed by CustomFieldsAdminMixin's own UI on this form:
        "custom_fields": "managed by CustomFieldsAdminMixin",
    }

    def test_no_unaccounted_form_fields(self):
        template = CHANGE_FORM_TEMPLATE.read_text()
        referenced = set(re.findall(r"adminform\.form\.([a-zA-Z_]+)", template))
        form_fields = set(ProductForm().fields)
        unaccounted = form_fields - referenced - set(self.ACCOUNTED_FOR)
        self.assertEqual(
            unaccounted,
            set(),
            "These Product form fields are bound but neither rendered in "
            "change_form.html nor listed in ACCOUNTED_FOR, so each is silently "
            "reset to empty on every save. Render them in the template, or add "
            f"them to ProductForm.Meta.exclude: {sorted(unaccounted)}",
        )

    def test_excluded_fields_are_not_bound(self):
        # ProductForm.Meta.exclude must keep these out of the bound form so a
        # no-op admin save cannot reset them.
        form_fields = set(ProductForm().fields)
        still_bound = [f for f in EXCLUDED_SAMPLE if f in form_fields]
        self.assertEqual(
            still_bound,
            [],
            f"These fields must be excluded from ProductForm but are still bound: {still_bound}",
        )

    def test_accounted_for_entries_are_still_real_fields(self):
        # Keep the allowlist honest: drop entries once a field is removed or
        # actually rendered, so it can never mask a future same-named field.
        template = CHANGE_FORM_TEMPLATE.read_text()
        referenced = set(re.findall(r"adminform\.form\.([a-zA-Z_]+)", template))
        form_fields = set(ProductForm().fields)
        stale = [f for f in self.ACCOUNTED_FOR if f not in form_fields or f in referenced]
        self.assertEqual(
            stale,
            [],
            f"ACCOUNTED_FOR lists fields that are no longer bound-and-unrendered: {stale}",
        )
