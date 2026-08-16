"""Phase 4a: the neutral visibility API that the shared editor uses to attach
RuleGroups to page elements and nav objects.

Covers the persistence seam and, importantly, the permission gate — being staff
is not enough; the caller must hold the target model's change permission.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from design.header_footer_models import HeaderTemplate, Menu, MenuItem, Widget, WidgetPlacement
from page_builder.models import Element, Page
from visibility.models import RuleGroup, RuleGroupMember, VisibilityRule

User = get_user_model()


def _rule_group(name="grp", rule_type="geo_region", value="NZ"):
    group = RuleGroup.objects.create(name=name)
    rule = VisibilityRule.objects.create(
        name=f"{rule_type}={value}", rule_type=rule_type, operator="equals", value={"value": value}
    )
    RuleGroupMember.objects.create(rule_group=group, rule=rule, order=0)
    return group


class VisibilityAttachApiTests(TestCase):
    def setUp(self):
        # Requests run the full middleware stack, which resolves the SiteSettings
        # singleton — seed it so those lookups don't 500.
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "admin_email": "admin@example.com",
                "default_currency": "USD",
                "enable_multi_warehouse": False,
            },
        )
        self.client = APIClient()
        self.superuser = User.objects.create_superuser("root", "root@example.com", "pw")
        self.group = _rule_group()
        self.page = Page.objects.create(title="P", slug="p", page_type="page", status="published")
        self.element = Element.objects.create(page=self.page, name="e", element_type="text")

    # --- options list -----------------------------------------------------
    def test_options_lists_active_groups(self):
        self.client.force_authenticate(self.superuser)
        resp = self.client.get(reverse("visibility_api:rule_groups"))
        self.assertEqual(resp.status_code, 200)
        ids = [g["id"] for g in resp.json()["rule_groups"]]
        self.assertIn(self.group.id, ids)

    # --- attach / read ----------------------------------------------------
    def test_attach_sets_element_m2m_and_get_reads_it(self):
        self.client.force_authenticate(self.superuser)
        url = reverse("visibility_api:attach")
        resp = self.client.post(
            url,
            {
                "target_type": "element",
                "target_id": self.element.id,
                "rule_group_ids": [self.group.id],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(self.element.visibility_rules.values_list("id", flat=True)), [self.group.id]
        )
        # GET reflects it
        read = self.client.get(url, {"target_type": "element", "target_id": self.element.id})
        self.assertEqual(read.json()["rule_group_ids"], [self.group.id])

    def test_attach_menuitem_and_widgetplacement(self):
        self.client.force_authenticate(self.superuser)
        menu = Menu.objects.create(name="M", slug="m")
        item = MenuItem.objects.create(menu=menu, item_type="link", title="x", url="/x/")
        header = HeaderTemplate.objects.create(name="H", slug="h")
        widget = Widget.objects.create(name="W", widget_type="text")
        placement = WidgetPlacement.objects.create(widget=widget, header=header, zone="z", order=0)
        url = reverse("visibility_api:attach")
        for ttype, obj, mgr in (
            ("menuitem", item, item.rule_groups),
            ("widgetplacement", placement, placement.rule_groups),
        ):
            resp = self.client.post(
                url,
                {"target_type": ttype, "target_id": obj.id, "rule_group_ids": [self.group.id]},
                format="json",
            )
            self.assertEqual(resp.status_code, 200, ttype)
            self.assertEqual(list(mgr.values_list("id", flat=True)), [self.group.id])

    def test_attach_replaces_and_filters_bogus_ids(self):
        self.client.force_authenticate(self.superuser)
        self.element.visibility_rules.add(self.group)
        other = _rule_group(name="other")
        resp = self.client.post(
            reverse("visibility_api:attach"),
            {
                "target_type": "element",
                "target_id": self.element.id,
                # bogus id 999999 must be dropped; full replace swaps group->other
                "rule_group_ids": [other.id, 999999],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["rule_group_ids"], [other.id])
        self.assertEqual(
            list(self.element.visibility_rules.values_list("id", flat=True)), [other.id]
        )

    def test_unknown_target_type_400(self):
        self.client.force_authenticate(self.superuser)
        resp = self.client.post(
            reverse("visibility_api:attach"),
            {"target_type": "bogus", "target_id": 1, "rule_group_ids": []},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    # --- permission gate --------------------------------------------------
    def test_non_staff_rejected(self):
        plain = User.objects.create_user("plain", "p@example.com", "pw")
        self.client.force_authenticate(plain)
        resp = self.client.post(
            reverse("visibility_api:attach"),
            {"target_type": "element", "target_id": self.element.id, "rule_group_ids": []},
            format="json",
        )
        self.assertIn(resp.status_code, (401, 403))

    def test_staff_without_change_perm_forbidden(self):
        # is_staff alone must NOT be enough — the per-target change permission is
        # the real gate (CLAUDE.md).
        staff = User.objects.create_user("staff", "s@example.com", "pw", is_staff=True)
        self.client.force_authenticate(staff)
        resp = self.client.post(
            reverse("visibility_api:attach"),
            {
                "target_type": "element",
                "target_id": self.element.id,
                "rule_group_ids": [self.group.id],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(self.element.visibility_rules.count(), 0)

    def test_staff_with_change_perm_allowed(self):
        staff = User.objects.create_user("staff2", "s2@example.com", "pw", is_staff=True)
        staff.user_permissions.add(Permission.objects.get(codename="change_element"))
        self.client.force_authenticate(staff)
        resp = self.client.post(
            reverse("visibility_api:attach"),
            {
                "target_type": "element",
                "target_id": self.element.id,
                "rule_group_ids": [self.group.id],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200)

    # --- quick create -----------------------------------------------------
    def test_quick_rule_creates_group_and_rule(self):
        self.client.force_authenticate(self.superuser)
        resp = self.client.post(
            reverse("visibility_api:quick_rule"),
            {
                "rule_type": "geo_region",
                "operator": "equals",
                "value": {"value": "NZ"},
                "name": "NZ",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        gid = resp.json()["rule_group"]["id"]
        group = RuleGroup.objects.get(id=gid)
        self.assertEqual(group.rules.count(), 1)
        self.assertEqual(group.rules.first().rule_type, "geo_region")

    def test_quick_rule_rejects_invalid_type(self):
        self.client.force_authenticate(self.superuser)
        resp = self.client.post(
            reverse("visibility_api:quick_rule"),
            {"rule_type": "not_a_type", "value": {}},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_quick_rule_rejects_regex_operator(self):
        # Security: quick-create must not be a raw-regex (ReDoS) vector.
        self.client.force_authenticate(self.superuser)
        resp = self.client.post(
            reverse("visibility_api:quick_rule"),
            {"rule_type": "referrer", "operator": "regex", "value": {"value": ".*"}},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(VisibilityRule.objects.filter(operator="regex").count(), 0)

    def test_attach_rejects_oversized_list(self):
        self.client.force_authenticate(self.superuser)
        resp = self.client.post(
            reverse("visibility_api:attach"),
            {
                "target_type": "element",
                "target_id": self.element.id,
                "rule_group_ids": list(range(1, 202)),
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
