"""Journey A/B: variant assignment, per-send tracking, engagement rollup, auto-lock."""

import uuid
from unittest import mock

from django.utils import timezone

from email_marketing.models import (
    Campaign,
    Journey,
    JourneyEnrollment,
    JourneyNode,
    JourneyStepSend,
)
from email_marketing.services import journeys as journey_svc

from .base import MarketingTestCase


class _JourneyABBase(MarketingTestCase):
    def _email(self, name="Step"):
        return Campaign.objects.create(
            site=self.site, name=name, subject="Hi", message_type="newsletter", html_content="x"
        )

    def _journey(self, status=Journey.STATUS_ACTIVE):
        return Journey.objects.create(
            site=self.site, name="Welcome", trigger_event=Journey.TRIGGER_SIGNUP, status=status
        )

    def _ab_send_node(
        self, journey, *, test_type="content", campaigns=None, base=None, subjects=None
    ):
        if test_type == "content":
            cfg = {
                "ab_test_type": "content",
                "variant_campaign_ids": [str(c.id) for c in campaigns],
            }
        else:
            cfg = {
                "ab_test_type": "subject",
                "campaign_id": str(base.id),
                "variant_subjects": subjects,
            }
        return self.add_node(journey, JourneyNode.TYPE_SEND_EMAIL, **cfg)

    def _wire_entry_send_exit(self, journey, send):
        entry = self.add_node(journey, JourneyNode.TYPE_ENTRY)
        exit_node = self.add_node(journey, JourneyNode.TYPE_EXIT)
        self.add_edge(journey, entry, send)
        self.add_edge(journey, send, exit_node)

    def _seed_sends(self, node, label, n, opened=0, clicked=0):
        sub = self.make_anon_emailable(f"{node.id}-{label}@ex.com")
        enr = JourneyEnrollment.objects.create(
            journey=node.journey, subscriber=sub, current_node=node, next_step_at=timezone.now()
        )
        for i in range(n):
            JourneyStepSend.objects.create(
                node=node,
                enrollment=enr,
                variant=label,
                outbox_id=uuid.uuid4(),
                opened=(i < opened),
                clicked=(i < clicked),
            )


class AssignmentTests(_JourneyABBase):
    def test_content_assignment_is_deterministic_and_stable(self):
        c1, c2 = self._email("A"), self._email("B")
        node = self._ab_send_node(self._journey(), test_type="content", campaigns=[c1, c2])
        sub = self.make_anon_emailable("a@ex.com")

        campaign, subject_override, label = journey_svc._resolve_node_send(node, sub)
        again = journey_svc._resolve_node_send(node, sub)

        self.assertEqual(label, again[2])  # stable
        self.assertIn(label, ["A", "B"])
        self.assertIsNone(subject_override)  # content: no subject swap
        self.assertEqual(campaign.id, (c1 if label == "A" else c2).id)

    def test_subject_variant_uses_the_base_campaign_with_an_override(self):
        base = self._email("Base")
        node = self._ab_send_node(
            self._journey(), test_type="subject", base=base, subjects=["Subj A", "Subj B"]
        )
        campaign, subject_override, label = journey_svc._resolve_node_send(
            node, self.make_anon_emailable("s@ex.com")
        )
        self.assertEqual(campaign.id, base.id)
        self.assertIn(subject_override, ["Subj A", "Subj B"])
        self.assertIn(label, ["A", "B"])

    def test_a_plain_send_node_is_unchanged(self):
        base = self._email("Plain")
        node = self.add_node(self._journey(), JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(base.id))
        campaign, subject_override, label = journey_svc._resolve_node_send(
            node, self.make_anon_emailable("p@ex.com")
        )
        self.assertEqual(campaign.id, base.id)
        self.assertIsNone(subject_override)
        self.assertEqual(label, "")

    def test_a_locked_node_sends_only_the_winner(self):
        c1, c2 = self._email("A"), self._email("B")
        node = self._ab_send_node(self._journey(), test_type="content", campaigns=[c1, c2])
        node.config["ab_winner_label"] = "B"
        node.save(update_fields=["config"])
        for i in range(5):
            campaign, _, label = journey_svc._resolve_node_send(
                node, self.make_anon_emailable(f"w{i}@ex.com")
            )
            self.assertEqual(label, "B")
            self.assertEqual(campaign.id, c2.id)


