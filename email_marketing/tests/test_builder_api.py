"""Behaviour tests for the builder API (Phase-1 visual builder).

Endpoints (all under ``/api/email-marketing/``, non-i18n) are staff-only, gated on
the ``marketing`` category at ``full`` level, and CSRF-enforced. They edit
``CampaignBlock`` rows and serialise them to the campaign's MJML on save.

CSRF: the Django test ``Client`` bypasses CSRF by default, so the happy-path
tests exercise the view logic. A separate test proves the endpoints are NOT
``@csrf_exempt`` (they rely on ``CsrfViewMiddleware``), and one runtime test
drives an enforcing client to confirm a token-less POST is rejected.
"""

import json
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client
from django.urls import reverse

from email_marketing import api_views
from email_marketing.models import Campaign, CampaignBlock

from .base import MarketingTestCase

User = get_user_model()


def grant_marketing_full(user):
    """Give ``user`` a StaffRole granting marketing:full (mirrors admin tests)."""
    from staff_roles.models import StaffRole
    from staff_roles.services import invalidate_user_cache

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


class BuilderApiTestBase(MarketingTestCase):
    def setUp(self):
        super().setUp()
        self.campaign = Campaign.objects.create(site=self.site, name="API Campaign", subject="Hi")

    # --- user builders ------------------------------------------------------

    def _staff_with_role(self):
        user = User.objects.create_user(
            username=f"mkt-{uuid.uuid4().hex[:8]}",
            email="mkt@test.spwig.com",
            password="pw",
            is_staff=True,
        )
        return grant_marketing_full(user)

    def _bare_staff(self):
        return User.objects.create_user(
            username=f"bare-{uuid.uuid4().hex[:8]}",
            email="bare@test.spwig.com",
            password="pw",
            is_staff=True,
        )

    def _non_staff(self):
        return User.objects.create_user(
            username=f"cust-{uuid.uuid4().hex[:8]}",
            email="cust@test.spwig.com",
            password="pw",
            is_staff=False,
        )

    def _post_json(self, url, payload, client=None):
        client = client or self.client
        return client.post(url, data=json.dumps(payload), content_type="application/json")


