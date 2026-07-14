from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from design.models import DesignMixin
from design.theme_models import Theme

User = get_user_model()


class Page(DesignMixin):
    """Core page model for different page types in the storefront"""

    PAGE_TYPES = [
        ("home", _("Home Page")),
        ("category", _("Category Page")),
        ("product", _("Product Page")),
        ("cart", _("Shopping Cart")),
        ("checkout", _("Checkout")),
        ("about", _("About Page")),
        ("contact", _("Contact Page")),
        ("blog", _("Blog Post")),
        ("custom", _("Custom Page")),
    ]

    STATUS_CHOICES = [
        ("draft", _("Draft")),
        ("published", _("Published")),
        ("archived", _("Archived")),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, default="custom")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    # SEO and metadata
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=320, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="page_og_images",
        help_text=_("Open Graph image displayed when this page is shared on social media"),
    )
    seo_auto_generated = models.BooleanField(
        default=False, help_text=_("Automatically regenerate SEO content when page is saved")
    )

    # Preview thumbnail (auto-generated screenshot)
    preview_thumbnail = models.ImageField(
        upload_to="page_previews/",
        blank=True,
        null=True,
        help_text=_("Auto-generated preview thumbnail of this page"),
    )
    preview_thumbnail_updated_at = models.DateTimeField(
        null=True, blank=True, help_text=_("When the preview thumbnail was last captured")
    )

    # Translations (JSON-based system for merchant-translatable content)
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Translations for page content in different languages"),
    )

    # Page configuration
    is_default_for_type = models.BooleanField(
        default=False, help_text=_("Use as default page for this type")
    )
    is_system_page = models.BooleanField(
        default=False,
        help_text=_("System pages cannot be deleted and require confirmation to modify"),
    )
    requires_auth = models.BooleanField(default=False)
    cache_timeout = models.PositiveIntegerField(
        default=300, help_text=_("Cache timeout in seconds")
    )

    # Relations
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)

    # Header/Footer configuration
    header_template = models.ForeignKey(
        "design.HeaderTemplate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pages",
        help_text=_("Header template for this page. Leave empty to use site default."),
    )
    footer_template = models.ForeignKey(
        "design.FooterTemplate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pages",
        help_text=_("Footer template for this page. Leave empty to use site default."),
    )
    hide_header = models.BooleanField(default=False, help_text=_("Hide the header on this page"))
    hide_footer = models.BooleanField(default=False, help_text=_("Hide the footer on this page"))

    # Page-level design configuration
    page_design_config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Page-level design settings including typography, background, and layout"),
    )
    # Structure: {
    #   "layout_preset": "standard",  # theme-default, narrow, standard, wide, full, custom
    #   "custom_width": "1100px",  # Only used when layout_preset is "custom"
    #   "background": {...},  # Background editor value
    #   "typography": {...},  # Typography editor value
    #   "text_color": "...",  # Text color value
    #   "animation": {...}  # Animation settings
    # }

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["page_type", "status"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["status", "published_at"]),
        ]
        constraints = [
            # Only one default page per page type (allows multiple non-default pages)
            models.UniqueConstraint(
                fields=["page_type"],
                condition=models.Q(is_default_for_type=True),
                name="unique_default_per_page_type",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_page_type_display()})"

    def get_translated_field(self, field_name, language_code=None):
        """
        Get translated value for a field with fallback logic.

        Args:
            field_name: Name of the field (title, meta_title, etc.)
            language_code: Target language. If None, uses current language.

        Returns:
            Translated value or original field value as fallback.
        """
        from django.utils import translation

        if not language_code:
            language_code = translation.get_language()

        # Normalize language code (e.g., 'en-us' -> 'en')
        if language_code and "-" in language_code:
            base_code = language_code.split("-")[0]
        else:
            base_code = language_code

        # Check translations JSONField
        if self.translations:
            # Try exact match
            if language_code in self.translations:
                value = self.translations[language_code].get(field_name)
                if value:
                    return value
            # Try base language
            if base_code in self.translations:
                value = self.translations[base_code].get(field_name)
                if value:
                    return value

        # Fallback to original field
        return getattr(self, field_name, "")

    @property
    def translated_title(self):
        """Get translated title or fallback to original."""
        return self.get_translated_field("title") or self.title

    @property
    def translated_meta_title(self):
        """Get translated meta title or fallback to original."""
        return self.get_translated_field("meta_title") or self.meta_title

    @property
    def translated_meta_description(self):
        """Get translated meta description or fallback to original."""
        return self.get_translated_field("meta_description") or self.meta_description

    @property
    def translated_meta_keywords(self):
        """Get translated meta keywords or fallback to original."""
        return self.get_translated_field("meta_keywords") or self.meta_keywords

    @property
    def effective_theme(self):
        """
        Get the theme to use for this page.
        Returns page's specific theme if set, otherwise returns the site's active theme.
        """
        if self.theme:
            return self.theme

        from design.theme_utils import get_active_theme

        return get_active_theme()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Ensure only one default per page type
        if self.is_default_for_type:
            Page.objects.filter(page_type=self.page_type, is_default_for_type=True).exclude(
                pk=self.pk
            ).update(is_default_for_type=False)

        # Track if this is a new page
        is_new = self.pk is None

        super().save(*args, **kwargs)

        # Auto-create initial draft version for new pages
        if is_new and not kwargs.get("skip_versioning"):
            self.create_draft_version(description="Initial version")

    def get_sections_ordered(self):
        """Get page sections in display order"""
        return self.sections.filter(is_active=True).order_by("order")

    def create_draft_version(self, user=None, description=""):
        """Create a new draft version of this page"""
        # Get the latest version number
        last_version = self.versions.order_by("-version_number").first()
        version_number = (last_version.version_number + 1) if last_version else 1

        # Mark any existing draft as not current
        self.versions.filter(is_current_draft=True).update(is_current_draft=False)

        # Create initial empty snapshot
        # (will be populated immediately after creation)
        version = PageVersion.objects.create(
            page=self,
            version_number=version_number,
            content_snapshot={},  # Provide empty dict to satisfy NOT NULL constraint
            is_current_draft=True,
            created_by=user,
            change_description=description,
        )

        # Create snapshot with actual data
        version.create_snapshot()

        return version

    def publish_current_draft(self, user=None, notes=""):
        """Publish the current draft version"""
        current_draft = self.versions.filter(is_current_draft=True).first()

        if not current_draft:
            # If no draft, create one from current state
            current_draft = self.create_draft_version(user, "Auto-created for publish")

        # Mark any existing published version as not published
        self.versions.filter(is_published=True).update(is_published=False)

        # Mark draft as published
        current_draft.is_published = True
        current_draft.is_current_draft = False
        current_draft.save()

        # Update page status
        self.status = "published"
        from django.utils import timezone

        self.published_at = timezone.now()
        self.save()

        # Create publish history record
        PagePublishHistory.objects.create(
            page=self, published_version=current_draft, published_by=user, publish_notes=notes
        )

        return current_draft

    def get_published_version(self):
        """Get the currently published version"""
        return self.versions.filter(is_published=True).first()

    def get_draft_version(self):
        """Get the current draft version"""
        return self.versions.filter(is_current_draft=True).first()

    def revert_to_version(self, version_id, user=None):
        """Revert page to a specific version"""
        version = self.versions.get(id=version_id)

        # Restore the snapshot
        version.restore_snapshot()

        # Create a new draft from this state
        new_draft = self.create_draft_version(user, f"Reverted to version {version.version_number}")

        return new_draft

    def duplicate(self, new_title=None):
        """Create a copy of this page with all its sections and elements"""
        new_title = new_title or _("Copy of {}").format(self.title)
        new_page = Page.objects.create(
            title=new_title,
            page_type="custom",
            status="draft",
            meta_title=self.meta_title,
            meta_description=self.meta_description,
            template_variant=self.template_variant,
            css_classes=self.css_classes.copy(),
            layout_config=self.layout_config.copy(),
            style_overrides=self.style_overrides.copy(),
            responsive_config=self.responsive_config.copy(),
            theme=self.theme,
            header_template=self.header_template,
            footer_template=self.footer_template,
            hide_header=self.hide_header,
            hide_footer=self.hide_footer,
            page_design_config=self.page_design_config.copy() if self.page_design_config else {},
            created_by=self.created_by,
        )

        # Copy all sections
        for section in self.sections.all():
            section.duplicate(new_page)

        return new_page


