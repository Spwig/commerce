"""
Blog views for Spwig eCommerce platform.

Provides views for:
- Blog listing with filtering
- Blog post detail
- Category and tag listing
- Subscriber management (verification, unsubscribe)
- RSS feed

"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import BlogPost, BlogCategory, BlogTag, BlogSubscriber, BlogSettings
from core.translation_utils import translate_storefront_context


def get_blog_context():
    """Get common blog context for templates."""
    settings = BlogSettings.get_settings()
    categories = BlogCategory.objects.filter(is_active=True)

    # Get tags with post counts
    tags = BlogTag.objects.filter(posts__status='published').distinct()

    return {
        'blog_settings': settings,
        'categories': categories,
        'tags': tags,
    }


def blog_list(request):
    """
    Blog listing page with pagination and filtering.

    Query parameters:
    - page: Page number for pagination
    - category: Filter by category slug
    - tag: Filter by tag slug
    - search: Search in title and content
    """
    settings = BlogSettings.get_settings()
    posts = BlogPost.published().select_related('category', 'featured_image')

    # Filtering
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    search = request.GET.get('search', '').strip()

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    if search:
        posts = posts.filter(
            models.Q(title__icontains=search) |
            models.Q(excerpt__icontains=search) |
            models.Q(simple_content__icontains=search)
        )

    # Pagination
    paginator = Paginator(posts, settings.posts_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Get featured posts for sidebar/header
    featured_posts = BlogPost.published().filter(is_featured=True)[:3]

    # Template selection from PageTemplateConfig
    from design.models import PageTemplateConfig
    from design.template_registry import get_blog_list_options, get_blog_list_template_path
    config = PageTemplateConfig.get_config()
    template_key = config.blog_list_template
    template_options = get_blog_list_options(template_key, config.blog_list_options or {})

    # Magazine template: build hero posts from featured or first N posts
    magazine_hero_posts = []
    magazine_remaining_posts = list(page_obj.object_list)
    is_first_page = not page_obj.has_previous()
    has_filters = category_slug or tag_slug or search

    if template_key == 'magazine' and is_first_page and not has_filters:
        hero_count = int(template_options.get('featured_count', 1))
        if featured_posts:
            magazine_hero_posts = list(featured_posts[:hero_count])
        elif magazine_remaining_posts:
            magazine_hero_posts = magazine_remaining_posts[:hero_count]
            magazine_remaining_posts = magazine_remaining_posts[hero_count:]

    context = {
        **get_blog_context(),
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'featured_posts': featured_posts,
        'magazine_hero_posts': magazine_hero_posts,
        'magazine_remaining_posts': magazine_remaining_posts,
        'current_category': category_slug,
        'current_tag': tag_slug,
        'search_query': search,
        'template_options': template_options,
    }

    translate_storefront_context(context, request)
    template_path = get_blog_list_template_path(template_key)
    return render(request, template_path, context)


def post_detail(request, slug):
    """
    Blog post detail view.

    Increments view count on each unique visit.
    Handles both simple content and page builder content.
    """
    post = get_object_or_404(
        BlogPost.objects.select_related(
            'category', 'featured_image', 'og_image', 'content_page'
        ).prefetch_related('tags'),
        slug=slug,
        status='published',
        published_at__lte=timezone.now()
    )

    # Increment view count (consider adding session check for unique views)
    BlogPost.objects.filter(pk=post.pk).update(
        view_count=models.F('view_count') + 1
    )

    settings = BlogSettings.get_settings()

    # Get related posts
    related_posts = []
    if settings.show_related_posts:
        related_posts = post.get_related_posts(limit=settings.related_posts_count)

    # Template selection: per-post override > site default
    from design.models import PageTemplateConfig
    from design.template_registry import get_blog_post_options, get_blog_post_template_path
    config = PageTemplateConfig.get_config()
    template_key = post.page_template or config.blog_post_template
    template_options = get_blog_post_options(template_key, config.blog_post_options or {})

    context = {
        **get_blog_context(),
        'post': post,
        'related_posts': related_posts,
        'template_options': template_options,
    }

    translate_storefront_context(context, request)

    # If using page builder, render via page builder template
    if post.use_page_builder and post.content_page:
        context['page'] = post.content_page
        return render(request, 'blog/post_detail_page_builder.html', context)

    template_path = get_blog_post_template_path(template_key)
    return render(request, template_path, context)


def category_posts(request, slug):
    """Blog posts filtered by category."""
    category = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    settings = BlogSettings.get_settings()

    posts = BlogPost.published().filter(
        category=category
    ).select_related('featured_image')

    paginator = Paginator(posts, settings.posts_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        **get_blog_context(),
        'category': category,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    }

    translate_storefront_context(context, request)
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """Blog posts filtered by tag."""
    tag = get_object_or_404(BlogTag, slug=slug)
    settings = BlogSettings.get_settings()

    posts = BlogPost.published().filter(
        tags=tag
    ).select_related('category', 'featured_image')

    paginator = Paginator(posts, settings.posts_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        **get_blog_context(),
        'tag': tag,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    }

    translate_storefront_context(context, request)
    return render(request, 'blog/tag_posts.html', context)


# =============================================================================
# Subscriber Views
# =============================================================================

@require_POST
@csrf_exempt  # CSRF token will be handled via API
def subscribe(request):
    """
    Handle blog subscription.

    POST data:
    - email: Subscriber email (required)
    - name: Subscriber name (optional)
    - frequency: Notification frequency (optional, default from settings)
    """
    import json

    settings = BlogSettings.get_settings()

    if not settings.enable_subscriptions:
        return JsonResponse({
            'success': False,
            'error': 'Subscriptions are currently disabled.'
        }, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    email = data.get('email', '').strip().lower()
    name = data.get('name', '').strip()
    frequency = data.get('frequency', settings.default_frequency)

    if not email:
        return JsonResponse({
            'success': False,
            'error': 'Email is required.'
        }, status=400)

    # Check if already subscribed
    existing = BlogSubscriber.objects.filter(email=email).first()
    if existing:
        if existing.is_active and existing.verification_status == 'verified':
            return JsonResponse({
                'success': False,
                'error': 'This email is already subscribed.'
            }, status=400)
        elif existing.is_active and existing.verification_status == 'pending':
            from blog.tasks import send_blog_verification_email
            send_blog_verification_email.delay(existing.pk)
            return JsonResponse({
                'success': True,
                'message': 'A verification email has been sent. Please check your inbox.'
            })
        else:
            # Resubscribe
            existing.resubscribe()
            if settings.require_double_opt_in:
                import secrets
                existing.verification_status = 'pending'
                existing.verification_token = secrets.token_urlsafe(32)
                existing.save()
                from blog.tasks import send_blog_verification_email
                send_blog_verification_email.delay(existing.pk)
                return JsonResponse({
                    'success': True,
                    'message': 'Please check your email to verify your subscription.'
                })
            else:
                existing.verify()
                return JsonResponse({
                    'success': True,
                    'message': 'You have been resubscribed!'
                })

    # Create new subscriber
    subscriber = BlogSubscriber.objects.create(
        email=email,
        name=name,
        notification_frequency=frequency,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
    )

    if settings.require_double_opt_in:
        from blog.tasks import send_blog_verification_email
        send_blog_verification_email.delay(subscriber.pk)
        return JsonResponse({
            'success': True,
            'message': 'Please check your email to verify your subscription.'
        })
    else:
        subscriber.verify()
        return JsonResponse({
            'success': True,
            'message': 'You have been subscribed!'
        })


@require_GET
def verify_subscription(request, token):
    """Verify email subscription via token."""
    subscriber = get_object_or_404(
        BlogSubscriber,
        verification_token=token,
        verification_status='pending'
    )

    subscriber.verify()

    return render(request, 'blog/subscription_verified.html', {
        'subscriber': subscriber,
    })


@require_GET
def unsubscribe(request, token):
    """Unsubscribe via one-click link."""
    subscriber = get_object_or_404(
        BlogSubscriber,
        unsubscribe_token=token
    )

    if request.GET.get('confirm') == '1':
        reason = request.GET.get('reason', '')
        subscriber.unsubscribe(reason=reason)
        return render(request, 'blog/unsubscribed.html', {
            'subscriber': subscriber,
        })

    return render(request, 'blog/unsubscribe_confirm.html', {
        'subscriber': subscriber,
    })


def subscription_preferences(request, token):
    """Manage subscription preferences."""
    subscriber = get_object_or_404(
        BlogSubscriber,
        unsubscribe_token=token,
        is_active=True
    )

    if request.method == 'POST':
        frequency = request.POST.get('frequency')
        if frequency in dict(BlogSubscriber.FREQUENCY_CHOICES):
            subscriber.notification_frequency = frequency

        # Handle category preferences
        category_ids = request.POST.getlist('categories')
        if category_ids:
            subscriber.subscribed_categories.set(category_ids)
        else:
            subscriber.subscribed_categories.clear()

        subscriber.save()

        return render(request, 'blog/preferences_updated.html', {
            'subscriber': subscriber,
        })

    context = {
        **get_blog_context(),
        'subscriber': subscriber,
    }

    return render(request, 'blog/subscription_preferences.html', context)


# =============================================================================
# RSS Feed
# =============================================================================

class BlogRSSFeedGenerator(Rss201rev2Feed):
    """Custom RSS feed with featured image support."""

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)

        # Add featured image as enclosure
        if item.get('featured_image_url'):
            handler.addQuickElement(
                'enclosure',
                attrs={
                    'url': item['featured_image_url'],
                    'type': 'image/jpeg',
                    'length': '0',
                }
            )

        # Add media:content for better image support
        if item.get('featured_image_url'):
            handler.addQuickElement(
                'media:content',
                attrs={
                    'url': item['featured_image_url'],
                    'medium': 'image',
                }
            )


class BlogRSSFeed(Feed):
    """RSS feed for blog posts."""
    feed_type = BlogRSSFeedGenerator

    def get_object(self, request):
        """Store request for use in other methods."""
        self.request = request
        return BlogSettings.get_settings()

    def title(self, obj):
        from core.models import SiteSettings
        site_settings = SiteSettings.get_settings()
        return f"{site_settings.site_name} Blog"

    def link(self, obj):
        return '/blog/'

    def description(self, obj):
        from core.models import SiteSettings
        site_settings = SiteSettings.get_settings()
        return f"Latest blog posts from {site_settings.site_name}"

    def items(self, obj):
        if not obj.rss_enabled:
            return []
        return BlogPost.published()[:obj.rss_posts_count]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        settings = BlogSettings.get_settings()
        if settings.rss_include_full_content:
            return item.simple_content or item.excerpt
        return item.excerpt

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published_at

    def item_author_name(self, item):
        if item.created_by:
            return item.created_by.get_full_name() or item.created_by.username
        return None

    def item_categories(self, item):
        categories = []
        if item.category:
            categories.append(item.category.name)
        categories.extend([tag.name for tag in item.tags.all()])
        return categories

    def item_extra_kwargs(self, item):
        """Add featured image to feed item."""
        extra = {}
        image_url = item.get_og_image_url()
        if image_url:
            # Make absolute URL
            if not image_url.startswith('http'):
                image_url = self.request.build_absolute_uri(image_url)
            extra['featured_image_url'] = image_url
        return extra


# Add models import at top
from django.db import models
