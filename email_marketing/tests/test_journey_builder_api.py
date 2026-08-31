"""Behaviour tests for the journey builder — the flowchart canvas + its API.

The view ``journey_builder`` renders the canvas shell; the
``email_marketing_api`` node/edge endpoints persist the graph. All are staff-only
and gated on the ``marketing`` category at ``full``.
"""

import json
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone

from email_marketing.models import (
    Campaign,
    Journey,
    JourneyEdge,
    JourneyNode,
    Segment,
)

from .base import MarketingTestCase

User = get_user_model()


class _JourneyBuilderBase(MarketingTestCase):
    def setUp(self):
        super().setUp()
        self.journey = Journey.objects.create(
            site=self.site, name="Welcome", trigger_event=Journey.TRIGGER_SIGNUP
        )

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

    def _entry(self):
        return JourneyNode.objects.create(journey=self.journey, node_type=JourneyNode.TYPE_ENTRY)

    def _node(self, node_type, **config):
        return JourneyNode.objects.create(
            journey=self.journey, node_type=node_type, config=config or {}
        )

    def _post(self, name, args, payload):
        return self.client.post(
            reverse(name, args=args),
            data=json.dumps(payload),
            content_type="application/json",
        )


class JourneyBuilderViewTests(_JourneyBuilderBase):
    def _url(self, journey_id=None):
        return reverse(
            "email_marketing_admin:journey_builder", args=[journey_id or self.journey.id]
        )

    def test_staff_with_role_gets_the_canvas_and_an_entry_node(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'id="jb-canvas"')
        self.assertContains(resp, 'id="jb-nodes-data"')
        # Opening the builder seeds the graph's single entry node.
        self.assertEqual(self.journey.nodes.filter(node_type=JourneyNode.TYPE_ENTRY).count(), 1)

    def test_non_staff_is_redirected(self):
        User.objects.create_user(username="c", email="c@test.spwig.com", password="pw")
        self.client.login(username="c", password="pw")
        resp = self.client.get(self._url())
        self.assertIn(resp.status_code, (302, 403))

    def test_unknown_journey_is_404(self):
        self.client.force_login(self._staff_with_role())
        self.assertEqual(self.client.get(self._url(uuid.uuid4())).status_code, 404)


