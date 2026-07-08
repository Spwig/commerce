"""
Template Preview Views
Handles preview and testing of email templates
"""

import json
import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.translation import gettext as _
from django.utils.encoding import force_str

from email_system.models import EmailTemplate, EmailTemplateTranslation
from email_system.services.template_renderer import TemplateRenderer
from email_system.services.sample_data import SampleDataProvider
from email_system.services.email_sender import EmailSendingService
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
def template_preview(request, template_id):
    """
    Preview email template with sample data

    Shows HTML and plain text versions side-by-side with language selection
    """
    base_template = get_object_or_404(EmailTemplate, id=template_id)
    language = request.GET.get('language', request.LANGUAGE_CODE)

    # Get sample data
    sample_data = SampleDataProvider.get_sample_data(
        base_template.template_type,
        language=language,
        request=request
    )

    # Get the template to render (base or translation)
    template = base_template
    if language != base_template.language_code:
        # Look for translation
        translation = EmailTemplateTranslation.objects.filter(
            template=base_template,
            language_code=language
        ).first()

        if translation:
            # Create temporary template object with translated content
            template = EmailTemplate(
                id=base_template.id,
                site=base_template.site,
                template_type=base_template.template_type,
                subject=translation.subject,
                html_content=translation.html_content,
                text_content=translation.text_content,
                is_system=base_template.is_system,
                is_active=True,
                language_code=language
            )

    # Render template directly
    from django.template import Template, Context
    from mjml.mjml2html import mjml_to_html
    from email_system.services.theme_integration import ThemeIntegrationService

    error = None
    subject = None
    html_body = None
    plain_text_body = None

    try:
        # Render subject
        subject_template = Template(template.subject)
        subject = subject_template.render(Context(sample_data))

        # Get theme CSS and context
        theme_service = ThemeIntegrationService()
        theme_css = theme_service.generate_theme_css()

        # Add theme context for template variables (bracket notation for hyphenated keys)
        theme_context = theme_service.get_email_context()
        sample_data['theme'] = theme_context

        # Inject theme CSS into MJML
        mjml_content = template.html_content
        if '<mj-head>' in mjml_content:
            mjml_content = mjml_content.replace(
                '</mj-head>',
                f'  <mj-style>\n{theme_css}\n  </mj-style>\n</mj-head>'
            )
        else:
            mj_head = f'''  <mj-head>
    <mj-style>
{theme_css}
    </mj-style>
  </mj-head>
'''
            mjml_content = mjml_content.replace('<mjml>', f'<mjml>\n{mj_head}')

        # Apply variables
        mjml_template = Template(mjml_content)
        mjml_rendered = mjml_template.render(Context(sample_data))

        # Convert MJML to HTML
        result = mjml_to_html(mjml_rendered)
        if result.get('errors'):
            error_messages = [f"{err.get('line')}:{err.get('message')}" for err in result['errors']]
            raise ValueError(f"MJML validation errors: {'; '.join(error_messages)}")
        html_body = result['html']

        # Inject mandatory Spwig branding footer
        html_body = _inject_spwig_footer(html_body, sample_data)

        # Render plain text
        if template.text_content:
            plain_template = Template(template.text_content)
            plain_text_body = plain_template.render(Context(sample_data))
        else:
            plain_text_body = "This email requires HTML support to view properly."

    except Exception as e:
        logger.error(f"Template preview error: {e}", exc_info=True)
        error = str(e)

    # Get base language (template's admin language - the template being viewed)
    base_language = base_template.language_code

    # Determine template language name for display
    admin_lang_names = {
        'en': _('English'),
        'es': _('Spanish'),
        'fr': _('French'),
        'de': _('German'),
        'ja': _('Japanese'),
        'pt': _('Portuguese'),
        'zh-hans': _('Chinese (Simplified)'),
    }
    base_language_name = force_str(admin_lang_names.get(base_language, base_language.upper()))

    # Get enabled site languages from Translation Service (merchant's storefront languages)
    enabled_site_languages = SiteLanguage.objects.filter(
        is_active=True
    ).order_by('order', 'name')

    # Build language list with translation status
    languages = []

    # Add base language first (the admin template language)
    languages.append({
        'code': base_language,
        'name': f"{base_language_name} ({force_str(_('Base'))})",
        'is_base': True,
        'has_translation': True,
    })

    # Add enabled site languages with translation status
    for site_lang in enabled_site_languages:
        if site_lang.code != base_language:
            # Check if translation exists for this site language
            has_translation = EmailTemplateTranslation.objects.filter(
                template=template,
                language_code=site_lang.code
            ).exists()

            languages.append({
                'code': site_lang.code,
                'name': force_str(site_lang.native_name or site_lang.name),
                'is_base': False,
                'has_translation': has_translation,
            })

    # Check if currently viewing a translation (not the base template)
    viewing_translation = (language != base_language)
    translation_exists = False
    if viewing_translation:
        translation_exists = EmailTemplateTranslation.objects.filter(
            template=base_template,
            language_code=language
        ).exists()

    # Get available variables for this template type
    available_variables = SampleDataProvider.get_available_variables(base_template.template_type)

    context = {
        'template': base_template,
        'language': language,
        'base_language': base_language,
        'base_language_name': base_language_name,
        'subject': subject,
        'html_body': html_body,
        'plain_text_body': plain_text_body,
        'sample_data': sample_data,
        'error': error,
        'languages': languages,
        'available_variables': available_variables,
        'viewing_translation': viewing_translation,
        'translation_exists': translation_exists,
    }

    return render(request, 'admin/email_system/template_preview.html', context)


