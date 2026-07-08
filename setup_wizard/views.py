import logging

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.utils import timezone
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect

from .models import SetupProgress
from .forms import (
    SiteInfoForm, ContactInfoForm, BusinessAddressForm,
    CurrencyLocaleForm, PaymentMethodsInfoForm, EcommerceSettingsForm,
    EmailSettingsForm, SEOSettingsForm, SocialMediaForm,
    ContactLocationForm,
)
from core.models import SiteSettings

logger = logging.getLogger(__name__)

# Maps each step key to the SiteSettings fields it updates
STEP_FIELD_MAPPING = {
    'site_info': ['site_name', 'site_url', 'site_description'],
    'contact_info': ['admin_email', 'support_email', 'phone_number'],
    'contact_location': [
        'admin_email', 'support_email', 'phone_number',
        'address_line_1', 'address_line_2', 'city',
        'state_province', 'postal_code', 'country',
    ],
    'business_address': [
        'address_line_1', 'address_line_2', 'city',
        'state_province', 'postal_code', 'country',
    ],
    'currency_locale': ['default_currency', 'default_language', 'default_timezone'],
    'ecommerce_settings': [
        'allow_guest_checkout', 'require_phone_for_checkout',
        'enable_inventory_tracking', 'auto_approve_reviews',
        'error_reporting_enabled',
    ],
    'email_settings': [
        'enable_order_confirmation_emails',
        'enable_shipping_notification_emails',
        'enable_low_stock_alerts', 'low_stock_threshold',
    ],
    'seo_settings': ['meta_title', 'meta_description', 'meta_keywords'],
    'social_media': ['facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url'],
}

# Form field names that differ from the model field names
FORM_TO_MODEL_FIELD_MAP = {
    'enable_error_reporting': 'error_reporting_enabled',
}

# Wizard groups for the modal wizard (5 groups instead of 9 steps)
WIZARD_GROUPS = [
    {
        'key': 'store',
        'title': _('Your Store'),
        'description': _('Set up your store identity'),
        'icon': 'fas fa-store',
        'required': True,
        'step_key': 'site_info',
        'form_class': SiteInfoForm,
        'progress_fields': ['site_info_completed'],
        'template': 'setup_wizard/partials/steps/store.html',
    },
    {
        'key': 'contact',
        'title': _('Contact & Location'),
        'description': _('Your contact details and business address'),
        'icon': 'fas fa-envelope',
        'required': True,
        'step_key': 'contact_location',
        'form_class': ContactLocationForm,
        'progress_fields': ['contact_info_completed', 'business_address_completed'],
        'template': 'setup_wizard/partials/steps/contact.html',
    },
    {
        'key': 'locale',
        'title': _('Currency & Locale'),
        'description': _('Set your currency, language, and timezone'),
        'icon': 'fas fa-coins',
        'required': True,
        'step_key': 'currency_locale',
        'form_class': CurrencyLocaleForm,
        'progress_fields': ['currency_locale_completed'],
        'template': 'setup_wizard/partials/steps/locale.html',
    },
    {
        'key': 'payments',
        'title': _('Payments'),
        'description': _('Configure how you accept payments'),
        'icon': 'fas fa-credit-card',
        'required': True,
        'step_key': 'payment_methods',
        'form_class': PaymentMethodsInfoForm,
        'progress_fields': ['payment_methods_configured'],
        'template': 'setup_wizard/partials/steps/payments.html',
    },
    {
        'key': 'finetune',
        'title': _('Fine-Tune'),
        'description': _('Optional settings to customize your store'),
        'icon': 'fas fa-sliders-h',
        'required': False,
        'step_key': 'finetune',
        'form_class': None,
        'progress_fields': [
            'ecommerce_settings_completed', 'email_settings_completed',
            'seo_settings_completed', 'social_media_completed',
        ],
        'template': 'setup_wizard/partials/steps/finetune.html',
    },
]


def get_wizard_groups(progress):
    """Return wizard groups with their completion status."""
    groups = []
    for group in WIZARD_GROUPS:
        completed = all(
            getattr(progress, field, False)
            for field in group['progress_fields']
        )
        groups.append({
            'key': group['key'],
            'title': str(group['title']),
            'description': str(group['description']),
            'icon': group['icon'],
            'required': group['required'],
            'completed': completed,
        })
    return groups


def _get_group_config(group_key):
    """Get group configuration by key."""
    for group in WIZARD_GROUPS:
        if group['key'] == group_key:
            return group
    return None


