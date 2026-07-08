from django.contrib import admin
from django.utils.html import mark_safe, format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import (
    DesignToken, ComponentStyle, GlobalDesignSettings, CustomCSS,
    PageTier, ComponentStore, TierComponentPermission,
    ComponentValidationReport
)
from .theme_models import Theme, ThemeInstallation, ThemeAsset
from component_updates.models import ComponentRegistry

# Import enhanced admin configurations (these auto-register via decorators)
from . import header_footer_admin
from . import branding_admin  # Enhanced branding admin replaces the basic one

@admin.register(DesignToken)
class DesignTokenAdmin(admin.ModelAdmin):
    """Admin interface for tier-aware design tokens with priority cascade"""
    change_list_template = 'admin/design/designtoken/change_list.html'
    list_display = [
        'name', 'token_type', 'value', 'source',
        'priority_level', 'tier_display', 'is_locked_display', 'is_active'
    ]
    list_filter = ['token_type', 'source', 'priority_level', 'is_locked', 'is_active']
    search_fields = ['name', 'value', 'description']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['theme', 'component']
    actions = [
        'sync_theme_tokens', 'sync_all_theme_tokens',
        'cleanup_orphaned_tokens', 'delete_tokens_for_inactive_themes',
    ]

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'token_type', 'value', 'description')
        }),
        (_('Priority & Source'), {
            'fields': ('source', 'priority_level', 'theme', 'component'),
            'description': _(
                'Token priority cascade: 1=Brand Builder (highest), '
                '2=Theme, 3=Component, 4=System (lowest). '
                'Lower number = higher priority in resolution. '
                'Set theme for theme tokens, component for component tokens.'
            )
        }),
        (_('Tier Restrictions'), {
            'fields': ('tier_restriction',),
            'description': _(
                'Select tiers where this token is available. '
                'Empty = all tiers. Options: A (System-Critical), '
                'B (Semi-Critical), C (Marketing).'
            )
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_locked'),
            'description': _(
                'Locked tokens cannot have their name changed. '
                'Theme tokens are locked by default to maintain consistency.'
            )
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def tier_display(self, obj):
        """Display tier restrictions in admin list"""
        if not obj.tier_restriction:
            return _('All Tiers')
        return ', '.join(sorted(obj.tier_restriction))
    tier_display.short_description = _('Available Tiers')

    def is_locked_display(self, obj):
        """Display lock indicator for locked tokens"""
        if obj.is_locked:
            return format_html(
                '<span style="color: #666; font-size: 1.1em;" title="{}">🔒</span>',
                _('This token is locked and cannot be renamed')
            )
        return ''
    is_locked_display.short_description = ''
    is_locked_display.admin_order_field = 'is_locked'

    def get_readonly_fields(self, request, obj=None):
        """Make name and is_locked read-only for theme tokens"""
        readonly = list(self.readonly_fields)
        if obj:
            # Theme tokens: name and is_locked are always read-only
            if obj.source == 'theme':
                readonly.extend(['name', 'is_locked', 'source', 'theme'])
            # Other locked tokens: only name is read-only
            elif obj.is_locked:
                readonly.append('name')
        return readonly

    def changelist_view(self, request, extra_context=None):
        """Add custom context for filters"""
        extra_context = extra_context or {}
        extra_context['token_types'] = DesignToken.TOKEN_TYPES
        extra_context['sources'] = DesignToken.SOURCE_CHOICES
        extra_context['priorities'] = DesignToken.PRIORITY_CHOICES
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        """Ensure theme tokens remain locked"""
        if obj.source == 'theme':
            obj.is_locked = True  # Enforce locked status for theme tokens
        super().save_model(request, obj, form, change)

    @admin.action(description=_('Sync selected theme tokens'))
    def sync_theme_tokens(self, request, queryset):
        """Sync selected theme tokens from their theme manifest"""
        from .token_sync_service import TokenSyncService

        themes_synced = set()
        for token in queryset.filter(source='theme', theme__isnull=False):
            if token.theme_id not in themes_synced:
                TokenSyncService.sync_theme_to_design_tokens(token.theme)
                themes_synced.add(token.theme_id)

        self.message_user(
            request,
            _('Synced tokens from %(count)d theme(s)') % {'count': len(themes_synced)}
        )

    @admin.action(description=_('Sync ALL theme tokens (all active themes)'))
    def sync_all_theme_tokens(self, request, queryset):
        """Sync tokens from all active themes"""
        from .token_sync_service import TokenSyncService

        total_created = 0
        total_updated = 0
        total_deleted = 0
        themes_count = 0

        for theme in Theme.objects.filter(is_active=True):
            created, updated, deleted = TokenSyncService.sync_theme_to_design_tokens(theme)
            total_created += created
            total_updated += updated
            total_deleted += deleted
            themes_count += 1

        self.message_user(
            request,
            _('Synced %(themes)d theme(s): %(created)d created, %(updated)d updated, %(deleted)d deleted') % {
                'themes': themes_count,
                'created': total_created,
                'updated': total_updated,
                'deleted': total_deleted
            }
        )

    @admin.action(description=_('Clean up orphaned tokens'))
    def cleanup_orphaned_tokens(self, request, queryset):
        """Delete tokens where source=theme but theme FK is null, or source=component but component FK is null."""
        orphaned_theme_count, _ = DesignToken.objects.filter(
            source='theme', theme__isnull=True
        ).delete()
        orphaned_component_count, _ = DesignToken.objects.filter(
            source='component', component__isnull=True
        ).delete()

        total = orphaned_theme_count + orphaned_component_count
        if total > 0:
            self.message_user(
                request,
                _('Deleted %(total)d orphaned token(s): %(theme)d theme, %(component)d component') % {
                    'total': total,
                    'theme': orphaned_theme_count,
                    'component': orphaned_component_count,
                }
            )
        else:
            self.message_user(request, _('No orphaned tokens found'))

    @admin.action(description=_('Delete tokens for inactive themes'))
    def delete_tokens_for_inactive_themes(self, request, queryset):
        """Delete theme tokens for themes where is_active=False."""
        inactive_themes = Theme.objects.filter(is_active=False)
        deleted_count, _ = DesignToken.objects.filter(
            source='theme', theme__in=inactive_themes
        ).delete()

        self.message_user(
            request,
            _('Deleted %(count)d token(s) from %(themes)d inactive theme(s)') % {
                'count': deleted_count,
                'themes': inactive_themes.count(),
            }
        )

# ThemePreset removed - using Theme model instead

@admin.register(ComponentStyle)
class ComponentStyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'component_type', 'is_active']
    list_filter = ['component_type', 'is_active']

@admin.register(GlobalDesignSettings)
class GlobalDesignSettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomCSS)
class CustomCSSAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'load_order']
    list_filter = ['is_active']
    ordering = ['load_order']


