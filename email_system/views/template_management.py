"""
Template Management Views
Custom admin interface for managing email templates
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q, Count
from django.http import JsonResponse

from email_system.models import EmailTemplate, EmailTemplateTranslation
from translations.models import SiteLanguage

logger = logging.getLogger(__name__)


def _inject_spwig_footer(html_body: str, context: dict = None) -> str:
    """
    Inject mandatory Spwig branding footer into email HTML.

    This footer is injected programmatically after MJML compilation so that
    merchants cannot remove it by editing templates.
    """
    shop_url = context.get('shop_url', '') if context else ''

    footer_html = f'''
    <!-- Spwig Branding Footer - Programmatically Injected -->
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:600px;margin:0 auto;">
      <tr>
        <td style="padding:15px 0 10px 0;text-align:center;">
          <hr style="border:none;border-top:1px solid #e5e7eb;margin:0 0 12px 0;" />
          <a href="https://spwig.com" style="color:#6b7280;text-decoration:none;font-size:11px;font-family:system-ui,-apple-system,BlinkMacSystemFont,sans-serif;" target="_blank">
            <img src="{shop_url}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align:middle;margin-right:4px;" />
            Powered by Spwig
          </a>
        </td>
      </tr>
    </table>
'''

    if '</body>' in html_body:
        return html_body.replace('</body>', f'{footer_html}</body>')
    else:
        return html_body + footer_html


@staff_member_required
def template_edit(request, template_id):
    """
    Edit template MJML, plain text, and subject with live preview

    Features:
    - Monaco code editor for MJML (syntax highlighting)
    - Plain text editor
    - Subject line editor
    - Live preview iframe
    - MJML validation on save
    - Version control
    """
    template = get_object_or_404(EmailTemplate, id=template_id)

    # Get merchant's current admin interface language
    admin_language = request.LANGUAGE_CODE

    # Try to get translation in admin's language
    translation = None
    content_to_edit = template
    is_editing_translation = False

    if admin_language != template.language_code:
        translation = EmailTemplateTranslation.objects.filter(
            template=template,
            language_code=admin_language
        ).first()

        if translation:
            # Create a temporary template object with translated content
            is_editing_translation = True
            content_to_edit = type('obj', (object,), {
                'id': template.id,
                'subject': translation.subject,
                'html_content': translation.html_content,
                'text_content': translation.text_content,
                'version': template.version,
                'template_type': template.template_type,
                'is_system': template.is_system,
                'language_code': admin_language,
            })()
        else:
            # No translation available - add info message
            messages.info(
                request,
                _('No translation available for %(language)s. Showing base template in %(base_lang)s.') % {
                    'language': admin_language.upper(),
                    'base_lang': template.language_code.upper()
                }
            )

    # Only allow editing custom templates
    if template.is_system and request.method == 'POST':
        messages.error(
            request,
            _('System templates cannot be edited. Clone this template to customize it.')
        )
        return redirect('email_system:clone_template', template.id)

    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        html_content = request.POST.get('html_content', '')
        text_content = request.POST.get('text_content', '')

        try:
            # Validate MJML before saving
            if html_content.strip():
                from mjml import mjml_to_html
                from io import StringIO
                try:
                    mjml_fp = StringIO(html_content)
                    mjml_to_html(mjml_fp)
                except Exception as mjml_error:
                    raise Exception(_('MJML validation failed: %(error)s') % {'error': str(mjml_error)})

            # Determine if we're editing a translation
            admin_language = request.LANGUAGE_CODE
            is_editing_translation = (
                admin_language != template.language_code and
                EmailTemplateTranslation.objects.filter(
                    template=template,
                    language_code=admin_language
                ).exists()
            )

            if is_editing_translation:
                # Update translation
                translation = EmailTemplateTranslation.objects.get(
                    template=template,
                    language_code=admin_language
                )
                translation.subject = subject
                translation.html_content = html_content
                translation.text_content = text_content
                translation.is_verified = True
                translation.save()

                messages.success(
                    request,
                    _('Translation saved successfully (%(language)s)') % {
                        'language': admin_language.upper()
                    }
                )

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': str(_('Translation saved successfully!')),
                        'version': template.version
                    })
            else:
                # Update base template
                template.subject = subject
                template.html_content = html_content
                template.text_content = text_content

                # Increment version
                template.version += 1
                template.save()

                messages.success(
                    request,
                    _('Template saved successfully! Version %(version)s') % {'version': template.version}
                )

                # Return JSON for AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': str(_('Template saved successfully!')),
                        'version': template.version
                    })

            return redirect('email_system:template_preview', template.id)

        except Exception as e:
            logger.error(f"Error saving template {template_id}: {e}", exc_info=True)
            error_msg = str(e)

            # Return JSON for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': error_msg
                }, status=400)

            messages.error(
                request,
                _('Error saving template: %(error)s') % {'error': error_msg}
            )

    # Get available variables for this template type
    from email_system.services.sample_data import SampleDataProvider
    available_variables = SampleDataProvider.get_available_variables(template.template_type)

    context = {
        'title': _('Edit Template: %(name)s') % {'name': template.get_template_type_display()},
        'template': content_to_edit,
        'available_variables': available_variables,
        'is_system': template.is_system,
        'editing_language': admin_language,
        'base_language': template.language_code,
        'is_translation': is_editing_translation,
    }

    return render(request, 'admin/email_system/template_edit.html', context)


@staff_member_required
def template_list(request):
    """
    List all email templates with filters and actions

    Modern card-based view following rules.md design patterns
    DEFAULT: Shows only templates in site's default language
    """
    from core.models import SiteSettings

    # Get site's default language
    site_settings = SiteSettings.get_settings()
    default_language = site_settings.default_language

    # Get filter parameters
    template_type = request.GET.get('type', '')
    status = request.GET.get('status', '')  # 'system', 'custom', 'active'
    search = request.GET.get('search', '')
    show_all_languages = request.GET.get('show_all_languages', '') == 'true'
    show_inactive = request.GET.get('show_inactive', '') == 'true'
    show_deleted = request.GET.get('show_deleted', '') == 'true'

    # Base query - show deleted if requested, otherwise only active (not deleted)
    if show_deleted:
        templates = EmailTemplate.all_objects.select_related('site', 'created_by').filter(is_deleted=True)
    else:
        templates = EmailTemplate.objects.select_related('site', 'created_by').all()

    # Apply filters
    if template_type:
        templates = templates.filter(template_type=template_type)

    # Language filtering: Default to site's default language
    if not show_all_languages:
        # Check if templates exist in default language
        if EmailTemplate.objects.filter(language_code=default_language).exists():
            templates = templates.filter(language_code=default_language)
        else:
            # Fallback to English if default language templates don't exist
            templates = templates.filter(language_code='en')

    # Active/Inactive filtering: Hide inactive by default
    if not show_inactive:
        templates = templates.filter(is_active=True)

    if status == 'system':
        templates = templates.filter(is_system=True)
    elif status == 'custom':
        templates = templates.filter(is_system=False)
    elif status == 'active':
        templates = templates.filter(is_active=True)

    if search:
        templates = templates.filter(
            Q(subject__icontains=search) |
            Q(template_type__icontains=search)
        )

    # Order by: active first, then system, then updated_at
    templates = templates.order_by('-is_active', '-is_system', '-updated_at')

    # Get statistics
    total_count = EmailTemplate.objects.count()
    system_count = EmailTemplate.objects.filter(is_system=True).count()
    custom_count = EmailTemplate.objects.filter(is_system=False).count()
    active_count = EmailTemplate.objects.filter(is_active=True).count()
    deleted_count = EmailTemplate.all_objects.filter(is_deleted=True).count()

    # Get available template types for filter
    template_types = EmailTemplate._meta.get_field('template_type').choices

    context = {
        'title': _('Email Templates'),
        'templates': templates,
        'template_types': template_types,
        'default_language': default_language,
        'show_all_languages': show_all_languages,
        'show_inactive': show_inactive,
        'show_deleted': show_deleted,
        'filters': {
            'type': template_type,
            'status': status,
            'search': search,
        },
        'statistics': {
            'total': total_count,
            'system': system_count,
            'custom': custom_count,
            'active': active_count,
            'deleted': deleted_count,
        },
    }

    return render(request, 'admin/email_system/template_list.html', context)


@staff_member_required
def clone_template(request, template_id):
    """
    Clone a template for customization

    Creates a copy of the template with is_system=False
    """
    template = get_object_or_404(EmailTemplate, id=template_id)

    if request.method == 'POST':
        try:
            # Get merchant's admin language
            admin_language = request.LANGUAGE_CODE

            # Clone template with language-specific translation
            cloned = template.clone(
                user=request.user,
                set_active=True,
                clone_language=admin_language
            )

            messages.success(
                request,
                _('Successfully cloned template "%(name)s" (%(language)s). You can now customize it.') % {
                    'name': template.get_template_type_display(),
                    'language': admin_language.upper()
                }
            )

            # Add fallback info message if translation didn't exist
            if admin_language != cloned.language_code:
                messages.info(
                    request,
                    _('Note: No translation was available for %(language)s. The clone uses the base template in %(base_lang)s.') % {
                        'language': admin_language.upper(),
                        'base_lang': cloned.language_code.upper()
                    }
                )

            return redirect('email_system:template_edit', cloned.id)

        except Exception as e:
            logger.error(f"Error cloning template {template_id}: {e}", exc_info=True)
            messages.error(
                request,
                _('Error cloning template: %(error)s') % {'error': str(e)}
            )

    return redirect('email_system:template_list')


def validate_template_deletion(template):
    """
    Validate if template can be safely deleted.

    Returns:
        tuple: (can_delete: bool, warnings: list, errors: list)
    """
    from email_system.models import EmailTemplate, EmailOutbox
    from datetime import timedelta
    from django.utils import timezone

    warnings = []
    errors = []

    # 1. System template check
    if template.is_system:
        errors.append({
            'code': 'SYSTEM_TEMPLATE',
            'message': _('System templates cannot be deleted. Clone this template to customize it.')
        })
        return (False, warnings, errors)

    # 2. Active template with no fallback check
    if template.is_active:
        other_active = EmailTemplate.objects.filter(
            site=template.site,
            template_type=template.template_type,
            language_code=template.language_code,
            is_active=True
        ).exclude(id=template.id).exists()

        if not other_active:
            # Check for system fallback
            system_fallback = EmailTemplate.objects.filter(
                site=template.site,
                template_type=template.template_type,
                language_code=template.language_code,
                is_system=True
            ).exists()

            if not system_fallback:
                errors.append({
                    'code': 'NO_FALLBACK',
                    'message': _(
                        'Cannot delete the only active template for "%(type)s" (%(lang)s). '
                        'Activate another template first, or deactivate this template instead of deleting it.'
                    ) % {
                        'type': template.get_template_type_display(),
                        'lang': template.get_language_code_display()
                    }
                })
            else:
                warnings.append({
                    'code': 'FALLBACK_TO_SYSTEM',
                    'message': _(
                        'Deleting this active template will cause emails to fall back to the system template.'
                    )
                })

    # 3. Pending/queued emails check
    pending_count = EmailOutbox.objects.filter(
        template_type=template.template_type,
        status__in=['pending', 'queued']
    ).count()

    if pending_count > 0:
        warnings.append({
            'code': 'PENDING_EMAILS',
            'message': _(
                'Warning: %(count)s email(s) are queued using this template type. '
                'They will use the fallback template when sent.'
            ) % {'count': pending_count}
        })

    # 4. Translation check
    translation_count = template.translations.count()
    if translation_count > 0:
        warnings.append({
            'code': 'HAS_TRANSLATIONS',
            'message': _(
                'This template has %(count)s translation(s) that will also be deleted.'
            ) % {'count': translation_count}
        })

    # 5. Recent usage check
    recent_usage = EmailOutbox.objects.filter(
        template_type=template.template_type,
        status='sent',
        sent_at__gte=timezone.now() - timedelta(days=30)
    ).count()

    if recent_usage > 0:
        warnings.append({
            'code': 'RECENT_USAGE',
            'message': _(
                'This template type was used to send %(count)s email(s) in the last 30 days.'
            ) % {'count': recent_usage}
        })

    can_delete = len(errors) == 0
    return (can_delete, warnings, errors)


@staff_member_required
def delete_template(request, template_id):
    """
    Delete a custom template with validation and warnings
    """
    template = get_object_or_404(EmailTemplate, id=template_id)

    # Validate deletion
    can_delete, warnings, errors = validate_template_deletion(template)

    # Show errors and block deletion
    if errors:
        for error in errors:
            messages.error(request, error['message'])
        return redirect('email_system:template_list')

    if request.method == 'POST':
        # Show warnings but allow deletion
        if warnings:
            for warning in warnings:
                messages.warning(request, warning['message'])

        template_name = template.get_template_type_display()
        template.delete(user=request.user)

        messages.success(
            request,
            _('Template "%(name)s" moved to recycle bin') % {'name': template_name}
        )
        return redirect('email_system:template_list')

    # GET request - show confirmation page with warnings
    context = {
        'template': template,
        'warnings': warnings,
        'can_delete': can_delete,
    }
    return render(request, 'admin/email_system/template_delete_confirm.html', context)


@staff_member_required
def restore_template(request, template_id):
    """
    Restore a deleted template from recycle bin
    """
    template = get_object_or_404(EmailTemplate.all_objects, id=template_id, is_deleted=True)

    if request.method == 'POST':
        template_name = template.get_template_type_display()
        template.restore()

        messages.success(
            request,
            _('Template "%(name)s" restored successfully') % {'name': template_name}
        )
        return redirect('email_system:template_list')

    # GET request - show confirmation page
    context = {
        'template': template,
    }
    return render(request, 'admin/email_system/template_restore_confirm.html', context)


@staff_member_required
def toggle_template_active(request, template_id):
    """
    Activate or deactivate a template

    When activating a template, it deactivates others of the same type
    """
    template = get_object_or_404(EmailTemplate, id=template_id)

    if request.method == 'POST':
        try:
            if template.is_active:
                template.deactivate()
                messages.success(
                    request,
                    _('Template "%(name)s" deactivated') % {
                        'name': template.get_template_type_display()
                    }
                )
            else:
                template.activate()
                messages.success(
                    request,
                    _('Template "%(name)s" activated') % {
                        'name': template.get_template_type_display()
                    }
                )
        except Exception as e:
            logger.error(f"Error toggling template {template_id}: {e}", exc_info=True)
            messages.error(
                request,
                _('Error updating template: %(error)s') % {'error': str(e)}
            )

    return redirect('email_system:template_list')


@staff_member_required
def translation_manager(request):
    """
    Translation management interface for email templates

    Shows translation coverage matrix and allows bulk translation
    Shows EmailTemplateTranslation records for merchant's storefront languages
    """
    from email_system.models import EmailTemplateTranslation
    from email_system.services.translation_service import EmailTemplateTranslationService
    from translations.models import SiteLanguage
    from core.models import SiteSettings

    # Get site's default language as base language for translations
    site_settings = SiteSettings.get_settings()
    base_lang = site_settings.default_language

    # Get all system templates in the site's default language
    # If templates don't exist in default language, fall back to English
    templates = EmailTemplate.objects.filter(
        is_system=True,
        language_code=base_lang
    ).order_by('template_type')

    if not templates.exists():
        templates = EmailTemplate.objects.filter(
            is_system=True,
            language_code='en'
        ).order_by('template_type')
        base_lang = 'en'

    # Get enabled languages from Translation Service (exclude base language)
    enabled_site_languages = SiteLanguage.objects.filter(
        is_active=True
    ).exclude(
        code=base_lang
    ).order_by('order', 'name')

    # Build supported languages list
    supported_languages = [(lang.code, lang.native_name) for lang in enabled_site_languages]

    # Build translation matrix
    translation_matrix = []
    total_needed = len(templates) * len(supported_languages)
    total_complete = 0

    # Get all pending/processing jobs for email templates
    from translations.models import TranslationJob

    pending_jobs = TranslationJob.objects.filter(
        content_type='email_template',
        status__in=['pending', 'processing']
    ).values_list('translated_data', 'target_languages', 'status')

    # Build a lookup dict: {template_id: {lang_code: status}}
    job_status_map = {}
    for translated_data, target_langs, status in pending_jobs:
        # Extract template_id from translated_data JSON field
        if translated_data and 'template_id' in translated_data:
            template_id = translated_data['template_id']
            if template_id not in job_status_map:
                job_status_map[template_id] = {}
            for lang in target_langs:
                job_status_map[template_id][lang] = status

    for template in templates:
        row = {
            'template': template,
            'languages': {},
            'has_translations': False
        }

        for lang_code, lang_name in supported_languages:
            translation = EmailTemplateTranslation.objects.filter(
                template=template,
                language_code=lang_code
            ).first()

            # Check if there's a pending/processing job for this template+language
            job_status = None
            if str(template.id) in job_status_map and lang_code in job_status_map[str(template.id)]:
                job_status = job_status_map[str(template.id)][lang_code]

            row['languages'][lang_code] = {
                'exists': translation is not None,
                'translation': translation,
                'verified': translation.is_verified if translation else False,
                'quality_score': translation.quality_score if translation else None,
                'outdated': translation.is_outdated() if translation else False,
                'job_status': job_status  # 'pending' or 'processing' or None
            }

            if translation:
                total_complete += 1
                row['has_translations'] = True

        translation_matrix.append(row)

    coverage_percentage = (total_complete / total_needed * 100) if total_needed > 0 else 0

    # Get base language display name
    try:
        base_site_language = SiteLanguage.objects.get(code=base_lang)
        base_language_name = base_site_language.native_name
    except SiteLanguage.DoesNotExist:
        base_language_name = base_lang.upper()

    context = {
        'title': _('Email Template Translations'),
        'translation_matrix': translation_matrix,
        'supported_languages': supported_languages,
        'base_language': base_lang,
        'base_language_name': base_language_name,
        'statistics': {
            'total_templates': len(templates),
            'total_languages': len(supported_languages),
            'total_needed': total_needed,
            'total_complete': total_complete,
            'total_missing': total_needed - total_complete,
            'coverage_percentage': coverage_percentage,
        },
    }

    return render(request, 'admin/email_system/translation_manager.html', context)


@staff_member_required
def translate_template(request, template_id):
    """
    Translate a template into multiple languages using AI
    Supports force_retranslate parameter to overwrite existing translations
    """
    template = get_object_or_404(EmailTemplate, id=template_id)

    if request.method == 'POST':
        from email_system.services.translation_service import EmailTemplateTranslationService

        # Get selected languages
        languages = request.POST.getlist('languages')
        force_retranslate = request.POST.get('force_retranslate') == 'true'

        if not languages:
            messages.error(request, _('Please select at least one language'))
            return redirect('email_system:translation_manager')

        try:
            service = EmailTemplateTranslationService()
            result = service.translate_template(
                template=template,
                target_languages=languages,
                user=request.user,
                force_retranslate=force_retranslate
            )

            if result['success']:
                messages.success(
                    request,
                    _('Translation jobs created for %(count)s language(s). Translations will be processed automatically.') % {
                        'count': len(result.get('jobs', []))
                    }
                )
            else:
                messages.error(
                    request,
                    _('Translation failed: %(message)s') % {'message': result.get('message', 'Unknown error')}
                )
        except Exception as e:
            logger.error(f"Translation error for template {template_id}: {e}", exc_info=True)
            messages.error(
                request,
                _('Error creating translation jobs: %(error)s') % {'error': str(e)}
            )

    return redirect('email_system:translation_manager')


@staff_member_required
def bulk_translate_all(request):
    """
    Create translation jobs for all templates in all missing languages
    """
    if request.method == 'POST':
        from email_system.services.translation_service import EmailTemplateTranslationService

        # Get all system templates
        templates = EmailTemplate.objects.filter(is_system=True, language_code='en')

        # All target languages
        target_languages = ['es', 'fr', 'de', 'ja', 'pt', 'zh-hans']

        total_jobs = 0
        errors = []

        service = EmailTemplateTranslationService()

        for template in templates:
            try:
                result = service.translate_template(
                    template=template,
                    target_languages=target_languages,
                    user=request.user
                )

                if result['success']:
                    total_jobs += len(result.get('jobs', []))
                else:
                    errors.append(f"{template.get_template_type_display()}: {result.get('message')}")
            except Exception as e:
                errors.append(f"{template.get_template_type_display()}: {str(e)}")

        if total_jobs > 0:
            messages.success(
                request,
                _('Created %(count)s translation jobs. Translations will be processed automatically.') % {
                    'count': total_jobs
                }
            )

        if errors:
            for error in errors[:5]:  # Show first 5 errors
                messages.warning(request, error)

    return redirect('email_system:translation_manager')


@staff_member_required
def preview_render(request):
    """
    Render MJML to HTML for live preview in editor

    POST data:
    - mjml_content: The MJML code to compile

    Returns:
    - JSON with html key containing compiled HTML
    """
    import json

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        mjml_content = data.get('mjml_content', '')

        if not mjml_content.strip():
            return JsonResponse({'html': '<div style="padding: 40px; text-align: center; color: #999;">No content to preview</div>'})

        try:
            from mjml import mjml_to_html
            from io import StringIO
            from django.template import Template, Context
            from email_system.services.sample_data import SampleDataProvider

            # First, render Django template variables with sample data
            try:
                # Get sample data for preview (use order_confirmation as default for variables)
                sample_data = SampleDataProvider.get_sample_data('order_confirmation', language='en', request=request)

                # Add theme context for template variables (bracket notation for hyphenated keys)
                from email_system.services.theme_integration import ThemeIntegrationService
                theme_service = ThemeIntegrationService()
                theme_context = theme_service.get_email_context()
                sample_data['theme'] = theme_context

                # Render Django template
                django_template = Template(mjml_content)
                rendered_mjml = django_template.render(Context(sample_data))
            except Exception as template_error:
                logger.warning(f"Django template rendering failed, using raw MJML: {template_error}")
                rendered_mjml = mjml_content

            # Compile MJML to HTML
            mjml_fp = StringIO(rendered_mjml)
            result = mjml_to_html(mjml_fp)

            # result is a DotMap with html and errors attributes
            html_content = result.html if hasattr(result, 'html') else str(result)

            if not html_content:
                return JsonResponse({
                    'html': '<div style="padding: 20px; color: red;">MJML compilation failed</div>',
                    'errors': result.errors if hasattr(result, 'errors') else []
                })

            # Inject mandatory Spwig branding footer
            html_content = _inject_spwig_footer(html_content, sample_data)

            return JsonResponse({
                'html': html_content,
                'errors': result.errors if hasattr(result, 'errors') else []
            })

        except ImportError:
            # MJML not installed, just return the raw content
            return JsonResponse({
                'html': f'<div style="padding: 20px; background: #fff3cd; color: #856404; border-radius: 4px;"><strong>MJML not installed.</strong><br>Preview shows raw MJML code. Install MJML: <code>pip install mjml</code></div><pre style="padding: 20px; background: #f8f9fa;">{mjml_content}</pre>'
            })
        except Exception as e:
            logger.error(f"MJML compilation error: {str(e)}")
            return JsonResponse({
                'html': f'<div style="padding: 20px; color: red;">MJML Error: {str(e)}</div>',
                'error': str(e)
            })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Preview render error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
