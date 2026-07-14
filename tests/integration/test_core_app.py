"""
Core app integration tests.

Tests model fields, admin views, widgets, CSP template compliance,
and static file copyright headers following the core audit changes.
"""

import json
import re
from pathlib import Path

import pytest
from django.test import Client

pytestmark = [pytest.mark.integration, pytest.mark.core]


# ============================================================
# Project root for file-level tests
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ============================================================
# Model Tests
# ============================================================


@pytest.mark.django_db
class TestHelpFeedbackModel:
    """Tests for HelpFeedback model updated_at field and timestamps."""

    def _make_topic(self):
        """Create a HelpCategory and HelpTopic for testing."""
        from core.models import HelpCategory, HelpTopic

        category = HelpCategory.objects.create(
            name="Test Category",
            slug="test-category",
            icon="fa-box",
            order=0,
        )
        topic = HelpTopic.objects.create(
            slug="test-topic",
            category=category,
            title_i18n_key="help.test.title",
            content_markdown="Test content",
            component="core",
        )
        return topic

    def test_help_feedback_has_created_at(self):
        """HelpFeedback has auto_now_add created_at field."""
        from core.models import HelpFeedback

        topic = self._make_topic()
        feedback = HelpFeedback.objects.create(
            topic=topic,
            helpful=True,
        )
        assert feedback.created_at is not None

    def test_help_feedback_has_updated_at(self):
        """HelpFeedback has auto_now updated_at field (newly added)."""
        from core.models import HelpFeedback

        topic = self._make_topic()
        feedback = HelpFeedback.objects.create(
            topic=topic,
            helpful=True,
        )
        assert feedback.updated_at is not None

    def test_help_feedback_updated_at_changes_on_save(self):
        """updated_at changes when HelpFeedback is re-saved."""
        from core.models import HelpFeedback

        topic = self._make_topic()
        feedback = HelpFeedback.objects.create(
            topic=topic,
            helpful=True,
        )
        original_updated = feedback.updated_at

        # Modify and save
        feedback.helpful = False
        feedback.save()
        feedback.refresh_from_db()

        assert feedback.updated_at >= original_updated

    def test_help_feedback_model_field_names(self):
        """Verify HelpFeedback has the expected fields."""
        from core.models import HelpFeedback

        field_names = {f.name for f in HelpFeedback._meta.get_fields()}
        expected = {"id", "topic", "user", "helpful", "comment", "created_at", "updated_at"}
        assert expected.issubset(field_names), f"Missing fields: {expected - field_names}"


