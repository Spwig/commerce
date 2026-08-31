"""Subscriber tags: the model, the has_tag segment rule, and the bulk actions."""

import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse

from email_marketing.models import Segment, SubscriberTag
from email_marketing.services.segmentation import available_rule_fields, resolve_segment

from .base import MarketingTestCase

User = get_user_model()


class SubscriberTagModelTests(MarketingTestCase):
    def test_slug_is_generated_from_name(self):
        tag = SubscriberTag.objects.create(site=self.site, name="VIP Customers")
        self.assertEqual(tag.slug, "vip-customers")

    def test_slug_is_unique_per_site(self):
        SubscriberTag.objects.create(site=self.site, name="VIP", slug="vip")
        from django.db import IntegrityError, transaction

        with self.assertRaises(IntegrityError), transaction.atomic():
            SubscriberTag.objects.create(site=self.site, name="VIP 2", slug="vip")


class HasTagRuleTests(MarketingTestCase):
    def _tag(self, name, slug):
        return SubscriberTag.objects.create(site=self.site, name=name, slug=slug)

    def _dynamic_segment(self, conditions, match="all"):
        return Segment.objects.create(
            site=self.site,
            name="Tagged",
            slug=f"tagged-{uuid.uuid4().hex[:6]}",
            kind=Segment.KIND_DYNAMIC,
            rules={"match": match, "conditions": conditions},
        )

    def test_available_rule_fields_omits_has_tag_when_no_tags(self):
        keys = {f["key"] for f in available_rule_fields()}
        self.assertNotIn("has_tag", keys)

    def test_available_rule_fields_includes_has_tag_with_options(self):
        self._tag("VIP", "vip")
        field = next(f for f in available_rule_fields() if f["key"] == "has_tag")
        self.assertEqual(field["type"], "select")
        self.assertIn({"value": "vip", "label": "VIP"}, field["options"])

    def test_has_tag_eq_matches_only_tagged_subscribers(self):
        vip = self._tag("VIP", "vip")
        tagged = self.make_anon_emailable("in@example.com")
        tagged.tags.add(vip)
        self.make_anon_emailable("out@example.com")  # untagged

        seg = self._dynamic_segment([{"field": "has_tag", "op": "eq", "value": "vip"}])
        emails = set(resolve_segment(seg).values_list("email", flat=True))
        self.assertEqual(emails, {"in@example.com"})

    def test_has_tag_in_matches_any_of(self):
        vip = self._tag("VIP", "vip")
        whale = self._tag("Whale", "whale")
        a = self.make_anon_emailable("a@example.com")
        a.tags.add(vip)
        b = self.make_anon_emailable("b@example.com")
        b.tags.add(whale)
        self.make_anon_emailable("c@example.com")

        seg = self._dynamic_segment([{"field": "has_tag", "op": "in", "value": ["vip", "whale"]}])
        emails = set(resolve_segment(seg).values_list("email", flat=True))
        self.assertEqual(emails, {"a@example.com", "b@example.com"})

    def test_has_tag_result_is_deduped(self):
        # A subscriber with two of the matched tags must appear once.
        vip = self._tag("VIP", "vip")
        whale = self._tag("Whale", "whale")
        sub = self.make_anon_emailable("multi@example.com")
        sub.tags.add(vip, whale)
        seg = self._dynamic_segment([{"field": "has_tag", "op": "in", "value": ["vip", "whale"]}])
        self.assertEqual(resolve_segment(seg).count(), 1)


class TagBulkActionTests(MarketingTestCase):
    def setUp(self):
        super().setUp()
        self.admin = User.objects.create_superuser(
            username="root", email="root@test.spwig.com", password="pw"
        )
        self.client.force_login(self.admin)
        self.tag = SubscriberTag.objects.create(site=self.site, name="VIP", slug="vip")
        self.s1 = self.make_subscriber("s1@example.com")
        self.s2 = self.make_subscriber("s2@example.com")

    def _changelist(self):
        return reverse("admin:email_marketing_subscriber_changelist")

    def test_add_tag_action_tags_selected(self):
        resp = self.client.post(
            self._changelist(),
            {
                "action": "add_tag_action",
                "_selected_action": [str(self.s1.pk), str(self.s2.pk)],
                "apply_tag": "1",
                "tag": str(self.tag.pk),
            },
        )
        self.assertEqual(resp.status_code, 302)  # back to the changelist
        self.assertIn(self.tag, self.s1.tags.all())
        self.assertIn(self.tag, self.s2.tags.all())

    def test_remove_tag_action_untags_selected(self):
        self.s1.tags.add(self.tag)
        resp = self.client.post(
            self._changelist(),
            {
                "action": "remove_tag_action",
                "_selected_action": [str(self.s1.pk)],
                "apply_tag": "1",
                "tag": str(self.tag.pk),
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn(self.tag, self.s1.tags.all())

    def test_action_without_apply_renders_the_picker(self):
        resp = self.client.post(
            self._changelist(),
            {
                "action": "add_tag_action",
                "_selected_action": [str(self.s1.pk)],
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'name="tag"')
