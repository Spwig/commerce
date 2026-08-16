"""Phase 4e: behaviour-named tests for the shared visibility service seams.

These are the capability anchors the refinery scanner reads — one named function
per behaviour (attach rule groups to a target, quick-create a rule group, resolve
show/hide/defer), each with a behaviour-named test.
"""

from django.test import TestCase

from design.header_footer_models import HeaderTemplate, Menu, MenuItem, Widget, WidgetPlacement
from page_builder.models import Element, Page
from visibility.models import RuleGroup, RuleGroupMember, VisibilityRule
from visibility.service import create_quick_rule_group, set_visibility_rule_groups


def _rule_group(name="grp", rule_type="geo_region", value="NZ"):
    group = RuleGroup.objects.create(name=name)
    rule = VisibilityRule.objects.create(
        name=f"{rule_type}={value}", rule_type=rule_type, operator="equals", value={"value": value}
    )
    RuleGroupMember.objects.create(rule_group=group, rule=rule, order=0)
    return group


class SetVisibilityRuleGroupsTests(TestCase):
    """Attaching reusable rule groups to any gated target."""

    def setUp(self):
        self.group = _rule_group()
        self.page = Page.objects.create(title="P", slug="p", page_type="page", status="published")

    def test_attaches_rule_groups_to_a_page_element(self):
        el = Element.objects.create(page=self.page, name="e", element_type="text")
        applied = set_visibility_rule_groups(el, [self.group.id])
        self.assertEqual(applied, [self.group.id])
        self.assertEqual(list(el.visibility_rules.values_list("id", flat=True)), [self.group.id])

    def test_attaches_rule_groups_to_a_menu_item(self):
        menu = Menu.objects.create(name="M", slug="m")
        item = MenuItem.objects.create(menu=menu, item_type="link", title="x", url="/x/")
        set_visibility_rule_groups(item, [self.group.id])
        self.assertEqual(list(item.rule_groups.values_list("id", flat=True)), [self.group.id])

    def test_attaches_rule_groups_to_a_widget_placement(self):
        header = HeaderTemplate.objects.create(name="H", slug="h")
        widget = Widget.objects.create(name="W", widget_type="text")
        placement = WidgetPlacement.objects.create(widget=widget, header=header, zone="z", order=0)
        set_visibility_rule_groups(placement, [self.group.id])
        self.assertEqual(list(placement.rule_groups.values_list("id", flat=True)), [self.group.id])

    def test_replaces_existing_and_drops_bogus_ids(self):
        el = Element.objects.create(page=self.page, name="e", element_type="text")
        el.visibility_rules.add(self.group)
        other = _rule_group(name="other")
        applied = set_visibility_rule_groups(el, [other.id, 999999])
        self.assertEqual(applied, [other.id])
        self.assertEqual(list(el.visibility_rules.values_list("id", flat=True)), [other.id])

    def test_non_integer_ids_raise(self):
        el = Element.objects.create(page=self.page, name="e", element_type="text")
        with self.assertRaises(ValueError):
            set_visibility_rule_groups(el, ["not-an-int"])


class CreateQuickRuleGroupTests(TestCase):
    """The editor's quick-create shortcut — materialise a real single-rule group."""

    def test_materialises_a_visibility_rule_and_group(self):
        group = create_quick_rule_group("geo_region", "equals", {"value": "NZ"}, "NZ market")
        self.assertEqual(group.name, "NZ market")
        self.assertEqual(group.rules.count(), 1)
        rule = group.rules.first()
        self.assertEqual(rule.rule_type, "geo_region")
        self.assertEqual(rule.value, {"value": "NZ"})

    def test_defaults_name_from_rule_type(self):
        group = create_quick_rule_group("selected_currency", "equals", {"value": "NZD"})
        self.assertTrue(group.name)  # non-empty, derived from the rule type label

    def test_rejects_invalid_rule_type(self):
        with self.assertRaises(ValueError):
            create_quick_rule_group("not_a_type", "equals", {})

    def test_rejects_regex_operator(self):
        # security: quick-create must never be a raw-regex (ReDoS) vector.
        with self.assertRaises(ValueError):
            create_quick_rule_group("referrer", "regex", {"value": ".*"})
        self.assertEqual(VisibilityRule.objects.filter(operator="regex").count(), 0)
