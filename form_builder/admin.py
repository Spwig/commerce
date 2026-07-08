"""
Form Builder Admin

Admin interface for creating and managing forms with:
- Card-based form list view
- Inline field editor
- Response viewing and export
"""
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count

from core.admin_mixins import TranslatableAdminMixin
from core.widgets import TranslatableFieldWidget
from .models import Form, FormStep, FormField, FormResponse


class FormAdminForm(forms.ModelForm):
    """Form with translatable field widgets for the Form model."""
    class Meta:
        model = Form
        fields = '__all__'
        widgets = {
            'title': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'description': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'rows': 3, 'class': 'vLargeTextField', 'style': 'width: 100%;'})
            ),
            'submit_button_text': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'success_message': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'rows': 3, 'class': 'vLargeTextField', 'style': 'width: 100%;'})
            ),
            'error_message': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'rows': 3, 'class': 'vLargeTextField', 'style': 'width: 100%;'})
            ),
        }


class FormFieldInline(admin.TabularInline):
    """Inline for managing form fields"""
    model = FormField
    extra = 1
    ordering = ['step__order', 'order']
    fields = [
        'field_name', 'field_type', 'label', 'is_required',
        'width', 'order', 'step'
    ]
    readonly_fields = []
    show_change_link = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('step')


class FormStepInline(admin.TabularInline):
    """Inline for managing form steps"""
    model = FormStep
    extra = 0
    ordering = ['order']
    fields = ['title', 'description', 'order', 'is_skippable']
    show_change_link = True


