"""A/B testing admin UI: setup wizard, detail hub, start/cancel, gating."""

import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from email_marketing.models import ABTest, Campaign, CampaignBlock, Segment
from email_marketing.services import ab_testing

from .base import MarketingTestCase

User = get_user_model()

_MJML = "<mjml><mj-body><mj-section><mj-column><mj-text>Hi</mj-text></mj-column></mj-section></mj-body></mjml>"


class _ABAdminBase(MarketingTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self._staff_with_role())

    def _staff_with_role(self):
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

    def _container(self, with_blocks=False):
        c = Campaign.objects.create(
            site=self.site,
            name="Promo",
            subject="Base subject",
            message_type="newsletter",
            html_content=_MJML,
        )
        if with_blocks:
            CampaignBlock.objects.create(
                campaign=c, block_type="heading", content={"text": "Hi"}, order=0
            )
            CampaignBlock.objects.create(
                campaign=c, block_type="text", content={"text": "Body"}, order=1
            )
        return c

    def _setup_url(self, c):
        return reverse("email_marketing_admin:ab_test_setup", args=[c.id])


class SetupTests(_ABAdminBase):
    def test_get_renders_the_setup_wizard(self):
        c = self._container()
        resp = self.client.get(self._setup_url(c))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'name="test_type"')

    def test_subject_test_creates_variants_sharing_content(self):
        c = self._container()
        resp = self.client.post(
            self._setup_url(c),
            {
                "test_type": "subject",
                "subject": ["Subject A", "Subject B"],
                "sample_percent": "20",
                "winner_metric": "opens",
                "test_window_hours": "4",
                "auto_send_winner": "on",
            },
        )
        self.assertEqual(resp.status_code, 302)
        test = ABTest.objects.get(campaign=c)
        self.assertEqual(test.test_type, "subject")
        variants = list(test.variants.order_by("label"))
        self.assertEqual([v.label for v in variants], ["A", "B"])
        self.assertEqual(variants[0].campaign.subject, "Subject A")
        # Subject test → variants share the container's rendered content.
        self.assertEqual(variants[0].campaign.html_content, c.html_content)
        self.assertEqual(variants[0].campaign.parent_id, c.id)

    def test_content_test_clones_the_container_blocks(self):
        c = self._container(with_blocks=True)
        resp = self.client.post(
            self._setup_url(c),
            {
                "test_type": "content",
                "num_variants": "2",
                "sample_percent": "50",
                "winner_metric": "clicks",
                "test_window_hours": "6",
            },
        )
        self.assertEqual(resp.status_code, 302)
        test = ABTest.objects.get(campaign=c)
        self.assertEqual(test.test_type, "content")
        for variant in test.variants.all():
            # Each variant is its own campaign with a copy of the 2 blocks.
            self.assertEqual(variant.campaign.blocks.count(), 2)
            self.assertNotEqual(variant.campaign_id, c.id)

    def test_subject_test_needs_two_subjects(self):
        c = self._container()
        resp = self.client.post(
            self._setup_url(c),
            {
                "test_type": "subject",
                "subject": ["Only one"],
                "sample_percent": "20",
            },
        )
        self.assertEqual(resp.status_code, 200)  # re-rendered with an error
        self.assertFalse(ABTest.objects.filter(campaign=c).exists())

    def test_subject_test_caps_the_number_of_variants(self):
        # A crafted POST with many subjects must not spawn an unbounded number of
        # child campaigns — the arm count is capped at MAX_VARIANTS.
        c = self._container()
        resp = self.client.post(
            self._setup_url(c),
            {
                "test_type": "subject",
                "subject": [f"Subject {i}" for i in range(9)],
                "sample_percent": "20",
                "winner_metric": "opens",
                "test_window_hours": "4",
            },
        )
        self.assertEqual(resp.status_code, 302)
        test = ABTest.objects.get(campaign=c)
        self.assertEqual(test.variants.count(), ab_testing.MAX_VARIANTS)
        self.assertEqual(
            Campaign.objects.filter(ab_variant__ab_test=test).count(), ab_testing.MAX_VARIANTS
        )


