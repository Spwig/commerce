"""Behaviour tests for the admin builder view (Phase-1 visual builder).

``campaign_builder`` renders the builder shell at
``/<lang>/admin/campaigns/<uuid>/builder/`` (name
``email_marketing_admin:campaign_builder``). It is staff-only and gated on the
``marketing`` category at ``full``. The rendered shell carries the block palette
and the ``json_script`` data islands the builder JS reads.
"""

import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from email_marketing.models import Campaign, CampaignBlock

from .base import MarketingTestCase

User = get_user_model()


class CampaignBuilderViewBehaviourTests(MarketingTestCase):
    def setUp(self):
        super().setUp()
        self.campaign = Campaign.objects.create(site=self.site, name="View Campaign", subject="Hi")

    def _url(self, campaign_id=None):
        return reverse(
            "email_marketing_admin:campaign_builder",
            args=[campaign_id or self.campaign.id],
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

    def test_staff_with_role_gets_builder_shell(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)

        html = resp.content.decode()
        # The palette renders group labels and each block's palette button.
        self.assertIn("Content", html)
        self.assertIn("Media", html)
        self.assertIn('data-block-type="heading"', html)
        self.assertIn('data-block-type="image"', html)
        # The JS data island the builder reads its blocks from.
        self.assertIn('id="em-blocks-data"', html)

    def test_builder_serialises_existing_blocks_into_data_island(self):
        CampaignBlock.objects.create(
            campaign=self.campaign,
            block_type="heading",
            content={"text": "Existing content"},
            order=0,
        )
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        # json_script HTML-escapes, so the text lands inside em-blocks-data.
        self.assertIn("Existing content", resp.content.decode())

    def test_non_staff_is_redirected_to_login(self):
        self.client.force_login(self._non_staff())
        resp = self.client.get(self._url())
        # staff_member_required redirects non-staff to the admin login.
        self.assertIn(resp.status_code, (302, 403))
        if resp.status_code == 302:
            self.assertIn("login", resp.url)

    def test_bare_staff_without_role_is_forbidden(self):
        # Deny-by-default: is_staff alone does not grant admin access. The
        # platform's /admin/ access layer redirects such a user away (302 to a
        # non-builder page) before the marketing gate would raise its own 403 --
        # either way they never see the builder.
        self.client.force_login(self._bare_staff())
        resp = self.client.get(self._url())
        self.assertIn(resp.status_code, (302, 403))
        if resp.status_code == 200:
            self.fail("bare staff must not receive the builder shell")
        # Sanity: the block data island (only in the real builder) is absent.
        self.assertNotIn(b'id="em-blocks-data"', resp.content)

    def test_anonymous_is_redirected_to_login(self):
        resp = self.client.get(self._url())
        self.assertIn(resp.status_code, (302, 403))

    def test_unknown_campaign_returns_404_for_authorised_staff(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(self._url(uuid.uuid4()))
        self.assertEqual(resp.status_code, 404)


class DashboardViewTests(MarketingTestCase):
    """The Campaign Studio dashboard is staff + marketing gated and renders."""

    def _url(self):
        return reverse("email_marketing_admin:dashboard")

    def _staff_with_role(self):
        from staff_roles.models import StaffRole
        from staff_roles.services import invalidate_user_cache

        user = User.objects.create_user(
            username=f"mkt-{uuid.uuid4().hex[:8]}",
            email="mkt2@test.spwig.com",
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

    def _bare_staff(self):
        return User.objects.create_user(
            username=f"bare-{uuid.uuid4().hex[:8]}",
            email="bare2@test.spwig.com",
            password="pw",
            is_staff=True,
        )

    def test_marketing_staff_sees_the_dashboard(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Campaign Studio")
        self.assertContains(resp, "em-dash-data")  # chart data island present

    def test_bare_staff_without_marketing_role_is_forbidden(self):
        # Deny-by-default: the admin access layer redirects (302) or the marketing
        # gate raises (403) — either way, no dashboard.
        self.client.force_login(self._bare_staff())
        resp = self.client.get(self._url())
        self.assertIn(resp.status_code, (302, 403))
        self.assertNotEqual(resp.status_code, 200)


class CampaignWizardTests(MarketingTestCase):
    """The New-Campaign wizard renders, creates a draft, and opens the builder."""

    def _url(self):
        return reverse("email_marketing_admin:campaign_wizard")

    def _staff_with_role(self):
        from staff_roles.models import StaffRole
        from staff_roles.services import invalidate_user_cache

        user = User.objects.create_user(
            username=f"mkt-{uuid.uuid4().hex[:8]}",
            email="mkt3@test.spwig.com",
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

    def test_get_renders_the_wizard(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "em-wizard-form")
        self.assertContains(resp, "wizard-steps")

    def test_post_creates_a_draft_and_redirects_to_the_builder(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.post(
            self._url(),
            {
                "campaign_type": "recurring",
                "name": "My Wizard Campaign",
                "subject": "Hi there",
                "preview_text": "peek",
                "message_type": "newsletter",
                "segment": "",
            },
        )
        campaign = Campaign.objects.get(name="My Wizard Campaign")
        self.assertEqual(campaign.campaign_type, Campaign.TYPE_RECURRING)
        self.assertEqual(campaign.status, Campaign.STATUS_DRAFT)
        self.assertEqual(campaign.subject, "Hi there")
        self.assertEqual(resp.status_code, 302)
        self.assertIn(str(campaign.id), resp.url)
        self.assertIn("builder", resp.url)

    def test_admin_add_redirects_to_the_wizard(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(reverse("admin:email_marketing_campaign_add"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("wizard", resp.url)


class ChangelistFilterTests(MarketingTestCase):
    """The AJAX card-filter endpoints back the modernized changelists."""

    def _staff_with_role(self):
        from staff_roles.models import StaffRole
        from staff_roles.services import invalidate_user_cache

        user = User.objects.create_user(
            username=f"mkt-{uuid.uuid4().hex[:8]}",
            email="mkt4@test.spwig.com",
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

    def test_campaign_filter_returns_cards_and_count_for_ajax(self):
        Campaign.objects.create(site=self.site, name="Findable Campaign", subject="Hi")
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(
            reverse("email_marketing_admin:filter_campaigns") + "?search=Findable",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertIn("Findable Campaign", data["html"])
        self.assertIn("list-row-card", data["html"])

    def test_campaign_filter_rejects_non_ajax(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(reverse("email_marketing_admin:filter_campaigns"))
        self.assertEqual(resp.status_code, 400)

    def test_subscriber_filter_search_narrows_results(self):
        self.make_subscriber("keep@example.com")
        self.make_subscriber("other@example.com")
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(
            reverse("email_marketing_admin:filter_subscribers") + "?search=keep",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.json()["count"], 1)
        self.assertIn("keep@example.com", resp.json()["html"])

    def test_changelist_page_uses_the_card_template(self):
        self.client.force_login(self._staff_with_role())
        resp = self.client.get(reverse("admin:email_marketing_campaign_changelist"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "list-filter-config")
        self.assertContains(resp, "filters-panel")