@staff_member_required
def template_preview_html(request, template_id):
    """
    Render HTML-only preview (for iframe)

    Returns raw HTML for displaying in preview iframe
    Note: Removes X-Frame-Options to allow display in an iframe
    """
    base_template = get_object_or_404(EmailTemplate, id=template_id)
    language = request.GET.get('language', request.LANGUAGE_CODE)

    # Get the template to render (base or translation)
    template = base_template
    if language != base_template.language_code:
        # Look for translation
        translation = EmailTemplateTranslation.objects.filter(
            template=base_template,
            language_code=language
        ).first()

        if translation:
            # Create temporary template object with translated content
            template = EmailTemplate(
                id=base_template.id,
                site=base_template.site,
                template_type=base_template.template_type,
                subject=translation.subject,
                html_content=translation.html_content,
                text_content=translation.text_content,
                is_system=base_template.is_system,
                is_active=True,
                language_code=language
            )

    # Get sample data
    sample_data = SampleDataProvider.get_sample_data(
        template.template_type,
        language=language,
        request=request
    )

    # Render template directly
    from django.template import Template, Context
    from mjml.mjml2html import mjml_to_html
    from email_system.services.theme_integration import ThemeIntegrationService

    try:
        # Get theme CSS and context
        theme_service = ThemeIntegrationService()
        theme_css = theme_service.generate_theme_css()

        # Add theme context for template variables (bracket notation for hyphenated keys)
        theme_context = theme_service.get_email_context()
        sample_data['theme'] = theme_context

        # Inject theme CSS into MJML
        mjml_content = template.html_content
        if '<mj-head>' in mjml_content:
            mjml_content = mjml_content.replace(
                '</mj-head>',
                f'  <mj-style>\n{theme_css}\n  </mj-style>\n</mj-head>'
            )
        else:
            mj_head = f'''  <mj-head>
    <mj-style>
{theme_css}
    </mj-style>
  </mj-head>
'''
            mjml_content = mjml_content.replace('<mjml>', f'<mjml>\n{mj_head}')

        # Apply variables
        mjml_template = Template(mjml_content)
        mjml_rendered = mjml_template.render(Context(sample_data))

        # Convert MJML to HTML
        result = mjml_to_html(mjml_rendered)
        if result.get('errors'):
            error_messages = [f"{err.get('line')}:{err.get('message')}" for err in result['errors']]
            raise ValueError(f"MJML validation errors: {'; '.join(error_messages)}")
        html_body = result['html']

        # Inject mandatory Spwig branding footer
        html_body = _inject_spwig_footer(html_body, sample_data)

        response = HttpResponse(html_body, content_type='text/html')
        # Remove X-Frame-Options to allow iframe display
        response.xframe_options_exempt = True
        # Override CSP frame-ancestors to allow same-origin iframe embedding
        response._csp_replace = {"frame-ancestors": ["'self'"]}
        response._csp_replace_ro = {"frame-ancestors": ["'self'"]}
        return response

    except Exception as e:
        logger.error(f"Template HTML preview error: {e}", exc_info=True)
        response = HttpResponse(
            f'<div style="padding: 20px; color: red;">Error: {str(e)}</div>',
            content_type='text/html',
            status=500
        )
        response.xframe_options_exempt = True
        response._csp_replace = {"frame-ancestors": ["'self'"]}
        response._csp_replace_ro = {"frame-ancestors": ["'self'"]}
        return response


