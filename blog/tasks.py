"""
Celery tasks for blog functionality.

Provides:
- Scheduled post publishing
- Subscriber notification tasks
- Weekly and monthly digest emails
- Auto-share to social platforms

"""
from celery import shared_task
from django.utils import timezone
from django.db import models
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
import logging

logger = logging.getLogger(__name__)


@shared_task(name='blog.tasks.publish_scheduled_posts')
def publish_scheduled_posts():
    """
    Publish posts that are scheduled for the current time.

    Should run every minute via Celery Beat.
    """
    from .models import BlogPost

    now = timezone.now()
    scheduled_posts = BlogPost.objects.filter(
        status='scheduled',
        scheduled_at__lte=now
    )

    published_count = 0
    for post in scheduled_posts:
        try:
            post.status = 'published'
            post.published_at = now
            post.save(update_fields=['status', 'published_at', 'updated_at'])

            # Trigger subscriber notifications if enabled
            if post.notify_subscribers and not post.notification_sent:
                notify_subscribers_of_new_post.delay(post.pk)

            # Trigger auto-shares if enabled
            trigger_auto_shares_for_post.delay(post.pk)

            published_count += 1
            logger.info(f"Published scheduled blog post: {post.title} (pk={post.pk})")

        except Exception as e:
            logger.error(f"Error publishing scheduled post {post.pk}: {e}")

    if published_count > 0:
        logger.info(f"Published {published_count} scheduled blog posts")

    return published_count


@shared_task(name='blog.tasks.notify_subscribers_of_new_post')
def notify_subscribers_of_new_post(post_pk):
    """
    Send notification emails to immediate subscribers for a new post.

    Args:
        post_pk: Primary key of the BlogPost
    """
    from .models import BlogPost, BlogSubscriber

    try:
        post = BlogPost.objects.get(pk=post_pk)
    except BlogPost.DoesNotExist:
        logger.error(f"Blog post {post_pk} not found for subscriber notification")
        return

    if post.notification_sent:
        logger.info(f"Notification already sent for post {post_pk}")
        return

    # Get active, verified subscribers with immediate frequency
    subscribers = BlogSubscriber.objects.filter(
        is_active=True,
        verification_status='verified',
        notification_frequency='immediate'
    )

    # Filter by category preferences if applicable
    if post.category:
        # Include subscribers with no category preference OR matching category
        subscribers = subscribers.filter(
            models.Q(subscribed_categories__isnull=True) |
            models.Q(subscribed_categories__pk=post.category.pk)
        ).distinct()

    sent_count = 0
    site = Site.objects.get(pk=1)

    # Track emails sent to avoid duplicates
    sent_emails = set()

    # Send to BlogSubscriber users (legacy system)
    for subscriber in subscribers:
        try:
            _send_new_post_notification(post, subscriber, site)
            sent_count += 1
            sent_emails.add(subscriber.email.lower())
        except Exception as e:
            logger.error(f"Error sending notification to {subscriber.email}: {e}")

    # Also send to registered users with CommunicationPreference blog notifications enabled
    # (excluding those already sent via BlogSubscriber)
    from django.contrib.auth import get_user_model
    from accounts.models import CommunicationPreference

    User = get_user_model()

    # Get users with blog notifications enabled (excluding already-sent emails)
    comm_prefs = CommunicationPreference.objects.filter(
        email_enabled=True,
        email_marketing=True,
        email_verified=True,
        app_preferences__blog__enabled=True,
        app_preferences__blog__frequency='immediate'
    ).select_related('user').exclude(
        user__email__in=sent_emails
    )

    for prefs in comm_prefs:
        try:
            # Create a pseudo-subscriber object for the email sending function
            class PseudoSubscriber:
                def __init__(self, user, prefs):
                    self.email = user.email
                    self.name = user.get_full_name() or user.username
                    self.language_code = prefs.language_code

                def get_unsubscribe_url(self, site):
                    return f"https://{site.domain}/accounts/unsubscribe/{prefs.unsubscribe_token}/?type=blog_post_published"

                def get_preferences_url(self, site):
                    return f"https://{site.domain}/accounts/preferences/"

            pseudo_subscriber = PseudoSubscriber(prefs.user, prefs)
            _send_new_post_notification(post, pseudo_subscriber, site)
            sent_count += 1
        except Exception as e:
            logger.error(f"Error sending notification to {prefs.user.email}: {e}")

    # Mark notification as sent
    post.notification_sent = True
    post.save(update_fields=['notification_sent'])

    logger.info(f"Sent {sent_count} notifications for blog post: {post.title}")
    return sent_count