class JourneyNodeApiTests(_JourneyBuilderBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self._staff_with_role())

    def test_create_node(self):
        resp = self._post(
            "email_marketing_api:create_journey_node",
            [self.journey.id],
            {
                "node_type": "wait_delay",
                "pos_x": 100,
                "pos_y": 200,
                "config": {"value": 3, "unit": "days"},
            },
        )
        self.assertEqual(resp.status_code, 200)
        node = resp.json()["node"]
        self.assertEqual(node["node_type"], "wait_delay")
        self.assertEqual(node["config"], {"value": 3, "unit": "days"})
        self.assertTrue(JourneyNode.objects.filter(id=node["id"]).exists())

    def test_unknown_node_type_is_rejected(self):
        resp = self._post(
            "email_marketing_api:create_journey_node",
            [self.journey.id],
            {"node_type": "nonsense"},
        )
        self.assertEqual(resp.status_code, 400)

    def test_only_one_entry_node_allowed(self):
        self._entry()
        resp = self._post(
            "email_marketing_api:create_journey_node",
            [self.journey.id],
            {"node_type": "entry"},
        )
        self.assertEqual(resp.status_code, 409)

    def test_send_config_drops_a_bogus_campaign_id(self):
        node = self._node("send_email")
        resp = self._post(
            "email_marketing_api:update_journey_node",
            [node.id],
            {"config": {"campaign_id": str(uuid.uuid4())}},  # not a real campaign
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["node"]["config"], {})

    def test_malformed_campaign_id_is_dropped_not_500(self):
        node = self._node("send_email")
        resp = self._post(
            "email_marketing_api:update_journey_node",
            [node.id],
            {"config": {"campaign_id": "not-a-uuid"}},  # would ValidationError on a UUID pk
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["node"]["config"], {})

    def test_send_config_keeps_a_real_campaign_id(self):
        campaign = Campaign.objects.create(site=self.site, name="C", subject="s")
        node = self._node("send_email")
        resp = self._post(
            "email_marketing_api:update_journey_node",
            [node.id],
            {"config": {"campaign_id": str(campaign.id)}},
        )
        self.assertEqual(resp.json()["node"]["config"], {"campaign_id": str(campaign.id)})

    def test_update_moves_a_node(self):
        node = self._node("wait_delay", value=1, unit="days")
        resp = self._post(
            "email_marketing_api:update_journey_node", [node.id], {"pos_x": 500, "pos_y": 600}
        )
        self.assertEqual(resp.status_code, 200)
        node.refresh_from_db()
        self.assertEqual((node.pos_x, node.pos_y), (500, 600))

    def test_entry_node_cannot_be_deleted(self):
        entry = self._entry()
        resp = self.client.post(reverse("email_marketing_api:delete_journey_node", args=[entry.id]))
        self.assertEqual(resp.status_code, 400)
        self.assertTrue(JourneyNode.objects.filter(id=entry.id).exists())

    def test_delete_removes_a_node(self):
        node = self._node("exit")
        resp = self.client.post(reverse("email_marketing_api:delete_journey_node", args=[node.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(JourneyNode.objects.filter(id=node.id).exists())


class JourneyEdgeApiTests(_JourneyBuilderBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self._staff_with_role())

    def _edge(self, from_node, to_node, branch="default"):
        return self._post(
            "email_marketing_api:create_journey_edge",
            [self.journey.id],
            {"from": str(from_node.id), "to": str(to_node.id), "branch": branch},
        )

    def test_connect_two_nodes(self):
        a, b = self._entry(), self._node("exit")
        resp = self._edge(a, b)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(JourneyEdge.objects.filter(from_node=a, to_node=b).exists())

    def test_self_loop_is_rejected(self):
        a = self._node("send_email")
        self.assertEqual(self._edge(a, a).status_code, 400)

    def test_branch_node_requires_yes_or_no(self):
        seg = Segment.objects.create(site=self.site, name="S", slug="s", kind=Segment.KIND_STATIC)
        branch = self._node("branch", condition="in_segment", segment_id=str(seg.id))
        target = self._node("exit")
        self.assertEqual(self._edge(branch, target, "default").status_code, 400)
        self.assertEqual(self._edge(branch, target, "yes").status_code, 200)

    def test_linear_node_rejects_yes_no(self):
        a, b = self._node("send_email"), self._node("exit")
        self.assertEqual(self._edge(a, b, "yes").status_code, 400)

    def test_exit_node_has_no_output(self):
        a, b = self._node("exit"), self._node("send_email")
        self.assertEqual(self._edge(a, b).status_code, 400)

    def test_second_edge_on_same_output_replaces_the_first(self):
        a = self._node("send_email")
        b, c = self._node("exit"), self._node("wait_delay", value=1, unit="days")
        self._edge(a, b)
        self._edge(a, c)  # replaces a->b
        edges = JourneyEdge.objects.filter(from_node=a, branch="default")
        self.assertEqual(edges.count(), 1)
        self.assertEqual(edges.first().to_node_id, c.id)

    def test_delete_edge(self):
        a, b = self._entry(), self._node("exit")
        self._edge(a, b)
        edge = JourneyEdge.objects.get(from_node=a, to_node=b)
        resp = self.client.post(reverse("email_marketing_api:delete_journey_edge", args=[edge.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(JourneyEdge.objects.filter(id=edge.id).exists())


class JourneyAdminRedirectTests(_JourneyBuilderBase):
    def test_admin_add_redirects_to_the_builder(self):
        user = User.objects.create_user(
            username="super",
            email="s@test.spwig.com",
            password="pw",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(user)
        resp = self.client.post(
            reverse("admin:email_marketing_journey_add"),
            data={
                "name": "New Journey",
                "trigger_event": Journey.TRIGGER_SIGNUP,
                "status": Journey.STATUS_DRAFT,
                "once_per_subscriber": "on",
                "cooldown_days": "0",
            },
        )
        journey = Journey.objects.get(name="New Journey")
        self.assertRedirects(
            resp,
            reverse("email_marketing_admin:journey_builder", args=[journey.id]),
            fetch_redirect_response=False,
        )


class JourneyShareApiTests(_JourneyBuilderBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self._staff_with_role())

    def test_list_templates(self):
        resp = self.client.get(reverse("email_marketing_api:list_journey_templates"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json()["templates"]) >= 1)

    def test_apply_template_builds_a_graph(self):
        resp = self._post(
            "email_marketing_api:apply_journey_template",
            [self.journey.id],
            {"template_key": "welcome"},
        )
        self.assertEqual(resp.status_code, 200)
        graph = resp.json()["graph"]
        self.assertTrue(len(graph["nodes"]) > 1)
        self.assertEqual(self.journey.nodes.filter(node_type=JourneyNode.TYPE_ENTRY).count(), 1)

    def test_apply_unknown_template_is_rejected(self):
        resp = self._post(
            "email_marketing_api:apply_journey_template",
            [self.journey.id],
            {"template_key": "nope"},
        )
        self.assertEqual(resp.status_code, 400)

    def test_export_returns_a_downloadable_document(self):
        JourneyNode.objects.create(journey=self.journey, node_type=JourneyNode.TYPE_ENTRY)
        resp = self.client.get(
            reverse("email_marketing_api:export_journey", args=[self.journey.id])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("attachment", resp["Content-Disposition"])
        self.assertEqual(resp.json()["spwig_journey"], 1)

    def test_export_then_import_round_trips_through_the_api(self):
        from email_marketing.models import Campaign

        campaign = Campaign.objects.create(site=self.site, name="Hello", subject="s")
        entry = self._entry()
        send = self._node("send_email", campaign_id=str(campaign.id))
        JourneyEdge.objects.create(journey=self.journey, from_node=entry, to_node=send)

        exported = self.client.get(
            reverse("email_marketing_api:export_journey", args=[self.journey.id])
        ).json()

        other = Journey.objects.create(
            site=self.site, name="Other", trigger_event=Journey.TRIGGER_SIGNUP
        )
        resp = self._post("email_marketing_api:import_journey", [other.id], {"doc": exported})
        self.assertEqual(resp.status_code, 200)
        imported_send = other.nodes.filter(node_type="send_email").first()
        self.assertEqual(imported_send.config.get("campaign_id"), str(campaign.id))

    def test_import_rejects_a_bogus_document(self):
        resp = self._post(
            "email_marketing_api:import_journey", [self.journey.id], {"doc": {"nope": True}}
        )
        self.assertEqual(resp.status_code, 422)


class JourneyStatsAndActivateTests(_JourneyBuilderBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self._staff_with_role())

    def _complete_graph(self):
        from email_marketing.models import Campaign

        c = Campaign.objects.create(site=self.site, name="C", subject="s")
        entry = self._entry()
        send = self._node("send_email", campaign_id=str(c.id))
        JourneyEdge.objects.create(journey=self.journey, from_node=entry, to_node=send)
        return entry, send

    def test_node_stats_counts_active_enrollments_by_current_node(self):
        from email_marketing.models import JourneyEnrollment

        entry, send = self._complete_graph()
        sub = self.make_anon_emailable("s@example.com")
        JourneyEnrollment.objects.create(
            journey=self.journey,
            subscriber=sub,
            current_node=send,
            next_step_at=timezone.now(),
            status=JourneyEnrollment.STATUS_ACTIVE,
        )
        resp = self.client.get(
            reverse("email_marketing_api:journey_node_stats", args=[self.journey.id])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["counts"].get(str(send.id)), 1)

    def test_validate_reports_issues(self):
        self._entry()  # entry only → not activatable
        resp = self.client.get(
            reverse("email_marketing_api:validate_journey", args=[self.journey.id])
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertFalse(body["can_activate"])
        self.assertTrue(body["issues"])

    def test_activate_is_blocked_when_invalid(self):
        self._entry()  # incomplete
        resp = self._post(
            "email_marketing_api:set_journey_status", [self.journey.id], {"status": "active"}
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertFalse(body["success"])
        self.assertTrue(body["blocked"])
        self.journey.refresh_from_db()
        self.assertEqual(self.journey.status, Journey.STATUS_DRAFT)  # unchanged

    def test_activate_succeeds_on_a_complete_graph(self):
        self._complete_graph()
        resp = self._post(
            "email_marketing_api:set_journey_status", [self.journey.id], {"status": "active"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["success"])
        self.journey.refresh_from_db()
        self.assertEqual(self.journey.status, Journey.STATUS_ACTIVE)

    def test_pause_always_applies(self):
        self._complete_graph()
        self.journey.status = Journey.STATUS_ACTIVE
        self.journey.save(update_fields=["status"])
        resp = self._post(
            "email_marketing_api:set_journey_status", [self.journey.id], {"status": "paused"}
        )
        self.assertTrue(resp.json()["success"])
        self.journey.refresh_from_db()
        self.assertEqual(self.journey.status, Journey.STATUS_PAUSED)

    def test_invalid_status_is_rejected(self):
        resp = self._post(
            "email_marketing_api:set_journey_status", [self.journey.id], {"status": "banana"}
        )
        self.assertEqual(resp.status_code, 400)