@admin.register(Form)
class FormAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """Admin for Form model with card-based list view"""

    form = FormAdminForm
    translatable_fields = ['title', 'description', 'submit_button_text', 'success_message', 'error_message']

    list_display = [
        'name', 'title', 'is_active', 'is_multi_step',
        'field_count_display', 'response_count_display', 'updated_at'
    ]
    list_filter = ['is_active', 'is_multi_step', 'spam_protection', 'created_at']
    search_fields = ['name', 'title', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']

    # Custom templates
    change_list_template = 'admin/form_builder/form/change_list.html'
    change_form_template = 'admin/form_builder/form/change_form.html'

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'title', 'description')
        }),
        (_('Submit Button & Messages'), {
            'fields': ('submit_button_text', 'success_message', 'error_message')
        }),
        (_('Settings'), {
            'fields': (
                'is_active', 'is_multi_step', 'require_login',
                'save_partial_responses'
            )
        }),
        (_('Spam Protection'), {
            'fields': ('spam_protection', 'recaptcha_site_key', 'recaptcha_secret_key'),
            'classes': ('collapse',)
        }),
        (_('Translations'), {
            'fields': ('translations',),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [FormStepInline, FormFieldInline]

    def get_queryset(self, request):
        """Annotate queryset with counts for efficiency"""
        return super().get_queryset(request).annotate(
            _field_count=Count('fields', distinct=True),
            _response_count=Count('responses', distinct=True)
        )

    def field_count_display(self, obj):
        """Display field count"""
        count = getattr(obj, '_field_count', obj.field_count)
        return format_html(
            '<span class="list-row-card-badge">'
            '<i class="fas fa-list"></i> {}'
            '</span>',
            count
        )
    field_count_display.short_description = _('Fields')
    field_count_display.admin_order_field = '_field_count'

    def response_count_display(self, obj):
        """Display response count with link to responses"""
        count = getattr(obj, '_response_count', obj.response_count)
        if count > 0:
            url = reverse('admin:form_builder_formresponse_changelist') + f'?form__id__exact={obj.pk}'
            return format_html(
                '<a href="{}" class="list-row-card-badge list-row-card-badge-success">'
                '<i class="fas fa-inbox"></i> {}'
                '</a>',
                url, count
            )
        return format_html(
            '<span class="list-row-card-badge">'
            '<i class="fas fa-inbox"></i> 0'
            '</span>'
        )
    response_count_display.short_description = _('Responses')
    response_count_display.admin_order_field = '_response_count'

    # ========================================================================
    # Soft-Delete Methods
    # ========================================================================

    def delete_model(self, request, obj):
        """Override delete_model to use soft delete"""
        obj.delete(user=request.user)

    def delete_queryset(self, request, queryset):
        """Override delete_queryset to use soft delete"""
        for obj in queryset:
            obj.delete(user=request.user)

    def changelist_view(self, request, extra_context=None):
        """Add extra context for the change list template"""
        extra_context = extra_context or {}

        # Get statistics
        queryset = self.get_queryset(request)
        extra_context['total_forms'] = queryset.count()
        extra_context['active_forms'] = queryset.filter(is_active=True).count()
        extra_context['total_responses'] = FormResponse.objects.filter(
            status='completed'
        ).count()
        extra_context['deleted_count'] = Form.all_objects.filter(
            is_deleted=True
        ).count()

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        js = TranslatableAdminMixin.Media.js + ('form_builder/js/admin_form_builder.js',)
        css = {
            'all': list(TranslatableAdminMixin.Media.css.get('all', [])) +
                   ['form_builder/css/admin_form_builder.css']
        }


@admin.register(FormStep)
class FormStepAdmin(admin.ModelAdmin):
    """Admin for FormStep model"""

    list_display = ['title', 'form', 'order', 'is_skippable']
    list_filter = ['form', 'is_skippable']
    search_fields = ['title', 'form__name']
    ordering = ['form', 'order']

    fieldsets = (
        (_('Step Information'), {
            'fields': ('form', 'title', 'description', 'order')
        }),
        (_('Navigation'), {
            'fields': ('is_skippable', 'next_button_text', 'back_button_text')
        }),
        (_('Translations'), {
            'fields': ('translations',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    """Admin for FormField model"""

    list_display = [
        'label', 'form', 'field_type', 'is_required', 'width', 'order'
    ]
    list_filter = ['form', 'field_type', 'is_required', 'width']
    search_fields = ['label', 'field_name', 'form__name']
    ordering = ['form', 'step__order', 'order']

    fieldsets = (
        (_('Field Identity'), {
            'fields': ('form', 'step', 'field_name', 'field_type')
        }),
        (_('Display'), {
            'fields': ('label', 'placeholder', 'help_text', 'default_value')
        }),
        (_('Validation'), {
            'fields': (
                'is_required', 'min_length', 'max_length',
                'min_value', 'max_value', 'validation_regex', 'validation_message'
            )
        }),
        (_('Options'), {
            'fields': ('options',),
            'classes': ('collapse',),
            'description': _('For select, radio, or checkbox group fields')
        }),
        (_('Rating Configuration'), {
            'fields': ('rating_config',),
            'classes': ('collapse',),
            'description': _('For star rating, Likert scale, or NPS fields')
        }),
        (_('File Upload Configuration'), {
            'fields': ('file_config',),
            'classes': ('collapse',),
            'description': _('Allowed file types, max size, max files')
        }),
        (_('Product Selector Configuration'), {
            'fields': ('product_config',),
            'classes': ('collapse',),
            'description': _('Category filters, max selections')
        }),
        (_('Layout'), {
            'fields': ('order', 'width', 'css_class')
        }),
        (_('Translations'), {
            'fields': ('translations',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    """Admin for FormResponse model with read-only viewing"""

    list_display = [
        'form', 'user_display', 'status', 'submitted_at',
        'ip_address', 'time_to_complete_display'
    ]
    list_filter = ['form', 'status', 'submitted_at']
    search_fields = ['form__name', 'user__email', 'ip_address']
    ordering = ['-submitted_at']
    readonly_fields = [
        'form', 'user', 'session_key', 'data', 'ip_address',
        'user_agent', 'referrer', 'language', 'current_step',
        'completed_steps', 'status', 'action_results',
        'started_at', 'submitted_at', 'completed_at', 'time_to_complete'
    ]

    change_list_template = 'admin/form_builder/formresponse/change_list.html'
    change_form_template = 'admin/form_builder/formresponse/change_form.html'

    fieldsets = (
        (_('Response Information'), {
            'fields': ('form', 'user', 'session_key', 'status')
        }),
        (_('Submitted Data'), {
            'fields': ('data',)
        }),
        (_('Metadata'), {
            'fields': ('ip_address', 'user_agent', 'referrer', 'language')
        }),
        (_('Progress'), {
            'fields': ('current_step', 'completed_steps'),
            'classes': ('collapse',)
        }),
        (_('Action Results'), {
            'fields': ('action_results',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': (
                'started_at', 'submitted_at', 'completed_at', 'time_to_complete'
            )
        }),
    )

    def has_add_permission(self, request):
        """Responses are created via form submission, not admin"""
        return False

    def has_change_permission(self, request, obj=None):
        """Responses should be read-only"""
        return False

    def user_display(self, obj):
        """Display user or anonymous indicator"""
        if obj.user:
            return obj.user.email
        return format_html(
            '<span class="quiet"><i class="fas fa-user-secret"></i> {}</span>',
            _('Anonymous')
        )
    user_display.short_description = _('Submitter')

    def time_to_complete_display(self, obj):
        """Display time to complete in human-readable format"""
        if obj.time_to_complete:
            minutes, seconds = divmod(obj.time_to_complete, 60)
            if minutes:
                return f'{minutes}m {seconds}s'
            return f'{seconds}s'
        return '-'
    time_to_complete_display.short_description = _('Time')

    def changelist_view(self, request, extra_context=None):
        """Add extra context for the change list template"""
        extra_context = extra_context or {}

        # Get statistics
        queryset = FormResponse.objects.all()
        extra_context['total_responses'] = queryset.count()
        extra_context['completed_responses'] = queryset.filter(
            status='completed'
        ).count()
        extra_context['draft_responses'] = queryset.filter(
            status='draft'
        ).count()

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ['form_builder/css/admin_form_builder.css']
        }