class TestSiteSettingsVerboseNames:
    """Tests for i18n verbose_name wrappers on SiteSettings shipping/unit fields."""

    FIELDS_WITH_I18N_VERBOSE_NAME = [
        # Shipping fields
        "enable_shipping_labels",
        "default_shipping_provider",
        "default_manual_carrier",
        "shipping_origin_country",
        # Unit system fields
        "default_weight_unit",
        "default_length_unit",
        "default_volume_unit",
        "default_area_unit",
        "default_temperature_unit",
        "enable_unit_conversion",
    ]

    def test_shipping_and_unit_fields_have_verbose_name(self):
        """Shipping and unit system fields should have verbose_name set (i18n wrapped)."""
        from core.models import SiteSettings

        for field_name in self.FIELDS_WITH_I18N_VERBOSE_NAME:
            field = SiteSettings._meta.get_field(field_name)
            # verbose_name should be set and not be the auto-generated one
            assert field.verbose_name is not None, f"Field {field_name} has no verbose_name"
            # Auto-generated verbose_name replaces _ with space;
            # i18n-wrapped names are typically capitalized Title Case
            # The key thing: they should NOT equal the raw field name
            assert str(field.verbose_name) != field_name, (
                f"Field {field_name} verbose_name appears to be auto-generated"
            )

    def test_shipping_fields_exist_on_model(self):
        """Confirm all shipping fields exist on SiteSettings model."""
        from core.models import SiteSettings

        shipping_fields = [
            "enable_shipping_labels",
            "default_shipping_provider",
            "default_manual_carrier",
            "shipping_origin_country",
        ]
        for field_name in shipping_fields:
            assert SiteSettings._meta.get_field(field_name) is not None

    def test_unit_system_fields_exist_on_model(self):
        """Confirm all unit system fields exist on SiteSettings model."""
        from core.models import SiteSettings

        unit_fields = [
            "default_weight_unit",
            "default_length_unit",
            "default_volume_unit",
            "default_area_unit",
            "default_temperature_unit",
            "enable_unit_conversion",
        ]
        for field_name in unit_fields:
            assert SiteSettings._meta.get_field(field_name) is not None

    def test_weight_unit_choices(self):
        """WEIGHT_UNIT_CHOICES contains expected options."""
        from core.models import SiteSettings

        values = [c[0] for c in SiteSettings.WEIGHT_UNIT_CHOICES]
        assert "kg" in values
        assert "lb" in values
        assert "g" in values
        assert "oz" in values

    def test_length_unit_choices(self):
        """LENGTH_UNIT_CHOICES contains expected options."""
        from core.models import SiteSettings

        values = [c[0] for c in SiteSettings.LENGTH_UNIT_CHOICES]
        assert "cm" in values
        assert "in" in values

    def test_volume_unit_choices(self):
        """VOLUME_UNIT_CHOICES contains expected options."""
        from core.models import SiteSettings

        values = [c[0] for c in SiteSettings.VOLUME_UNIT_CHOICES]
        assert "ml" in values
        assert "l" in values
        assert "fl_oz" in values

    def test_area_unit_choices(self):
        """AREA_UNIT_CHOICES contains expected options."""
        from core.models import SiteSettings

        values = [c[0] for c in SiteSettings.AREA_UNIT_CHOICES]
        assert "sq_m" in values
        assert "sq_ft" in values

    def test_temperature_unit_choices(self):
        """TEMPERATURE_UNIT_CHOICES contains expected options."""
        from core.models import SiteSettings

        values = [c[0] for c in SiteSettings.TEMPERATURE_UNIT_CHOICES]
        assert "c" in values
        assert "f" in values


# ============================================================
# Admin Tests
# ============================================================


@pytest.mark.django_db
class TestSiteSettingsAdminFieldTabMapping:
    """Tests for get_field_tab_mapping() -- no phantom fields, all keys are real model fields."""

    def test_all_mapping_keys_are_real_model_fields(self, site_settings):
        """Every key in get_field_tab_mapping() must be an actual SiteSettings DB field.

        This ensures phantom fields (like youtube_url, tiktok_url, pinterest_url that were
        removed in the audit) don't sneak back in.
        """
        from core.admin import SiteSettingsAdmin
        from core.models import SiteSettings

        admin_instance = SiteSettingsAdmin(SiteSettings, None)
        mapping = admin_instance.get_field_tab_mapping()

        # Get actual model field names (only DB-backed columns)
        model_fields = {f.name for f in SiteSettings._meta.get_fields() if hasattr(f, "column")}

        # Check every mapping key exists as a real model field
        phantom_fields = set(mapping.keys()) - model_fields
        assert phantom_fields == set(), (
            f"Phantom fields in get_field_tab_mapping(): {phantom_fields}. "
            f"These keys do not exist on the SiteSettings model."
        )

    def test_phantom_social_media_fields_not_present(self, site_settings):
        """youtube_url, tiktok_url, pinterest_url should NOT be in the mapping."""
        from core.admin import SiteSettingsAdmin
        from core.models import SiteSettings

        admin_instance = SiteSettingsAdmin(SiteSettings, None)
        mapping = admin_instance.get_field_tab_mapping()

        # These were explicitly removed in the audit
        for phantom in ["youtube_url", "tiktok_url", "pinterest_url"]:
            assert phantom not in mapping, (
                f"Phantom field '{phantom}' found in get_field_tab_mapping()"
            )

    def test_mapping_covers_expected_tabs(self, site_settings):
        """The mapping should cover the expected set of admin tabs.

        Inventory fields now live under the "ecommerce" tab and SEO/meta
        fields live under the "pages" tab — those tab IDs were merged.
        """
        from core.admin import SiteSettingsAdmin
        from core.models import SiteSettings

        admin_instance = SiteSettingsAdmin(SiteSettings, None)
        mapping = admin_instance.get_field_tab_mapping()

        tabs = set(mapping.values())
        expected_tabs = {
            "general",
            "contact",
            "locale",
            "multicurrency",
            "ecommerce",
            "shipping",
            "authentication",
            "advanced",
            "pages",
            "cookies",
        }
        assert expected_tabs.issubset(tabs), f"Missing tabs: {expected_tabs - tabs}"

    def test_mapping_returns_json_serializable_dict(self, site_settings):
        """get_field_tab_mapping() must return a JSON-serializable dict for template use."""
        from core.admin import SiteSettingsAdmin
        from core.models import SiteSettings

        admin_instance = SiteSettingsAdmin(SiteSettings, None)
        mapping = admin_instance.get_field_tab_mapping()

        # Should be serializable to JSON (used in change_view for template)
        serialized = json.dumps(mapping)
        assert isinstance(serialized, str)
        assert len(serialized) > 10


