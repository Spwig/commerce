"""
Admin configuration for accounts app
Includes OAuth provider settings, social app management, and User admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from django.urls import path, reverse
from django.db.models import Q, Count
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from .models import (
    CustomerProfile,
    OAuthProviderSettings,
    StaffMember,
    CommunicationPreference,
    PreferenceChangeLog,
)

User = get_user_model()


# Note: CustomerProfile is registered in customers/admin.py with enhanced analytics
# We only register OAuth-specific models here

@admin.register(OAuthProviderSettings)
class OAuthProviderSettingsAdmin(admin.ModelAdmin):
    """Admin interface for OAuth provider settings - accessible via OAuth Dashboard only"""
    change_form_template = 'admin/accounts/oauthprovidersettings/change_form.html'

    list_display = [
        'provider_display',
        'enabled_status',
        'configuration_status',
        'button_order',
        'updated_at'
    ]
    list_filter = ['enabled', 'is_configured', 'provider']
    search_fields = ['provider', 'display_name']
    ordering = ['button_order', 'provider']

    def has_module_permission(self, request):
        """Hide from admin index - access via OAuth Dashboard instead"""
        return False

    fieldsets = (
        (_('Provider Configuration'), {
            'fields': ('provider', 'display_name', 'enabled', 'button_order'),
            'classes': ('tab-basic',),
        }),
        (_('Advanced Settings'), {
            'fields': ('custom_scopes', 'configuration_notes'),
            'classes': ('tab-advanced',),
        }),
        (_('Status'), {
            'fields': ('is_configured',),
            'classes': ('tab-status',),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('tab-timestamps',),
        }),
    )

    readonly_fields = ['is_configured', 'created_at', 'updated_at']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        return super().change_view(request, object_id, form_url, extra_context)

    def provider_display(self, obj):
        """Display provider with icon"""
        icons = {
            'google': '🔍',
            'apple': '🍎',
            'microsoft': '🪟',
        }
        icon = icons.get(obj.provider, '🔐')
        return format_html(
            '<span style="font-size: 16px;">{} {}</span>',
            icon,
            obj.get_provider_display()
        )
    provider_display.short_description = _('Provider')

    def enabled_status(self, obj):
        """Display enabled status with color"""
        if obj.enabled:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Enabled</span>'
            )
        return format_html(
            '<span style="color: gray;">○ Disabled</span>'
        )
    enabled_status.short_description = _('Status')

    def configuration_status(self, obj):
        """Display configuration status with color"""
        if obj.is_configured:
            return format_html(
                '<span style="color: green;">✓ Configured</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Not Configured</span>'
        )
    configuration_status.short_description = _('OAuth Credentials')

    def get_form(self, request, obj=None, **kwargs):
        """Add helpful text to form fields"""
        form = super().get_form(request, obj, **kwargs)

        form.base_fields['provider'].help_text = _(
            'Select OAuth provider. Configure credentials in Social Applications section below.'
        )
        form.base_fields['display_name'].help_text = _(
            'Name shown on customer login button (e.g., "Sign in with Google")'
        )
        form.base_fields['enabled'].help_text = _(
            'Show this provider to customers. Provider must be configured first.'
        )
        form.base_fields['button_order'].help_text = _(
            'Display order (lower numbers appear first)'
        )

        return form

    def save_model(self, request, obj, form, change):
        """Add helpful message after saving"""
        super().save_model(request, obj, form, change)

        if obj.enabled and not obj.is_configured:
            self.message_user(
                request,
                _(
                    f'Warning: {obj.get_provider_display()} is enabled but not configured. '
                    f'Please add OAuth credentials in Social Applications.'
                ),
                level='WARNING'
            )


# Customize SocialApp admin for better merchant experience
class CustomSocialAppAdmin(admin.ModelAdmin):
    """Enhanced admin for Social Applications (OAuth credentials) - accessible via OAuth Dashboard only"""
    list_display = ['name', 'provider_display', 'has_credentials', 'sites_list']
    list_filter = ['provider']
    filter_horizontal = ['sites']

    def has_module_permission(self, request):
        """Hide from admin index - access via OAuth Dashboard instead"""
        return False

    fieldsets = (
        (_('Provider Information'), {
            'fields': ('provider', 'name', 'sites'),
            'description': _(
                'Select the OAuth provider and give it a descriptive name. '
                'Make sure to add your site to the Sites list.'
            )
        }),
        (_('OAuth Credentials'), {
            'fields': ('client_id', 'secret', 'key'),
            'description': _(
                '<strong>How to get credentials:</strong><br>'
                '<ul>'
                '<li><strong>Google:</strong> Visit <a href="https://console.cloud.google.com" target="_blank">Google Cloud Console</a></li>'
                '<li><strong>Apple:</strong> Visit <a href="https://developer.apple.com" target="_blank">Apple Developer Portal</a></li>'
                '<li><strong>Microsoft:</strong> Visit <a href="https://portal.azure.com" target="_blank">Azure Portal</a></li>'
                '</ul>'
                'See documentation for detailed setup instructions.'
            )
        }),
    )

    def provider_display(self, obj):
        """Display provider with icon"""
        icons = {
            'google': '🔍 Google',
            'apple': '🍎 Apple',
            'microsoft': '🪟 Microsoft',
        }
        return icons.get(obj.provider, obj.provider.title())
    provider_display.short_description = _('Provider')

    def has_credentials(self, obj):
        """Check if credentials are configured"""
        has_creds = bool(obj.client_id and (obj.secret or obj.provider == 'apple'))
        if has_creds:
            return format_html('<span style="color: green;">✓ Yes</span>')
        return format_html('<span style="color: red;">✗ No</span>')
    has_credentials.boolean = False
    has_credentials.short_description = _('Has Credentials')

    def sites_list(self, obj):
        """Display associated sites"""
        sites = obj.sites.all()
        if sites:
            return ', '.join([site.domain for site in sites])
        return format_html('<span style="color: red;">No sites configured!</span>')
    sites_list.short_description = _('Sites')

    def save_model(self, request, obj, form, change):
        """Validate and provide helpful messages"""
        super().save_model(request, obj, form, change)

        if not obj.client_id:
            self.message_user(
                request,
                _('Remember to add the Client ID from your OAuth provider.'),
                level='WARNING'
            )

        if not obj.sites.exists():
            self.message_user(
                request,
                _('Remember to add your site to the Sites list!'),
                level='WARNING'
            )


# Unregister default SocialApp admin and register custom one
admin.site.unregister(SocialApp)
admin.site.register(SocialApp, CustomSocialAppAdmin)


# Optional: Customize SocialAccount admin for debugging
class CustomSocialAccountAdmin(admin.ModelAdmin):
    """Admin for viewing social account connections"""
    list_display = ['user', 'provider', 'uid', 'date_joined']
    list_filter = ['provider', 'date_joined']
    search_fields = ['user__email', 'uid']
    readonly_fields = ['user', 'provider', 'uid', 'extra_data', 'date_joined']

    def has_add_permission(self, request):
        """Disable manual creation"""
        return False


# Unregister default and register custom
admin.site.unregister(SocialAccount)
admin.site.register(SocialAccount, CustomSocialAccountAdmin)


# ============================================================================
# Custom User Admin with 2FA Status
# ============================================================================

class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User admin with 2FA status column and staff profile link"""

    list_display = [
        'email',
        'display_roles',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'mfa_status_display',
        'date_joined',
    ]

    list_filter = BaseUserAdmin.list_filter + ('date_joined',)

    def display_roles(self, obj):
        """Show colored role badges for the user."""
        from staff_roles.services import get_user_roles
        roles = get_user_roles(obj)
        if obj.is_superuser and not roles:
            return format_html(
                '<span style="background: #7c3aed; color: #fff; padding: 2px 8px; '
                'border-radius: 10px; font-size: 11px;">Owner</span>'
            )
        if not roles:
            return format_html('<span style="color: var(--body-quiet-color);">—</span>')
        color_map = {
            'primary': '#7c3aed', 'success': '#22c55e', 'warning': '#f59e0b',
            'error': '#ef4444', 'info': '#06b6d4', 'default': '#6b7280',
        }
        badges = []
        for role in roles:
            bg = color_map.get(role.color, '#6b7280')
            badges.append(
                '<span style="background: {}; color: #fff; padding: 2px 8px; '
                'border-radius: 10px; font-size: 11px; margin-right: 4px;">'
                '{}</span>'.format(bg, role.display_name)
            )
        return format_html(''.join(badges))
    display_roles.short_description = _('Roles')

    def mfa_status_display(self, obj):
        """Display MFA status with color-coded badge"""
        try:
            from allauth.mfa.utils import is_mfa_enabled
            if is_mfa_enabled(obj):
                return format_html(
                    '<span style="display: inline-block; padding: 3px 8px; '
                    'background: #d4edda; color: #155724; border-radius: 4px; '
                    'font-size: 11px; font-weight: 600;">'
                    '<i class="fas fa-check-circle"></i> Enabled</span>'
                )
            else:
                return format_html(
                    '<span style="display: inline-block; padding: 3px 8px; '
                    'background: #f8d7da; color: #721c24; border-radius: 4px; '
                    'font-size: 11px; font-weight: 600;">'
                    '<i class="fas fa-times-circle"></i> Not Enabled</span>'
                )
        except ImportError:
            return format_html(
                '<span style="color: var(--body-quiet-color);">-</span>'
            )
    mfa_status_display.short_description = _('2FA Status')
    mfa_status_display.admin_order_field = None  # Can't order by this field

    def get_urls(self):
        """Add custom URLs for staff profile and MFA verification"""
        urls = super().get_urls()
        custom_urls = [
            path(
                'staff-profile/',
                self.admin_site.admin_view(self.staff_profile_view),
                name='accounts_staff_profile'
            ),
            path(
                'staff-profile/revoke-device/<int:device_id>/',
                self.admin_site.admin_view(self.revoke_trusted_device_view),
                name='accounts_revoke_trusted_device'
            ),
            path(
                'staff-profile/revoke-all-devices/',
                self.admin_site.admin_view(self.revoke_all_trusted_devices_view),
                name='accounts_revoke_all_trusted_devices'
            ),
            path(
                'staff-profile/update-name/',
                self.admin_site.admin_view(self.update_name_view),
                name='accounts_update_name'
            ),
            path(
                'staff-profile/update-pin/',
                self.admin_site.admin_view(self.update_pin_view),
                name='accounts_update_pin'
            ),
            path(
                'staff-profile/revoke-mobile-session/<int:token_id>/',
                self.admin_site.admin_view(self.revoke_mobile_session_view),
                name='accounts_revoke_mobile_session'
            ),
            path(
                'mfa/verify/',
                self.mfa_verify_view,  # No admin_view wrapper - needs to be accessible before MFA verified
                name='mfa_verify'
            ),
        ]
        return custom_urls + urls

    def staff_profile_view(self, request):
        """Comprehensive staff profile dashboard"""
        from django.shortcuts import render
        from django.utils.timesince import timesince
        from core.models import TrustedDevice

        user = request.user

        # ---- Trusted devices ----
        trusted_devices = TrustedDevice.objects.filter(
            user=user, is_revoked=False
        ).order_by('-created_at')

        # ---- MFA status ----
        mfa_enabled = False
        totp_authenticator = None
        recovery_codes_remaining = 0
        try:
            from allauth.mfa.utils import is_mfa_enabled
            from allauth.mfa.models import Authenticator
            mfa_enabled = is_mfa_enabled(user)
            if mfa_enabled:
                try:
                    totp_authenticator = Authenticator.objects.get(
                        user=user, type=Authenticator.Type.TOTP
                    )
                except Authenticator.DoesNotExist:
                    pass
                try:
                    recovery_auth = Authenticator.objects.get(
                        user=user, type=Authenticator.Type.RECOVERY_CODES
                    )
                    codes = recovery_auth.data.get('codes', [])
                    recovery_codes_remaining = len([c for c in codes if not c.get('used', False)])
                except Authenticator.DoesNotExist:
                    pass
        except ImportError:
            pass

        # ---- Roles ----
        roles = []
        try:
            from staff_roles.services import get_user_roles
            roles = list(get_user_roles(user))
        except ImportError:
            pass

        # ---- POS access ----
        has_pos = False
        try:
            from staff_roles.services import can_access_pos
            has_pos = can_access_pos(user)
        except ImportError:
            pass

        # ---- Permissions summary ----
        permissions_summary = []
        try:
            from staff_roles.categories import PERMISSION_CATEGORIES
            for key, cat in sorted(PERMISSION_CATEGORIES.items(), key=lambda x: x[1]['sort_order']):
                # Determine effective level across all roles
                effective = 'none'
                if user.is_superuser:
                    effective = 'full'
                else:
                    for role in roles:
                        role_level = role.permission_categories.get(key, 'none')
                        if role_level == 'full':
                            effective = 'full'
                            break
                        elif role_level == 'view' and effective == 'none':
                            effective = 'view'
                permissions_summary.append({
                    'key': key,
                    'label': str(cat['label']),
                    'icon': cat['icon'],
                    'level': effective,
                })
        except ImportError:
            pass

        # ---- Mobile devices (grouped by device_id) ----
        mobile_devices = []
        mobile_device_count = 0
        max_devices_per_user = 0  # 0 = unlimited (safe fallback if SiteSettings unavailable)
        try:
            from admin_api.models import MobileAuthToken, DeviceRegistration
            from core.models import SiteSettings
            from django.db.models import Max

            site_settings = SiteSettings.get_settings()
            max_devices_per_user = site_settings.max_devices_per_user

            # Get unique devices with active refresh tokens (this is what counts toward the limit)
            active_devices = (
                MobileAuthToken.objects.filter(
                    user=user, token_type='refresh', is_revoked=False
                )
                .values('device_id', 'device_name')
                .annotate(last_active=Max('last_used_at'))
                .order_by('-last_active')
            )

            # Get device registrations for platform info
            device_regs = {
                dr.device_id: dr
                for dr in DeviceRegistration.objects.filter(user=user)
            }

            # Build device info — use any non-revoked token for the PK (prefer refresh since access tokens expire quickly)
            for device in active_devices:
                did = device['device_id']
                reg = device_regs.get(did)

                # Get a stable token PK for the revoke endpoint (refresh tokens last 14 days)
                revoke_token = MobileAuthToken.objects.filter(
                    user=user, device_id=did, is_revoked=False
                ).order_by('-expires_at').first()

                # Get latest IP from most recently used token (any type)
                latest_used = MobileAuthToken.objects.filter(
                    user=user, device_id=did, last_used_ip__isnull=False
                ).order_by('-last_used_at').first()

                mobile_devices.append({
                    'device_id': did,
                    'device_name': device['device_name'] or 'Unknown Device',
                    'last_active': device['last_active'],
                    'last_ip': latest_used.last_used_ip if latest_used else None,
                    'platform': reg.platform if reg else None,
                    'has_push': reg.is_active if reg else False,
                    'token_pk': revoke_token.pk if revoke_token else None,
                })

            mobile_device_count = len(mobile_devices)
        except (ImportError, Exception):
            pass

        # ---- POS data (conditional) ----
        pos_staff = None
        pos_terminals = []
        pos_recent_shifts = []
        pos_orders_30d = 0
        pos_shifts_30d = 0
        if has_pos:
            try:
                from pos_app.models import POSStaffDiscount, POSShift, POSTerminal
                from datetime import timedelta
                thirty_days_ago = timezone.now() - timedelta(days=30)

                try:
                    pos_staff = POSStaffDiscount.objects.get(user=user)
                except POSStaffDiscount.DoesNotExist:
                    pass

                pos_terminals = list(
                    POSTerminal.objects.filter(
                        assigned_users=user, is_active=True
                    ).select_related('warehouse')[:10]
                )

                pos_recent_shifts = list(
                    POSShift.objects.filter(cashier=user)
                    .select_related('terminal')
                    .order_by('-started_at')[:5]
                )

                pos_shifts_30d = POSShift.objects.filter(
                    cashier=user, started_at__gte=thirty_days_ago
                ).count()

                try:
                    from orders.models import Order
                    pos_orders_30d = Order.objects.filter(
                        cashier=user,
                        channel='pos',
                        created_at__gte=thirty_days_ago,
                    ).count()
                except (ImportError, Exception):
                    pass
            except ImportError:
                pass

        # ---- Blog data ----
        blog_post_count = 0
        recent_blog_posts = []
        try:
            from blog.models import BlogPost
            recent_blog_posts = list(
                BlogPost.objects.filter(created_by=user)
                .order_by('-created_at')[:3]
            )
            blog_post_count = BlogPost.objects.filter(created_by=user).count()
        except (ImportError, Exception):
            pass

        context = {
            **self.admin_site.each_context(request),
            'title': _('My Profile'),
            # Security
            'mfa_enabled': mfa_enabled,
            'totp_authenticator': totp_authenticator,
            'recovery_codes_remaining': recovery_codes_remaining,
            'trusted_devices': trusted_devices,
            'trusted_device_count': trusted_devices.count(),
            # Roles & permissions
            'roles': roles,
            'permissions_summary': permissions_summary,
            # Mobile devices
            'mobile_devices': mobile_devices,
            'mobile_device_count': mobile_device_count,
            'max_devices_per_user': max_devices_per_user,
            # POS
            'has_pos': has_pos,
            'pos_staff': pos_staff,
            'pos_terminals': pos_terminals,
            'pos_terminal_count': len(pos_terminals),
            'pos_recent_shifts': pos_recent_shifts,
            'pos_orders_30d': pos_orders_30d,
            'pos_shifts_30d': pos_shifts_30d,
            # Blog / Activity
            'blog_post_count': blog_post_count,
            'recent_blog_posts': recent_blog_posts,
        }

        return render(request, 'admin/accounts/staff_profile.html', context)

    def update_name_view(self, request):
        """AJAX: Update current user's first/last name"""
        import json
        from django.http import JsonResponse

        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        first_name = data.get('first_name', '').strip()[:150]
        last_name = data.get('last_name', '').strip()[:150]

        if not first_name and not last_name:
            return JsonResponse({'success': False, 'error': 'Name cannot be empty'}, status=400)

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save(update_fields=['first_name', 'last_name'])

        return JsonResponse({
            'success': True,
            'full_name': request.user.get_full_name(),
        })

    def update_pin_view(self, request):
        """AJAX: Update current user's cashier PIN"""
        import json
        import re
        from django.http import JsonResponse

        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        pin = data.get('pin', '').strip()

        if not pin or not re.match(r'^\d{4,6}$', pin):
            return JsonResponse({'success': False, 'error': 'PIN must be 4-6 digits'}, status=400)

        try:
            from pos_app.models import POSStaffDiscount
            staff, _created = POSStaffDiscount.objects.get_or_create(user=request.user)
            staff.cashier_pin = pin
            staff.save(update_fields=['cashier_pin'])
            return JsonResponse({'success': True})
        except ImportError:
            return JsonResponse({'success': False, 'error': 'POS module not available'}, status=400)

    def revoke_mobile_session_view(self, request, token_id):
        """AJAX: Revoke a mobile device — revokes all tokens for the device and removes its registration."""
        from django.http import JsonResponse

        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

        try:
            from admin_api.models import MobileAuthToken, DeviceRegistration
            token = MobileAuthToken.objects.get(
                pk=token_id, user=request.user, is_revoked=False
            )
            device_id = token.device_id

            # Revoke ALL tokens for this device (access, refresh, 2fa_pending)
            MobileAuthToken.revoke_all_for_device(
                request.user, device_id, reason='Device removed from profile page'
            )

            # Also remove the device registration (push notifications)
            DeviceRegistration.objects.filter(
                user=request.user, device_id=device_id
            ).delete()

            return JsonResponse({'success': True})
        except MobileAuthToken.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
        except ImportError:
            return JsonResponse({'success': False, 'error': 'Module not available'}, status=400)

    def revoke_trusted_device_view(self, request, device_id):
        """Revoke a single trusted device"""
        from django.shortcuts import redirect
        from django.contrib import messages
        from core.models import TrustedDevice

        if request.method == 'POST':
            try:
                device = TrustedDevice.objects.get(
                    pk=device_id,
                    user=request.user,
                    is_revoked=False
                )
                device.is_revoked = True
                device.save(update_fields=['is_revoked'])
                messages.success(
                    request,
                    _('Device "{}" has been revoked.').format(device.device_name)
                )
            except TrustedDevice.DoesNotExist:
                messages.error(request, _('Device not found or already revoked.'))

        return redirect('admin:accounts_staff_profile')

    def revoke_all_trusted_devices_view(self, request):
        """Revoke all trusted devices for the current user"""
        from django.shortcuts import redirect
        from django.contrib import messages
        from core.models import TrustedDevice

        if request.method == 'POST':
            count = TrustedDevice.revoke_all_for_user(
                request.user,
                reason='User revoked all devices'
            )
            if count:
                messages.success(
                    request,
                    _('All {} trusted device(s) have been revoked.').format(count)
                )
            else:
                messages.info(request, _('No trusted devices to revoke.'))

        return redirect('admin:accounts_staff_profile')

    def mfa_verify_view(self, request):
        """
        MFA verification view for admin login.

        This is shown when a user with 2FA logs into admin via the standard
        Django admin login (which bypasses allauth's MFA flow).
        """
        from django.shortcuts import render, redirect
        from django.contrib import messages
        from django.contrib.auth.decorators import login_required
        from django.utils.decorators import method_decorator
        from allauth.mfa.models import Authenticator
        from allauth.mfa import totp
        from core.middleware.mfa_enforcement import MFA_VERIFIED_SESSION_KEY
        from core.models import SiteSettings, TrustedDevice

        # Must be authenticated
        if not request.user.is_authenticated:
            return redirect('admin:login')

        # Must be staff
        if not request.user.is_staff:
            return redirect('admin:index')

        # Check if user has TOTP enabled
        try:
            authenticator = Authenticator.objects.get(
                user=request.user,
                type=Authenticator.Type.TOTP
            )
        except Authenticator.DoesNotExist:
            # No 2FA set up - shouldn't be here
            return redirect('admin:index')

        error = None
        show_trust_device = False

        # Check if trusted devices are enabled
        try:
            settings = SiteSettings.get_settings()
            show_trust_device = settings.allow_trusted_devices
        except Exception:
            pass

        if request.method == 'POST':
            code = request.POST.get('code', '').strip()
            trust_device = request.POST.get('trust_device') == 'on'

            if code:
                # Validate TOTP code
                totp_wrapper = authenticator.wrap()
                if totp_wrapper.validate_code(code):
                    # Code is valid - mark session as MFA verified
                    request.session[MFA_VERIFIED_SESSION_KEY] = timezone.now().isoformat()
                    request.session.modified = True

                    # Handle trusted device if requested
                    if trust_device and show_trust_device:
                        try:
                            device, token = TrustedDevice.create_trusted_device(
                                user=request.user,
                                request=request,
                                remember_days=settings.trusted_device_days
                            )
                            # Set the cookie on the response
                            next_url = request.session.pop('mfa_next_url', reverse('admin:index'))
                            response = redirect(next_url)
                            response.set_cookie(
                                'spwig_trusted_device',
                                token,
                                max_age=settings.trusted_device_days * 24 * 60 * 60,
                                httponly=True,
                                secure=request.is_secure(),
                                samesite='Lax'
                            )
                            messages.success(request, _('Verification successful. This device is now trusted.'))
                            return response
                        except Exception as e:
                            # Trust device failed but MFA verified - continue anyway
                            pass

                    # Redirect to original destination
                    next_url = request.session.pop('mfa_next_url', reverse('admin:index'))
                    messages.success(request, _('Verification successful.'))
                    return redirect(next_url)
                else:
                    error = _('Invalid code. Please try again.')
            else:
                error = _('Please enter your authentication code.')

        context = {
            **self.admin_site.each_context(request),
            'title': _('Two-Factor Authentication'),
            'error': error,
            'show_trust_device': show_trust_device,
        }

        return render(request, 'admin/accounts/mfa_verify.html', context)


