"""Per-campaign delivery/engagement reporting (bounce rollup + metrics).

Two surfaces: (1) the EmailEvent → CampaignSend rollup that records bounces and
complaints on the send (mirrors the open/click rollup); (2) campaign_report()'s
counts and rates.
"""

import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from email_marketing.models import Campaign, CampaignSend
from email_marketing.services import reporting
from email_system.models import EmailEvent, EmailOutbox

from .base import MarketingTestCase

User = get_user_model()

User = get_user_model()


class BounceRollupTests(MarketingTestCase):
    def _campaign(self):
        return Campaign.objects.create(site=self.site, name="C", subject="s")

    def _send(self, campaign, email="r@example.com", status=CampaignSend.STATUS_SENT):
        sub = self.make_anon_emailable(email)
        outbox = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            from_email="store@example.com",
            to_email=email,
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="sent",
        )
        return CampaignSend.objects.create(
            campaign=campaign, subscriber=sub, outbox=outbox, status=status
        )

    def test_bounced_event_stamps_the_campaign_send(self):
        cs = self._send(self._campaign())
        EmailEvent.objects.create(email=cs.outbox, event_type="bounced", bounce_type="hard")
        cs.refresh_from_db()
        self.assertTrue(cs.bounced)
        self.assertEqual(cs.bounce_type, "hard")
        self.assertIsNotNone(cs.bounced_at)
        self.assertFalse(cs.complained)

    def test_complained_event_stamps_the_campaign_send(self):
        cs = self._send(self._campaign())
        EmailEvent.objects.create(email=cs.outbox, event_type="complained")
        cs.refresh_from_db()
        self.assertTrue(cs.complained)
        self.assertIsNotNone(cs.complained_at)

    def test_first_bounce_wins_and_a_later_one_is_a_noop(self):
        cs = self._send(self._campaign())
        EmailEvent.objects.create(email=cs.outbox, event_type="bounced", bounce_type="soft")
        EmailEvent.objects.create(email=cs.outbox, event_type="bounced", bounce_type="hard")
        cs.refresh_from_db()
        self.assertEqual(cs.bounce_type, "soft")  # first event wins