class DetailAndActionTests(_ABAdminBase):
    def _test_with_variants(self):
        c = self._container()
        ab_testing.create_ab_test(
            c, test_type="subject", variant_subjects=["A subj", "B subj"], sample_percent=100
        )
        return ABTest.objects.get(campaign=c)

    def _detail_url(self, test):
        return reverse("email_marketing_admin:ab_test_detail", args=[test.id])

    def test_detail_renders_for_a_draft(self):
        test = self._test_with_variants()
        resp = self.client.get(self._detail_url(test))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Start test")

    def test_start_action_flips_to_testing(self):
        seg = Segment.objects.create(site=self.site, name="A", slug="a", kind=Segment.KIND_STATIC)
        for i in range(20):
            seg.members.add(self.make_anon_emailable(f"m{i}@example.com"))
        c = self._container()
        c.segment = seg
        c.save(update_fields=["segment"])
        ab_testing.create_ab_test(
            c, test_type="subject", variant_subjects=["A", "B"], sample_percent=100
        )
        test = ABTest.objects.get(campaign=c)

        resp = self.client.post(reverse("email_marketing_admin:ab_test_start", args=[test.id]))
        self.assertEqual(resp.status_code, 302)
        test.refresh_from_db()
        self.assertEqual(test.status, ABTest.STATUS_TESTING)

    def test_cancel_action(self):
        test = self._test_with_variants()
        resp = self.client.post(reverse("email_marketing_admin:ab_test_cancel", args=[test.id]))
        self.assertEqual(resp.status_code, 302)
        test.refresh_from_db()
        self.assertEqual(test.status, ABTest.STATUS_CANCELLED)


class GatingTests(_ABAdminBase):
    def test_non_marketing_staff_cannot_reach_setup(self):
        bare = User.objects.create_user(
            username="bare", email="bare@test.spwig.com", password="pw", is_staff=True
        )
        self.client.force_login(bare)
        c = self._container()
        resp = self.client.get(self._setup_url(c))
        self.assertIn(resp.status_code, (302, 403))


