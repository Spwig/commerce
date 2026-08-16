"""Regression tests for the visibility rule builder admin view + save API.

Guards the fix in commit 19290a939: the ``page_builder -> visibility`` app move
(9140a4c27) left eight ORM queries in the rule builder addressing
``RuleGroupMember``'s FK to ``RuleGroup`` as ``group=`` instead of the real field
``rule_group=``, raising ``FieldError: Cannot resolve keyword 'group'``. NO test
exercised the builder view or its save API, so the whole suite stayed green while
the admin page 500'd. These tests close that gap.

The eight fixed call sites:
  * page_builder/admin_views.py :: _build_rules_tree           (GET builder view)
  * page_builder/api_views.py   :: RuleGroupAPIView._build_group_data (GET detail/list)
  * page_builder/api_views.py   :: save_rule_group_structure   (update_or_create + remove)
  * page_builder/api_views.py   :: _update_group_rules         (child-group create/delete)
  * page_builder/api_views.py   :: VisibilityRuleAPIView.post  (append rule: Max + create)

Two follow-up bugs surfaced while writing these tests were then fixed in source,
and their coverage is now asserted as normal (all-green) behaviour:
  * ``RuleGroup`` gained a real ``priority`` field (visibility migration 0003).
    Before it, ``_build_rules_tree`` / ``_build_group_data`` reading
    ``group.priority`` and ``_save_nested_groups`` doing
    ``RuleGroup.objects.create(priority=...)`` 500'd the admin GET-edit view, the
    RuleGroup GET/POST/PUT API, and the HTTP child-group save path. Now asserted
    at 200 (``test_admin_builder_edit_returns_200_with_tree``,
    ``test_get_group_detail_returns_rules_in_order``,
    ``test_put_structure_creates_child_group``) plus a priority round-trip
    (``test_group_priority_round_trips_through_api``).
  * The append off-by-one -- ``aggregate(Max("order"))["max_order"] or -1``
    treated a legitimate max of 0 as falsy -- was replaced with an explicit None
    check, asserted by ``test_append_after_order_zero_does_not_collide``.
"""

import json

from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.test import Client, TestCase
from django.urls import reverse

from visibility.models import RuleGroup, RuleGroupMember, VisibilityRule

User = get_user_model()


def _rule(name, rule_type="geo_region", operator="equals", value=None):
    """Create a saved VisibilityRule with realistic field values."""
    return VisibilityRule.objects.create(
        name=name,
        rule_type=rule_type,
        operator=operator,
        value={"value": "NZ"} if value is None else value,
        is_active=True,
        priority=5,
    )


def _group(name="grp", logic="AND"):
    return RuleGroup.objects.create(name=name, logic_operator=logic, is_active=True)


def _member(group, rule, order):
    # The whole point of the fix: this FK keyword is `rule_group`, not `group`.
    return RuleGroupMember.objects.create(rule_group=group, rule=rule, order=order)


class RuleBuilderTestBase(TestCase):
    """Shared setup: seed the SiteSettings singleton (every client request runs
    the currency middleware, which resolves it) and a staff user."""

    def setUp(self):
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "admin_email": "admin@example.com",
                "default_currency": "USD",
                "enable_multi_warehouse": False,
            },
        )
        self.admin = User.objects.create_superuser("root", "root@example.com", "pw")
        self.client = Client()
        self.client.force_login(self.admin)

    def _json(self, method, url, payload):
        return getattr(self.client, method)(
            url, data=json.dumps(payload), content_type="application/json"
        )