# Unregister default User admin and register custom one
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)


# ============================================================================
# Staff Member Admin (Proxy Model - Staff Only)
# ============================================================================

class RoleFilter(admin.SimpleListFilter):
    """Filter staff by StaffRole."""
    title = _('Role')
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        from staff_roles.models import StaffRole
        return [(r.pk, r.display_name) for r in StaffRole.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            from staff_roles.models import StaffRole
            try:
                role = StaffRole.objects.get(pk=self.value())
                return queryset.filter(groups=role.group)
            except StaffRole.DoesNotExist:
                pass
        return queryset


class AccessTypeFilter(admin.SimpleListFilter):
    """Filter staff by access type (Admin/POS/Both)."""
    title = _('Access Type')
    parameter_name = 'access'

    def lookups(self, request, model_admin):
        return [
            ('admin_only', _('Admin Only')),
            ('pos_only', _('POS Only')),
            ('both', _('Admin & POS')),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        from staff_roles.models import StaffRole
        admin_groups = StaffRole.objects.filter(can_access_admin=True).values_list('group_id', flat=True)
        pos_groups = StaffRole.objects.filter(can_access_pos=True).values_list('group_id', flat=True)

        if self.value() == 'admin_only':
            return queryset.filter(groups__in=admin_groups).exclude(groups__in=pos_groups).distinct()
        elif self.value() == 'pos_only':
            return queryset.filter(groups__in=pos_groups).exclude(groups__in=admin_groups).distinct()
        elif self.value() == 'both':
            return queryset.filter(groups__in=admin_groups).filter(groups__in=pos_groups).distinct()
        return queryset


class MFAStatusFilter(admin.SimpleListFilter):
    """Filter staff by MFA status."""
    title = _('2FA Status')
    parameter_name = 'mfa'

    def lookups(self, request, model_admin):
        return [
            ('enabled', _('Enabled')),
            ('disabled', _('Not Enabled')),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        try:
            from allauth.mfa.models import Authenticator
            users_with_mfa = Authenticator.objects.filter(
                type=Authenticator.Type.TOTP
            ).values_list('user_id', flat=True)
            if self.value() == 'enabled':
                return queryset.filter(pk__in=users_with_mfa)
            else:
                return queryset.exclude(pk__in=users_with_mfa)
        except ImportError:
            return queryset


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    """Dedicated admin for managing staff members."""

    change_list_template = 'admin/accounts/staffmember/change_list.html'
    change_form_template = 'admin/accounts/staffmember/change_form.html'

    list_display = ['email', 'first_name', 'last_name', 'is_active', 'date_joined']
    list_filter = [RoleFilter, AccessTypeFilter, 'is_active', MFAStatusFilter]
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['-date_joined']

    fieldsets = (
        (_('Account'), {
            'fields': ('email', 'first_name', 'last_name', 'username'),
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_staff'),
        }),
    )

    class Media:
        css = {'all': ('accounts/css/staff_management.css',)}
        js = ('accounts/js/staff_management.js',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('groups')

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/toggle-role/',
                self.admin_site.admin_view(self.toggle_role_view),
                name='staffmember_toggle_role',
            ),
            path(
                '<int:user_id>/save-pos-settings/',
                self.admin_site.admin_view(self.save_pos_settings_view),
                name='staffmember_save_pos_settings',
            ),
            path(
                '<int:user_id>/revoke-session/<int:token_id>/',
                self.admin_site.admin_view(self.revoke_session_view),
                name='staffmember_revoke_session',
            ),
            path(
                'filter/',
                self.admin_site.admin_view(self.filter_staff_view),
                name='staffmember_filter',
            ),
        ]
        return custom_urls + urls

    # ------------------------------------------------------------------
    # Change List View
    # ------------------------------------------------------------------
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        qs = self.get_queryset(request)

        # Stats
        total_staff = qs.count()
        active_staff = qs.filter(is_active=True).count()
        inactive_staff = total_staff - active_staff

        # POS access count
        pos_count = 0
        try:
            from staff_roles.models import StaffRole
            pos_groups = StaffRole.objects.filter(can_access_pos=True).values_list('group_id', flat=True)
            pos_count = qs.filter(groups__in=pos_groups).distinct().count()
            # Add superusers who always have POS access
            pos_count += qs.filter(is_superuser=True).exclude(groups__in=pos_groups).count()
        except Exception:
            pass

        # 2FA count
        mfa_count = 0
        try:
            from allauth.mfa.models import Authenticator
            users_with_mfa = Authenticator.objects.filter(
                type=Authenticator.Type.TOTP
            ).values_list('user_id', flat=True)
            mfa_count = qs.filter(pk__in=users_with_mfa).count()
        except ImportError:
            pass

        # Staff list with role data
        from staff_roles.services import get_user_roles, can_access_pos, can_access_admin
        staff_list = []
        for member in qs.filter(is_active=True).select_related().prefetch_related('groups')[:100]:
            roles = list(get_user_roles(member))
            staff_list.append({
                'user': member,
                'roles': roles,
                'has_admin': can_access_admin(member),
                'has_pos': can_access_pos(member),
                'is_owner': member.is_superuser,
            })

        # All roles for filter dropdown
        all_roles = []
        try:
            from staff_roles.models import StaffRole
            all_roles = list(StaffRole.objects.all())
        except Exception:
            pass

        extra_context.update({
            'total_staff': total_staff,
            'active_staff': active_staff,
            'inactive_staff': inactive_staff,
            'pos_count': pos_count,
            'mfa_count': mfa_count,
            'staff_list': staff_list,
            'all_roles': all_roles,
        })

        return super().changelist_view(request, extra_context)

    # ------------------------------------------------------------------
    # Change Form View
    # ------------------------------------------------------------------
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        try:
            staff_user = User.objects.get(pk=object_id)
        except User.DoesNotExist:
            from django.http import Http404
            raise Http404

        from staff_roles.services import get_user_roles, can_access_pos, can_access_admin
        from staff_roles.models import StaffRole
        from staff_roles.categories import PERMISSION_CATEGORIES

        roles = list(get_user_roles(staff_user))
        has_pos = can_access_pos(staff_user)
        has_admin = can_access_admin(staff_user)

        # All roles for toggle cards
        all_roles = list(StaffRole.objects.all().select_related('group'))
        user_group_ids = set(staff_user.groups.values_list('id', flat=True))
        role_cards = []
        for role in all_roles:
            role_cards.append({
                'role': role,
                'assigned': role.group_id in user_group_ids,
            })

        # Effective permissions
        permissions_summary = []
        for key, cat in sorted(PERMISSION_CATEGORIES.items(), key=lambda x: x[1]['sort_order']):
            effective = 'none'
            if staff_user.is_superuser:
                effective = 'full'
            else:
                for role in roles:
                    role_level = role.permission_categories.get(key, 'none')
                    if role_level == 'full':
                        effective = 'full'
                        break
                    elif role_level == 'view' and effective == 'none':
                        effective = 'view'
            permissions_summary.append({
                'key': key,
                'label': str(cat['label']),
                'icon': cat['icon'],
                'level': effective,
            })

        # MFA status
        mfa_enabled = False
        try:
            from allauth.mfa.utils import is_mfa_enabled
            mfa_enabled = is_mfa_enabled(staff_user)
        except ImportError:
            pass

        # Trusted devices
        trusted_devices = []
        try:
            from core.models import TrustedDevice
            trusted_devices = list(
                TrustedDevice.objects.filter(user=staff_user, is_revoked=False)
                .order_by('-created_at')[:10]
            )
        except Exception:
            pass

        # Mobile sessions
        mobile_sessions = []
        try:
            from admin_api.models import MobileAuthToken
            mobile_sessions = list(
                MobileAuthToken.objects.filter(
                    user=staff_user, token_type='access', is_revoked=False
                ).order_by('-last_used_at')[:10]
            )
        except (ImportError, Exception):
            pass

        # POS data
        pos_staff = None
        pos_terminals = []
        pos_recent_shifts = []
        pos_orders_30d = 0
        pos_shifts_30d = 0
        if has_pos:
            try:
                from pos_app.models import POSStaffDiscount, POSShift, POSTerminal
                from datetime import timedelta
                thirty_days_ago = timezone.now() - timedelta(days=30)

                try:
                    pos_staff = POSStaffDiscount.objects.get(user=staff_user)
                except POSStaffDiscount.DoesNotExist:
                    pass

                pos_terminals = list(
                    POSTerminal.objects.filter(
                        assigned_users=staff_user, is_active=True
                    ).select_related('warehouse')[:10]
                )

                pos_recent_shifts = list(
                    POSShift.objects.filter(cashier=staff_user)
                    .select_related('terminal')
                    .order_by('-started_at')[:5]
                )

                pos_shifts_30d = POSShift.objects.filter(
                    cashier=staff_user, started_at__gte=thirty_days_ago
                ).count()

                try:
                    from orders.models import Order
                    pos_orders_30d = Order.objects.filter(
                        cashier=staff_user,
                        channel='pos',
                        created_at__gte=thirty_days_ago,
                    ).count()
                except (ImportError, Exception):
                    pass
            except ImportError:
                pass

        # Blog data
        blog_post_count = 0
        recent_blog_posts = []
        try:
            from blog.models import BlogPost
            recent_blog_posts = list(
                BlogPost.objects.filter(created_by=staff_user)
                .order_by('-created_at')[:3]
            )
            blog_post_count = BlogPost.objects.filter(created_by=staff_user).count()
        except (ImportError, Exception):
            pass

        # WebAuthn credential count for biometric status
        webauthn_credential_count = 0
        try:
            from pos_app.models import WebAuthnCredential
            webauthn_credential_count = WebAuthnCredential.objects.filter(user=staff_user).count()
        except (ImportError, Exception):
            pass

        extra_context.update({
            'staff_user': staff_user,
            'roles': roles,
            'has_pos': has_pos,
            'has_admin': has_admin,
            'role_cards': role_cards,
            'permissions_summary': permissions_summary,
            'mfa_enabled': mfa_enabled,
            'trusted_devices': trusted_devices,
            'mobile_sessions': mobile_sessions,
            'pos_staff': pos_staff,
            'pos_terminals': pos_terminals,
            'pos_recent_shifts': pos_recent_shifts,
            'pos_orders_30d': pos_orders_30d,
            'pos_shifts_30d': pos_shifts_30d,
            'blog_post_count': blog_post_count,
            'recent_blog_posts': recent_blog_posts,
            'webauthn_credential_count': webauthn_credential_count,
        })

        return super().change_view(request, object_id, form_url, extra_context)

    # ------------------------------------------------------------------
    # AJAX: Toggle Role
    # ------------------------------------------------------------------
    def toggle_role_view(self, request, user_id):
        import json
        from django.http import JsonResponse
        from staff_roles.models import StaffRole
        from staff_roles.services import invalidate_user_cache

        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        try:
            staff_user = User.objects.get(pk=user_id, is_staff=True)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)

        role_id = data.get('role_id')
        action = data.get('action')  # 'assign' or 'remove'

        try:
            role = StaffRole.objects.get(pk=role_id)
        except StaffRole.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Role not found'}, status=404)

        if action == 'assign':
            staff_user.groups.add(role.group)
        elif action == 'remove':
            staff_user.groups.remove(role.group)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)

        invalidate_user_cache(staff_user)

        return JsonResponse({'success': True})

    # ------------------------------------------------------------------
    # AJAX: Save POS Settings
    # ------------------------------------------------------------------
    def save_pos_settings_view(self, request, user_id):
        import json
        from django.http import JsonResponse

        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        try:
            staff_user = User.objects.get(pk=user_id, is_staff=True)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)

        try:
            from pos_app.models import POSStaffDiscount
            pos_staff, _created = POSStaffDiscount.objects.get_or_create(user=staff_user)

            # Update fields
            if 'max_discount_percentage' in data:
                val = data['max_discount_percentage']
                try:
                    from decimal import Decimal
                    pos_staff.max_discount_percentage = Decimal(str(val))
                except (ValueError, TypeError):
                    pass

            if 'max_discount_amount' in data:
                val = data['max_discount_amount']
                if val in ('', None):
                    pos_staff.max_discount_amount = None
                else:
                    try:
                        from decimal import Decimal
                        pos_staff.max_discount_amount = Decimal(str(val))
                    except (ValueError, TypeError):
                        pass

            bool_fields = [
                'can_apply_item_discounts', 'can_apply_cart_discounts',
                'requires_reason', 'is_manager',
            ]
            for field in bool_fields:
                if field in data:
                    setattr(pos_staff, field, bool(data[field]))

            if 'manager_pin' in data:
                pin = str(data['manager_pin']).strip()
                if pin == '' or (pin.isdigit() and 4 <= len(pin) <= 6):
                    pos_staff.manager_pin = pin

            if 'cashier_pin' in data:
                pin = str(data['cashier_pin']).strip()
                if pin == '' or (pin.isdigit() and 4 <= len(pin) <= 6):
                    pos_staff.cashier_pin = pin

            if data.get('remove_card'):
                pos_staff.card_identifier = ''

            pos_staff.save()

            if data.get('remove_biometric'):
                try:
                    from pos_app.models import WebAuthnCredential
                    WebAuthnCredential.objects.filter(user=staff_user).delete()
                except ImportError:
                    pass

            return JsonResponse({'success': True})
        except ImportError:
            return JsonResponse({'success': False, 'error': 'POS module not available'}, status=400)

    # ------------------------------------------------------------------
    # AJAX: Revoke Mobile Session
    # ------------------------------------------------------------------
    def revoke_session_view(self, request, user_id, token_id):
        from django.http import JsonResponse

        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

        try:
            from admin_api.models import MobileAuthToken
            token = MobileAuthToken.objects.get(
                pk=token_id, user_id=user_id, is_revoked=False
            )
            token.revoke(reason='Revoked by admin from staff management')
            return JsonResponse({'success': True})
        except MobileAuthToken.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
        except ImportError:
            return JsonResponse({'success': False, 'error': 'Module not available'}, status=400)

    # ------------------------------------------------------------------
    # AJAX: Filter Staff (for AJAX list refresh)
    # ------------------------------------------------------------------
    def filter_staff_view(self, request):
        from django.http import JsonResponse
        from django.template.loader import render_to_string
        from staff_roles.services import get_user_roles, can_access_pos, can_access_admin

        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid request'}, status=400)

        qs = self.get_queryset(request)

        # Apply filters
        search = request.GET.get('search', '').strip()
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        role_id = request.GET.get('role', '')
        if role_id:
            from staff_roles.models import StaffRole
            try:
                role = StaffRole.objects.get(pk=role_id)
                qs = qs.filter(groups=role.group)
            except StaffRole.DoesNotExist:
                pass

        access = request.GET.get('access', '')
        if access:
            from staff_roles.models import StaffRole
            admin_groups = StaffRole.objects.filter(can_access_admin=True).values_list('group_id', flat=True)
            pos_groups = StaffRole.objects.filter(can_access_pos=True).values_list('group_id', flat=True)
            if access == 'admin_only':
                qs = qs.filter(groups__in=admin_groups).exclude(groups__in=pos_groups).distinct()
            elif access == 'pos_only':
                qs = qs.filter(groups__in=pos_groups).exclude(groups__in=admin_groups).distinct()
            elif access == 'both':
                qs = qs.filter(groups__in=admin_groups).filter(groups__in=pos_groups).distinct()

        status = request.GET.get('status', '')
        if status == 'active':
            qs = qs.filter(is_active=True)
        elif status == 'inactive':
            qs = qs.filter(is_active=False)

        mfa = request.GET.get('mfa', '')
        if mfa:
            try:
                from allauth.mfa.models import Authenticator
                users_with_mfa = Authenticator.objects.filter(
                    type=Authenticator.Type.TOTP
                ).values_list('user_id', flat=True)
                if mfa == 'enabled':
                    qs = qs.filter(pk__in=users_with_mfa)
                elif mfa == 'disabled':
                    qs = qs.exclude(pk__in=users_with_mfa)
            except ImportError:
                pass

        # Build staff list
        staff_list = []
        for member in qs.select_related().prefetch_related('groups')[:100]:
            roles = list(get_user_roles(member))
            staff_list.append({
                'user': member,
                'roles': roles,
                'has_admin': can_access_admin(member),
                'has_pos': can_access_pos(member),
                'is_owner': member.is_superuser,
            })

        html = render_to_string(
            'admin/accounts/staffmember/partials/staff_cards.html',
            {'staff_list': staff_list},
            request=request,
        )

        return JsonResponse({'html': html, 'count': qs.count()})