def _send_new_post_notification(post, subscriber, site):
    """Send individual post notification email."""
    from email_system.services.email_sender import EmailSendingService

    # Get language for subscriber
    language = subscriber.language_code

    # Get translated content
    content = post.get_translated_content(language)

    context = {
        'post': post,
        'subscriber': subscriber,
        'site': site,
        'unsubscribe_url': subscriber.get_unsubscribe_url(site),
        'preferences_url': subscriber.get_preferences_url(site),
        'title': content['title'],
        'excerpt': content['excerpt'],
    }

    subject = f"New Blog Post: {content['title']}"
    html_content = render_to_string('blog/emails/new_post_notification.html', context)
    text_content = render_to_string('blog/emails/new_post_notification.txt', context)

    # Send via email system with preference checking
    try:
        EmailSendingService.queue_email(
            to_email=subscriber.email,
            subject=subject,
            html_body=html_content,
            text_body=text_content,
            template_type='blog_post_published',  # Enables preference checking
        )
    except Exception as e:
        logger.error(f"Failed to send email to {subscriber.email}: {e}")
        raise


@shared_task(name='blog.tasks.send_blog_verification_email')
def send_blog_verification_email(subscriber_id):
    """
    Send a double opt-in verification email to a blog subscriber.

    Uses the 'blog_subscription_confirmed' MJML template from the email system.
    """
    from .models import BlogSubscriber
    from email_system.services.email_sender import EmailSendingService

    try:
        subscriber = BlogSubscriber.objects.get(pk=subscriber_id)
    except BlogSubscriber.DoesNotExist:
        logger.warning(f"Subscriber {subscriber_id} not found, skipping verification email")
        return

    if subscriber.verification_status != 'pending':
        logger.info(f"Subscriber {subscriber.email} is not pending, skipping verification email")
        return

    site = Site.objects.get(pk=1)

    context = {
        'subscriber_name': subscriber.name or subscriber.email,
        'blog_name': site.name,
        'confirmation_url': subscriber.get_verification_url(site),
    }

    try:
        EmailSendingService.send_template_email(
            to_email=subscriber.email,
            template_type='blog_subscription_confirmed',
            context=context,
            language=subscriber.language_code,
        )
        subscriber.verification_sent_at = timezone.now()
        subscriber.save(update_fields=['verification_sent_at'])
        logger.info(f"Sent verification email to {subscriber.email}")
    except Exception as e:
        logger.error(f"Failed to send verification email to {subscriber.email}: {e}")
        raise


@shared_task(name='blog.tasks.send_weekly_digest')
def send_weekly_digest():
    """
    Send weekly digest to subscribers.

    Should run once per week at the configured time via Celery Beat.
    """
    from .models import BlogPost, BlogSubscriber, BlogSettings
    from datetime import timedelta

    settings = BlogSettings.get_settings()
    now = timezone.now()

    # Check if it's the right day and hour
    if now.weekday() != settings.weekly_digest_day:
        logger.info(f"Skipping weekly digest: today is {now.weekday()}, scheduled for {settings.weekly_digest_day}")
        return

    if now.hour != settings.weekly_digest_hour:
        logger.info(f"Skipping weekly digest: current hour is {now.hour}, scheduled for {settings.weekly_digest_hour}")
        return

    # Get posts from last week
    week_ago = now - timedelta(days=7)
    posts = BlogPost.objects.filter(
        status='published',
        published_at__gte=week_ago,
        published_at__lt=now
    ).order_by('-published_at')

    if not posts.exists():
        logger.info("No posts to include in weekly digest")
        return

    # Get weekly subscribers
    subscribers = BlogSubscriber.objects.filter(
        is_active=True,
        verification_status='verified',
        notification_frequency='weekly'
    )

    sent_count = 0
    site = Site.objects.get(pk=1)

    for subscriber in subscribers:
        # Filter posts by subscriber's category preferences
        subscriber_posts = posts
        if subscriber.subscribed_categories.exists():
            subscriber_posts = posts.filter(
                category__in=subscriber.subscribed_categories.all()
            )

        if not subscriber_posts.exists():
            continue

        try:
            _send_digest_email(
                subscriber=subscriber,
                posts=subscriber_posts,
                digest_type='weekly',
                site=site
            )
            subscriber.last_digest_sent_at = now
            subscriber.save(update_fields=['last_digest_sent_at'])
            sent_count += 1
        except Exception as e:
            logger.error(f"Error sending weekly digest to {subscriber.email}: {e}")

    logger.info(f"Sent {sent_count} weekly digest emails")
    return sent_count


