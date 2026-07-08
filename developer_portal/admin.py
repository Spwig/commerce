"""
Developer Portal Admin
Admin interface for managing developer profiles and reviewing component submissions.
"""

import logging

from django.contrib import admin
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.html import format_html
from django.contrib import messages

from .models import (
    DeveloperProfile, ComponentSubmission, SubmissionReview,
    DeveloperLicenseRequest, ComponentAnalytics,
    ComponentReviewMirror, ComponentVersionMirror,
)
from .services.publishing import PublishingService
from .services.email_service import DeveloperEmailService

logger = logging.getLogger(__name__)


class SubmissionReviewInline(admin.TabularInline):
    model = SubmissionReview
    extra = 0
    readonly_fields = ('reviewer', 'action', 'comment', 'created_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DeveloperProfile)
class DeveloperProfileAdmin(admin.ModelAdmin):
    change_list_template = 'admin/developer_portal/developerprofile/change_list.html'
    list_display = (
        'display_name', 'developer_slug', 'user', 'status_badge',
        'company_name', 'country', 'submissions_count', 'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('display_name', 'developer_slug', 'user__email', 'company_name')
    readonly_fields = (
        'api_key', 'upgrade_server_author_slug', 'created_at',
        'updated_at', 'approved_at',
    )
    actions = ['approve_developers', 'reject_developers', 'suspend_developers']

    fieldsets = (
        (None, {
            'fields': (
                'user', 'developer_slug', 'display_name', 'bio',
                'website', 'company_name', 'country', 'logo', 'status',
            ),
        }),
        (_('Review'), {
            'fields': ('rejection_reason',),
        }),
        (_('API Access'), {
            'fields': ('api_key', 'upgrade_server_author_slug'),
        }),
        (_('Notifications'), {
            'fields': ('review_notification_preference',),
        }),
        (_('Payout Settings'), {
            'fields': ('payout_method', 'payout_details'),
            'classes': ('collapse',),
        }),
        (_('Timestamps'), {
            'fields': ('terms_accepted_at', 'created_at', 'updated_at', 'approved_at'),
        }),
    )

    def status_badge(self, obj):
        css_map = {
            'pending': 'dev-admin-badge-pending',
            'approved': 'dev-admin-badge-approved',
            'rejected': 'dev-admin-badge-rejected',
            'suspended': 'dev-admin-badge-suspended',
        }
        css_class = css_map.get(obj.status, 'dev-admin-badge-suspended')
        return format_html(
            '<span class="dev-admin-badge {}">{}</span>',
            css_class, obj.get_status_display(),
        )
    status_badge.short_description = _('Status')

    def submissions_count(self, obj):
        return obj.submissions.count()
    submissions_count.short_description = _('Submissions')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        stats = DeveloperProfile.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            approved=Count('id', filter=Q(status='approved')),
            suspended=Count('id', filter=Q(status='suspended')),
        )
        extra_context['stats'] = stats
        return super().changelist_view(request, extra_context)

    @admin.action(description=_('Approve selected developers'))
    def approve_developers(self, request, queryset):
        publishing_service = PublishingService()
        approved = 0
        for profile in queryset.filter(status=DeveloperProfile.Status.PENDING):
            # Create author on upgrade server
            author_slug = publishing_service.ensure_author(profile)
            if author_slug:
                profile.upgrade_server_author_slug = author_slug
            profile.approve()
            DeveloperEmailService.send_account_approved(profile)
            approved += 1
        messages.success(request, _('%(count)d developer(s) approved.') % {'count': approved})

    @admin.action(description=_('Reject selected developers'))
    def reject_developers(self, request, queryset):
        rejected = 0
        for profile in queryset.filter(status=DeveloperProfile.Status.PENDING):
            profile.status = DeveloperProfile.Status.REJECTED
            profile.save(update_fields=['status', 'updated_at'])
            DeveloperEmailService.send_account_rejected(profile)
            rejected += 1
        messages.success(request, _('%(count)d developer(s) rejected.') % {'count': rejected})

    @admin.action(description=_('Suspend selected developers'))
    def suspend_developers(self, request, queryset):
        suspended = 0
        for profile in queryset.filter(status=DeveloperProfile.Status.APPROVED):
            profile.status = DeveloperProfile.Status.SUSPENDED
            profile.save(update_fields=['status', 'updated_at'])
            DeveloperEmailService.send_account_suspended(profile)
            suspended += 1
        messages.success(request, _('%(count)d developer(s) suspended.') % {'count': suspended})


@admin.register(ComponentSubmission)
class ComponentSubmissionAdmin(admin.ModelAdmin):
    change_list_template = 'admin/developer_portal/componentsubmission/change_list.html'
    list_display = (
        'component_name', 'type_badge', 'version', 'developer_name',
        'validation_badge', 'review_badge', 'pricing_display', 'submitted_at',
    )
    list_filter = ('component_type', 'validation_status', 'review_status', 'pricing_model', 'is_published')
    search_fields = ('component_name', 'component_slug', 'developer__display_name')
    readonly_fields = (
        'id', 'package_checksum', 'package_size_bytes', 'manifest_data',
        'validation_status', 'validation_results', 'validated_at',
        'is_published', 'published_at', 'upgrade_server_component_slug',
        'upgrade_server_version_id', 'submitted_at', 'updated_at',
    )
    inlines = [SubmissionReviewInline]
    actions = [
        'approve_submissions', 'reject_submissions',
        'request_revision', 'publish_to_upgrade_server',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'id', 'developer', 'component_type', 'component_slug',
                'component_name', 'version', 'description', 'changelog',
            ),
        }),
        (_('Package'), {
            'fields': (
                'package_file', 'package_checksum', 'package_size_bytes',
            ),
        }),
        (_('Visual Assets'), {
            'fields': ('thumbnail', 'preview_images'),
        }),
        (_('Validation'), {
            'fields': (
                'validation_status', 'validation_results', 'validated_at',
            ),
        }),
        (_('Review'), {
            'fields': (
                'review_status', 'reviewer', 'review_notes', 'reviewed_at',
            ),
        }),
        (_('Publication'), {
            'fields': (
                'is_published', 'published_at',
                'upgrade_server_component_slug', 'upgrade_server_version_id',
            ),
        }),
        (_('Pricing'), {
            'fields': ('pricing_model', 'price', 'currency'),
        }),
        (_('Manifest'), {
            'fields': ('manifest_data',),
            'classes': ('collapse',),
        }),
    )

    def developer_name(self, obj):
        return obj.developer.display_name
    developer_name.short_description = _('Developer')

    def type_badge(self, obj):
        return format_html(
            '<span class="dev-admin-badge dev-admin-badge-type">'
            '<i class="fas {}"></i> {}</span>',
            obj.type_icon, obj.type_display,
        )
    type_badge.short_description = _('Type')

    def validation_badge(self, obj):
        css_map = {
            'pending': 'dev-admin-badge-pending',
            'validating': 'dev-admin-badge-validating',
            'passed': 'dev-admin-badge-passed',
            'failed': 'dev-admin-badge-failed',
        }
        css_class = css_map.get(obj.validation_status, 'dev-admin-badge-pending')
        return format_html(
            '<span class="dev-admin-badge {}">{}</span>',
            css_class, obj.get_validation_status_display(),
        )
    validation_badge.short_description = _('Validation')

    def review_badge(self, obj):
        css_map = {
            'pending': 'dev-admin-badge-pending',
            'in_review': 'dev-admin-badge-in-review',
            'approved': 'dev-admin-badge-approved',
            'rejected': 'dev-admin-badge-rejected',
            'revision_requested': 'dev-admin-badge-revision-requested',
        }
        css_class = css_map.get(obj.review_status, 'dev-admin-badge-pending')
        return format_html(
            '<span class="dev-admin-badge {}">{}</span>',
            css_class, obj.get_review_status_display(),
        )
    review_badge.short_description = _('Review')

    def pricing_display(self, obj):
        if obj.is_free:
            return format_html(
                '<span class="dev-admin-badge-free">{}</span>',
                _('Free'),
            )
        return format_html(
            '<span class="dev-admin-badge-paid">{} {}</span>',
            obj.currency, obj.price,
        )
    pricing_display.short_description = _('Pricing')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        stats = ComponentSubmission.objects.aggregate(
            total=Count('id'),
            pending_review=Count('id', filter=Q(
                validation_status='passed', review_status='pending',
            )),
            approved=Count('id', filter=Q(review_status='approved')),
            published=Count('id', filter=Q(is_published=True)),
        )
        extra_context['stats'] = stats
        return super().changelist_view(request, extra_context)

    def _do_review_action(self, request, queryset, action, new_status, success_msg):
        """Helper for review actions."""
        count = 0
        for submission in queryset.filter(
            validation_status=ComponentSubmission.ValidationStatus.PASSED,
        ):
            submission.review_status = new_status
            submission.reviewer = request.user
            submission.reviewed_at = timezone.now()
            submission.review_notes = request.POST.get('review_notes', '')
            submission.save(update_fields=[
                'review_status', 'reviewer', 'reviewed_at',
                'review_notes', 'updated_at',
            ])
            SubmissionReview.objects.create(
                submission=submission,
                reviewer=request.user,
                action=action,
                comment=submission.review_notes,
            )
            # Send email notification based on review outcome
            if new_status == ComponentSubmission.ReviewStatus.APPROVED:
                DeveloperEmailService.send_submission_approved(submission)
            elif new_status == ComponentSubmission.ReviewStatus.REJECTED:
                DeveloperEmailService.send_submission_rejected(submission)
            elif new_status == ComponentSubmission.ReviewStatus.REVISION_REQUESTED:
                DeveloperEmailService.send_revision_requested(submission)
            count += 1
        messages.success(request, success_msg % {'count': count})

    @admin.action(description=_('Approve selected submissions'))
    def approve_submissions(self, request, queryset):
        self._do_review_action(
            request, queryset,
            SubmissionReview.Action.APPROVE,
            ComponentSubmission.ReviewStatus.APPROVED,
            _('%(count)d submission(s) approved.'),
        )

    @admin.action(description=_('Reject selected submissions'))
    def reject_submissions(self, request, queryset):
        self._do_review_action(
            request, queryset,
            SubmissionReview.Action.REJECT,
            ComponentSubmission.ReviewStatus.REJECTED,
            _('%(count)d submission(s) rejected.'),
        )

    @admin.action(description=_('Request revision for selected submissions'))
    def request_revision(self, request, queryset):
        self._do_review_action(
            request, queryset,
            SubmissionReview.Action.REQUEST_REVISION,
            ComponentSubmission.ReviewStatus.REVISION_REQUESTED,
            _('Revision requested for %(count)d submission(s).'),
        )

    @admin.action(description=_('Publish approved submissions to upgrade server'))
    def publish_to_upgrade_server(self, request, queryset):
        publishing_service = PublishingService()
        published = 0
        errors = []

        for submission in queryset.filter(
            review_status=ComponentSubmission.ReviewStatus.APPROVED,
            is_published=False,
        ):
            result = publishing_service.publish_component(submission)
            if result['success']:
                submission.is_published = True
                submission.published_at = timezone.now()
                submission.upgrade_server_component_slug = result['component_slug']
                submission.upgrade_server_version_id = result['version_id']
                submission.save(update_fields=[
                    'is_published', 'published_at',
                    'upgrade_server_component_slug', 'upgrade_server_version_id',
                    'updated_at',
                ])
                DeveloperEmailService.send_component_published(submission)
                published += 1
            else:
                errors.append(f'{submission.component_name}: {result["error"]}')

        if published:
            messages.success(
                request,
                _('%(count)d submission(s) published to upgrade server.') % {'count': published},
            )
        if errors:
            messages.error(
                request,
                _('Failed to publish: %(errors)s') % {'errors': '; '.join(errors)},
            )


