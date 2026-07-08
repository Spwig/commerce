"""
Admin interface for Component Update System
"""

from django.contrib import admin
from django.utils.html import format_html, escape
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, path
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings as django_settings

from .models import (
    UpdateChannel,
    ComponentRegistry,
    ComponentVersion,
    ComponentDependency,
    UpdateLog,
    UpdateServerConfig,
    PlatformUpdate
)
from .services import UpdateManager, UpdateAuthenticationError, UpdateInstallError, PlatformUpdateService, PlatformUpdateError
from management.services import SystemStatusService

# Upgrader service URL — fleet instances point to the shared fleet_upgrader,
# self-hosted/dedicated use the per-instance upgrader sidecar.
_UPGRADER_URL = getattr(django_settings, 'UPGRADER_URL', 'http://upgrader:8080')


@admin.register(UpdateChannel)
class UpdateChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    ordering = ['priority', 'name']


class ComponentVersionInline(admin.TabularInline):
    model = ComponentVersion
    extra = 0
    readonly_fields = ['version', 'installed_at', 'health_status', 'is_active']
    fields = ['version', 'installed_at', 'is_active', 'health_status', 'rollback_available']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class ComponentDependencyInline(admin.TabularInline):
    model = ComponentDependency
    fk_name = 'component'
    extra = 0
    readonly_fields = ['depends_on', 'version_constraint']
    fields = ['depends_on', 'version_constraint', 'is_required']