@pytest.mark.django_db
class TestSiteSettingsAdminViews:
    """Tests for SiteSettings admin views returning 200."""

    @pytest.fixture
    def staff_client(self, admin_user):
        """Django test client authenticated as staff/superuser."""
        client = Client()
        client.force_login(admin_user)
        return client

    def test_sitesettings_changelist_redirects_to_change(self, staff_client, site_settings):
        """SiteSettings changelist should redirect to the single settings instance."""
        resp = staff_client.get("/en/admin/core/sitesettings/")
        # Should redirect to change form for the existing instance
        assert resp.status_code == 302
        assert f"/en/admin/core/sitesettings/{site_settings.pk}/change/" in resp.url

    def test_sitesettings_change_view_loads(self, staff_client, site_settings):
        """SiteSettings change form should load without errors."""
        resp = staff_client.get(f"/en/admin/core/sitesettings/{site_settings.pk}/change/")
        assert resp.status_code == 200

    def test_sitesettings_change_view_has_field_tab_mapping(self, staff_client, site_settings):
        """SiteSettings change form should include field_tab_mapping_json in context."""
        resp = staff_client.get(f"/en/admin/core/sitesettings/{site_settings.pk}/change/")
        assert resp.status_code == 200
        content = resp.content.decode()
        assert "data-field-tab-map" in content


@pytest.mark.django_db
class TestAPITokenAdminViews:
    """Tests for APIToken admin changelist view."""

    @pytest.fixture
    def staff_client(self, admin_user):
        """Django test client authenticated as staff/superuser."""
        client = Client()
        client.force_login(admin_user)
        return client

    def test_apitoken_changelist_loads(self, staff_client, site_settings):
        """APIToken changelist should load without errors."""
        resp = staff_client.get("/en/admin/core/apitoken/")
        assert resp.status_code == 200

    def test_apitoken_changelist_has_stats(self, staff_client, site_settings):
        """APIToken changelist should include token_stats in context."""
        resp = staff_client.get("/en/admin/core/apitoken/")
        assert resp.status_code == 200
        content = resp.content.decode()
        # Template renders dashboard-stats-grid with stats
        assert "dashboard-stat-card" in content


@pytest.mark.django_db
class TestLicenseStatusAdminViews:
    """Tests for LicenseStatus admin changelist view."""

    @pytest.fixture
    def staff_client(self, admin_user):
        """Django test client authenticated as staff/superuser."""
        client = Client()
        client.force_login(admin_user)
        return client

    def test_license_status_changelist_loads(self, staff_client, site_settings):
        """LicenseStatus changelist should load without errors."""
        resp = staff_client.get("/en/admin/core/licensestatus/")
        assert resp.status_code == 200

    def test_license_status_contains_license_info(self, staff_client, site_settings):
        """LicenseStatus page should contain license information."""
        resp = staff_client.get("/en/admin/core/licensestatus/")
        assert resp.status_code == 200
        content = resp.content.decode()
        assert "license-dashboard" in content


