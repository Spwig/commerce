"""
DRF API Views for Blog.

Provides customer-facing and staff endpoints for:
- Blog posts (CRUD + publish/schedule/draft actions)
- Blog categories (CRUD)
- Blog tags (CRUD)
- Subscriber management (subscribe, verify, unsubscribe, preferences)
- Blog settings (public read)

"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import F, Prefetch
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)

from admin_api.permissions import IsStaffUser
from core.api.api_descriptions import (
    VALIDATION_ERROR as API_VALIDATION_ERROR,
    STAFF_ACCESS_REQUIRED,
)
from core.api.throttling import BurstRateThrottle, SustainedRateThrottle, PublicWriteThrottle
from core.api.authentication import HeadlessAPIMixin

from .models import BlogPost, BlogCategory, BlogTag, BlogSubscriber, BlogSettings
from .serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogPostWriteSerializer,
    BlogCategorySerializer,
    BlogCategoryDetailSerializer,
    BlogCategoryWriteSerializer,
    BlogTagSerializer,
    BlogTagWriteSerializer,
    BlogSubscribeSerializer,
    BlogPreferencesSerializer,
    BlogSettingsPublicSerializer,
)


# =============================================================================
# Blog Post ViewSet
# =============================================================================

@extend_schema_view(
    list=extend_schema(
        tags=['Blog'],
        summary=_("List blog posts"),
        description=_(
            "Returns a paginated list of blog posts. "
            "Public access returns published posts only. "
            "Authenticated staff see all statuses. "
            "Supports filtering by category slug, tag slug, featured/pinned flags and status. "
            "Use the `search` param to search across title, excerpt and content. "
            "Supports the `Accept-Language` header for translated title and excerpt."
        ),
        parameters=[
            OpenApiParameter('category__slug', str, description=_("Filter by category slug")),
            OpenApiParameter('tags__slug', str, description=_("Filter by tag slug")),
            OpenApiParameter('is_featured', bool, description=_("Filter featured posts")),
            OpenApiParameter('is_pinned', bool, description=_("Filter pinned posts")),
            OpenApiParameter('status', str, description=_("Filter by status (staff only)")),
            OpenApiParameter('search', str, description=_("Search in title, excerpt, content")),
            OpenApiParameter('ordering', str, description=_("Order by: published_at, view_count, reading_time_minutes, created_at (prefix with - for desc)")),
        ],
    ),
    retrieve=extend_schema(
        tags=['Blog'],
        summary=_("Get blog post"),
        description=_(
            "Returns full blog post detail including content, related posts, and SEO fields. "
            "Increments the view count. "
            "When `content_type` is `page_builder`, `simple_content` is null — "
            "the layout is rendered server-side and not available via API. "
            "Supports the `Accept-Language` header for translated fields."
        ),
    ),
    create=extend_schema(
        tags=['Blog'],
        summary=_("Create blog post"),
        description=_(
            "Create a new blog post. Staff access required. "
            "Slug is auto-generated from title if not provided. "
            "Tags are supplied as a list of tag slugs. "
            "Featured image is supplied as a MediaAsset primary key."
        ),
        responses={
            201: BlogPostDetailSerializer,
            400: OpenApiResponse(description=API_VALIDATION_ERROR),
            403: OpenApiResponse(description=STAFF_ACCESS_REQUIRED),
        },
    ),
    update=extend_schema(
        tags=['Blog'],
        summary=_("Update blog post"),
        description=_("Full update of a blog post. Staff access required."),
    ),
    partial_update=extend_schema(
        tags=['Blog'],
        summary=_("Partially update blog post"),
        description=_("Partial update of a blog post. Staff access required."),
    ),
    destroy=extend_schema(
        tags=['Blog'],
        summary=_("Delete blog post"),
        description=_("Permanently delete a blog post. Staff access required."),
        responses={
            204: OpenApiResponse(description=_("Post deleted")),
            403: OpenApiResponse(description=STAFF_ACCESS_REQUIRED),
        },
    ),
)
class BlogPostViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    Blog post API endpoint.

    - list/retrieve: Public (published posts). Staff see all statuses.
    - create/update/destroy: Staff only.
    - publish/schedule/draft: Staff only custom actions.
    """
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'tags__slug', 'is_featured', 'is_pinned', 'status']
    search_fields = ['title', 'excerpt', 'simple_content']
    ordering_fields = ['published_at', 'view_count', 'reading_time_minutes', 'created_at']
    ordering = ['-is_pinned', '-published_at']

    def get_queryset(self):
        base = BlogPost.objects.select_related(
            'category', 'featured_image', 'og_image', 'created_by'
        ).prefetch_related('tags')
        if self.request.user and self.request.user.is_staff:
            return base.all()
        return base.filter(status='published', published_at__lte=timezone.now())

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def get_throttles(self):
        if self.action in ('list', 'retrieve'):
            return [BurstRateThrottle(), SustainedRateThrottle()]
        return []

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BlogPostWriteSerializer
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count atomically (same as frontend view)
        BlogPost.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        tags=['Blog'],
        summary=_("Publish blog post"),
        description=_("Immediately publish a blog post. Sets status to 'published' and published_at to now if not already set."),
        responses={
            200: BlogPostDetailSerializer,
            400: OpenApiResponse(description=_("Post already published")),
            403: OpenApiResponse(description=STAFF_ACCESS_REQUIRED),
        },
    )
    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        post = self.get_object()
        if post.status == 'published':
            return Response(
                {'detail': 'Post is already published.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.status = 'published'
        if not post.published_at:
            post.published_at = timezone.now()
        post.scheduled_at = None
        post.save(update_fields=['status', 'published_at', 'scheduled_at'])
        return Response(BlogPostDetailSerializer(post, context={'request': request}).data)

    @extend_schema(
        tags=['Blog'],
        summary=_("Schedule blog post"),
        description=_("Schedule a blog post for future publication. Requires `scheduled_at` in the request body (ISO 8601 datetime)."),
        responses={
            200: BlogPostDetailSerializer,
            400: OpenApiResponse(description=_("Missing or past scheduled_at")),
            403: OpenApiResponse(description=STAFF_ACCESS_REQUIRED),
        },
    )
    @action(detail=True, methods=['post'])
    def schedule(self, request, slug=None):
        post = self.get_object()
        scheduled_at = request.data.get('scheduled_at')
        if not scheduled_at:
            return Response(
                {'detail': 'scheduled_at is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        from rest_framework.fields import DateTimeField
        try:
            scheduled_at = DateTimeField().to_internal_value(scheduled_at)
        except Exception:
            return Response(
                {'detail': 'Invalid scheduled_at format. Use ISO 8601 datetime.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if scheduled_at <= timezone.now():
            return Response(
                {'detail': 'scheduled_at must be in the future.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.status = 'scheduled'
        post.scheduled_at = scheduled_at
        post.save(update_fields=['status', 'scheduled_at'])
        return Response(BlogPostDetailSerializer(post, context={'request': request}).data)

    @extend_schema(
        tags=['Blog'],
        summary=_("Revert blog post to draft"),
        description=_("Set a blog post status back to draft."),
        responses={
            200: BlogPostDetailSerializer,
            403: OpenApiResponse(description=STAFF_ACCESS_REQUIRED),
        },
    )
    @action(detail=True, methods=['post'])
    def draft(self, request, slug=None):
        post = self.get_object()
        post.status = 'draft'
        post.save(update_fields=['status'])
        return Response(BlogPostDetailSerializer(post, context={'request': request}).data)


# =============================================================================
# Blog Category ViewSet
# =============================================================================

@extend_schema_view(
    list=extend_schema(
        tags=['Blog'],
        summary=_("List blog categories"),
        description=_(
            "Returns active blog categories. Staff see all categories including inactive ones. "
            "Supports the `Accept-Language` header for translated name and description."
        ),
    ),
    retrieve=extend_schema(
        tags=['Blog'],
        summary=_("Get blog category"),
        description=_("Returns a single category with SEO fields and child categories."),
    ),
    create=extend_schema(
        tags=['Blog'],
        summary=_("Create blog category"),
        description=_("Create a new blog category. Staff access required. Slug is auto-generated from name if not provided."),
        responses={
            201: BlogCategoryDetailSerializer,
            400: OpenApiResponse(description=API_VALIDATION_ERROR),
            403: OpenApiResponse(description=STAFF_ACCESS_REQUIRED),
        },
    ),
    update=extend_schema(
        tags=['Blog'],
        summary=_("Update blog category"),
        description=_("Full update of a category. Staff access required."),
    ),
    partial_update=extend_schema(
        tags=['Blog'],
        summary=_("Partially update blog category"),
        description=_("Partial update of a category. Staff access required."),
    ),
    destroy=extend_schema(
        tags=['Blog'],
        summary=_("Delete blog category"),
        description=_("Delete a blog category. Staff access required."),
    ),
)
class BlogCategoryViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    Blog category API endpoint.

    - list/retrieve: Public (active categories). Staff see all.
    - create/update/destroy: Staff only.
    """
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['sort_order', 'name']
    ordering = ['sort_order', 'name']

    def get_queryset(self):
        base = BlogCategory.objects.prefetch_related(
            Prefetch('children', queryset=BlogCategory.objects.filter(is_active=True))
        )
        if self.request.user and self.request.user.is_staff:
            return base.all()
        return base.filter(is_active=True)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def get_throttles(self):
        if self.action in ('list', 'retrieve'):
            return [BurstRateThrottle(), SustainedRateThrottle()]
        return []

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BlogCategoryWriteSerializer
        if self.action == 'retrieve':
            return BlogCategoryDetailSerializer
        return BlogCategorySerializer


# =============================================================================
# Blog Tag ViewSet
# =============================================================================

@extend_schema_view(
    list=extend_schema(
        tags=['Blog'],
        summary=_("List blog tags"),
        description=_(
            "Returns blog tags that have at least one published post. "
            "Staff see all tags including unused ones. "
            "Supports the `Accept-Language` header for translated tag names."
        ),
    ),
    retrieve=extend_schema(
        tags=['Blog'],
        summary=_("Get blog tag"),
        description=_("Returns a single tag."),
    ),
    create=extend_schema(
        tags=['Blog'],
        summary=_("Create blog tag"),
        description=_("Create a new blog tag. Staff access required. Slug is auto-generated from name if not provided."),
        responses={
            201: BlogTagSerializer,
            400: OpenApiResponse(description=API_VALIDATION_ERROR),
            403: OpenApiResponse(description=STAFF_ACCESS_REQUIRED),
        },
    ),
    update=extend_schema(
        tags=['Blog'],
        summary=_("Update blog tag"),
        description=_("Full update of a tag. Staff access required."),
    ),
    partial_update=extend_schema(
        tags=['Blog'],
        summary=_("Partially update blog tag"),
        description=_("Partial update of a tag. Staff access required."),
    ),
    destroy=extend_schema(
        tags=['Blog'],
        summary=_("Delete blog tag"),
        description=_("Delete a blog tag. Staff access required."),
    ),
)
class BlogTagViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    Blog tag API endpoint.

    - list/retrieve: Public. Staff see unused tags too.
    - create/update/destroy: Staff only.
    """
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'post_count']
    ordering = ['name']

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return BlogTag.objects.all()
        return BlogTag.objects.filter(post_count__gt=0)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def get_throttles(self):
        if self.action in ('list', 'retrieve'):
            return [BurstRateThrottle(), SustainedRateThrottle()]
        return []

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BlogTagWriteSerializer
        return BlogTagSerializer


# =============================================================================
# Subscription Function-Based Views
# =============================================================================

@extend_schema(
    tags=['Blog'],
    summary=_("Subscribe to blog notifications"),
    description=_(
        "Subscribe an email address to blog notifications. "
        "Handles new subscriptions, resending verification emails, and resubscribes. "
        "If double opt-in is enabled a verification email will be sent. "
        "Rate limited to 20 requests per hour per IP."
    ),
    request=BlogSubscribeSerializer,
    responses={
        200: OpenApiResponse(description=_("Success — verification sent or already handled")),
        400: OpenApiResponse(description=_("Validation error or subscriptions disabled")),
    },
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
@throttle_classes([PublicWriteThrottle])
def blog_subscribe(request):
    """Subscribe an email address to blog notifications."""
    blog_settings = BlogSettings.get_settings()

    if not blog_settings.enable_subscriptions:
        return Response(
            {'success': False, 'error': 'Subscriptions are currently disabled.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = BlogSubscribeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data
    email = data['email']
    name = data.get('name', '')
    frequency = data.get('notification_frequency', blog_settings.default_frequency)
    category_ids = data.get('category_ids', [])
    language_code = data.get('language_code', 'en')

    existing = BlogSubscriber.objects.filter(email=email).first()
    if existing:
        if existing.is_active and existing.verification_status == 'verified':
            return Response(
                {'success': False, 'error': 'This email is already subscribed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif existing.is_active and existing.verification_status == 'pending':
            from blog.tasks import send_blog_verification_email
            send_blog_verification_email.delay(existing.pk)
            return Response({'success': True, 'message': 'A verification email has been sent. Please check your inbox.'})
        else:
            # Resubscribe
            existing.resubscribe()
            existing.language_code = language_code
            existing.notification_frequency = frequency
            existing.save(update_fields=['language_code', 'notification_frequency'])
            if category_ids:
                existing.subscribed_categories.set(category_ids)
            if blog_settings.require_double_opt_in:
                import secrets
                existing.verification_status = 'pending'
                existing.verification_token = secrets.token_urlsafe(32)
                existing.save(update_fields=['verification_status', 'verification_token'])
                from blog.tasks import send_blog_verification_email
                send_blog_verification_email.delay(existing.pk)
                return Response({'success': True, 'message': 'Please check your email to verify your subscription.'})
            else:
                existing.verify()
                return Response({'success': True, 'message': 'You have been resubscribed!'})

    # Create new subscriber
    subscriber = BlogSubscriber.objects.create(
        email=email,
        name=name,
        notification_frequency=frequency,
        language_code=language_code,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
    )
    if category_ids:
        subscriber.subscribed_categories.set(category_ids)

    if blog_settings.require_double_opt_in:
        from blog.tasks import send_blog_verification_email
        send_blog_verification_email.delay(subscriber.pk)
        return Response({'success': True, 'message': 'Please check your email to verify your subscription.'})

    subscriber.verify()
    return Response({'success': True, 'message': 'You have been subscribed!'})


@extend_schema(
    tags=['Blog'],
    summary=_("Verify blog subscription"),
    description=_(
        "Verify an email subscription using the token sent in the verification email. "
        "The token is single-use and is cleared on successful verification."
    ),
    responses={
        200: OpenApiResponse(description=_("Subscription verified")),
        404: OpenApiResponse(description=_("Invalid or already-used token")),
    },
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
@throttle_classes([BurstRateThrottle])
def blog_verify_subscription(request, token):
    """Verify an email subscription via a token from a verification email."""
    subscriber = get_object_or_404(
        BlogSubscriber,
        verification_token=token,
        verification_status='pending',
    )
    subscriber.verify()
    return Response({'success': True, 'message': 'Your subscription has been verified. Thank you!'})


@extend_schema(
    tags=['Blog'],
    summary=_("Unsubscribe from blog"),
    description=_(
        "Unsubscribe an email address using the unsubscribe token. "
        "Optionally include a `reason` query parameter. "
        "The unsubscribe token remains stable and can be used for preference management."
    ),
    parameters=[
        OpenApiParameter('reason', str, location=OpenApiParameter.QUERY, description=_("Optional unsubscribe reason"), required=False),
    ],
    responses={
        200: OpenApiResponse(description=_("Successfully unsubscribed")),
        404: OpenApiResponse(description=_("Invalid unsubscribe token")),
    },
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
@throttle_classes([BurstRateThrottle])
def blog_unsubscribe(request, token):
    """Unsubscribe from blog notifications via an unsubscribe token."""
    subscriber = get_object_or_404(BlogSubscriber, unsubscribe_token=token)
    if not subscriber.is_active:
        return Response({'success': True, 'message': 'You are already unsubscribed.'})
    reason = request.query_params.get('reason', '')
    subscriber.unsubscribe(reason=reason)
    return Response({'success': True, 'message': 'You have been unsubscribed.'})


@extend_schema(
    tags=['Blog'],
    summary=_("Get or update subscription preferences"),
    description=_(
        "GET: Returns current subscription preferences for the given unsubscribe token. "
        "PUT: Updates notification frequency, subscribed categories, and language. "
        "The unsubscribe token is used as the authentication mechanism."
    ),
    request=BlogPreferencesSerializer,
    responses={
        200: BlogPreferencesSerializer,
        400: OpenApiResponse(description=API_VALIDATION_ERROR),
        404: OpenApiResponse(description=_("Invalid token or subscription not active")),
    },
)
@api_view(['GET', 'PUT'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
@throttle_classes([BurstRateThrottle])
def blog_subscription_preferences(request, token):
    """Get or update blog subscription preferences."""
    subscriber = get_object_or_404(
        BlogSubscriber,
        unsubscribe_token=token,
        is_active=True,
    )

    if request.method == 'GET':
        serializer = BlogPreferencesSerializer({
            'notification_frequency': subscriber.notification_frequency,
            'subscribed_categories': subscriber.subscribed_categories.all(),
            'language_code': subscriber.language_code,
            'is_active': subscriber.is_active,
            'verification_status': subscriber.verification_status,
            'email': subscriber.email,
        })
        return Response(serializer.data)

    # PUT
    serializer = BlogPreferencesSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data
    update_fields = []

    if 'notification_frequency' in data:
        subscriber.notification_frequency = data['notification_frequency']
        update_fields.append('notification_frequency')

    if 'language_code' in data:
        subscriber.language_code = data['language_code']
        update_fields.append('language_code')

    if update_fields:
        subscriber.save(update_fields=update_fields)

    category_ids = data.get('subscribed_category_ids', [])
    if category_ids:
        subscriber.subscribed_categories.set(category_ids)
    elif 'subscribed_category_ids' in request.data:
        # Explicit empty list clears all category preferences (receive all posts)
        subscriber.subscribed_categories.clear()

    return Response({
        'success': True,
        'message': 'Preferences updated.',
        'notification_frequency': subscriber.notification_frequency,
        'language_code': subscriber.language_code,
        'subscribed_categories': [
            {'id': c.id, 'name': c.name, 'slug': c.slug}
            for c in subscriber.subscribed_categories.all()
        ],
    })


# =============================================================================
# Blog Settings View
# =============================================================================

@extend_schema(
    tags=['Blog'],
    summary=_("Get public blog settings"),
    description=_(
        "Returns the public-facing blog configuration including posts per page, "
        "display options (reading time, view count, related posts), "
        "RSS settings, and subscription configuration."
    ),
    responses={200: BlogSettingsPublicSerializer},
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
@throttle_classes([BurstRateThrottle])
def blog_settings_api(request):
    """Return the public-facing blog settings."""
    settings = BlogSettings.get_settings()
    serializer = BlogSettingsPublicSerializer(settings)
    return Response(serializer.data)