class SetupWizardView:
    """
    Multi-step setup wizard for first-time store configuration.
    """

    # Define the wizard steps and their forms (kept for backward compatibility)
    STEPS = [
        {
            'key': 'site_info',
            'title': _('Site Information'),
            'description': _('Configure your store details'),
            'form_class': SiteInfoForm,
            'icon': 'fas fa-store',
            'required': True,
            'progress_field': 'site_info_completed'
        },
        {
            'key': 'contact_info',
            'title': _('Contact Information'),
            'description': _('Set up contact details'),
            'form_class': ContactInfoForm,
            'icon': 'fas fa-envelope',
            'required': True,
            'progress_field': 'contact_info_completed'
        },
        {
            'key': 'currency_locale',
            'title': _('Currency & Locale'),
            'description': _('Configure currency, language, and timezone'),
            'form_class': CurrencyLocaleForm,
            'icon': 'fas fa-coins',
            'required': True,
            'progress_field': 'currency_locale_completed'
        },
        {
            'key': 'payment_methods',
            'title': _('Payment Providers'),
            'description': _('Review payment provider setup'),
            'form_class': PaymentMethodsInfoForm,
            'icon': 'fas fa-credit-card',
            'required': True,
            'progress_field': 'payment_methods_configured'
        },
        {
            'key': 'business_address',
            'title': _('Business Address'),
            'description': _('Add your business location'),
            'form_class': BusinessAddressForm,
            'icon': 'fas fa-map-marker-alt',
            'required': False,
            'progress_field': 'business_address_completed'
        },
        {
            'key': 'ecommerce_settings',
            'title': _('E-commerce Settings'),
            'description': _('Configure store preferences'),
            'form_class': EcommerceSettingsForm,
            'icon': 'fas fa-cog',
            'required': False,
            'progress_field': 'ecommerce_settings_completed'
        },
        {
            'key': 'email_settings',
            'title': _('Email Notifications'),
            'description': _('Set up email preferences'),
            'form_class': EmailSettingsForm,
            'icon': 'fas fa-bell',
            'required': False,
            'progress_field': 'email_settings_completed'
        },
        {
            'key': 'seo_settings',
            'title': _('SEO Settings'),
            'description': _('Configure SEO defaults'),
            'form_class': SEOSettingsForm,
            'icon': 'fas fa-search',
            'required': False,
            'progress_field': 'seo_settings_completed'
        },
        {
            'key': 'social_media',
            'title': _('Social Media'),
            'description': _('Add social media links'),
            'form_class': SocialMediaForm,
            'icon': 'fas fa-share-alt',
            'required': False,
            'progress_field': 'social_media_completed'
        },
    ]

    @classmethod
    def get_step_by_key(cls, step_key):
        """Get step configuration by key"""
        for step in cls.STEPS:
            if step['key'] == step_key:
                return step
        return None

    @classmethod
    def get_step_index(cls, step_key):
        """Get step index by key"""
        for i, step in enumerate(cls.STEPS):
            if step['key'] == step_key:
                return i
        return 0

    @classmethod
    def get_next_step_key(cls, current_step_key):
        """Get the next step key"""
        current_index = cls.get_step_index(current_step_key)
        if current_index < len(cls.STEPS) - 1:
            return cls.STEPS[current_index + 1]['key']
        return None

    @classmethod
    def get_previous_step_key(cls, current_step_key):
        """Get the previous step key"""
        current_index = cls.get_step_index(current_step_key)
        if current_index > 0:
            return cls.STEPS[current_index - 1]['key']
        return None


# ---------------------------------------------------------------------------
# Legacy standalone views (redirect to dashboard with ?setup=open)
# ---------------------------------------------------------------------------

@staff_member_required
def wizard_start(request):
    """Redirect to dashboard with setup modal open."""
    return redirect(reverse('admin:management_shop_dashboard') + '?setup=open')


@staff_member_required
def wizard_step(request, step_key):
    """Redirect to dashboard with setup modal open."""
    return redirect(reverse('admin:management_shop_dashboard') + '?setup=open')


@staff_member_required
def wizard_complete(request):
    """Redirect to dashboard."""
    return redirect(reverse('admin:management_shop_dashboard'))


@staff_member_required
def wizard_skip(request):
    """Skip the setup wizard."""
    if request.method == 'POST':
        progress = SetupProgress.get_progress()
        progress.skip_wizard(request.user)
        messages.warning(
            request,
            _("Setup wizard skipped. You can complete setup anytime from the dashboard.")
        )
    return redirect('admin:index')


# ---------------------------------------------------------------------------
# AJAX API views for the modal wizard
# ---------------------------------------------------------------------------

