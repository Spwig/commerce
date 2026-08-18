"""
Regression tests for the restyled SubscriptionPlan admin change form.

`SubscriptionPlanAdmin` uses a custom tabbed `change_form_template`
(admin/subscriptions/subscriptionplan/change_form.html) that:

- renders admin-base.css tabs (General / Pricing / Tiers & Add-ons /
  Lifecycle / Advanced),
- renders a dashboard header + stats grid fed by `change_view`
  (active_subscriptions, pricing_tiers_count, addons_count, total_revenue),
- places the two inlines into the "Tiers & Add-ons" tab, matched by
  `inline_admin_formset.formset.prefix` (`pricing_tiers` and `addons`).

The important regression guard is that the **add-on** inline actually renders:
an earlier iteration matched inlines by a verbose-name substring, which silently
dropped the PlanAddon inline. It is now matched by formset prefix.

These are Django ``TestCase`` tests (mirroring test_models.py) so they run
identically under ``pytest`` and ``manage.py test`` without depending on the
pytest-only autouse fixtures in conftest.py.
"""

from decimal import Decimal

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from djmoney.money import Money

from subscriptions.models import PlanAddon, PlanPricingTier, SubscriptionPlan

User = get_user_model()


def _ensure_site_settings():
    """Ensure Site 1 and default SiteSettings exist (currency middleware needs it)."""
    from django.contrib.sites.models import Site

    from core.models import SiteSettings

    if not Site.objects.filter(pk=1).exists():
        Site.objects.create(pk=1, domain="testserver", name="Test Site")

    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@example.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )


def _scrape_form_data(html, form_id):
    """Build a POST payload from the currently-rendered <form id=form_id>.

    Mirrors what a browser would submit: current values of every input/select/
    textarea inside the form, honouring checkbox/radio checked state and select
    selection. Submit buttons and file inputs are omitted (the caller adds the
    admin submit name explicitly).
    """
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form", id=form_id)
    assert form is not None, f"form#{form_id} not found in rendered page"

    data = {}

    def _append(name, value):
        if name in data:
            existing = data[name]
            if isinstance(existing, list):
                existing.append(value)
            else:
                data[name] = [existing, value]
        else:
            data[name] = value

    for inp in form.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        input_type = (inp.get("type") or "text").lower()
        if input_type in ("submit", "button", "image", "reset", "file"):
            continue
        if input_type in ("checkbox", "radio"):
            if inp.has_attr("checked"):
                _append(name, inp.get("value", "on"))
            continue
        _append(name, inp.get("value", ""))

    for textarea in form.find_all("textarea"):
        name = textarea.get("name")
        if not name:
            continue
        _append(name, textarea.text or "")

    for select in form.find_all("select"):
        name = select.get("name")
        if not name:
            continue
        options = select.find_all("option")
        selected = [o for o in options if o.has_attr("selected")]
        if not selected and options:
            # A browser defaults to the first option when none is marked selected.
            selected = [options[0]]
        for o in selected:
            _append(name, o.get("value", ""))

    return data


