"""
View Tests

Tests for referral program admin views and AJAX endpoints.
"""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .factories import (
    create_referral_attribution,
    create_referral_identity,
    create_referral_program,
    create_referral_reward,
    create_user,
)

User = get_user_model()


@override_settings(LANGUAGE_CODE="en")
class ReferralDashboardViewTest(TestCase):
    """Tests for referral dashboard view."""

    def setUp(self):
        self.program = create_referral_program()
        self.admin = create_user(email="admin@example.com", is_staff=True)
        self.client = Client()
        self.client.force_login(self.admin)

    def test_dashboard_requires_staff(self):
        """Test that dashboard requires staff access."""
        # Create regular user
        user = create_user(email="user@example.com", is_staff=False)
        client = Client()
        client.force_login(user)

        # Try to access dashboard
        response = client.get(reverse("referrals:dashboard"))

        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_successfully(self):
        """Test that dashboard loads successfully for staff."""
        response = self.client.get(reverse("referrals:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("program", response.context)
        self.assertIn("total_referrals", response.context)
        self.assertIn("pending_approvals", response.context)

    def test_dashboard_displays_kpis(self):
        """Test that dashboard displays correct KPIs."""
        # Create test data
        referrer = create_user(email="referrer@example.com")
        referee = create_user(email="referee@example.com")
        referee2 = create_user(email="referee2@example.com")
        identity = create_referral_identity(customer=referrer)

        # Create attributions (use same program)
        create_referral_attribution(
            program=self.program,
            referrer_identity=identity,
            referee_customer=referee,
            status="approved",
        )
        create_referral_attribution(
            program=self.program,
            referrer_identity=identity,
            referee_customer=referee2,
            status="pending",
        )

        response = self.client.get(reverse("referrals:dashboard"))

        # Check KPIs
        self.assertEqual(response.context["total_referrals"], 2)
        self.assertEqual(response.context["pending_approvals"], 1)
        self.assertEqual(response.context["success_rate"], 50.0)

    def test_dashboard_displays_top_referrer(self):
        """Test that dashboard displays top referrer."""
        # Create referrer with multiple successful referrals
        referrer = create_user(email="referrer@example.com")
        identity = create_referral_identity(customer=referrer)

        # Create 3 approved attributions (use same program)
        for i in range(3):
            referee = create_user(email=f"referee{i}@example.com")
            create_referral_attribution(
                program=self.program,
                referrer_identity=identity,
                referee_customer=referee,
                status="approved",
            )

        response = self.client.get(reverse("referrals:dashboard"))

        # Check top referrer
        self.assertIsNotNone(response.context["top_referrer"])
        self.assertEqual(response.context["top_referrer"]["count"], 3)

    def test_dashboard_post_updates_program(self):
        """Test that POST updates program settings."""
        response = self.client.post(
            reverse("referrals:dashboard"), {"name": "Updated Program Name", "status": "active"}
        )

        # Should redirect
        self.assertEqual(response.status_code, 302)

        # Check program was updated
        self.program.refresh_from_db()
        self.assertEqual(self.program.name, "Updated Program Name")
        self.assertEqual(self.program.status, "active")


@override_settings(LANGUAGE_CODE="en")
class FilterAttributionsViewTest(TestCase):
    """Tests for filter_attributions AJAX view."""

    def setUp(self):
        self.program = create_referral_program()
        self.admin = create_user(email="admin@example.com", is_staff=True)
        self.client = Client()
        self.client.force_login(self.admin)

    def test_requires_ajax(self):
        """Test that view requires AJAX request."""
        response = self.client.get(reverse("referrals:filter_attributions"))

        self.assertEqual(response.status_code, 400)

    def test_filter_by_status(self):
        """Test filtering by status."""
        # Create attributions with different statuses
        create_referral_attribution(status="pending")
        create_referral_attribution(status="approved")
        create_referral_attribution(status="rejected")

        response = self.client.get(
            reverse("referrals:filter_attributions"),
            {"status": "pending"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("html", data)
        self.assertIn("count", data)

    def test_filter_by_search(self):
        """Test filtering by search term."""
        # Create attributions
        referrer1 = create_user(email="john@example.com")
        referrer2 = create_user(email="jane@example.com")
        identity1 = create_referral_identity(customer=referrer1)
        identity2 = create_referral_identity(customer=referrer2)

        create_referral_attribution(referrer_identity=identity1)
        create_referral_attribution(referrer_identity=identity2)

        response = self.client.get(
            reverse("referrals:filter_attributions"),
            {"search": "john"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)

    def test_filter_by_date_range(self):
        """Test filtering by date range."""
        # Create attribution
        create_referral_attribution()

        today = timezone.now().date()

        response = self.client.get(
            reverse("referrals:filter_attributions"),
            {"date_from": str(today), "date_to": str(today)},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)


@override_settings(LANGUAGE_CODE="en")
class FilterRewardsViewTest(TestCase):
    """Tests for filter_rewards AJAX view."""

    def setUp(self):
        self.program = create_referral_program()
        self.admin = create_user(email="admin@example.com", is_staff=True)
        self.client = Client()
        self.client.force_login(self.admin)

    def test_requires_ajax(self):
        """Test that view requires AJAX request."""
        response = self.client.get(reverse("referrals:filter_rewards"))

        self.assertEqual(response.status_code, 400)

    def test_filter_by_status(self):
        """Test filtering by status."""
        # Create rewards with different statuses
        create_referral_reward(status="pending")
        create_referral_reward(status="issued")
        create_referral_reward(status="redeemed")

        response = self.client.get(
            reverse("referrals:filter_rewards"),
            {"status": "issued"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("html", data)
        self.assertIn("count", data)

    def test_filter_by_kind(self):
        """Test filtering by reward kind."""
        # Create rewards of different kinds
        create_referral_reward(kind="credit")
        create_referral_reward(kind="coupon")

        response = self.client.get(
            reverse("referrals:filter_rewards"),
            {"kind": "credit"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)

    def test_filter_expiring_soon(self):
        """Test filtering rewards expiring soon."""
        # Create reward expiring in 3 days
        from datetime import timedelta

        expiry_date = timezone.now() + timedelta(days=3)

        create_referral_reward(status="issued", expires_at=expiry_date)

        response = self.client.get(
            reverse("referrals:filter_rewards"),
            {"expiring_soon": "true"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)


@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(LANGUAGE_CODE="en")
class ApproveAttributionViewTest(TestCase):
    """Tests for approve_attribution view."""

    def setUp(self):
        self.program = create_referral_program()
        self.admin = create_user(email="admin@example.com", is_staff=True)
        self.client = Client()
        self.client.force_login(self.admin)

    def test_requires_post(self):
        """Test that view requires POST."""
        attribution = create_referral_attribution(status="pending")

        response = self.client.get(reverse("referrals:approve_attribution", args=[attribution.pk]))

        self.assertEqual(response.status_code, 405)

    def test_approve_pending_attribution(self):
        """Test approving pending attribution."""
        attribution = create_referral_attribution(status="pending")

        response = self.client.post(reverse("referrals:approve_attribution", args=[attribution.pk]))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

        # Check attribution was approved
        attribution.refresh_from_db()
        self.assertEqual(attribution.status, "approved")
        self.assertIsNotNone(attribution.approved_at)
        self.assertEqual(attribution.reviewed_by, self.admin)

    def test_cannot_approve_non_pending(self):
        """Test that non-pending attributions cannot be approved."""
        attribution = create_referral_attribution(status="approved")

        response = self.client.post(reverse("referrals:approve_attribution", args=[attribution.pk]))

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])


@override_settings(LANGUAGE_CODE="en")
class RejectAttributionViewTest(TestCase):
    """Tests for reject_attribution view."""

    def setUp(self):
        self.program = create_referral_program()
        self.admin = create_user(email="admin@example.com", is_staff=True)
        self.client = Client()
        self.client.force_login(self.admin)

    def test_requires_post(self):
        """Test that view requires POST."""
        attribution = create_referral_attribution(status="pending")

        response = self.client.get(reverse("referrals:reject_attribution", args=[attribution.pk]))

        self.assertEqual(response.status_code, 405)

    def test_reject_pending_attribution(self):
        """Test rejecting pending attribution."""
        attribution = create_referral_attribution(status="pending")

        response = self.client.post(
            reverse("referrals:reject_attribution", args=[attribution.pk]),
            {"reason": "fraud_risk", "notes": "High risk score"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

        # Check attribution was rejected
        attribution.refresh_from_db()
        self.assertEqual(attribution.status, "rejected")
        self.assertEqual(attribution.rejection_reason, "fraud_risk")
        self.assertIn("High risk score", attribution.rejection_notes)

    def test_cannot_reject_non_pending(self):
        """Test that non-pending attributions cannot be rejected."""
        attribution = create_referral_attribution(status="approved")

        response = self.client.post(
            reverse("referrals:reject_attribution", args=[attribution.pk]), {"reason": "fraud_risk"}
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])


@override_settings(LANGUAGE_CODE="en")
class IssueRewardViewTest(TestCase):
    """Tests for issue_reward_view."""

    def setUp(self):
        self.program = create_referral_program()
        self.admin = create_user(email="admin@example.com", is_staff=True)
        self.client = Client()
        self.client.force_login(self.admin)

    def test_requires_post(self):
        """Test that view requires POST."""
        reward = create_referral_reward(status="pending")

        response = self.client.get(reverse("referrals:issue_reward", args=[reward.pk]))

        self.assertEqual(response.status_code, 405)

    @patch("referrals.signals.send_referral_reward_email")
    def test_issue_pending_reward(self, mock_send_email):
        """Test issuing pending reward."""
        # Mock email sending to avoid EmailSender import error
        mock_send_email.return_value = True

        reward = create_referral_reward(status="pending")

        response = self.client.post(reverse("referrals:issue_reward", args=[reward.pk]))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

        # Check reward was issued
        reward.refresh_from_db()
        self.assertEqual(reward.status, "issued")
        self.assertIsNotNone(reward.issued_at)

    def test_cannot_issue_non_pending(self):
        """Test that non-pending rewards cannot be issued."""
        reward = create_referral_reward(status="issued")

        response = self.client.post(reverse("referrals:issue_reward", args=[reward.pk]))

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])


@override_settings(LANGUAGE_CODE="en")
class RevokeRewardViewTest(TestCase):
    """Tests for revoke_reward_view."""

    def setUp(self):
        self.program = create_referral_program()
        self.admin = create_user(email="admin@example.com", is_staff=True)
        self.client = Client()
        self.client.force_login(self.admin)

    def test_requires_post(self):
        """Test that view requires POST."""
        reward = create_referral_reward(status="issued")

        response = self.client.get(reverse("referrals:revoke_reward", args=[reward.pk]))

        self.assertEqual(response.status_code, 405)

    def test_revoke_issued_reward(self):
        """Test revoking issued reward."""
        reward = create_referral_reward(status="issued")

        response = self.client.post(
            reverse("referrals:revoke_reward", args=[reward.pk]), {"reason": "Order cancelled"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

        # Check reward was revoked
        reward.refresh_from_db()
        self.assertEqual(reward.status, "revoked")
        self.assertIn("Order cancelled", reward.revocation_reason)

    def test_cannot_revoke_redeemed(self):
        """Test that redeemed rewards cannot be revoked."""
        reward = create_referral_reward(status="redeemed")

        response = self.client.post(
            reverse("referrals:revoke_reward", args=[reward.pk]), {"reason": "Test"}
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