# PageSection model has been removed - sections are no longer used
# Elements can be added directly to pages or nested in containers


class Element(DesignMixin):
    """Page elements (text, images, buttons, containers, etc.) that can be nested"""

    ELEMENT_TYPES = [
        # Basic Elements
        ("container", _("Container")),
        ("text", _("Text Block")),
        ("heading", _("Heading")),
        ("image", _("Image")),
        ("video", _("Video")),
        ("button", _("Button/Link")),
        ("spacer", _("Spacer")),
        ("divider", _("Divider")),
        ("icon", _("Icon")),
        ("map", _("Map")),
        ("social_links", _("Social Media Links")),
        ("countdown", _("Countdown Timer")),
        ("custom_html", _("Custom HTML")),
        # Product Elements
        ("product_card", _("Product Card")),
        ("product_list", _("Product List")),
        ("category_card", _("Category Card")),
        # Complex Elements (formerly sections)
        ("hero", _("Hero Section")),
        ("product_grid", _("Product Grid")),
        ("product_carousel", _("Product Carousel")),
        ("cta_banner", _("Call to Action Banner")),
        ("testimonials", _("Testimonials")),
        ("gallery", _("Image Gallery")),
        ("contact_form", _("Contact Form")),
        ("newsletter", _("Newsletter Signup")),
        ("form", _("Generic Form")),
    ]

    # Allow elements to belong to either a page directly OR a section (for backwards compatibility)
    page = models.ForeignKey(
        Page,
        related_name="elements",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Page this element belongs to"),
    )
    parent_element = models.ForeignKey(
        "self",
        related_name="child_elements",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Parent container element for nested elements"),
    )
    element_type = models.CharField(max_length=30, choices=ELEMENT_TYPES, default="text")
    name = models.CharField(max_length=200)

    # Content and configuration
    content = models.JSONField(default=dict, help_text=_("Element content and configuration data"))

    # Translations
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Translations for element content in different languages"),
    )

    # Layout
    order = models.PositiveIntegerField(default=0)
    column_span = models.PositiveIntegerField(default=12, help_text=_("Grid column span (1-12)"))
    column_offset = models.PositiveIntegerField(default=0, help_text=_("Grid column offset"))

    # Alignment and spacing
    text_align = models.CharField(
        max_length=10,
        default="left",
        choices=[
            ("left", _("Left")),
            ("center", _("Center")),
            ("right", _("Right")),
            ("justify", _("Justify")),
        ],
    )
    vertical_align = models.CharField(
        max_length=10,
        default="top",
        choices=[
            ("top", _("Top")),
            ("middle", _("Middle")),
            ("bottom", _("Bottom")),
        ],
    )

    # Visibility and behavior
    is_active = models.BooleanField(default=True)
    show_on_mobile = models.BooleanField(default=True)
    show_on_tablet = models.BooleanField(default=True)
    show_on_desktop = models.BooleanField(default=True)

    # Advanced visibility rules
    visibility_rules = models.ManyToManyField(
        "RuleGroup",
        blank=True,
        related_name="elements",
        help_text=_("Advanced visibility rules for conditional display"),
    )

    # Links and interactions
    link_url = models.URLField(blank=True)
    link_target = models.CharField(
        max_length=10,
        default="_self",
        choices=[
            ("_self", _("Same Window")),
            ("_blank", _("New Window")),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Element"
        verbose_name_plural = "Elements"
        indexes = [
            models.Index(fields=["page", "order"]),
            models.Index(fields=["parent_element", "order"]),
            models.Index(fields=["element_type"]),
        ]

    def get_translated_content(self, language_code=None):
        """
        Get translated content for the element with fallback logic.

        Args:
            language_code: Target language code. If None, uses current language.

        Returns:
            dict: Content with translations applied, or original content if no translation exists.
        """
        from django.utils import translation

        # Get the target language code
        if not language_code:
            language_code = translation.get_language()

        # Normalize language code (e.g., 'en-us' -> 'en')
        if language_code and "-" in language_code:
            base_code = language_code.split("-")[0]
        else:
            base_code = language_code

        # Start with original content
        translated_content = self.content.copy() if self.content else {}

        # Check if we have translations for this language
        if self.translations and language_code:
            # Try exact match first
            if language_code in self.translations:
                lang_translations = self.translations[language_code]
            # Try base language code
            elif base_code in self.translations:
                lang_translations = self.translations[base_code]
            else:
                lang_translations = None

            # Apply translations if found
            if lang_translations and isinstance(lang_translations, dict):
                # Filter out metadata fields
                for field_key, field_value in lang_translations.items():
                    if not field_key.startswith("_"):
                        translated_content[field_key] = field_value

        return translated_content

    def __str__(self):
        parent = (
            self.page.title
            if self.page
            else (self.parent_element.name if self.parent_element else "No parent")
        )
        return f"{self.name} ({self.get_element_type_display()}) - {parent}"

    def duplicate(self, new_page=None, new_parent=None):
        """Create a copy of this element for a new page or parent"""
        new_element = Element.objects.create(
            page=new_page or self.page,
            parent_element=new_parent or self.parent_element,
            element_type=self.element_type,
            name=self.name,
            content=self.content.copy(),
            order=self.order,
            column_span=self.column_span,
            column_offset=self.column_offset,
            text_align=self.text_align,
            vertical_align=self.vertical_align,
            is_active=self.is_active,
            show_on_mobile=self.show_on_mobile,
            show_on_tablet=self.show_on_tablet,
            show_on_desktop=self.show_on_desktop,
            link_url=self.link_url,
            link_target=self.link_target,
            template_variant=self.template_variant,
            css_classes=self.css_classes.copy(),
            layout_config=self.layout_config.copy(),
            style_overrides=self.style_overrides.copy(),
            responsive_config=self.responsive_config.copy(),
        )
        # Copy visibility rules
        new_element.visibility_rules.set(self.visibility_rules.all())
        return new_element

    def check_visibility(self, request=None, context=None):
        """
        Check if this element should be visible based on all conditions
        Returns True if visible, False otherwise
        """
        # First check basic active status
        if not self.is_active:
            return False

        # Check device-specific visibility
        if request:
            user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
            # Simple device detection (can be enhanced with user-agents library)
            is_mobile = any(x in user_agent for x in ["mobile", "android", "iphone"])
            is_tablet = "ipad" in user_agent or (
                "android" in user_agent and "mobile" not in user_agent
            )
            is_desktop = not is_mobile and not is_tablet

            if is_mobile and not self.show_on_mobile:
                return False
            if is_tablet and not self.show_on_tablet:
                return False
            if is_desktop and not self.show_on_desktop:
                return False

        # Check advanced visibility rules
        if self.visibility_rules.exists():
            # Build context if not provided
            if context is None and request:
                from .visibility_evaluator import ContextCollector

                collector = ContextCollector()
                context = collector.collect_context(request)

            # Evaluate all rule groups (OR logic between groups)
            for rule_group in self.visibility_rules.filter(is_active=True):
                if rule_group.evaluate(context):
                    return True

            # If we have rules but none matched, hide the element
            return False

        # No rules defined, element is visible
        return True


class PageTemplate(models.Model):
    """Saveable template configurations for entire pages"""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    page_type = models.CharField(max_length=20, choices=Page.PAGE_TYPES, default="custom")

    # Template data
    template_data = models.JSONField(
        help_text=_("Complete page configuration including sections and elements")
    )

    # Preview and metadata
    preview_image = models.ImageField(upload_to="template_previews/", blank=True, null=True)
    version = models.CharField(max_length=20, default="1.0.0")
    category = models.CharField(
        max_length=50,
        default="general",
        choices=[
            ("general", _("General")),
            ("ecommerce", _("E-commerce")),
            ("blog", _("Blog")),
            ("portfolio", _("Portfolio")),
            ("business", _("Business")),
            ("landing", _("Landing Page")),
        ],
    )

    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    # Author and dates
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-usage_count", "-created_at"]
        indexes = [
            models.Index(fields=["page_type", "category"]),
            models.Index(fields=["is_public", "-usage_count"]),
        ]

    def __str__(self):
        return f"{self.name} (v{self.version})"

    def create_page_from_template(self, title, user=None):
        """Create a new page instance from this template"""
        data = self.template_data

        # Create the page
        page = Page.objects.create(
            title=title,
            page_type=data.get("page_type", self.page_type),
            status="draft",
            meta_title=data.get("meta_title", ""),
            meta_description=data.get("meta_description", ""),
            template_variant=data.get("template_variant", "default"),
            css_classes=data.get("css_classes", {}),
            layout_config=data.get("layout_config", {}),
            style_overrides=data.get("style_overrides", {}),
            responsive_config=data.get("responsive_config", {}),
            created_by=user,
        )

        # Create elements (sections are no longer used - convert to container elements)
        for section_data in data.get("sections", []):
            # Convert old sections to container elements
            container = Element.objects.create(
                page=page,
                element_type="container",
                name=section_data.get("name", "Container"),
                order=section_data.get("order", 0),
                content={
                    "width": section_data.get("width", "full"),
                    "background_type": section_data.get("background_type", "none"),
                    "background_config": section_data.get("background_config", {}),
                },
                responsive_config=section_data.get("responsive_config", {}),
            )

            for element_data in section_data.get("elements", []):
                Element.objects.create(
                    parent_element=container,
                    element_type=element_data.get("element_type", "text"),
                    name=element_data.get("name", "Element"),
                    content=element_data.get("content", {}),
                    order=element_data.get("order", 0),
                    column_span=element_data.get("column_span", 12),
                    template_variant=element_data.get("template_variant", "default"),
                    css_classes=element_data.get("css_classes", {}),
                    layout_config=element_data.get("layout_config", {}),
                    style_overrides=element_data.get("style_overrides", {}),
                    responsive_config=element_data.get("responsive_config", {}),
                )

        # Update usage count
        self.usage_count += 1
        self.save(update_fields=["usage_count"])

        return page


# SectionTemplate removed - sections no longer exist
# class SectionTemplate(models.Model):
#     """Reusable section templates (deprecated - use ElementTemplate instead)"""
#     pass


class ElementTemplate(models.Model):
    """Pre-configured element templates"""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    element_type = models.CharField(max_length=30, choices=Element.ELEMENT_TYPES)

    # Template data
    template_data = models.JSONField(help_text=_("Element configuration and content"))

    # Preview and metadata
    preview_image = models.ImageField(upload_to="element_previews/", blank=True, null=True)
    category = models.CharField(max_length=50, default="general")
    tags = models.CharField(max_length=255, blank=True, help_text=_("Comma-separated tags"))

    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)

    # Author and dates
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-usage_count", "-created_at"]
        indexes = [
            models.Index(fields=["element_type", "category"]),
            models.Index(fields=["is_public", "-usage_count"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_element_type_display()})"


class PageVersion(models.Model):
    """Versioned snapshots of page content for draft/publish workflow"""

    page = models.ForeignKey(Page, related_name="versions", on_delete=models.CASCADE)
    version_number = models.PositiveIntegerField()

    # Complete snapshot of page and all its elements
    content_snapshot = models.JSONField(
        default=dict, help_text=_("Complete page configuration including all elements")
    )

    # Version metadata
    is_published = models.BooleanField(default=False)
    is_current_draft = models.BooleanField(default=False)

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Optional change description
    change_description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["-version_number"]
        unique_together = ["page", "version_number"]
        indexes = [
            models.Index(fields=["page", "-version_number"]),
            models.Index(fields=["page", "is_published"]),
            models.Index(fields=["page", "is_current_draft"]),
        ]

    def __str__(self):
        status = (
            "Published" if self.is_published else ("Draft" if self.is_current_draft else "Version")
        )
        return f"{self.page.title} - {status} v{self.version_number}"

    def create_snapshot(self):
        """Create a complete snapshot of the page state"""
        elements_data = []

        # Get all root elements (directly on page)
        root_elements = self.page.elements.filter(parent_element__isnull=True).order_by("order")

        def serialize_element(element):
            """Recursively serialize element and its children"""
            element_data = {
                "id": element.id,
                "element_type": element.element_type,
                "name": element.name,
                "content": element.content,
                "order": element.order,
                "column_span": element.column_span,
                "column_offset": element.column_offset,
                "text_align": element.text_align,
                "vertical_align": element.vertical_align,
                "is_active": element.is_active,
                "show_on_mobile": element.show_on_mobile,
                "show_on_tablet": element.show_on_tablet,
                "show_on_desktop": element.show_on_desktop,
                "link_url": element.link_url,
                "link_target": element.link_target,
                "template_variant": element.template_variant,
                "css_classes": element.css_classes,
                "layout_config": element.layout_config,
                "style_overrides": element.style_overrides,
                "responsive_config": element.responsive_config,
                "children": [],
            }

            # Recursively add children
            for child in element.child_elements.order_by("order"):
                element_data["children"].append(serialize_element(child))

            return element_data

        for element in root_elements:
            elements_data.append(serialize_element(element))

        # Create the complete snapshot
        self.content_snapshot = {
            "page": {
                "title": self.page.title,
                "slug": self.page.slug,
                "page_type": self.page.page_type,
                "meta_title": self.page.meta_title,
                "meta_description": self.page.meta_description,
                "meta_keywords": self.page.meta_keywords,
                "template_variant": self.page.template_variant,
                "css_classes": self.page.css_classes,
                "layout_config": self.page.layout_config,
                "style_overrides": self.page.style_overrides,
                "responsive_config": self.page.responsive_config,
                "requires_auth": self.page.requires_auth,
                "cache_timeout": self.page.cache_timeout,
                # Page-level configuration
                "header_template_id": self.page.header_template_id,
                "footer_template_id": self.page.footer_template_id,
                "hide_header": self.page.hide_header,
                "hide_footer": self.page.hide_footer,
                "page_design_config": self.page.page_design_config,
            },
            "elements": elements_data,
            "version": self.version_number,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        self.save(update_fields=["content_snapshot"])

    def restore_snapshot(self):
        """Restore the page to this version's state"""
        if not self.content_snapshot:
            raise ValueError("No snapshot available for this version")

        snapshot = self.content_snapshot
        page_data = snapshot.get("page", {})

        # Update page fields
        for field in [
            "title",
            "slug",
            "page_type",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "template_variant",
            "css_classes",
            "layout_config",
            "style_overrides",
            "responsive_config",
            "requires_auth",
            "cache_timeout",
            "header_template_id",
            "footer_template_id",
            "hide_header",
            "hide_footer",
            "page_design_config",
        ]:
            if field in page_data:
                setattr(self.page, field, page_data[field])

        self.page.save()

        # Clear existing elements
        self.page.elements.all().delete()

        # Recreate elements from snapshot
        def create_element(element_data, parent=None):
            """Recursively create elements"""
            children = element_data.pop("children", [])
            element_data.pop("id", None)  # Don't reuse old IDs

            element = Element.objects.create(
                page=self.page if not parent else None, parent_element=parent, **element_data
            )

            for child_data in children:
                create_element(child_data, parent=element)

            return element

        for element_data in snapshot.get("elements", []):
            create_element(element_data.copy())


class VisibilityRule(models.Model):
    """
    Advanced visibility rules for page elements
    Allows conditional display based on various criteria
    """

    # Rule Types
    RULE_TYPES = [
        # Geographic
        ("geo_country", _("Country")),
        ("geo_region", _("Region/State")),
        ("geo_city", _("City")),
        ("geo_timezone", _("Time Zone")),
        # User & Authentication
        ("user_logged_in", _("Logged In Status")),
        ("user_group", _("User Group")),
        ("user_segment", _("Customer Segment")),
        ("user_lifetime_value", _("Customer Lifetime Value")),
        ("user_order_count", _("Order Count")),
        # Device & Technical
        ("device_type", _("Device Type")),
        ("browser", _("Browser")),
        ("operating_system", _("Operating System")),
        ("screen_size", _("Screen Size")),
        ("connection_speed", _("Connection Speed")),
        # Time-Based
        ("date_range", _("Date Range")),
        ("time_range", _("Time of Day")),
        ("day_of_week", _("Day of Week")),
        ("business_hours", _("Business Hours")),
        # Behavioral
        ("first_visit", _("First Time Visitor")),
        ("visit_count", _("Visit Count")),
        ("page_views", _("Page Views in Session")),
        ("time_on_site", _("Time on Site")),
        ("referrer", _("Referrer Source")),
        ("utm_campaign", _("UTM Campaign")),
        # E-commerce
        ("cart_value", _("Cart Value")),
        ("cart_items", _("Cart Item Count")),
        ("has_purchased", _("Has Purchased Before")),
        ("abandoned_cart", _("Has Abandoned Cart")),
        ("wishlist_items", _("Has Wishlist Items")),
        # Language & Localization
        ("browser_language", _("Browser Language")),
        ("selected_language", _("Selected Language")),
        ("selected_currency", _("Selected Currency")),
    ]

    # Operators
    OPERATORS = [
        ("equals", _("Equals")),
        ("not_equals", _("Not Equals")),
        ("contains", _("Contains")),
        ("not_contains", _("Does Not Contain")),
        ("greater_than", _("Greater Than")),
        ("less_than", _("Less Than")),
        ("in_list", _("In List")),
        ("not_in_list", _("Not In List")),
        ("is_true", _("Is True")),
        ("is_false", _("Is False")),
        ("between", _("Between")),
        ("regex", _("Matches Regex")),
    ]

    # Logic Operators for combining rules
    LOGIC_OPERATORS = [
        ("AND", _("All conditions must match")),
        ("OR", _("Any condition matches")),
    ]

    name = models.CharField(max_length=200, help_text=_("Descriptive name for this rule"))

    description = models.TextField(
        blank=True, help_text=_("Optional description of what this rule does")
    )

    # Rule configuration
    rule_type = models.CharField(
        max_length=50, choices=RULE_TYPES, help_text=_("Type of condition to check")
    )

    operator = models.CharField(
        max_length=20, choices=OPERATORS, default="equals", help_text=_("How to compare the value")
    )

    # Value to compare against (stored as JSON for flexibility)
    value = models.JSONField(default=dict, help_text=_("Value or values to compare against"))

    # Additional configuration
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(
        default=0, help_text=_("Higher priority rules are evaluated first")
    )

    # Caching
    cache_duration = models.IntegerField(
        default=300, help_text=_("How long to cache rule evaluation results (seconds)")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Visibility Rule")
        verbose_name_plural = _("Visibility Rules")
        ordering = ["-priority", "name"]
        indexes = [
            models.Index(fields=["rule_type", "is_active"]),
            models.Index(fields=["priority", "is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()})"

    def evaluate(self, context):
        """
        Evaluate this rule against the provided context
        Returns True if the rule matches, False otherwise
        """
        from .visibility_evaluator import RuleEvaluator

        evaluator = RuleEvaluator()
        return evaluator.evaluate_single_rule(self, context)


class RuleGroup(models.Model):
    """
    Groups multiple visibility rules with logic operators
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # How to combine rules in this group
    logic_operator = models.CharField(
        max_length=3,
        choices=VisibilityRule.LOGIC_OPERATORS,
        default="AND",
        help_text=_("How to combine rules in this group"),
    )

    # Rules in this group
    rules = models.ManyToManyField(VisibilityRule, related_name="groups", through="RuleGroupMember")

    # Nested groups support
    parent_group = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="child_groups"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Rule Group")
        verbose_name_plural = _("Rule Groups")
        ordering = ["name"]

    def __str__(self):
        operator_display = "ALL" if self.logic_operator == "AND" else "ANY"
        return f"{self.name} ({operator_display})"

    def evaluate(self, context):
        """
        Evaluate all rules in this group against the context
        """
        from .visibility_evaluator import RuleEvaluator

        evaluator = RuleEvaluator()
        return evaluator.evaluate_rule_group(self, context)


class RuleGroupMember(models.Model):
    """
    Through model for rule group membership with ordering
    """

    rule_group = models.ForeignKey(RuleGroup, on_delete=models.CASCADE)
    rule = models.ForeignKey(VisibilityRule, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ["rule_group", "rule"]

    def __str__(self):
        return f"{self.rule_group} → {self.rule} (order={self.order})"


class PagePublishHistory(models.Model):
    """Track page publish events for audit and rollback"""

    page = models.ForeignKey(Page, related_name="publish_history", on_delete=models.CASCADE)
    published_version = models.ForeignKey(PageVersion, on_delete=models.SET_NULL, null=True)

    # Publishing metadata
    published_at = models.DateTimeField(auto_now_add=True)
    published_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Optional rollback tracking
    rolled_back_at = models.DateTimeField(null=True, blank=True)
    rolled_back_by = models.ForeignKey(
        User, related_name="rollbacks", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Publishing notes
    publish_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["page", "-published_at"]),
        ]

    def __str__(self):
        return f"{self.page.title} - Published {self.published_at}"