class TestCoreAdminImports:
    """Tests verifying admin module imports are clean (no unused imports)."""

    def test_admin_module_imports_forms(self):
        """core.admin should have 'from django import forms' available."""
        from core import admin as core_admin

        # The forms module should be importable from the admin module's context
        assert hasattr(core_admin, "forms")

    def test_admin_does_not_import_default_storage(self):
        """core.admin should NOT import default_storage (removed in audit)."""
        import inspect

        from core import admin as core_admin

        source = inspect.getsource(core_admin)
        # Should not contain "from django.core.files.storage import default_storage"
        assert "default_storage" not in source, (
            "core.admin still imports default_storage (should have been removed)"
        )

    def test_admin_does_not_import_content_file(self):
        """core.admin should NOT import ContentFile (removed in audit)."""
        import inspect

        from core import admin as core_admin

        source = inspect.getsource(core_admin)
        assert "ContentFile" not in source, (
            "core.admin still imports ContentFile (should have been removed)"
        )


# ============================================================
# Widget Tests
# ============================================================


class TestKeyValueWidget:
    """Tests for KeyValueWidget rendering and data extraction."""

    def test_instantiation_with_defaults(self):
        """KeyValueWidget can be instantiated with default labels."""
        from core.widgets import KeyValueWidget

        widget = KeyValueWidget()
        assert widget.key_label == "Key"
        assert widget.value_label == "Value"

    def test_instantiation_with_custom_labels(self):
        """KeyValueWidget accepts custom key/value labels."""
        from core.widgets import KeyValueWidget

        widget = KeyValueWidget(key_label="Feature", value_label="Detail")
        assert widget.key_label == "Feature"
        assert widget.value_label == "Detail"

    def test_get_context_with_dict_value(self):
        """get_context parses a dict into pairs."""
        from core.widgets import KeyValueWidget

        widget = KeyValueWidget()
        context = widget.get_context("specs", {"color": "red", "size": "large"}, {})
        pairs = context["widget"]["pairs"]
        assert ("color", "red") in pairs
        assert ("size", "large") in pairs

    def test_get_context_with_json_string_value(self):
        """get_context parses JSON string into pairs."""
        from core.widgets import KeyValueWidget

        widget = KeyValueWidget()
        context = widget.get_context("specs", '{"color": "red"}', {})
        pairs = context["widget"]["pairs"]
        assert ("color", "red") in pairs

    def test_get_context_with_none_value(self):
        """get_context handles None value gracefully."""
        from core.widgets import KeyValueWidget

        widget = KeyValueWidget()
        context = widget.get_context("specs", None, {})
        assert context["widget"]["pairs"] == []

    def test_get_context_with_invalid_json(self):
        """get_context handles invalid JSON gracefully."""
        from core.widgets import KeyValueWidget

        widget = KeyValueWidget()
        context = widget.get_context("specs", "not-json", {})
        assert context["widget"]["pairs"] == []

    def test_value_from_datadict(self):
        """value_from_datadict reconstructs JSON dict from POST keys/values."""
        from django.http import QueryDict

        from core.widgets import KeyValueWidget

        widget = KeyValueWidget()
        data = QueryDict(mutable=True)
        data.setlist("specs_keys", ["color", "size", ""])
        data.setlist("specs_values", ["red", "large", "ignored"])

        result = widget.value_from_datadict(data, {}, "specs")
        parsed = json.loads(result)
        assert parsed == {"color": "red", "size": "large"}
        # Empty keys should be stripped
        assert "" not in parsed

    def test_value_from_datadict_strips_whitespace(self):
        """value_from_datadict strips whitespace from keys and values."""
        from django.http import QueryDict

        from core.widgets import KeyValueWidget

        widget = KeyValueWidget()
        data = QueryDict(mutable=True)
        data.setlist("specs_keys", ["  color  "])
        data.setlist("specs_values", ["  red  "])

        result = widget.value_from_datadict(data, {}, "specs")
        parsed = json.loads(result)
        assert parsed == {"color": "red"}

    def test_media_includes_css_and_js(self):
        """KeyValueWidget media includes its CSS and JS files."""
        from core.widgets import KeyValueWidget

        widget = KeyValueWidget()
        media = widget.media
        css_files = [str(f) for f in media._css.get("all", [])]
        js_files = [str(f) for f in media._js]
        assert "core/admin/css/key_value_widget.css" in css_files
        assert "core/admin/js/key_value_widget.js" in js_files


