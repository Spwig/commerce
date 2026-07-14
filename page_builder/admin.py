from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from core.admin_mixins import TranslatableAdminMixin
from seo_generator.admin_mixin import SEOGeneratorAdminMixin

from .forms import PageForm
from .models import (
    Element,
    ElementTemplate,
    Page,
    PageTemplate,
    RuleGroup,
    RuleGroupMember,
    VisibilityRule,
)


class ElementInline(admin.TabularInline):
    model = Element
    extra = 0
    fields = [
        "name",
        "element_type",
        "order",
        "column_span",
        "is_active",
        "show_on_mobile",
        "show_on_tablet",
        "show_on_desktop",
    ]
    readonly_fields = []
    ordering = ["order"]

    # PageSectionInline was removed — sections no longer used; elements are added
    # directly to pages or nested in containers.
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("page")


@admin.register(Page)
class PageAdmin(TranslatableAdminMixin, SEOGeneratorAdminMixin, admin.ModelAdmin):
    """
    Admin for Page model with JSON-based translations.

    Uses TranslatableAdminMixin for merchant-translatable content fields
    (title, meta_title, meta_description, meta_keywords) instead of
    django-modeltranslation.
    """

    form = PageForm
    change_list_template = "admin/page_builder/page/change_list.html"
    change_form_template = "admin/page_builder/page/change_form.html"

    # Auto-generate slug from title
    prepopulated_fields = {"slug": ("title",)}

    list_display = [
        "title",
        "page_type",
        "status_display",
        "theme_display",
        "elements_count",
        "is_default_for_type",
        "system_page_display",
        "preview_link",
        "updated_at",
    ]
    list_filter = [
        "page_type",
        "status",
        "is_default_for_type",
        "is_system_page",
        "requires_auth",
        "theme",
        "created_at",
    ]
    search_fields = ["title", "slug", "meta_title", "meta_description"]
    readonly_fields = ["created_by", "created_at", "updated_at", "published_at", "preview_link"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("title", "slug", "page_type", "status")}),
        (
            _("Content & Design"),
            {"fields": ("theme", "template_variant", "is_default_for_type", "is_system_page")},
        ),
        (
            _("SEO & Metadata"),
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                    "meta_keywords",
                    "og_image",
                    "seo_auto_generated",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Advanced Settings"),
            {"fields": ("requires_auth", "cache_timeout"), "classes": ("collapse",)},
        ),
        (
            _("Design Customization"),
            {
                "fields": ("css_classes", "layout_config", "style_overrides", "responsive_config"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Publishing Info"),
            {
                "fields": (
                    "created_by",
                    "created_at",
                    "updated_at",
                    "published_at",
                    "preview_link",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = []  # Sections removed

    actions = [
        "publish_pages",
        "unpublish_pages",
        "duplicate_pages",
        "create_template_from_pages",
        "regenerate_thumbnails",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("theme", "created_by")
            .prefetch_related("elements")
        )

    def changelist_view(self, request, extra_context=None):
        """Add custom context for filters"""
        from design.theme_models import Theme

        extra_context = extra_context or {}
        extra_context["page_types"] = Page.PAGE_TYPES
        extra_context["themes"] = Theme.objects.filter(is_active=True).order_by("name")
        # Check for queued thumbnail captures (bulk action or single-page save)
        capture_queue = request.session.pop("_capture_thumbnail_queue", None)
        # Also pick up single-page capture from save_model (when user clicks "Save" → changelist)
        single_page_id = request.session.pop("_capture_thumbnail_page_id", None)
        single_page_slug = request.session.pop("_capture_thumbnail_page_slug", None)
        if single_page_id and single_page_slug:
            single_item = [{"id": single_page_id, "slug": single_page_slug}]
            capture_queue = (capture_queue or []) + single_item
        if capture_queue:
            extra_context["capture_thumbnail_queue"] = capture_queue
        return super().changelist_view(request, extra_context=extra_context)

    def status_display(self, obj):
        status_colors = {"draft": "#ffc107", "published": "#28a745", "archived": "#6c757d"}
        color = status_colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_status_display()
        )

    status_display.short_description = _("Status")

    def theme_display(self, obj):
        if obj.theme:
            return format_html('<span style="color: #007bff;">🎨 {}</span>', obj.theme.name)
        return format_html('<span style="color: #6c757d;">{}</span>', _("Default"))

    theme_display.short_description = _("Theme")

    def system_page_display(self, obj):
        """Display system page status with visual indicator."""
        if obj.is_system_page:
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 4px; '
                "background: #f0f7ff; color: #0066cc; padding: 2px 8px; "
                'border-radius: 4px; font-size: 11px; font-weight: 600;" '
                'title="This is a system page. Changes may affect core store functionality.">'
                '<i class="fas fa-lock" style="font-size: 10px;"></i> {}</span>',
                _("System"),
            )
        return format_html('<span style="color: #6c757d;">—</span>')

    system_page_display.short_description = _("Type")

    def elements_count(self, obj):
        count = obj.elements.count()
        if count > 0:
            return format_html('<span style="color: #17a2b8;">{} elements</span>', count)
        return format_html('<span style="color: #dc3545;">No elements</span>')

    elements_count.short_description = "Elements"

    def preview_link(self, obj):
        if obj.pk:
            from django.urls import reverse

            preview_url = reverse("page_builder_admin:page_preview", kwargs={"slug": obj.slug})
            builder_url = reverse("page_builder_admin:visual_builder", kwargs={"page_id": obj.pk})
            return format_html(
                '<div style="display: flex; gap: 8px; align-items: center;">'
                '<a href="{}" target="_blank" title="Preview Page" style="'
                "display: inline-flex; align-items: center; justify-content: center; "
                "width: 32px; height: 32px; border-radius: 6px; background: #28a745; "
                "color: white; text-decoration: none; font-size: 14px; "
                "transition: all 0.2s ease; border: none;"
                '" onmouseover="this.style.background=\'#218838\'" onmouseout="this.style.background=\'#28a745\'">🔍</a>'
                '<a href="{}" target="_blank" title="Visual Page Builder" style="'
                "display: inline-flex; align-items: center; justify-content: center; "
                "width: 32px; height: 32px; border-radius: 6px; background: #3b82f6; "
                "color: white; text-decoration: none; font-size: 14px; "
                "transition: all 0.2s ease; border: none;"
                '" onmouseover="this.style.background=\'#2563eb\'" onmouseout="this.style.background=\'#3b82f6\'">✨</a>'
                "</div>",
                preview_url,
                builder_url,
            )
        return _("Save page first")

    preview_link.short_description = _("Actions")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        # Flag thumbnail capture for the response page
        if obj.slug:
            request.session["_capture_thumbnail_page_id"] = obj.pk
            request.session["_capture_thumbnail_page_slug"] = obj.slug

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        # Check if thumbnail capture was requested after save
        page_id = request.session.pop("_capture_thumbnail_page_id", None)
        page_slug = request.session.pop("_capture_thumbnail_page_slug", None)
        if page_id and page_slug:
            extra_context["capture_thumbnail_page_id"] = page_id
            extra_context["capture_thumbnail_page_slug"] = page_slug
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        """Auto-create a draft page and redirect to the visual builder."""
        from django.core.exceptions import PermissionDenied

        if not self.has_add_permission(request):
            raise PermissionDenied

        # Generate unique slug
        base_slug = slugify("Untitled Page")
        slug = base_slug
        counter = 2
        while Page.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        page = Page.objects.create(
            title=_("Untitled Page"),
            slug=slug,
            page_type="custom",
            status="draft",
            created_by=request.user,
        )

        builder_url = reverse("page_builder_admin:visual_builder", kwargs={"page_id": page.pk})
        return redirect(builder_url)

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of system pages that are assigned to site settings.
        """
        if obj is None:
            return super().has_delete_permission(request, obj)

        # Check if this is a system page
        if obj.is_system_page:
            # Check if it's assigned to any role in site settings
            from core.models import SiteSettings

            try:
                settings = SiteSettings.get_settings()
                page_fields = [
                    "home_page",
                    "privacy_page",
                    "terms_page",
                    "cookie_page",
                    "shipping_page",
                    "returns_page",
                    "error_404_page",
                    "error_500_page",
                ]
                for field in page_fields:
                    if getattr(settings, field, None) == obj:
                        return False
            except Exception:
                pass

        return super().has_delete_permission(request, obj)

    def delete_model(self, request, obj):
        """
        Additional check before deletion with informative error messages.
        """
        from django.contrib import messages

        from core.models import SiteSettings

        # Check if this is a system page that's assigned
        if obj.is_system_page:
            try:
                settings = SiteSettings.get_settings()
                field_labels = {
                    "home_page": _("Home Page"),
                    "privacy_page": _("Privacy Policy"),
                    "terms_page": _("Terms of Use"),
                    "cookie_page": _("Cookie Policy"),
                    "shipping_page": _("Shipping Information"),
                    "returns_page": _("Returns Policy"),
                    "error_404_page": _("404 Error Page"),
                    "error_500_page": _("500 Error Page"),
                }
                for field, label in field_labels.items():
                    if getattr(settings, field, None) == obj:
                        messages.error(
                            request,
                            _(
                                "Cannot delete this page: It is currently assigned as the {} in Site Settings. "
                                "Please assign a different page first."
                            ).format(label),
                        )
                        return
            except Exception:
                pass

        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """
        Prevent bulk deletion of assigned system pages.
        """
        from django.contrib import messages

        from core.models import SiteSettings

        try:
            settings = SiteSettings.get_settings()
            page_fields = [
                "home_page",
                "privacy_page",
                "terms_page",
                "cookie_page",
                "shipping_page",
                "returns_page",
                "error_404_page",
                "error_500_page",
            ]

            # Find pages that are assigned
            assigned_pages = set()
            for field in page_fields:
                page = getattr(settings, field, None)
                if page:
                    assigned_pages.add(page.pk)

            # Filter out assigned system pages
            protected = queryset.filter(pk__in=assigned_pages, is_system_page=True)
            if protected.exists():
                protected_titles = list(protected.values_list("title", flat=True))
                messages.warning(
                    request,
                    _(
                        "The following pages could not be deleted because they are assigned in Site Settings: {}"
                    ).format(", ".join(protected_titles)),
                )
                # Only delete non-protected pages
                queryset = queryset.exclude(pk__in=assigned_pages)

        except Exception:
            pass

        super().delete_queryset(request, queryset)

    def publish_pages(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(status="published", published_at=timezone.now())
        self.message_user(request, _(f"Published {updated} pages."))

    publish_pages.short_description = _("Publish selected pages")

    def unpublish_pages(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, _(f"Unpublished {updated} pages."))

    unpublish_pages.short_description = _("Unpublish selected pages")

    def duplicate_pages(self, request, queryset):
        count = 0
        for page in queryset:
            page.duplicate()
            count += 1
        self.message_user(request, _(f"Duplicated {count} pages."))

    duplicate_pages.short_description = _("Duplicate selected pages")

    def create_template_from_pages(self, request, queryset):
        # This would open a form to create templates from selected pages
        selected = list(queryset.values_list("id", flat=True))
        return redirect(
            f"/admin/page_builder/page/create-templates/?pages={','.join(map(str, selected))}"
        )

    create_template_from_pages.short_description = _("Create templates from pages")

    def regenerate_thumbnails(self, request, queryset):
        """Queue thumbnail regeneration for selected pages."""
        pages_to_capture = []
        for page in queryset.filter(slug__isnull=False).exclude(slug="")[:10]:
            pages_to_capture.append({"id": page.pk, "slug": page.slug})
        if pages_to_capture:
            request.session["_capture_thumbnail_queue"] = pages_to_capture
            self.message_user(
                request,
                _(
                    "Queued %(count)d page(s) for thumbnail regeneration. Thumbnails will be captured in the background."
                )
                % {"count": len(pages_to_capture)},
            )
        else:
            self.message_user(request, _("No pages with slugs found to capture."), level="warning")

    regenerate_thumbnails.short_description = _("Regenerate preview thumbnails")


# PageSection admin removed - model no longer exists
"""
class PageSectionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'page', 'order', 'width',
        'elements_count', 'is_active', 'responsive_display'
    ]
    list_filter = [
        'width', 'background_type', 'is_active',
        'show_on_mobile', 'show_on_tablet', 'show_on_desktop', 'animation_type'
    ]
    search_fields = ['name', 'page__title']
    ordering = ['page', 'order']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('page', 'name', 'order')
        }),
        (_('Layout & Appearance'), {
            'fields': ('width', 'background_type', 'background_config')
        }),
        (_('Responsive Settings'), {
            'fields': ('show_on_mobile', 'show_on_tablet', 'show_on_desktop'),
            'classes': ('collapse',)
        }),
        (_('Animation & Effects'), {
            'fields': ('animation_type', 'animation_delay'),
            'classes': ('collapse',)
        }),
        (_('Design Customization'), {
            'fields': ('template_variant', 'css_classes', 'layout_config', 'style_overrides', 'responsive_config'),
            'classes': ('collapse',)
        })
    )

    inlines = [SectionElementInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('page').prefetch_related('elements')

    def elements_count(self, obj):
        count = obj.elements.count()
        return format_html(
            '<span style="color: #17a2b8;">{} elements</span>',
            count
        )
    elements_count.short_description = _('Elements')

    def responsive_display(self, obj):
        devices = []
        if obj.show_on_mobile:
            devices.append('📱')
        if obj.show_on_tablet:
            devices.append('📱')
        if obj.show_on_desktop:
            devices.append('💻')
        return ''.join(devices) if devices else '❌'
    responsive_display.short_description = _('Devices')
"""


@admin.register(Element)
class ElementAdmin(TranslationAdmin):
    change_list_template = "admin/page_builder/element/change_list.html"

    list_display = [
        "name",
        "element_type",
        "page",
        "order",
        "column_span",
        "visibility_info",
        "is_active",
        "responsive_display",
        "has_link",
    ]
    list_filter = [
        "page",
        "element_type",
        "is_active",
        "show_on_mobile",
        "show_on_tablet",
        "show_on_desktop",
        "text_align",
    ]
    search_fields = ["name", "page__title", "content"]
    ordering = ["page", "order"]
    readonly_fields = ["content_help", "created_at", "updated_at"]
    filter_horizontal = ["visibility_rules"]

    fieldsets = (
        (
            _("Basic Information"),
            {"fields": ("page", "parent_element", "name", "element_type", "order", "is_active")},
        ),
        (
            _("Content"),
            {
                "fields": ("content", "content_help"),
                "description": _(
                    "Content is stored as JSON. Examples:<br>"
                    '<strong>Heading:</strong> {"text": "My Title", "tag": "h2", "size": "xl"}<br>'
                    '<strong>Text:</strong> {"text": "Your content here", "size": "base"}<br>'
                    '<strong>Button:</strong> {"text": "Click Me", "url": "/link/", "style": "primary"}<br>'
                    '<strong>Image:</strong> {"src": "/path/to/image.jpg", "alt": "Description"}'
                ),
            },
        ),
        (
            _("Layout & Positioning"),
            {"fields": ("column_span", "column_offset", "text_align", "vertical_align")},
        ),
        (
            _("Responsive Settings"),
            {
                "fields": ("show_on_mobile", "show_on_tablet", "show_on_desktop"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Advanced Visibility Rules"),
            {
                "fields": ("visibility_rules",),
                "description": _("Configure conditional display rules for this element"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Links & Interactions"),
            {"fields": ("link_url", "link_target"), "classes": ("collapse",)},
        ),
        (
            _("Design Customization"),
            {
                "fields": (
                    "template_variant",
                    "css_classes",
                    "layout_config",
                    "style_overrides",
                    "responsive_config",
                ),
                "classes": ("collapse",),
            },
        ),
        (_("Metadata"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("page")
            .prefetch_related("visibility_rules")
        )

    def changelist_view(self, request, extra_context=None):
        """Add custom context for grouped display"""
        extra_context = extra_context or {}

        # Get all pages with their elements
        from page_builder.models import Page

        pages_with_elements = []

        # Get all pages, ordered by title
        pages = Page.objects.prefetch_related("elements", "elements__visibility_rules").order_by(
            "title"
        )

        for page in pages:
            # Get all elements for this page (including nested ones)
            all_elements = page.elements.all().order_by("order")

            if all_elements.exists():
                pages_with_elements.append(
                    {
                        "page": page,
                        "elements": all_elements,
                        "element_count": all_elements.count(),
                    }
                )

        extra_context["pages_with_elements"] = pages_with_elements

        # Debug output
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Pages found: {pages.count()}")
        logger.info(f"Pages with elements: {len(pages_with_elements)}")

        return super().changelist_view(request, extra_context=extra_context)

    def responsive_display(self, obj):
        devices = []
        if obj.show_on_mobile:
            devices.append('<i class="fas fa-mobile-alt" title="Mobile"></i>')
        if obj.show_on_tablet:
            devices.append('<i class="fas fa-tablet-alt" title="Tablet"></i>')
        if obj.show_on_desktop:
            devices.append('<i class="fas fa-desktop" title="Desktop"></i>')
        return (
            format_html(" ".join(devices))
            if devices
            else format_html('<span style="color: #999;">—</span>')
        )

    responsive_display.short_description = _("Devices")

    def visibility_info(self, obj):
        """Show if element has visibility rules applied"""
        rule_count = obj.visibility_rules.count()
        if rule_count > 0:
            return format_html(
                '<span style="background: #ffc107; color: #000; padding: 2px 6px; border-radius: 3px; font-size: 11px;">'
                '<i class="fas fa-eye"></i> {} {}</span>',
                rule_count,
                _("rule") if rule_count == 1 else _("rules"),
            )
        return format_html('<span style="color: #999;">—</span>')

    visibility_info.short_description = _("Visibility Rules")

    def has_link(self, obj):
        return format_html('<i class="fas fa-link"></i>') if obj.link_url else ""

    has_link.short_description = _("Link")

    def content_help(self, obj):
        """Show content examples based on element type"""
        examples = {
            "heading": '{"text": "My Heading", "tag": "h2", "size": "xl", "weight": "bold", "color": "gray-900"}',
            "text": '{"text": "Your paragraph text here", "size": "base", "color": "gray-700"}',
            "button": '{"text": "Click Me", "url": "/link/", "style": "primary", "size": "md"}',
            "image": '{"src": "/static/images/sample.jpg", "alt": "Description", "width": "full", "height": "auto"}',
        }

        example = examples.get(obj.element_type, '{"key": "value"}')

        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 12px;">'
            "<strong>Example for {0}:</strong><br>"
            '<code style="color: #d63384;">{1}</code>'
            "</div>",
            obj.element_type.title(),
            example,
        )

    content_help.short_description = _("Content Format Guide")


@admin.register(PageTemplate)
class PageTemplateAdmin(admin.ModelAdmin):
    change_list_template = "admin/page_builder/pagetemplate/change_list.html"
    list_display = [
        "name",
        "page_type",
        "category",
        "version",
        "usage_count",
        "is_public",
        "is_premium",
        "created_by",
        "created_at",
    ]
    list_filter = ["page_type", "category", "is_public", "is_premium", "created_at"]
    search_fields = ["name", "description", "created_by__username"]
    readonly_fields = ["usage_count", "created_at", "updated_at", "template_preview"]

    fieldsets = (
        (
            _("Basic Information"),
            {"fields": ("name", "description", "page_type", "category", "version")},
        ),
        (_("Template Data"), {"fields": ("template_data",)}),
        (_("Settings"), {"fields": ("is_public", "is_premium", "preview_image")}),
        (
            _("Usage Statistics"),
            {"fields": ("usage_count", "template_preview"), "classes": ("collapse",)},
        ),
        (
            _("Author Info"),
            {"fields": ("created_by", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    actions = ["duplicate_templates", "export_templates"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("created_by")

    def changelist_view(self, request, extra_context=None):
        """Add custom context for filters"""
        extra_context = extra_context or {}
        extra_context["page_types"] = Page.PAGE_TYPES
        extra_context["categories"] = [
            ("general", _("General")),
            ("ecommerce", _("E-commerce")),
            ("blog", _("Blog")),
            ("portfolio", _("Portfolio")),
            ("business", _("Business")),
            ("landing", _("Landing Page")),
        ]
        return super().changelist_view(request, extra_context=extra_context)

    def template_preview(self, obj):
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">'
            "<strong>Usage:</strong> {} times<br>"
            "<strong>Type:</strong> {}<br>"
            "<strong>Category:</strong> {}<br>"
            "<strong>Public:</strong> {}<br>"
            "</div>",
            obj.usage_count,
            obj.get_page_type_display(),
            obj.category.title(),
            "✅" if obj.is_public else "❌",
        )

    template_preview.short_description = _("Template Info")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def duplicate_templates(self, request, queryset):
        count = 0
        for template in queryset:
            PageTemplate.objects.create(
                name=_(f"Copy of {template.name}"),
                description=template.description,
                page_type=template.page_type,
                template_data=template.template_data.copy(),
                category=template.category,
                is_public=False,
                created_by=request.user,
            )
            count += 1
        self.message_user(request, _(f"Duplicated {count} templates."))

    duplicate_templates.short_description = _("Duplicate selected templates")

    def export_templates(self, request, queryset):
        # This would trigger a download of the template data
        self.message_user(request, _("Export functionality coming soon!"))

    export_templates.short_description = _("Export selected templates")


# SectionTemplate removed - sections no longer exist
"""
@admin.register(SectionTemplate)
class SectionTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'usage_count',
        'is_public', 'created_by', 'created_at'
    ]
    list_filter = ['category', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'tags', 'created_by__username']
    readonly_fields = ['usage_count', 'created_at', 'updated_at']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'description', 'category', 'tags')
        }),
        (_('Template Data'), {
            'fields': ('template_data',)
        }),
        (_('Settings'), {
            'fields': ('is_public', 'preview_image')
        }),
        (_('Statistics'), {
            'fields': ('usage_count',),
            'classes': ('collapse',)
        }),
        (_('Author Info'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
"""


@admin.register(ElementTemplate)
class ElementTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "element_type",
        "category",
        "usage_count",
        "is_public",
        "created_by",
        "created_at",
    ]
    list_filter = ["element_type", "category", "is_public", "created_at"]
    search_fields = ["name", "description", "tags", "created_by__username"]
    readonly_fields = ["usage_count", "created_at", "updated_at"]

    fieldsets = (
        (
            _("Basic Information"),
            {"fields": ("name", "description", "element_type", "category", "tags")},
        ),
        (_("Template Data"), {"fields": ("template_data",)}),
        (_("Settings"), {"fields": ("is_public", "preview_image")}),
        (_("Statistics"), {"fields": ("usage_count",), "classes": ("collapse",)}),
        (
            _("Author Info"),
            {"fields": ("created_by", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("created_by")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(VisibilityRule)
class VisibilityRuleAdmin(admin.ModelAdmin):
    change_list_template = "admin/page_builder/visibilityrule/change_list.html"
    list_display = [
        "name",
        "rule_type_display",
        "operator",
        "is_active",
        "priority",
        "cache_duration",
        "updated_at",
        "wizard_link",
    ]
    list_filter = ["rule_type", "operator", "is_active", "priority"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "description", "is_active", "priority")}),
        (
            _("Rule Configuration"),
            {
                "fields": ("rule_type", "operator", "value"),
                "description": _("Configure the condition to evaluate"),
            },
        ),
        (
            _("Performance"),
            {
                "fields": ("cache_duration",),
                "description": _("How long to cache rule evaluation results (in seconds)"),
                "classes": ("collapse",),
            },
        ),
        (_("Metadata"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def rule_type_display(self, obj):
        return obj.get_rule_type_display()

    rule_type_display.short_description = _("Rule Type")

    def changelist_view(self, request, extra_context=None):
        """Add extra context for the change list template"""
        extra_context = extra_context or {}
        extra_context["total_rules"] = VisibilityRule.objects.count()
        extra_context["active_rules"] = VisibilityRule.objects.filter(is_active=True).count()
        extra_context["rule_types"] = VisibilityRule.RULE_TYPES
        extra_context["operators"] = VisibilityRule.OPERATORS
        return super().changelist_view(request, extra_context=extra_context)

    def get_fieldsets(self, request, obj=None):
        """Dynamic fieldsets based on rule type"""
        fieldsets = super().get_fieldsets(request, obj)

        if obj:
            # Add help text based on rule type
            help_texts = {
                "geo_country": _("Use ISO country codes (e.g., US, GB, FR)"),
                "user_group": _("Enter group names as a list"),
                "date_range": _('Use format: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}'),
                "time_range": _('Use format: {"start": "HH:MM", "end": "HH:MM"}'),
                "cart_value": _("Enter numeric value for comparison"),
            }

            if obj.rule_type in help_texts:
                for fieldset in fieldsets:
                    if fieldset[0] == _("Rule Configuration"):
                        fieldset[1]["description"] = help_texts[obj.rule_type]
                        break

        return fieldsets

    def add_view(self, request, form_url="", extra_context=None):
        """Redirect add view to the wizard"""
        from django.shortcuts import redirect

        return redirect("page_builder_admin:visibility_rule_wizard")

    def wizard_link(self, obj):
        """Link to edit rule in wizard"""
        from django.urls import reverse
        from django.utils.html import format_html

        url = reverse("page_builder_admin:visibility_rule_wizard_edit", args=[obj.pk])
        return format_html(
            '<a href="{}" class="button" title="{}"><i class="fas fa-magic"></i></a>',
            url,
            _("Edit in Wizard"),
        )

    wizard_link.short_description = _("Wizard")


class RuleGroupMemberInline(admin.TabularInline):
    model = RuleGroupMember
    extra = 1
    fields = ["rule", "order"]
    ordering = ["order"]
    autocomplete_fields = ["rule"]


@admin.register(RuleGroup)
class RuleGroupAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "logic_operator_display",
        "rules_count",
        "parent_group",
        "is_active",
        "updated_at",
        "builder_link",
    ]
    list_filter = ["logic_operator", "is_active", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [RuleGroupMemberInline]
    change_list_template = "admin/page_builder/rulegroup/change_list.html"

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "description", "is_active")}),
        (
            _("Logic Configuration"),
            {
                "fields": ("logic_operator", "parent_group"),
                "description": _("How to combine rules in this group"),
            },
        ),
        (_("Metadata"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def logic_operator_display(self, obj):
        return obj.get_logic_operator_display()

    logic_operator_display.short_description = _("Logic")

    def rules_count(self, obj):
        return obj.rules.count()

    rules_count.short_description = _("Rules")

    def builder_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html

        url = reverse("page_builder_admin:rule_builder_edit", args=[obj.pk])
        return format_html(
            '<a href="{}" class="button" style="padding: 4px 8px; font-size: 11px;">'
            '<i class="fas fa-project-diagram"></i> Open Builder</a>',
            url,
        )

    builder_link.short_description = _("Builder")
    builder_link.allow_tags = True

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("rules", "child_groups")

    def changelist_view(self, request, extra_context=None):
        from django.urls import reverse

        extra_context = extra_context or {}
        extra_context["rule_builder_url"] = reverse("page_builder_admin:rule_builder")
        return super().changelist_view(request, extra_context=extra_context)


# Update ElementAdmin to include visibility rules