@admin.register(ComponentRegistry)
class ComponentRegistryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/component_updates/componentregistry/change_list.html'

    class Media:
        css = {'all': ('component_updates/admin/css/platform_update_list.css',)}

    list_display = [
        'name',
        'component_type',
        'current_version',
        'update_status',
        'channel',
        'auto_update',
        'locked',
        'last_checked'
    ]
    list_filter = [
        'component_type',
        'update_available',
        'auto_update',
        'locked',
        'update_channel'
    ]
    search_fields = ['name', 'slug', 'description', 'author']
    readonly_fields = [
        'slug',
        'current_version',
        'installed_at',
        'last_updated',
        'last_checked',
        'update_status_detail',
        'rollback_options'
    ]

    fieldsets = (
        (_('Component Information'), {
            'fields': ('component_type', 'slug', 'name', 'description', 'author')
        }),
        (_('Version & Update Status'), {
            'fields': (
                'current_version',
                'update_status_detail',
                'latest_version',
                'update_channel',
                'auto_update'
            )
        }),
        (_('Lock & Freeze'), {
            'fields': ('locked', 'lock_reason'),
            'classes': ('collapse',)
        }),
        (_('Platform Compatibility'), {
            'fields': ('engine_min_version', 'engine_max_version'),
            'classes': ('collapse',)
        }),
        (_('Links'), {
            'fields': ('homepage_url', 'support_url'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('installed_at', 'last_updated', 'last_checked'),
            'classes': ('collapse',)
        }),
        (_('Rollback'), {
            'fields': ('rollback_options',),
            'classes': ('collapse',)
        }),
    )

    inlines = [ComponentVersionInline, ComponentDependencyInline]

    actions = ['check_for_updates', 'install_updates', 'enable_auto_update', 'disable_auto_update', 'lock_components', 'unlock_components']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('filter/', self.admin_site.admin_view(self.filter_components), name='component_updates_componentregistry_filter'),
            path('check-updates/', self.admin_site.admin_view(self.check_all_updates), name='component_updates_componentregistry_check_updates'),
            path('<int:pk>/install-update/', self.admin_site.admin_view(self.install_single_update), name='component_updates_componentregistry_install_update'),
            path('<int:pk>/toggle-lock/', self.admin_site.admin_view(self.toggle_lock), name='component_updates_componentregistry_toggle_lock'),
            path('version-history/<slug:slug>/', self.admin_site.admin_view(self.get_version_history), name='component_updates_componentregistry_version_history'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Stats for overview cards
        total_components = ComponentRegistry.objects.count()
        updates_available = ComponentRegistry.objects.filter(update_available=True, locked=False).count()
        up_to_date = ComponentRegistry.objects.filter(update_available=False).count()
        locked_count = ComponentRegistry.objects.filter(locked=True).count()

        # All possible component types for the filter dropdown
        component_types = ComponentRegistry.COMPONENT_TYPES

        # Get system version info for platform updates
        system_version = SystemStatusService.get_version_info()

        # Get maintenance status for display
        maintenance_status = {}
        try:
            from core.license import get_license_manager
            maintenance_status = get_license_manager().get_maintenance_status()
        except Exception:
            pass

        extra_context.update({
            'total_components': total_components,
            'updates_available': updates_available,
            'up_to_date': up_to_date,
            'locked_count': locked_count,
            'component_types': component_types,
            'system_version': system_version,
            'maintenance_status': maintenance_status,
        })

        return super().changelist_view(request, extra_context=extra_context)

    def filter_components(self, request):
        """AJAX endpoint for filtering components"""
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid request'}, status=400)

        queryset = ComponentRegistry.objects.all()

        # Apply filters
        search = request.GET.get('search', '')
        component_type = request.GET.get('type', '')
        update_status = request.GET.get('update_status', '')
        locked = request.GET.get('locked', '')
        auto_update = request.GET.get('auto_update', '')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(slug__icontains=search) |
                Q(description__icontains=search) |
                Q(author__icontains=search)
            )

        if component_type:
            queryset = queryset.filter(component_type=component_type)

        if update_status == 'available':
            queryset = queryset.filter(update_available=True)
        elif update_status == 'uptodate':
            queryset = queryset.filter(update_available=False)

        if locked == 'locked':
            queryset = queryset.filter(locked=True)
        elif locked == 'unlocked':
            queryset = queryset.filter(locked=False)

        if auto_update == 'enabled':
            queryset = queryset.filter(auto_update=True)
        elif auto_update == 'disabled':
            queryset = queryset.filter(auto_update=False)

        # Render HTML
        html = render_to_string(
            'admin/component_updates/partials/component_cards.html',
            {'components': queryset, 'request': request}
        )

        # Calculate stats for filtered results
        total = ComponentRegistry.objects.count()
        updates = ComponentRegistry.objects.filter(update_available=True, locked=False).count()
        uptodate = ComponentRegistry.objects.filter(update_available=False).count()
        locked_count = ComponentRegistry.objects.filter(locked=True).count()

        return JsonResponse({
            'html': html,
            'count': queryset.count(),
            'stats': {
                'total': total,
                'updates': updates,
                'uptodate': uptodate,
                'locked': locked_count,
            }
        })

    def check_all_updates(self, request):
        """Check all components for updates"""
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        try:
            manager = UpdateManager()
            result = manager.check_for_updates()
            return JsonResponse({
                'success': True,
                'updates_found': result.get('updates_found', 0),
                'message': f"Found {result.get('updates_found', 0)} update(s) available"
            })
        except UpdateAuthenticationError as e:
            return JsonResponse({'success': False, 'error': f'Authentication failed: {e}'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def install_single_update(self, request, pk):
        """Install update for a single component"""
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        try:
            component = ComponentRegistry.objects.get(pk=pk)
            if component.locked:
                return JsonResponse({'success': False, 'error': 'Component is locked'})
            if not component.update_available:
                return JsonResponse({'success': False, 'error': 'No update available'})

            manager = UpdateManager()
            manager.install_update(component)
            return JsonResponse({'success': True, 'message': f'Successfully updated {component.name}'})
        except ComponentRegistry.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Component not found'})
        except UpdateInstallError as e:
            return JsonResponse({'success': False, 'error': str(e)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def toggle_lock(self, request, pk):
        """Toggle lock status for a component"""
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        try:
            import json
            data = json.loads(request.body) if request.body else {}
            lock = data.get('lock', True)

            component = ComponentRegistry.objects.get(pk=pk)
            component.locked = lock
            if lock:
                component.lock_reason = 'Locked via admin interface'
            else:
                component.lock_reason = ''
            component.save()

            return JsonResponse({'success': True, 'locked': component.locked})
        except ComponentRegistry.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Component not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def get_version_history(self, request, slug):
        """AJAX endpoint: fetch version history from update server for any component slug."""
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid request'}, status=400)

        channel = request.GET.get('channel', 'stable')

        try:
            manager = UpdateManager()
            versions = manager.get_version_history(slug, channel=channel)
            return JsonResponse({'success': True, 'versions': versions})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def update_status(self, obj):
        """Display colorful update status"""
        if obj.locked:
            return format_html('<span class="cu-status-locked">🔒 Locked</span>')
        elif obj.update_available:
            return format_html('<span class="cu-status-update">⬆️ Update Available</span>')
        else:
            return format_html('<span class="cu-status-ok">✓ Up to date</span>')
    update_status.short_description = _('Status')

    def update_status_detail(self, obj):
        """Detailed update status for change form"""
        if obj.locked:
            return format_html(
                '<div class="cu-detail-box cu-detail-box-locked">'
                '<strong>🔒 Component Locked</strong><br>'
                'Reason: {}'
                '</div>',
                obj.lock_reason or 'No reason provided'
            )
        elif obj.update_available:
            return format_html(
                '<div class="cu-detail-box cu-detail-box-warning">'
                '<strong>⬆️ Update Available</strong><br>'
                'Current: {} → Latest: {}<br>'
                'Channel: {}'
                '</div>',
                obj.current_version,
                obj.latest_version,
                obj.update_channel or 'None'
            )
        else:
            return format_html(
                '<div class="cu-detail-box cu-detail-box-success">'
                '<strong>✓ Up to Date</strong><br>'
                'Version: {}'
                '</div>',
                obj.current_version
            )
    update_status_detail.short_description = _('Update Status')

    def channel(self, obj):
        return obj.update_channel.name if obj.update_channel else '-'
    channel.short_description = _('Channel')

    def rollback_options(self, obj):
        """Display available rollback versions"""
        versions = obj.get_rollback_versions()
        if not versions:
            return format_html('<em>No rollback versions available</em>')

        health_class_map = {
            'healthy': 'cu-health-healthy',
            'degraded': 'cu-health-degraded',
            'unhealthy': 'cu-health-unhealthy',
            'unknown': 'cu-health-unknown',
        }

        items = ''
        for version in versions:
            css_class = health_class_map.get(version.health_status, 'cu-health-unknown')
            items += format_html(
                '<li>Version {} - <span class="{}">{}</span> ({})</li>',
                version.version,
                css_class,
                version.get_health_status_display(),
                version.installed_at.strftime('%Y-%m-%d')
            )
        return format_html('<ul class="cu-version-list">{}</ul>', items)
    rollback_options.short_description = _('Rollback Versions')

    # Admin actions
    def check_for_updates(self, request, queryset):
        """Check selected components for updates"""
        manager = UpdateManager()
        updates_found = 0

        try:
            for component in queryset:
                result = manager.check_for_updates(component=component)
                updates_found += result['updates_found']

            if updates_found > 0:
                self.message_user(
                    request,
                    f'Found {updates_found} update(s) available',
                    messages.WARNING
                )
            else:
                self.message_user(
                    request,
                    f'All {queryset.count()} component(s) are up to date',
                    messages.SUCCESS
                )
        except UpdateAuthenticationError as e:
            self.message_user(
                request,
                f'Authentication failed: {e}',
                messages.ERROR
            )
        except Exception as e:
            self.message_user(
                request,
                f'Update check failed: {e}',
                messages.ERROR
            )
    check_for_updates.short_description = _('Check for updates')

    def install_updates(self, request, queryset):
        """Install available updates for selected components"""
        manager = UpdateManager()
        installed = 0
        skipped = 0
        failed = 0

        for component in queryset:
            if component.locked:
                skipped += 1
                continue

            if not component.update_available:
                skipped += 1
                continue

            try:
                manager.install_update(component)
                installed += 1
            except Exception as e:
                failed += 1
                self.message_user(
                    request,
                    f'Failed to update {component.name}: {e}',
                    messages.ERROR
                )

        if installed > 0:
            self.message_user(
                request,
                f'Successfully installed {installed} update(s)',
                messages.SUCCESS
            )
        if skipped > 0:
            self.message_user(
                request,
                f'Skipped {skipped} component(s) (locked or no updates)',
                messages.WARNING
            )
    install_updates.short_description = _('Install available updates')

    def enable_auto_update(self, request, queryset):
        updated = queryset.update(auto_update=True)
        self.message_user(request, f'Auto-update enabled for {updated} component(s)')
    enable_auto_update.short_description = _('Enable auto-update')

    def disable_auto_update(self, request, queryset):
        updated = queryset.update(auto_update=False)
        self.message_user(request, f'Auto-update disabled for {updated} component(s)')
    disable_auto_update.short_description = _('Disable auto-update')

    def lock_components(self, request, queryset):
        updated = queryset.update(locked=True, lock_reason='Locked via admin action')
        self.message_user(request, f'Locked {updated} component(s)')
    lock_components.short_description = _('Lock components')

    def unlock_components(self, request, queryset):
        updated = queryset.update(locked=False, lock_reason='')
        self.message_user(request, f'Unlocked {updated} component(s)')
    unlock_components.short_description = _('Unlock components')


@admin.register(ComponentVersion)
class ComponentVersionAdmin(admin.ModelAdmin):
    list_display = [
        'component',
        'version',
        'is_active',
        'health_status',
        'installed_at',
        'install_method',
        'security_update'
    ]
    list_filter = [
        'is_active',
        'health_status',
        'install_method',
        'security_update',
        'breaking_changes',
        'rollback_available'
    ]
    search_fields = ['component__name', 'version', 'release_notes']
    readonly_fields = [
        'component',
        'version',
        'installed_at',
        'package_checksum',
        'health_checked_at',
        'installed_by'
    ]

    fieldsets = (
        (_('Version Information'), {
            'fields': ('component', 'version', 'is_active')
        }),
        (_('Installation'), {
            'fields': (
                'installed_at',
                'install_method',
                'installed_by',
                'rollback_available'
            )
        }),
        (_('Health Status'), {
            'fields': ('health_status', 'health_checked_at', 'health_details')
        }),
        (_('Package Info'), {
            'fields': (
                'package_url',
                'package_checksum',
                'package_size_bytes'
            ),
            'classes': ('collapse',)
        }),
        (_('Release Notes'), {
            'fields': (
                'release_notes',
                'breaking_changes',
                'security_update'
            ),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_version', 'mark_rollback_available']

    def activate_version(self, request, queryset):
        """Activate selected version (only one should be selected)"""
        if queryset.count() != 1:
            self.message_user(request, 'Please select exactly one version to activate', level='error')
            return

        version = queryset.first()
        version.activate()
        self.message_user(request, f'Activated {version.component.name} v{version.version}')
    activate_version.short_description = _('Activate this version')

    def mark_rollback_available(self, request, queryset):
        updated = queryset.update(rollback_available=True)
        self.message_user(request, f'Marked {updated} version(s) as rollback available')
    mark_rollback_available.short_description = _('Mark as rollback available')


@admin.register(UpdateLog)
class UpdateLogAdmin(admin.ModelAdmin):
    list_display = [
        'component',
        'action',
        'status',
        'version_change',
        'started_at',
        'duration',
        'performed_by',
        'is_automatic'
    ]
    list_filter = [
        'action',
        'status',
        'is_automatic',
        'started_at'
    ]
    search_fields = ['component__name', 'error_message']
    readonly_fields = [
        'component',
        'action',
        'status',
        'old_version',
        'new_version',
        'started_at',
        'completed_at',
        'duration_seconds',
        'performed_by',
        'error_display'
    ]

    fieldsets = (
        (_('Operation Details'), {
            'fields': (
                'component',
                'action',
                'status',
                'old_version',
                'new_version'
            )
        }),
        (_('Timing'), {
            'fields': (
                'started_at',
                'completed_at',
                'duration_seconds'
            )
        }),
        (_('User & Automation'), {
            'fields': (
                'performed_by',
                'is_automatic'
            )
        }),
        (_('Error Information'), {
            'fields': ('error_display',),
            'classes': ('collapse',)
        }),
        (_('Additional Details'), {
            'fields': ('details',),
            'classes': ('collapse',)
        }),
    )

    def version_change(self, obj):
        if obj.old_version and obj.new_version:
            return f'{obj.old_version} → {obj.new_version}'
        elif obj.new_version:
            return f'New: {obj.new_version}'
        return '-'
    version_change.short_description = _('Version Change')

    def duration(self, obj):
        if obj.duration_seconds is not None:
            return f'{obj.duration_seconds}s'
        return '-'
    duration.short_description = _('Duration')

    def error_display(self, obj):
        if not obj.error_message:
            return format_html('<em>No errors</em>')

        if obj.error_traceback:
            return format_html(
                '<div class="cu-detail-box cu-detail-box-error">'
                '<strong>Error:</strong><br>{}'
                '<br><br><strong>Traceback:</strong><br><pre>{}</pre>'
                '</div>',
                obj.error_message,
                obj.error_traceback
            )
        return format_html(
            '<div class="cu-detail-box cu-detail-box-error">'
            '<strong>Error:</strong><br>{}'
            '</div>',
            obj.error_message
        )
    error_display.short_description = _('Error Details')

    def has_add_permission(self, request):
        return False


@admin.register(UpdateServerConfig)
class UpdateServerConfigAdmin(admin.ModelAdmin):
    list_display = [
        'server_url',
        'api_version',
        'connection_status',
        'jwt_status',
        'last_check'
    ]
    readonly_fields = [
        'installation_uuid',
        'jwt_expires_at',
        'last_check',
        'last_connection_attempt',
        'connection_status_detail'
    ]

    fieldsets = (
        (_('Server Configuration'), {
            'fields': ('server_url', 'api_version')
        }),
        (_('Authentication'), {
            'fields': (
                'installation_uuid',
                'license_key',
                'jwt_token',
                'jwt_expires_at'
            )
        }),
        (_('Update Behavior'), {
            'fields': (
                'check_interval_hours',
                'auto_download',
                'auto_install_security'
            )
        }),
        (_('Telemetry'), {
            'fields': ('send_telemetry',)
        }),
        (_('Connection Status'), {
            'fields': (
                'connection_status_detail',
                'last_check',
                'last_connection_attempt',
                'last_connection_error'
            )
        }),
    )

    class Media:
        css = {'all': ('component_updates/admin/css/platform_update_list.css',)}

    def changelist_view(self, request, extra_context=None):
        from core.license import get_license_manager
        if get_license_manager().is_spwig_hosted():
            from django.shortcuts import redirect
            from django.urls import reverse
            return redirect(reverse('admin:component_updates_hosted_upgrade'))
        return super().changelist_view(request, extra_context)

    def connection_status(self, obj):
        if obj.is_connected:
            return format_html('<span class="cu-connection-ok">● Connected</span>')
        return format_html('<span class="cu-connection-error">● Disconnected</span>')
    connection_status.short_description = _('Status')

    def jwt_status(self, obj):
        if obj.is_jwt_valid():
            return format_html('<span class="cu-jwt-valid">✓ Valid</span>')
        return format_html('<span class="cu-jwt-expired">⚠ Expired</span>')
    jwt_status.short_description = _('JWT')

    def connection_status_detail(self, obj):
        if obj.is_connected:
            if obj.last_connection_attempt:
                return format_html(
                    '<div class="cu-detail-box cu-detail-box-success">'
                    '<strong>✓ Connected to Update Server</strong><br>'
                    'Last successful connection: {}'
                    '</div>',
                    obj.last_connection_attempt.strftime("%Y-%m-%d %H:%M:%S")
                )
            return format_html(
                '<div class="cu-detail-box cu-detail-box-success">'
                '<strong>✓ Connected to Update Server</strong>'
                '</div>'
            )
        else:
            if obj.last_connection_error:
                return format_html(
                    '<div class="cu-detail-box cu-detail-box-error">'
                    '<strong>✗ Not Connected</strong><br>'
                    'Error: {}'
                    '</div>',
                    obj.last_connection_error
                )
            return format_html(
                '<div class="cu-detail-box cu-detail-box-error">'
                '<strong>✗ Not Connected</strong>'
                '</div>'
            )
    connection_status_detail.short_description = _('Connection Details')

    def has_add_permission(self, request):
        # Only allow one instance (singleton)
        return not UpdateServerConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of the config
        return False


@admin.register(ComponentDependency)
class ComponentDependencyAdmin(admin.ModelAdmin):
    list_display = [
        'component',
        'depends_on',
        'version_constraint',
        'is_required',
        'created_at'
    ]
    list_filter = ['is_required', 'created_at']
    search_fields = [
        'component__name',
        'depends_on__name',
        'version_constraint'
    ]
    readonly_fields = ['created_at']


# =============================================================================
# Platform Update Admin
# =============================================================================

@admin.register(PlatformUpdate)
class PlatformUpdateAdmin(admin.ModelAdmin):
    """
    Admin interface for platform updates.
    Provides visual feedback for update progress and history.
    """
    change_list_template = 'admin/component_updates/platformupdate/change_list.html'

    list_display = [
        'version_change',
        'status_badge',
        'progress_bar',
        'channel_badge',
        'duration_display',
        'initiated_by',
        'created_at'
    ]
    list_filter = ['status', 'channel', 'security_update', 'breaking_changes', 'created_at']
    search_fields = ['from_version', 'to_version', 'error_message']
    readonly_fields = [
        'id', 'from_version', 'to_version', 'channel',
        'status', 'progress_percent', 'current_step', 'steps', 'log_lines',
        'package_checksum', 'package_size_bytes', 'bytes_downloaded',
        'changelog', 'release_notes', 'requires_migration',
        'migration_estimate_seconds', 'breaking_changes', 'security_update',
        'rollback_available', 'rollback_version',
        'error_message', 'error_stage', 'error_traceback',
        'created_at', 'started_at', 'completed_at',
        'duration_seconds', 'downtime_seconds',
        'initiated_by', 'celery_task_id',
        'progress_display', 'log_display', 'error_display'
    ]
    ordering = ['-created_at']

    fieldsets = (
        (_('Update Information'), {
            'fields': (
                'id',
                ('from_version', 'to_version'),
                'channel',
                'status',
            )
        }),
        (_('Progress'), {
            'fields': (
                'progress_display',
            )
        }),
        (_('Release Details'), {
            'fields': (
                'changelog',
                'release_notes',
                ('requires_migration', 'migration_estimate_seconds'),
                ('breaking_changes', 'security_update'),
            ),
            'classes': ('collapse',)
        }),
        (_('Package Details'), {
            'fields': (
                'package_size_bytes',
                'bytes_downloaded',
                'package_checksum',
            ),
            'classes': ('collapse',)
        }),
        (_('Rollback'), {
            'fields': (
                'rollback_available',
                'rollback_version',
            ),
            'classes': ('collapse',)
        }),
        (_('Timing'), {
            'fields': (
                'created_at',
                'started_at',
                'completed_at',
                ('duration_seconds', 'downtime_seconds'),
            ),
            'classes': ('collapse',)
        }),
        (_('User & Task'), {
            'fields': (
                'initiated_by',
                'celery_task_id',
            ),
            'classes': ('collapse',)
        }),
        (_('Logs'), {
            'fields': ('log_display',),
            'classes': ('collapse',)
        }),
        (_('Error Information'), {
            'fields': ('error_display',),
            'classes': ('collapse',)
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('check/', self.admin_site.admin_view(self.check_for_update), name='component_updates_platformupdate_check'),
            path('start/', self.admin_site.admin_view(self.start_update), name='component_updates_platformupdate_start'),
            path('<uuid:pk>/status/', self.admin_site.admin_view(self.get_status), name='component_updates_platformupdate_status'),
            path('<uuid:pk>/cancel/', self.admin_site.admin_view(self.cancel_update), name='component_updates_platformupdate_cancel'),
            path('check-hotfix/', self.admin_site.admin_view(self.check_for_hotfix_api), name='component_updates_platformupdate_check_hotfix'),
            path('apply-hotfix/', self.admin_site.admin_view(self.apply_hotfix_api), name='component_updates_platformupdate_apply_hotfix'),
            path('rollback-hotfix/', self.admin_site.admin_view(self.rollback_hotfix_api), name='component_updates_platformupdate_rollback_hotfix'),
            path('hotfix-status/', self.admin_site.admin_view(self.hotfix_status_api), name='component_updates_platformupdate_hotfix_status'),
            # Hosted upgrade scheduling
            path('hosted-upgrade/', self.admin_site.admin_view(self.hosted_upgrade_view), name='component_updates_hosted_upgrade'),
            path('hosted-upgrade/api/check/', self.admin_site.admin_view(self.hosted_upgrade_check_api), name='component_updates_hosted_upgrade_check'),
            path('hosted-upgrade/api/schedule/', self.admin_site.admin_view(self.hosted_upgrade_schedule_api), name='component_updates_hosted_upgrade_schedule'),
            path('hosted-upgrade/api/status/', self.admin_site.admin_view(self.hosted_upgrade_status_api), name='component_updates_hosted_upgrade_status'),
            path('hosted-upgrade/api/snooze/', self.admin_site.admin_view(self.hosted_upgrade_snooze_api), name='component_updates_hosted_upgrade_snooze'),
            path('hosted-upgrade/api/cancel/', self.admin_site.admin_view(self.hosted_upgrade_cancel_api), name='component_updates_hosted_upgrade_cancel'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        from core.license import get_license_manager
        if get_license_manager().is_spwig_hosted():
            from django.shortcuts import redirect
            from django.urls import reverse
            return redirect(reverse('admin:component_updates_hosted_upgrade'))
        import json

        extra_context = extra_context or {}

        # Get current version
        service = PlatformUpdateService()
        current_version = service.get_current_version()

        # Check if update is in progress
        current_update = PlatformUpdate.get_current_update()

        # Reconcile stale in-progress updates: if the update has been running
        # for over 30 minutes, check the upgrader. If it's idle, the upgrade
        # finished but the PlatformUpdate record was never updated (Celery died).
        if current_update and current_update.started_at:
            from django.utils import timezone
            elapsed = (timezone.now() - current_update.started_at).total_seconds()
            if elapsed > 1800:
                try:
                    import requests as req
                    _params = {'instance': getattr(django_settings, 'FLEET_INSTANCE_NAME', '')} if getattr(django_settings, 'FLEET_INSTANCE_NAME', '') else {}
                    resp = req.get(f'{_UPGRADER_URL}/status', params=_params, timeout=3)
                    op = resp.json().get('operation', {})
                    upgrader_done = (
                        op.get('type') != 'upgrade'
                        or op.get('status') in ('idle', 'completed', 'failed')
                    )
                    if upgrader_done:
                        if op.get('failed'):
                            current_update.mark_failed(
                                op.get('error', 'Upgrade failed (recovered from stale state)'),
                                error_stage='recovery'
                            )
                        else:
                            current_update.mark_completed()
                        current_update = None
                except Exception:
                    pass  # Can't reach upgrader — leave as-is

        # Check for cached update info
        from django.core.cache import cache
        update_info = cache.get('platform_update_available', {})

        # Get hotfix status
        hotfix_status = {}
        try:
            hotfix_status = service.get_hotfix_status()
        except Exception:
            pass

        # Extract just the missing hotfix numbers for the apply button
        missing_hf_numbers = [
            hf['hotfix_number']
            for hf in hotfix_status.get('missing_hotfixes', [])
        ]

        # Check if a hotfix operation is currently in progress (via upgrader)
        hotfix_in_progress = False
        hotfix_target_version = ''
        try:
            import requests as req
            _params = {'instance': getattr(django_settings, 'FLEET_INSTANCE_NAME', '')} if getattr(django_settings, 'FLEET_INSTANCE_NAME', '') else {}
            upgrader_resp = req.get(f'{_UPGRADER_URL}/status', params=_params, timeout=3)
            upgrader_data = upgrader_resp.json().get('operation', {})
            if (upgrader_data.get('type') in ('hotfix', 'hotfix_rollback')
                    and upgrader_data.get('status') == 'in_progress'):
                hotfix_in_progress = True
                hotfix_target_version = upgrader_data.get('target_version', '')
        except Exception:
            pass

        extra_context.update({
            'current_version': current_version,
            'current_update': current_update,
            'update_info': update_info,
            'update_info_json': json.dumps(update_info),
            'rollback_info': service.get_rollback_info(),
            'hotfix_status': hotfix_status,
            'missing_hotfix_numbers_json': json.dumps(missing_hf_numbers),
            'hotfix_in_progress': hotfix_in_progress,
            'hotfix_target_version': hotfix_target_version,
        })

        return super().changelist_view(request, extra_context)

    class Media:
        css = {'all': ('component_updates/admin/css/platform_update_list.css',)}

    def version_change(self, obj):
        """Display version change with arrow."""
        return format_html(
            '<span class="cu-version-mono">'
            'v{} <span class="cu-version-arrow">→</span> v{}'
            '</span>',
            obj.from_version, obj.to_version
        )
    version_change.short_description = _('Version')
    version_change.admin_order_field = 'to_version'

    def status_badge(self, obj):
        """Display status as colored badge."""
        css_class = 'cu-badge cu-badge-{}'.format(obj.status)
        return format_html(
            '<span class="{}">{}</span>',
            css_class, obj.get_status_display()
        )
    status_badge.short_description = _('Status')
    status_badge.admin_order_field = 'status'

    def progress_bar(self, obj):
        """Display progress as mini bar."""
        if obj.status == 'completed':
            return format_html('<span class="cu-status-ok">✓</span>')
        if obj.status in ['failed', 'rolled_back']:
            return format_html('<span class="cu-connection-error">✗</span>')

        percent = obj.progress_percent
        return format_html(
            '<div class="cu-progress-mini-track">'
            '<div class="cu-progress-mini-fill" style="width: {}%;"></div>'
            '</div>'
            '<span class="cu-progress-mini-label">{}%</span>',
            percent, percent
        )
    progress_bar.short_description = _('Progress')

    def channel_badge(self, obj):
        """Display channel as badge."""
        channel_class_map = {
            'stable': 'cu-channel-stable',
            'beta': 'cu-channel-beta',
            'dev': 'cu-channel-dev',
        }
        css_class = channel_class_map.get(obj.channel, 'cu-channel-stable')
        return format_html(
            '<span class="{}">{}</span>',
            css_class, obj.channel.upper()
        )
    channel_badge.short_description = _('Channel')

    def duration_display(self, obj):
        """Display duration in human-readable format."""
        if obj.duration_seconds is None:
            return '-'

        minutes = obj.duration_seconds // 60
        seconds = obj.duration_seconds % 60

        if minutes > 0:
            return f'{minutes}m {seconds}s'
        return f'{seconds}s'
    duration_display.short_description = _('Duration')
    duration_display.admin_order_field = 'duration_seconds'

    def progress_display(self, obj):
        """Display progress details with steps."""
        if not obj.steps:
            return format_html('<em>No progress data</em>')

        # Build progress bar
        progress_bar = format_html(
            '<div class="cu-progress-bar-wrapper">'
            '<div class="cu-progress-bar-row">'
            '<div class="cu-progress-bar-outer">'
            '<div class="cu-progress-bar-inner" style="width: {}%;"></div>'
            '</div>'
            '<span class="cu-progress-bar-pct">{}%</span>'
            '</div>'
            '<div class="cu-progress-step-label">{}</div>'
            '</div>',
            obj.progress_percent,
            obj.progress_percent,
            escape(obj.current_step or '')
        )

        # Build steps list
        step_class_map = {
            'completed': ('✅', 'cu-step-completed'),
            'in_progress': ('⏳', 'cu-step-in-progress'),
        }
        steps_html = ''
        for step in obj.steps:
            status = step.get('status', 'pending')
            name = step.get('name', '')
            detail = step.get('detail', '')
            icon, css_class = step_class_map.get(status, ('⬚', 'cu-step-pending'))

            if detail:
                steps_html += format_html(
                    '<div class="cu-progress-step-row">'
                    '<span>{}</span>'
                    '<span class="{}">{}</span>'
                    '<span class="cu-step-detail">{}</span>'
                    '</div>',
                    icon, css_class, name, detail
                )
            else:
                steps_html += format_html(
                    '<div class="cu-progress-step-row">'
                    '<span>{}</span>'
                    '<span class="{}">{}</span>'
                    '</div>',
                    icon, css_class, name
                )

        return format_html(
            '<div class="cu-progress-container">{}<div class="cu-progress-steps">{}</div></div>',
            progress_bar, steps_html
        )
    progress_display.short_description = _('Progress Details')

    def log_display(self, obj):
        """Display recent log lines."""
        if not obj.log_lines:
            return format_html('<em>No log entries</em>')

        lines_html = ''
        for line in obj.log_lines[-30:]:
            lines_html += format_html('<div class="cu-log-line">{}</div>', line)

        return format_html('<div class="cu-log-terminal">{}</div>', lines_html)
    log_display.short_description = _('Log Output')

    def error_display(self, obj):
        """Display error information if any."""
        if not obj.error_message:
            return format_html('<em class="cu-no-errors">No errors</em>')

        if obj.error_traceback:
            return format_html(
                '<div class="cu-error-box">'
                '<div class="cu-error-stage">Error in: {}</div>'
                '<div class="cu-error-message">{}</div>'
                '<details class="cu-error-traceback-toggle">'
                '<summary>Show Traceback</summary>'
                '<pre class="cu-error-traceback">{}</pre>'
                '</details>'
                '</div>',
                obj.error_stage or 'Unknown stage',
                obj.error_message,
                obj.error_traceback
            )
        return format_html(
            '<div class="cu-error-box">'
            '<div class="cu-error-stage">Error in: {}</div>'
            '<div class="cu-error-message">{}</div>'
            '</div>',
            obj.error_stage or 'Unknown stage',
            obj.error_message
        )
    error_display.short_description = _('Error Details')

    def check_for_update(self, request):
        """API endpoint to check for platform updates."""
        try:
            service = PlatformUpdateService()
            result = service.check_for_update()

            # Cache the result
            from django.core.cache import cache
            cache.set('platform_update_available', result, timeout=86400)

            return JsonResponse(result)

        except PlatformUpdateError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def start_update(self, request):
        """API endpoint to start a platform update."""
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)

        try:
            # Check if update can be started
            if not PlatformUpdate.can_start_update():
                return JsonResponse({
                    'error': 'An update is already in progress'
                }, status=400)

            # Get update info from cache
            from django.core.cache import cache
            update_info = cache.get('platform_update_available', {})

            if not update_info.get('update_available'):
                return JsonResponse({
                    'error': 'No update available'
                }, status=400)

            # Create update record
            service = PlatformUpdateService()
            update = service.create_update_record(
                to_version=update_info['latest_version'],
                update_info=update_info,
                user=request.user
            )

            # Start Celery task
            from .tasks import perform_platform_update
            task = perform_platform_update.delay(str(update.id))

            update.celery_task_id = task.id
            update.save(update_fields=['celery_task_id'])

            messages.success(request, f"Platform update to v{update.to_version} started")

            return JsonResponse({
                'success': True,
                'update_id': str(update.id),
                'task_id': task.id
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get_status(self, request, pk):
        """API endpoint to get update status."""
        try:
            service = PlatformUpdateService()
            status = service.get_update_status(str(pk))

            # If update is in an active deploying state with stale progress,
            # supplement with live data from the upgrader. This handles the
            # race where the shop is back but the Celery task (which wrote
            # progress to PlatformUpdate) was killed during container recreation.
            if status.get('status') in ('deploying', 'health_check', 'switching') \
                    and status.get('progress_percent', 0) < 95:
                try:
                    import requests as req
                    _params = {'instance': getattr(django_settings, 'FLEET_INSTANCE_NAME', '')} if getattr(django_settings, 'FLEET_INSTANCE_NAME', '') else {}
                    resp = req.get(f'{_UPGRADER_URL}/status', params=_params, timeout=3)
                    op = resp.json().get('operation', {})
                    if op.get('type') == 'upgrade':
                        upgrader_progress = op.get('progress', 0)
                        if upgrader_progress > status.get('progress_percent', 0):
                            status['progress_percent'] = upgrader_progress
                            status['current_step'] = op.get('step', status.get('current_step', ''))
                            status['steps'] = op.get('steps', status.get('steps', []))
                            status['log_lines'] = op.get('log_lines', status.get('log_lines', []))
                        if op.get('completed'):
                            status['status'] = 'completed'
                            status['progress_percent'] = 100
                        elif op.get('failed'):
                            status['status'] = 'failed'
                            status['error_message'] = op.get('error', '')
                except Exception:
                    pass  # Upgrader unreachable — use DB status as-is

            return JsonResponse(status)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def cancel_update(self, request, pk):
        """API endpoint to cancel an update (if possible)."""
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)

        try:
            update = PlatformUpdate.objects.get(id=pk)

            # Only allow cancellation in early stages
            if update.status not in ['checking', 'downloading']:
                return JsonResponse({
                    'error': 'Update cannot be cancelled at this stage'
                }, status=400)

            # Cancel Celery task if running
            if update.celery_task_id:
                from celery import current_app
                current_app.control.revoke(update.celery_task_id, terminate=True)

            update.mark_failed('Cancelled by user', 'User cancellation')

            return JsonResponse({'success': True})

        except PlatformUpdate.DoesNotExist:
            return JsonResponse({'error': 'Update not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def check_for_hotfix_api(self, request):
        """API endpoint to check for hotfixes from the update server."""
        try:
            service = PlatformUpdateService()
            result = service.check_for_hotfix()
            return JsonResponse(result)
        except PlatformUpdateError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def apply_hotfix_api(self, request):
        """API endpoint to apply hotfixes via the upgrader service."""
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)

        try:
            import json as json_mod
            import requests as req

            data = json_mod.loads(request.body) if request.body else {}
            version = data.get('version')
            hotfix_numbers = data.get('hotfix_numbers', [])

            # Legacy compat: single hotfix_number → list
            if not hotfix_numbers:
                single = data.get('hotfix_number')
                if single:
                    hotfix_numbers = [int(single)]

            if not version or not hotfix_numbers:
                return JsonResponse(
                    {'error': 'version and hotfix_numbers required'}, status=400
                )

            payload = {'version': version, 'hotfix_numbers': hotfix_numbers}
            if getattr(django_settings, 'FLEET_INSTANCE_NAME', ''):
                payload['instance'] = getattr(django_settings, 'FLEET_INSTANCE_NAME', '')

            response = req.post(
                f'{_UPGRADER_URL}/hotfixes/apply',
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            result = response.json()

            # Clear cached hotfix check so the UI no longer shows it as available
            if result.get('success'):
                from django.core.cache import cache
                cache.delete('hotfix_check_result')

            return JsonResponse(result)
        except req.ConnectionError:
            return JsonResponse({
                'error': 'Could not connect to upgrader service. Is it running?'
            }, status=503)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def rollback_hotfix_api(self, request):
        """API endpoint to rollback hotfixes via the upgrader service."""
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)

        try:
            import requests as req

            payload = {}
            if getattr(django_settings, 'FLEET_INSTANCE_NAME', ''):
                payload['instance'] = getattr(django_settings, 'FLEET_INSTANCE_NAME', '')

            response = req.post(
                f'{_UPGRADER_URL}/hotfixes/rollback',
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            return JsonResponse(response.json())
        except req.ConnectionError:
            return JsonResponse({
                'error': 'Could not connect to upgrader service. Is it running?'
            }, status=503)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def hotfix_status_api(self, request):
        """Proxy upgrader operation status for hotfix progress polling."""
        try:
            import requests as req

            params = {}
            if getattr(django_settings, 'FLEET_INSTANCE_NAME', ''):
                params['instance'] = getattr(django_settings, 'FLEET_INSTANCE_NAME', '')

            response = req.get(f'{_UPGRADER_URL}/status', params=params, timeout=5)
            data = response.json()
            op = data.get('operation', {})

            return JsonResponse({
                'status': op.get('status', 'idle'),
                'progress_percent': op.get('progress', 0),
                'current_step': op.get('step', ''),
                'steps': op.get('steps', []),
                'log_lines': op.get('log_lines', []),
                'error_message': op.get('error'),
                'estimated_seconds_remaining': None,
            })
        except Exception:
            # Upgrader unreachable — return a transient error status
            # (JS will continue polling; this happens briefly during restarts)
            return JsonResponse({
                'status': 'in_progress',
                'progress_percent': 0,
                'current_step': 'Waiting for services...',
                'steps': [],
                'log_lines': [],
                'error_message': None,
                'estimated_seconds_remaining': None,
            })

    # ── Hosted Upgrade Scheduling ──────────────────────────────────────

    def _proxy_to_update_server(self, path, method='GET', data=None):
        """Proxy a request to the update server hosting API.

        Uses the shop's stored JWT token for authentication.
        The browser never sees the JWT — this acts as a secure proxy.
        """
        import requests as req
        config = UpdateServerConfig.get_instance()
        if not config.server_url or not config.jwt_token:
            return {'error': 'Update server not configured'}, 503

        # Refresh token if needed
        if not config.is_jwt_valid():
            try:
                from component_updates.services import UpdateManager
                manager = UpdateManager()
                manager._ensure_authenticated()
                config.refresh_from_db()
            except Exception as e:
                return {'error': f'Authentication failed: {e}'}, 503

        url = f'{config.server_url.rstrip("/")}/api/v1/hosting/{path}'
        headers = {
            'Authorization': f'Bearer {config.jwt_token}',
            'Content-Type': 'application/json',
        }
        try:
            if method == 'GET':
                resp = req.get(url, headers=headers, timeout=15)
            else:
                resp = req.post(url, headers=headers, json=data or {}, timeout=15)
            return resp.json(), resp.status_code
        except req.RequestException as e:
            return {'error': f'Update server unreachable: {e}'}, 503
        except ValueError:
            return {'error': 'Invalid response from update server'}, 502

    def hosted_upgrade_view(self, request):
        """Hosted upgrade scheduling page for Spwig-hosted merchants."""
        from core.license import get_license_manager
        if not get_license_manager().is_spwig_hosted():
            from django.shortcuts import redirect
            from django.urls import reverse
            return redirect(reverse('admin:component_updates_platformupdate_changelist'))

        service = PlatformUpdateService()
        current_version = service.get_current_version()

        # Pass update server details for direct browser polling during upgrade
        config = UpdateServerConfig.get_instance()
        progress_url = ''
        if config.server_url and config.installation_uuid:
            progress_url = (
                f'{config.server_url.rstrip("/")}/api/v1/hosting/upgrades/progress/'
                f'{config.installation_uuid}/'
            )

        return render(request, 'admin/component_updates/platformupdate/hosted_upgrade.html', {
            'title': _('Platform Updates'),
            'opts': self.model._meta,
            'current_version': current_version,
            'direct_progress_url': progress_url,
        })

    def hosted_upgrade_check_api(self, request):
        """Proxy: check for available updates via update server."""
        data, status_code = self._proxy_to_update_server('upgrades/check/')
        return JsonResponse(data, status=status_code)

    def hosted_upgrade_schedule_api(self, request):
        """Proxy: schedule or trigger an upgrade via update server."""
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)
        import json
        try:
            body = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        data, status_code = self._proxy_to_update_server(
            'upgrades/schedule/', method='POST', data=body,
        )
        return JsonResponse(data, status=status_code)

    def hosted_upgrade_status_api(self, request):
        """Proxy: get upgrade status/progress via update server."""
        data, status_code = self._proxy_to_update_server('upgrades/status/')
        return JsonResponse(data, status=status_code)

    def hosted_upgrade_snooze_api(self, request):
        """Proxy: snooze upgrade notification via update server."""
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)
        import json
        try:
            body = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        data, status_code = self._proxy_to_update_server(
            'upgrades/snooze/', method='POST', data=body,
        )
        return JsonResponse(data, status=status_code)

    def hosted_upgrade_cancel_api(self, request):
        """Proxy: cancel a scheduled upgrade via update server."""
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)
        data, status_code = self._proxy_to_update_server(
            'upgrades/cancel/', method='POST',
        )
        return JsonResponse(data, status=status_code)

    def has_add_permission(self, request):
        # Updates are started via the check/start flow, not via add form
        return False

    def has_change_permission(self, request, obj=None):
        # Updates are read-only
        return False

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of update records
        return False
