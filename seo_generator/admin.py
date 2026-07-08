from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Q

from seo_generator.models import SEOProviderAccount


@admin.register(SEOProviderAccount)
class SEOProviderAccountAdmin(admin.ModelAdmin):
    """Admin for SEO provider connections."""

    change_list_template = 'admin/seo_generator/seoprovideraccount/change_list.html'

    list_per_page = 1000

    list_display = [
        'display_name',
        'provider_type',
        'is_active_badge',
        'is_primary_badge',
        'created_at',
    ]
    list_filter = ['is_active', 'is_primary', 'created_at']
    search_fields = ['name', 'provider_key', 'component__name', 'component__slug']
    readonly_fields = [
        'credentials_display',
        'created_at',
        'updated_at',
    ]

    fieldsets = (
        (_('Provider Information'), {
            'fields': ('site', 'component', 'provider_key', 'name')
        }),
        (_('Configuration'), {
            'fields': ('is_active', 'is_primary', 'priority', 'settings')
        }),
        (_('Credentials'), {
            'fields': ('credentials_display',),
            'description': _('Credentials are encrypted and managed through the provider wizard. To update credentials, reinstall the provider.'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description=_('Name'))
    def display_name(self, obj):
        return obj.name

    @admin.display(description=_('Provider'))
    def provider_type(self, obj):
        if obj.component:
            return obj.component.name
        return obj.provider_key or '-'

    @admin.display(description=_('Status'))
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span class="status-badge active">'
                '<i class="fas fa-check-circle"></i> ACTIVE'
                '</span>'
            )
        return format_html(
            '<span class="status-badge inactive">'
            '<i class="fas fa-times-circle"></i> INACTIVE'
            '</span>'
        )

    @admin.display(description=_('Primary'))
    def is_primary_badge(self, obj):
        if obj.is_primary:
            return format_html(
                '<span class="status-badge primary">'
                '<i class="fas fa-star"></i> PRIMARY'
                '</span>'
            )
        return '-'

    @admin.display(description=_('Credentials'))
    def credentials_display(self, obj):
        if obj.credentials:
            return format_html(
                '<div class="messagelist"><li class="info">'
                '<i class="fas fa-lock"></i> <strong>{}</strong><br>'
                '<span class="quiet help">{} bytes encrypted data</span>'
                '</li></div>',
                _('Credentials are encrypted and stored securely'),
                len(obj.credentials)
            )
        return format_html(
            '<div class="messagelist"><li class="warning">'
            '<i class="fas fa-exclamation-triangle"></i> {}'
            '</li></div>',
            _('No credentials configured (built-in provider)')
        )

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the provider account list view."""
        extra_context = extra_context or {}

        all_providers = SEOProviderAccount.objects.select_related('component').all()

        extra_context['active_count'] = all_providers.filter(is_active=True).count()
        extra_context['inactive_count'] = all_providers.filter(is_active=False).count()

        try:
            extra_context['primary_provider'] = all_providers.get(is_primary=True)
        except SEOProviderAccount.DoesNotExist:
            extra_context['primary_provider'] = None

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Filter queryset based on request parameters."""
        qs = super().get_queryset(request).select_related('component', 'site')

        is_active = request.GET.get('is_active')
        if is_active:
            qs = qs.filter(is_active=(is_active == '1'))

        is_primary = request.GET.get('is_primary')
        if is_primary:
            qs = qs.filter(is_primary=(is_primary == '1'))

        search = request.GET.get('q')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(provider_key__icontains=search) |
                Q(component__name__icontains=search)
            )

        return qs
