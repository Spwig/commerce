"""Journey-level report: enrollment funnel + attributed revenue (total + per step)."""

import uuid
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from attribution.models import Campaign as AttributionCampaign
from attribution.models import TouchPoint
from attribution.services.resolution import resolve_order
from email_marketing.models import Campaign, Journey, JourneyEnrollment, JourneyNode
from email_marketing.services import reporting
from email_marketing.services.attribution_link import ensure_attribution_campaign

from .base import MarketingTestCase

User = get_user_model()


class _JBase(MarketingTestCase):
    def _journey(self, **kw):
        kw.setdefault("trigger_event", Journey.TRIGGER_CART_ABANDONED)
        kw.setdefault("status", Journey.STATUS_ACTIVE)
        return Journey.objects.create(site=self.site, name="J", **kw)

    def _enroll(self, journey, status, n=1):
        for _ in range(n):
            JourneyEnrollment.objects.create(
                journey=journey,
                subscriber=self.make_subscriber(f"{uuid.uuid4().hex[:8]}@ex.com"),
                status=status,
                next_step_at=timezone.now(),
            )


class JourneyNodeCampaignIdsTests(_JBase):
    def test_single_send_node(self):
        j = self._journey()
        c = Campaign.objects.create(site=self.site, name="C", subject="s")
        node = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        self.assertEqual(reporting._journey_node_campaign_ids(node), [str(c.id)])

    def test_content_ab_node_collects_all_arms(self):
        j = self._journey()
        a, b = uuid.uuid4().hex, uuid.uuid4().hex
        node = self.add_node(
            j, JourneyNode.TYPE_SEND_EMAIL, ab_test_type="content", variant_campaign_ids=[a, b]
        )
        self.assertEqual(reporting._journey_node_campaign_ids(node), [a, b])

    def test_malformed_campaign_id_is_dropped_not_500(self):
        # A hand-edited / imported node config with a non-UUID id must not blow up the
        # report (it would otherwise raise ValidationError at filter(id__in=...)).
        j = self._journey()
        node = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id="not-a-uuid")
        self.assertEqual(reporting._journey_node_campaign_ids(node), [])
        # journey_revenue tolerates it → zero revenue, no exception.
        self.assertEqual(reporting.journey_revenue(j)["revenue"], Decimal("0.00"))

    def test_subject_ab_node_excludes_subject_strings(self):
        j = self._journey()
        c = Campaign.objects.create(site=self.site, name="C", subject="s")
        node = self.add_node(
            j,
            JourneyNode.TYPE_SEND_EMAIL,
            ab_test_type="subject",
            campaign_id=str(c.id),
            variant_subjects=["Subject A", "Subject B"],
        )
        # Only the single base campaign id — subject strings are not campaign ids.
        self.assertEqual(reporting._journey_node_campaign_ids(node), [str(c.id)])


class JourneyFunnelTests(_JBase):
    def test_counts_by_status(self):
        j = self._journey()
        self._enroll(j, JourneyEnrollment.STATUS_ACTIVE, 2)
        self._enroll(j, JourneyEnrollment.STATUS_COMPLETED, 1)
        self._enroll(j, JourneyEnrollment.STATUS_CANCELLED, 1)
        self.assertEqual(
            reporting.journey_funnel(j),
            {"enrolled": 4, "active": 2, "completed": 1, "cancelled": 1},
        )

    def test_empty_journey(self):
        self.assertEqual(
            reporting.journey_funnel(self._journey()),
            {"enrolled": 0, "active": 0, "completed": 0, "cancelled": 0},
        )