# ============================================================
# Communication Preferences Admin
# ============================================================

@admin.register(CommunicationPreference)
class CommunicationPreferenceAdmin(admin.ModelAdmin):
    """Admin interface for customer communication preferences."""

    change_list_template = 'admin/accounts/communicationpreference/change_list.html'

    list_display = [
        'user_email',
        'email_status',
        'sms_status',
        'marketing_status',
        'verification_status',
        'consent_source_display',
        'updated_at',
    ]

    list_filter = [
        'email_enabled',
        'sms_enabled',
        'email_marketing',
        'sms_marketing',
        'email_verified',
        'sms_verified',
        'consent_source',
        'language_code',
    ]

    search_fields = [
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
        'unsubscribe_token',
    ]

    readonly_fields = [
        'unsubscribe_token',
        'consent_timestamp',
        'consent_ip',
        'consent_user_agent',
        'created_at',
        'updated_at',
        'email_verified_at',
        'sms_verified_at',
    ]

    fieldsets = (
        (_('User'), {
            'fields': ('user',),
        }),
        (_('Email Preferences'), {
            'fields': (
                'email_enabled',
                'email_transactional',
                'email_marketing',
                ('email_verified', 'email_verified_at'),
            ),
            'description': _(
                'Email communication settings. Transactional emails (order confirmations, etc.) '
                'are always sent regardless of these settings.'
            ),
        }),
        (_('SMS Preferences'), {
            'fields': (
                'sms_enabled',
                'sms_transactional',
                'sms_marketing',
                ('sms_verified', 'sms_verified_at'),
            ),
            'description': _(
                'SMS communication settings. All SMS requires explicit customer opt-in (TCPA compliance).'
            ),
        }),
        (_('App-Specific Preferences'), {
            'fields': ('app_preferences',),
            'classes': ('collapse',),
            'description': _(
                'JSON field containing preferences for blog, loyalty, referrals, and affiliate communications.'
            ),
        }),
        (_('Consent Tracking (GDPR Compliance)'), {
            'fields': (
                'consent_source',
                'consent_timestamp',
                'consent_ip',
                'consent_user_agent',
            ),
            'classes': ('collapse',),
            'description': _(
                'Consent metadata required for GDPR Article 7 compliance. '
                'Records when, where, and how customer provided consent.'
            ),
        }),
        (_('Unsubscribe'), {
            'fields': ('unsubscribe_token',),
            'classes': ('collapse',),
            'description': _(
                'Unique token for one-click unsubscribe links in marketing emails.'
            ),
        }),
        (_('Metadata'), {
            'fields': (
                'language_code',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )

    actions = [
        'bulk_verify_email',
        'bulk_unsubscribe_marketing',
        'export_preferences_csv',
        'export_preferences_json',
    ]

    def changelist_view(self, request, extra_context=None):
        """Inject context for the custom change list template."""
        extra_context = extra_context or {}
        extra_context['consent_source_choices'] = CommunicationPreference.CONSENT_SOURCE_CHOICES
        return super().changelist_view(request, extra_context=extra_context)

    # Custom list display methods

    def user_email(self, obj):
        """Display user email with link to user admin."""
        url = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.user.email
        )
    user_email.short_description = _('User')
    user_email.admin_order_field = 'user__email'

    def email_status(self, obj):
        """Display email enabled/disabled status."""
        if obj.email_enabled:
            return format_html(
                '<span class="badge-yes" title="{}">&#10003;</span>',
                _('Email enabled')
            )
        return format_html(
            '<span class="badge-no" title="{}">&#9675;</span>',
            _('Email disabled')
        )
    email_status.short_description = _('Email')

    def sms_status(self, obj):
        """Display SMS enabled/disabled status."""
        if obj.sms_enabled:
            return format_html(
                '<span class="badge-yes" title="{}">&#10003;</span>',
                _('SMS enabled')
            )
        return format_html(
            '<span class="badge-no" title="{}">&#9675;</span>',
            _('SMS disabled')
        )
    sms_status.short_description = _('SMS')

    def marketing_status(self, obj):
        """Display marketing opt-in status."""
        if obj.email_marketing or obj.sms_marketing:
            return format_html(
                '<span class="badge-yes">&#10003; {}</span>',
                _('Opted In')
            )
        return format_html(
            '<span class="badge-no">&#9675; {}</span>',
            _('Opted Out')
        )
    marketing_status.short_description = _('Marketing')

    def verification_status(self, obj):
        """Display verification status for email/SMS."""
        email_badge = '&#10003;' if obj.email_verified else '&#9675;'
        sms_badge = '&#10003;' if obj.sms_verified else '&#9675;'

        return format_html(
            '<span title="{}: {}">{}</span> '
            '<span title="{}: {}">{}</span>',
            _('Email verified'), _('Yes') if obj.email_verified else _('No'),
            email_badge,
            _('SMS verified'), _('Yes') if obj.sms_verified else _('No'),
            sms_badge,
        )
    verification_status.short_description = _('Verified')

    def consent_source_display(self, obj):
        """Display consent source."""
        return obj.get_consent_source_display()
    consent_source_display.short_description = _('Source')
    consent_source_display.admin_order_field = 'consent_source'

    # Admin actions

    @admin.action(description=_('Mark email as verified'))
    def bulk_verify_email(self, request, queryset):
        """Bulk verify email addresses for selected users."""
        count = queryset.update(
            email_verified=True,
            email_verified_at=timezone.now(),
        )

        # Invalidate cache for all users
        from accounts.services.preference_service import PreferenceService
        for pref in queryset:
            PreferenceService.invalidate_cache(pref.user.id)

        self.message_user(
            request,
            _(f'Successfully verified email for {count} user(s).'),
            level='SUCCESS'
        )

    @admin.action(description=_('Unsubscribe from all marketing'))
    def bulk_unsubscribe_marketing(self, request, queryset):
        """Bulk unsubscribe users from all marketing communications."""
        count = queryset.count()

        for pref in queryset:
            # Disable all marketing
            pref.email_marketing = False
            pref.sms_marketing = False

            # Disable all app marketing
            if 'blog' in pref.app_preferences:
                pref.app_preferences['blog']['enabled'] = False
            if 'loyalty' in pref.app_preferences:
                pref.app_preferences['loyalty']['enabled'] = False
            if 'referrals' in pref.app_preferences:
                pref.app_preferences['referrals']['enabled'] = False
            if 'affiliate' in pref.app_preferences:
                pref.app_preferences['affiliate']['enabled'] = False

            pref.save()

            # Invalidate cache
            from accounts.services.preference_service import PreferenceService
            PreferenceService.invalidate_cache(pref.user.id)

        self.message_user(
            request,
            _(f'Successfully unsubscribed {count} user(s) from all marketing communications.'),
            level='SUCCESS'
        )

    @admin.action(description=_('Export preferences as CSV'))
    def export_preferences_csv(self, request, queryset):
        """Export selected preferences as CSV for analysis."""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="communication_preferences.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'User Email',
            'Email Enabled',
            'Email Marketing',
            'Email Verified',
            'SMS Enabled',
            'SMS Marketing',
            'SMS Verified',
            'Blog Enabled',
            'Loyalty Enabled',
            'Referrals Enabled',
            'Affiliate Enabled',
            'Consent Source',
            'Consent Date',
            'Language',
        ])

        for pref in queryset.select_related('user'):
            writer.writerow([
                pref.user.email,
                pref.email_enabled,
                pref.email_marketing,
                pref.email_verified,
                pref.sms_enabled,
                pref.sms_marketing,
                pref.sms_verified,
                pref.app_preferences.get('blog', {}).get('enabled', False),
                pref.app_preferences.get('loyalty', {}).get('enabled', False),
                pref.app_preferences.get('referrals', {}).get('enabled', False),
                pref.app_preferences.get('affiliate', {}).get('enabled', False),
                pref.consent_source,
                pref.consent_timestamp.strftime('%Y-%m-%d %H:%M:%S') if pref.consent_timestamp else '',
                pref.language_code,
            ])

        return response

    @admin.action(description=_('Export preferences as JSON (with history)'))
    def export_preferences_json(self, request, queryset):
        """Export selected preferences as JSON with full change history for GDPR compliance."""
        import json
        from django.http import HttpResponse
        from accounts.services.preference_export_service import PreferenceExportService

        # Single user export
        if queryset.count() == 1:
            pref = queryset.first()
            data = PreferenceExportService.export_user_preferences(pref.user)

            response = HttpResponse(
                json.dumps(data, indent=2),
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="preferences_{pref.user.username}.json"'

        # Multiple users export
        else:
            exports = []
            for pref in queryset.select_related('user'):
                data = PreferenceExportService.export_user_preferences(pref.user)
                exports.append(data)

            response = HttpResponse(
                json.dumps(exports, indent=2),
                content_type='application/json'
            )
            response['Content-Disposition'] = 'attachment; filename="preferences_export.json"'

        return response

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')

    # Add inline for change logs
    class PreferenceChangeLogInline(admin.TabularInline):
        """Inline display of preference change history."""
        model = PreferenceChangeLog
        extra = 0
        can_delete = False
        max_num = 20  # Show last 20 changes
        fields = ['timestamp', 'action', 'source', 'ip_address']
        readonly_fields = fields
        ordering = ['-timestamp']

        def has_add_permission(self, request, obj=None):
            return False

    inlines = [PreferenceChangeLogInline]


# ============================================================
# Preference Change Log Admin (Audit Trail)
# ============================================================

@admin.register(PreferenceChangeLog)
class PreferenceChangeLogAdmin(admin.ModelAdmin):
    """
    Admin interface for preference change audit logs.

    Read-only audit trail for GDPR Article 7 compliance showing all preference
    changes with full context (who, when, where, what changed).
    """

    change_list_template = 'admin/accounts/preferencechangelog/change_list.html'

    list_display = [
        'user_email',
        'action',
        'source',
        'timestamp',
        'ip_address',
    ]

    list_filter = [
        'source',
        'action',
        'timestamp',
    ]

    search_fields = [
        'user__email',
        'user__username',
        'action',
        'ip_address',
    ]

    readonly_fields = [
        'user',
        'preference',
        'timestamp',
        'action',
        'old_value',
        'new_value',
        'ip_address',
        'user_agent',
        'source',
        'notes',
    ]

    fieldsets = (
        (_('Change Details'), {
            'fields': ('user', 'preference', 'action', 'source', 'timestamp'),
        }),
        (_('Changes'), {
            'fields': ('old_value', 'new_value'),
            'description': _('Before and after state of the preference change'),
        }),
        (_('Audit Context'), {
            'fields': ('ip_address', 'user_agent', 'notes'),
            'description': _('Technical details for audit trail'),
        }),
    )

    ordering = ['-timestamp']

    def user_email(self, obj):
        """Display user email."""
        return obj.user.email
    user_email.short_description = _('User')
    user_email.admin_order_field = 'user__email'

    def has_add_permission(self, request):
        """Audit logs cannot be manually created."""
        return False

    def has_change_permission(self, request, obj=None):
        """Audit logs are immutable."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete audit logs."""
        return request.user.is_superuser

    def changelist_view(self, request, extra_context=None):
        """Inject source choices for the custom change list template."""
        extra_context = extra_context or {}
        extra_context['source_choices'] = PreferenceChangeLog.SOURCE_CHOICES
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user', 'preference')