@staff_member_required
@require_http_methods(["GET"])
def api_step_content(request, group_key):
    """Return rendered form HTML for a wizard group."""
    group = _get_group_config(group_key)
    if not group:
        return JsonResponse({'error': 'Invalid step'}, status=400)

    site_settings = SiteSettings.get_settings()
    progress = SetupProgress.get_progress()

    context = {
        'group': group,
        'progress': progress,
    }

    if group_key == 'store':
        initial = {
            'site_name': site_settings.site_name,
            'site_url': site_settings.site_url,
            'site_description': site_settings.site_description,
        }
        context['form'] = SiteInfoForm(initial=initial)
        context['is_hosted'] = settings.IS_HOSTED

    elif group_key == 'contact':
        initial = {
            'admin_email': site_settings.admin_email,
            'support_email': site_settings.support_email,
            'phone_number': site_settings.phone_number,
            'address_line_1': site_settings.address_line_1,
            'address_line_2': site_settings.address_line_2,
            'city': site_settings.city,
            'state_province': site_settings.state_province,
            'postal_code': site_settings.postal_code,
            'country': site_settings.country,
        }
        context['form'] = ContactLocationForm(initial=initial)

    elif group_key == 'locale':
        initial = {
            'default_currency': site_settings.default_currency,
            'default_language': site_settings.default_language,
            'default_timezone': site_settings.default_timezone,
        }
        context['form'] = CurrencyLocaleForm(initial=initial)
        # Show server time for timezone comparison
        server_tz = site_settings.default_timezone or 'UTC'
        try:
            import zoneinfo
            server_now = timezone.now().astimezone(zoneinfo.ZoneInfo(server_tz))
            context['server_time'] = server_now.strftime('%H:%M:%S') + f' ({server_tz})'
        except Exception:
            context['server_time'] = timezone.now().strftime('%H:%M:%S') + ' (UTC)'

    elif group_key == 'payments':
        context['form'] = PaymentMethodsInfoForm()
        # Show configured payment providers
        try:
            from payment_providers.models import PaymentProviderAccount
            providers = PaymentProviderAccount.objects.select_related('component').filter(
                is_active=True
            ).order_by('-is_default', 'display_name')
            context['configured_providers'] = providers
            context['provider_count'] = providers.count()
        except Exception:
            context['configured_providers'] = []
            context['provider_count'] = 0

    elif group_key == 'finetune':
        context['ecommerce_form'] = EcommerceSettingsForm(initial={
            'allow_guest_checkout': site_settings.allow_guest_checkout,
            'require_phone_for_checkout': site_settings.require_phone_for_checkout,
            'enable_inventory_tracking': site_settings.enable_inventory_tracking,
            'auto_approve_reviews': site_settings.auto_approve_reviews,
            'enable_error_reporting': site_settings.error_reporting_enabled,
        })
        context['email_form'] = EmailSettingsForm(initial={
            'enable_order_confirmation_emails': site_settings.enable_order_confirmation_emails,
            'enable_shipping_notification_emails': site_settings.enable_shipping_notification_emails,
            'enable_low_stock_alerts': site_settings.enable_low_stock_alerts,
            'low_stock_threshold': site_settings.low_stock_threshold,
        })
        context['seo_form'] = SEOSettingsForm(initial={
            'meta_title': site_settings.meta_title,
            'meta_description': site_settings.meta_description,
            'meta_keywords': site_settings.meta_keywords,
        })
        context['social_form'] = SocialMediaForm(initial={
            'facebook_url': site_settings.facebook_url,
            'twitter_url': site_settings.twitter_url,
            'instagram_url': site_settings.instagram_url,
            'linkedin_url': site_settings.linkedin_url,
        })

    html = render_to_string(group['template'], context, request=request)
    return JsonResponse({'html': html})


@staff_member_required
@csrf_protect
@require_http_methods(["POST"])
def api_step_save(request, group_key):
    """Save form data for a wizard group via AJAX."""
    group = _get_group_config(group_key)
    if not group:
        return JsonResponse({'success': False, 'errors': {'__all__': ['Invalid step']}}, status=400)

    progress = SetupProgress.get_progress()

    # Payment step: just mark as acknowledged
    if group_key == 'payments':
        progress.mark_step_completed('payment_methods_configured', request.user)
        return JsonResponse({
            'success': True,
            'progress': _get_progress_data(progress),
        })

    # Fine-tune step: process multiple sub-forms
    if group_key == 'finetune':
        return _save_finetune_step(request, progress)

    # Regular steps: validate form and save
    form_class = group['form_class']
    form = form_class(request.POST, request.FILES)

    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)

    step_key = group['step_key']
    success = process_step_data(step_key, form.cleaned_data, request.user)

    if not success:
        return JsonResponse({
            'success': False,
            'errors': {'__all__': [str(_('Error saving settings. Please try again.'))]},
        }, status=500)

    # Mark progress fields as completed
    for field in group['progress_fields']:
        progress.mark_step_completed(field, request.user)

    return JsonResponse({
        'success': True,
        'progress': _get_progress_data(progress),
    })


