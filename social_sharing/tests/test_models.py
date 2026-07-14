"""
Social Sharing Model Tests
"""

from django.db import IntegrityError
from django.test import TestCase

from social_sharing.models import SocialShare
from social_sharing.settings_models import SocialSharingSettings
from social_sharing.tests.factories import (
    create_settings,
    create_share_count,
    create_social_share,
    create_user,
    get_product_content_type,
)


class SocialShareModelTest(TestCase):
    """Tests for SocialShare model."""

    def test_create_share_with_user(self):
        user = create_user()
        share = create_social_share(user=user, platform="facebook")
        self.assertEqual(share.platform, "facebook")
        self.assertEqual(share.user, user)
        self.assertIsNotNone(share.shared_at)
        self.assertIsNotNone(share.created_at)
        self.assertIsNotNone(share.updated_at)

    def test_create_anonymous_share(self):
        share = create_social_share(user=None, platform="twitter")
        self.assertIsNone(share.user)
        self.assertEqual(share.platform, "twitter")

    def test_str_with_user(self):
        user = create_user(email="test@example.com")
        share = create_social_share(user=user, platform="facebook")
        self.assertIn("test@example.com", str(share))
        self.assertIn("Facebook", str(share))

    def test_str_anonymous(self):
        share = create_social_share(user=None)
        self.assertIn("Anonymous", str(share))

    def test_ordering_is_newest_first(self):
        share1 = create_social_share(platform="facebook")
        share2 = create_social_share(platform="twitter")
        shares = list(SocialShare.objects.all())
        self.assertEqual(shares[0], share2)
        self.assertEqual(shares[1], share1)

    def test_all_platform_choices_valid(self):
        """Each platform choice should create a valid share."""
        for platform_code, _ in SocialShare.PLATFORM_CHOICES:
            share = create_social_share(platform=platform_code)
            self.assertEqual(share.platform, platform_code)

    def test_device_type_choices(self):
        for device_code, _ in SocialShare.DEVICE_CHOICES:
            share = create_social_share(device_type=device_code)
            self.assertEqual(share.device_type, device_code)

    def test_user_on_delete_set_null(self):
        """Deleting the user should set share.user to NULL, not delete the share."""
        user = create_user()
        share = create_social_share(user=user)
        share_id = share.id
        user.delete()
        share.refresh_from_db()
        self.assertIsNone(share.user)
        self.assertEqual(share.id, share_id)


class ShareCountModelTest(TestCase):
    """Tests for ShareCount model."""

    def test_create_share_count(self):
        sc = create_share_count(platform="facebook", count=5)
        self.assertEqual(sc.count, 5)
        self.assertEqual(sc.platform, "facebook")

    def test_str(self):
        sc = create_share_count(platform="facebook", count=42)
        self.assertIn("Facebook", str(sc))
        self.assertIn("42", str(sc))

    def test_unique_together(self):
        """Same content_type + object_id + platform should fail."""
        ct = get_product_content_type()
        create_share_count(platform="facebook", content_type=ct, object_id=1)
        with self.assertRaises(IntegrityError):
            create_share_count(platform="facebook", content_type=ct, object_id=1)

    def test_different_platforms_allowed(self):
        """Same content but different platforms should succeed."""
        ct = get_product_content_type()
        sc1 = create_share_count(platform="facebook", content_type=ct, object_id=1)
        sc2 = create_share_count(platform="twitter", content_type=ct, object_id=1)
        self.assertNotEqual(sc1.pk, sc2.pk)


class SocialSharingSettingsModelTest(TestCase):
    """Tests for SocialSharingSettings singleton model."""

    def test_singleton_pattern(self):
        """Only one settings instance should exist (pk=1)."""
        settings1 = create_settings()
        settings2 = create_settings(enable_on_products=False)
        self.assertEqual(settings1.pk, settings2.pk)
        self.assertEqual(SocialSharingSettings.objects.count(), 1)

    def test_get_settings_cached(self):
        """get_settings() should return the singleton."""
        create_settings(enable_on_products=True)
        settings = SocialSharingSettings.get_settings()
        self.assertTrue(settings.enable_on_products)

    def test_delete_prevention(self):
        """Settings should not be deletable."""
        settings = create_settings()
        settings.delete()
        # Should still exist
        self.assertTrue(SocialSharingSettings.objects.filter(pk=1).exists())

    def test_str(self):
        settings = create_settings()
        self.assertIn("Social Sharing Settings", str(settings))

    def test_default_values(self):
        settings = create_settings()
        self.assertTrue(settings.enable_on_products)
        self.assertFalse(settings.enable_on_categories)
        self.assertTrue(settings.enable_on_blog_posts)
        self.assertFalse(settings.enable_on_pages)
        self.assertEqual(settings.placement_position, "below_content")
