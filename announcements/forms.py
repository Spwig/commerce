from django import forms
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.widgets import CKEditor5Widget
from media_library.widgets import MediaLibrarySelectWidget
from core.widgets import TranslatableFieldWidget
from page_builder.models import RuleGroup

from .models import Announcement


class _RuleGroupChoiceField(forms.ModelMultipleChoiceField):
    """Use the description as label so intent is clear (e.g. 'Show only on mobile phones')."""
    def label_from_instance(self, obj):
        return obj.description or obj.name


class AnnouncementForm(forms.ModelForm):
    """Form for the Announcement admin with CKEditor and media library integration."""

    visibility_rules = _RuleGroupChoiceField(
        queryset=RuleGroup.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={'class': 'ann-visibility-select'}),
        required=False,
    )

    class Meta:
        model = Announcement
        fields = '__all__'
        widgets = {
            'title': TranslatableFieldWidget(
                base_widget=CKEditor5Widget(config_name='announcement_basic')
            ),
            'body': TranslatableFieldWidget(
                base_widget=CKEditor5Widget(config_name='announcement_basic')
            ),
            'link_text': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={
                    'maxlength': '100',
                    'class': 'vTextField',
                })
            ),
            'image': MediaLibrarySelectWidget(),
            'expires_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'vDateField'},
                format='%Y-%m-%dT%H:%M',
            ),
            'product_reference': forms.HiddenInput(),
            'category_reference': forms.HiddenInput(),
            'blog_post_reference': forms.HiddenInput(),
            'page_reference': forms.HiddenInput(),
        }
