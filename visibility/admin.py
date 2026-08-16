from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import RuleGroup, RuleGroupMember, VisibilityRule


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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("rules", "child_groups")

    def changelist_view(self, request, extra_context=None):
        from django.urls import reverse

        extra_context = extra_context or {}
        extra_context["rule_builder_url"] = reverse("page_builder_admin:rule_builder")
        return super().changelist_view(request, extra_context=extra_context)