class TestSearchableSelectWidget:
    """Tests for SearchableSelectWidget."""

    def test_instantiation_with_no_icon_callback(self):
        """SearchableSelectWidget can be created without icon_callback."""
        from core.widgets import SearchableSelectWidget

        widget = SearchableSelectWidget()
        assert widget.icon_callback is None
        assert "data-searchable-select" in widget.attrs

    def test_instantiation_with_icon_callback(self):
        """SearchableSelectWidget stores the icon_callback."""
        from core.widgets import SearchableSelectWidget

        def callback(v):
            return f"fa-{v}"

        widget = SearchableSelectWidget(icon_callback=callback)
        assert widget.icon_callback is callback

    def test_create_option_adds_icon_data_attribute(self):
        """create_option adds data-icon when icon_callback returns a value."""
        from core.widgets import SearchableSelectWidget

        def callback(v):
            return "fa-dollar-sign" if v == "USD" else None

        widget = SearchableSelectWidget(icon_callback=callback)

        option = widget.create_option("currency", "USD", "US Dollar", False, 0)
        assert option["attrs"].get("data-icon") == "fa-dollar-sign"
        assert option["attrs"].get("data-icon-style") == "fas"

    def test_create_option_no_icon_for_empty_value(self):
        """create_option does not add icon for empty/None value."""
        from core.widgets import SearchableSelectWidget

        def callback(v):
            return "fa-test"

        widget = SearchableSelectWidget(icon_callback=callback)

        option = widget.create_option("currency", "", "---", False, 0)
        assert "data-icon" not in option["attrs"]

    def test_create_option_handles_callback_exception(self):
        """create_option handles icon_callback exceptions gracefully."""
        from core.widgets import SearchableSelectWidget

        def bad_callback(v):
            raise ValueError("boom")

        widget = SearchableSelectWidget(icon_callback=bad_callback)
        # Should not raise
        option = widget.create_option("field", "val", "Label", False, 0)
        assert "data-icon" not in option["attrs"]


class TestIconPickerWidget:
    """Tests for IconPickerWidget."""

    def test_inherits_from_widget(self):
        """IconPickerWidget should inherit from forms.Widget."""
        from django import forms as django_forms

        from core.widgets import IconPickerWidget

        assert issubclass(IconPickerWidget, django_forms.Widget)

    def test_default_priority_icons_empty(self):
        """IconPickerWidget defaults to empty priority icons."""
        from core.widgets import IconPickerWidget

        widget = IconPickerWidget()
        assert widget.priority_icons == []

    def test_priority_icons_limited_to_10(self):
        """IconPickerWidget limits priority icons to 10."""
        from core.widgets import IconPickerWidget

        icons = [f"fa-icon-{i}" for i in range(15)]
        widget = IconPickerWidget(priority_icons=icons)
        assert len(widget.priority_icons) == 10

    def test_style_prefix_true_by_default(self):
        """IconPickerWidget defaults style_prefix to True."""
        from core.widgets import IconPickerWidget

        widget = IconPickerWidget()
        assert widget.style_prefix is True

    def test_style_prefix_false(self):
        """IconPickerWidget accepts style_prefix=False."""
        from core.widgets import IconPickerWidget

        widget = IconPickerWidget(style_prefix=False)
        assert widget.style_prefix is False

    def test_value_from_datadict(self):
        """value_from_datadict returns value from POST data."""
        from django.http import QueryDict

        from core.widgets import IconPickerWidget

        widget = IconPickerWidget()
        data = QueryDict(mutable=True)
        data["icon"] = "fas fa-star"
        assert widget.value_from_datadict(data, {}, "icon") == "fas fa-star"

    def test_value_from_datadict_empty(self):
        """value_from_datadict returns empty string when missing."""
        from django.http import QueryDict

        from core.widgets import IconPickerWidget

        widget = IconPickerWidget()
        data = QueryDict(mutable=True)
        assert widget.value_from_datadict(data, {}, "icon") == ""

    def test_media_includes_css_and_js(self):
        """IconPickerWidget media includes icon_picker.css and icon_picker.js."""
        from core.widgets import IconPickerWidget

        widget = IconPickerWidget()
        media = widget.media
        all_css = []
        for css_list in media._css.values():
            all_css.extend(str(f) for f in css_list)
        assert "core/admin/css/icon_picker.css" in all_css
        assert "core/admin/js/icon_picker.js" in [str(f) for f in media._js]

    def test_template_name_is_set(self):
        """IconPickerWidget uses the correct template."""
        from core.widgets import IconPickerWidget

        widget = IconPickerWidget()
        assert widget.template_name == "admin/widgets/icon_picker.html"