# ---------------------------------------------------------------------------
# 1. Admin builder GET view  (page_builder_admin:rule_builder[_edit])
# ---------------------------------------------------------------------------
class AdminRuleBuilderViewTests(RuleBuilderTestBase):
    def setUp(self):
        super().setUp()
        self.parent = _group("parent")
        self.rule_a = _rule("A", "geo_region", value={"value": "NZ"})
        self.rule_b = _rule("B", "user_logged_in", operator="is_true", value={"value": True})
        _member(self.parent, self.rule_a, order=0)
        _member(self.parent, self.rule_b, order=1)
        # Nested child group -> exercises _build_rules_tree recursion.
        self.child = _group("child")
        self.child.parent_group = self.parent
        self.child.save()
        self.child_rule = _rule("C", "device_type", value={"value": "mobile"})
        _member(self.child, self.child_rule, order=0)

    def test_builder_new_view_renders(self):
        """GET the 'new' builder (no group_id) -> 200. Wiring / URL smoke; this
        path does not call _build_rules_tree so it is unaffected by the priority
        bug."""
        resp = self.client.get(reverse("page_builder_admin:rule_builder"))
        self.assertEqual(resp.status_code, 200)
        # Empty tree when creating from scratch.
        self.assertEqual(json.loads(resp.context["rules_tree_json"]), [])

    def test_admin_builder_edit_query_uses_rule_group_keyword(self):
        """The exact surface that 500'd for the user. Reverting _build_rules_tree
        to ``filter(group=...)`` reintroduces ``FieldError: Cannot resolve keyword
        'group'`` -- that query runs before the (separate, still-unfixed)
        ``group.priority`` read, so a revert is distinguishable and this test
        fails. Today the fixed query runs fine and execution reaches the priority
        read, which raises AttributeError -- tolerated here (see module docstring;
        pinned by test_admin_builder_edit_returns_200_when_priority_field_exists).
        """
        url = reverse("page_builder_admin:rule_builder_edit", kwargs={"group_id": self.parent.id})
        try:
            resp = self.client.get(url)
        except FieldError as exc:  # pragma: no cover - only on a regression
            self.fail(f"_build_rules_tree regressed to group= keyword: {exc}")
        except AttributeError as exc:
            # Known second bug: RuleGroup has no `priority` field. This means the
            # rule_group= membership query already succeeded.
            self.assertIn("priority", str(exc))
        else:
            # Only reachable once the priority field is restored.
            self.assertEqual(resp.status_code, 200)

    def test_popup_builder_edit_query_uses_rule_group_keyword(self):
        """rule_builder_popup_view shares _build_rules_tree; same guarantee."""
        url = reverse(
            "page_builder_admin:rule_builder_popup_edit", kwargs={"group_id": self.parent.id}
        )
        try:
            resp = self.client.get(url)
        except FieldError as exc:  # pragma: no cover - only on a regression
            self.fail(f"_build_rules_tree (popup) regressed to group= keyword: {exc}")
        except AttributeError as exc:
            self.assertIn("priority", str(exc))
        else:
            self.assertEqual(resp.status_code, 200)

    def test_admin_builder_edit_returns_200_with_tree(self):
        """GET-edit surface (the one that originally 500'd) now returns 200 with
        the tree reflecting members in ``order`` and the nested child group.
        Guards both the ``rule_group=`` membership query and the ``group.priority``
        read (restored via visibility migration 0003)."""
        url = reverse("page_builder_admin:rule_builder_edit", kwargs={"group_id": self.parent.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        tree = json.loads(resp.context["rules_tree_json"])
        rule_children = [c for c in tree["children"] if c["type"] == "rule"]
        self.assertEqual([c["name"] for c in rule_children], ["A", "B"])
        self.assertEqual([c["order"] for c in rule_children], [0, 1])
        group_children = [c for c in tree["children"] if c["type"] == "group"]
        self.assertEqual([g["name"] for g in group_children], ["child"])

    def test_non_staff_denied(self):
        """Negative permission test: a non-staff user is redirected away from the
        builder (staff_member_required)."""
        plain = User.objects.create_user("plain", "p@example.com", "pw")
        self.client.force_login(plain)
        resp = self.client.get(reverse("page_builder_admin:rule_builder"))
        # staff_member_required redirects to the admin login.
        self.assertIn(resp.status_code, (301, 302))
        self.assertIn("login", resp["Location"])


# ---------------------------------------------------------------------------
# 2. Rule group save/structure API  (page_builder_api:rule_group_structure)
# ---------------------------------------------------------------------------
class SaveRuleGroupStructureTests(RuleBuilderTestBase):
    def setUp(self):
        super().setUp()
        self.group = _group("g")
        self.rule_a = _rule("A", "geo_region", value={"value": "NZ"})
        self.rule_b = _rule("B", "geo_country", value={"value": "US"})
        self.rule_c = _rule("C", "device_type", value={"value": "mobile"})

    def _structure_url(self, group_id):
        return reverse("page_builder_api:rule_group_structure", kwargs={"group_id": group_id})

    def test_put_structure_creates_members_with_rule_group_fk_and_order(self):
        """Round-trip: PUT a set of rules -> RuleGroupMember rows exist against the
        correct rule_group with sequential order. Guards
        ``update_or_create(rule_group=group, ...)``. A revert to ``group=`` raises
        FieldError inside the view -> caught -> 500, so this asserts 200 too."""
        resp = self._json(
            "put",
            self._structure_url(self.group.id),
            {"rules": [{"id": self.rule_a.id}, {"id": self.rule_b.id}]},
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertTrue(resp.json()["success"])

        members = list(RuleGroupMember.objects.filter(rule_group=self.group).order_by("order"))
        self.assertEqual([m.rule_id for m in members], [self.rule_a.id, self.rule_b.id])
        self.assertEqual([m.order for m in members], [0, 1])

    def test_put_structure_removes_dropped_members(self):
        """PUT a smaller set -> the dropped member is deleted. Guards
        ``filter(rule_group=group, rule_id__in=removed).delete()``."""
        # Seed two members.
        _member(self.group, self.rule_a, 0)
        _member(self.group, self.rule_b, 1)

        resp = self._json(
            "put",
            self._structure_url(self.group.id),
            {"rules": [{"id": self.rule_a.id}]},
        )
        self.assertEqual(resp.status_code, 200, resp.content)

        remaining = list(RuleGroupMember.objects.filter(rule_group=self.group))
        self.assertEqual([m.rule_id for m in remaining], [self.rule_a.id])
        self.assertFalse(
            RuleGroupMember.objects.filter(rule_group=self.group, rule=self.rule_b).exists()
        )

    def test_put_structure_reorders_existing_members(self):
        """Re-PUT with a new order -> update_or_create updates the order in place
        rather than duplicating (unique_together rule_group+rule)."""
        _member(self.group, self.rule_a, 0)
        _member(self.group, self.rule_b, 1)

        resp = self._json(
            "put",
            self._structure_url(self.group.id),
            {"rules": [{"id": self.rule_b.id}, {"id": self.rule_a.id}]},
        )
        self.assertEqual(resp.status_code, 200, resp.content)

        members = list(RuleGroupMember.objects.filter(rule_group=self.group).order_by("order"))
        self.assertEqual([m.rule_id for m in members], [self.rule_b.id, self.rule_a.id])
        self.assertEqual(RuleGroupMember.objects.filter(rule_group=self.group).count(), 2)

    def test_update_group_rules_helper_uses_rule_group_fk(self):
        """Direct unit test of ``_update_group_rules`` -- the child-group rule
        membership writer. It clears then recreates ``RuleGroupMember`` rows via
        ``rule_group=``; a revert to ``group=`` raises FieldError here. Exercised
        directly as a focused unit test of the helper, alongside the end-to-end
        HTTP coverage in test_put_structure_creates_child_group.
        """
        from page_builder.api_views import _update_group_rules

        child = RuleGroup.objects.create(name="child", parent_group=self.group)
        _member(child, self.rule_a, 0)  # pre-existing membership to be cleared

        _update_group_rules(child, [{"id": self.rule_b.id}, {"id": self.rule_c.id}])

        members = list(RuleGroupMember.objects.filter(rule_group=child).order_by("order"))
        self.assertEqual([m.rule_id for m in members], [self.rule_b.id, self.rule_c.id])
        self.assertEqual([m.order for m in members], [0, 1])
        # The previously-present rule_a membership was cleared.
        self.assertFalse(
            RuleGroupMember.objects.filter(rule_group=child, rule=self.rule_a).exists()
        )

    def test_put_structure_creates_child_group(self):
        """PUT with a new nested child group creates the child under the parent
        (via ``_save_nested_groups`` -> ``RuleGroup.objects.create(priority=...)``,
        now that ``RuleGroup`` has a ``priority`` field) and writes its rule
        membership with the correct ``rule_group`` FK."""
        resp = self._json(
            "put",
            self._structure_url(self.group.id),
            {
                "rules": [{"id": self.rule_a.id}],
                "child_groups": [{"name": "Nested", "rules": [{"id": self.rule_c.id}]}],
            },
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        child = RuleGroup.objects.get(parent_group=self.group, name="Nested")
        child_members = list(RuleGroupMember.objects.filter(rule_group=child))
        self.assertEqual([m.rule_id for m in child_members], [self.rule_c.id])
        # Parent membership persisted alongside the child.
        self.assertEqual(
            list(
                RuleGroupMember.objects.filter(rule_group=self.group).values_list(
                    "rule_id", flat=True
                )
            ),
            [self.rule_a.id],
        )

    def test_put_structure_non_staff_denied(self):
        """Negative permission test: non-staff gets 403 from staff_required_api."""
        _member(self.group, self.rule_a, 0)
        plain = User.objects.create_user("plain", "p@example.com", "pw")
        self.client.force_login(plain)
        resp = self._json("put", self._structure_url(self.group.id), {"rules": []})
        self.assertIn(resp.status_code, (401, 403))
        # State untouched.
        self.assertEqual(RuleGroupMember.objects.filter(rule_group=self.group).count(), 1)


# ---------------------------------------------------------------------------
# 3. Append-rule-to-group branch  (VisibilityRuleAPIView.post, name=rules)
# ---------------------------------------------------------------------------
class AppendRuleToGroupTests(RuleBuilderTestBase):
    def setUp(self):
        super().setUp()
        self.group = _group("g")
        self.existing = _rule("existing", "geo_region", value={"value": "NZ"})
        # Non-zero order so Max()+1 is exercised without tripping the falsy-zero
        # ``or -1`` bug (that bug is pinned separately below).
        _member(self.group, self.existing, order=3)

    def test_post_rule_with_group_id_appends_at_max_order_plus_one(self):
        """POST a new rule with ``group_id`` -> it is appended as a member at
        ``Max(order)+1``. Guards both the ``filter(rule_group=group).aggregate(Max)``
        and ``create(rule_group=group, ...)`` call sites. A revert to ``group=``
        raises FieldError inside the view -> caught -> 500, so asserting 200 +
        membership guards the fix."""
        resp = self._json(
            "post",
            reverse("page_builder_api:rules"),
            {
                "name": "appended",
                "rule_type": "geo_country",
                "operator": "equals",
                "value": {"value": "US"},
                "group_id": self.group.id,
            },
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        new_rule_id = resp.json()["rule"]["id"]

        member = RuleGroupMember.objects.get(rule_group=self.group, rule_id=new_rule_id)
        self.assertEqual(member.order, 4)  # existing was 3 -> Max(3)+1
        self.assertEqual(
            list(
                RuleGroupMember.objects.filter(rule_group=self.group)
                .order_by("order")
                .values_list("rule_id", flat=True)
            ),
            [self.existing.id, new_rule_id],
        )

    def test_post_rule_into_empty_group_gets_order_zero(self):
        """First append into an empty group -> ``Max`` is None, ``or -1`` gives -1,
        so order = 0."""
        empty = _group("empty")
        resp = self._json(
            "post",
            reverse("page_builder_api:rules"),
            {
                "name": "first",
                "rule_type": "geo_region",
                "operator": "equals",
                "value": {"value": "AU"},
                "group_id": empty.id,
            },
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        member = RuleGroupMember.objects.get(rule_group=empty)
        self.assertEqual(member.order, 0)

    def test_append_after_order_zero_does_not_collide(self):
        """Appending when the current highest ``order`` is exactly 0 lands the new
        member at order 1 (no collision). Guards the falsy-zero fix in
        ``VisibilityRuleAPIView.post`` (``next_order = 0 if max_order is None else
        max_order + 1`` replacing the old ``... or -1``)."""
        grp = _group("zero")
        first = _rule("first", "geo_region", value={"value": "NZ"})
        _member(grp, first, order=0)
        resp = self._json(
            "post",
            reverse("page_builder_api:rules"),
            {
                "name": "second",
                "rule_type": "geo_country",
                "operator": "equals",
                "value": {"value": "US"},
                "group_id": grp.id,
            },
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        new_id = resp.json()["rule"]["id"]
        member = RuleGroupMember.objects.get(rule_group=grp, rule_id=new_id)
        self.assertEqual(member.order, 1)


# ---------------------------------------------------------------------------
# 4. Rule group GET API  (page_builder_api:rule_group_detail)
# ---------------------------------------------------------------------------
class RuleGroupDetailApiTests(RuleBuilderTestBase):
    def setUp(self):
        super().setUp()
        self.group = _group("g")
        self.rule_a = _rule("A", "geo_region", value={"value": "NZ"})
        self.rule_b = _rule("B", "geo_country", value={"value": "US"})
        _member(self.group, self.rule_a, 0)
        _member(self.group, self.rule_b, 1)

    def test_get_group_detail_returns_rules_in_order(self):
        """RuleGroup GET-detail API returns 200 with the members walked (via
        ``filter(rule_group=group)`` in ``_build_group_data``) and returned in
        ``order``. Guards both the ``rule_group=`` membership query and the
        ``group.priority`` read (restored via visibility migration 0003)."""
        url = reverse("page_builder_api:rule_group_detail", kwargs={"group_id": self.group.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()["group"]
        self.assertEqual(payload["priority"], self.group.priority)
        rules = payload["rules"]
        self.assertEqual([r["id"] for r in rules], [self.rule_a.id, self.rule_b.id])
        self.assertEqual([r["order"] for r in rules], [0, 1])

    def test_get_group_detail_non_staff_denied(self):
        """Negative permission test for the GET-detail endpoint."""
        plain = User.objects.create_user("plain", "p@example.com", "pw")
        self.client.force_login(plain)
        url = reverse("page_builder_api:rule_group_detail", kwargs={"group_id": self.group.id})
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (401, 403))

    def test_group_priority_round_trips_through_api(self):
        """POST create with ``priority`` persists it; PUT updating ``priority``
        changes it. Exercises the newly-added ``RuleGroup.priority`` field end to
        end through ``RuleGroupAPIView`` (create + patch both echo it back via
        ``_build_group_data``)."""
        # POST create with an explicit priority.
        create = self._json(
            "post",
            reverse("page_builder_api:rule_groups"),
            {"name": "Priced", "logic_operator": "AND", "priority": 7},
        )
        self.assertEqual(create.status_code, 200, create.content)
        gid = create.json()["group"]["id"]
        self.assertEqual(create.json()["group"]["priority"], 7)
        self.assertEqual(RuleGroup.objects.get(id=gid).priority, 7)

        # PUT update the priority.
        update = self._json(
            "put",
            reverse("page_builder_api:rule_group_detail", kwargs={"group_id": gid}),
            {"priority": 9},
        )
        self.assertEqual(update.status_code, 200, update.content)
        self.assertEqual(update.json()["group"]["priority"], 9)
        self.assertEqual(RuleGroup.objects.get(id=gid).priority, 9)
