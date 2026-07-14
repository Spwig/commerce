from django import forms
from django.utils.translation import gettext_lazy as _

from .models import MediaAsset


class TranslatableCharField(forms.CharField):
    """Custom widget for translatable text fields"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update(
            {"data-translatable": "true", "class": "vTextField translatable-field"}
        )


class TranslatableTextField(forms.CharField):
    """Custom widget for translatable textarea fields"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.Textarea)
        super().__init__(*args, **kwargs)
        self.widget.attrs.update(
            {"data-translatable": "true", "class": "vLargeTextField translatable-field"}
        )


class MediaAssetForm(forms.ModelForm):
    """Form for editing media assets with translation support"""

    title = TranslatableCharField(
        max_length=255, label=_("Title"), help_text=_("The title of the media asset")
    )

    alt_text = TranslatableCharField(
        max_length=255,
        required=False,
        label=_("Alt Text"),
        help_text=_("Alternative text for accessibility"),
    )

    description = TranslatableTextField(
        required=False,
        label=_("Description"),
        help_text=_("Detailed description of the media asset"),
    )

    class Meta:
        model = MediaAsset
        fields = [
            "title",
            "alt_text",
            "description",
            "folder",
            "tags",
            "focal_point_x",
            "focal_point_y",
            "is_public",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add field names as data attributes for translation editor
        for field_name in ["title", "alt_text", "description"]:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["data-field-name"] = field_name

        # Add media asset ID for API calls
        if self.instance and self.instance.pk:
            for field in self.fields.values():
                field.widget.attrs["data-media-id"] = str(self.instance.pk)