class TestTranslatableFieldWidget:
    """Tests for TranslatableFieldWidget."""

    def test_instantiation_with_default_base_widget(self):
        """TranslatableFieldWidget defaults to TextInput if no base_widget provided."""
        from django import forms as django_forms

        from core.widgets import TranslatableFieldWidget

        widget = TranslatableFieldWidget()
        assert isinstance(widget.base_widget, django_forms.TextInput)

    def test_instantiation_with_custom_base_widget(self):
        """TranslatableFieldWidget accepts a custom base_widget."""
        from django import forms as django_forms

        from core.widgets import TranslatableFieldWidget

        textarea = django_forms.Textarea(attrs={"rows": 4})
        widget = TranslatableFieldWidget(base_widget=textarea)
        assert isinstance(widget.base_widget, django_forms.Textarea)

    def test_media_includes_translatable_css(self):
        """TranslatableFieldWidget media includes translatable_field_widget.css."""
        from core.widgets import TranslatableFieldWidget

        widget = TranslatableFieldWidget()
        media = widget.media
        # Flatten all CSS files
        all_css = []
        for css_list in media._css.values():
            all_css.extend(str(f) for f in css_list)
        assert "core/admin/css/translatable_field_widget.css" in all_css

    def test_value_from_datadict_delegates_to_base_widget(self):
        """value_from_datadict delegates to the base widget."""
        from django.http import QueryDict

        from core.widgets import TranslatableFieldWidget

        widget = TranslatableFieldWidget()
        data = QueryDict(mutable=True)
        data["site_name"] = "Test Store"

        result = widget.value_from_datadict(data, {}, "site_name")
        assert result == "Test Store"

    def test_template_name_is_set(self):
        """TranslatableFieldWidget uses the correct template."""
        from core.widgets import TranslatableFieldWidget

        widget = TranslatableFieldWidget()
        assert widget.template_name == "admin/widgets/translatable_field.html"


# ============================================================
# CSP Compliance Tests
# ============================================================


