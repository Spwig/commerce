"""
Social Sharing Admin Tests
"""

from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.sites.models import Site

from social_sharing.admin import SocialShareAdmin, ShareCountAdmin, SocialSharingSettingsAdmin
from social_sharing.models import SocialShare, ShareCount
from social_sharing.settings_models import SocialSharingSettings
from social_sharing.tests.factories import (
    create_user, create_social_share, create_share_count,
    create_settings, get_product_content_type,
)


def _ensure_site_and_settings():
    """Ensure Django Site and SiteSettings exist for middleware."""
    Site.objects.get_or_create(pk=1, defaults={'domain': 'testserver', 'name': 'Test'})
    from core.models import SiteSettings
    if not SiteSettings.objects.filter(pk=1).exists():
        SiteSettings.objects.create(
            pk=1,
            site_name='Test Store',
            admin_email='test@test.spwig.com',
            default_currency='USD',
        )


class SocialShareAdminTest(TestCase):
    """Tests for SocialShareAdmin."""

    def setUp(self):
        self.site = AdminSite()
        self.admin_class = SocialShareAdmin(SocialShare, self.site)
        self.admin_user = create_user(email='admin4@test.spwig.com', is_staff=True)
        self.factory = RequestFactory()

    def test_has_no_add_permission(self):
        """Cannot manually create shares via admin."""
        request = self.factory.get('/')
        request.user = self.admin_user
        self.assertFalse(self.admin_class.has_add_permission(request))

    def test_has_no_change_permission(self):
        """Cannot edit shares via admin."""
        request = self.factory.get('/')
        request.user = self.admin_user
        self.assertFalse(self.admin_class.has_change_permission(request))

    def test_platform_badge_uses_css_class(self):
        """Platform badge should use CSS class, not inline styles."""
        share = create_social_share(platform='facebook')
        result = self.admin_class.platform_badge(share)
        self.assertIn('social-admin-platform-badge', result)
        self.assertIn('platform-facebook', result)
        self.assertNotIn('style=', result)

    def test_user_info_anonymous_uses_css_class(self):
        """Anonymous user display should use CSS class, not inline styles."""
        share = create_social_share(user=None, object_id=100)
        result = self.admin_class.user_info(share)
        self.assertIn('social-admin-anonymous', result)
        self.assertNotIn('style=', result)

    def test_user_info_with_user_has_link(self):
        """User info should link to user admin page."""
        user = create_user(email='linked@test.spwig.com')
        share = create_social_share(user=user, object_id=101)
        result = self.admin_class.user_info(share)
        self.assertIn('href=', result)
        self.assertIn('linked@test.spwig.com', result)

    def test_media_includes_css(self):
        """Admin should load CSS from Media class."""
        media = self.admin_class.media
        css_files = str(media)
        self.assertIn('admin-shares.css', css_files)


class ShareCountAdminTest(TestCase):
    """Tests for ShareCountAdmin."""

    def setUp(self):
        self.site = AdminSite()
        self.admin_class = ShareCountAdmin(ShareCount, self.site)
        self.admin_user = create_user(email='admin5@test.spwig.com', is_staff=True)
        self.factory = RequestFactory()

    def test_has_no_add_permission(self):
        request = self.factory.get('/')
        request.user = self.admin_user
        self.assertFalse(self.admin_class.has_add_permission(request))

    def test_has_no_change_permission(self):
        request = self.factory.get('/')
        request.user = self.admin_user
        self.assertFalse(self.admin_class.has_change_permission(request))

    def test_has_no_delete_permission(self):
        request = self.factory.get('/')
        request.user = self.admin_user
        self.assertFalse(self.admin_class.has_delete_permission(request))

    def test_count_display_uses_css_class(self):
        """Count display should use CSS class, not inline styles."""
        sc = create_share_count(count=5, object_id=200)
        result = self.admin_class.count_display(sc)
        self.assertIn('social-admin-count-normal', result)
        self.assertNotIn('style=', result)

    def test_count_display_high(self):
        sc = create_share_count(count=1500, object_id=201)
        result = self.admin_class.count_display(sc)
        self.assertIn('social-admin-count-high', result)

    def test_count_display_medium(self):
        sc = create_share_count(count=500, object_id=202)
        result = self.admin_class.count_display(sc)
        self.assertIn('social-admin-count-medium', result)

    def test_platform_badge_uses_css_class(self):
        sc = create_share_count(platform='twitter', object_id=203)
        result = self.admin_class.platform_badge(sc)
        self.assertIn('social-admin-platform-badge', result)
        self.assertIn('platform-twitter', result)
        self.assertNotIn('style=', result)


