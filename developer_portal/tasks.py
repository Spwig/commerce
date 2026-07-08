"""
Developer Portal Celery Tasks
Periodic sync tasks for analytics and reviews from the upgrade server.
Only active when SPWIG_IS_HQ=True (developer_portal in INSTALLED_APPS).
"""

import logging
import time
from decimal import Decimal, InvalidOperation
from celery import shared_task
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from core.celery_utils import BackgroundDBTask

logger = logging.getLogger(__name__)


@shared_task(name='developer_portal.sync_developer_analytics', base=BackgroundDBTask, ignore_result=True)
def sync_developer_analytics():
    """
    Sync download analytics for all approved developers from the upgrade server.
    Runs every 5 minutes via Celery Beat.
    """
    from .models import DeveloperProfile, ComponentAnalytics, DailyDownloadStat
    from .services.analytics_service import AnalyticsService

    service = AnalyticsService()
    developers = DeveloperProfile.objects.filter(
        status=DeveloperProfile.Status.APPROVED,
        upgrade_server_author_slug__gt='',
    )

    synced = 0
    for dev in developers:
        try:
            data = service.get_author_analytics(dev.upgrade_server_author_slug)
            if not data or 'components' not in data:
                continue

            # Upsert per-component stats
            for comp_data in data['components']:
                ComponentAnalytics.objects.update_or_create(
                    developer=dev,
                    component_slug=comp_data['slug'],
                    defaults={
                        'component_name': comp_data.get('name', ''),
                        'current_version': comp_data.get('current_version', ''),
                        'is_published': comp_data.get('is_published', True),
                        'downloads_total': comp_data.get('downloads_total', 0),
                        'downloads_period': comp_data.get('downloads_period', 0),
                        'period_days': data.get('period_days', 30),
                        'versions_count': comp_data.get('versions_count', 0),
                    },
                )

            # Upsert daily download trends
            for day_data in data.get('daily_downloads', []):
                DailyDownloadStat.objects.update_or_create(
                    developer=dev,
                    date=day_data['date'],
                    defaults={'downloads': day_data['downloads']},
                )

            synced += 1

        except Exception as e:
            logger.error('Failed to sync analytics for %s: %s', dev.developer_slug, e)

    logger.info('Synced analytics for %d developers', synced)
    return {'developers_synced': synced}