class SubscriptionPlanAdminChangeFormTest(TestCase):
    """Regression coverage for the custom tabbed SubscriptionPlan change form."""

    @classmethod
    def setUpTestData(cls):
        _ensure_site_settings()
        cls.admin = User.objects.create_superuser(
            username="qa_admin",
            email="qa_admin@example.com",
            password="qa-pass-12345",
        )
        cls.plan = SubscriptionPlan.objects.create(
            name="Coffee Club",
            slug="coffee-club",
            description="Fresh beans every month.",
            pricing_model="tiered",
        )
        cls.tier = PlanPricingTier.objects.create(
            plan=cls.plan,
            tier_name="Monthly",
            billing_cycle="monthly",
            billing_interval=1,
            discount_percentage=Decimal("0.00"),
            is_default=True,
            is_active=True,
        )
        cls.addon = PlanAddon.objects.create(
            plan=cls.plan,
            name="Priority Support",
            description="Front of the queue.",
            price=Money(Decimal("10.00"), "USD"),
            billing_frequency="per_cycle",
            allow_quantity=False,
            is_required=False,
            is_active=True,
        )

    def setUp(self):
        _ensure_site_settings()
        self.client.force_login(self.admin)

    def _change_url(self):
        return reverse("admin:subscriptions_subscriptionplan_change", args=[self.plan.pk])

    def test_change_page_renders_tabs_stats_and_both_inlines(self):
        """GET the change page: tabbed nav, stats grid, and BOTH inline field sets."""
        response = self.client.get(self._change_url())
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        # Tab navigation container + all five tab buttons.
        self.assertIn('class="admin-tabs"', html)
        for tab in ("general", "pricing", "tiers", "lifecycle", "advanced"):
            self.assertIn(f'data-tab="{tab}"', html, f"missing tab button data-tab={tab}")

        # Custom form id (proves the custom template rendered, not Django's default).
        self.assertIn('id="subscriptionplan_form"', html)

        # Dashboard stats grid + a stat value fed by change_view extra_context.
        self.assertIn("dashboard-stats-grid", html)

        # Pricing-tier inline field is present...
        self.assertIn("id_pricing_tiers-0-tier_name", html)
        # ...and the add-on inline field is present. This is the regression guard:
        # an earlier verbose-name-substring match dropped this inline; it is now
        # matched by formset prefix ('addons').
        self.assertIn("id_addons-0-name", html)

    def test_change_view_injects_dashboard_stat_context(self):
        """change_view must inject the dashboard-stats context keys."""
        response = self.client.get(self._change_url())
        self.assertEqual(response.status_code, 200)
        # pricing_tiers_count / addons_count reflect the one tier + one add-on.
        self.assertEqual(response.context["pricing_tiers_count"], 1)
        self.assertEqual(response.context["addons_count"], 1)
        self.assertEqual(response.context["active_subscriptions"], 0)
        self.assertIn("total_revenue", response.context)

    def test_add_page_renders_custom_form(self):
        """GET the add page returns 200 and uses the custom form id."""
        url = reverse("admin:subscriptions_subscriptionplan_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="subscriptionplan_form"', response.content.decode())

    def test_change_form_post_updates_plan_name(self):
        """POST via the custom form submits all fields + inline management forms.

        Proves the restyled template is actually submittable end to end: we scrape
        the rendered form, change only the plan name, POST it, and confirm the DB
        value updates and the admin redirects (302).
        """
        get_response = self.client.get(self._change_url())
        self.assertEqual(get_response.status_code, 200)

        data = _scrape_form_data(get_response.content.decode(), "subscriptionplan_form")

        # Sanity: the scraped payload carries both inline management forms, so the
        # POST exercises the full custom template (not just the top-level fields).
        self.assertIn("pricing_tiers-TOTAL_FORMS", data)
        self.assertIn("addons-TOTAL_FORMS", data)
        # And the existing rows are present in the payload.
        self.assertEqual(data.get("pricing_tiers-0-tier_name"), "Monthly")
        self.assertEqual(data.get("addons-0-name"), "Priority Support")

        data["name"] = "Coffee Club Deluxe"
        data["_save"] = "Save"

        post_response = self.client.post(self._change_url(), data)
        self.assertEqual(
            post_response.status_code,
            302,
            msg=f"expected redirect after save, got {post_response.status_code}; "
            f"form errors: "
            f"{getattr(post_response, 'context', None) and post_response.context.get('adminform') and post_response.context['adminform'].form.errors}",
        )

        self.plan.refresh_from_db()
        self.assertEqual(self.plan.name, "Coffee Club Deluxe")
        # Inlines survived the round-trip unchanged.
        self.assertEqual(self.plan.pricing_tiers.count(), 1)
        self.assertEqual(self.plan.addons.count(), 1)
