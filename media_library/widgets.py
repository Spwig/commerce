from django import forms
from django.forms.renderers import get_default_renderer
from django.urls import reverse
from django.utils.safestring import mark_safe


class MediaLibraryWidget(forms.ClearableFileInput):
    """
    A widget for selecting images from the media library instead of uploading files directly
    """

    template_name = "media_library/widgets/media_library_widget.html"

    def __init__(self, attrs=None):
        default_attrs = {
            "class": "media-library-input",
            "style": "display: none;",  # Hide the default file input
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        """Return the URL of the selected image if available"""
        # Check if value exists and has a file before accessing url
        # Django's FieldFile has a 'url' attribute but raises ValueError if no file
        if value:
            try:
                if hasattr(value, "url"):
                    return value.url
            except ValueError:
                # No file associated with the field
                return None
        return value if value else None

    def render(self, name, value, attrs=None, renderer=None):
        """Render the media library widget"""
        if renderer is None:
            renderer = get_default_renderer()

        context = {
            "widget": {
                "name": name,
                "value": self.format_value(value),
                "attrs": attrs or {},
                "is_hidden": self.is_hidden,
                "required": self.is_required,
                "template_name": self.template_name,
            },
            "field_name": name,
            "current_value": self.format_value(value),
            "gallery_url": reverse("admin:media_library_gallery"),
            "api_url": "/api/media/assets/",
        }

        return mark_safe(renderer.render(self.template_name, context))

    @property
    def media(self):
        """Include necessary CSS and JavaScript files"""
        return forms.Media(
            css={
                "all": [
                    "media_library/css/media-library.css",
                    "media_library/css/upload-queue.css",
                    "utilities/base/current/utility_base.css",
                ]
            },
            js=[
                "media_library/js/upload-queue.js",
                "media_library/js/media-library.js",
            ],
        )


class MediaLibrarySelectWidget(forms.Widget):
    """
    A simplified widget that shows a button to open the media library.
    Used for ForeignKey fields to MediaAsset - NOT for file uploads.
    Extends forms.Widget (not ClearableFileInput) to avoid file upload interference.
    """

    template_name = "media_library/widgets/media_library_select.html"

    def __init__(self, attrs=None, selection_mode="single"):
        self.selection_mode = selection_mode
        default_attrs = {
            "class": "media-library-select",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()

        # Handle MediaAsset objects vs IDs
        import uuid

        from media_library.models import MediaAsset

        display_value = ""  # The ID to store in hidden input
        image_url = ""  # The URL to display in preview

        if value:
            # If value is a MediaAsset object, get its ID and URL
            if isinstance(value, MediaAsset):
                display_value = str(value.id)
                # Get the best available URL for display
                if value.webp_file:
                    image_url = value.webp_file.url
                elif value.original_file:
                    image_url = value.original_file.url
            # If value is a UUID object, convert to string
            elif isinstance(value, (uuid.UUID, str, int)):
                display_value = str(value)
                try:
                    media_asset = MediaAsset.objects.get(pk=value)
                    if media_asset.webp_file:
                        image_url = media_asset.webp_file.url
                    elif media_asset.original_file:
                        image_url = media_asset.original_file.url
                except MediaAsset.DoesNotExist:
                    pass

        # Build auto-save configuration from attrs if provided
        auto_save_config = {
            "url": self.attrs.get("auto_save_url", ""),
            "app_label": self.attrs.get("auto_save_app", ""),
            "model_name": self.attrs.get("auto_save_model", ""),
            "pk": self.attrs.get("auto_save_pk", ""),
            "field": self.attrs.get("auto_save_field", ""),
        }
        # Only include auto_save if URL is configured
        has_auto_save = bool(auto_save_config["url"])

        context = {
            "widget": {
                "name": name,
                "value": display_value,
                "attrs": attrs or {},
                "is_hidden": self.is_hidden,
                "required": self.is_required,
            },
            "field_name": name,
            "current_value": display_value,
            "image_url": image_url,
            "selection_mode": self.selection_mode,
            "gallery_url": reverse("admin:media_library_gallery"),
            "auto_save": auto_save_config if has_auto_save else None,
        }

        return mark_safe(renderer.render(self.template_name, context))

    def value_from_datadict(self, data, files, name):
        """
        Get the MediaAsset ID from POST data.
        The widget submits the MediaAsset UUID in a hidden input field.
        Returns None if empty (for proper ForeignKey null handling).
        """
        value = data.get(name)
        # Return None instead of empty string for ForeignKey compatibility
        return value if value else None

    @property
    def media(self):
        return forms.Media(
            css={
                "all": [
                    "media_library/css/media-library.css",
                    "media_library/css/upload-queue.css",
                    "utilities/base/current/utility_base.css",
                ]
            },
            js=[
                "media_library/js/upload-queue.js",
                "media_library/js/media-library.js",
                "media_library/js/media-library-select-widget.js",
            ],
        )