class RecordingTests(_JourneyABBase):
    def test_advance_records_a_variant_send_with_the_outbox_id(self):
        journey = self._journey()
        c1, c2 = self._email("A"), self._email("B")
        send = self._ab_send_node(journey, test_type="content", campaigns=[c1, c2])
        self._wire_entry_send_exit(journey, send)
        enrollment = journey_svc.enroll_subscriber(journey, self.make_anon_emailable("adv@ex.com"))

        outbox = uuid.uuid4()
        with mock.patch(
            "email_marketing.services.campaigns.send_campaign_to_subscriber",
            return_value={"queued": True, "outbox_id": str(outbox)},
        ):
            journey_svc.advance_enrollment(enrollment)

        jss = JourneyStepSend.objects.get(node=send)
        self.assertEqual(str(jss.outbox_id), str(outbox))
        self.assertIn(jss.variant, ["A", "B"])
        self.assertEqual(jss.enrollment_id, enrollment.id)

    def test_a_skipped_send_records_nothing(self):
        journey = self._journey()
        c1, c2 = self._email("A"), self._email("B")
        send = self._ab_send_node(journey, test_type="content", campaigns=[c1, c2])
        self._wire_entry_send_exit(journey, send)
        enrollment = journey_svc.enroll_subscriber(journey, self.make_anon_emailable("skip@ex.com"))

        with mock.patch(
            "email_marketing.services.campaigns.send_campaign_to_subscriber",
            return_value={"queued": False, "reason": "not_emailable"},  # no outbox_id
        ):
            journey_svc.advance_enrollment(enrollment)

        self.assertFalse(JourneyStepSend.objects.filter(node=send).exists())


class EngagementRollupTests(_JourneyABBase):
    def test_an_open_event_rolls_up_onto_the_variant_send(self):
        from email_system.models import EmailEvent, EmailOutbox

        node = self._ab_send_node(
            self._journey(), test_type="content", campaigns=[self._email("A"), self._email("B")]
        )
        enr = JourneyEnrollment.objects.create(
            journey=node.journey,
            subscriber=self.make_anon_emailable("o@ex.com"),
            current_node=node,
            next_step_at=timezone.now(),
        )
        outbox = EmailOutbox.objects.create(
            site=self.site, account=self.account, to_email="o@ex.com", subject="s", html_body="b"
        )
        jss = JourneyStepSend.objects.create(
            node=node, enrollment=enr, variant="A", outbox_id=outbox.id
        )

        # A real EmailEvent fires the (public-endpoint) rollup signal.
        EmailEvent.objects.create(email=outbox, event_type="clicked", occurred_at=timezone.now())

        jss.refresh_from_db()
        self.assertTrue(jss.clicked)
        self.assertTrue(jss.opened)  # a click implies an open


class WinnerLockTests(_JourneyABBase):
    def test_beat_locks_a_clear_winner(self):
        journey = self._journey()
        send = self._ab_send_node(
            journey, test_type="content", campaigns=[self._email("A"), self._email("B")]
        )
        self._seed_sends(send, "A", 40, opened=8)  # 20%
        self._seed_sends(send, "B", 40, opened=32)  # 80% — clear winner

        out = journey_svc.lock_due_journey_winners()

        self.assertEqual(out["locked"], 1)
        send.refresh_from_db()
        self.assertEqual(send.ab_winner_label, "B")
        self.assertTrue(send.config.get("ab_winner_locked_at"))

    def test_beat_leaves_a_small_sample_unlocked(self):
        journey = self._journey()
        send = self._ab_send_node(
            journey, test_type="content", campaigns=[self._email("A"), self._email("B")]
        )
        self._seed_sends(send, "A", 3, opened=0)
        self._seed_sends(send, "B", 3, opened=1)  # too small to trust

        out = journey_svc.lock_due_journey_winners()

        self.assertEqual(out["locked"], 0)
        send.refresh_from_db()
        self.assertEqual(send.ab_winner_label, "")


