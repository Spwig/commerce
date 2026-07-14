from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import SetupProgress


@admin.register(SetupProgress)
class SetupProgressAdmin(admin.ModelAdmin):
    """
    Admin interface for Setup Progress (read-only monitoring)
    """

    class Media:
        css = {"all": ("setup_wizard/admin/css/admin_progress.css",)}

    def has_add_permission(self, request):
        # Only allow one instance (singleton)
        return not SetupProgress.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Never allow deletion of setup progress
        return False

    list_display = (
        "get_completion_status",
        "get_essential_status",
        "setup_started_at",
        "setup_completed_at",
        "last_step_completed",
    )

    readonly_fields = (
        "completion_summary",
        "essential_items_status",
        "optional_items_status",
        "setup_started_at",
        "setup_completed_at",
        "setup_started_by",
        "setup_completed_by",
        "last_step_completed",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("Setup Overview"),
            {
                "fields": ("completion_summary",),
                "description": _("Overall setup progress and status"),
            },
        ),
        (
            _("Essential Setup Items"),
            {
                "fields": ("essential_items_status",),
                "description": _("Required setup items for store operation"),
            },
        ),
        (
            _("Optional Setup Items"),
            {
                "fields": ("optional_items_status",),
                "description": _("Additional setup items to enhance your store"),
            },
        ),
        (
            _("Setup Timeline"),
            {
                "fields": (
                    "setup_started_at",
                    "setup_started_by",
                    "setup_completed_at",
                    "setup_completed_by",
                    "last_step_completed",
                ),
                "description": _("Timeline and user tracking for setup process"),
                "classes": ("collapse",),
            },
        ),
        (
            _("System Information"),
            {
                "fields": ("created_at", "updated_at"),
                "description": _("System timestamps"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_completion_status(self, obj):
        """Display overall completion status"""
        percentage = obj.get_completion_percentage()
        if percentage == 100:
            css_class = "progress-complete"
            icon = '<i class="fas fa-check-circle"></i>'
            text = _("Complete")
        elif percentage >= 50:
            css_class = "progress-partial"
            icon = '<i class="fas fa-circle-half-stroke"></i>'
            text = _("%(percentage)s%% Done") % {"percentage": percentage}
        else:
            css_class = "progress-incomplete"
            icon = '<i class="fas fa-circle-exclamation"></i>'
            text = _("%(percentage)s%% Done") % {"percentage": percentage}

        return format_html(
            '<span class="setup-progress-status {}">{} {}</span>', css_class, icon, text
        )

    get_completion_status.short_description = _("Overall Progress")

    def get_essential_status(self, obj):
        """Display essential setup status"""
        if obj.is_essential_setup_complete():
            return format_html(
                '<span class="setup-progress-status progress-complete">'
                '<i class="fas fa-check-circle"></i> {}</span>',
                _("Complete"),
            )
        else:
            percentage = obj.get_essential_completion_percentage()
            return format_html(
                '<span class="setup-progress-status progress-incomplete">'
                '<i class="fas fa-circle-exclamation"></i> {}% {}</span>',
                percentage,
                _("Done"),
            )

    get_essential_status.short_description = _("Essential Items")

    def completion_summary(self, obj):
        """Display completion summary with actions"""
        overall_percentage = obj.get_completion_percentage()
        essential_percentage = obj.get_essential_completion_percentage()

        if obj.is_setup_complete():
            status_class = "status-complete"
            status_text = _("Setup Complete!")
            status_desc = _("Your store is fully configured and ready for business.")
        elif obj.is_essential_setup_complete():
            status_class = "status-essential-complete"
            status_text = _("Essential Setup Complete")
            status_desc = _(
                "Your store is ready to start selling. Optional items can be completed anytime."
            )
        else:
            status_class = "status-incomplete"
            status_text = _("Setup Incomplete")
            status_desc = _("Essential setup items are still needed before your store is ready.")

        setup_url = reverse("setup_wizard:start")
        dashboard_url = reverse("admin:index")
        remaining = len(obj.get_incomplete_essential_items()) + len(
            obj.get_incomplete_optional_items()
        )

        essential_class = (
            "progress-complete" if obj.is_essential_setup_complete() else "progress-incomplete"
        )
        action_text = (
            _("Review Setup") if obj.is_essential_setup_complete() else _("Complete Setup")
        )

        return format_html(
            '<div class="setup-summary {status_class}">'
            '  <h3 class="setup-summary-title"><i class="fas fa-chart-pie"></i> {status_text}</h3>'
            '  <p class="setup-summary-desc">{status_desc}</p>'
            '  <div class="setup-summary-stats">'
            '    <div class="setup-stat">'
            '      <div class="setup-stat-value">{overall}%</div>'
            '      <div class="setup-stat-label">{overall_label}</div>'
            "    </div>"
            '    <div class="setup-stat">'
            '      <div class="setup-stat-value {essential_class}">{essential}%</div>'
            '      <div class="setup-stat-label">{essential_label}</div>'
            "    </div>"
            '    <div class="setup-stat">'
            '      <div class="setup-stat-value">{remaining}</div>'
            '      <div class="setup-stat-label">{remaining_label}</div>'
            "    </div>"
            "  </div>"
            '  <div class="setup-summary-actions">'
            '    <a href="{setup_url}" class="btn btn-primary">'
            '      <i class="fas fa-rocket"></i> {action_text}'
            "    </a>"
            '    <a href="{dashboard_url}" class="btn btn-secondary">'
            '      <i class="fas fa-tachometer-alt"></i> {dashboard_label}'
            "    </a>"
            "  </div>"
            "</div>",
            status_class=status_class,
            status_text=status_text,
            status_desc=status_desc,
            overall=overall_percentage,
            overall_label=_("Overall Progress"),
            essential=essential_percentage,
            essential_class=essential_class,
            essential_label=_("Essential Items"),
            remaining=remaining,
            remaining_label=_("Items Remaining"),
            setup_url=setup_url,
            action_text=action_text,
            dashboard_url=dashboard_url,
            dashboard_label=_("Dashboard"),
        )

    completion_summary.short_description = _("Setup Status")

    def _render_items_status(self, items):
        """Render a list of setup items as HTML"""
        items_html = []
        for item in items:
            css_class = "item-completed" if item["completed"] else "item-pending"
            icon_class = "fas fa-check-circle" if item["completed"] else "fas fa-circle"

            items_html.append(
                format_html(
                    '<div class="setup-item {css_class}">'
                    '  <span class="setup-item-icon"><i class="{step_icon}"></i></span>'
                    '  <div class="setup-item-content">'
                    '    <strong class="setup-item-label">{label}</strong>'
                    '    <div class="setup-item-desc">{description}</div>'
                    "  </div>"
                    '  <span class="setup-item-status"><i class="{icon_class}"></i></span>'
                    "</div>",
                    css_class=css_class,
                    step_icon=item["icon"],
                    label=item["label"],
                    description=item["description"],
                    icon_class=icon_class,
                )
            )

        return format_html("".join(str(h) for h in items_html))

    def essential_items_status(self, obj):
        """Display essential setup items status"""
        return self._render_items_status(obj.get_essential_items())

    essential_items_status.short_description = _("Essential Items")

    def optional_items_status(self, obj):
        """Display optional setup items status"""
        return self._render_items_status(obj.get_optional_items())

    optional_items_status.short_description = _("Optional Items")

    def changelist_view(self, request, extra_context=None):
        """Override changelist to redirect to the single progress instance"""
        if SetupProgress.objects.exists():
            progress = SetupProgress.objects.first()
            return redirect(reverse("admin:setup_wizard_setupprogress_change", args=[progress.pk]))
        else:
            return redirect(reverse("admin:setup_wizard_setupprogress_add"))

    def response_change(self, request, obj):
        """Override to provide custom success message"""
        response = super().response_change(request, obj)
        completion = obj.get_completion_percentage()
        self.message_user(
            request,
            _("Setup progress reviewed. Current completion: {completion}%").format(
                completion=completion
            ),
        )
        return response