class ChangelistExclusionTests(_ABAdminBase):
    def test_variant_child_campaigns_are_hidden_from_the_list(self):
        c = self._container()
        ab_testing.create_ab_test(
            c, test_type="subject", variant_subjects=["A", "B"], sample_percent=100
        )
        resp = self.client.get(
            reverse("email_marketing_admin:filter_campaigns"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()["html"]
        self.assertIn("Promo", body)  # the container shows
        self.assertNotIn("variant A", body)  # its child variants do not


class ReviewFollowupTests(_ABAdminBase):
    """Regressions for the Stage 2 Codex + security review findings."""

    def _with_test(self, **kwargs):
        c = self._container(with_blocks=kwargs.pop("with_blocks", False))
        ab_testing.create_ab_test(
            c,
            test_type=kwargs.get("test_type", "subject"),
            variant_subjects=kwargs.get("variant_subjects", ["A subj", "B subj"]),
            num_variants=kwargs.get("num_variants", 2),
            sample_percent=kwargs.get("sample_percent", 100),
        )
        return c, ABTest.objects.get(campaign=c)

    def test_ab_action_lookups_are_scoped_to_the_current_site(self):
        # A test hanging off another site's campaign must be unreachable, even with
        # a valid UUID — the detail/start/cancel views scope by campaign__site.
        from django.contrib.sites.models import Site

        other = Site.objects.create(domain="other.example", name="Other")
        foreign = Campaign.objects.create(
            site=other, name="Foreign", subject="x", message_type="newsletter", html_content=_MJML
        )
        foreign_test = ABTest.objects.create(
            campaign=foreign,
            test_type="subject",
            winner_metric="opens",
            sample_percent=20,
            test_window_hours=4,
        )
        for name, method in (
            ("ab_test_detail", self.client.get),
            ("ab_test_start", self.client.post),
            ("ab_test_cancel", self.client.post),
        ):
            resp = method(reverse(f"email_marketing_admin:{name}", args=[foreign_test.id]))
            self.assertEqual(resp.status_code, 404, name)

    def test_start_and_cancel_reject_get(self):
        _, test = self._with_test()
        for name in ("ab_test_start", "ab_test_cancel"):
            resp = self.client.get(reverse(f"email_marketing_admin:{name}", args=[test.id]))
            self.assertEqual(resp.status_code, 405, name)

    def test_builder_for_a_variant_links_back_to_the_parent_test(self):
        _, test = self._with_test(with_blocks=True, test_type="content")
        variant = test.variants.first()
        resp = self.client.get(
            reverse("email_marketing_admin:campaign_builder", args=[variant.campaign_id])
        )
        self.assertEqual(resp.status_code, 200)
        # Opening a variant's builder points back at the parent test...
        self.assertContains(resp, reverse("email_marketing_admin:ab_test_detail", args=[test.id]))
        # ...not at a nested "set up A/B test" on the child campaign.
        self.assertNotContains(
            resp, reverse("email_marketing_admin:ab_test_setup", args=[variant.campaign_id])
        )

    def test_cancelled_test_shows_live_metrics_not_snapshot_zero(self):
        from email_marketing.admin_views import _ab_variant_rows
        from email_marketing.models import CampaignSend

        _, test = self._with_test(variant_subjects=["A", "B"])
        variant = test.variants.order_by("label").first()  # label "A"
        CampaignSend.objects.create(
            campaign=variant.campaign,
            subscriber=self.make_anon_emailable("opener@example.com"),
            status=CampaignSend.STATUS_SENT,
            opened=True,
        )
        test.status = ABTest.STATUS_CANCELLED
        test.save(update_fields=["status"])

        row = next(r for r in _ab_variant_rows(test) if r["label"] == "A")
        # Snapshots were never written (only decide_ab_test writes them); the row
        # must fall through to the live CampaignSend counts rather than showing 0.
        self.assertEqual(row["recipients"], 1)
        self.assertEqual(row["opened"], 1)
        self.assertEqual(row["open_rate"], 100.0)

    def test_send_now_refuses_variant_child_campaigns(self):
        from django.contrib.admin.sites import AdminSite
        from django.contrib.messages.storage.fallback import FallbackStorage
        from django.test import RequestFactory

        from email_marketing.admin import CampaignAdmin

        _, test = self._with_test(variant_subjects=["A", "B"])
        variant = test.variants.first()

        request = RequestFactory().post("/")
        request.user = self._staff_with_role()
        request.session = {}
        request._messages = FallbackStorage(request)
        CampaignAdmin(Campaign, AdminSite()).send_now(
            request, Campaign.objects.filter(pk=variant.campaign_id)
        )

        variant.campaign.refresh_from_db()
        self.assertEqual(variant.campaign.status, Campaign.STATUS_DRAFT)  # not sent
        self.assertTrue(
            any("can't be sent directly" in str(m) for m in request._messages),
            "expected a warning that the variant child can't be sent directly",
        )

    def test_variant_name_is_truncated_to_the_model_limit(self):
        # A container name at the column limit would overflow once " — variant A"
        # is appended; create() skips full_clean(), so the service must truncate.
        name_max = Campaign._meta.get_field("name").max_length
        c = Campaign.objects.create(
            site=self.site,
            name="N" * name_max,
            subject="s",
            message_type="newsletter",
            html_content=_MJML,
        )
        ab_testing.create_ab_test(
            c, test_type="subject", variant_subjects=["A", "B"], sample_percent=100
        )
        for variant in ABTest.objects.get(campaign=c).variants.all():
            self.assertLessEqual(len(variant.campaign.name), name_max)


class SignificanceDisplayTests(_ABAdminBase):
    """The results hub shows a significant / inconclusive / not-enough-data verdict."""

    def _seed(self, sends, decide=True):
        from email_marketing.models import CampaignSend

        c = self._container()
        ab_testing.create_ab_test(
            c, test_type="subject", variant_subjects=["A", "B"], sample_percent=100
        )
        test = ABTest.objects.get(campaign=c)
        test.status = ABTest.STATUS_TESTING
        test.save(update_fields=["status"])
        for label, (n, opened) in sends.items():
            variant = test.variants.get(label=label)
            for i in range(n):
                CampaignSend.objects.create(
                    campaign=variant.campaign,
                    subscriber=self.make_anon_emailable(f"{test.id}-{label}{i}@ex.com"),
                    status=CampaignSend.STATUS_SENT,
                    opened=(i < opened),
                )
        if decide:
            ab_testing.decide_ab_test(test)
        return test

    def _detail(self, test):
        return self.client.get(reverse("email_marketing_admin:ab_test_detail", args=[test.id]))

    def test_a_clear_winner_reads_as_significant(self):
        # 20% vs 80% over 40 each — unmistakable.
        resp = self._detail(self._seed({"A": (40, 8), "B": (40, 32)}))
        self.assertContains(resp, "statistically clear")
        self.assertContains(resp, "confidence")

    def test_a_reliable_near_tie_reads_as_inconclusive(self):
        # 45% vs 55% over 100 each — enough data, but too close.
        resp = self._detail(self._seed({"A": (100, 45), "B": (100, 55)}))
        self.assertContains(resp, "Too close to call")

    def test_a_tiny_sample_reads_as_not_enough_data(self):
        resp = self._detail(self._seed({"A": (5, 0), "B": (1, 1)}))
        self.assertContains(resp, "Not enough data")

    def test_a_running_test_shows_the_live_leader(self):
        resp = self._detail(self._seed({"A": (40, 8), "B": (40, 32)}, decide=False))
        self.assertContains(resp, "Leading")
        self.assertContains(resp, "confidence")

    def test_leader_is_ranked_by_raw_rate_not_rounded(self):
        # Both round to 33.3%, but B's true rate is higher — B must lead.
        from email_marketing.admin_views import _significance

        rows = [
            {
                "label": "A",
                "recipients": 10000,
                "opened": 3333,
                "clicked": 0,
                "open_rate": 33.3,
                "click_rate": 0.0,
            },
            {
                "label": "B",
                "recipients": 10000,
                "opened": 3334,
                "clicked": 0,
                "open_rate": 33.3,
                "click_rate": 0.0,
            },
        ]
        result = _significance(rows, ABTest.METRIC_OPENS)
        self.assertEqual(result["leader"], "B")


class RecurringABAdminTests(_ABAdminBase):
    """Recurring A/B: schedule form, wizard redirect, and occurrence results linking."""

    def _recurring(self):
        return Campaign.objects.create(
            site=self.site,
            name="Weekly digest",
            subject="News",
            message_type="newsletter",
            campaign_type=Campaign.TYPE_RECURRING,
            html_content=_MJML,
        )

    def test_broadcast_ab_wizard_redirects_a_recurring_campaign(self):
        c = self._recurring()
        resp = self.client.get(self._setup_url(c))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(str(c.id), resp["Location"])  # -> the campaign change page
        self.assertFalse(ABTest.objects.filter(campaign=c).exists())  # no broadcast test made

    def test_schedule_form_parses_the_subject_textarea_into_a_list(self):
        from email_marketing.admin import CampaignScheduleForm

        form = CampaignScheduleForm()
        form.cleaned_data = {"ab_test_subjects": "First\nSecond\n\n Third "}
        self.assertEqual(form.clean_ab_test_subjects(), ["First", "Second", "Third"])

    def test_schedule_form_rejects_a_lone_subject(self):
        from django import forms as djforms

        from email_marketing.admin import CampaignScheduleForm

        form = CampaignScheduleForm()
        form.cleaned_data = {"ab_test_subjects": "Only one"}
        with self.assertRaises(djforms.ValidationError):
            form.clean_ab_test_subjects()

    def test_occurrence_history_links_ab_occurrences_to_their_results(self):
        from django.contrib.admin.sites import AdminSite

        from email_marketing.admin import CampaignAdmin

        template = self._recurring()
        plain = Campaign.objects.create(
            site=self.site,
            name="Occ plain",
            subject="s",
            parent=template,
            campaign_type=Campaign.TYPE_BROADCAST,
            html_content=_MJML,
        )
        ab_occ = Campaign.objects.create(
            site=self.site,
            name="Occ ab",
            subject="s",
            parent=template,
            campaign_type=Campaign.TYPE_BROADCAST,
            html_content=_MJML,
        )
        ab_testing.create_ab_test(
            ab_occ, test_type="subject", variant_subjects=["A", "B"], sample_percent=100
        )
        test = ABTest.objects.get(campaign=ab_occ)

        html = str(CampaignAdmin(Campaign, AdminSite()).occurrence_history(template))
        self.assertIn(reverse("email_marketing_admin:ab_test_detail", args=[test.id]), html)
        self.assertIn(reverse("admin:email_marketing_campaign_change", args=[plain.id]), html)

    def test_recurring_change_page_exposes_the_ab_fields(self):
        from email_marketing.models import CampaignSchedule

        su = User.objects.create_superuser(
            username=f"su-{uuid.uuid4().hex[:8]}", email="su@test.spwig.com", password="pw"
        )
        self.client.force_login(su)
        c = self._recurring()
        CampaignSchedule.objects.create(campaign=c, cadence="weekly", weekday=0)

        resp = self.client.get(reverse("admin:email_marketing_campaign_change", args=[c.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "A/B subject lines")  # the config is reachable in the admin

    def test_schedule_form_seeds_the_ab_textarea_as_a_string(self):
        from email_marketing.admin import CampaignScheduleForm
        from email_marketing.models import CampaignSchedule

        # A default (empty) schedule must render "" — never "[]", which an unchanged
        # save would parse as one subject and reject.
        empty = CampaignSchedule.objects.create(
            campaign=self._recurring(), cadence="weekly", weekday=0
        )
        self.assertEqual(CampaignScheduleForm(instance=empty).initial.get("ab_test_subjects"), "")
        # A configured schedule seeds the textarea one subject per line.
        configured = CampaignSchedule.objects.create(
            campaign=self._recurring(),
            cadence="weekly",
            weekday=0,
            ab_test_subjects=["First", "Second"],
        )
        self.assertEqual(
            CampaignScheduleForm(instance=configured).initial.get("ab_test_subjects"),
            "First\nSecond",
        )


class ABDashboardTests(_ABAdminBase):
    """The Campaign Studio dashboard surfaces A/B activity (running / decided / journeys)."""

    def _url(self):
        return reverse("email_marketing_admin:dashboard")

    def _seed_test(self, sends, decide, name):
        from email_marketing.models import CampaignSend

        c = self._container()
        c.name = name
        c.save(update_fields=["name"])
        ab_testing.create_ab_test(
            c, test_type="subject", variant_subjects=["A", "B"], sample_percent=100
        )
        test = ABTest.objects.get(campaign=c)
        test.status = ABTest.STATUS_TESTING
        test.save(update_fields=["status"])
        for label, (n, opened) in sends.items():
            variant = test.variants.get(label=label)
            for i in range(n):
                CampaignSend.objects.create(
                    campaign=variant.campaign,
                    subscriber=self.make_anon_emailable(f"{test.id}-{label}{i}@ex.com"),
                    status=CampaignSend.STATUS_SENT,
                    opened=(i < opened),
                )
        if decide:
            ab_testing.decide_ab_test(test)
        return test

    def test_counts_running_and_decided_and_lists_both(self):
        self._seed_test({"A": (40, 8), "B": (40, 32)}, decide=True, name="Decided promo")
        self._seed_test({"A": (20, 4), "B": (20, 10)}, decide=False, name="Running promo")

        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["ab_running"], 1)
        self.assertEqual(resp.context["ab_decided_30d"], 1)
        names = {t["campaign_name"] for t in resp.context["recent_ab_tests"]}
        self.assertEqual(names, {"Decided promo", "Running promo"})

    def test_renders_the_ab_section_with_a_significant_verdict(self):
        # 20% vs 80% over 40 each → a clear, reliable winner.
        self._seed_test({"A": (40, 8), "B": (40, 32)}, decide=True, name="Clear winner promo")
        resp = self.client.get(self._url())
        self.assertContains(resp, "Recent A/B tests")
        self.assertContains(resp, "Clear winner promo")
        self.assertContains(resp, "confidence")  # significant badge

    def test_ab_section_shows_an_empty_state(self):
        resp = self.client.get(self._url())
        self.assertContains(resp, "No A/B tests yet")
        self.assertEqual(resp.context["ab_running"], 0)
        self.assertEqual(resp.context["recent_ab_tests"], [])

    def test_journey_ab_steps_and_winners_are_tallied(self):
        from email_marketing.models import Journey, JourneyNode

        journey = Journey.objects.create(
            site=self.site, name="J", trigger_event="signup", status=Journey.STATUS_ACTIVE
        )
        # An A/B send node with no winner yet…
        JourneyNode.objects.create(
            journey=journey,
            node_type=JourneyNode.TYPE_SEND_EMAIL,
            config={"ab_test_type": "subject", "variant_subjects": ["S1", "S2"]},
        )
        # …and one with a locked winner.
        JourneyNode.objects.create(
            journey=journey,
            node_type=JourneyNode.TYPE_SEND_EMAIL,
            config={
                "ab_test_type": "subject",
                "variant_subjects": ["S1", "S2"],
                "ab_winner_label": "A",
            },
        )
        resp = self.client.get(self._url())
        self.assertEqual(resp.context["journey_ab_steps"], 2)
        self.assertEqual(resp.context["journey_ab_winners"], 1)

    def test_legacy_completed_test_verdict_is_recomputed_from_snapshot(self):
        # A completed test with winner_confidence=None (a legacy test decided before
        # the field existed) must have its dashboard verdict recomputed from the
        # snapshot, not always read "not enough data".
        test = self._seed_test({"A": (40, 8), "B": (40, 32)}, decide=True, name="Legacy promo")
        test.winner_confidence = None  # simulate a pre-field completed test
        test.save(update_fields=["winner_confidence"])

        resp = self.client.get(self._url())
        row = next(
            t for t in resp.context["recent_ab_tests"] if t["campaign_name"] == "Legacy promo"
        )
        self.assertEqual(row["verdict"], "significant")  # recomputed, not "insufficient"