@shared_task(name='developer_portal.sync_developer_reviews', base=BackgroundDBTask, ignore_result=True)
def sync_developer_reviews():
    """
    Sync reviews for all approved developers from the upgrade server.
    Also pushes any unsynced developer responses.
    After sync, sends immediate email notifications for new reviews
    to developers with 'immediate' notification preference.
    Runs every 5 minutes via Celery Beat.
    """
    from .models import DeveloperProfile, ComponentReviewMirror
    from .services.analytics_service import AnalyticsService
    from .services.email_service import DeveloperEmailService

    service = AnalyticsService()
    developers = DeveloperProfile.objects.filter(
        status=DeveloperProfile.Status.APPROVED,
        upgrade_server_author_slug__gt='',
    )

    synced = 0
    responses_pushed = 0
    new_reviews = []
    now = timezone.now()

    for dev in developers:
        try:
            # Step 1: Push any unsynced responses first
            unsynced = dev.component_reviews.filter(response_synced=False)
            for review in unsynced:
                if review.developer_response and review.upgrade_server_review_id:
                    success = service.push_review_response(
                        review_id=review.upgrade_server_review_id,
                        author_slug=dev.upgrade_server_author_slug,
                        response_text=review.developer_response,
                    )
                    if success:
                        review.response_synced = True
                        review.save(update_fields=['response_synced', 'last_synced_at'])
                        responses_pushed += 1

            # Step 2: Pull reviews from upgrade server
            page = 1
            while True:
                data = service.get_author_reviews(
                    dev.upgrade_server_author_slug, page=page, page_size=50
                )
                if not data or not data.get('results'):
                    break

                for r in data['results']:
                    review_id = r.get('id')
                    if not review_id:
                        continue

                    # Parse datetime
                    response_at = None
                    if r.get('developer_response_at'):
                        response_at = parse_datetime(r['developer_response_at'])

                    review_created = parse_datetime(r['created_at'])

                    # Build defaults - preserve local unsynced response
                    defaults = {
                        'component_slug': r.get('component_slug', ''),
                        'component_name': r.get('component_name', ''),
                        'rating': r['rating'],
                        'title': r.get('title', ''),
                        'comment': r.get('comment', ''),
                        'author_name': r['author_name'],
                        'is_verified_purchase': r.get('is_verified_purchase', False),
                        'review_created_at': review_created,
                    }

                    # Only overwrite response from server if server has one
                    # (preserves local unsynced response)
                    server_response = r.get('developer_response', '')
                    if server_response:
                        defaults['developer_response'] = server_response
                        defaults['developer_response_at'] = response_at
                        defaults['response_synced'] = True

                    obj, created = ComponentReviewMirror.objects.update_or_create(
                        developer=dev,
                        upgrade_server_review_id=review_id,
                        defaults=defaults,
                    )

                    # Track newly created reviews for notification
                    # 24-hour guard prevents flooding on first sync
                    if (
                        created
                        and obj.review_created_at
                        and (now - obj.review_created_at).total_seconds() < 86400
                    ):
                        new_reviews.append(obj)

                if page >= data.get('pages', 1):
                    break
                page += 1

            synced += 1

        except Exception as e:
            logger.error('Failed to sync reviews for %s: %s', dev.developer_slug, e)

    # Step 3: Send immediate notifications for new reviews
    notifications_sent = 0
    for review in new_reviews:
        try:
            pref = review.developer.review_notification_preference
            if pref == 'immediate':
                DeveloperEmailService.send_new_review(review)
                review.notification_sent_at = now
                review.save(update_fields=['notification_sent_at'])
                notifications_sent += 1
        except Exception as e:
            logger.error(
                'Failed to send review notification for review %s: %s',
                review.pk, e,
            )

    logger.info(
        'Synced reviews for %d developers, pushed %d responses, '
        'sent %d immediate notifications',
        synced, responses_pushed, notifications_sent,
    )
    return {
        'developers_synced': synced,
        'responses_pushed': responses_pushed,
        'notifications_sent': notifications_sent,
    }