def _save_finetune_step(request, progress):
    """Handle the fine-tune step which has multiple sub-forms."""
    all_errors = {}

    # Process each sub-form
    sub_steps = [
        ('ecommerce_settings', EcommerceSettingsForm, 'ecommerce_settings_completed'),
        ('email_settings', EmailSettingsForm, 'email_settings_completed'),
        ('seo_settings', SEOSettingsForm, 'seo_settings_completed'),
        ('social_media', SocialMediaForm, 'social_media_completed'),
    ]

    for step_key, form_class, progress_field in sub_steps:
        form = form_class(request.POST)
        if form.is_valid():
            process_step_data(step_key, form.cleaned_data, request.user)
            progress.mark_step_completed(progress_field, request.user)
        else:
            all_errors.update(form.errors)

    if all_errors:
        return JsonResponse({
            'success': False,
            'errors': all_errors,
        }, status=400)

    return JsonResponse({
        'success': True,
        'progress': _get_progress_data(progress),
    })


def _get_progress_data(progress):
    """Return serializable progress data."""
    progress.refresh_from_db()
    return {
        'completion_percentage': progress.get_completion_percentage(),
        'essential_completion_percentage': progress.get_essential_completion_percentage(),
        'is_essential_complete': progress.is_essential_setup_complete(),
        'is_complete': progress.is_setup_complete(),
        'groups': get_wizard_groups(progress),
    }


# ---------------------------------------------------------------------------
# Data persistence (uses QuerySet.update to bypass SiteSettings.full_clean)
# ---------------------------------------------------------------------------

def get_step_initial_data(step_key, site_settings):
    """Get initial data for form pre-population."""
    if step_key == 'site_info':
        return {
            'site_name': site_settings.site_name,
            'site_url': site_settings.site_url,
            'site_description': site_settings.site_description,
        }
    elif step_key == 'contact_info':
        return {
            'admin_email': site_settings.admin_email,
            'support_email': site_settings.support_email,
            'phone_number': site_settings.phone_number,
        }
    elif step_key == 'business_address':
        return {
            'address_line_1': site_settings.address_line_1,
            'address_line_2': site_settings.address_line_2,
            'city': site_settings.city,
            'state_province': site_settings.state_province,
            'postal_code': site_settings.postal_code,
            'country': site_settings.country,
        }
    elif step_key == 'currency_locale':
        return {
            'default_currency': site_settings.default_currency,
            'default_language': site_settings.default_language,
            'default_timezone': site_settings.default_timezone,
        }
    elif step_key == 'ecommerce_settings':
        return {
            'allow_guest_checkout': site_settings.allow_guest_checkout,
            'require_phone_for_checkout': site_settings.require_phone_for_checkout,
            'enable_inventory_tracking': site_settings.enable_inventory_tracking,
            'auto_approve_reviews': site_settings.auto_approve_reviews,
            'enable_error_reporting': site_settings.error_reporting_enabled,
        }
    elif step_key == 'email_settings':
        return {
            'enable_order_confirmation_emails': site_settings.enable_order_confirmation_emails,
            'enable_shipping_notification_emails': site_settings.enable_shipping_notification_emails,
            'enable_low_stock_alerts': site_settings.enable_low_stock_alerts,
            'low_stock_threshold': site_settings.low_stock_threshold,
        }
    elif step_key == 'seo_settings':
        return {
            'meta_title': site_settings.meta_title,
            'meta_description': site_settings.meta_description,
            'meta_keywords': site_settings.meta_keywords,
        }
    elif step_key == 'social_media':
        return {
            'facebook_url': site_settings.facebook_url,
            'twitter_url': site_settings.twitter_url,
            'instagram_url': site_settings.instagram_url,
            'linkedin_url': site_settings.linkedin_url,
        }
    return {}


