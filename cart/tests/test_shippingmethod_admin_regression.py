"""Regression: the Shipping Method admin change form used to 500.

`ShippingMethodAdmin.change_view` built its `active_promotions` context by
OR-combining a plain queryset with an aggregated (`Count`) one and calling
`.distinct()`, which emits invalid `SELECT DISTINCT ... GROUP BY` SQL on
Postgres. The change_form template evaluates that queryset, so the page 500'd.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from cart.models import ShippingMethod
from shipping.models import ShippingPromotion

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
class ShippingMethodChangeFormRegressionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _ensure_site_settings()
        cls.admin = User.objects.create_superuser(
            username="sm_admin", email="sm@test.local", password="pw"
        )
        cls.method = ShippingMethod.objects.create(name="Standard", method_type="flat_rate")
        ptype = ShippingPromotion._meta.get_field("promotion_type").choices[0][0]
        # One promotion explicitly targeting this method...
        targeted = ShippingPromotion.objects.create(
            name="Free over $50", promotion_type=ptype, is_active=True
        )
        targeted.shipping_methods.add(cls.method)
        # ...and one that applies to all methods (no restrictions) — the branch
        # that added the aggregate to the union.
        ShippingPromotion.objects.create(
            name="Site-wide free shipping", promotion_type=ptype, is_active=True
        )

    def test_change_form_renders(self):
        self.client.force_login(self.admin)
        url = reverse("admin:cart_shippingmethod_change", args=[self.method.pk])
        resp = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(resp.status_code, 200)

    def test_add_form_renders(self):
        self.client.force_login(self.admin)
        url = reverse("admin:cart_shippingmethod_add")
        resp = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(resp.status_code, 200)