class SanitizerTests(_JourneyABBase):
    def test_content_ab_config_is_accepted_and_a_client_winner_is_stripped(self):
        from email_marketing.api_views import _sanitize_node_config

        c1, c2 = self._email("A"), self._email("B")
        out = _sanitize_node_config(
            JourneyNode.TYPE_SEND_EMAIL,
            {
                "ab_test_type": "content",
                "variant_campaign_ids": [str(c1.id), str(c2.id)],
                "ab_metric": "clicks",
                "ab_winner_label": "A",  # a crafted payload must not force a winner
            },
        )
        self.assertEqual(out["ab_test_type"], "content")
        self.assertEqual(out["variant_campaign_ids"], [str(c1.id), str(c2.id)])
        self.assertEqual(out["ab_metric"], "clicks")
        self.assertNotIn("ab_winner_label", out)

    def test_a_lone_variant_falls_back_to_a_plain_send(self):
        from email_marketing.api_views import _sanitize_node_config

        c1 = self._email("A")
        out = _sanitize_node_config(
            JourneyNode.TYPE_SEND_EMAIL,
            {
                "ab_test_type": "content",
                "variant_campaign_ids": [str(c1.id)],
                "campaign_id": str(c1.id),
            },
        )
        self.assertNotIn("ab_test_type", out)
        self.assertEqual(out["campaign_id"], str(c1.id))

    def test_a_locked_winner_is_carried_only_when_the_test_is_unchanged(self):
        from email_marketing.api_views import _carry_winner

        locked = {
            "ab_test_type": "content",
            "variant_campaign_ids": ["a", "b"],
            "ab_metric": "opens",
            "ab_winner_label": "B",
            "ab_winner_locked_at": "t",
        }
        # Same arms + metric → keep the winner.
        same = _carry_winner(
            dict(locked),
            {"ab_test_type": "content", "variant_campaign_ids": ["a", "b"], "ab_metric": "opens"},
        )
        self.assertEqual(same["ab_winner_label"], "B")
        # Swapped a variant → reset (a fresh test must re-earn a winner).
        swapped = _carry_winner(
            dict(locked),
            {"ab_test_type": "content", "variant_campaign_ids": ["a", "c"], "ab_metric": "opens"},
        )
        self.assertNotIn("ab_winner_label", swapped)
        # Changed the metric → reset.
        remetric = _carry_winner(
            dict(locked),
            {"ab_test_type": "content", "variant_campaign_ids": ["a", "b"], "ab_metric": "clicks"},
        )
        self.assertNotIn("ab_winner_label", remetric)


class StatsAndValidationTests(_JourneyABBase):
    def test_ab_summary_reports_per_variant_rates_and_winner(self):
        from email_marketing.api_views import _journey_ab_summary

        node = self._ab_send_node(
            self._journey(), test_type="content", campaigns=[self._email("A"), self._email("B")]
        )
        self._seed_sends(node, "A", 20, opened=4)  # 20%
        self._seed_sends(node, "B", 20, opened=16)  # 80%
        node.config["ab_winner_label"] = "B"
        node.save(update_fields=["config"])

        summary = _journey_ab_summary(node)

        self.assertEqual(summary["winner"], "B")
        self.assertEqual(summary["metric"], "opens")
        rates = {v["label"]: v["open_rate"] for v in summary["variants"]}
        self.assertEqual(rates["A"], 20.0)
        self.assertEqual(rates["B"], 80.0)
        self.assertIsNotNone(summary["confidence"])  # a 40-recipient split is reliable

    def _linear_ab(self, **node_cfg):
        journey = self._journey()
        entry = self.add_node(journey, JourneyNode.TYPE_ENTRY)
        send = self.add_node(journey, JourneyNode.TYPE_SEND_EMAIL, **node_cfg)
        exit_node = self.add_node(journey, JourneyNode.TYPE_EXIT)
        self.add_edge(journey, entry, send)
        self.add_edge(journey, send, exit_node)
        return journey

    def test_validation_flags_an_under_configured_ab_step(self):
        from email_marketing.services.journey_validation import validate_journey

        journey = self._linear_ab(
            ab_test_type="content",
            variant_campaign_ids=[str(self._email("A").id)],  # only one
        )
        issues = validate_journey(journey)
        self.assertTrue(any("at least two email variants" in i["message"] for i in issues))

    def test_validation_accepts_a_valid_content_ab_step(self):
        from email_marketing.services.journey_validation import validate_journey

        c1, c2 = self._email("A"), self._email("B")
        journey = self._linear_ab(
            ab_test_type="content", variant_campaign_ids=[str(c1.id), str(c2.id)]
        )
        issues = validate_journey(journey)
        self.assertFalse(any("Send email" in i["message"] for i in issues))

    def test_variant_sends_reset_when_the_test_is_redefined(self):
        from email_marketing.api_views import _reset_ab_sends_if_changed

        node = self._ab_send_node(
            self._journey(), test_type="content", campaigns=[self._email("A"), self._email("B")]
        )
        self._seed_sends(node, "A", 5)
        self._seed_sends(node, "B", 5)
        old = dict(node.config)

        # Same arms → old sends are kept.
        _reset_ab_sends_if_changed(node, old, dict(old))
        self.assertEqual(JourneyStepSend.objects.filter(node=node).count(), 10)
        # Swapped arms → old engagement is discarded so the new test starts clean.
        _reset_ab_sends_if_changed(
            node, old, {"ab_test_type": "content", "variant_campaign_ids": ["x", "y"]}
        )
        self.assertEqual(JourneyStepSend.objects.filter(node=node).count(), 0)
