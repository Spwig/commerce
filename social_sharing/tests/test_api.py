"""
Social Sharing API Tests
"""

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from social_sharing.models import SocialShare
from social_sharing.tests.factories import (
    create_share_count,
    create_social_share,
    create_test_blog_post,
    create_user,
    get_product_content_type,
)

User = get_user_model()


def _ensure_site_and_settings():
    """Ensure Django Site and SiteSettings exist for middleware."""
    Site.objects.get_or_create(pk=1, defaults={"domain": "testserver", "name": "Test"})
    from core.models import SiteSettings

    if not SiteSettings.objects.filter(pk=1).exists():
        SiteSettings.objects.create(
            pk=1,
            site_name="Test Store",
            admin_email="test@test.spwig.com",
            default_currency="USD",
        )


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class TrackShareAPITest(TestCase):
    """Tests for POST /api/social/track/"""

    def setUp(self):
        _ensure_site_and_settings()
        from django.core.cache import cache

        cache.clear()  # Reset DRF throttle state between tests
        self.client = APIClient()
        self.user = create_user()
        self.ct = get_product_content_type()
        self.blog_post = create_test_blog_post()
        self.object_id = self.blog_post.pk
        self.url = "/api/social/track/"

    def test_track_share_authenticated(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "https://example.com/product/1/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data["success"])
        self.assertIn("share_id", resp.data)

    def test_track_share_unauthenticated_returns_401_or_403(self):
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "https://example.com/product/1/",
            },
            format="json",
        )
        self.assertIn(resp.status_code, [401, 403])

    def test_track_share_missing_fields(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_track_share_invalid_platform(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "reddit",
                "url": "https://example.com/product/1/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        # With serializer-based validation, platform errors are nested
        # under `errors.platform` rather than a free-text `error` field.
        self.assertIn("platform", resp.data.get("errors", {}))

    def test_track_share_invalid_content_type(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            self.url,
            {
                "content_type": "nonexistent_model",
                "object_id": 1,
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_track_share_creates_record(self):
        self.client.force_authenticate(user=self.user)
        self.assertEqual(SocialShare.objects.count(), 0)
        self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "twitter",
                "url": "https://example.com/product/1/",
            },
            format="json",
        )
        self.assertEqual(SocialShare.objects.count(), 1)
        share = SocialShare.objects.first()
        self.assertEqual(share.platform, "twitter")
        self.assertEqual(share.user, self.user)

    # ─── Security hardening tests (added after security audit) ──────────

    def test_track_share_rejects_javascript_url(self):
        """URLValidator should reject `javascript:` scheme to prevent stored XSS."""
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "javascript:alert(1)",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)

    def test_track_share_rejects_data_url(self):
        """URLValidator should reject `data:` URIs."""
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "data:text/html,<script>alert(1)</script>",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)

    def test_track_share_rejects_non_whitelisted_content_type(self):
        """The whitelist should block attempts to share against `user`, `session`, etc."""
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            self.url,
            {
                "content_type": "user",  # not in SHAREABLE_CONTENT_TYPES
                "object_id": self.user.id,
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)

    def test_track_share_rejects_nonexistent_object_id(self):
        """The existence check should reject orphan IDs (enumeration defense)."""
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": 999999,  # definitely no BlogPost with this pk
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class TrackShareAnonymousAPITest(TestCase):
    """Tests for POST /api/social/track/anonymous/ — guest share tracking."""

    def setUp(self):
        _ensure_site_and_settings()
        from django.core.cache import cache

        cache.clear()  # Reset DRF throttle state between tests
        self.client = APIClient()
        self.ct = get_product_content_type()
        self.blog_post = create_test_blog_post()
        self.object_id = self.blog_post.pk
        self.url = "/api/social/track/anonymous/"

    def test_anonymous_share_without_auth_succeeds(self):
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "https://example.com/products/vc-serum",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data["success"])
        self.assertIn("share_id", resp.data)

    def test_anonymous_share_creates_record_with_null_user(self):
        self.assertEqual(SocialShare.objects.count(), 0)
        self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "whatsapp",
                "url": "https://example.com/products/vc-serum",
            },
            format="json",
        )
        self.assertEqual(SocialShare.objects.count(), 1)
        share = SocialShare.objects.first()
        self.assertIsNone(share.user)
        self.assertEqual(share.platform, "whatsapp")
        self.assertEqual(share.object_id, self.object_id)

    def test_anonymous_share_links_to_session_key(self):
        """Anonymous shares should link to the visitor's session for funnel attribution."""
        # Prime a session so session_key is stable
        self.client.get("/")  # harmless request to create a session
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "twitter",
                "url": "https://example.com/products/vc-serum",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        share = SocialShare.objects.first()
        self.assertTrue(share.session_id)  # non-empty

    def test_anonymous_share_accepts_app_label_model_form(self):
        """Both 'blogpost' and 'blog.blogpost' should work."""
        resp = self.client.post(
            self.url,
            {
                "content_type": f"{self.ct.app_label}.{self.ct.model}",
                "object_id": self.object_id,
                "platform": "telegram",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)

    def test_anonymous_share_missing_fields_returns_400(self):
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_anonymous_share_invalid_platform_returns_400(self):
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "reddit",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_anonymous_share_invalid_content_type_returns_400(self):
        resp = self.client.post(
            self.url,
            {
                "content_type": "definitely_not_a_model",
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_anonymous_share_non_integer_object_id_returns_400(self):
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": "not-a-number",
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    # ─── Security hardening tests (added after security audit) ──────────

    def test_anonymous_share_rejects_javascript_url(self):
        """URLValidator blocks `javascript:` URIs — no stored XSS via admin templates."""
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "javascript:alert(document.cookie)",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)

    def test_anonymous_share_rejects_data_url(self):
        """URLValidator blocks `data:` URIs."""
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "data:text/html,<script>alert(1)</script>",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)

    def test_anonymous_share_rejects_non_whitelisted_content_type(self):
        """Blocks shares against internal models (User, Session, etc.)."""
        resp = self.client.post(
            self.url,
            {
                "content_type": "user",  # not in SHAREABLE_CONTENT_TYPES
                "object_id": 1,
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)

    def test_anonymous_share_rejects_session_content_type(self):
        """Blocks shares against `session` even though it's a valid Django ContentType."""
        resp = self.client.post(
            self.url,
            {
                "content_type": "session",
                "object_id": 1,
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)

    def test_anonymous_share_rejects_nonexistent_object_id(self):
        """Orphan object_ids are rejected — blocks ID enumeration."""
        resp = self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": 999999,  # no BlogPost with this pk
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(SocialShare.objects.count(), 0)

    def test_anonymous_share_does_not_create_session_on_validation_failure(self):
        """Invalid requests must not persist a Django session — no amplification attack."""
        from django.contrib.sessions.models import Session

        initial_sessions = Session.objects.count()
        # Invalid platform → validation fails
        self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "reddit",
                "url": "https://example.com/",
            },
            format="json",
        )
        # Invalid URL → validation fails
        self.client.post(
            self.url,
            {
                "content_type": self.ct.model,
                "object_id": self.object_id,
                "platform": "facebook",
                "url": "javascript:alert(1)",
            },
            format="json",
        )
        # Invalid content type → validation fails
        self.client.post(
            self.url,
            {
                "content_type": "user",
                "object_id": 1,
                "platform": "facebook",
                "url": "https://example.com/",
            },
            format="json",
        )
        # No new sessions should have been persisted
        self.assertEqual(Session.objects.count(), initial_sessions)


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class GetShareCountsAPITest(TestCase):
    """Tests for GET /api/social/counts/<content_type>/<object_id>/"""

    def setUp(self):
        _ensure_site_and_settings()
        self.client = APIClient()
        self.ct = get_product_content_type()

    def test_get_share_counts(self):
        create_share_count(platform="facebook", content_type=self.ct, object_id=300, count=10)
        create_share_count(platform="twitter", content_type=self.ct, object_id=300, count=5)

        resp = self.client.get(f"/api/social/counts/{self.ct.model}/300/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["facebook"], 10)
        self.assertEqual(resp.data["twitter"], 5)
        self.assertEqual(resp.data["total"], 15)

    def test_get_share_counts_no_auth_required(self):
        """Share counts should be publicly accessible."""
        resp = self.client.get(f"/api/social/counts/{self.ct.model}/301/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total"], 0)

    def test_get_share_counts_invalid_content_type(self):
        resp = self.client.get("/api/social/counts/nonexistent_model/1/")
        self.assertEqual(resp.status_code, 404)

    def test_get_share_counts_zero_for_no_shares(self):
        resp = self.client.get(f"/api/social/counts/{self.ct.model}/999/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total"], 0)
        for platform_code, _ in SocialShare.PLATFORM_CHOICES:
            self.assertEqual(resp.data[platform_code], 0)


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class GetUserSharesAPITest(TestCase):
    """Tests for GET /api/social/user/shares/"""

    def setUp(self):
        _ensure_site_and_settings()
        self.client = APIClient()
        self.user = create_user()
        self.url = "/api/social/user/shares/"

    def test_get_user_shares_authenticated(self):
        self.client.force_authenticate(user=self.user)
        create_social_share(user=self.user, platform="facebook", object_id=400)
        create_social_share(user=self.user, platform="twitter", object_id=401)

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total_shares"], 2)
        self.assertEqual(resp.data["by_platform"]["facebook"], 1)
        self.assertEqual(resp.data["by_platform"]["twitter"], 1)
        self.assertEqual(len(resp.data["recent_shares"]), 2)

    def test_get_user_shares_unauthenticated(self):
        resp = self.client.get(self.url)
        self.assertIn(resp.status_code, [401, 403])

    def test_get_user_shares_empty(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total_shares"], 0)

    def test_user_only_sees_own_shares(self):
        other_user = create_user()
        self.client.force_authenticate(user=self.user)
        create_social_share(user=other_user, platform="facebook", object_id=402)
        create_social_share(user=self.user, platform="twitter", object_id=403)

        resp = self.client.get(self.url)
        self.assertEqual(resp.data["total_shares"], 1)
        self.assertEqual(resp.data["by_platform"]["twitter"], 1)
        self.assertEqual(resp.data["by_platform"]["facebook"], 0)
