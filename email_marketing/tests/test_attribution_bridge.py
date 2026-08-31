"""Attribution bridge (Slice 1): per-campaign revenue linkage.

Campaign Studio mints a stable per-campaign slug, ensures a matching
attribution.Campaign, stamps that slug on the outbox, and the tracking layer emits
it as utm_campaign — so a converting click credits revenue back to the specific
campaign. The read helper aggregates that revenue by slug.
"""

import uuid
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from attribution.models import Campaign as AttributionCampaign
from attribution.models import TouchPoint
from attribution.services import reporting as attribution_reporting
from attribution.services.resolution import resolve_order
from email_marketing.models import Campaign, CampaignSend
from email_marketing.services import reporting as em_reporting
from email_marketing.services.attribution_link import ensure_attribution_campaign
from email_system.models import EmailOutbox
from email_system.services.tracking_service import TrackingService

from .base import MarketingTestCase

User = get_user_model()


class SlugTests(MarketingTestCase):
    def test_slug_is_minted_readable_and_stable(self):
        c = Campaign.objects.create(site=self.site, name="Spring Sale!", subject="s")
        slug = c.ensure_attribution_slug()
        self.assertTrue(slug.startswith("email-spring-sale-"))
        self.assertTrue(slug.endswith(c.id.hex))  # full uuid tail → collision-proof
        self.assertEqual(Campaign.objects.get(pk=c.pk).attribution_slug, slug)
        # A later rename must not fork the slug (freezes revenue history).
        c.name = "Totally Renamed"
        c.save(update_fields=["name"])
        self.assertEqual(c.ensure_attribution_slug(), slug)

    def test_unslugifiable_name_falls_back(self):
        c = Campaign.objects.create(site=self.site, name="!!!", subject="s")
        self.assertTrue(c.ensure_attribution_slug().startswith("email-campaign-"))


class AttributionCampaignSyncTests(MarketingTestCase):
    def test_ensure_creates_email_campaign_and_is_idempotent(self):
        c = Campaign.objects.create(site=self.site, name="Promo", subject="s")
        slug = ensure_attribution_campaign(c)
        self.assertIsNotNone(slug)
        ac = AttributionCampaign.objects.get(slug=slug)
        self.assertEqual(ac.channel_hint, "email")
        self.assertTrue(ac.is_active)
        self.assertEqual(ensure_attribution_campaign(c), slug)  # idempotent
        self.assertEqual(AttributionCampaign.objects.filter(slug=slug).count(), 1)


class OutboxTaggingTests(MarketingTestCase):
    def test_send_stamps_slug_on_outbox_and_syncs_attribution_campaign(self):
        from email_marketing.services import campaigns as campaigns_svc

        c = Campaign.objects.create(
            site=self.site,
            name="Newsletter",
            subject="Hi",
            html_content=(
                "<mjml><mj-body><mj-section><mj-column>"
                "<mj-text>hi</mj-text></mj-column></mj-section></mj-body></mjml>"
            ),
        )
        sub = self.make_anon_emailable("r@example.com")
        res = campaigns_svc.send_campaign_to_subscriber(c, sub)
        self.assertTrue(res["queued"])
        c.refresh_from_db()
        outbox = EmailOutbox.objects.get(id=res["outbox_id"])
        self.assertTrue(c.attribution_slug)
        self.assertEqual(outbox.attribution_campaign, c.attribution_slug)
        self.assertTrue(AttributionCampaign.objects.filter(slug=c.attribution_slug).exists())


class TrackingEmissionTests(MarketingTestCase):
    def _outbox(self, **kw):
        kw.setdefault("site", self.site)
        kw.setdefault("account", self.account)
        kw.setdefault("from_email", "s@example.com")
        kw.setdefault("to_email", "r@example.com")
        kw.setdefault("subject", "s")
        kw.setdefault("html_body", "<p>h</p>")
        kw.setdefault("status", "queued")
        return EmailOutbox.objects.create(**kw)

    def test_stamped_slug_is_emitted_as_utm_campaign(self):
        ob = self._outbox(attribution_campaign="email-x-abc12345", template_type="newsletter")
        self.assertEqual(TrackingService()._attribution_campaign(ob.id), "email-x-abc12345")

    def test_falls_back_to_marketing_template_type(self):
        ob = self._outbox(attribution_campaign="", template_type="newsletter")
        self.assertEqual(TrackingService()._attribution_campaign(ob.id), "newsletter")

    def test_transactional_email_is_not_attributed(self):
        ob = self._outbox(attribution_campaign="", template_type="order_confirmation")
        self.assertIsNone(TrackingService()._attribution_campaign(ob.id))

    def test_transactional_email_ignores_a_stamped_slug(self):
        # Drift backstop: a slug stamped on a transactional email must NOT tag its
        # links (would misattribute the recipient's next order).
        ob = self._outbox(
            attribution_campaign="email-x-deadbeef", template_type="order_confirmation"
        )
        self.assertIsNone(TrackingService()._attribution_campaign(ob.id))


