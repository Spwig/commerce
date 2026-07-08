"""
Affiliate App Admin Configuration
Provides Django admin interface for affiliate program management with theme support
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django import forms
from datetime import timedelta

import json
from core.admin_mixins import TranslatableAdminMixin
from core.widgets import TranslatableFieldWidget

from .models import (
    Program, Affiliate, AffiliateProgramMembership,
    Link, Click, Commission, Payout, AffiliateSettings, AffiliateReportSettings
)
from .services.email_notifications import (
    send_affiliate_approved_email,
    send_affiliate_rejected_email,
    send_affiliate_suspended_email,
    send_affiliate_activated_email,
    send_program_membership_approved_email,
    send_program_membership_rejected_email,
    send_commission_earned_email,
    send_commission_approved_email,
    send_commission_rejected_email,
    send_commission_reversed_email,
    send_payout_processing_email,
    send_payout_completed_email,
    send_payout_failed_email,
    send_payout_cancelled_email,
)


# ============================================
# Inline Admin Classes
# ============================================

class AffiliateProgramMembershipInline(admin.TabularInline):
    """Inline for affiliate memberships in program admin"""
    model = AffiliateProgramMembership
    extra = 0
    fields = ('affiliate', 'status', 'applied_at', 'approved_at', 'notes')
    readonly_fields = ('applied_at', 'approved_at')
    autocomplete_fields = ['affiliate']


class LinkInline(admin.TabularInline):
    """Inline for tracking links in affiliate admin"""
    model = Link
    extra = 0
    fields = ('link_code', 'program', 'destination_url', 'label', 'is_active', 'created_at')
    readonly_fields = ('link_code', 'created_at')
    autocomplete_fields = ['program']


class CommissionInline(admin.TabularInline):
    """Inline for commissions in affiliate admin"""
    model = Commission
    extra = 0
    fields = ('program', 'order', 'amount', 'status', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = False


# ============================================
# Program Admin
# ============================================

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Admin interface for Affiliate Programs"""

    change_list_template = 'admin/affiliate/program/change_list.html'
    change_form_template = 'admin/affiliate/program/change_form.html'

    list_display = (
        'name', 'merchant', 'commission_display', 'status_badge',
        'affiliates_count', 'revenue_this_month', 'created_at'
    )
    list_filter = ('status', 'commission_type', 'created_at', 'auto_approve_affiliates')
    search_fields = ('name', 'slug', 'merchant__username', 'merchant__email', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'program_stats')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'merchant', 'description', 'status')
        }),
        (_('Commission Configuration'), {
            'fields': ('commission_type', 'commission_value', 'cookie_lifetime_days', 'minimum_payout'),
            'description': _('Configure how affiliates earn commissions')
        }),
        (_('Settings'), {
            'fields': ('auto_approve_affiliates',),
            'classes': ('collapse',)
        }),
        (_('Statistics'), {
            'fields': ('program_stats',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [AffiliateProgramMembershipInline]

    actions = ['activate_programs', 'pause_programs', 'archive_programs']

    def commission_display(self, obj):
        """Display commission value with type"""
        if obj.commission_type == 'percentage':
            return format_html(
                '<span class="badge badge-info"><i class="fas fa-percentage"></i> {}%</span>',
                obj.commission_value
            )
        else:
            return format_html(
                '<span class="badge badge-success"><i class="fas fa-dollar-sign"></i> ${}</span>',
                obj.commission_value
            )
    commission_display.short_description = _('Commission')

    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'active': 'success',
            'paused': 'warning',
            'archived': 'secondary'
        }
        icons = {
            'active': 'fa-check-circle',
            'paused': 'fa-pause-circle',
            'archived': 'fa-archive'
        }
        return format_html(
            '<span class="badge badge-{}"><i class="fas {}"></i> {}</span>',
            colors.get(obj.status, 'secondary'),
            icons.get(obj.status, 'fa-circle'),
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    def affiliates_count(self, obj):
        """Count of active affiliates"""
        count = obj.affiliates.filter(
            affiliateprogrammembership__status='approved'
        ).count()
        return format_html(
            '<a href="{}?programs__id__exact={}">'
            '<i class="fas fa-users"></i> {}</a>',
            reverse('admin:affiliate_affiliate_changelist'),
            obj.id,
            count
        )
    affiliates_count.short_description = _('Affiliates')

    def revenue_this_month(self, obj):
        """Total commissions this month"""
        start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        total = obj.commissions.filter(
            created_at__gte=start_of_month,
            status__in=['approved', 'paid']
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        return format_html(
            '<span class="badge badge-primary"><i class="fas fa-dollar-sign"></i> ${}</span>',
            f'{total:,.2f}'
        )
    revenue_this_month.short_description = _('Revenue (This Month)')

    def program_stats(self, obj):
        """Display comprehensive program statistics"""
        if not obj.pk:
            return _('Save the program first to see statistics')

        # Get stats
        affiliates_count = obj.affiliates.filter(
            affiliateprogrammembership__status='approved'
        ).count()
        pending_count = obj.affiliates.filter(
            affiliateprogrammembership__status='pending'
        ).count()

        total_clicks = Click.objects.filter(link__program=obj).count()
        total_commissions = obj.commissions.aggregate(Sum('amount'))['amount__sum'] or 0
        pending_commissions = obj.commissions.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
        paid_commissions = obj.commissions.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0

        html = f"""
        <div class="affiliate-stats-grid">
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-users"></i> {_('Active Affiliates')}</div>
                <div class="stat-value">{affiliates_count}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-clock"></i> {_('Pending Applications')}</div>
                <div class="stat-value">{pending_count}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-mouse-pointer"></i> {_('Total Clicks')}</div>
                <div class="stat-value">{total_clicks:,}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-dollar-sign"></i> {_('Total Commissions')}</div>
                <div class="stat-value">${total_commissions:,.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-hourglass-half"></i> {_('Pending Commissions')}</div>
                <div class="stat-value">${pending_commissions:,.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-check-circle"></i> {_('Paid Commissions')}</div>
                <div class="stat-value">${paid_commissions:,.2f}</div>
            </div>
        </div>
        <style>
            .affiliate-stats-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
                margin-top: 1rem;
            }}
            .stat-item {{
                background: var(--body-bg, #f8f9fa);
                border: 1px solid var(--border-color, #dee2e6);
                border-radius: 8px;
                padding: 1rem;
                text-align: center;
            }}
            .stat-label {{
                font-size: 0.875rem;
                color: var(--body-quiet-color, #6c757d);
                margin-bottom: 0.5rem;
            }}
            .stat-value {{
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--primary, #007bff);
            }}
        </style>
        """
        return mark_safe(html)
    program_stats.short_description = _('Program Statistics')

    # Actions
    def activate_programs(self, request, queryset):
        """Activate selected programs"""
        count = queryset.update(status='active')
        self.message_user(request, _('{} programs activated').format(count))
    activate_programs.short_description = _('Activate selected programs')

    def pause_programs(self, request, queryset):
        """Pause selected programs"""
        count = queryset.update(status='paused')
        self.message_user(request, _('{} programs paused').format(count))
    pause_programs.short_description = _('Pause selected programs')

    def archive_programs(self, request, queryset):
        """Archive selected programs"""
        count = queryset.update(status='archived')
        self.message_user(request, _('{} programs archived').format(count))
    archive_programs.short_description = _('Archive selected programs')

    def changelist_view(self, request, extra_context=None):
        """Override to add programs to context for card-based display"""
        extra_context = extra_context or {}

        # Get programs with annotations for the card display
        programs = Program.objects.annotate(
            affiliates_count=Count(
                'affiliates',
                filter=Q(affiliateprogrammembership__status='approved')
            ),
            active_affiliates=Count(
                'affiliates',
                filter=Q(affiliateprogrammembership__status='approved')
            ),
            total_earned=Sum('commissions__amount')
        ).order_by('-created_at')

        extra_context['programs'] = programs

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Override to add dashboard context for program detail view"""
        extra_context = extra_context or {}

        try:
            program = Program.objects.get(pk=object_id)

            # Get program statistics
            affiliates_count = program.affiliates.filter(
                affiliateprogrammembership__status='approved'
            ).count()
            pending_count = program.affiliates.filter(
                affiliateprogrammembership__status='pending'
            ).count()
            total_clicks = Click.objects.filter(link__program=program).count()

            # Commission stats
            commission_stats = program.commissions.aggregate(
                total=Sum('amount'),
                pending=Sum('amount', filter=Q(status='pending')),
                approved=Sum('amount', filter=Q(status='approved')),
                paid=Sum('amount', filter=Q(status='paid'))
            )

            # Conversion stats
            total_links = Link.objects.filter(program=program).count()
            conversions = program.commissions.filter(
                status__in=['approved', 'paid']
            ).count()

            # Get members with annotations
            from django.db.models import F
            members = AffiliateProgramMembership.objects.filter(
                program=program
            ).select_related('affiliate__user').annotate(
                member_commissions=Count(
                    'affiliate__commissions',
                    filter=Q(affiliate__commissions__program=program)
                ),
                member_earned=Sum(
                    'affiliate__commissions__amount',
                    filter=Q(
                        affiliate__commissions__program=program,
                        affiliate__commissions__status__in=['approved', 'paid']
                    )
                ),
                member_clicks=Count(
                    'affiliate__links__clicks',
                    filter=Q(affiliate__links__program=program)
                )
            ).order_by('-applied_at')

            extra_context.update({
                'program': program,
                'affiliates_count': affiliates_count,
                'pending_count': pending_count,
                'total_clicks': total_clicks,
                'total_commissions': commission_stats['total'] or 0,
                'pending_commissions': commission_stats['pending'] or 0,
                'approved_commissions': commission_stats['approved'] or 0,
                'paid_commissions': commission_stats['paid'] or 0,
                'total_links': total_links,
                'conversions': conversions,
                'members': members,
            })
        except Program.DoesNotExist:
            pass

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


# ============================================
# Affiliate Admin
# ============================================

@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    """Admin interface for Affiliates"""

    change_list_template = 'admin/affiliate/affiliate/change_list.html'
    change_form_template = 'admin/affiliate/affiliate/change_form.html'

    list_display = (
        'affiliate_code', 'customer_link', 'status_badge', 'programs_count',
        'total_commissions', 'outstanding_balance_display', 'total_paid_display', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = (
        'affiliate_code', 'user__username', 'user__email',
        'user__first_name', 'user__last_name', 'company_name', 'payment_email'
    )
    readonly_fields = ('affiliate_code', 'view_customer_profile', 'created_at', 'updated_at', 'affiliate_stats')
    autocomplete_fields = ['user']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('user', 'view_customer_profile', 'affiliate_code', 'status')
        }),
        (_('Contact Information'), {
            'fields': ('company_name', 'website'),
            'classes': ('collapse',)
        }),
        (_('Payment Information'), {
            'fields': ('payment_email', 'payment_method'),
        }),
        (_('Statistics'), {
            'fields': ('affiliate_stats',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [LinkInline, CommissionInline]

    actions = ['approve_affiliates', 'suspend_affiliates', 'activate_affiliates']

    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': 'warning',
            'active': 'success',
            'suspended': 'danger',
            'rejected': 'secondary'
        }
        icons = {
            'pending': 'fa-clock',
            'active': 'fa-check-circle',
            'suspended': 'fa-ban',
            'rejected': 'fa-times-circle'
        }
        return format_html(
            '<span class="badge badge-{}"><i class="fas {}"></i> {}</span>',
            colors.get(obj.status, 'secondary'),
            icons.get(obj.status, 'fa-circle'),
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    def customer_link(self, obj):
        """Link to customer profile instead of user"""
        try:
            customer_profile = obj.user.profile
            url = reverse('admin:accounts_customerprofile_change', args=[customer_profile.pk])
            display_name = obj.user.get_full_name() or obj.user.username
            return format_html(
                '<a href="{}" title="View customer profile">'
                '<i class="fas fa-user"></i> {}</a>',
                url,
                display_name
            )
        except Exception:
            # Fallback if no profile exists
            return format_html(
                '<i class="fas fa-user-slash text-muted"></i> {}',
                obj.user.username
            )
    customer_link.short_description = _('Customer')

    def view_customer_profile(self, obj):
        """Display a button to view the customer profile"""
        if not obj or not obj.pk:
            return '-'
        try:
            customer_profile = obj.user.profile
            url = reverse('admin:accounts_customerprofile_change', args=[customer_profile.pk])
            return format_html(
                '<a href="{}" class="button default" style="padding: 8px 16px; display: inline-block;">'
                '<i class="fas fa-user-circle"></i> View Customer Profile</a>',
                url
            )
        except Exception:
            return format_html(
                '<span class="text-muted">'
                '<i class="fas fa-exclamation-triangle"></i> No customer profile found</span>'
            )
    view_customer_profile.short_description = _('Customer Profile')

    def programs_count(self, obj):
        """Count of approved programs"""
        count = obj.programs.filter(
            affiliateprogrammembership__status='approved'
        ).count()
        return format_html('<i class="fas fa-briefcase"></i> {}', count)
    programs_count.short_description = _('Programs')

    def total_commissions(self, obj):
        """Total commissions earned"""
        total = obj.commissions.filter(
            status__in=['approved', 'paid']
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        return format_html(
            '<span class="badge badge-success"><i class="fas fa-dollar-sign"></i> ${}</span>',
            f'{total:,.2f}'
        )
    total_commissions.short_description = _('Total Earned')

    def outstanding_balance_display(self, obj):
        """Outstanding balance (approved but not paid)"""
        balance = obj.outstanding_balance

        return format_html(
            '<span class="badge badge-warning"><i class="fas fa-hourglass-half"></i> ${}</span>',
            f'{balance:,.2f}'
        )
    outstanding_balance_display.short_description = _('Outstanding Balance')
    outstanding_balance_display.admin_order_field = 'commissions__amount'

    def total_paid_display(self, obj):
        """Total paid amount"""
        paid = obj.total_paid

        return format_html(
            '<span class="badge badge-success"><i class="fas fa-check-circle"></i> ${}</span>',
            f'{paid:,.2f}'
        )
    total_paid_display.short_description = _('Total Paid')

    def affiliate_stats(self, obj):
        """Display comprehensive affiliate statistics"""
        if not obj.pk:
            return _('Save the affiliate first to see statistics')

        # Get stats
        total_links = obj.links.count()
        active_links = obj.links.filter(is_active=True).count()
        total_clicks = Click.objects.filter(link__affiliate=obj).count()

        total_earned = obj.commissions.filter(
            status__in=['approved', 'paid']
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        pending = obj.commissions.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
        approved = obj.commissions.filter(status='approved').aggregate(Sum('amount'))['amount__sum'] or 0
        paid = obj.commissions.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0

        total_payouts = obj.payouts.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0

        # Last 30 days stats
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_clicks = Click.objects.filter(
            link__affiliate=obj,
            clicked_at__gte=thirty_days_ago
        ).count()
        recent_commissions = obj.commissions.filter(
            created_at__gte=thirty_days_ago
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        html = f"""
        <div class="affiliate-stats-grid">
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-link"></i> {_('Tracking Links')}</div>
                <div class="stat-value">{total_links} <small>({active_links} active)</small></div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-mouse-pointer"></i> {_('Total Clicks')}</div>
                <div class="stat-value">{total_clicks:,}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-chart-line"></i> {_('Clicks (30 days)')}</div>
                <div class="stat-value">{recent_clicks:,}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-dollar-sign"></i> {_('Total Earned')}</div>
                <div class="stat-value">${total_earned:,.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-clock"></i> {_('Pending')}</div>
                <div class="stat-value text-warning">${pending:,.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-check"></i> {_('Approved')}</div>
                <div class="stat-value text-info">${approved:,.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-check-circle"></i> {_('Paid')}</div>
                <div class="stat-value text-success">${paid:,.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-money-bill-wave"></i> {_('Total Payouts')}</div>
                <div class="stat-value">${total_payouts:,.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label"><i class="fas fa-chart-area"></i> {_('Earnings (30 days)')}</div>
                <div class="stat-value">${recent_commissions:,.2f}</div>
            </div>
        </div>
        """
        return format_html(html)
    affiliate_stats.short_description = _('Affiliate Statistics')

    # Actions
    def approve_affiliates(self, request, queryset):
        """Approve selected affiliates"""
        count = 0
        for affiliate in queryset.filter(status='pending'):
            affiliate.status = 'active'
            affiliate.save()
            # Send approval email
            send_affiliate_approved_email(affiliate)
            count += 1
        self.message_user(request, _('{} affiliates approved and notified').format(count))
    approve_affiliates.short_description = _('Approve selected affiliates')

    def suspend_affiliates(self, request, queryset):
        """Suspend selected affiliates"""
        count = 0
        for affiliate in queryset.exclude(status='suspended'):
            affiliate.status = 'suspended'
            affiliate.save()
            # Send suspension email
            send_affiliate_suspended_email(affiliate)
            count += 1
        self.message_user(request, _('{} affiliates suspended and notified').format(count))
    suspend_affiliates.short_description = _('Suspend selected affiliates')

    def activate_affiliates(self, request, queryset):
        """Activate selected affiliates (reactivate from suspended)"""
        count = 0
        for affiliate in queryset.filter(status='suspended'):
            affiliate.status = 'active'
            affiliate.save()
            # Send activation email
            send_affiliate_activated_email(affiliate)
            count += 1
        self.message_user(request, _('{} affiliates activated and notified').format(count))
    activate_affiliates.short_description = _('Activate selected affiliates')

    def changelist_view(self, request, extra_context=None):
        """Override to add affiliates to context for card-based display"""
        extra_context = extra_context or {}

        # Get affiliates with annotations for the card display
        # Use different names to avoid conflict with model @property methods
        affiliates = Affiliate.objects.select_related('user').annotate(
            programs_count=Count(
                'programs',
                filter=Q(affiliateprogrammembership__status='approved')
            ),
            links_count=Count('links'),
            # Annotations for sorting (prefixed to avoid property conflict)
            sort_total_earned=Sum(
                'commissions__amount',
                filter=Q(commissions__status__in=['approved', 'paid'])
            ),
            sort_outstanding_balance=Sum(
                'commissions__amount',
                filter=Q(commissions__status='approved')
            )
        ).order_by('-created_at')

        extra_context['affiliates'] = affiliates

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Override to add dashboard context for affiliate detail view"""
        extra_context = extra_context or {}

        try:
            affiliate = Affiliate.objects.select_related('user').get(pk=object_id)

            # Get affiliate statistics
            programs_count = affiliate.programs.filter(
                affiliateprogrammembership__status='approved'
            ).count()
            links_count = affiliate.links.count()
            total_clicks = Click.objects.filter(link__affiliate=affiliate).count()

            # Commission stats
            commission_stats = affiliate.commissions.aggregate(
                total=Sum('amount', filter=Q(status__in=['approved', 'paid'])),
                pending=Sum('amount', filter=Q(status='pending')),
                approved=Sum('amount', filter=Q(status='approved')),
                paid=Sum('amount', filter=Q(status='paid'))
            )

            # Conversions (approved + paid commissions)
            conversions = affiliate.commissions.filter(
                status__in=['approved', 'paid']
            ).count()

            # Get memberships for the right column
            memberships = AffiliateProgramMembership.objects.filter(
                affiliate=affiliate
            ).select_related('program').order_by('-applied_at')

            # Get recent commissions
            recent_commissions = affiliate.commissions.select_related(
                'program'
            ).order_by('-created_at')[:5]

            extra_context.update({
                'affiliate': affiliate,
                'programs_count': programs_count,
                'links_count': links_count,
                'total_clicks': total_clicks,
                'total_earned': commission_stats['total'] or 0,
                'pending_commissions': commission_stats['pending'] or 0,
                'outstanding_balance': commission_stats['approved'] or 0,
                'paid_commissions': commission_stats['paid'] or 0,
                'conversions': conversions,
                'memberships': memberships,
                'recent_commissions': recent_commissions,
            })
        except Affiliate.DoesNotExist:
            pass

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


# ============================================
# Affiliate Program Membership Admin
# ============================================

@admin.register(AffiliateProgramMembership)
class AffiliateProgramMembershipAdmin(admin.ModelAdmin):
    """Admin interface for Program Memberships"""

    change_list_template = 'admin/affiliate/affiliateprogrammembership/change_list.html'

    list_display = (
        'affiliate', 'program', 'status_badge', 'applied_at', 'approved_at'
    )
    list_filter = ('status', 'applied_at', 'approved_at')
    search_fields = (
        'affiliate__affiliate_code', 'affiliate__user__username',
        'program__name', 'notes'
    )
    readonly_fields = ('applied_at', 'approved_at')
    autocomplete_fields = ['affiliate', 'program']

    fieldsets = (
        (_('Membership'), {
            'fields': ('affiliate', 'program', 'status')
        }),
        (_('Notes'), {
            'fields': ('notes',),
        }),
        (_('Timestamps'), {
            'fields': ('applied_at', 'approved_at'),
        }),
    )

    actions = ['approve_memberships', 'reject_memberships']

    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': 'warning',
            'approved': 'success',
            'rejected': 'danger'
        }
        icons = {
            'pending': 'fa-clock',
            'approved': 'fa-check-circle',
            'rejected': 'fa-times-circle'
        }
        return format_html(
            '<span class="badge badge-{}"><i class="fas {}"></i> {}</span>',
            colors.get(obj.status, 'secondary'),
            icons.get(obj.status, 'fa-circle'),
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    # Actions
    def approve_memberships(self, request, queryset):
        """Approve selected memberships"""
        now = timezone.now()
        count = 0
        for membership in queryset.filter(status='pending'):
            membership.status = 'approved'
            membership.approved_at = now
            membership.save()
            # Send approval email
            send_program_membership_approved_email(membership)
            count += 1
        self.message_user(request, _('{} memberships approved and notified').format(count))
    approve_memberships.short_description = _('Approve selected memberships')

    def reject_memberships(self, request, queryset):
        """Reject selected memberships"""
        count = 0
        for membership in queryset.filter(status='pending'):
            membership.status = 'rejected'
            membership.approved_at = None
            membership.save()
            # Send rejection email
            send_program_membership_rejected_email(membership)
            count += 1
        self.message_user(request, _('{} memberships rejected and notified').format(count))
    reject_memberships.short_description = _('Reject selected memberships')

    def changelist_view(self, request, extra_context=None):
        """Override to add memberships and programs to context for card-based display"""
        extra_context = extra_context or {}

        # Get memberships with annotations for the card display
        from django.db.models import F
        memberships = AffiliateProgramMembership.objects.select_related(
            'affiliate__user', 'program'
        ).annotate(
            commissions_count=Count(
                'affiliate__commissions',
                filter=Q(affiliate__commissions__program=F('program'))
            ),
            total_earned=Sum(
                'affiliate__commissions__amount',
                filter=Q(
                    affiliate__commissions__program=F('program'),
                    affiliate__commissions__status__in=['approved', 'paid']
                )
            ),
            links_count=Count(
                'affiliate__links',
                filter=Q(affiliate__links__program=F('program'))
            )
        ).order_by('-applied_at')

        extra_context['memberships'] = memberships

        # Get programs for filter dropdown
        extra_context['programs'] = Program.objects.filter(status='active').order_by('name')

        return super().changelist_view(request, extra_context=extra_context)


# ============================================
# Link Admin
# ============================================

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """Admin interface for Tracking Links"""

    list_display = (
        'link_code', 'affiliate', 'program', 'label', 'clicks_count',
        'is_active', 'created_at'
    )
    list_filter = ('is_active', 'created_at', 'program')
    search_fields = (
        'link_code', 'affiliate__affiliate_code', 'label', 'destination_url'
    )
    readonly_fields = ('link_code', 'created_at', 'updated_at', 'tracking_url', 'link_stats')
    autocomplete_fields = ['affiliate', 'program']

    fieldsets = (
        (_('Link Information'), {
            'fields': ('affiliate', 'program', 'link_code', 'destination_url', 'label', 'is_active')
        }),
        (_('Tracking'), {
            'fields': ('tracking_url', 'link_stats'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_links', 'deactivate_links']

    def tracking_url(self, obj):
        """Display the full tracking URL"""
        if not obj.pk:
            return _('Save the link first to get the tracking URL')

        url = obj.get_tracking_url()
        full_url = f"https://yourdomain.com{url}"  # Replace with actual domain
        return format_html(
            '<div style="margin-bottom: 0.5rem;">'
            '<input type="text" value="{}" style="width: 100%; padding: 0.5rem;" readonly>'
            '</div>'
            '<button type="button" onclick="navigator.clipboard.writeText(\'{}\'); '
            'alert(\'Copied to clipboard!\');" class="btn btn-sm btn-primary">'
            '<i class="fas fa-copy"></i> {}</button>',
            full_url, full_url, _('Copy to Clipboard')
        )
    tracking_url.short_description = _('Tracking URL')

    def clicks_count(self, obj):
        """Display click count"""
        count = obj.clicks.count()
        return format_html(
            '<a href="{}?link__id__exact={}">'
            '<i class="fas fa-mouse-pointer"></i> {}</a>',
            reverse('admin:affiliate_click_changelist'),
            obj.id,
            count
        )
    clicks_count.short_description = _('Clicks')

    def link_stats(self, obj):
        """Display link statistics"""
        if not obj.pk:
            return _('Save the link first to see statistics')

        total_clicks = obj.clicks.count()
        last_7_days = timezone.now() - timedelta(days=7)
        recent_clicks = obj.clicks.filter(clicked_at__gte=last_7_days).count()

        conversions = obj.clicks.filter(commissions__isnull=False).distinct().count()
        conversion_rate = (conversions / total_clicks * 100) if total_clicks > 0 else 0

        total_revenue = obj.clicks.filter(
            commissions__status__in=['approved', 'paid']
        ).aggregate(Sum('commissions__amount'))['commissions__amount__sum'] or 0

        html = f"""
        <div class="link-stats">
            <p><strong><i class="fas fa-mouse-pointer"></i> {_('Total Clicks')}:</strong> {total_clicks:,}</p>
            <p><strong><i class="fas fa-chart-line"></i> {_('Clicks (7 days)')}:</strong> {recent_clicks:,}</p>
            <p><strong><i class="fas fa-shopping-cart"></i> {_('Conversions')}:</strong> {conversions}</p>
            <p><strong><i class="fas fa-percentage"></i> {_('Conversion Rate')}:</strong> {conversion_rate:.2f}%</p>
            <p><strong><i class="fas fa-dollar-sign"></i> {_('Total Revenue')}:</strong> ${total_revenue:,.2f}</p>
        </div>
        """
        return format_html(html)
    link_stats.short_description = _('Link Statistics')

    # Actions
    def activate_links(self, request, queryset):
        """Activate selected links"""
        count = queryset.update(is_active=True)
        self.message_user(request, _('{} links activated').format(count))
    activate_links.short_description = _('Activate selected links')

    def deactivate_links(self, request, queryset):
        """Deactivate selected links"""
        count = queryset.update(is_active=False)
        self.message_user(request, _('{} links deactivated').format(count))
    deactivate_links.short_description = _('Deactivate selected links')


# ============================================
# Click Admin
# ============================================

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    """Admin interface for Click Tracking"""

    list_display = (
        'link', 'ip_address', 'clicked_at', 'has_conversion'
    )
    list_filter = ('clicked_at',)
    search_fields = (
        'ip_address', 'link__link_code', 'link__affiliate__affiliate_code',
        'session_id', 'cookie_value'
    )
    readonly_fields = ('clicked_at', 'click_details')
    autocomplete_fields = ['link']

    fieldsets = (
        (_('Click Information'), {
            'fields': ('link', 'ip_address', 'clicked_at')
        }),
        (_('Technical Details'), {
            'fields': ('user_agent', 'referrer', 'session_id', 'cookie_value'),
            'classes': ('collapse',)
        }),
        (_('Additional Information'), {
            'fields': ('click_details',),
            'classes': ('collapse',)
        }),
    )

    def has_conversion(self, obj):
        """Check if click resulted in conversion"""
        has_commission = obj.commissions.exists()
        if has_commission:
            return format_html(
                '<span class="badge badge-success"><i class="fas fa-check-circle"></i> {}</span>',
                _('Yes')
            )
        return format_html(
            '<span class="badge badge-secondary"><i class="fas fa-times"></i> {}</span>',
            _('No')
        )
    has_conversion.short_description = _('Conversion')

    def click_details(self, obj):
        """Display detailed click information"""
        if not obj.pk:
            return _('Save the click first to see details')

        commissions = obj.commissions.all()
        commission_html = ""
        if commissions:
            commission_html = "<h4>" + str(_("Conversions")) + "</h4><ul>"
            for comm in commissions:
                commission_html += f"<li><i class='fas fa-shopping-cart'></i> Order #{comm.order.id} - ${comm.amount} ({comm.get_status_display()})</li>"
            commission_html += "</ul>"
        else:
            commission_html = f"<p><em><i class='fas fa-info-circle'></i> {_('No conversions yet')}</em></p>"

        html = f"""
        <div class="click-details">
            <h4><i class="fas fa-link"></i> {_('Link Information')}</h4>
            <p><strong>{_('Affiliate')}:</strong> {obj.link.affiliate}</p>
            <p><strong>{_('Program')}:</strong> {obj.link.program}</p>
            <p><strong>{_('Destination')}:</strong> <a href="{obj.link.destination_url}" target="_blank">{obj.link.destination_url}</a></p>

            {commission_html}
        </div>
        """
        return format_html(html)
    click_details.short_description = _('Click Details')


# ============================================
# Commission Admin
# ============================================

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    """Admin interface for Commissions"""

    change_list_template = 'admin/affiliate/commission/change_list.html'

    list_display = (
        'id', 'affiliate', 'program', 'order_link', 'amount',
        'status_badge', 'created_at'
    )
    list_filter = ('status', 'created_at', 'approved_at', 'paid_at', 'program')
    search_fields = (
        'affiliate__affiliate_code', 'affiliate__user__username',
        'program__name', 'order__id', 'notes'
    )
    readonly_fields = ('created_at', 'approved_at', 'paid_at')
    autocomplete_fields = ['affiliate', 'program', 'order', 'click']

    fieldsets = (
        (_('Commission Information'), {
            'fields': ('affiliate', 'program', 'order', 'click', 'amount', 'status')
        }),
        (_('Notes'), {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'approved_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_commissions', 'reject_commissions', 'mark_as_paid']

    def order_link(self, obj):
        """Link to order admin"""
        return format_html(
            '<a href="{}" target="_blank">'
            '<i class="fas fa-external-link-alt"></i> Order #{}</a>',
            reverse('admin:orders_order_change', args=[obj.order.id]),
            obj.order.id
        )
    order_link.short_description = _('Order')

    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': 'warning',
            'approved': 'info',
            'rejected': 'danger',
            'paid': 'success'
        }
        icons = {
            'pending': 'fa-clock',
            'approved': 'fa-check',
            'rejected': 'fa-times',
            'paid': 'fa-check-circle'
        }
        return format_html(
            '<span class="badge badge-{}"><i class="fas {}"></i> {}</span>',
            colors.get(obj.status, 'secondary'),
            icons.get(obj.status, 'fa-circle'),
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    # Actions
    def approve_commissions(self, request, queryset):
        """Approve selected commissions"""
        now = timezone.now()
        count = 0
        for commission in queryset.filter(status='pending'):
            commission.status = 'approved'
            commission.approved_at = now
            commission.save()
            # Send approval email
            send_commission_approved_email(commission)
            count += 1
        self.message_user(request, _('{} commissions approved and notified').format(count))
    approve_commissions.short_description = _('Approve selected commissions')

    def reject_commissions(self, request, queryset):
        """Reject selected commissions"""
        count = 0
        for commission in queryset.filter(status='pending'):
            commission.status = 'rejected'
            commission.save()
            # Send rejection email
            send_commission_rejected_email(commission)
            count += 1
        self.message_user(request, _('{} commissions rejected and notified').format(count))
    reject_commissions.short_description = _('Reject selected commissions')

    def mark_as_paid(self, request, queryset):
        """Mark selected commissions as paid"""
        now = timezone.now()
        count = queryset.filter(status='approved').update(status='paid', paid_at=now)
        self.message_user(request, _('{} commissions marked as paid').format(count))
    mark_as_paid.short_description = _('Mark selected commissions as paid')

    def get_row_css_classes(self, request, obj):
        """Add CSS classes to rows based on status"""
        return f'status-{obj.status}'

    def changelist_view(self, request, extra_context=None):
        """Add statistics to the changelist context"""
        extra_context = extra_context or {}

        # Get commission statistics
        stats = Commission.objects.aggregate(
            pending_count=Count('id', filter=Q(status='pending')),
            approved_count=Count('id', filter=Q(status='approved')),
            paid_count=Count('id', filter=Q(status='paid')),
            rejected_count=Count('id', filter=Q(status='rejected')),
            total_amount=Sum('amount', filter=Q(status__in=['approved', 'paid']))
        )

        extra_context['pending_count'] = stats['pending_count'] or 0
        extra_context['approved_count'] = stats['approved_count'] or 0
        extra_context['paid_count'] = stats['paid_count'] or 0
        extra_context['rejected_count'] = stats['rejected_count'] or 0
        extra_context['total_commissions'] = stats['total_amount'] or 0

        # Get pending payouts count
        extra_context['pending_payouts'] = Payout.objects.filter(
            status__in=['pending', 'processing']
        ).count()

        # Get affiliates and programs for filter dropdowns
        extra_context['affiliates'] = Affiliate.objects.select_related('user').filter(
            commissions__isnull=False
        ).distinct().order_by('user__username')
        extra_context['programs'] = Program.objects.filter(
            commissions__isnull=False
        ).distinct().order_by('name')

        # Get recent commissions for card display (limit 20)
        extra_context['recent_commissions'] = Commission.objects.select_related(
            'affiliate__user', 'program', 'order'
        ).prefetch_related('payouts').order_by('-created_at')[:20]

        return super().changelist_view(request, extra_context=extra_context)


# ============================================
# Payout Admin
# ============================================

class CommissionInlineForPayout(admin.TabularInline):
    """Inline for viewing commissions in payout admin"""
    model = Payout.commissions.through
    extra = 0
    verbose_name = _('Commission')
    verbose_name_plural = _('Commissions')
    fields = ('commission_display', 'order_display', 'amount_display', 'status_display')
    readonly_fields = ('commission_display', 'order_display', 'amount_display', 'status_display')
    can_delete = False

    def commission_display(self, obj):
        if obj.commission:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:affiliate_commission_change', args=[obj.commission.pk]),
                f'Commission #{obj.commission.pk}'
            )
        return '-'
    commission_display.short_description = _('Commission')

    def order_display(self, obj):
        if obj.commission and obj.commission.order:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:orders_order_change', args=[obj.commission.order.pk]),
                f'Order #{obj.commission.order.pk}'
            )
        return '-'
    order_display.short_description = _('Order')

    def amount_display(self, obj):
        if obj.commission:
            return f'${obj.commission.amount:,.2f}'
        return '-'
    amount_display.short_description = _('Amount')

    def status_display(self, obj):
        if obj.commission:
            return obj.commission.get_status_display()
        return '-'
    status_display.short_description = _('Status')


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    """Admin interface for Payouts"""

    change_list_template = 'admin/affiliate/payout/change_list.html'

    list_display = (
        'id', 'affiliate', 'commission_count_display', 'amount', 'method',
        'status_badge', 'created_at', 'completed_at'
    )
    list_filter = ('status', 'method', 'created_at', 'completed_at')
    search_fields = (
        'affiliate__affiliate_code', 'affiliate__user__username',
        'reference', 'notes'
    )
    readonly_fields = (
        'created_at', 'processed_at', 'completed_at', 'payout_summary',
        'provider_reference', 'provider_response'
    )
    autocomplete_fields = ['affiliate']
    filter_horizontal = ['commissions']

    fieldsets = (
        (_('Payout Information'), {
            'fields': ('affiliate', 'amount', 'currency', 'method', 'status', 'reference')
        }),
        (_('Commissions'), {
            'fields': ('commissions', 'payout_summary'),
            'description': _('Select the commissions included in this payout')
        }),
        (_('Provider Integration'), {
            'fields': ('provider_account', 'provider_reference', 'provider_response'),
            'classes': ('collapse',),
            'description': _('Details from the payout provider (PayPal/Airwallex)')
        }),
        (_('Notes'), {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'processed_at', 'completed_at'),
        }),
    )

    inlines = [CommissionInlineForPayout]

    actions = [
        'mark_as_processing', 'mark_as_completed', 'mark_as_failed',
        'cancel_payouts', 'process_with_provider'
    ]

    def changelist_view(self, request, extra_context=None):
        """Override to add statistics for the payout change list."""
        from django.db.models import Sum, Q
        from payout_providers.models import PayoutProviderAccount

        extra_context = extra_context or {}

        # Calculate statistics
        all_payouts = Payout.objects.all()

        extra_context['total_count'] = all_payouts.count()
        extra_context['pending_count'] = all_payouts.filter(status='pending').count()
        extra_context['pending_amount'] = all_payouts.filter(status='pending').aggregate(
            total=Sum('amount'))['total'] or 0
        extra_context['processing_count'] = all_payouts.filter(status='processing').count()
        extra_context['completed_count'] = all_payouts.filter(status='completed').count()
        extra_context['completed_amount'] = all_payouts.filter(status='completed').aggregate(
            total=Sum('amount'))['total'] or 0
        extra_context['failed_count'] = all_payouts.filter(
            Q(status='failed') | Q(status='cancelled')).count()

        # Provider accounts for filter
        extra_context['provider_accounts'] = PayoutProviderAccount.objects.filter(
            is_active=True).values('id', 'name')

        # Method choices for filter
        extra_context['method_choices'] = all_payouts.values_list(
            'method', flat=True).distinct()

        # Payouts for display
        extra_context['payouts'] = self.get_queryset(request).select_related(
            'affiliate__user', 'provider_account'
        ).prefetch_related('commissions')

        return super().changelist_view(request, extra_context=extra_context)

    def commission_count_display(self, obj):
        """Display count of commissions in payout"""
        count = obj.commission_count
        return format_html(
            '<span class="badge badge-info"><i class="fas fa-list"></i> {} commission{}</span>',
            count,
            's' if count != 1 else ''
        )
    commission_count_display.short_description = _('Commissions')

    def payout_summary(self, obj):
        """Display summary of payout"""
        if not obj.pk:
            return _('Save to view summary')

        from core.utils import safe_money_sum
        commissions_list = obj.commissions.all()
        total_amount = safe_money_sum(c.amount for c in commissions_list)

        html = f"""
        <div style="background: var(--body-bg, #f8f9fa); padding: 15px; border-radius: 8px; border: 1px solid var(--border-color, #dee2e6);">
            <h4 style="margin-top: 0; color: var(--body-fg, #333);">{_('Payout Summary')}</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div><strong>{_('Number of Commissions')}:</strong> {obj.commission_count}</div>
                <div><strong>{_('Payout Amount')}:</strong> ${obj.amount:,.2f}</div>
                <div><strong>{_('Calculated Total')}:</strong> ${total_amount:,.2f}</div>
                <div><strong>{_('Payment Method')}:</strong> {obj.method}</div>
                <div><strong>{_('Status')}:</strong> {obj.get_status_display()}</div>
                <div><strong>{_('Reference')}:</strong> {obj.reference or _('Not set')}</div>
            </div>
        </div>
        """
        return format_html(html)
    payout_summary.short_description = _('Summary')

    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': 'warning',
            'processing': 'info',
            'completed': 'success',
            'failed': 'danger',
            'cancelled': 'secondary'
        }
        icons = {
            'pending': 'fa-clock',
            'processing': 'fa-spinner fa-spin',
            'completed': 'fa-check-circle',
            'failed': 'fa-times-circle',
            'cancelled': 'fa-ban'
        }
        return format_html(
            '<span class="badge badge-{}"><i class="fas {}"></i> {}</span>',
            colors.get(obj.status, 'secondary'),
            icons.get(obj.status, 'fa-circle'),
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    # Actions
    def mark_as_processing(self, request, queryset):
        """Mark selected payouts as processing"""
        count = 0
        for payout in queryset.filter(status='pending'):
            payout.mark_as_processing()
            # Send processing email
            send_payout_processing_email(payout)
            count += 1

        self.message_user(
            request,
            _('Successfully marked {} payout(s) as processing and notified affiliates.').format(count),
            level='success' if count > 0 else 'warning'
        )
    mark_as_processing.short_description = _('Mark as processing')

    def mark_as_completed(self, request, queryset):
        """Mark selected payouts as completed and update commissions"""
        count = 0
        commission_count = 0

        for payout in queryset.filter(status__in=['pending', 'processing']):
            comm_count = payout.commission_count
            payout.mark_as_completed()
            # Send completion email
            send_payout_completed_email(payout)
            count += 1
            commission_count += comm_count

        if count > 0:
            self.message_user(
                request,
                _('Successfully completed {} payout(s) covering {} commission(s). Commissions marked as paid and affiliates notified.').format(
                    count, commission_count
                ),
                level='success'
            )
        else:
            self.message_user(
                request,
                _('No payouts were eligible for completion (must be pending or processing).'),
                level='warning'
            )
    mark_as_completed.short_description = _('Mark as completed (and pay commissions)')

    def mark_as_failed(self, request, queryset):
        """Mark selected payouts as failed"""
        count = 0
        for payout in queryset.exclude(status='completed'):
            payout.mark_as_failed(notes=_('Marked as failed by admin'))
            # Send failure email
            send_payout_failed_email(payout)
            count += 1

        self.message_user(
            request,
            _('Marked {} payout(s) as failed and notified affiliates.').format(count),
            level='warning' if count > 0 else 'info'
        )
    mark_as_failed.short_description = _('Mark as failed')

    def cancel_payouts(self, request, queryset):
        """Cancel payouts and revert commission statuses"""
        count = 0
        commission_count = 0

        for payout in queryset.exclude(status='cancelled'):
            comm_count = payout.commission_count
            payout.cancel(notes=_('Cancelled by admin'))
            # Send cancellation email
            send_payout_cancelled_email(payout)
            count += 1
            commission_count += comm_count

        if count > 0:
            self.message_user(
                request,
                _('Cancelled {} payout(s). {} commission(s) reverted to approved status. Affiliates notified.').format(
                    count, commission_count
                ),
                level='warning'
            )
        else:
            self.message_user(
                request,
                _('No payouts to cancel.'),
                level='info'
            )
    cancel_payouts.short_description = _('Cancel payouts (revert commissions)')

    def process_with_provider(self, request, queryset):
        """
        Process selected payouts through configured payout provider (async).

        Dispatches to PayPal or Airwallex based on affiliate's payment method.
        Uses Celery tasks for async processing with retry support.
        """
        from payout_providers.models import PayoutProviderAccount
        from payout_providers.tasks import process_payout, process_batch_payouts

        # Get available provider accounts
        paypal_account = PayoutProviderAccount.objects.filter(
            provider_type='paypal',
            is_active=True,
            is_default=True
        ).first()

        airwallex_account = PayoutProviderAccount.objects.filter(
            provider_type='airwallex',
            is_active=True,
            is_default=True
        ).first()

        if not paypal_account and not airwallex_account:
            self.message_user(
                request,
                _('No active payout providers configured. Please configure PayPal or Airwallex.'),
                level='error'
            )
            return

        pending_payouts = queryset.filter(status='pending').select_related('affiliate')
        if not pending_payouts.exists():
            self.message_user(
                request,
                _('No pending payouts selected. Only pending payouts can be processed.'),
                level='warning'
            )
            return

        # Group payouts by provider for batch optimization
        paypal_payout_ids = []
        airwallex_payout_ids = []
        skipped_count = 0

        for payout in pending_payouts:
            affiliate = payout.affiliate
            payment_method = affiliate.payment_method

            # Determine which provider to use
            if payment_method == 'paypal' and paypal_account:
                paypal_payout_ids.append(payout.id)
            elif payment_method == 'bank_transfer' and airwallex_account:
                airwallex_payout_ids.append(payout.id)
            elif paypal_account:
                # Fallback to PayPal if available
                paypal_payout_ids.append(payout.id)
            elif airwallex_account:
                # Fallback to Airwallex if available
                airwallex_payout_ids.append(payout.id)
            else:
                skipped_count += 1

        queued_count = 0

        # Use batch processing for PayPal (up to 15,000 per batch)
        if paypal_payout_ids and paypal_account:
            try:
                if len(paypal_payout_ids) > 1:
                    # Batch process for efficiency
                    process_batch_payouts.delay(paypal_payout_ids, paypal_account.id)
                    queued_count += len(paypal_payout_ids)
                else:
                    # Single payout
                    process_payout.delay(paypal_payout_ids[0], paypal_account.id)
                    queued_count += 1
            except Exception as e:
                self.message_user(
                    request,
                    _('Failed to queue PayPal payouts: {}').format(str(e)),
                    level='error'
                )

        # Process Airwallex payouts individually (no batch support)
        if airwallex_payout_ids and airwallex_account:
            try:
                for payout_id in airwallex_payout_ids:
                    process_payout.delay(payout_id, airwallex_account.id)
                    queued_count += 1
            except Exception as e:
                self.message_user(
                    request,
                    _('Failed to queue Airwallex payouts: {}').format(str(e)),
                    level='error'
                )

        # Report results
        if queued_count:
            self.message_user(
                request,
                _('Queued {} payout(s) for async processing. Status will update via webhooks.').format(queued_count),
                level='success'
            )

        if skipped_count:
            self.message_user(
                request,
                _('Skipped {} payout(s) - no provider available for their payment method.').format(skipped_count),
                level='warning'
            )
    process_with_provider.short_description = _('Process with payout provider (PayPal/Airwallex)')


# ============================================
# Affiliate Settings Admin (Singleton)
# ============================================

class AffiliateSettingsForm(forms.ModelForm):
    """Form for AffiliateSettings with translatable field widgets"""

    class Meta:
        model = AffiliateSettings
        fields = '__all__'
        widgets = {
            'hero_title': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'hero_subtitle': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 2})
            ),
            'features_title': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'how_it_works_title': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'cta_title': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'cta_description': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 2})
            ),
            'welcome_message': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 3})
            ),
        }


@admin.register(AffiliateSettings)
class AffiliateSettingsAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """Admin interface for Affiliate Portal Settings (singleton)"""

    form = AffiliateSettingsForm
    change_form_template = 'admin/affiliate/affiliatesettings/change_form.html'
    list_display = ('__str__', 'hero_title', 'updated_at')

    # Fields that can be translated via the translation editor
    translatable_fields = [
        'hero_title', 'hero_subtitle', 'features_title',
        'how_it_works_title', 'cta_title', 'cta_description', 'welcome_message'
    ]

    fieldsets = (
        (_('Hero Section'), {
            'fields': ('hero_title', 'hero_subtitle'),
            'description': _('Customize the main banner on the affiliate landing page')
        }),
        (_('Features Section'), {
            'fields': ('features_title', 'features'),
            'description': _('List of features to display. Each item should have: icon (FontAwesome class), title, and description'),
        }),
        (_('How It Works Section'), {
            'fields': ('how_it_works_title', 'steps'),
            'description': _('Steps showing how the affiliate program works. Each item should have: title and description'),
        }),
        (_('Call to Action Section'), {
            'fields': ('cta_title', 'cta_description'),
            'description': _('Final call-to-action section at the bottom of the page')
        }),
        (_('Registration Form'), {
            'fields': ('registration_form', 'allow_guest_registration', 'terms_url'),
            'description': _('Configure the affiliate registration form. Leave form blank to use default fields.')
        }),
        (_('Registration Settings'), {
            'fields': ('require_approval', 'welcome_message'),
            'description': _('Control how new affiliate registrations are handled')
        }),
    )

    class Media:
        js = TranslatableAdminMixin.Media.js
        css = TranslatableAdminMixin.Media.css

    def has_add_permission(self, request):
        """Only allow one instance"""
        return not AffiliateSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of settings"""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect to change view if settings exist, otherwise to add view"""
        from django.shortcuts import redirect
        settings = AffiliateSettings.objects.first()
        if settings:
            return redirect('admin:affiliate_affiliatesettings_change', settings.pk)
        # No settings exist, redirect to add view
        return redirect('admin:affiliate_affiliatesettings_add')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add context for the live preview and translation support"""
        extra_context = extra_context or {}

        try:
            settings = AffiliateSettings.objects.get(pk=object_id)
            extra_context['affiliate_settings'] = settings
        except AffiliateSettings.DoesNotExist:
            pass

        # JSON-encode translatable_fields for JavaScript consumption
        # The mixin will add translatable_fields, but we need it JSON-encoded
        extra_context['translatable_fields'] = json.dumps(self.translatable_fields)

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        """Add context for the live preview on add page"""
        extra_context = extra_context or {}

        # Provide default values for preview
        extra_context['affiliate_settings'] = None

        # JSON-encode translatable_fields for JavaScript consumption
        extra_context['translatable_fields'] = json.dumps(self.translatable_fields)

        return super().add_view(request, form_url, extra_context=extra_context)


@admin.register(AffiliateReportSettings)
class AffiliateReportSettingsAdmin(admin.ModelAdmin):
    """Admin interface for Affiliate Report Settings (singleton)"""

    list_display = ('__str__', 'monthly_report_enabled', 'monthly_report_day', 'monthly_report_hour', 'updated_at')

    fieldsets = (
        (_('Monthly Report Settings'), {
            'fields': ('monthly_report_enabled', 'monthly_report_day', 'monthly_report_hour', 'include_top_orders_count'),
            'description': _('Configure when and how monthly performance reports are sent to affiliates')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        """Only allow one instance"""
        return not AffiliateReportSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of settings"""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect changelist to edit page for singleton model."""
        from django.shortcuts import redirect
        from django.urls import reverse

        # Get or create singleton instance
        settings = AffiliateReportSettings.get_settings()

        # Redirect to change page
        url = reverse('admin:affiliate_affiliatereportsettings_change', args=[settings.pk])
        return redirect(url)