def process_step_data(step_key, cleaned_data, user):
    """
    Save step data using QuerySet.update() to bypass SiteSettings.full_clean().

    This avoids validation errors when saving partial data (e.g., saving site
    info before admin_email has been set).
    """
    try:
        fields = STEP_FIELD_MAPPING.get(step_key)
        if fields is None and step_key == 'payment_methods':
            return True

        if fields is None:
            logger.error("Unknown step key: %s", step_key)
            return False

        update_kwargs = {}
        for field in fields:
            form_field = field
            # Check if the model field name maps from a different form field name
            for form_name, model_name in FORM_TO_MODEL_FIELD_MAP.items():
                if model_name == field and form_name in cleaned_data:
                    form_field = form_name
                    break
            if form_field in cleaned_data:
                update_kwargs[field] = cleaned_data[form_field]

        if update_kwargs:
            SiteSettings.objects.filter(pk=1).update(**update_kwargs)

        # Handle special cases
        if step_key == 'site_info' and cleaned_data.get('favicon'):
            _handle_favicon_upload(cleaned_data['favicon'])

        if step_key in ('business_address', 'contact_location'):
            # Only create inventory structure if address fields are provided
            if cleaned_data.get('country'):
                site_settings = SiteSettings.get_settings()
                create_default_inventory_structure(cleaned_data, site_settings)

        # Update built-in email account with merchant's email
        if step_key == 'contact_location':
            admin_email = cleaned_data.get('admin_email')
            if admin_email:
                try:
                    from email_system.models import EmailAccount
                    builtin_account = EmailAccount.objects.filter(
                        provider_key='builtin_smtp',
                        component__isnull=True,
                    ).first()
                    if builtin_account:
                        builtin_account.from_email = admin_email
                        builtin_account.reply_to = admin_email
                        update_fields = ['from_email', 'reply_to']
                        # Update from_name if site_name is available
                        site_name = SiteSettings.objects.values_list(
                            'site_name', flat=True
                        ).get(pk=1)
                        if site_name:
                            builtin_account.from_name = site_name
                            update_fields.append('from_name')
                        builtin_account.save(update_fields=update_fields)
                except Exception as e:
                    logger.error("Error updating built-in email account: %s", e)

        return True

    except Exception as e:
        logger.error("Error processing step %s: %s", step_key, e)
        return False


def _handle_favicon_upload(favicon_file):
    """Upload favicon and link it to SiteSettings."""
    try:
        from media_library.models import MediaAsset
        site_settings = SiteSettings.get_settings()
        media_asset = MediaAsset.objects.create(
            title=f"Favicon - {site_settings.site_name or 'Site'}",
            original_file=favicon_file,
            alt_text="Site favicon",
            asset_type='image',
        )
        SiteSettings.objects.filter(pk=1).update(favicon=media_asset)
        # Mark favicon_uploaded flag
        progress = SetupProgress.get_progress()
        progress.favicon_uploaded = True
        progress.save()
    except Exception as e:
        logger.error("Error uploading favicon: %s", e)


def create_default_inventory_structure(cleaned_data, site_settings):
    """
    Create default SalesRegion and Warehouse for new installation.

    This sets up the minimum required multi-location inventory structure
    based on the merchant's business address and currency settings.
    """
    try:
        from catalog.models import SalesRegion, Warehouse

        currency = site_settings.default_currency or 'USD'
        country = cleaned_data.get('country', '')

        if not country:
            return

        region, created = SalesRegion.objects.get_or_create(
            code='DEFAULT',
            defaults={
                'name': _('Default Region'),
                'countries': [country],
                'default_currency': currency,
                'is_active': True,
                'priority': 100
            }
        )

        if not created:
            if country not in region.countries:
                region.countries.append(country)
                region.save()

        warehouse_code = 'MAIN-WH'
        if not Warehouse.objects.filter(code=warehouse_code).exists():
            Warehouse.objects.create(
                name=_('Main Warehouse'),
                code=warehouse_code,
                region=region,
                address_line1=cleaned_data.get('address_line_1', ''),
                address_line2=cleaned_data.get('address_line_2', ''),
                city=cleaned_data.get('city', ''),
                state_province=cleaned_data.get('state_province', ''),
                postal_code=cleaned_data.get('postal_code', ''),
                country=country,
                is_active=True,
                fulfillment_priority=100,
                stock_buffer_percentage=10,
                contact_email=site_settings.admin_email or '',
                contact_phone=site_settings.phone_number or '',
            )

    except ImportError:
        pass
    except Exception as e:
        logger.error("Error creating default inventory structure: %s", e)


# ---------------------------------------------------------------------------
# Progress API
# ---------------------------------------------------------------------------

@staff_member_required
@require_http_methods(["GET"])
def progress_api(request):
    """API endpoint for getting setup progress."""
    progress = SetupProgress.get_progress()
    return JsonResponse(_get_progress_data(progress))