@shared_task(name='blog.tasks.send_monthly_digest')
def send_monthly_digest():
    """
    Send monthly digest to subscribers.

    Should run once per month at the configured time via Celery Beat.
    """
    from .models import BlogPost, BlogSubscriber, BlogSettings
    from datetime import timedelta

    settings = BlogSettings.get_settings()
    now = timezone.now()

    # Check if it's the right day and hour
    if now.day != settings.monthly_digest_day:
        logger.info(f"Skipping monthly digest: today is day {now.day}, scheduled for day {settings.monthly_digest_day}")
        return

    if now.hour != settings.monthly_digest_hour:
        logger.info(f"Skipping monthly digest: current hour is {now.hour}, scheduled for {settings.monthly_digest_hour}")
        return

    # Get posts from last month
    month_ago = now - timedelta(days=30)
    posts = BlogPost.objects.filter(
        status='published',
        published_at__gte=month_ago,
        published_at__lt=now
    ).order_by('-published_at')

    if not posts.exists():
        logger.info("No posts to include in monthly digest")
        return

    # Get monthly subscribers
    subscribers = BlogSubscriber.objects.filter(
        is_active=True,
        verification_status='verified',
        notification_frequency='monthly'
    )

    sent_count = 0
    site = Site.objects.get(pk=1)

    for subscriber in subscribers:
        # Filter posts by subscriber's category preferences
        subscriber_posts = posts
        if subscriber.subscribed_categories.exists():
            subscriber_posts = posts.filter(
                category__in=subscriber.subscribed_categories.all()
            )

        if not subscriber_posts.exists():
            continue

        try:
            _send_digest_email(
                subscriber=subscriber,
                posts=subscriber_posts,
                digest_type='monthly',
                site=site
            )
            subscriber.last_digest_sent_at = now
            subscriber.save(update_fields=['last_digest_sent_at'])
            sent_count += 1
        except Exception as e:
            logger.error(f"Error sending monthly digest to {subscriber.email}: {e}")

    logger.info(f"Sent {sent_count} monthly digest emails")
    return sent_count


def _send_digest_email(subscriber, posts, digest_type, site):
    """Send digest email to a subscriber."""
    from email_system.services.email_sender import EmailSendingService

    language = subscriber.language_code

    context = {
        'posts': posts,
        'subscriber': subscriber,
        'site': site,
        'digest_type': digest_type,
        'unsubscribe_url': subscriber.get_unsubscribe_url(site),
        'preferences_url': subscriber.get_preferences_url(site),
    }

    if digest_type == 'weekly':
        subject = f"Your Weekly Blog Digest"
        template_type = 'blog_weekly_digest'
    else:
        subject = f"Your Monthly Blog Digest"
        template_type = 'blog_monthly_digest'

    html_content = render_to_string(f'blog/emails/{digest_type}_digest.html', context)
    text_content = render_to_string(f'blog/emails/{digest_type}_digest.txt', context)

    try:
        EmailSendingService.queue_email(
            to_email=subscriber.email,
            subject=subject,
            html_body=html_content,
            text_body=text_content,
            template_type=template_type,  # Enables preference checking
        )
    except Exception as e:
        logger.error(f"Failed to send digest to {subscriber.email}: {e}")
        raise


# =============================================================================
# Auto-Share Tasks
# =============================================================================

