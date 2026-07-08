from django.conf import settings
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .models import DomainConfiguration


@admin.register(DomainConfiguration)
class DomainConfigurationAdmin(admin.ModelAdmin):
    """Minimal admin registration. Primary UI is via the Site Settings tab."""

    list_display = ('domain', 'ssl_mode', 'status', 'cert_expires_at')
    readonly_fields = (
        'previous_domain', 'cert_domain', 'cert_issuer',
        'cert_expires_at', 'cert_obtained_at', 'is_wildcard',
        'status', 'last_error', 'task_id',
        'created_at', 'updated_at',
    )

    def has_add_permission(self, request):
        # Singleton: prevent adding if one already exists
        return not DomainConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = []
        if settings.IS_HOSTED:
            custom_urls = [
                path(
                    'custom-domain/',
                    self.admin_site.admin_view(self.custom_domain_view),
                    name='domain_ssl_custom_domain',
                ),
            ]
        return custom_urls + urls

    def custom_domain_view(self, request):
        """Admin page for hosted custom domain management."""
        context = {
            **self.admin_site.each_context(request),
            'title': _('Custom Domain'),
            'opts': self.model._meta,
        }
        return TemplateResponse(
            request,
            'admin/domain_ssl/custom_domain.html',
            context,
        )
