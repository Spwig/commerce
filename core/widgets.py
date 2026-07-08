"""
Custom form widgets for enhanced UX in admin interface.
"""
import json

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class KeyValueWidget(forms.Widget):
    """
    Widget for editing JSONField dicts as key-value rows.

    Renders an interactive key-value pair editor with add/remove row
    functionality. Saves back as a JSON dict.

    Usage:
        from core.widgets import KeyValueWidget

        widgets = {
            'features': KeyValueWidget(key_label='Feature', value_label='Detail'),
            'specifications': KeyValueWidget(key_label='Specification', value_label='Value'),
        }
    """
    template_name = 'admin/widgets/key_value_widget.html'

    def __init__(self, key_label='Key', value_label='Value', attrs=None):
        self.key_label = key_label
        self.value_label = value_label
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if isinstance(value, str):
            try:
                pairs = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pairs = {}
        else:
            pairs = value or {}
        context['widget']['pairs'] = list(pairs.items()) if isinstance(pairs, dict) else []
        context['widget']['key_label'] = self.key_label
        context['widget']['value_label'] = self.value_label
        return context

    def value_from_datadict(self, data, files, name):
        keys = data.getlist(f'{name}_keys')
        values = data.getlist(f'{name}_values')
        result = {}
        for k, v in zip(keys, values):
            k = k.strip()
            if k:
                result[k] = v.strip()
        return json.dumps(result)

    @property
    def media(self):
        return forms.Media(
            css={'all': ('core/admin/css/key_value_widget.css',)},
            js=('core/admin/js/key_value_widget.js',)
        )


class SearchableSelectWidget(forms.Select):
    """
    Enhanced select widget with search functionality and Font Awesome icon support.

    Features:
    - Searchable dropdown with live filtering
    - Font Awesome icon display for each option
    - Clean single-element UI (replaces select entirely)
    - Keyboard navigation support
    - Theme-aware styling

    Usage:
        from core.widgets import SearchableSelectWidget
        from core.utils.locale_helpers import get_currency_icon

        widget = SearchableSelectWidget(
            icon_callback=get_currency_icon,
            attrs={'data-placeholder': 'Search currencies...'}
        )
    """

    def __init__(self, icon_callback=None, *args, **kwargs):
        """
        Initialize the searchable select widget.

        Args:
            icon_callback: Optional function that takes an option value and returns
                          a Font Awesome icon class (e.g., 'fa-dollar-sign').
                          If None, no icons will be displayed.
        """
        self.icon_callback = icon_callback
        super().__init__(*args, **kwargs)

        # Add searchable-select marker attribute
        if 'attrs' not in kwargs:
            self.attrs = {}
        self.attrs['data-searchable-select'] = ''

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """
        Override to add icon data attribute to each option element.

        The icon class is added as a data-icon attribute which will be parsed
        by the JavaScript SearchableSelect class to render icons in the dropdown.

        Args:
            name: Field name
            value: Option value
            label: Option display label
            selected: Whether option is selected
            index: Option index
            subindex: Sub-option index (for optgroups)
            attrs: Additional attributes

        Returns:
            Option dictionary with icon data attribute added
        """
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        # Add icon data attribute if callback provided and value exists
        if self.icon_callback and value:
            try:
                icon_class = self.icon_callback(value)
                if icon_class:
                    # Add Font Awesome icon class to data attribute
                    option['attrs']['data-icon'] = icon_class
                    # Use solid style by default (fas)
                    option['attrs']['data-icon-style'] = 'fas'
            except Exception:
                # Silently ignore icon callback errors
                # This ensures the widget still works even if icon mapping fails
                pass

        return option