class VoucherSearchBehaviourTests(BuilderApiTestBase):
    """The Discount Code block's voucher picker data source."""

    def _make_voucher(self, code, **kwargs):
        from vouchers.models import VoucherCode

        defaults = {
            "name": f"{code} promo",
            "discount_type": "percentage",
            "discount_value": 20,
            "is_active": True,
        }
        defaults.update(kwargs)
        return VoucherCode.objects.create(code=code, **defaults)

    def _url(self):
        return reverse("email_marketing_api:voucher_search")

    def test_staff_with_marketing_role_gets_active_vouchers_with_summary(self):
        self._make_voucher("SAVE20")
        self.client.force_login(self._staff_with_role())

        resp = self.client.get(self._url(), HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(resp.status_code, 200)
        vouchers = resp.json()["vouchers"]
        by_code = {v["code"]: v for v in vouchers}
        self.assertIn("SAVE20", by_code)
        self.assertEqual(by_code["SAVE20"]["summary"], "20% off")

    def test_search_filters_by_code(self):
        self._make_voucher("SUMMER")
        self._make_voucher("WINTER")
        self.client.force_login(self._staff_with_role())

        resp = self.client.get(self._url() + "?search=summ", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        codes = {v["code"] for v in resp.json()["vouchers"]}
        self.assertEqual(codes, {"SUMMER"})

    def test_inactive_vouchers_are_excluded(self):
        self._make_voucher("OLD", is_active=False)
        self.client.force_login(self._staff_with_role())

        resp = self.client.get(self._url(), HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        codes = {v["code"] for v in resp.json()["vouchers"]}
        self.assertNotIn("OLD", codes)

    def test_bare_staff_without_marketing_role_is_denied(self):
        self.client.force_login(self._bare_staff())
        resp = self.client.get(self._url(), HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(resp.status_code, 403)


class CreateBlockAuthBehaviourTests(BuilderApiTestBase):
    def _url(self):
        return reverse("email_marketing_api:create_block")

    def test_anonymous_is_denied_and_creates_no_block(self):
        resp = self._post_json(
            self._url(), {"campaign_id": str(self.campaign.id), "block_type": "heading"}
        )
        # staff_member_required redirects unauthenticated callers to admin login.
        self.assertIn(resp.status_code, (302, 403))
        self.assertEqual(self.campaign.blocks.count(), 0)

    def test_non_staff_user_is_denied_and_creates_no_block(self):
        self.client.force_login(self._non_staff())
        resp = self._post_json(
            self._url(), {"campaign_id": str(self.campaign.id), "block_type": "heading"}
        )
        # staff_member_required rejects non-staff (redirect to login).
        self.assertIn(resp.status_code, (302, 403))
        self.assertEqual(self.campaign.blocks.count(), 0)

    def test_bare_staff_without_role_gets_json_403(self):
        # Deny-by-default: is_staff alone is not enough; the marketing gate returns
        # a JSON 403 (ajax=True) rather than a redirect.
        self.client.force_login(self._bare_staff())
        resp = self._post_json(
            self._url(), {"campaign_id": str(self.campaign.id), "block_type": "heading"}
        )
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(self.campaign.blocks.count(), 0)

    def test_staff_with_marketing_role_creates_block_with_defaults(self):
        self.client.force_login(self._staff_with_role())
        resp = self._post_json(
            self._url(), {"campaign_id": str(self.campaign.id), "block_type": "heading"}
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertTrue(body["success"])

        self.assertEqual(self.campaign.blocks.count(), 1)
        block = self.campaign.blocks.get()
        self.assertEqual(block.block_type, "heading")
        self.assertEqual(block.order, 1)
        # Fresh block seeded with the registry's declared defaults.
        self.assertEqual(block.content["text"], "Your heading")
        self.assertEqual(block.content["level"], "h2")

    def test_staff_creating_unknown_block_type_gets_400(self):
        self.client.force_login(self._staff_with_role())
        resp = self._post_json(
            self._url(),
            {"campaign_id": str(self.campaign.id), "block_type": "nope"},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(self.campaign.blocks.count(), 0)


class UpdateBlockBehaviourTests(BuilderApiTestBase):
    def _block(self):
        return CampaignBlock.objects.create(
            campaign=self.campaign,
            block_type="heading",
            content={"text": "Original", "level": "h2", "align": "left", "color": ""},
            order=0,
        )

    def test_update_persists_known_prop_and_drops_unknown_key(self):
        block = self._block()
        self.client.force_login(self._staff_with_role())
        url = reverse("email_marketing_api:update_block", args=[block.id])

        resp = self._post_json(url, {"content": {"evil": "x", "text": "Hi"}})

        self.assertEqual(resp.status_code, 200)
        block.refresh_from_db()
        # Known prop written...
        self.assertEqual(block.content["text"], "Hi")
        # ...unknown prop rejected (mass-assignment guard).
        self.assertNotIn("evil", block.content)

    def test_update_rejects_non_object_content(self):
        block = self._block()
        self.client.force_login(self._staff_with_role())
        url = reverse("email_marketing_api:update_block", args=[block.id])

        resp = self._post_json(url, {"content": "not-a-dict"})
        self.assertEqual(resp.status_code, 400)
        block.refresh_from_db()
        self.assertEqual(block.content["text"], "Original")

    def test_update_denied_for_bare_staff(self):
        block = self._block()
        self.client.force_login(self._bare_staff())
        url = reverse("email_marketing_api:update_block", args=[block.id])

        resp = self._post_json(url, {"content": {"text": "Hacked"}})
        self.assertEqual(resp.status_code, 403)
        block.refresh_from_db()
        self.assertEqual(block.content["text"], "Original")


class DeleteBlockBehaviourTests(BuilderApiTestBase):
    def test_staff_can_delete_block(self):
        block = CampaignBlock.objects.create(
            campaign=self.campaign, block_type="text", content={"text": "x"}, order=0
        )
        self.client.force_login(self._staff_with_role())
        url = reverse("email_marketing_api:delete_block", args=[block.id])

        resp = self._post_json(url, {})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["success"])
        self.assertFalse(CampaignBlock.objects.filter(id=block.id).exists())

    def test_delete_denied_for_bare_staff_keeps_block(self):
        block = CampaignBlock.objects.create(
            campaign=self.campaign, block_type="text", content={"text": "x"}, order=0
        )
        self.client.force_login(self._bare_staff())
        url = reverse("email_marketing_api:delete_block", args=[block.id])

        resp = self._post_json(url, {})
        self.assertEqual(resp.status_code, 403)
        self.assertTrue(CampaignBlock.objects.filter(id=block.id).exists())


class ReorderBlocksBehaviourTests(BuilderApiTestBase):
    def test_reorder_applies_posted_id_order(self):
        a = CampaignBlock.objects.create(
            campaign=self.campaign, block_type="heading", content={"text": "A"}, order=0
        )
        b = CampaignBlock.objects.create(
            campaign=self.campaign, block_type="heading", content={"text": "B"}, order=1
        )
        c = CampaignBlock.objects.create(
            campaign=self.campaign, block_type="heading", content={"text": "C"}, order=2
        )
        self.client.force_login(self._staff_with_role())
        url = reverse("email_marketing_api:reorder_blocks")

        # Reverse the order: c, b, a.
        resp = self._post_json(
            url,
            {"campaign_id": str(self.campaign.id), "order": [str(c.id), str(b.id), str(a.id)]},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["success"])

        a.refresh_from_db()
        b.refresh_from_db()
        c.refresh_from_db()
        self.assertEqual(c.order, 0)
        self.assertEqual(b.order, 1)
        self.assertEqual(a.order, 2)
        # And the serialised order now reflects the new sequence.
        self.assertEqual(
            list(self.campaign.blocks.values_list("content", flat=True)),
            [{"text": "C"}, {"text": "B"}, {"text": "A"}],
        )

    def test_reorder_rejects_non_list_order(self):
        self.client.force_login(self._staff_with_role())
        url = reverse("email_marketing_api:reorder_blocks")
        resp = self._post_json(url, {"campaign_id": str(self.campaign.id), "order": "nope"})
        self.assertEqual(resp.status_code, 400)


class SaveCampaignBehaviourTests(BuilderApiTestBase):
    def test_save_writes_html_content_and_reports_success(self):
        CampaignBlock.objects.create(
            campaign=self.campaign,
            block_type="heading",
            content={"text": "Saved via API"},
            order=0,
        )
        self.client.force_login(self._staff_with_role())
        url = reverse("email_marketing_api:save_campaign", args=[self.campaign.id])

        resp = self._post_json(url, {})
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertTrue(body["success"])
        self.assertGreater(body["mjml_length"], 0)

        self.campaign.refresh_from_db()
        self.assertIn("Saved via API", self.campaign.html_content)
        self.assertTrue(self.campaign.html_content.startswith("<mjml>"))

    def test_save_denied_for_bare_staff(self):
        self.client.force_login(self._bare_staff())
        url = reverse("email_marketing_api:save_campaign", args=[self.campaign.id])
        resp = self._post_json(url, {})
        self.assertEqual(resp.status_code, 403)


class CsrfBehaviourTests(BuilderApiTestBase):
    def test_builder_endpoints_are_not_csrf_exempt(self):
        # These views rely on CsrfViewMiddleware; none may opt out via
        # @csrf_exempt (which would set csrf_exempt=True on the callable).
        for view in (
            api_views.create_block,
            api_views.update_block,
            api_views.delete_block,
            api_views.reorder_blocks,
            api_views.save_campaign,
        ):
            self.assertFalse(
                getattr(view, "csrf_exempt", False),
                f"{view.__name__} must not be @csrf_exempt",
            )

    def test_token_less_post_is_rejected_by_csrf_middleware(self):
        # An enforcing client with an authorised staff user, but no CSRF token,
        # must be rejected by the middleware before the view logic runs.
        enforcing = Client(enforce_csrf_checks=True)
        enforcing.force_login(self._staff_with_role())
        resp = enforcing.post(
            reverse("email_marketing_api:create_block"),
            data=json.dumps({"campaign_id": str(self.campaign.id), "block_type": "heading"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(self.campaign.blocks.count(), 0)


class PreviewBehaviourTests(BuilderApiTestBase):
    def _url(self):
        return reverse("email_marketing_api:preview_campaign", args=[self.campaign.id])

    def test_preview_returns_compiled_email_with_sample_merge(self):
        CampaignBlock.objects.create(
            campaign=self.campaign,
            block_type="heading",
            content={"text": "Hi [[first_name]]", "level": "h1"},
            order=0,
        )
        self.client.force_login(self._staff_with_role())

        resp = self.client.get(self._url())

        self.assertEqual(resp.status_code, 200)
        html = resp.json()["html"]
        self.assertIn("<table", html.lower())  # compiled email-safe HTML
        self.assertIn("Alex", html)  # merge field shown as sample
        self.assertNotIn("[[first_name]]", html)  # token substituted

    def test_preview_denied_for_non_staff(self):
        self.client.force_login(self._non_staff())
        resp = self.client.get(self._url())
        self.assertIn(resp.status_code, (302, 403))


class SegmentCountBehaviourTests(BuilderApiTestBase):
    def _url(self):
        return reverse("email_marketing_api:preview_segment_count")

    def _sub(self, email):
        from email_marketing.models import Subscriber

        return Subscriber.objects.create(site=self.site, email=email)

    def test_count_matches_active_subscribers_for_empty_rules(self):
        self._sub("a@example.com")
        self._sub("b@example.com")
        self.client.force_login(self._staff_with_role())

        resp = self._post_json(self._url(), {"rules": {"match": "all", "conditions": []}})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 2)

    def test_non_dict_rules_returns_400(self):
        self.client.force_login(self._staff_with_role())
        resp = self._post_json(self._url(), {"rules": "nope"})
        self.assertEqual(resp.status_code, 400)

    def test_count_denied_for_non_staff(self):
        self.client.force_login(self._non_staff())
        resp = self._post_json(self._url(), {"rules": {"conditions": []}})
        self.assertIn(resp.status_code, (302, 403))