class SocialSharingSettingsAdminTest(TestCase):
    """Tests for SocialSharingSettingsAdmin."""

    def setUp(self):
        _ensure_site_and_settings()
        self.admin = create_user(email='admin6@test.spwig.com', is_staff=True)
        self.client.login(username='admin6@test.spwig.com', password='testpass123')

    def test_changelist_redirects_to_singleton(self):
        """Settings list view should redirect to the singleton change page."""
        resp = self.client.get('/en/admin/social_sharing/socialsharingsettings/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('socialsharingsettings/1/change/', resp.url)

    def test_cannot_delete_settings(self):
        """Settings should not have delete permission."""
        site = AdminSite()
        admin_cls = SocialSharingSettingsAdmin(SocialSharingSettings, site)
        request = RequestFactory().get('/')
        request.user = self.admin
        self.assertFalse(admin_cls.has_delete_permission(request))


class SocialSharingSettingsFormTest(TestCase):
    """Tests for the custom SocialSharingSettingsForm."""

    def setUp(self):
        _ensure_site_and_settings()

    def test_form_has_checkbox_widget_for_platforms(self):
        """enabled_platforms should use CheckboxSelectMultiple."""
        from django import forms as django_forms
        from social_sharing.forms import SocialSharingSettingsForm
        form = SocialSharingSettingsForm()
        self.assertIsInstance(
            form.fields['enabled_platforms'].widget,
            django_forms.CheckboxSelectMultiple
        )

    def test_form_excludes_widget_slug(self):
        """widget_slug should not appear in the form."""
        from social_sharing.forms import SocialSharingSettingsForm
        form = SocialSharingSettingsForm()
        self.assertNotIn('widget_slug', form.fields)

    def test_form_excludes_default_config(self):
        """default_config should not appear in the form."""
        from social_sharing.forms import SocialSharingSettingsForm
        form = SocialSharingSettingsForm()
        self.assertNotIn('default_config', form.fields)

    def test_form_has_new_appearance_fields(self):
        """All new appearance fields should be present."""
        from social_sharing.forms import SocialSharingSettingsForm
        form = SocialSharingSettingsForm()
        for field_name in ['button_style', 'button_size', 'layout_direction',
                           'show_title', 'mobile_visibility']:
            self.assertIn(field_name, form.fields, f'{field_name} missing from form')

    def test_form_saves_platforms_as_list(self):
        """Selecting platforms should save as a JSON list."""
        from social_sharing.forms import SocialSharingSettingsForm
        settings = create_settings()
        form_data = {
            'enable_on_products': True,
            'enable_on_categories': False,
            'enable_on_blog_posts': True,
            'enable_on_pages': False,
            'placement_position': 'below_content',
            'enabled_platforms': ['facebook', 'twitter'],
            'button_style': 'icon_only',
            'button_size': 'medium',
            'layout_direction': 'horizontal',
            'show_title': True,
            'mobile_visibility': 'show',
            'show_counts': True,
            'track_shares': True,
        }
        form = SocialSharingSettingsForm(data=form_data, instance=settings)
        self.assertTrue(form.is_valid(), form.errors)
        obj = form.save()
        self.assertEqual(obj.enabled_platforms, ['facebook', 'twitter'])

    def test_empty_platforms_saves_empty_list(self):
        """No platforms selected saves empty list (meaning: show all)."""
        from social_sharing.forms import SocialSharingSettingsForm
        settings = create_settings()
        form_data = {
            'enable_on_products': True,
            'enable_on_categories': False,
            'enable_on_blog_posts': True,
            'enable_on_pages': False,
            'placement_position': 'below_content',
            'enabled_platforms': [],
            'button_style': 'icon_only',
            'button_size': 'medium',
            'layout_direction': 'horizontal',
            'show_title': True,
            'mobile_visibility': 'show',
            'show_counts': True,
            'track_shares': True,
        }
        form = SocialSharingSettingsForm(data=form_data, instance=settings)
        self.assertTrue(form.is_valid(), form.errors)
        obj = form.save()
        self.assertEqual(obj.enabled_platforms, [])