@shared_task(name='developer_portal.sync_developer_components', base=BackgroundDBTask, ignore_result=True)
def sync_developer_components():
    """
    Sync component metadata and version history from the upgrade server.
    Enriches ComponentAnalytics with marketplace data (description, pricing,
    thumbnail, type) and creates ComponentVersionMirror records.
    Also syncs author logo URL to DeveloperProfile.
    Runs every 5 minutes via Celery Beat.
    """
    from .models import (
        DeveloperProfile, ComponentAnalytics, ComponentVersionMirror,
    )
    from .services.analytics_service import AnalyticsService

    service = AnalyticsService()
    developers = DeveloperProfile.objects.filter(
        status=DeveloperProfile.Status.APPROVED,
        upgrade_server_author_slug__gt='',
    )

    synced = 0
    components_total = 0
    versions_total = 0

    for dev in developers:
        try:
            logo_url_updated = False

            # Step 1: Fetch all components via marketplace browse
            page = 1
            while True:
                data = service.get_author_components(
                    dev.upgrade_server_author_slug, page=page, page_size=100,
                )
                if not data or not data.get('results'):
                    break

                for comp in data['results']:
                    slug = comp.get('slug', '')
                    if not slug:
                        continue

                    # Parse price safely
                    try:
                        price = Decimal(comp.get('price_eur', '0'))
                    except (InvalidOperation, TypeError):
                        price = Decimal('0')

                    # Enrich ComponentAnalytics with marketplace data
                    ComponentAnalytics.objects.update_or_create(
                        developer=dev,
                        component_slug=slug,
                        defaults={
                            'component_name': comp.get('name', ''),
                            'current_version': comp.get('current_version', ''),
                            'is_published': True,
                            'component_type': comp.get('component_type', ''),
                            'description': comp.get('description', ''),
                            'thumbnail_url': comp.get('thumbnail_url', '') or '',
                            'pricing_model': comp.get('pricing_model', 'free'),
                            'price_eur': price,
                            'downloads_total': comp.get('download_count', 0),
                            'rating_count': comp.get('rating_count', 0),
                        },
                    )
                    components_total += 1

                    # Step 2: Fetch version history for this component
                    time.sleep(0.2)  # Rate-limit courtesy delay
                    detail = service.get_component_detail(slug)
                    if detail:
                        # Sync author logo URL (once per developer)
                        if not logo_url_updated:
                            author_info = detail.get('author', {})
                            new_logo_url = author_info.get('logo_url', '')
                            if new_logo_url and new_logo_url != dev.logo_url:
                                dev.logo_url = new_logo_url
                                dev.save(update_fields=['logo_url', 'updated_at'])
                            logo_url_updated = True

                        # Sync versions
                        for ver in detail.get('versions', []):
                            ver_num = ver.get('version', '')
                            if not ver_num:
                                continue

                            published_at = None
                            if ver.get('published_at'):
                                published_at = parse_datetime(ver['published_at'])

                            ComponentVersionMirror.objects.update_or_create(
                                developer=dev,
                                component_slug=slug,
                                version=ver_num,
                                defaults={
                                    'channel': ver.get('channel', 'stable'),
                                    'changelog': ver.get('changelog', ''),
                                    'published_at': published_at,
                                    'package_size_bytes': ver.get('package_size_bytes', 0) or 0,
                                    'breaking_changes': ver.get('breaking_changes', False),
                                    'security_update': ver.get('security_update', False),
                                },
                            )
                            versions_total += 1

                if page >= data.get('pages', 1):
                    break
                page += 1

            synced += 1

        except Exception as e:
            logger.error('Failed to sync components for %s: %s', dev.developer_slug, e)

    logger.info(
        'Synced components for %d developers: %d components, %d versions',
        synced, components_total, versions_total,
    )
    return {
        'developers_synced': synced,
        'components': components_total,
        'versions': versions_total,
    }


@shared_task(name='developer_portal.send_review_digests', base=BackgroundDBTask, ignore_result=True)
def send_review_digests():
    """
    Send review digest emails to developers with daily or weekly preference.
    Runs every hour. Sends:
    - Daily digest at ~8:00 UTC (hour 8)
    - Weekly digest on Mondays at ~8:00 UTC
    Collects all reviews where notification_sent_at is NULL for each developer.
    """
    from .models import DeveloperProfile, ComponentReviewMirror
    from .services.email_service import DeveloperEmailService

    now = timezone.now()

    # Only run digest logic at ~8:00 UTC (between 7:30 and 8:30)
    if now.hour != 8:
        return {'skipped': True, 'reason': 'Not digest hour'}

    is_monday = now.weekday() == 0
    digests_sent = 0

    # Collect developers who want digests
    prefs_to_process = ['daily']
    if is_monday:
        prefs_to_process.append('weekly')

    developers = DeveloperProfile.objects.filter(
        status=DeveloperProfile.Status.APPROVED,
        review_notification_preference__in=prefs_to_process,
    )

    for dev in developers:
        try:
            # Get un-notified reviews for this developer
            pending_reviews = ComponentReviewMirror.objects.filter(
                developer=dev,
                notification_sent_at__isnull=True,
            ).order_by('-review_created_at')

            if not pending_reviews.exists():
                continue

            period = dev.review_notification_preference
            reviews_list = list(pending_reviews)

            DeveloperEmailService.send_review_digest(dev, reviews_list, period)

            # Mark all as notified
            pending_reviews.update(notification_sent_at=now)
            digests_sent += 1

        except Exception as e:
            logger.error(
                'Failed to send review digest for %s: %s',
                dev.developer_slug, e,
            )

    logger.info('Sent %d review digests', digests_sent)
    return {'digests_sent': digests_sent, 'is_monday': is_monday}
