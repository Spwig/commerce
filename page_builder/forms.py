"""
Forms for page_builder app.

Provides custom forms with translatable field widgets for the Page model.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from core.widgets import TranslatableFieldWidget
from media_library.widgets import MediaLibrarySelectWidget
from .models import Page


class PageForm(forms.ModelForm):
    """
    Custom form for Page model with translatable fields.

    Uses TranslatableFieldWidget to wrap translatable text fields with
    translation buttons that integrate with the Translation Service.
    """

    title = forms.CharField(
        max_length=200,
        label=_('Title'),
        widget=TranslatableFieldWidget(
            base_widget=forms.TextInput(attrs={
                'class': 'vTextField',
                'style': 'width: 99%;'
            })
        )
    )

    meta_title = forms.CharField(
        max_length=200,
        required=False,
        label=_('Meta Title'),
        help_text=_('SEO title for search engines. Leave blank to use page title.'),
        widget=TranslatableFieldWidget(
            base_widget=forms.TextInput(attrs={
                'class': 'vTextField',
                'style': 'width: 99%;'
            })
        )
    )

    meta_description = forms.CharField(
        max_length=320,
        required=False,
        label=_('Meta Description'),
        help_text=_('SEO description for search engines (max 320 characters).'),
        widget=TranslatableFieldWidget(
            base_widget=forms.Textarea(attrs={
                'rows': 3,
                'class': 'vLargeTextField',
                'style': 'width: 99%;'
            })
        )
    )

    meta_keywords = forms.CharField(
        max_length=255,
        required=False,
        label=_('Meta Keywords'),
        help_text=_('Comma-separated keywords for SEO.'),
        widget=TranslatableFieldWidget(
            base_widget=forms.TextInput(attrs={
                'class': 'vTextField',
                'style': 'width: 99%;'
            })
        )
    )

    class Meta:
        model = Page
        fields = '__all__'
        exclude = ['created_by', 'translations']  # Auto-set by admin, managed by translation system
        widgets = {
            'og_image': MediaLibrarySelectWidget(selection_mode='single'),
        }
        help_texts = {
            'og_image': _(
                'Open Graph image displayed when this page is shared on social media '
                '(Facebook, LinkedIn, Twitter, etc.). Recommended size: 1200x630 pixels.'
            ),
        }