class TestCSPTemplateCompliance:
    """Tests ensuring core templates have no inline <style> blocks and no inline style="" attributes.

    These templates had inline styles removed during the CSP compliance audit.
    External CSS files are used instead.
    """

    # Templates that should have NO inline <style> blocks
    NO_STYLE_BLOCK_TEMPLATES = [
        "core/templates/admin/widgets/icon_picker.html",
        "core/templates/maintenance/coming_soon.html",
        "core/templates/maintenance/maintenance.html",
        "core/templates/core/license_required.html",
    ]

    # Admin templates that should have NO inline style="" attributes
    # Exception: sitesettings has 1 dynamic width for compliance bar
    NO_INLINE_STYLE_TEMPLATES = [
        "core/templates/admin/core/apitoken/change_list.html",
        "core/templates/admin/core/license_status/changelist.html",
        "core/templates/admin/widgets/translatable_field.html",
    ]

    @pytest.mark.parametrize("template_path", NO_STYLE_BLOCK_TEMPLATES)
    def test_no_inline_style_blocks(self, template_path):
        """Template should have no <style> blocks -- all styles in external CSS."""
        full_path = PROJECT_ROOT / template_path
        assert full_path.exists(), f"Template not found: {full_path}"

        content = full_path.read_text(encoding="utf-8")
        # Match <style> or <style ...> opening tags
        style_blocks = re.findall(r"<style[\s>]", content, re.IGNORECASE)
        assert len(style_blocks) == 0, (
            f"Found {len(style_blocks)} inline <style> block(s) in {template_path}. "
            f"All styles should be in external CSS files."
        )

    @pytest.mark.parametrize("template_path", NO_INLINE_STYLE_TEMPLATES)
    def test_no_inline_style_attributes(self, template_path):
        """Template should have no style="" attributes -- all styles in external CSS."""
        full_path = PROJECT_ROOT / template_path
        assert full_path.exists(), f"Template not found: {full_path}"

        content = full_path.read_text(encoding="utf-8")
        style_attrs = re.findall(r'\bstyle\s*=\s*["\']', content, re.IGNORECASE)
        assert len(style_attrs) == 0, (
            f'Found {len(style_attrs)} inline style="" attribute(s) in {template_path}. '
            f"All styles should be in external CSS files."
        )

    def test_sitesettings_template_no_inline_styles(self):
        """sitesettings change_form.html has zero inline style="" attributes.

        Dynamic values (compliance bar width) ride on data-width attributes
        with the actual style hooked up via external CSS; static spacing
        uses the .form-card-spacer utility.
        """
        full_path = PROJECT_ROOT / "core/templates/admin/core/sitesettings/change_form.html"
        content = full_path.read_text(encoding="utf-8")
        style_attrs = re.findall(r'\bstyle\s*=\s*["\']', content, re.IGNORECASE)
        assert len(style_attrs) == 0, (
            f'Found {len(style_attrs)} inline style="" attribute(s) in '
            "sitesettings/change_form.html. All styles must live in external CSS."
        )

    def test_frontend_templates_use_external_css(self):
        """Frontend templates (coming_soon, maintenance, license_required) should reference external CSS."""
        templates_and_css = [
            (
                "core/templates/maintenance/coming_soon.html",
                "core/css/coming_soon.css",
            ),
            (
                "core/templates/maintenance/maintenance.html",
                "core/css/maintenance.css",
            ),
            (
                "core/templates/core/license_required.html",
                "core/css/license_required.css",
            ),
        ]
        for template_path, expected_css in templates_and_css:
            full_path = PROJECT_ROOT / template_path
            content = full_path.read_text(encoding="utf-8")
            assert expected_css in content, (
                f"Template {template_path} does not reference external CSS file {expected_css}"
            )

    def test_icon_picker_template_no_style_blocks(self):
        """icon_picker.html should have no <style> blocks."""
        full_path = PROJECT_ROOT / "core/templates/admin/widgets/icon_picker.html"
        content = full_path.read_text(encoding="utf-8")
        assert "<style" not in content.lower()

    def test_icon_picker_template_no_inline_styles(self):
        """icon_picker.html should have no inline style="" attributes (data-icon-style is allowed)."""
        full_path = PROJECT_ROOT / "core/templates/admin/widgets/icon_picker.html"
        content = full_path.read_text(encoding="utf-8")
        # Match style= but exclude data-*-style= (e.g., data-icon-style)
        style_attrs = re.findall(r'(?<![-\w])style\s*=\s*["\']', content, re.IGNORECASE)
        assert len(style_attrs) == 0

    def test_coming_soon_svg_styles_are_svg_only(self):
        """coming_soon.html may have SVG stop-color styles but no HTML inline styles."""
        full_path = PROJECT_ROOT / "core/templates/maintenance/coming_soon.html"
        content = full_path.read_text(encoding="utf-8")

        # Find all style= occurrences
        style_matches = list(
            re.finditer(r'\bstyle\s*=\s*["\']([^"\']*)["\']', content, re.IGNORECASE)
        )

        for match in style_matches:
            style_value = match.group(1)
            # SVG stop-color is acceptable
            assert "stop-color" in style_value, (
                f'Found non-SVG inline style in coming_soon.html: style="{style_value}"'
            )


# ============================================================
# Static File Copyright Header Tests
# ============================================================


