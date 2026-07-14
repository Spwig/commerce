"""
Template Renderer Service
Converts MJML templates to HTML with theme integration and variable substitution
"""

import logging

from django.template import Context, Template
from django.utils.translation import get_language
from mjml.mjml2html import mjml_to_html

logger = logging.getLogger(__name__)


class TemplateRenderer:
    """
    Renders email templates with theme integration and tracking
    """

    def __init__(self):
        from email_system.services.theme_integration import ThemeIntegrationService

        self.theme_service = ThemeIntegrationService()

    def render(
        self,
        template_type: str,
        context: dict,
        language: str | None = None,
        email_outbox_id: str | None = None,
        enable_tracking: bool = True,
    ) -> tuple[str, str, str]:
        """
        Render email template to HTML and plain text

        Args:
            template_type: Template type (e.g., 'order_confirmation')
            context: Template variables (e.g., {'customer_name': 'John', 'order_number': '12345'})
            language: Language code (defaults to current language)
            email_outbox_id: EmailOutbox UUID string for tracking (optional)
            enable_tracking: Enable open/click tracking (default: True)

        Returns:
            Tuple of (subject, html_body, plain_text_body)

        Raises:
            EmailTemplate.DoesNotExist: If template not found
            mjml.MJMLValidationError: If MJML syntax invalid
        """
        # Get language
        if not language:
            language = get_language() or "en"

        # Load template (with translation fallback)
        template = self._load_template(template_type, language)

        # Validate required variables
        self._validate_context(template, context)

        # Render subject
        subject = self._render_subject(template, context)

        # Get theme CSS variables (for CSS injection - legacy approach)
        theme_css = self.theme_service.generate_theme_css()

        # Inject theme CSS into MJML
        mjml_with_theme = self._inject_theme_css(template.html_content, theme_css)

        # Get theme context for template variables (new approach using TokenResolver)
        # This enables templates to use {{ theme.color.primary }}, {{ theme.font.family_body }}, etc.
        theme_context = self.theme_service.get_email_context()
        context["theme"] = theme_context

        # Add flat variables for backward compatibility with legacy MJML components
        # These support the old {{ theme_primary_color }} syntax
        if theme_context.get("color"):
            context["theme_primary_color"] = theme_context["color"].get("primary", "")
            context["theme_secondary_color"] = theme_context["color"].get("secondary", "")
            context["theme_text_color"] = theme_context["color"].get("text", "")
            context["theme_text_muted_color"] = theme_context["color"].get("text_muted", "")
            context["theme_background_color"] = theme_context["color"].get("background", "")
            context["theme_surface_color"] = theme_context["color"].get("surface", "")
            context["theme_border_color"] = theme_context["color"].get("border", "")
            context["theme_success_color"] = theme_context["color"].get("success", "")
            context["theme_warning_color"] = theme_context["color"].get("warning", "")
            context["theme_error_color"] = theme_context["color"].get("error", "")

        # Add site logo URLs for all size presets
        site_logo_context = self._get_site_logo_context(context.get("shop_url", ""))
        context.update(site_logo_context)

        # Add site settings (shop_name, support_email, etc.) - only if not already in context
        site_settings_context = self._get_site_settings_context(context.get("shop_url", ""))
        for key, value in site_settings_context.items():
            if key not in context or not context[key]:
                context[key] = value

        # Apply Django template variables to MJML
        mjml_rendered = self._apply_variables(mjml_with_theme, context)

        # Convert MJML to HTML
        html_body = self._mjml_to_html(mjml_rendered)

        # Inject mandatory Spwig branding footer (cannot be removed by merchants)
        html_body = self._inject_spwig_footer(html_body, context)

        # Add tracking if enabled
        if enable_tracking and email_outbox_id:
            from email_system.services.tracking_service import TrackingService

            tracking_service = TrackingService()
            html_body = tracking_service.add_tracking(html_body, email_outbox_id)

        # Render plain text
        plain_text_body = self._render_plain_text(template, context)

        logger.info(
            f"Rendered template '{template_type}' in language '{language}' "
            f"with tracking={'enabled' if enable_tracking else 'disabled'}"
        )

        return subject, html_body, plain_text_body

    def _load_template(self, template_type: str, language: str):
        """
        Load template with translation fallback

        Uses EmailTemplate.get_active_template() which handles priority:
        1. Active custom template for specific language
        2. Active system template for specific language
        3. Active system template for English
        4. First system template found
        """
        from email_system.models import EmailTemplate, EmailTemplateTranslation

        # Get active template (custom or system)
        template = EmailTemplate.get_active_template(
            template_type=template_type, language_code=language
        )

        # Check for translation if not in template's native language
        if language != template.language_code:
            try:
                translation = EmailTemplateTranslation.objects.filter(
                    template=template, language_code=language
                ).first()

                if translation:
                    # Create temporary template object with translated content
                    translated_template = EmailTemplate(
                        template_type=template_type,
                        subject=translation.subject,
                        html_content=translation.html_content,
                        text_content=translation.text_content,
                        is_system=template.is_system,
                        is_active=True,
                        language_code=language,
                    )
                    translated_template.id = template.id
                    translated_template.site = template.site
                    return translated_template
            except Exception as e:
                logger.debug(f"Could not load translation for {template_type}/{language}: {e}")

        return template

    # Required variables per template type (core templates used by signals)
    TEMPLATE_REQUIRED_VARS = {
        "order_confirmation": [
            "customer_name",
            "order_number",
            "order_date",
            "order_total",
            "order_url",
        ],
        "shipping_confirmation": ["customer_name", "order_number", "tracking_number"],
        "delivery_confirmation": ["customer_name", "order_number", "delivery_date"],
        "refund_notification": ["customer_name", "order_number", "refund_amount"],
        "admin_new_order": ["order_number", "customer_name", "order_total"],
        "order_cancelled": ["customer_name", "order_number"],
        "order_note_notification": ["customer_name", "order_number"],
        "payment_confirmation": ["customer_name", "order_number", "order_total"],
        "password_reset": ["reset_url"],
        "account_invitation": ["customer_name", "activation_url"],
        "account_welcome": ["customer_name"],
    }

    def _validate_context(self, template, context: dict) -> None:
        """
        Validate that all required variables are present in context.

        Logs warnings for missing variables but does not raise exceptions,
        since sending an email with a missing variable is better than
        failing to send the email entirely.
        """
        required = self.TEMPLATE_REQUIRED_VARS.get(template.template_type, [])
        missing = [var for var in required if var not in context or not context[var]]
        if missing:
            logger.warning(
                f"Template '{template.template_type}' missing required variables: "
                f"{', '.join(missing)}"
            )

    def _render_subject(self, template, context: dict) -> str:
        """
        Render subject line with Django template engine
        """
        subject_template = Template(template.subject)
        return subject_template.render(Context(context))

    def _inject_theme_css(self, mjml_content: str, theme_css: str) -> str:
        """
        Inject theme CSS into MJML <mj-head> section

        If <mj-head> exists, add <mj-style> inside it
        If not, create <mj-head> after <mjml> opening tag
        """
        if "<mj-head>" in mjml_content:
            # Insert before closing </mj-head>
            return mjml_content.replace(
                "</mj-head>", f"  <mj-style>\n{theme_css}\n  </mj-style>\n</mj-head>"
            )
        else:
            # Create <mj-head> section
            mj_head = f"""  <mj-head>
    <mj-style>
{theme_css}
    </mj-style>
  </mj-head>
"""
            return mjml_content.replace("<mjml>", f"<mjml>\n{mj_head}")

    def _apply_variables(self, mjml_content: str, context: dict) -> str:
        """
        Apply Django template variables to MJML content
        """
        template = Template(mjml_content)
        return template.render(Context(context))

    def _mjml_to_html(self, mjml_content: str) -> str:
        """
        Convert MJML to HTML using mjml Python library

        Raises:
            ValueError: If MJML syntax is invalid
        """
        try:
            result = mjml_to_html(mjml_content)

            if result.get("errors"):
                error_messages = [
                    f"{err.get('line')}:{err.get('message')}" for err in result["errors"]
                ]
                raise ValueError(f"MJML validation errors: {'; '.join(error_messages)}")

            return result["html"]

        except Exception as e:
            logger.error(f"MJML conversion failed: {e}")
            raise

    def _inject_spwig_footer(self, html_body: str, context: dict = None) -> str:
        """
        Inject mandatory Spwig branding footer into email HTML.

        This footer is injected programmatically after MJML compilation so that
        merchants cannot remove it by editing templates. This is essential for
        marketing as the platform is billed at a one-time fee.

        Args:
            html_body: The compiled HTML email body
            context: Template context containing shop_url

        Returns:
            HTML with Spwig branding footer injected before </body>
        """
        shop_url = context.get("shop_url", "") if context else ""

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

        # Insert before </body> if present, otherwise append
        if "</body>" in html_body:
            return html_body.replace("</body>", f"{footer_html}</body>")
        else:
            return html_body + footer_html

    def _render_plain_text(self, template, context: dict) -> str:
        """
        Render plain text version with Django template engine
        """
        if not template.text_content:
            logger.warning(
                f"No plain text template for '{template.template_type}', using placeholder"
            )
            return "This email requires HTML support to view properly."

        plain_template = Template(template.text_content)
        return plain_template.render(Context(context))

    def _get_site_logo_context(self, base_url: str = "") -> dict[str, str]:
        """
        Get site logo URLs for all size presets as absolute URLs.

        Args:
            base_url: Base URL for making relative URLs absolute (typically shop_url)

        Returns:
            Dict with site_logo_url and size variants:
            - site_logo_url: Email-optimized size (400x100)
            - site_logo_url_header: Header size (300x80)
            - site_logo_url_footer: Footer size (200x60)
            - site_logo_url_square: Square variant (160x160)

            All values are empty strings if no logo is configured.
        """
        try:
            from core.models import SiteSettings

            site_settings = SiteSettings.get_settings()

            def make_absolute(url: str) -> str:
                if not url:
                    return ""
                if url.startswith("http"):
                    return url
                if base_url:
                    return f"{base_url.rstrip('/')}{url}"
                return url

            return {
                "site_logo_url": make_absolute(site_settings.get_site_logo_url("email") or ""),
                "site_logo_url_header": make_absolute(
                    site_settings.get_site_logo_url("header") or ""
                ),
                "site_logo_url_footer": make_absolute(
                    site_settings.get_site_logo_url("footer") or ""
                ),
                "site_logo_url_square": make_absolute(
                    site_settings.get_site_logo_url("square") or ""
                ),
            }
        except Exception as e:
            logger.warning(f"Could not load site logo for email: {e}")
            return {
                "site_logo_url": "",
                "site_logo_url_header": "",
                "site_logo_url_footer": "",
                "site_logo_url_square": "",
            }

    def _get_site_settings_context(self, base_url: str = "") -> dict[str, str]:
        """
        Get site configuration variables from SiteSettings.

        Args:
            base_url: Base URL for shop_url if not configured in settings

        Returns:
            Dict with site settings:
            - shop_name: Store name
            - shop_url: Store URL
            - support_email: Support email (falls back to admin_email)
            - support_phone: Phone number
            - current_year: Current year for copyright notices
        """
        from django.utils import timezone

        try:
            from core.models import SiteSettings

            site_settings = SiteSettings.get_settings()

            return {
                "shop_name": site_settings.site_name or "",
                "shop_url": base_url or site_settings.site_url or "",
                "support_email": site_settings.get_support_email() or "",
                "support_phone": site_settings.phone_number or "",
                "current_year": timezone.now().year,
            }
        except Exception as e:
            logger.warning(f"Could not load site settings for email: {e}")
            from django.utils import timezone

            return {
                "shop_name": "",
                "shop_url": base_url,
                "support_email": "",
                "support_phone": "",
                "current_year": timezone.now().year,
            }


class TemplateRendererException(Exception):
    """Base exception for template rendering errors"""

    pass


class TemplateNotFoundException(TemplateRendererException):
    """Template not found for given type and language"""

    pass


class TemplateValidationException(TemplateRendererException):
    """Template validation failed (invalid MJML or missing variables)"""

    pass