@shared_task(name='blog.tasks.trigger_auto_shares_for_post')
def trigger_auto_shares_for_post(post_pk):
    """
    Create auto-share entries for a newly published post.

    Args:
        post_pk: Primary key of the BlogPost
    """
    from .models import BlogPost, SocialConnectorAccount, BlogPostAutoShare
    from django.contrib.sites.models import Site

    try:
        post = BlogPost.objects.get(pk=post_pk)
    except BlogPost.DoesNotExist:
        logger.error(f"Blog post {post_pk} not found for auto-share")
        return

    site = Site.objects.get(pk=1)

    # Get active social accounts
    social_accounts = SocialConnectorAccount.objects.filter(
        site=site,
        status='active',
        auto_share_enabled=True
    )

    created_count = 0

    for account in social_accounts:
        # Check if post has auto-share enabled for this provider
        should_share = False

        if account.provider_key.startswith('facebook') and post.auto_share_facebook:
            should_share = True
        elif account.provider_key.startswith('instagram') and post.auto_share_instagram:
            should_share = True
        elif account.provider_key.startswith('linkedin') and post.auto_share_linkedin:
            should_share = True

        if not should_share:
            continue

        # Create auto-share entry (if not already exists)
        auto_share, created = BlogPostAutoShare.objects.get_or_create(
            post=post,
            social_account=account,
            defaults={
                'status': 'pending',
            }
        )

        if created:
            created_count += 1
            logger.info(f"Created auto-share for {post.title} -> {account.name}")

            # Queue the actual share task
            process_auto_share.delay(str(auto_share.pk))

    logger.info(f"Created {created_count} auto-share entries for post: {post.title}")
    return created_count


@shared_task(name='blog.tasks.process_auto_share', bind=True, max_retries=3)
def process_auto_share(self, auto_share_pk):
    """
    Process a single auto-share entry.

    Posts content to the social platform via the connector.

    Args:
        auto_share_pk: Primary key (UUID) of the BlogPostAutoShare
    """
    from .models import BlogPostAutoShare
    import uuid

    try:
        auto_share = BlogPostAutoShare.objects.get(pk=uuid.UUID(auto_share_pk))
    except BlogPostAutoShare.DoesNotExist:
        logger.error(f"Auto-share {auto_share_pk} not found")
        return

    if auto_share.status in ['posted', 'skipped']:
        logger.info(f"Auto-share {auto_share_pk} already processed")
        return

    # Update status to posting
    auto_share.status = 'posting'
    auto_share.save(update_fields=['status'])

    try:
        account = auto_share.social_account
        post = auto_share.post

        # Check if account is still active
        if account.status != 'active':
            auto_share.status = 'failed'
            auto_share.error_message = f"Social account status is {account.status}"
            auto_share.save(update_fields=['status', 'error_message'])
            return

        # Load the social connector
        connector = _load_social_connector(account)

        if not connector:
            auto_share.status = 'failed'
            auto_share.error_message = "Social connector not found or not installed"
            auto_share.save(update_fields=['status', 'error_message'])
            return

        # Build post content
        content = _build_share_content(post, account)

        # Get post image URL
        image_url = post.get_og_image_url()

        # Post to social platform
        result = connector.post(
            account=account,
            text=content,
            link=f"https://{Site.objects.get(pk=1).domain}{post.get_absolute_url()}",
            image_url=image_url
        )

        # Update auto-share with success
        auto_share.status = 'posted'
        auto_share.platform_post_id = result.get('post_id', '')
        auto_share.platform_post_url = result.get('post_url', '')
        auto_share.posted_at = timezone.now()
        auto_share.posted_content = content
        auto_share.save()

        # Update account last successful post
        account.last_successful_post_at = timezone.now()
        account.save(update_fields=['last_successful_post_at'])

        logger.info(f"Successfully posted to {account.name}: {post.title}")

    except Exception as e:
        logger.error(f"Error processing auto-share {auto_share_pk}: {e}")

        auto_share.status = 'failed'
        auto_share.error_message = str(e)
        auto_share.retry_count += 1
        auto_share.next_retry_at = auto_share.calculate_next_retry()
        auto_share.save()

        # Retry if possible
        if auto_share.can_retry():
            retry_delay = auto_share.next_retry_at - timezone.now()
            raise self.retry(countdown=int(retry_delay.total_seconds()), exc=e)