class TierComponentPermissionInline(admin.TabularInline):
    """Inline for tier component permissions"""
    model = TierComponentPermission
    extra = 1
    fields = ['component', 'allowed_regions', 'max_instances']
    autocomplete_fields = ['component']


@admin.register(PageTier)
class PageTierAdmin(admin.ModelAdmin):
    """Admin interface for page tier security configuration"""
    list_display = [
        'page_type', 'tier', 'display_name',
        'max_external_scripts', 'allows_custom_html',
        'created_at'
    ]
    list_filter = ['tier', 'allows_custom_html']
    search_fields = ['page_type', 'display_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [TierComponentPermissionInline]

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('page_type', 'tier', 'display_name', 'description')
        }),
        (_('Page Structure'), {
            'fields': ('schema', 'locked_regions'),
            'classes': ('collapse',)
        }),
        (_('Security Settings'), {
            'fields': (
                'csp_policy',
                'max_external_scripts',
                'allows_custom_html'
            ),
            'description': (
                'Security configuration for this page tier. '
                'Tier A has strictest settings, Tier C most flexible.'
            )
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        """Make page_type readonly after creation to prevent breaking references"""
        if obj:  # Editing existing object
            return self.readonly_fields + ('page_type',)
        return self.readonly_fields


class ValidationReportInline(admin.TabularInline):
    """Inline for component validation reports."""
    model = ComponentValidationReport
    extra = 0
    readonly_fields = [
        'validated_at', 'validated_by', 'is_valid',
        'version_validated', 'error_count_display', 'warning_count_display'
    ]
    fields = [
        'validated_at', 'validated_by', 'is_valid',
        'version_validated', 'error_count_display', 'warning_count_display'
    ]
    can_delete = False
    ordering = ['-validated_at']

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description=_('Errors'))
    def error_count_display(self, obj):
        """Display error count with color."""
        count = obj.error_count()
        if count > 0:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">{}</span>',
                count
            )
        return count

    @admin.display(description=_('Warnings'))
    def warning_count_display(self, obj):
        """Display warning count with color."""
        count = obj.warning_count()
        if count > 0:
            return format_html(
                '<span style="color: #ffc107;">{}</span>',
                count
            )
        return count