class CampaignReportTests(MarketingTestCase):
    def _campaign(self, **kw):
        kw.setdefault("site", self.site)
        kw.setdefault("name", "C")
        kw.setdefault("subject", "s")
        return Campaign.objects.create(**kw)

    def _bulk(self, campaign, n, **fields):
        # Distinct subscribers so the (campaign, subscriber) unique holds.
        base = fields.pop("_prefix", "u")
        for i in range(n):
            sub = self.make_anon_emailable(f"{base}{i}-{campaign.id.hex[:6]}@example.com")
            CampaignSend.objects.create(campaign=campaign, subscriber=sub, **fields)

    def test_counts_and_rates(self):
        c = self._campaign()
        # 10 sent+delivered, of which 6 opened / 3 clicked
        self._bulk(c, 6, status=CampaignSend.STATUS_SENT, opened=True, clicked=True, _prefix="oc")
        self._bulk(c, 4, status=CampaignSend.STATUS_SENT, _prefix="plain")
        # 2 sent then async-bounced (soft), 1 hard sync-reject (failed+bounced)
        self._bulk(
            c, 2, status=CampaignSend.STATUS_SENT, bounced=True, bounce_type="soft", _prefix="sb"
        )
        self._bulk(
            c, 1, status=CampaignSend.STATUS_FAILED, bounced=True, bounce_type="hard", _prefix="hb"
        )
        # 1 complaint (delivered but complained), 2 skipped-suppressed
        self._bulk(c, 1, status=CampaignSend.STATUS_SENT, complained=True, _prefix="cx")
        self._bulk(
            c, 2, status=CampaignSend.STATUS_SKIPPED, skip_reason="suppressed", _prefix="sup"
        )

        r = reporting.campaign_report(c)
        self.assertEqual(r["recipients"], 16)
        self.assertEqual(r["sent"], 13)  # all SENT rows (incl the 2 async-bounced + 1 complained)
        self.assertEqual(r["failed"], 1)
        self.assertEqual(r["attempted"], 14)  # sent + failed
        self.assertEqual(r["bounced"], 3)
        self.assertEqual(r["hard_bounced"], 1)
        self.assertEqual(r["soft_bounced"], 2)
        self.assertEqual(r["complained"], 1)
        self.assertEqual(r["skipped_suppressed"], 2)
        # delivered = SENT and not bounced = 13 - 2 = 11
        self.assertEqual(r["delivered"], 11)
        # opens over delivered: 6/11, bounces over attempted: 3/14
        self.assertEqual(r["open_rate"], round(100 * 6 / 11, 1))
        self.assertEqual(r["click_rate"], round(100 * 6 / 11, 1))
        self.assertEqual(r["bounce_rate"], round(100 * 3 / 14, 1))
        self.assertEqual(r["complaint_rate"], round(100 * 1 / 11, 1))

    def test_open_on_a_bounced_send_is_excluded_from_the_rate(self):
        # An open recorded on a send that later bounced must not count toward opens,
        # or open_rate (opens / delivered) could exceed 100%.
        c = self._campaign()
        self._bulk(c, 1, status=CampaignSend.STATUS_SENT, opened=True, _prefix="d")
        self._bulk(
            c,
            1,
            status=CampaignSend.STATUS_SENT,
            opened=True,
            bounced=True,
            bounce_type="soft",
            _prefix="ob",
        )
        r = reporting.campaign_report(c)
        self.assertEqual(r["delivered"], 1)
        self.assertEqual(r["opened"], 1)  # the bounced-open is excluded
        self.assertEqual(r["open_rate"], 100.0)

    def test_empty_campaign_is_all_zeros(self):
        r = reporting.campaign_report(self._campaign())
        self.assertEqual(r["recipients"], 0)
        self.assertEqual(r["delivered"], 0)
        self.assertEqual(r["open_rate"], 0.0)
        self.assertEqual(r["bounce_rate"], 0.0)

    def test_ab_parent_aggregates_variant_children(self):
        parent = self._campaign(name="A/B parent")
        va = self._campaign(name="variant A", parent=parent)
        vb = self._campaign(name="variant B", parent=parent)
        self._bulk(va, 5, status=CampaignSend.STATUS_SENT, opened=True, _prefix="a")
        self._bulk(
            vb, 5, status=CampaignSend.STATUS_SENT, bounced=True, bounce_type="hard", _prefix="b"
        )
        r = reporting.campaign_report(parent)
        self.assertEqual(r["sent"], 10)
        self.assertEqual(r["opened"], 5)
        self.assertEqual(r["bounced"], 5)
        self.assertEqual(r["delivered"], 5)  # only variant A's sends weren't bounced


class CampaignReportViewTests(MarketingTestCase):
    def setUp(self):
        super().setUp()
        self.campaign = Campaign.objects.create(site=self.site, name="Promo", subject="s")

    def _staff_with_marketing(self):
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

    def _url(self):
        return reverse("email_marketing_admin:campaign_report", args=[self.campaign.id])

    def test_report_page_renders_metrics_for_marketing_staff(self):
        sub = self.make_anon_emailable("r@example.com")
        CampaignSend.objects.create(
            campaign=self.campaign,
            subscriber=sub,
            status=CampaignSend.STATUS_SENT,
            opened=True,
        )
        self.client.force_login(self._staff_with_marketing())
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["report"]["delivered"], 1)
        self.assertEqual(resp.context["report"]["open_rate"], 100.0)
        self.assertContains(resp, "Open rate")
        # Time-series chart payload + canvas are present (Slice 1).
        self.assertContains(resp, "em-report-series")
        self.assertContains(resp, "emReportChart")

    def test_non_marketing_staff_is_denied(self):
        user = User.objects.create_user(
            username=f"plain-{uuid.uuid4().hex[:8]}",
            email="plain@test.spwig.com",
            password="pw",
            is_staff=True,
        )
        self.client.force_login(user)
        resp = self.client.get(self._url())
        self.assertIn(resp.status_code, (302, 403))

    def test_unknown_campaign_is_404(self):
        self.client.force_login(self._staff_with_marketing())
        resp = self.client.get(
            reverse("email_marketing_admin:campaign_report", args=[uuid.uuid4()])
        )
        self.assertEqual(resp.status_code, 404)