def _load_social_connector(account):
    """
    Load the social connector class for an account.

    Dynamically imports the connector from the component registry,
    following the same pattern as translations/providers/registry.py.

    Returns the connector instance or None if not found.
    """
    import json
    from component_updates.integration_paths import INTEGRATIONS_DIR, import_component_module

    component = account.component
    if not component:
        # Try to find component by provider_key
        from component_updates.models import ComponentRegistry
        component = ComponentRegistry.objects.filter(
            component_type='social_connector',
            slug=account.provider_key,
        ).exclude(current_version__isnull=True).first()

    if not component:
        logger.warning(f"No social connector component found for {account.provider_key}")
        return None

    component_dir = INTEGRATIONS_DIR / 'social_connector' / component.slug / 'current'
    if not component_dir.exists():
        logger.warning(f"Social connector directory not found: {component_dir}")
        return None

    # Load manifest
    manifest_path = component_dir / 'manifest.json'
    if not manifest_path.exists():
        logger.error(f"No manifest.json found in {component_dir}")
        return None

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load manifest from {component_dir}: {e}")
        return None

    # Import connector module
    module_path = manifest.get('entry_point', 'connector')
    connector_class_name = manifest.get('class_name', 'Connector')
    module_name = f"social_connector_{component.slug}"

    try:
        module = import_component_module(component_dir, module_path, module_name)
        connector_class = getattr(module, connector_class_name, None)
        if not connector_class:
            logger.error(f"Connector class '{connector_class_name}' not found in module")
            return None

        credentials = account.get_credentials()
        return connector_class(credentials=credentials)
    except Exception as e:
        logger.error(f"Failed to load social connector for {account.provider_key}: {e}")
        return None


def _build_share_content(post, account):
    """
    Build the share content for a social post.

    Uses account template if configured, otherwise default format.
    """
    template = account.post_template or "{title}\n\n{excerpt}\n\n{url}"
    hashtags = account.default_hashtags or ""

    # Get translated content (primary language)
    content = post.get_translated_content(None)

    # Custom message overrides template
    if post.social_share_message:
        text = post.social_share_message
    else:
        text = template.format(
            title=content['title'],
            excerpt=content['excerpt'][:200] + "..." if len(content['excerpt']) > 200 else content['excerpt'],
            url=post.get_absolute_url(),
            hashtags=hashtags
        )

    return text


@shared_task(name='blog.tasks.retry_failed_auto_shares')
def retry_failed_auto_shares():
    """
    Retry failed auto-shares that are due for retry.

    Should run every 5 minutes via Celery Beat.
    """
    from .models import BlogPostAutoShare

    now = timezone.now()

    # Get failed shares that are due for retry
    pending_retries = BlogPostAutoShare.objects.filter(
        status='failed',
        next_retry_at__lte=now,
        retry_count__lt=models.F('max_retries')
    )

    queued_count = 0
    for auto_share in pending_retries:
        if auto_share.can_retry():
            auto_share.status = 'pending'
            auto_share.save(update_fields=['status'])
            process_auto_share.delay(str(auto_share.pk))
            queued_count += 1

    if queued_count > 0:
        logger.info(f"Queued {queued_count} auto-shares for retry")

    return queued_count


@shared_task(name='blog.tasks.refresh_expiring_social_tokens')
def refresh_expiring_social_tokens():
    """
    Refresh OAuth tokens that are about to expire.

    Should run hourly via Celery Beat.
    """
    from .models import SocialConnectorAccount
    from datetime import timedelta

    now = timezone.now()
    expiry_threshold = now + timedelta(hours=24)  # Refresh tokens expiring in 24 hours

    expiring_accounts = SocialConnectorAccount.objects.filter(
        status='active',
        access_token_expires_at__lte=expiry_threshold,
        access_token_expires_at__gt=now
    )

    refreshed_count = 0
    for account in expiring_accounts:
        try:
            connector = _load_social_connector(account)
            if connector and hasattr(connector, 'refresh_token'):
                connector.refresh_token(account)
                refreshed_count += 1
                logger.info(f"Refreshed token for {account.name}")
        except Exception as e:
            logger.error(f"Error refreshing token for {account.name}: {e}")
            account.status = 'token_expired'
            account.last_error = str(e)
            account.last_error_at = now
            account.save()

    if refreshed_count > 0:
        logger.info(f"Refreshed {refreshed_count} social account tokens")

    return refreshed_count