class JourneyRevenueTests(_JBase):
    def _attribute(self, campaign, amount):
        from tests.factories import OrderFactory

        user = User.objects.create_user(
            username=f"b-{uuid.uuid4().hex[:8]}",
            email=f"{uuid.uuid4().hex[:8]}@ex.com",
            password="x",
        )
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

    def test_revenue_total_steps_and_per_enrollee(self):
        j = self._journey()
        c = Campaign.objects.create(site=self.site, name="Welcome offer", subject="s")
        self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        self._enroll(j, JourneyEnrollment.STATUS_ACTIVE, 2)  # 2 enrolled → per-enrollee = rev/2
        self._attribute(c, Decimal("100.00"))

        rev = reporting.journey_revenue(j)
        self.assertEqual(rev["revenue"], Decimal("100.00"))
        self.assertEqual(rev["orders"], 1)
        self.assertEqual(rev["aov"], Decimal("100.00"))
        self.assertEqual(rev["revenue_per_enrollee"], Decimal("50.00"))
        self.assertEqual(len(rev["steps"]), 1)
        step = rev["steps"][0]
        self.assertEqual(step["revenue"], Decimal("100.00"))
        self.assertEqual(step["label"], "Welcome offer")
        self.assertFalse(step["ab"])
        # Engagement is always present now (zero here — no actual journey send occurred).
        self.assertEqual(step["engagement"], {"sent": 0, "opened": 0, "clicked": 0})

    def test_plain_send_records_step_send_and_engagement_rolls_up(self):
        # The deferred follow-up: a plain (non-A/B) journey send now records a
        # JourneyStepSend (variant ""), so per-step opens/clicks work for all steps.
        from email_marketing.models import JourneyStepSend
        from email_marketing.services.journeys import advance_enrollment
        from email_system.models import EmailEvent, EmailOutbox

        j = self._journey()
        c = Campaign.objects.create(
            site=self.site,
            name="Step",
            subject="Hi",
            html_content=(
                "<mjml><mj-body><mj-section><mj-column>"
                "<mj-text>hi</mj-text></mj-column></mj-section></mj-body></mjml>"
            ),
        )
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        send = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        exit_node = self.add_node(j, JourneyNode.TYPE_EXIT)
        self.add_edge(j, entry, send)
        self.add_edge(j, send, exit_node)

        sub = self.make_anon_emailable("enrollee@ex.com")
        enr = JourneyEnrollment.objects.create(
            journey=j,
            subscriber=sub,
            current_node=send,
            status=JourneyEnrollment.STATUS_ACTIVE,
            next_step_at=timezone.now(),
        )
        advance_enrollment(enr)

        sends = JourneyStepSend.objects.filter(node=send)
        self.assertEqual(sends.count(), 1)
        jss = sends.first()
        self.assertEqual(jss.variant, "")  # plain step

        # An open event on the send's outbox rolls up onto the JourneyStepSend.
        outbox = EmailOutbox.objects.get(id=jss.outbox_id)
        EmailEvent.objects.create(email=outbox, event_type="opened")
        jss.refresh_from_db()
        self.assertTrue(jss.opened)

        step = reporting.journey_revenue(j)["steps"][0]
        self.assertEqual(step["engagement"], {"sent": 1, "opened": 1, "clicked": 0})

    def test_revenue_zero_when_nothing_attributed(self):
        j = self._journey()
        c = Campaign.objects.create(site=self.site, name="C", subject="s")
        self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        rev = reporting.journey_revenue(j)
        self.assertEqual(rev["revenue"], Decimal("0.00"))
        self.assertEqual(rev["revenue_per_enrollee"], Decimal("0.00"))


class JourneyReportViewTests(_JBase):
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

    def _url(self, journey):
        return reverse("email_marketing_admin:journey_report", args=[journey.id])

    def test_renders_for_marketing_staff(self):
        j = self._journey()
        self._enroll(j, JourneyEnrollment.STATUS_ACTIVE, 1)
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(self._url(j))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Attributed revenue")
        self.assertEqual(resp.context["funnel"]["enrolled"], 1)

    def test_non_marketing_staff_denied(self):
        j = self._journey()
        user = User.objects.create_user(
            username=f"p-{uuid.uuid4().hex[:6]}",
            email="p@test.spwig.com",
            password="pw",
            is_staff=True,
        )
        self.client.force_login(user)
        self.assertIn(self.client.get(self._url(j)).status_code, (302, 403))

    def test_unknown_journey_404(self):
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(reverse("email_marketing_admin:journey_report", args=[uuid.uuid4()]))
        self.assertEqual(resp.status_code, 404)