@staff_member_required
@require_http_methods(["POST"])
def send_test_email(request, template_id):
    """
    Send test email to specified address

    POST params:
        - email: Recipient email address
        - language: Language code (optional, default 'en')

    Returns JSON with success/error status
    """
    template = get_object_or_404(EmailTemplate, id=template_id)

    # Get parameters from JSON body (JS sends Content-Type: application/json)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        # Fall back to POST data for form submissions
        data = request.POST

    recipient_email = data.get('email')
    language = data.get('language', 'en')

    if not recipient_email:
        return JsonResponse({
            'success': False,
            'error': _('Email address is required')
        }, status=400)

    # Get sample data
    sample_data = SampleDataProvider.get_sample_data(
        template.template_type,
        language=language,
        request=request
    )

    try:
        # Send test email
        outbox = EmailSendingService.send_template_email(
            to_email=recipient_email,
            template_type=template.template_type,
            context=sample_data,
            language=language,
            enable_tracking=False
        )

        logger.info(
            f"Test email sent: template={template.template_type}, "
            f"to={recipient_email}, language={language}"
        )

        return JsonResponse({
            'success': True,
            'message': _('Test email sent successfully to %(email)s') % {'email': recipient_email},
            'outbox_id': str(outbox.id)
        })

    except Exception as e:
        logger.error(f"Test email send failed: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
def template_variables(request, template_id):
    """
    Get available variables for template

    Returns JSON with list of available template variables
    """
    template = get_object_or_404(EmailTemplate, id=template_id)

    variables = SampleDataProvider.get_available_variables(template.template_type)
    sample_data = SampleDataProvider.get_sample_data(template.template_type)

    # Format for display
    variable_list = []
    for var_name in variables:
        var_value = sample_data.get(var_name)
        # Convert complex types to string for display
        if isinstance(var_value, (list, dict)):
            var_value = str(var_value)[:100] + '...' if len(str(var_value)) > 100 else str(var_value)

        variable_list.append({
            'name': var_name,
            'value': var_value,
            'syntax': f'{{{{ {var_name} }}}}'
        })

    return JsonResponse({
        'template_type': template.template_type,
        'variables': variable_list
    })


@staff_member_required
@require_http_methods(["GET", "POST"])
def edit_translation(request, template_id, language_code):
    """
    Get or update email template translation

    GET: Returns translation data (or base template if no translation exists)
    POST: Creates or updates translation

    POST params:
        - subject: Translated subject line
        - html_content: Translated HTML/MJML content
        - text_content: Translated plain text content

    Returns JSON with success/error status
    """
    template = get_object_or_404(EmailTemplate, id=template_id)

    if request.method == 'GET':
        # Try to get existing translation
        try:
            translation = EmailTemplateTranslation.objects.get(
                template=template,
                language_code=language_code
            )

            return JsonResponse({
                'success': True,
                'translation': {
                    'subject': translation.subject,
                    'html_content': translation.html_content,
                    'text_content': translation.text_content,
                    'is_verified': translation.is_verified,
                    'exists': True
                },
                'base_template': {
                    'subject': template.subject,
                    'html_content': template.html_content,
                    'text_content': template.text_content,
                }
            })
        except EmailTemplateTranslation.DoesNotExist:
            # Return base template content for new translation
            return JsonResponse({
                'success': True,
                'translation': {
                    'subject': '',
                    'html_content': '',
                    'text_content': '',
                    'is_verified': False,
                    'exists': False
                },
                'base_template': {
                    'subject': template.subject,
                    'html_content': template.html_content,
                    'text_content': template.text_content,
                }
            })

    elif request.method == 'POST':
        # Get POST data
        subject = request.POST.get('subject', '').strip()
        html_content = request.POST.get('html_content', '').strip()
        text_content = request.POST.get('text_content', '').strip()

        # Validation
        if not subject:
            return JsonResponse({
                'success': False,
                'error': _('Subject line is required')
            }, status=400)

        if not html_content:
            return JsonResponse({
                'success': False,
                'error': _('HTML content is required')
            }, status=400)

        try:
            # Create or update translation
            translation, created = EmailTemplateTranslation.objects.update_or_create(
                template=template,
                language_code=language_code,
                defaults={
                    'subject': subject,
                    'html_content': html_content,
                    'text_content': text_content,
                    'is_verified': True,  # Manual edits are considered verified
                }
            )

            action = _('created') if created else _('updated')
            logger.info(
                f"Translation {action}: template={template.template_type}, "
                f"language={language_code}, user={request.user.username}"
            )

            return JsonResponse({
                'success': True,
                'message': _('Translation %(action)s successfully') % {'action': action},
                'translation_id': str(translation.id),
                'created': created
            })

        except Exception as e:
            logger.error(f"Translation save failed: {e}", exc_info=True)
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
