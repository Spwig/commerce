"""
Celery beat tasks for hosted-service quota monitoring.

Exposes:

    refresh_hosted_service_usage
        Runs every 5 minutes under Community edition. Polls each hosted
        service's ``/api/v1/usage/`` endpoint and writes the merged
        snapshot to the Django cache. This is the *only* place the
        outbound HTTPS lives — admin request threads read from cache.

    check_hosted_service_quotas
        Runs once daily. Sends a one-off email to the admin when any of
        GeoIP/Geocoder/Push crosses 90% of its Community-tier quota.
        Rate-limited to at most one email per merchant per service per
        calendar month via a Django cache key.
"""

import logging
from datetime import datetime, timedelta, timezone

from celery import shared_task
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


def _current_month_bucket() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m')


@shared_task(bind=True, max_retries=0, ignore_result=True)
def refresh_hosted_service_usage(self):
    """
    Poll GeoIP / Geocoder / Push /usage/ endpoints and write the merged
    snapshot to the Django cache. No-op for non-Community installs.
    """
    try:
        from core.license import get_license_manager
        if not get_license_manager().is_community():
            return
    except Exception:
        return

    from core.hosted_services import refresh_usage_snapshot
    try:
        refresh_usage_snapshot()
    except Exception as e:
        # The snapshot itself already swallows per-service failures; a
        # top-level exception is genuinely surprising and worth logging.
        logger.warning("Hosted-service usage refresh failed: %s", e)


def _sent_key(service: str) -> str:
    return f'hosted_services:quota_email_sent:{service}:{_current_month_bucket()}'


def _admin_email() -> str:
    """Grab the site admin's email from ``SiteSettings``."""
    try:
        from core.models import SiteSettings
        site_settings = SiteSettings.objects.first()
        if site_settings and site_settings.admin_email:
            return site_settings.admin_email
    except Exception as e:
        logger.debug("Could not read SiteSettings.admin_email: %s", e)
    return ''


@shared_task(bind=True, max_retries=0, ignore_result=True)
def check_hosted_service_quotas(self):
    """
    Poll the hosted-services usage snapshot and email the admin once per
    calendar month per service if any service crosses 90% of its quota.
    """
    # Community edition only — paid tiers have plenty of headroom
    try:
        from core.license import get_license_manager
        if not get_license_manager().is_community():
            return
    except Exception:
        return

    admin_email = _admin_email()
    if not admin_email:
        logger.debug("No admin email configured; skipping quota alert")
        return

    # Force a fresh poll before evaluating the daily quota email — we
    # don't want to fire the email off a snapshot that's up to 5 min
    # stale when the merchant may already be past 100%.
    from core.hosted_services import refresh_usage_snapshot
    snapshot = refresh_usage_snapshot()

    triggered = []
    for key in ('geoip', 'geocoder', 'push'):
        svc = snapshot.get(key)
        if not svc or not svc.get('primary_window'):
            continue
        pct = svc['primary_window'].get('pct', 0)
        # Only 90-99% band: at 100% the merchant already sees a 429 and the
        # bright red banner in-admin, so an email is redundant.
        if pct < 90 or svc.get('over_limit'):
            continue
        sent_key = _sent_key(key)
        if cache.get(sent_key):
            continue
        triggered.append(svc)
        # Cache for 45 days so it covers the calendar-month boundary
        cache.set(sent_key, True, timeout=45 * 24 * 3600)

    if not triggered:
        return

    upgrade_url = snapshot.get('upgrade_url', 'https://updates.spwig.com/upgrade/')
    _send_quota_email(admin_email, triggered, upgrade_url)


def _send_quota_email(to: str, services: list, upgrade_url: str) -> None:
    """
    Send the quota-warning email via the platform email sender.

    Uses ``email_system.services.email_sender`` if available; falls back to
    Django's ``send_mail`` if the email system isn't wired up (e.g. tests).
    """
    subject_lines = ', '.join(
        f"{s['service']}: {s['primary_window']['pct']}% used"
        for s in services
    )
    subject = f"Approaching Spwig service limit — {subject_lines}"

    lines = [
        "Hi,",
        "",
        "One or more of your Spwig hosted services is above 90% of its "
        "Community-tier quota this period:",
        "",
    ]
    for s in services:
        w = s['primary_window']
        lines.append(
            f"  • {s['service']}: {w['current']} / {w['limit']} "
            f"({w['pct']}% used, {w['label']})"
        )
    lines += [
        "",
        "When a service hits 100% of the Community quota, requests start "
        "returning 429 until the window resets. To keep things running "
        "without interruption, upgrade to a paid tier:",
        "",
        f"  {upgrade_url}",
        "",
        "You'll only receive this email once per calendar month per service.",
        "",
        "— Spwig",
    ]
    body = '\n'.join(lines)

    try:
        # Prefer the platform's email sender if available
        from email_system.services.email_sender import EmailSendingService
        service = EmailSendingService()
        service.send_email(
            to_email=to,
            subject=subject,
            body_text=body,
            body_html=None,
        )
        logger.info("Sent quota-warning email to %s for %d service(s)",
                    to, len(services))
    except Exception as e:
        logger.debug("Email sender path failed (%s); falling back to send_mail", e)
        try:
            from django.core.mail import send_mail
            send_mail(
                subject=subject,
                message=body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                recipient_list=[to],
                fail_silently=True,
            )
            logger.info("Sent quota-warning email to %s via send_mail fallback", to)
        except Exception as e2:
            logger.warning("Quota-warning email failed for %s: %s", to, e2)