@admin.register(SubmissionReview)
class SubmissionReviewAdmin(admin.ModelAdmin):
    change_list_template = 'admin/developer_portal/submissionreview/change_list.html'
    list_display = ('submission', 'reviewer', 'action', 'created_at')
    list_filter = ('action', 'created_at')
    readonly_fields = ('submission', 'reviewer', 'action', 'comment', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DeveloperLicenseRequest)
class DeveloperLicenseRequestAdmin(admin.ModelAdmin):
    change_list_template = 'admin/developer_portal/developerlicenserequest/change_list.html'
    list_display = (
        'developer_name', 'license_type_display', 'is_free', 'status_badge',
        'license_key_display', 'created_at',
    )
    list_filter = ('status', 'license_type', 'is_free', 'created_at')
    search_fields = ('developer__display_name', 'developer__user__email', 'license_key')
    readonly_fields = (
        'id', 'is_free', 'order', 'license_key', 'license_expires_at',
        'setup_token', 'setup_token_id', 'setup_token_expires_at',
        'reviewed_by', 'reviewed_at', 'created_at',
    )
    actions = ['approve_requests', 'reject_requests']

    fieldsets = (
        (None, {
            'fields': ('id', 'developer', 'license_type', 'is_free', 'status', 'reason'),
        }),
        (_('Admin'), {
            'fields': ('admin_notes', 'reviewed_by', 'reviewed_at'),
        }),
        (_('License'), {
            'fields': ('order', 'license_key', 'license_expires_at', 'setup_token', 'setup_token_id', 'setup_token_expires_at'),
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
        }),
    )

    def developer_name(self, obj):
        return obj.developer.display_name
    developer_name.short_description = _('Developer')

    def license_type_display(self, obj):
        return obj.get_license_type_display()
    license_type_display.short_description = _('License Type')

    def status_badge(self, obj):
        css_map = {
            'pending': 'dev-admin-badge-pending',
            'approved': 'dev-admin-badge-approved',
            'rejected': 'dev-admin-badge-rejected',
        }
        css_class = css_map.get(obj.status, 'dev-admin-badge-suspended')
        return format_html(
            '<span class="dev-admin-badge {}">{}</span>',
            css_class, obj.get_status_display(),
        )
    status_badge.short_description = _('Status')

    def license_key_display(self, obj):
        if obj.license_key:
            return format_html(
                '<code class="dev-admin-license-key">{}</code>',
                obj.license_key,
            )
        return '-'
    license_key_display.short_description = _('License Key')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        stats = DeveloperLicenseRequest.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            approved=Count('id', filter=Q(status='approved')),
            rejected=Count('id', filter=Q(status='rejected')),
        )
        extra_context['stats'] = stats
        return super().changelist_view(request, extra_context)

    @admin.action(description=_('Approve selected license requests'))
    def approve_requests(self, request, queryset):
        from .services.license_provisioning import provision_dev_license
        approved = 0
        for req in queryset.filter(status=DeveloperLicenseRequest.Status.PENDING):
            req.reviewed_by = request.user
            # Auto-provision via update server
            try:
                provision_dev_license(req)
                DeveloperEmailService.send_license_approved(req)
                approved += 1
            except Exception as e:
                logger.error(f"Failed to provision license for {req.developer}: {e}")
                messages.warning(
                    request,
                    _('Could not provision license for %(dev)s: %(err)s') % {
                        'dev': req.developer.display_name,
                        'err': str(e),
                    }
                )
        if approved:
            messages.success(
                request,
                _('%(count)d license request(s) approved and provisioned.') % {'count': approved},
            )

    @admin.action(description=_('Reject selected license requests'))
    def reject_requests(self, request, queryset):
        rejected = 0
        for req in queryset.filter(status=DeveloperLicenseRequest.Status.PENDING):
            req.status = DeveloperLicenseRequest.Status.REJECTED
            req.reviewed_by = request.user
            req.reviewed_at = timezone.now()
            req.save(update_fields=[
                'status', 'reviewed_by', 'reviewed_at',
            ])
            DeveloperEmailService.send_license_rejected(req)
            rejected += 1
        messages.success(
            request,
            _('%(count)d license request(s) rejected.') % {'count': rejected},
        )


