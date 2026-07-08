"""
Social Sharing Signal Tests
"""

from django.test import TestCase
from unittest.mock import patch, MagicMock

from social_sharing.models import SocialShare, ShareCount
from social_sharing.tests.factories import (
    create_user, create_social_share, get_product_content_type,
)


class ShareCountSignalTest(TestCase):
    """Tests for share count signal handlers."""

    def test_creating_share_increments_count(self):
        """Creating a SocialShare should auto-create/increment ShareCount."""
        ct = get_product_content_type()
        create_social_share(platform='facebook', content_type=ct, object_id=1)

        sc = ShareCount.objects.get(content_type=ct, object_id=1, platform='facebook')
        self.assertEqual(sc.count, 1)

    def test_second_share_increments_existing_count(self):
        """Second share should increment existing ShareCount."""
        ct = get_product_content_type()
        create_social_share(platform='facebook', content_type=ct, object_id=1)
        create_social_share(platform='facebook', content_type=ct, object_id=1)

        sc = ShareCount.objects.get(content_type=ct, object_id=1, platform='facebook')
        self.assertEqual(sc.count, 2)

    def test_different_platforms_separate_counts(self):
        """Different platforms should have separate ShareCount records."""
        ct = get_product_content_type()
        create_social_share(platform='facebook', content_type=ct, object_id=1)
        create_social_share(platform='twitter', content_type=ct, object_id=1)

        self.assertEqual(ShareCount.objects.filter(content_type=ct, object_id=1).count(), 2)
        self.assertEqual(
            ShareCount.objects.get(content_type=ct, object_id=1, platform='facebook').count, 1
        )
        self.assertEqual(
            ShareCount.objects.get(content_type=ct, object_id=1, platform='twitter').count, 1
        )

    def test_deleting_share_decrements_count(self):
        """Deleting a share should decrement the ShareCount."""
        ct = get_product_content_type()
        share1 = create_social_share(platform='facebook', content_type=ct, object_id=1)
        create_social_share(platform='facebook', content_type=ct, object_id=1)

        # Count should be 2
        sc = ShareCount.objects.get(content_type=ct, object_id=1, platform='facebook')
        self.assertEqual(sc.count, 2)

        # Delete one
        share1.delete()
        sc.refresh_from_db()
        self.assertEqual(sc.count, 1)

    def test_deleting_last_share_removes_count(self):
        """Deleting the last share should remove the ShareCount record."""
        ct = get_product_content_type()
        share = create_social_share(platform='facebook', content_type=ct, object_id=1)
        self.assertTrue(
            ShareCount.objects.filter(content_type=ct, object_id=1, platform='facebook').exists()
        )

        share.delete()
        self.assertFalse(
            ShareCount.objects.filter(content_type=ct, object_id=1, platform='facebook').exists()
        )

    @patch('social_sharing.signals.BadgeAwardingService', create=True)
    @patch('social_sharing.signals.LoyaltyMember', create=True)
    def test_loyalty_badge_check_on_share(self, mock_member_class, mock_badge_class):
        """Creating a share by a logged-in user should attempt badge check."""
        user = create_user()

        # Mock the loyalty member lookup
        mock_member = MagicMock()
        mock_member_class.objects.get.return_value = mock_member

        # Mock the badge service
        mock_service = MagicMock()
        mock_service.check_and_award_badges.return_value = []
        mock_badge_class.return_value = mock_service

        with patch('social_sharing.signals.LoyaltyMember', mock_member_class), \
             patch('social_sharing.signals.BadgeAwardingService', mock_badge_class):
            create_social_share(user=user, platform='facebook')

    def test_anonymous_share_skips_badge_check(self):
        """Anonymous shares should not attempt badge check."""
        # This should not raise even if loyalty app isn't installed
        create_social_share(user=None, platform='facebook')