class CampaignRevenueReadTests(MarketingTestCase):
    def test_empty_slugs_returns_zeros(self):
        self.assertEqual(
            attribution_reporting.campaign_revenue([]),
            {"revenue": Decimal("0.00"), "orders": 0, "aov": Decimal("0.00")},
        )

    def test_click_to_purchase_credits_the_campaign(self):
        from tests.factories import OrderFactory

        user = User.objects.create_user(
            username=f"buyer-{uuid.uuid4().hex[:6]}", email="buyer@example.com", password="x"
        )
        c = Campaign.objects.create(site=self.site, name="Skincare Drop", subject="s")
        slug = ensure_attribution_campaign(c)
        ac = AttributionCampaign.objects.get(slug=slug)
        # status="processing" is NOT auto-resolved by the order orchestrator, so the
        # explicit resolve_order below is the single attribution pass (with the touch).
        order = OrderFactory(user=user, status="processing", total_amount=Decimal("120.00"))
        tp = TouchPoint.objects.create(
            visitor_key="vk1",
            customer=user,
            channel="email",
            medium="email",
            campaign=slug,
            campaign_ref=ac,
        )
        TouchPoint.objects.filter(pk=tp.pk).update(
            occurred_at=timezone.now() - timedelta(minutes=30)
        )
        resolve_order(order)

        result = attribution_reporting.campaign_revenue([slug])
        self.assertEqual(result["orders"], 1)
        self.assertEqual(result["revenue"], Decimal("120.00"))
        self.assertEqual(result["aov"], Decimal("120.00"))
        # And it appears in the store-wide by-campaign overview.
        by_slug = {r["slug"]: r for r in attribution_reporting.revenue_by_campaign()}
        self.assertIn(slug, by_slug)


class CampaignRevenueSurfaceTests(MarketingTestCase):
    """Slice 2: the campaign_revenue rollup (revenue/AOV/ROAS/rev-per-email) + report card."""

    def _user(self):
        return User.objects.create_user(
            username=f"b-{uuid.uuid4().hex[:8]}",
            email=f"{uuid.uuid4().hex[:8]}@ex.com",
            password="x",
        )

    def _attribute(self, campaign, user, amount):
        from tests.factories import OrderFactory

        slug = ensure_attribution_campaign(campaign)
        ac = AttributionCampaign.objects.get(slug=slug)
        order = OrderFactory(user=user, status="processing", total_amount=amount)
        tp = TouchPoint.objects.create(
            visitor_key=f"vk-{user.id}",
            customer=user,
            channel="email",
            medium="email",
            campaign=slug,
            campaign_ref=ac,
        )
        TouchPoint.objects.filter(pk=tp.pk).update(
            occurred_at=timezone.now() - timedelta(minutes=30)
        )
        resolve_order(order)

    def _marketing_staff(self):
        from django.contrib.auth.models import Group

        from staff_roles.models import StaffRole
        from staff_roles.services import invalidate_user_cache

        user = User.objects.create_user(
            username=f"mkt-{uuid.uuid4().hex[:8]}",
            email="mkt@test.spwig.com",
            password="pw",
            is_staff=True,
        )
        group = Group.objects.create(name=f"marketing-{uuid.uuid4().hex[:8]}")
        user.groups.add(group)
        StaffRole.objects.create(
            group=group,
            display_name=group.name,
            can_access_admin=True,
            permission_categories={"marketing": "full"},
        )
        invalidate_user_cache(user)
        return user

    def test_revenue_aov_and_revenue_per_email(self):
        c = Campaign.objects.create(site=self.site, name="Rev", subject="s")
        # One delivered send → revenue-per-email denominator of 1.
        CampaignSend.objects.create(
            campaign=c,
            subscriber=self.make_anon_emailable("d@ex.com"),
            status=CampaignSend.STATUS_SENT,
        )
        self._attribute(c, self._user(), Decimal("100.00"))
        rev = em_reporting.campaign_revenue(c)
        self.assertEqual(rev["revenue"], Decimal("100.00"))
        self.assertEqual(rev["orders"], 1)
        self.assertEqual(rev["aov"], Decimal("100.00"))
        self.assertEqual(rev["revenue_per_email"], Decimal("100.00"))
        self.assertIsNone(rev["roas"])  # no spend recorded

    def test_roas_when_spend_recorded(self):
        from djmoney.money import Money

        c = Campaign.objects.create(
            site=self.site, name="Rev2", subject="s", spend=Money(Decimal("25.00"), "USD")
        )
        self._attribute(c, self._user(), Decimal("100.00"))
        self.assertEqual(em_reporting.campaign_revenue(c)["roas"], Decimal("4.00"))

    def test_roas_is_none_when_spend_currency_differs_from_base(self):
        # Base currency is USD (test SiteSettings); spend in EUR must NOT produce a
        # currency-mixed ROAS — better no figure than a wrong one.
        from djmoney.money import Money

        c = Campaign.objects.create(
            site=self.site, name="Rev3", subject="s", spend=Money(Decimal("25.00"), "EUR")
        )
        self._attribute(c, self._user(), Decimal("100.00"))
        self.assertIsNone(em_reporting.campaign_revenue(c)["roas"])

    def test_scope_rollup_includes_children(self):
        parent = Campaign.objects.create(site=self.site, name="P", subject="s")
        child = Campaign.objects.create(site=self.site, name="Cx", subject="s", parent=parent)
        self._attribute(child, self._user(), Decimal("60.00"))
        self.assertEqual(em_reporting.campaign_revenue(parent)["revenue"], Decimal("60.00"))

    def test_empty_campaign_reports_zero_revenue(self):
        c = Campaign.objects.create(site=self.site, name="Empty", subject="s")
        rev = em_reporting.campaign_revenue(c)
        self.assertEqual(rev["revenue"], Decimal("0.00"))
        self.assertEqual(rev["orders"], 0)
        self.assertIsNone(rev["roas"])

    def test_report_page_renders_revenue_card(self):
        c = Campaign.objects.create(site=self.site, name="Shown", subject="s")
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(reverse("email_marketing_admin:campaign_report", args=[c.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Attributed revenue")
        self.assertIn("revenue", resp.context)