# ============================================
# Read-Only Mirror Model Admin
# ============================================

class ReadOnlyModelAdmin(admin.ModelAdmin):
    """Base class for read-only admin views of synced mirror data."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ComponentAnalytics)
class ComponentAnalyticsAdmin(ReadOnlyModelAdmin):
    list_display = (
        'component_name', 'developer', 'component_type',
        'downloads_total', 'downloads_period', 'average_rating',
        'rating_count', 'last_synced_at',
    )
    list_filter = ('component_type', 'pricing_model', 'is_published')
    search_fields = ('component_name', 'component_slug', 'developer__display_name')


@admin.register(ComponentReviewMirror)
class ComponentReviewMirrorAdmin(ReadOnlyModelAdmin):
    list_display = (
        'component_name', 'developer', 'author_name',
        'rating', 'is_verified_purchase', 'response_synced',
        'review_created_at',
    )
    list_filter = ('rating', 'is_verified_purchase', 'response_synced', 'is_read')
    search_fields = ('component_name', 'author_name', 'developer__display_name')


@admin.register(ComponentVersionMirror)
class ComponentVersionMirrorAdmin(ReadOnlyModelAdmin):
    list_display = (
        'component_slug', 'version', 'channel', 'developer',
        'breaking_changes', 'security_update', 'published_at',
    )
    list_filter = ('channel', 'breaking_changes', 'security_update')
    search_fields = ('component_slug', 'version', 'developer__display_name')
