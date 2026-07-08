"""
Email action executors for form builder.
Handles email notifications to merchants and auto-reply emails to submitters.
"""
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone

from .base import BaseAction

logger = logging.getLogger(__name__)


class EmailNotificationAction(BaseAction):
    """
    Send email notification to merchant/staff when a form is submitted.

    Config schema:
    {
        "to_emails": ["admin@store.com"],
        "subject_template": "New submission: {{form_title}}",
        "include_data": true
    }
    """

    def execute(self):
        to_emails = self.config.get('to_emails', [])
        if not to_emails:
            logger.warning(
                "EmailNotificationAction: No recipients configured for action %s",
                self.action.pk
            )
            return {'status': 'skipped', 'reason': 'No recipients configured'}

        from email_system.services.email_sender import EmailSendingService

        context = self.get_form_data_context()

        # Build submission_data list for the template
        submission_data = []
        if self.config.get('include_data', True):
            for field in self.form_response.form.fields.all().order_by('step__order', 'order'):
                if field.field_type in ('heading', 'paragraph', 'divider', 'hidden'):
                    continue
                value = self.form_response.data.get(field.field_name, '')
                if value:
                    submission_data.append({
                        'label': field.translated_label,
                        'value': value,
                    })

        # Build admin URL
        try:
            site = Site.objects.get_current()
            site_url = f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
        except Exception:
            site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')

        template_context = {
            'form_name': context.get('form_title') or context.get('form_name', ''),
            'submitter_name': context.get('submitter_name', 'Anonymous'),
            'submitter_email': context.get('submitter_email', ''),
            'submission_date': timezone.now().strftime('%B %d, %Y at %I:%M %p'),
            'submission_id': f"FORM-{self.form_response.pk}",
            'submission_data': submission_data,
            'admin_submission_url': f"{site_url}/en/admin/form_builder/formresponse/{self.form_response.pk}/change/",
            'reply_to_email': context.get('submitter_email', ''),
        }

        results = []
        for to_email in to_emails:
            try:
                EmailSendingService.send_template_email(
                    to_email=to_email,
                    template_type='form_submission_admin_notification',
                    context=template_context,
                    enable_tracking=False,
                )
                results.append(to_email)
            except Exception as e:
                logger.error(
                    "EmailNotificationAction: Failed to send to %s for response %s: %s",
                    to_email, self.form_response.pk, e
                )

        if results:
            logger.info(
                "EmailNotificationAction: Queued for %s for response %s",
                results, self.form_response.pk
            )
            return {'status': 'sent', 'recipients': results}
        return {'status': 'error', 'error': 'All recipients failed'}


class AutoReplyAction(BaseAction):
    """
    Send auto-reply email to the form submitter.

    Config schema:
    {
        "email_field": "email",
        "subject": "Thank you for your submission",
        "body_template": "Dear {{submitter_name}}, thank you..."
    }
    """

    def execute(self):
        email_field = self.config.get('email_field', 'email')
        context = self.get_form_data_context()

        # Get submitter's email from form data
        to_email = self.form_response.data.get(email_field, '')
        if not to_email:
            # Fallback to authenticated user email
            if self.form_response.user:
                to_email = self.form_response.user.email
            else:
                logger.warning(
                    "AutoReplyAction: No email found for response %s (field: %s)",
                    self.form_response.pk, email_field
                )
                return {'status': 'skipped', 'reason': 'No submitter email found'}

        from email_system.services.email_sender import EmailSendingService

        # Map form action config to template variables
        subject = self.render_template_string(
            self.config.get('subject', 'Thank you for your submission'),
            context
        )
        body_message = self.render_template_string(
            self.config.get('body_template', ''),
            context
        )

        template_context = {
            'submitter_name': context.get('submitter_name', ''),
            'auto_response_subject': subject,
            'auto_response_heading': subject,
            'auto_response_message': body_message,
            'submission_id': f"FORM-{self.form_response.pk}",
        }

        try:
            EmailSendingService.send_template_email(
                to_email=to_email,
                template_type='form_submission_auto_response',
                context=template_context,
                enable_tracking=False,
            )

            logger.info(
                "AutoReplyAction: Queued for %s for response %s",
                to_email, self.form_response.pk
            )
            return {'status': 'sent', 'recipient': to_email}
        except Exception as e:
            logger.error(
                "AutoReplyAction: Failed for response %s: %s",
                self.form_response.pk, e
            )
            return {'status': 'error', 'error': str(e)}