class TranslatableFieldWidget(forms.Widget):
    """
    Widget that wraps a text input field with a translation button.

    This widget renders a text field (TextInput or Textarea) with a translate button
    next to it. When clicked, the button opens the translation editor modal allowing
    users to translate the field content into multiple languages.

    Features:
    - Renders base widget (TextInput or Textarea)
    - Adds translation button with Font Awesome language icon
    - Integrates with generic translation API
    - Uses TranslationEditor.js utility

    Usage:
        from core.widgets import TranslatableFieldWidget
        from django import forms

        # Wrap a TextInput
        widget = TranslatableFieldWidget(
            base_widget=forms.TextInput(attrs={'class': 'form-control'})
        )

        # Wrap a Textarea
        widget = TranslatableFieldWidget(
            base_widget=forms.Textarea(attrs={'rows': 4})
        )

    Note:
        Requires TranslatableAdminMixin to inject translation context into template.
    """

    template_name = 'admin/widgets/translatable_field.html'

    def __init__(self, base_widget=None, attrs=None):
        """
        Initialize the translatable field widget.

        Args:
            base_widget: The base widget to wrap (TextInput, Textarea, etc.)
                        Defaults to TextInput if not provided.
            attrs: Additional HTML attributes for the widget
        """
        super().__init__(attrs)

        # Use provided widget or default to TextInput
        if base_widget is None:
            base_widget = forms.TextInput()

        self.base_widget = base_widget

    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the widget using Django's template system.

        Args:
            name: Field name
            value: Field value
            attrs: HTML attributes
            renderer: Django template renderer

        Returns:
            Rendered HTML string
        """
        from django.template.loader import render_to_string
        from django_ckeditor_5.widgets import CKEditor5Widget

        # Get base widget HTML
        base_widget_html = self.base_widget.render(name, value, attrs)

        # Detect field type
        is_richtext = isinstance(self.base_widget, CKEditor5Widget)
        field_type = 'richtext' if is_richtext else 'text'

        # Get CKEditor config name if applicable
        ckeditor_config = None
        if is_richtext:
            ckeditor_config = getattr(self.base_widget, 'config_name', 'default')

        # Prepare context for template
        context = {
            'base_widget_html': base_widget_html,
            'field_name': name,
            'field_type': field_type,
            'is_richtext': is_richtext,
            'ckeditor_config': ckeditor_config,
        }

        # Render using template
        return render_to_string(self.template_name, context)

    def value_from_datadict(self, data, files, name):
        """
        Extract value from POST data using the base widget's method.

        Args:
            data: POST data dictionary
            files: FILES data dictionary
            name: Field name

        Returns:
            Extracted value
        """
        return self.base_widget.value_from_datadict(data, files, name)

    @property
    def media(self):
        """
        Return media assets required by this widget.

        Includes the base widget's media plus translation editor assets.
        """
        widget_media = forms.Media(
            css={'all': ('core/admin/css/translatable_field_widget.css',)}
        )
        return self.base_widget.media + widget_media


class IconPickerWidget(forms.Widget):
    """
    Universal Font Awesome icon picker with compact grid + full modal browser.

    Features:
    - Compact inline view with selected icon preview
    - Priority (suggested) icons displayed as a clickable grid
    - "Browse all icons" button opens a full modal with ~550 categorized icons
    - Search/filter by name and keywords in the modal
    - Works with both 'fa-star' and 'fas fa-star' value formats
    - Dispatches 'icon-picker:change' CustomEvent for form integration
    - Dark mode + responsive + CSP-compliant

    Usage:
        from core.widgets import IconPickerWidget

        # In form Meta.widgets (stores 'fas fa-star' format):
        'icon': IconPickerWidget(
            priority_icons=['fa-shopping-bag', 'fa-store', 'fa-tag'],
        )

        # For models storing 'fa-star' format (no prefix):
        'icon': IconPickerWidget(
            priority_icons=['fa-medal', 'fa-crown', 'fa-trophy'],
            style_prefix=False,
        )
    """
    template_name = 'admin/widgets/icon_picker.html'

    def __init__(self, priority_icons=None, style_prefix=True, attrs=None):
        """
        Args:
            priority_icons: List of FA class names (e.g., ['fa-truck', 'fa-box'])
                           shown prominently as suggested icons. Max 10 displayed.
            style_prefix: If True, widget stores 'fas fa-star' format.
                         If False, stores 'fa-star' format.
                         Must match the model field's expected format.
            attrs: Additional HTML attributes.
        """
        super().__init__(attrs)
        self.priority_icons = (priority_icons or [])[:10]
        self.style_prefix = style_prefix

    def get_context(self, name, value, attrs):
        from core.icon_registry import ICON_REGISTRY, get_registry_as_json

        context = super().get_context(name, value, attrs)

        # Resolve priority icons from registry with selection state
        priority_data = []
        for icon_class in self.priority_icons:
            bare_class = icon_class.split()[-1] if ' ' in icon_class else icon_class
            for entry in ICON_REGISTRY:
                if entry['class'] == bare_class:
                    icon_data = dict(entry)
                    # Determine if this priority icon matches current value
                    full_val = f"{entry['style']} {entry['class']}"
                    icon_data['is_selected'] = (
                        value == entry['class'] or value == full_val
                    )
                    priority_data.append(icon_data)
                    break

        # Resolve display label for current value
        display_label = value or ''
        if value:
            bare_val = value.split()[-1] if ' ' in value else value
            for entry in ICON_REGISTRY:
                if entry['class'] == bare_val:
                    display_label = entry['label']
                    break

        # Translations for JS
        translations = {
            'noIconSelected': str(_('No icon selected')),
            'chooseIcon': str(_('Choose an Icon')),
            'searchIcons': str(_('Search icons...')),
            'allCategories': str(_('All')),
            'noIconsFound': str(_('No icons found')),
            'iconCount': str(_('icons')),
        }

        context['widget'].update({
            'icon_value': value or '',
            'icon_display_label': display_label,
            'style_prefix': self.style_prefix,
            'priority_icons': priority_data,
            'icon_registry_json': mark_safe(json.dumps(
                get_registry_as_json(), ensure_ascii=False
            )),
            'translations_json': json.dumps(translations),
        })
        return context

    def value_from_datadict(self, data, files, name):
        return data.get(name, '')

    @property
    def media(self):
        return forms.Media(
            css={'all': ('core/admin/css/icon_picker.css',)},
            js=('core/admin/js/icon_picker.js',),
        )
