"""
Blog Admin Views

AJAX endpoints for admin list filtering.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Prefetch, Q
from django.http import JsonResponse
from django.template.loader import render_to_string

from media_library.models import MediaThumbnail

from .models import BlogCategory, BlogPost, BlogSubscriber, BlogTag


def blog_post_list_queryset():
    """Base queryset for the blog-post changelist and its AJAX filter endpoint.

    Prefetches the "medium" featured-image thumbnail so the card thumbnails don't
    fire a query each (MediaAsset.get_thumbnail reads the prefetch cache). Shared
    so the initial page and AJAX-filtered results stay identical.
    """
    return BlogPost.objects.select_related(
        "category", "featured_image", "created_by"
    ).prefetch_related(
        "tags",
        Prefetch(
            "featured_image__thumbnails",
            queryset=MediaThumbnail.objects.filter(size_preset="medium"),
        ),
    )


@staff_member_required
def filter_blog_categories(request):
    """
    AJAX endpoint for filtering blog categories in admin.

    Query Parameters:
    - search: Search by name or description
    - parent: Filter by parent category (use 'null' for top-level only)
    - status: Filter by active/inactive
    - has_posts: Filter by has posts (yes/no)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all categories
    categories = BlogCategory.objects.select_related("parent").prefetch_related("children", "posts")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        categories = categories.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # Parent filter
    parent_filter = request.GET.get("parent", "")
    if parent_filter == "null":
        categories = categories.filter(parent__isnull=True)
    elif parent_filter:
        try:
            parent_id = int(parent_filter)
            categories = categories.filter(parent_id=parent_id)
        except ValueError:
            pass

    # Status filter
    status_filter = request.GET.get("status", "")
    if status_filter == "active":
        categories = categories.filter(is_active=True)
    elif status_filter == "inactive":
        categories = categories.filter(is_active=False)

    # Has posts filter
    has_posts = request.GET.get("has_posts", "")
    if has_posts:
        categories = categories.annotate(post_count=Count("posts"))
        if has_posts == "yes":
            categories = categories.filter(post_count__gt=0)
        elif has_posts == "no":
            categories = categories.filter(post_count=0)

    # Order by sort_order then name
    categories = categories.order_by("sort_order", "name")

    html = render_to_string(
        "admin/blog/blogcategory/partials/category_cards.html",
        {"categories": categories, "request": request},
    )

    return JsonResponse({"html": html, "count": categories.count()})


@staff_member_required
def filter_blog_tags(request):
    """
    AJAX endpoint for filtering blog tags in admin.

    Query Parameters:
    - search: Search by name
    - usage: Filter by usage (used/unused)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all tags
    tags = BlogTag.objects.prefetch_related("posts")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        tags = tags.filter(name__icontains=search)

    # Usage filter
    usage_filter = request.GET.get("usage", "")
    if usage_filter:
        tags = tags.annotate(post_count=Count("posts"))
        if usage_filter == "used":
            tags = tags.filter(post_count__gt=0)
        elif usage_filter == "unused":
            tags = tags.filter(post_count=0)

    # Order by name
    tags = tags.order_by("name")

    html = render_to_string(
        "admin/blog/blogtag/partials/tag_cards.html", {"tags": tags, "request": request}
    )

    return JsonResponse({"html": html, "count": tags.count()})


@staff_member_required
def filter_blog_subscribers(request):
    """
    AJAX endpoint for filtering blog subscribers in admin.

    Query Parameters:
    - search: Search by email or name
    - verification: Filter by verification status
    - frequency: Filter by notification frequency
    - active: Filter by active status
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all subscribers
    subscribers = BlogSubscriber.objects.prefetch_related("subscribed_categories")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        subscribers = subscribers.filter(Q(email__icontains=search) | Q(name__icontains=search))

    # Verification status filter
    verification_filter = request.GET.get("verification", "")
    if verification_filter:
        subscribers = subscribers.filter(verification_status=verification_filter)

    # Frequency filter
    frequency_filter = request.GET.get("frequency", "")
    if frequency_filter:
        subscribers = subscribers.filter(notification_frequency=frequency_filter)

    # Active status filter
    active_filter = request.GET.get("active", "")
    if active_filter == "active":
        subscribers = subscribers.filter(is_active=True)
    elif active_filter == "inactive":
        subscribers = subscribers.filter(is_active=False)

    # Order by most recent first
    subscribers = subscribers.order_by("-created_at")

    html = render_to_string(
        "admin/blog/blogsubscriber/partials/subscriber_cards.html",
        {"subscribers": subscribers, "request": request},
    )

    return JsonResponse({"html": html, "count": subscribers.count()})


@staff_member_required
def filter_blog_posts(request):
    """
    AJAX endpoint for filtering blog posts in admin.

    Query Parameters:
    - search: Search by title, excerpt, or content
    - status: Filter by status (published/draft/scheduled/archived)
    - category: Filter by category id
    - featured: '1' → featured posts only
    - seo: 'complete' / 'incomplete' by meta_title + meta_description
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Mirror the changelist's view/change permission gate — staff_member_required
    # alone would let any staff user enumerate posts (incl. drafts).
    if not (
        request.user.has_perm("blog.view_blogpost") or request.user.has_perm("blog.change_blogpost")
    ):
        return JsonResponse({"error": "Forbidden"}, status=403)

    posts = blog_post_list_queryset()

    search = request.GET.get("search", "").strip()
    if search:
        posts = posts.filter(
            Q(title__icontains=search)
            | Q(excerpt__icontains=search)
            | Q(simple_content__icontains=search)
        )

    status_filter = request.GET.get("status", "")
    if status_filter:
        posts = posts.filter(status=status_filter)

    category_filter = request.GET.get("category", "")
    if category_filter:
        try:
            posts = posts.filter(category_id=int(category_filter))
        except ValueError:
            pass

    if request.GET.get("featured", "") == "1":
        posts = posts.filter(is_featured=True)

    seo_filter = request.GET.get("seo", "")
    seo_complete = (
        Q(meta_title__isnull=False)
        & ~Q(meta_title="")
        & Q(meta_description__isnull=False)
        & ~Q(meta_description="")
    )
    if seo_filter == "complete":
        posts = posts.filter(seo_complete)
    elif seo_filter == "incomplete":
        posts = posts.exclude(seo_complete)

    html = render_to_string(
        "admin/blog/blogpost/partials/post_card.html",
        {"posts": posts, "request": request},
    )

    return JsonResponse({"html": html, "count": posts.count()})
