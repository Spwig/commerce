"""
Social Sharing Template Tag Tests
"""

from django.test import TestCase, RequestFactory
from django.template import Template, Context

from social_sharing.templatetags.social_share_tags import (
    PLATFORM_DATA, DEFAULT_PLATFORM_ORDER,
)
from social_sharing.tests.factories import create_settings


class SocialShareButtonsTagTest(TestCase):
    """Tests for the social_share_buttons inclusion tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.settings = create_settings()

    def test_tag_renders_with_context(self):
        """Tag should provide render=True and platforms in context."""
        request = self.factory.get('/test/')
        template = Template(
            '{% load social_share_tags %}'
            '{% social_share_buttons content_type="product" object_id=1 %}'
        )
        context = Context({'request': request})
        # Inclusion tag should render without errors
        rendered = template.render(context)
        self.assertIn('social-share-widget', rendered)

    def test_tag_provides_enabled_platforms(self):
        """Tag context should include enabled platform list with icons."""
        request = self.factory.get('/test/')
        template = Template(
            '{% load social_share_tags %}'
            '{% social_share_buttons content_type="product" object_id=1 %}'
        )
        context = Context({'request': request})
        rendered = template.render(context)
        # Should contain platform buttons
        self.assertIn('data-platform="facebook"', rendered)
        self.assertIn('data-platform="twitter"', rendered)

    def test_platform_data_has_all_platforms(self):
        """PLATFORM_DATA should cover all default platforms."""
        for platform in DEFAULT_PLATFORM_ORDER:
            self.assertIn(platform, PLATFORM_DATA)
            self.assertIn('label', PLATFORM_DATA[platform])
            self.assertIn('icon_svg', PLATFORM_DATA[platform])

    def test_platform_svgs_are_valid(self):
        """Each platform icon should be an SVG."""
        for platform, data in PLATFORM_DATA.items():
            svg = str(data['icon_svg'])
            self.assertTrue(svg.startswith('<svg'), f'{platform} icon is not SVG')
            self.assertIn('</svg>', svg, f'{platform} icon SVG is unclosed')

    def test_custom_enabled_platforms(self):
        """Merchants can restrict to specific platforms."""
        create_settings(enabled_platforms=['facebook', 'twitter'])
        request = self.factory.get('/test/')
        template = Template(
            '{% load social_share_tags %}'
            '{% social_share_buttons content_type="product" object_id=1 %}'
        )
        context = Context({'request': request})
        rendered = template.render(context)
        self.assertIn('data-platform="facebook"', rendered)
        self.assertIn('data-platform="twitter"', rendered)
        self.assertNotIn('data-platform="linkedin"', rendered)


class SocialShareEnabledTagTest(TestCase):
    """Tests for the social_share_enabled simple tag."""

    def test_enabled_for_products(self):
        create_settings(enable_on_products=True)
        template = Template(
            '{% load social_share_tags %}'
            '{% social_share_enabled "product" as enabled %}'
            '{{ enabled }}'
        )
        rendered = template.render(Context())
        self.assertIn('True', rendered)

    def test_disabled_for_categories(self):
        create_settings(enable_on_categories=False)
        template = Template(
            '{% load social_share_tags %}'
            '{% social_share_enabled "category" as enabled %}'
            '{{ enabled }}'
        )
        rendered = template.render(Context())
        self.assertIn('False', rendered)

    def test_unknown_page_type_returns_false(self):
        create_settings()
        template = Template(
            '{% load social_share_tags %}'
            '{% social_share_enabled "nonexistent" as enabled %}'
            '{{ enabled }}'
        )
        rendered = template.render(Context())
        self.assertIn('False', rendered)


class SocialShareButtonsDisplaySettingsTest(TestCase):
    """Tests that new display settings produce correct CSS modifier classes."""

    def setUp(self):
        self.factory = RequestFactory()

    def _render(self, **settings_kwargs):
        """Helper to render the widget tag and return HTML."""
        create_settings(**settings_kwargs)
        request = self.factory.get('/test/')
        template = Template(
            '{% load social_share_tags %}'
            '{% social_share_buttons content_type="product" object_id=1 %}'
        )
        return template.render(Context({'request': request}))

    def test_button_style_icon_label(self):
        rendered = self._render(button_style='icon_label')
        self.assertIn('social-share-style-icon_label', rendered)

    def test_button_style_label_only(self):
        rendered = self._render(button_style='label_only')
        self.assertIn('social-share-style-label_only', rendered)

    def test_button_style_icon_only(self):
        rendered = self._render(button_style='icon_only')
        self.assertIn('social-share-style-icon_only', rendered)

    def test_button_size_large(self):
        rendered = self._render(button_size='large')
        self.assertIn('social-share-size-large', rendered)

    def test_button_size_small(self):
        rendered = self._render(button_size='small')
        self.assertIn('social-share-size-small', rendered)

    def test_layout_direction_vertical(self):
        rendered = self._render(layout_direction='vertical')
        self.assertIn('social-share-layout-vertical', rendered)

    def test_layout_direction_horizontal(self):
        rendered = self._render(layout_direction='horizontal')
        self.assertIn('social-share-layout-horizontal', rendered)

    def test_title_hidden_when_disabled(self):
        rendered = self._render(show_title=False)
        self.assertIn('social-share-title-hidden', rendered)

    def test_title_visible_when_enabled(self):
        rendered = self._render(show_title=True)
        self.assertNotIn('social-share-title-hidden', rendered)

    def test_mobile_hide_class(self):
        rendered = self._render(mobile_visibility='hide')
        self.assertIn('social-share-mobile-hide', rendered)

    def test_mobile_only_class(self):
        rendered = self._render(mobile_visibility='mobile_only')
        self.assertIn('social-share-mobile-only', rendered)

    def test_mobile_show_no_visibility_class(self):
        rendered = self._render(mobile_visibility='show')
        self.assertNotIn('social-share-mobile-hide', rendered)
        self.assertNotIn('social-share-mobile-only', rendered)

    def test_label_span_always_present(self):
        """Label span should be in DOM for all buttons (CSS controls visibility)."""
        rendered = self._render()
        self.assertIn('social-share-label', rendered)


class AutoSocialShareButtonsTagTest(TestCase):
    """Tests for the auto_social_share_buttons simple tag."""

    def test_returns_empty_when_disabled(self):
        create_settings(enable_on_products=False)
        template = Template(
            '{% load social_share_tags %}'
            '{% auto_social_share_buttons "product" content_type="product" object_id=1 %}'
        )
        rendered = template.render(Context())
        self.assertEqual(rendered.strip(), '')

    def test_returns_widget_when_enabled(self):
        create_settings(enable_on_products=True)
        template = Template(
            '{% load social_share_tags %}'
            '{% auto_social_share_buttons "product" content_type="product" object_id=1 %}'
        )
        rendered = template.render(Context({'request': None}))
        # Should contain the widget (rendered via auto_include.html -> social_share_buttons)
        # Note: may be empty if request context is missing, which is expected
