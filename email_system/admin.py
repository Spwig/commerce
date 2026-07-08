from django.contrib import admin, messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from email_system.models import EmailAccount, EmailTemplate, EmailOutbox, EmailEvent, ScheduledEmail
from email_system.providers.registry import ProviderRegistry


@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    """Admin for email provider accounts"""

    # Use custom change_list template for modern card view
    change_list_template = 'email_system/admin/emailaccount_changelist.html'

    # Show all accounts on one page for client-side filtering
    list_per_page = 1000

    list_display = [
        'from_email',
        'component_name',
        'is_active_badge',
        'is_default_badge',
        'connection_status_badge',
        'last_tested_at',
        'created_at'
    ]
    list_filter = ['is_active', 'is_default', 'connection_status', 'created_at']
    search_fields = ['from_email', 'from_name', 'component__name', 'component__slug', 'provider_key']
    readonly_fields = [
        'credentials_display',
        'dkim_key_display',
        'connection_status',
        'connection_error',
        'last_tested_at',
        'created_at',
        'updated_at',
        'created_by'
    ]

    actions = ['regenerate_dkim_keys']

    class Media:
        css = {
            'all': (
                'email_system/css/email-admin-base.css',
                'email_system/css/admin_account_list.css',
            )
        }

    change_form_template = 'admin/email_system/emailaccount/change_form.html'

    fieldsets = (
        (_('Provider Information'), {
            'fields': ('site', 'component'),
            'classes': ('tab-provider',),
        }),
        (_('Sender Configuration'), {
            'fields': ('from_email', 'from_name', 'reply_to'),
            'classes': ('tab-sender',),
        }),
        (_('Configuration'), {
            'fields': ('is_active', 'is_default', 'settings'),
            'classes': ('tab-config',),
        }),
        (_('DKIM Configuration'), {
            'fields': ('dkim_key_display',),
            'description': _('DKIM keys are used to digitally sign outgoing emails. Use "Regenerate DKIM Keys" action to create new keys.'),
            'classes': ('tab-dkim',),
        }),
        (_('Credentials'), {
            'fields': ('credentials_display',),
            'description': _('Credentials are encrypted and managed through the provider setup. To update credentials, reconnect the provider.'),
            'classes': ('tab-credentials',),
        }),
        (_('Connection Status'), {
            'fields': ('connection_status', 'connection_error', 'last_tested_at'),
            'classes': ('tab-connection',),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('tab-timestamps',),
        }),
    )

    def component_name(self, obj):
        """Display component name"""
        if obj.component:
            return obj.component.name
        elif obj.provider_key == 'builtin_smtp':
            return _('Built-in SMTP Server')
        else:
            return _('Unknown Provider')
    component_name.short_description = _('Provider')

    def is_active_badge(self, obj):
        """Display active status badge"""
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
    is_active_badge.short_description = _('Status')

    def is_default_badge(self, obj):
        """Display default account badge"""
        if obj.is_default:
            return format_html(
                '<span class="status-badge primary">'
                '<i class="fas fa-star"></i> DEFAULT'
                '</span>'
            )
        return '-'
    is_default_badge.short_description = _('Default')

    def connection_status_badge(self, obj):
        """Display connection status with color coding"""
        css_class = {
            'pending': 'status-badge-pending',
            'connected': 'status-badge-success',
            'error': 'status-badge-error',
        }.get(obj.connection_status, 'status-badge-pending')
        return format_html(
            '<span class="email-admin-badge {}">{}</span>',
            css_class,
            obj.get_connection_status_display().upper()
        )
    connection_status_badge.short_description = _('Connection')

    def credentials_display(self, obj):
        """Display encrypted credentials info"""
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
            _('No credentials configured')
        )
    credentials_display.short_description = _('Credentials')

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the account list view"""
        extra_context = extra_context or {}

        # Get all email accounts
        from pathlib import Path
        from django.conf import settings
        from django.templatetags.static import static
        from django.db.models import Q
        from component_updates.integration_paths import INTEGRATIONS_DIR
        import json

        all_accounts = EmailAccount.objects.select_related('component').all()

        # Add logo URLs to each account
        for account in all_accounts:
            logo_url = ''

            # Handle built-in provider
            if account.provider_key == 'builtin_smtp' and not account.component:
                # Built-in provider logo from static files
                logo_path = Path(settings.BASE_DIR) / 'email_system' / 'static' / 'email_system' / 'providers' / 'builtin' / 'logo.svg'
                if logo_path.exists():
                    logo_url = static('email_system/providers/builtin/logo.svg')
            elif account.component:
                # External provider logo from components
                version = account.component.current_version or 'v1.0.0'
                if not version.startswith('v'):
                    version = f'v{version}'

                provider_dir = INTEGRATIONS_DIR / 'email_provider' / account.component.slug / version
                manifest_path = provider_dir / 'manifest.json'

                if manifest_path.exists():
                    with open(manifest_path) as f:
                        manifest = json.load(f)

                        # Get logo URL - handle both dict and string formats
                        logo_file = manifest.get('logo', {})
                        if isinstance(logo_file, dict):
                            logo_filename = logo_file.get('file', '')
                        else:
                            logo_filename = logo_file if logo_file else ''

                        if logo_filename:
                            logo_path = provider_dir / logo_filename
                            if logo_path.exists():
                                logo_url = static(f'email_provider/{account.component.slug}/current/{logo_filename}')

            account.logo_url = logo_url

        # Status counts
        extra_context['active_count'] = all_accounts.filter(is_active=True).count()
        extra_context['inactive_count'] = all_accounts.filter(is_active=False).count()

        # Connection status counts
        extra_context['connected_count'] = all_accounts.filter(connection_status='connected').count()
        extra_context['error_count'] = all_accounts.filter(connection_status='error').count()
        extra_context['pending_count'] = all_accounts.filter(connection_status='pending').count()

        # Default account
        try:
            extra_context['default_account'] = all_accounts.get(is_default=True)
        except EmailAccount.DoesNotExist:
            extra_context['default_account'] = None

        # Component counts (group by provider type)
        from django.db.models import Count, Q

        # Count external providers
        component_counts = all_accounts.filter(
            component__isnull=False
        ).values(
            'component__slug',
            'component__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')

        # Build component list with counts
        components_with_counts = []
        for item in component_counts:
            if item['component__slug']:
                components_with_counts.append({
                    'slug': item['component__slug'],
                    'name': item['component__name'],
                    'count': item['count']
                })

        # Add built-in provider count if any exist
        builtin_count = all_accounts.filter(
            provider_key='builtin_smtp',
            component__isnull=True
        ).count()

        if builtin_count > 0:
            components_with_counts.insert(0, {
                'slug': 'builtin_smtp',
                'name': _('Built-in SMTP Server'),
                'count': builtin_count
            })

        extra_context['component_counts'] = components_with_counts

        # Call parent to get the changelist
        response = super().changelist_view(request, extra_context=extra_context)

        # Add logo URLs to the result_list (the queryset shown in the template)
        if hasattr(response, 'context_data') and 'cl' in response.context_data:
            cl = response.context_data['cl']
            for account in cl.result_list:
                logo_url = ''

                # Handle built-in provider
                if account.provider_key == 'builtin_smtp' and not account.component:
                    # Built-in provider logo from static files
                    logo_path = Path(settings.BASE_DIR) / 'email_system' / 'static' / 'email_system' / 'providers' / 'builtin' / 'logo.svg'
                    if logo_path.exists():
                        logo_url = static('email_system/providers/builtin/logo.svg')
                elif account.component:
                    # External provider logo from components
                    version = account.component.current_version or 'v1.0.0'
                    if not version.startswith('v'):
                        version = f'v{version}'

                    provider_dir = INTEGRATIONS_DIR / 'email_provider' / account.component.slug / version
                    manifest_path = provider_dir / 'manifest.json'

                    if manifest_path.exists():
                        with open(manifest_path) as f:
                            manifest = json.load(f)

                            # Get logo URL - handle both dict and string formats
                            logo_file = manifest.get('logo', {})
                            if isinstance(logo_file, dict):
                                logo_filename = logo_file.get('file', '')
                            else:
                                logo_filename = logo_file if logo_file else ''

                            if logo_filename:
                                logo_path = provider_dir / logo_filename
                                if logo_path.exists():
                                    logo_url = static(f'email_provider/{account.component.slug}/current/{logo_filename}')

                account.logo_url = logo_url

        return response

    def get_queryset(self, request):
        """Filter queryset based on request parameters"""
        qs = super().get_queryset(request).select_related('component', 'site')

        # Connection status filter
        connection_status = request.GET.get('connection_status')
        if connection_status:
            qs = qs.filter(connection_status=connection_status)

        # Active status filter
        is_active = request.GET.get('is_active')
        if is_active:
            qs = qs.filter(is_active=(is_active == '1'))

        # Default filter
        is_default = request.GET.get('is_default')
        if is_default:
            qs = qs.filter(is_default=(is_default == '1'))

        # Component filter
        component = request.GET.get('component')
        if component:
            if component == 'builtin_smtp':
                # Filter for built-in provider
                qs = qs.filter(provider_key='builtin_smtp', component__isnull=True)
            else:
                # Filter for external component providers
                qs = qs.filter(component__slug=component)

        # Search query
        search = request.GET.get('q')
        if search:
            qs = qs.filter(
                Q(from_email__icontains=search) |
                Q(from_name__icontains=search) |
                Q(component__name__icontains=search) |
                Q(component__slug__icontains=search) |
                Q(provider_key__icontains=search)
            )

        return qs

    def dkim_key_display(self, obj):
        """Display DKIM keys and DNS record"""
        if obj.provider_key != 'builtin_smtp':
            return format_html(
                '<div class="messagelist"><li class="info">'
                '<i class="fas fa-info-circle"></i> {}'
                '</li></div>',
                _('DKIM keys are only managed for the built-in SMTP provider.')
            )

        try:
            creds = obj.get_credentials()
            dkim_public_key = creds.get('dkim_public_key')
            dkim_selector = creds.get('dkim_selector', 'mail')

            if not dkim_public_key:
                return format_html(
                    '<div class="messagelist"><li class="warning">'
                    '<i class="fas fa-exclamation-triangle"></i> <strong>{}</strong><br>'
                    '<span class="quiet">{}</span>'
                    '</li></div>',
                    _('No DKIM keys generated'),
                    _('Use "Regenerate DKIM Keys" action to generate keys.')
                )

            # Extract domain from from_email
            domain = obj.from_email.split('@')[1] if '@' in obj.from_email else 'example.com'

            # Generate DNS record
            from email_system.smtp_server.dkim_handler import DKIMHandler
            handler = DKIMHandler(domain=domain, selector=dkim_selector)
            dns_record = handler.get_dns_record(dkim_public_key)

            return format_html(
                '<div class="dkim-key-info">'
                '<div class="messagelist"><li class="success">'
                '<i class="fas fa-key"></i> <strong>{}</strong>'
                '</li></div>'
                '<div class="field-box dkim-dns-record-box">'
                '<p class="dkim-dns-heading"><strong>{}</strong></p>'
                '<p class="dkim-dns-field">'
                '<strong>{}</strong>: <code>{}</code>'
                '</p>'
                '<p class="dkim-dns-field dkim-dns-value">'
                '<strong>{}</strong>: <code class="dkim-dns-code">{}</code>'
                '</p>'
                '<p class="dkim-dns-actions">'
                '<button type="button" data-action="copy-to-clipboard" data-clipboard-text="{}" '
                'class="button dkim-copy-btn">'
                '<i class="fas fa-copy"></i> {}'
                '</button>'
                '</p>'
                '</div>'
                '</div>',
                _('DKIM keys configured'),
                _('DNS TXT Record:'),
                _('Name'),
                f'{dkim_selector}._domainkey.{domain}',
                _('Value'),
                dns_record,
                dns_record,
                _('Copy DNS Record')
            )
        except Exception as e:
            return format_html(
                '<div class="messagelist"><li class="error">'
                '<i class="fas fa-exclamation-circle"></i> <strong>{}</strong><br>'
                '<span class="quiet">{}</span>'
                '</li></div>',
                _('Error loading DKIM keys'),
                str(e)
            )
    dkim_key_display.short_description = _('DKIM Keys')

    def regenerate_dkim_keys(self, request, queryset):
        """Admin action to regenerate DKIM keys for selected accounts"""
        from email_system.smtp_server.dkim_handler import DKIMHandler

        regenerated_count = 0
        errors = []

        for account in queryset:
            if account.provider_key != 'builtin_smtp':
                errors.append(f'{account.name}: {_("Only built-in SMTP accounts can have DKIM keys regenerated")}')
                continue

            try:
                # Extract domain from from_email
                if '@' not in account.from_email:
                    errors.append(f'{account.name}: {_("Invalid from_email format")}')
                    continue

                domain = account.from_email.split('@')[1]
                creds = account.get_credentials()
                selector = creds.get('dkim_selector', 'mail')

                # Generate new keys
                handler = DKIMHandler(domain=domain, selector=selector)
                private_key, public_key = handler.generate_key_pair()

                # Store keys
                handler.store_keys(private_key, public_key, account)

                regenerated_count += 1

                self.message_user(
                    request,
                    _(f'✓ DKIM keys regenerated for {account.name}'),
                    messages.SUCCESS
                )

            except Exception as e:
                errors.append(f'{account.name}: {str(e)}')

        # Summary message
        if regenerated_count > 0:
            self.message_user(
                request,
                _(f'Successfully regenerated DKIM keys for {regenerated_count} account(s)'),
                messages.SUCCESS
            )

        if errors:
            for error in errors:
                self.message_user(request, error, messages.ERROR)

    regenerate_dkim_keys.short_description = _('Regenerate DKIM keys for selected accounts')


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    """Admin for email templates"""

    list_display = [
        'template_type',
        'language_code',
        'subject',
        'is_active_badge',
        'is_system_badge',
        'preview_button',
        'updated_at'
    ]
    list_filter = ['template_type', 'language_code', 'is_active', 'is_system']
    search_fields = ['subject', 'html_content', 'text_content']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'version', 'parent_template']

    actions = ['clone_template', 'activate_template', 'deactivate_template']

    fieldsets = (
        (_('Template Information'), {
            'fields': ('site', 'template_type', 'language_code')
        }),
        (_('Content'), {
            'fields': ('subject', 'html_content', 'text_content')
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_system')
        }),
        (_('Version Control'), {
            'fields': ('version', 'parent_template'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )

    def is_active_badge(self, obj):
        """Display active status badge"""
        if obj.is_active:
            return format_html(
                '<span class="email-admin-badge status-badge-success">ACTIVE</span>'
            )
        return format_html(
            '<span class="email-admin-badge status-badge-pending">INACTIVE</span>'
        )
    is_active_badge.short_description = _('Status')

    def is_system_badge(self, obj):
        """Display system template badge"""
        if obj.is_system:
            return format_html(
                '<span class="email-admin-badge status-badge-pending">SYSTEM</span>'
            )
        return '-'
    is_system_badge.short_description = _('Type')

    def preview_button(self, obj):
        """Display preview button"""
        url = reverse('email_system:template_preview', args=[obj.id])
        return format_html(
            '<a href="{}" class="button email-admin-preview-btn" target="_blank">'
            '<i class="fas fa-eye"></i> {}'
            '</a>',
            url,
            _('Preview')
        )
    preview_button.short_description = _('Actions')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        from django.conf import settings
        if not getattr(settings, 'SPWIG_IS_HQ', False):
            from email_system.models import EmailTemplate
            for prefix in EmailTemplate.HQ_ONLY_PREFIXES:
                qs = qs.exclude(template_type__startswith=prefix)
        return qs

    def clone_template(self, request, queryset):
        """Admin action to clone selected templates"""
        from django.contrib import messages

        cloned_count = 0
        errors = []

        for template in queryset:
            try:
                clone = template.clone(user=request.user, set_active=False)
                cloned_count += 1
                self.message_user(
                    request,
                    _(f'Successfully cloned template: {template.get_template_type_display()} ({template.language_code})'),
                    messages.SUCCESS
                )
            except Exception as e:
                errors.append(f'{template.get_template_type_display()}: {str(e)}')

        if cloned_count > 0:
            self.message_user(
                request,
                _(f'Successfully cloned {cloned_count} template(s)'),
                messages.SUCCESS
            )

        if errors:
            for error in errors:
                self.message_user(request, error, messages.ERROR)

    clone_template.short_description = _('Clone selected templates')

    def activate_template(self, request, queryset):
        """Admin action to activate selected templates"""
        from django.contrib import messages

        activated_count = 0
        errors = []

        for template in queryset:
            try:
                template.activate()
                activated_count += 1
            except Exception as e:
                errors.append(f'{template.get_template_type_display()}: {str(e)}')

        if activated_count > 0:
            self.message_user(
                request,
                _(f'Successfully activated {activated_count} template(s)'),
                messages.SUCCESS
            )

        if errors:
            for error in errors:
                self.message_user(request, error, messages.ERROR)

    activate_template.short_description = _('Activate selected templates')

    def deactivate_template(self, request, queryset):
        """Admin action to deactivate selected templates"""
        from django.contrib import messages

        deactivated_count = 0
        errors = []

        for template in queryset:
            try:
                template.deactivate()
                deactivated_count += 1
            except Exception as e:
                errors.append(f'{template.get_template_type_display()}: {str(e)}')

        if deactivated_count > 0:
            self.message_user(
                request,
                _(f'Successfully deactivated {deactivated_count} template(s)'),
                messages.SUCCESS
            )

        if errors:
            for error in errors:
                self.message_user(request, error, messages.ERROR)

    deactivate_template.short_description = _('Deactivate selected templates')


@admin.register(EmailOutbox)
class EmailOutboxAdmin(admin.ModelAdmin):
    """Admin for email outbox (queue and history)"""

    change_list_template = 'admin/email_system/emailoutbox/change_list.html'

    list_display = [
        'subject',
        'to_email',
        'from_email',
        'status_badge',
        'queued_at',
        'sent_at',
        'retry_count'
    ]
    list_filter = ['status', 'queued_at', 'sent_at', 'template_type']
    search_fields = ['subject', 'to_email', 'from_email', 'provider_message_id']
    readonly_fields = [
        'provider_message_id',
        'error_message',
        'created_at',
        'queued_at',
        'sent_at',
        'failed_at'
    ]
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('Email Details'), {
            'fields': ('site', 'account', 'to_email', 'from_email', 'from_name')
        }),
        (_('Content'), {
            'fields': ('subject', 'html_body', 'text_body', 'reply_to')
        }),
        (_('Additional Recipients'), {
            'fields': ('cc', 'bcc'),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('headers', 'tags', 'attachments', 'template_type'),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('status', 'provider_message_id', 'error_message', 'retry_count', 'max_retries')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'queued_at', 'sent_at', 'failed_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['release_held_emails_action']

    def status_badge(self, obj):
        """Display status with color coding"""
        css_class = {
            'queued': 'status-badge-info',
            'held': 'status-badge-warning',
            'logged': 'status-badge-pending',
            'sending': 'status-badge-warning',
            'sent': 'status-badge-success',
            'failed': 'status-badge-error',
            'bounced': 'status-badge-error',
            'skipped': 'status-badge-pending',
        }.get(obj.status, 'status-badge-pending')
        return format_html(
            '<span class="email-admin-badge {}">{}</span>',
            css_class,
            obj.get_status_display().upper()
        )
    status_badge.short_description = _('Status')

    def has_add_permission(self, request):
        """Outbox is read-only, emails are created programmatically."""
        return False

    def release_held_emails_action(self, request, queryset):
        """Release selected held emails for sending."""
        from django.utils import timezone
        updated = queryset.filter(status='held').update(
            status='queued', queued_at=timezone.now()
        )
        if updated:
            self.message_user(request, _('Released %d email(s) for delivery.') % updated, messages.SUCCESS)
        else:
            self.message_user(request, _('No held emails in selection.'), messages.WARNING)
    release_held_emails_action.short_description = _('Release held emails for delivery')

    def changelist_view(self, request, extra_context=None):
        """Add stats context for the custom change list template."""
        extra_context = extra_context or {}

        qs = EmailOutbox.objects.all()
        extra_context['total_emails'] = qs.count()
        extra_context['sent_count'] = qs.filter(status='sent').count()
        extra_context['failed_count'] = qs.filter(status='failed').count()
        extra_context['queued_count'] = qs.filter(status='queued').count()
        extra_context['held_count'] = qs.filter(status='held').count()
        extra_context['logged_count'] = qs.filter(status='logged').count()

        # Distinct template types for filter dropdown
        extra_context['template_types'] = list(
            qs.exclude(template_type='')
            .values_list('template_type', flat=True)
            .distinct()
            .order_by('template_type')
        )

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(EmailEvent)
class EmailEventAdmin(admin.ModelAdmin):
    """Admin for email delivery events"""

    list_display = [
        'email',
        'event_type_badge',
        'bounce_type',
        'occurred_at',
        'created_at'
    ]
    list_filter = ['event_type', 'bounce_type', 'occurred_at']
    search_fields = ['email__subject', 'email__to_email', 'bounce_reason']
    readonly_fields = [
        'email',
        'event_type',
        'event_data',
        'bounce_type',
        'bounce_reason',
        'user_agent',
        'ip_address',
        'created_at',
        'occurred_at'
    ]
    date_hierarchy = 'occurred_at'

    fieldsets = (
        (_('Event Information'), {
            'fields': ('email', 'event_type', 'occurred_at')
        }),
        (_('Event Data'), {
            'fields': ('event_data',),
            'classes': ('collapse',)
        }),
        (_('Bounce Details'), {
            'fields': ('bounce_type', 'bounce_reason'),
            'classes': ('collapse',)
        }),
        (_('Tracking'), {
            'fields': ('user_agent', 'ip_address'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def event_type_badge(self, obj):
        """Display event type with color coding"""
        css_class = {
            'delivered': 'status-badge-success',
            'bounced': 'status-badge-error',
            'opened': 'status-badge-info',
            'clicked': 'status-badge-info',
            'complained': 'status-badge-error',
            'unsubscribed': 'status-badge-warning',
        }.get(obj.event_type, 'status-badge-pending')
        return format_html(
            '<span class="email-admin-badge {}">{}</span>',
            css_class,
            obj.get_event_type_display().upper()
        )
    event_type_badge.short_description = _('Event Type')


@admin.register(ScheduledEmail)
class ScheduledEmailAdmin(admin.ModelAdmin):
    list_display = ('template_type', 'recipient_email', 'scheduled_for', 'status', 'sent_at')
    list_filter = ('status', 'template_type')
    search_fields = ('recipient_email', 'template_type')
    readonly_fields = ('created_at', 'sent_at', 'error_message')
    ordering = ('-scheduled_for',)
