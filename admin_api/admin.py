from django.contrib import admin
from django.db.models import Case, When, IntegerField
from django.utils.html import format_html

from .models import CustomerMessage, MessageReadReceipt, StaffInvitation


@admin.register(CustomerMessage)
class CustomerMessageAdmin(admin.ModelAdmin):
    change_list_template = 'admin/admin_api/customermessage/change_list.html'
    change_form_template = 'admin/admin_api/customermessage/change_form.html'
    list_display = ['name', 'email', 'subject', 'message_type', 'status', 'created_at']
    list_filter = ['status', 'message_type', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['user', 'created_at', 'updated_at', 'ip_address', 'user_agent', 'read_at', 'read_by', 'replied_at', 'replied_by']
    list_per_page = 25

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unread_count'] = CustomerMessage.objects.filter(status='unread').count()
        extra_context['read_count'] = CustomerMessage.objects.filter(status='read').count()
        extra_context['replied_count'] = CustomerMessage.objects.filter(status='replied').count()
        extra_context['archived_count'] = CustomerMessage.objects.filter(status='archived').count()
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        try:
            message = CustomerMessage.objects.select_related(
                'order', 'read_by', 'replied_by'
            ).get(pk=object_id)
            # Auto-mark as read when opened
            if message.status == 'unread':
                message.mark_as_read(request.user)
            # Record per-user read receipt
            MessageReadReceipt.objects.get_or_create(
                source='contact_form',
                object_id=message.pk,
                user=request.user,
            )
            extra_context['can_reply'] = message.status not in ('replied', 'archived')
            extra_context['is_replied'] = message.status == 'replied'
        except CustomerMessage.DoesNotExist:
            pass
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'order', 'read_by', 'replied_by'
        ).order_by(
            Case(
                When(status='unread', then=0),
                When(status='read', then=1),
                When(status='replied', then=2),
                When(status='archived', then=3),
                default=4,
                output_field=IntegerField(),
            ),
            '-created_at'
        )


@admin.register(StaffInvitation)
class StaffInvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'invited_by', 'status_badge', 'created_at', 'expires_at']
    list_filter = ['is_accepted', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['token', 'invited_by', 'is_accepted', 'accepted_at', 'created_at']
    list_per_page = 25

    def status_badge(self, obj):
        if obj.is_accepted:
            return format_html('<span class="status-badge-success">Accepted</span>')
        elif obj.is_expired:
            return format_html('<span class="status-badge-error">Expired</span>')
        return format_html('<span class="status-badge-pending">Pending</span>')
    status_badge.short_description = 'Status'

    def has_add_permission(self, request):
        return False