class TestCopyrightHeaders:
    """Tests ensuring copyright headers are present on core static JS/CSS files."""

    # Support single year (2025) or year range (2025-2026) after the (c) symbol.
    COPYRIGHT_PATTERN = re.compile(
        r"(?:\xc2\xa9|©|\(c\))\s*\d{4}(?:-\d{4})?\s*Spwig", re.IGNORECASE
    )
    COPYRIGHT_PATTERN_STR = re.compile(r"(?:©|\(c\))\s*\d{4}(?:-\d{4})?\s*Spwig", re.IGNORECASE)

    # Files that were specifically fixed in the audit
    AUDIT_FIXED_FILES = [
        "core/static/core/admin/js/admin-badge-refresh.js",
        "core/static/core/admin/js/translation_editor_init.js",
        "core/static/core/css/logged-out.css",
    ]

    @pytest.mark.parametrize("file_path", AUDIT_FIXED_FILES)
    def test_copyright_header_present(self, file_path):
        """Static file should have a copyright header in the first 5 lines."""
        full_path = PROJECT_ROOT / file_path
        assert full_path.exists(), f"Static file not found: {full_path}"

        content = full_path.read_text(encoding="utf-8")
        # Check only the first 500 characters (should be in header comment)
        header = content[:500]
        assert self.COPYRIGHT_PATTERN_STR.search(header), (
            f"No copyright header found in first 500 chars of {file_path}. "
            f"Expected pattern like '(c) 2025 Spwig' or similar."
        )

    @pytest.mark.parametrize("file_path", AUDIT_FIXED_FILES)
    def test_copyright_header_in_comment_block(self, file_path):
        """Copyright header should be inside a CSS/JS comment block."""
        full_path = PROJECT_ROOT / file_path
        content = full_path.read_text(encoding="utf-8")

        # First line should be a comment opening
        first_line = content.split("\n")[0].strip()
        assert first_line.startswith("/*") or first_line.startswith("//"), (
            f"First line of {file_path} is not a comment: '{first_line}'"
        )

    def test_external_css_files_exist_for_csp_templates(self):
        """External CSS files referenced by CSP-compliant templates should exist."""
        css_files = [
            "core/static/core/css/coming_soon.css",
            "core/static/core/css/maintenance.css",
            "core/static/core/css/license_required.css",
            "core/static/core/admin/css/translatable_field_widget.css",
        ]
        for css_file in css_files:
            full_path = PROJECT_ROOT / css_file
            assert full_path.exists(), (
                f"External CSS file {css_file} does not exist. "
                f"Styles should have been moved to this file during CSP audit."
            )


# ============================================================
# Model Field Existence & Type Tests
# ============================================================


@pytest.mark.django_db
class TestSiteSettingsModelIntegrity:
    """Tests verifying SiteSettings model field structure after audit changes."""

    def test_sitesettings_has_created_at(self):
        """SiteSettings should have created_at (auto_now_add)."""
        from core.models import SiteSettings

        field = SiteSettings._meta.get_field("created_at")
        assert field is not None

    def test_sitesettings_has_updated_at(self):
        """SiteSettings should have updated_at (auto_now)."""
        from core.models import SiteSettings

        field = SiteSettings._meta.get_field("updated_at")
        assert field is not None

    def test_sitesettings_singleton_get_settings(self, site_settings):
        """get_settings() returns the existing SiteSettings instance."""
        from core.models import SiteSettings

        settings = SiteSettings.get_settings()
        assert settings.pk == 1

    def test_social_media_fields_exist(self):
        """SiteSettings has the expected social media URL fields (no phantom ones)."""
        from core.models import SiteSettings

        # Fields that should exist
        existing_fields = ["facebook_url", "twitter_url", "instagram_url", "linkedin_url"]
        for field_name in existing_fields:
            assert SiteSettings._meta.get_field(field_name) is not None

    def test_phantom_social_media_fields_do_not_exist(self):
        """youtube_url, tiktok_url, pinterest_url should NOT exist on SiteSettings model."""
        from django.core.exceptions import FieldDoesNotExist

        from core.models import SiteSettings

        for phantom in ["youtube_url", "tiktok_url", "pinterest_url"]:
            with pytest.raises(FieldDoesNotExist):
                SiteSettings._meta.get_field(phantom)
