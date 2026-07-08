"""
Developer Portal Email Service
Sends transactional emails for developer portal events.
"""

import logging

from django.conf import settings
from django.contrib.sites.models import Site

logger = logging.getLogger(__name__)


class DeveloperEmailService:
    """
    Centralized email sending for all developer portal notifications.
    Each method builds the appropriate context and sends via EmailSendingService.
    """

    @staticmethod
    def _get_site_url():
        """Get the site URL for building links."""
        try:
            site = Site.objects.get_current()
            return f"https://{site.domain}" if not settings.DEBUG else f"http://{site.domain}"
        except Exception:
            return getattr(settings, 'SITE_URL', 'http://localhost:8000')

    @staticmethod
    def _get_support_email():
        """Get the support email address."""
        return getattr(settings, 'DEFAULT_SUPPORT_EMAIL', 'developers@spwig.com')

    @staticmethod
    def _send(to_email, template_type, context):
        """Send an email using the template system."""
        try:
            from email_system.services.email_sender import EmailSendingService
            outbox = EmailSendingService.send_template_email(
                to_email=to_email,
                template_type=template_type,
                context=context,
                language='en',
            )
            if outbox and outbox.status == 'queued':
                EmailSendingService.send_email(str(outbox.id))
                logger.info(
                    "Sent %s email to %s", template_type, to_email
                )
            elif outbox and outbox.status == 'skipped':
                logger.info(
                    "Skipped %s email to %s: %s",
                    template_type, to_email, outbox.skip_reason
                )
            return outbox
        except Exception:
            logger.error(
                "Failed to send %s email to %s",
                template_type, to_email, exc_info=True
            )
            return None

    @classmethod
    def send_registration_ack(cls, profile):
        """Send registration acknowledgement to developer."""
        site_url = cls._get_site_url()
        cls._send(
            to_email=profile.user.email,
            template_type='dev_registration_ack',
            context={
                'developer_name': profile.display_name,
                'developer_email': profile.user.email,
                'portal_url': f"{site_url}/en/developers/",
            },
        )

    @classmethod
    def send_account_approved(cls, profile):
        """Send approval notification to developer."""
        site_url = cls._get_site_url()
        cls._send(
            to_email=profile.user.email,
            template_type='dev_account_approved',
            context={
                'developer_name': profile.display_name,
                'dashboard_url': f"{site_url}/en/developers/dashboard/",
                'license_url': f"{site_url}/en/developers/license/",
                'docs_url': f"{site_url}/en/developers/",
            },
        )

    @classmethod
    def send_account_rejected(cls, profile):
        """Send rejection notification to developer."""
        site_url = cls._get_site_url()
        cls._send(
            to_email=profile.user.email,
            template_type='dev_account_rejected',
            context={
                'developer_name': profile.display_name,
                'rejection_reason': profile.rejection_reason or '',
                'support_email': cls._get_support_email(),
                'portal_url': f"{site_url}/en/developers/",
            },
        )

    @classmethod
    def send_account_suspended(cls, profile):
        """Send suspension notification to developer."""
        cls._send(
            to_email=profile.user.email,
            template_type='dev_account_suspended',
            context={
                'developer_name': profile.display_name,
                'suspension_reason': profile.rejection_reason or '',
                'support_email': cls._get_support_email(),
            },
        )

    @classmethod
    def send_submission_received(cls, submission):
        """Send submission received confirmation to developer."""
        site_url = cls._get_site_url()
        cls._send(
            to_email=submission.developer.user.email,
            template_type='dev_submission_received',
            context={
                'developer_name': submission.developer.display_name,
                'component_name': submission.component_name,
                'component_type': submission.type_display,
                'version': submission.version,
                'submission_url': f"{site_url}/en/developers/submissions/{submission.id}/",
            },
        )

    @classmethod
    def send_submission_approved(cls, submission):
        """Send submission approved notification to developer."""
        site_url = cls._get_site_url()
        cls._send(
            to_email=submission.developer.user.email,
            template_type='dev_submission_approved',
            context={
                'developer_name': submission.developer.display_name,
                'component_name': submission.component_name,
                'component_type': submission.type_display,
                'version': submission.version,
                'review_notes': submission.review_notes or '',
                'submission_url': f"{site_url}/en/developers/submissions/{submission.id}/",
            },
        )

    @classmethod
    def send_submission_rejected(cls, submission):
        """Send submission rejected notification to developer."""
        site_url = cls._get_site_url()
        cls._send(
            to_email=submission.developer.user.email,
            template_type='dev_submission_rejected',
            context={
                'developer_name': submission.developer.display_name,
                'component_name': submission.component_name,
                'component_type': submission.type_display,
                'version': submission.version,
                'review_notes': submission.review_notes or '',
                'submission_url': f"{site_url}/en/developers/submissions/{submission.id}/",
            },
        )

    @classmethod
    def send_revision_requested(cls, submission):
        """Send revision requested notification to developer."""
        site_url = cls._get_site_url()
        cls._send(
            to_email=submission.developer.user.email,
            template_type='dev_revision_requested',
            context={
                'developer_name': submission.developer.display_name,
                'component_name': submission.component_name,
                'component_type': submission.type_display,
                'version': submission.version,
                'review_notes': submission.review_notes or '',
                'submission_url': f"{site_url}/en/developers/submissions/{submission.id}/",
            },
        )

    @classmethod
    def send_component_published(cls, submission):
        """Send component published notification to developer."""
        site_url = cls._get_site_url()
        cls._send(
            to_email=submission.developer.user.email,
            template_type='dev_component_published',
            context={
                'developer_name': submission.developer.display_name,
                'component_name': submission.component_name,
                'component_type': submission.type_display,
                'version': submission.version,
                'dashboard_url': f"{site_url}/en/developers/analytics/",
            },
        )

    @classmethod
    def send_new_review(cls, review):
        """Send new review notification to developer (immediate preference)."""
        site_url = cls._get_site_url()
        rating_stars = '\u2605' * review.rating + '\u2606' * (5 - review.rating)
        cls._send(
            to_email=review.developer.user.email,
            template_type='dev_new_review',
            context={
                'developer_name': review.developer.display_name,
                'component_name': review.component_name,
                'rating': review.rating,
                'rating_stars': rating_stars,
                'review_title': review.title or '',
                'review_comment': review.comment or '',
                'reviewer_name': review.author_name or 'Anonymous',
                'is_verified_purchase': review.is_verified_purchase,
                'reviews_url': f"{site_url}/en/developers/reviews/",
            },
        )

    @classmethod
    def send_review_digest(cls, developer, reviews, period):
        """Send review digest email to developer (daily/weekly)."""
        site_url = cls._get_site_url()
        review_list = []
        for review in reviews:
            rating_stars = '\u2605' * review.rating + '\u2606' * (5 - review.rating)
            review_list.append({
                'component_name': review.component_name,
                'rating': review.rating,
                'rating_stars': rating_stars,
                'title': review.title or '',
                'comment': review.comment or '',
                'reviewer_name': review.author_name or 'Anonymous',
            })

        cls._send(
            to_email=developer.user.email,
            template_type='dev_review_digest',
            context={
                'developer_name': developer.display_name,
                'reviews': review_list,
                'review_count': len(review_list),
                'period': period,
                'reviews_url': f"{site_url}/en/developers/reviews/",
            },
        )

    @classmethod
    def send_license_approved(cls, license_request):
        """Send license approved notification to developer."""
        site_url = cls._get_site_url()
        expires_at = ''
        if license_request.license_expires_at:
            expires_at = license_request.license_expires_at.strftime('%B %d, %Y')

        cls._send(
            to_email=license_request.developer.user.email,
            template_type='dev_license_approved',
            context={
                'developer_name': license_request.developer.display_name,
                'license_key': license_request.license_key,
                'license_type': license_request.get_license_type_display(),
                'expires_at': expires_at,
                'dashboard_url': f"{site_url}/en/developers/dashboard/",
            },
        )

    @classmethod
    def send_license_rejected(cls, license_request):
        """Send license rejected notification to developer."""
        cls._send(
            to_email=license_request.developer.user.email,
            template_type='dev_license_rejected',
            context={
                'developer_name': license_request.developer.display_name,
                'rejection_reason': license_request.admin_notes or '',
                'support_email': cls._get_support_email(),
            },
        )