@admin.register(ComponentStore)
class ComponentStoreAdmin(admin.ModelAdmin):
    """Admin interface for component registry"""
    list_display = [
        'component_type', 'display_name', 'version', 'author',
        'review_status', 'validation_status', 'signature_status',
        'render_mode', 'script_budget_kb', 'created_at'
    ]
    list_filter = ['review_status', 'render_mode', 'author', 'created_at']
    search_fields = ['component_type', 'display_name', 'author', 'description']
    readonly_fields = [
        'checksum_sha256', 'signature', 'signed_by', 'signed_at',
        'created_at', 'updated_at', 'reviewed_at'
    ]
    actions = [
        'sign_components', 'verify_components', 'validate_components',
        'approve_components', 'reject_components', 'suspend_components',
        'apply_system_permissions', 'apply_marketing_permissions',
        'apply_product_permissions', 'remove_all_permissions'
    ]
    inlines = [ValidationReportInline]

    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'component_type', 'display_name', 'description',
                'version', 'author'
            )
        }),
        (_('Capabilities & Restrictions'), {
            'fields': (
                'capabilities', 'allowed_tiers', 'render_mode'
            )
        }),
        (_('Security Settings'), {
            'fields': (
                'external_domains', 'script_budget_kb',
                'requires_sandbox'
            ),
            'description': 'Security configuration for this component'
        }),
        (_('Distribution'), {
            'fields': (
                'package_file', 'signature', 'checksum_sha256',
                'signed_by', 'signed_at'
            ),
            'classes': ('collapse',)
        }),
        (_('Review'), {
            'fields': (
                'review_status', 'reviewed_by', 'reviewed_at',
                'review_notes'
            ),
            'description': 'Component review and approval status'
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        """Make component_type readonly after creation"""
        if obj:  # Editing existing object
            return self.readonly_fields + ('component_type',)
        return self.readonly_fields

    @admin.display(description=_('Signature Status'))
    def signature_status(self, obj):
        """Display signature status with color indicator."""
        from django.utils.html import format_html

        if obj.is_signed():
            # Verify signature
            is_valid, message = obj.verify_integrity()
            if is_valid:
                return format_html(
                    '<span style="color: #28a745;">● {}</span>',
                    _('Signed')
                )
            else:
                return format_html(
                    '<span style="color: #dc3545;">● {}</span>',
                    _('Invalid')
                )
        else:
            return format_html(
                '<span style="color: #6c757d;">○ {}</span>',
                _('Unsigned')
            )

    @admin.action(description=_('Sign selected components'))
    def sign_components(self, request, queryset):
        """Sign selected components."""
        from design.component_signer import get_component_signer

        signed_count = 0
        failed_count = 0
        signer = get_component_signer()

        for component in queryset:
            # Only sign approved components
            if component.review_status != 'approved':
                self.message_user(
                    request,
                    _('Skipped %(component)s - not approved') % {
                        'component': component
                    },
                    level='warning'
                )
                continue

            success, message = component.sign_package()
            if success:
                component.save()
                signed_count += 1
            else:
                failed_count += 1
                self.message_user(
                    request,
                    _('Failed to sign %(component)s: %(error)s') % {
                        'component': component,
                        'error': message
                    },
                    level='error'
                )

        if signed_count > 0:
            self.message_user(
                request,
                _('Successfully signed %(count)d component(s)') % {
                    'count': signed_count
                },
                level='success'
            )

    @admin.action(description=_('Verify component signatures'))
    def verify_components(self, request, queryset):
        """Verify signatures of selected components."""
        valid_count = 0
        invalid_count = 0
        unsigned_count = 0

        for component in queryset:
            if not component.is_signed():
                unsigned_count += 1
                continue

            is_valid, message = component.verify_integrity()
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                self.message_user(
                    request,
                    _('%(component)s: %(message)s') % {
                        'component': component,
                        'message': message
                    },
                    level='error'
                )

        # Summary message
        summary_parts = []
        if valid_count > 0:
            summary_parts.append(_('%(count)d valid') % {'count': valid_count})
        if invalid_count > 0:
            summary_parts.append(_('%(count)d invalid') % {'count': invalid_count})
        if unsigned_count > 0:
            summary_parts.append(_('%(count)d unsigned') % {'count': unsigned_count})

        self.message_user(
            request,
            _('Verification complete: %(summary)s') % {
                'summary': ', '.join(summary_parts)
            },
            level='success' if invalid_count == 0 else 'warning'
        )

    @admin.display(description=_('Validation Status'))
    def validation_status(self, obj):
        """Display latest validation status with color indicator."""
        from django.utils.html import format_html

        # Get latest validation report
        latest_report = obj.validation_reports.first()

        if not latest_report:
            return format_html(
                '<span style="color: #6c757d;">○ {}</span>',
                _('Not Validated')
            )

        if latest_report.is_valid:
            if latest_report.warning_count() > 0:
                return format_html(
                    '<span style="color: #ffc107;">● {} ({}w)</span>',
                    _('Valid'),
                    latest_report.warning_count()
                )
            else:
                return format_html(
                    '<span style="color: #28a745;">● {}</span>',
                    _('Valid')
                )
        else:
            return format_html(
                '<span style="color: #dc3545;">● {} ({}e)</span>',
                _('Invalid'),
                latest_report.error_count()
            )

    @admin.action(description=_('Validate selected components'))
    def validate_components(self, request, queryset):
        """Run validation pipeline on selected components."""
        from design.component_validator import ComponentValidator

        validated_count = 0
        valid_count = 0
        invalid_count = 0

        for component in queryset:
            # Run validation
            validator = ComponentValidator(component)
            is_valid, errors, warnings = validator.validate()

            # Create validation report
            report = ComponentValidationReport.objects.create(
                component=component,
                validated_by=request.user,
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                version_validated=component.version
            )

            validated_count += 1
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                # Show first error for each invalid component
                if errors:
                    self.message_user(
                        request,
                        _('%(component)s: %(error)s') % {
                            'component': component,
                            'error': errors[0]
                        },
                        level='error'
                    )

        # Summary message
        summary = []
        if valid_count > 0:
            summary.append(_('%(count)d valid') % {'count': valid_count})
        if invalid_count > 0:
            summary.append(_('%(count)d invalid') % {'count': invalid_count})

        self.message_user(
            request,
            _('Validated %(total)d component(s): %(summary)s') % {
                'total': validated_count,
                'summary': ', '.join(summary)
            },
            level='success' if invalid_count == 0 else 'warning'
        )

    @admin.action(description=_('Approve selected components'))
    def approve_components(self, request, queryset):
        """Approve components after validation."""
        from django.utils import timezone

        approved_count = 0
        skipped_count = 0

        for component in queryset:
            # Check if component has been validated
            latest_report = component.validation_reports.first()

            if not latest_report:
                self.message_user(
                    request,
                    _('%(component)s has not been validated') % {
                        'component': component
                    },
                    level='warning'
                )
                skipped_count += 1
                continue

            # Check if validation passed
            if not latest_report.is_valid:
                self.message_user(
                    request,
                    _('%(component)s has validation errors') % {
                        'component': component
                    },
                    level='error'
                )
                skipped_count += 1
                continue

            # Check if component is signed
            if not component.is_signed():
                self.message_user(
                    request,
                    _('%(component)s is not signed') % {
                        'component': component
                    },
                    level='warning'
                )
                skipped_count += 1
                continue

            # Approve component
            component.review_status = 'approved'
            component.reviewed_by = request.user
            component.reviewed_at = timezone.now()
            component.save()
            approved_count += 1

        if approved_count > 0:
            self.message_user(
                request,
                _('Approved %(count)d component(s)') % {'count': approved_count},
                level='success'
            )
        if skipped_count > 0:
            self.message_user(
                request,
                _('Skipped %(count)d component(s)') % {'count': skipped_count},
                level='warning'
            )

    @admin.action(description=_('Reject selected components'))
    def reject_components(self, request, queryset):
        """Reject components with reason."""
        from django.utils import timezone

        # For simplicity, we'll reject with a generic message
        # In a real implementation, you might want a form to collect rejection reason
        rejected_count = queryset.update(
            review_status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
            review_notes='Rejected by admin'
        )

        self.message_user(
            request,
            _('Rejected %(count)d component(s)') % {'count': rejected_count},
            level='success'
        )

    @admin.action(description=_('Suspend selected components'))
    def suspend_components(self, request, queryset):
        """Suspend components (remove from use but keep in registry)."""
        from django.utils import timezone

        suspended_count = 0

        for component in queryset:
            # Only suspend approved components
            if component.review_status != 'approved':
                continue

            component.review_status = 'suspended'
            component.reviewed_by = request.user
            component.reviewed_at = timezone.now()
            component.review_notes = 'Suspended by admin - security or quality concerns'
            component.save()
            suspended_count += 1

        self.message_user(
            request,
            _('Suspended %(count)d component(s)') % {'count': suspended_count},
            level='success'
        )

    @admin.action(description=_('Apply system permissions (all tiers)'))
    def apply_system_permissions(self, request, queryset):
        """Apply system component permissions (allowed in all tiers)."""
        from design.component_permissions import apply_permission_template

        total_permissions = 0
        for component in queryset:
            permissions = apply_permission_template(component, 'system')
            total_permissions += len(permissions)

        self.message_user(
            request,
            _('Applied system permissions to %(count)d component(s), '
              'created %(perms)d tier permissions') % {
                'count': queryset.count(),
                'perms': total_permissions
            },
            level='success'
        )

    @admin.action(description=_('Apply marketing permissions (Tier C only)'))
    def apply_marketing_permissions(self, request, queryset):
        """Apply marketing component permissions (Tier C only)."""
        from design.component_permissions import apply_permission_template

        total_permissions = 0
        for component in queryset:
            permissions = apply_permission_template(component, 'marketing')
            total_permissions += len(permissions)

        self.message_user(
            request,
            _('Applied marketing permissions to %(count)d component(s), '
              'created %(perms)d tier permissions') % {
                'count': queryset.count(),
                'perms': total_permissions
            },
            level='success'
        )

    @admin.action(description=_('Apply product permissions (Tier B, C)'))
    def apply_product_permissions(self, request, queryset):
        """Apply product component permissions (Tier B and C)."""
        from design.component_permissions import apply_permission_template

        total_permissions = 0
        for component in queryset:
            permissions = apply_permission_template(component, 'product')
            total_permissions += len(permissions)

        self.message_user(
            request,
            _('Applied product permissions to %(count)d component(s), '
              'created %(perms)d tier permissions') % {
                'count': queryset.count(),
                'perms': total_permissions
            },
            level='success'
        )

    @admin.action(description=_('Remove all tier permissions'))
    def remove_all_permissions(self, request, queryset):
        """Remove all tier permissions from selected components."""
        from design.component_permissions import remove_all_permissions

        total_deleted = 0
        for component in queryset:
            deleted = remove_all_permissions(component)
            total_deleted += deleted

        self.message_user(
            request,
            _('Removed %(count)d tier permissions from %(components)d component(s)') % {
                'count': total_deleted,
                'components': queryset.count()
            },
            level='success'
        )


@admin.register(ComponentValidationReport)
class ComponentValidationReportAdmin(admin.ModelAdmin):
    """Admin interface for component validation reports."""
    list_display = [
        'component', 'validated_at', 'validated_by',
        'is_valid', 'error_count_display', 'warning_count_display',
        'version_validated'
    ]
    list_filter = ['is_valid', 'validated_at', 'validated_by']
    search_fields = ['component__component_type', 'component__display_name']
    readonly_fields = [
        'component', 'validated_at', 'validated_by', 'is_valid',
        'errors_display', 'warnings_display', 'version_validated'
    ]

    fieldsets = (
        (_('Validation Info'), {
            'fields': ('component', 'validated_at', 'validated_by', 'version_validated')
        }),
        (_('Results'), {
            'fields': ('is_valid', 'errors_display', 'warnings_display')
        }),
    )

    def has_add_permission(self, request):
        """Validation reports are created automatically."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Keep validation history."""
        return False

    @admin.display(description=_('Errors'))
    def error_count_display(self, obj):
        """Display error count with color."""
        count = obj.error_count()
        if count > 0:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">{}</span>',
                count
            )
        return 0

    @admin.display(description=_('Warnings'))
    def warning_count_display(self, obj):
        """Display warning count with color."""
        count = obj.warning_count()
        if count > 0:
            return format_html(
                '<span style="color: #ffc107;">{}</span>',
                count
            )
        return 0

    @admin.display(description=_('Errors'))
    def errors_display(self, obj):
        """Display errors as formatted list."""
        if not obj.errors:
            return format_html('<span style="color: #28a745;">{}</span>', _('None'))

        errors_html = '<ul style="margin: 0; padding-left: 20px;">'
        for error in obj.errors:
            errors_html += f'<li style="color: #dc3545;">{error}</li>'
        errors_html += '</ul>'
        return format_html(errors_html)

    @admin.display(description=_('Warnings'))
    def warnings_display(self, obj):
        """Display warnings as formatted list."""
        if not obj.warnings:
            return format_html('<span style="color: #28a745;">{}</span>', _('None'))

        warnings_html = '<ul style="margin: 0; padding-left: 20px;">'
        for warning in obj.warnings:
            warnings_html += f'<li style="color: #ffc107;">{warning}</li>'
        warnings_html += '</ul>'
        return format_html(warnings_html)


# Theme System Admin Classes

class ThemeAssetInline(admin.TabularInline):
    """Inline for theme assets"""
    model = ThemeAsset
    extra = 0
    readonly_fields = ['asset_type', 'path', 'size', 'mime_type']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    """Admin interface for themes"""
    list_display = [
        'name', 'version', 'slug', 'author',
        'is_active', 'is_default', 'is_marketplace',
        'created_at'
    ]
    list_filter = ['is_active', 'is_default', 'is_marketplace', 'created_at']
    search_fields = ['name', 'slug', 'author', 'description']
    actions = ['sync_tokens_for_selected']
    readonly_fields = [
        'package_checksum', 'extracted_path',
        'installed_at', 'created_at', 'updated_at'
    ]

    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'name', 'slug', 'version', 'description',
                'author', 'author_email', 'author_website', 'license'
            )
        }),
        (_('Compatibility'), {
            'fields': ('engine_min_version', 'engine_max_version', 'feature_flags')
        }),
        (_('Package'), {
            'fields': (
                'package_file', 'package_checksum',
                'extracted_path'
            )
        }),
        (_('Configuration'), {
            'fields': ('manifest', 'token_migrations', 'preview_images')
        }),
        (_('Status'), {
            'fields': (
                'is_active', 'is_default', 'is_marketplace',
                'created_by', 'installed_at', 'created_at', 'updated_at'
            )
        })
    )

    inlines = [ThemeAssetInline]

    @admin.action(description=_('Sync design tokens for selected themes'))
    def sync_tokens_for_selected(self, request, queryset):
        """Run TokenSyncService for selected themes to populate DesignToken records."""
        from .token_sync_service import TokenSyncService

        total_created = 0
        total_updated = 0
        total_deleted = 0

        for theme in queryset:
            created, updated, deleted = TokenSyncService.sync_theme_to_design_tokens(theme)
            total_created += created
            total_updated += updated
            total_deleted += deleted

        self.message_user(
            request,
            _('Synced %(count)d theme(s): %(created)d created, %(updated)d updated, %(deleted)d deleted') % {
                'count': queryset.count(),
                'created': total_created,
                'updated': total_updated,
                'deleted': total_deleted,
            }
        )

    def get_urls(self):
        """Add custom admin URLs for unified theme management"""
        from django.urls import path
        from .unified_theme_views import (
            unified_theme_management_view,
            activate_theme_ajax,
            rollback_theme_ajax,
            install_theme_ajax,
            uninstall_theme_ajax,
            check_theme_updates_ajax,
            get_theme_detail_ajax,
        )

        urls = super().get_urls()
        custom_urls = [
            # Unified management view (modern marketplace-style UI)
            path('unified/', unified_theme_management_view, name='unified_theme_management'),
            path('activate/<slug:slug>/', activate_theme_ajax, name='activate_theme'),
            path('rollback/<slug:slug>/', rollback_theme_ajax, name='rollback_theme'),
            path('install/<slug:slug>/', install_theme_ajax, name='install_theme'),
            path('uninstall/<slug:slug>/', uninstall_theme_ajax, name='uninstall_theme'),
            path('check-updates/', check_theme_updates_ajax, name='check_theme_updates'),
            path('detail/<slug:slug>/', get_theme_detail_ajax, name='get_theme_detail'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """Redirect to unified theme management view"""
        from django.shortcuts import redirect
        return redirect('admin:unified_theme_management')


# ThemeBrandingAdmin is now imported from branding_admin.py with enhanced UI


@admin.register(ThemeInstallation)
class ThemeInstallationAdmin(admin.ModelAdmin):
    """Admin interface for theme installations"""
    list_display = [
        'theme', 'installed_at', 'installed_by',
        'previous_theme', 'has_migrations'
    ]
    list_filter = ['installed_at', 'theme']
    readonly_fields = [
        'theme', 'installed_at', 'installed_by',
        'previous_theme', 'customization_snapshot',
        'migrations_applied'
    ]

    def has_migrations(self, obj):
        """Check if migrations were applied"""
        return bool(obj.migrations_applied)
    has_migrations.boolean = True
    has_migrations.short_description = 'Migrations Applied'

    def has_add_permission(self, request):
        """Prevent manual creation"""
        return False


@admin.register(ThemeAsset)
class ThemeAssetAdmin(admin.ModelAdmin):
    """Admin interface for theme assets"""
    list_display = [
        'path', 'theme', 'asset_type', 'size',
        'is_critical', 'route', 'created_at'
    ]
    list_filter = ['asset_type', 'is_critical', 'theme']
    search_fields = ['path', 'theme__name']
    readonly_fields = ['size', 'checksum', 'mime_type', 'created_at']

    def has_add_permission(self, request):
        """Assets are auto-created during theme installation"""
        return False


# Widget admin is in header_footer_admin.py
# Widget package system has been removed - widgets are now baked into the platform
