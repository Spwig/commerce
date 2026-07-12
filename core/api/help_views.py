"""
Help System API Views
REST API endpoints for help system
"""
import re
from datetime import datetime
from django.db.models import Q, F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from core.models import HelpCategory, HelpTopic, HelpFeedback, HelpView
from core.api.help_serializers import (
    HelpCategorySerializer,
    HelpTopicListSerializer,
    HelpTopicDetailSerializer,
    HelpFeedbackSerializer,
    HelpSearchSerializer,
    HelpSemanticSearchSerializer,
    HelpContextSerializer,
    AdminMetadataResponseSerializer,
    AdminModelMetadataSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary=_("List all help categories"),
        description=_("Get list of all help categories with topic counts"),
        tags=['Help System'],
    ),
    retrieve=extend_schema(
        summary=_("Get help category details"),
        description=_("Get detailed information about a specific help category"),
        tags=['Help System'],
    ),
)
class HelpCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for browsing help categories
    Read-only access to help categories
    """
    queryset = HelpCategory.objects.all().order_by('order', 'name')
    serializer_class = HelpCategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    pagination_class = None  # Disable pagination for help categories

    @extend_schema(
        summary=_("Get topics in category"),
        description=_("Get all published topics in this category"),
        responses={200: HelpTopicListSerializer(many=True)},
        tags=['Help System'],
    )
    @action(detail=True, methods=['get'])
    def topics(self, request, slug=None):
        """Get all topics in this category"""
        category = self.get_object()
        topics = HelpTopic.objects.filter(
            category=category,
            is_published=True
        ).order_by('title_i18n_key')

        serializer = HelpTopicListSerializer(topics, many=True, context={'request': request})
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary=_("List help topics"),
        description=_("Get list of published help topics with optional filtering"),
        parameters=[
            OpenApiParameter('category', OpenApiTypes.STR, description=_('Filter by category slug')),
            OpenApiParameter('component', OpenApiTypes.STR, description=_('Filter by component')),
            OpenApiParameter('search', OpenApiTypes.STR, description=_('Search in title and keywords')),
        ],
        tags=['Help System'],
    ),
    retrieve=extend_schema(
        summary=_("Get help topic details"),
        description=_("Get detailed content for a specific help topic"),
        tags=['Help System'],
    ),
)
class HelpTopicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for browsing help topics
    Read-only access with search and filtering
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    pagination_class = None  # Disable pagination for help topics

    def get_queryset(self):
        """Get published topics with optional filtering"""
        queryset = HelpTopic.objects.filter(is_published=True).select_related('category')

        # Filter by category
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by component
        component = self.request.query_params.get('component')
        if component:
            queryset = queryset.filter(component=component)

        # Simple search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title_i18n_key__icontains=search) |
                Q(keywords__contains=[search]) |
                Q(content_markdown__icontains=search)
            )

        return queryset.order_by('category__order', 'title_i18n_key')

    def get_serializer_class(self):
        """Use detail serializer for retrieve, list serializer for list"""
        if self.action == 'retrieve':
            return HelpTopicDetailSerializer
        return HelpTopicListSerializer

    def retrieve(self, request, *args, **kwargs):
        """Get topic and record view"""
        instance = self.get_object()

        # Increment view count
        HelpTopic.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)

        # Record view for telemetry (anonymous)
        session_id = request.session.session_key or 'anonymous'
        HelpView.objects.create(
            topic=instance,
            session_id=session_id,
            context_url=request.META.get('HTTP_REFERER', ''),
        )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary=_("Search help topics"),
        description=_("Full-text search across help topics with relevance ranking"),
        request=HelpSearchSerializer,
        responses={200: HelpTopicListSerializer(many=True)},
        tags=['Help System'],
    )
    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Advanced search for help topics
        Searches in title, content, keywords with relevance ranking
        """
        serializer = HelpSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data['query']
        component = serializer.validated_data.get('component')
        category = serializer.validated_data.get('category')
        limit = serializer.validated_data.get('limit', 10)

        # Build base queryset
        queryset = HelpTopic.objects.filter(is_published=True).select_related('category')

        if component:
            queryset = queryset.filter(component=component)

        if category:
            queryset = queryset.filter(category__slug=category)

        # Search terms
        search_terms = query.lower().split()

        # Score topics by relevance
        results = []
        for topic in queryset:
            score = 0

            # Check title (highest weight)
            title = topic.title_i18n_key.lower()
            for term in search_terms:
                if term in title:
                    score += 10

            # Check keywords (medium weight). Coerce to str: authored YAML
            # frontmatter can yield non-string values (e.g. an unquoted 9.99
            # parses as float), which would otherwise crash .lower().
            if topic.keywords:
                keywords = [str(k).lower() for k in topic.keywords if k is not None]
                for term in search_terms:
                    for keyword in keywords:
                        if term in keyword:
                            score += 5

            # Check content (lower weight)
            content = topic.content_markdown.lower()
            for term in search_terms:
                score += content.count(term)

            # Boost by popularity
            if topic.view_count > 0:
                score += min(topic.view_count / 100, 5)  # Max 5 points

            # Boost by helpfulness
            if topic.helpfulness_percentage:
                score += topic.helpfulness_percentage / 20  # Max 5 points

            if score > 0:
                results.append((score, topic))

        # Sort by relevance and limit
        results.sort(reverse=True, key=lambda x: x[0])
        topics = [topic for score, topic in results[:limit]]

        result_serializer = HelpTopicListSerializer(topics, many=True, context={'request': request})
        return Response(result_serializer.data)

    @extend_schema(
        summary=_("Semantic search for help topics"),
        description=_("Search using natural language understanding with automatic fallback to keyword search"),
        request=HelpSemanticSearchSerializer,
        responses={200: HelpTopicListSerializer(many=True)},
        tags=['Help System'],
    )
    @action(detail=False, methods=['post'])
    def semantic_search(self, request):
        """
        Semantic search with automatic fallback to keyword search.

        Uses sentence transformers and pgvector for context-aware search.
        Falls back to keyword search if semantic search fails or is unavailable.
        """
        import logging
        logger = logging.getLogger(__name__)

        try:
            # Validate request
            serializer = HelpSemanticSearchSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Perform semantic search
            from core.services.semantic_search import SearchService

            results = SearchService.search(
                query=serializer.validated_data['query'],
                language=serializer.validated_data.get('language', 'en'),
                component=serializer.validated_data.get('component'),
                category=serializer.validated_data.get('category'),
                limit=serializer.validated_data.get('limit', 10),
                threshold=serializer.validated_data.get('threshold', 0.4)
            )

            # Extract topics from results
            topics = [r['topic'] for r in results]

            # Serialize and return
            result_serializer = HelpTopicListSerializer(topics, many=True, context={'request': request})
            return Response({
                'results': result_serializer.data,
                'search_type': 'semantic',
                'count': len(topics)
            })

        except Exception as e:
            # Fallback to keyword search
            logger.error(f"Semantic search failed: {e}, falling back to keyword search")
            return self.search(request)

    @extend_schema(
        summary=_("Get contextual help suggestions"),
        description=_("Get help topics relevant to current page/context"),
        request=HelpContextSerializer,
        responses={200: HelpTopicListSerializer(many=True)},
        tags=['Help System'],
    )
    @action(detail=False, methods=['post'])
    def contextual(self, request):
        """
        Get help suggestions based on current page context
        Uses url_patterns to match relevant topics
        """
        serializer = HelpContextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url_path = serializer.validated_data['url_path']
        component = serializer.validated_data.get('component')
        limit = serializer.validated_data.get('limit', 5)

        # Build base queryset
        queryset = HelpTopic.objects.filter(is_published=True).select_related('category')

        if component:
            queryset = queryset.filter(component=component)

        # Find topics with matching URL patterns
        matching_topics = []
        for topic in queryset:
            if not topic.url_patterns:
                continue

            for pattern in topic.url_patterns:
                try:
                    if re.search(pattern, url_path):
                        matching_topics.append(topic)
                        break
                except re.error:
                    # Invalid regex pattern, skip
                    continue

        # If no pattern matches, return most popular topics for component
        if not matching_topics:
            matching_topics = list(
                queryset.filter(component=component or 'core')
                .order_by('-view_count')[:limit]
            )

        # Limit results
        matching_topics = matching_topics[:limit]

        result_serializer = HelpTopicListSerializer(
            matching_topics,
            many=True,
            context={'request': request}
        )
        return Response(result_serializer.data)

    @extend_schema(
        summary=_("Submit feedback for help topic"),
        description=_("Submit helpful/not helpful feedback with optional comment"),
        request=HelpFeedbackSerializer,
        responses={201: HelpFeedbackSerializer},
        tags=['Help System'],
    )
    @action(detail=True, methods=['post'])
    def feedback(self, request, slug=None):
        """Submit feedback for this topic"""
        topic = self.get_object()

        serializer = HelpFeedbackSerializer(
            data={**request.data, 'topic': topic.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    list=extend_schema(
        summary=_("List help feedback"),
        description=_("Get feedback for help topics (admin only)"),
        tags=['Help System'],
    ),
    retrieve=extend_schema(
        summary=_("Get help feedback details"),
        description=_("Get detailed information about a specific feedback entry including topic, rating, and comment. Admin only."),
        tags=['Help System'],
    ),
)
class HelpFeedbackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing help feedback
    Read-only access for administrators
    """
    queryset = HelpFeedback.objects.all().select_related('topic', 'user').order_by('-created_at')
    serializer_class = HelpFeedbackSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disable pagination for help feedback

    def get_queryset(self):
        """Filter by topic if specified"""
        queryset = super().get_queryset()

        topic_slug = self.request.query_params.get('topic')
        if topic_slug:
            queryset = queryset.filter(topic__slug=topic_slug)

        return queryset


# Admin Metadata API for Help System Documentation Discovery


class IsAdminOrHasAPIToken(BasePermission):
    """
    Custom permission that allows access if:
    1. User is authenticated and is staff/admin, OR
    2. Request has valid API token in Authorization header
    """

    def has_permission(self, request, view):
        # Check if user is authenticated admin
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True

        # Check if request has valid API token
        return _check_api_token(request)


def _check_api_token(request):
    """
    Verify API token from Authorization header

    Checks both environment variable (legacy) and database tokens.

    Args:
        request: Django request object

    Returns:
        bool: True if valid token provided, False otherwise
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False

    token_string = auth_header.replace('Bearer ', '').strip()

    # Get client IP for tracking
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0].strip()
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    # Method 1: Check database tokens (preferred)
    from core.utils.api_tokens import validate_api_token
    db_token = validate_api_token(
        token_string,
        token_type=None,  # Accept any token type for now
        record_usage=True,
        ip_address=ip_address
    )

    if db_token:
        return True

    # Method 2: Check environment variable (legacy fallback)
    env_token = getattr(settings, 'ADMIN_METADATA_API_TOKEN', None)
    if env_token and token_string == env_token:
        return True

    return False


def _extract_fieldsets_data(model_admin):
    """
    Extract fieldsets configuration from ModelAdmin

    Args:
        model_admin: Django ModelAdmin instance

    Returns:
        list: List of fieldset dictionaries
    """
    fieldsets = getattr(model_admin, 'fieldsets', None)
    fieldsets_data = []

    if fieldsets:
        for name, opts in fieldsets:
            # Handle nested field tuples and flatten them
            fields = opts.get('fields', [])
            flat_fields = []
            for field in fields:
                if isinstance(field, (list, tuple)):
                    flat_fields.extend([str(f) for f in field])
                else:
                    flat_fields.append(str(field))

            fieldsets_data.append({
                'name': name,
                'fields': flat_fields,
                'classes': list(opts.get('classes', [])),
                'description': opts.get('description', ''),
            })

    return fieldsets_data


def _extract_inlines_data(model_admin):
    """
    Extract inline formsets configuration from ModelAdmin

    Args:
        model_admin: Django ModelAdmin instance

    Returns:
        list: List of inline dictionaries
    """
    inlines_data = []

    for inline in getattr(model_admin, 'inlines', []):
        inline_model = getattr(inline, 'model', None)
        inlines_data.append({
            'class': inline.__name__,
            'model': inline_model.__name__ if inline_model else None,
            'extra': getattr(inline, 'extra', 1),
            'max_num': getattr(inline, 'max_num', None),
            'min_num': getattr(inline, 'min_num', None),
        })

    return inlines_data


def _extract_custom_actions(model_admin):
    """
    Extract custom admin actions from ModelAdmin

    Args:
        model_admin: Django ModelAdmin instance

    Returns:
        list: List of custom action names
    """
    actions = getattr(model_admin, 'actions', None)
    custom_actions = []

    # Handle None or empty actions
    if not actions:
        return custom_actions

    for action in actions:
        # Convert action to string name
        action_name = action if isinstance(action, str) else action.__name__
        # Exclude default Django actions
        if action_name not in ['delete_selected']:
            custom_actions.append(action_name)

    return custom_actions


def _extract_media_data(model_admin):
    """
    Extract Media (JS/CSS) configuration from ModelAdmin

    Args:
        model_admin: Django ModelAdmin instance

    Returns:
        dict or None: Media configuration dictionary
    """
    media_obj = getattr(model_admin, 'Media', None)

    if media_obj:
        js_files = getattr(media_obj, 'js', [])
        css_files = getattr(media_obj, 'css', {})

        return {
            'js': list(js_files) if js_files else [],
            'css': dict(css_files) if css_files else {},
        }

    return None


def _build_model_metadata(model, model_admin):
    """
    Build complete metadata dictionary for a single ModelAdmin

    Args:
        model: Django model class
        model_admin: Django ModelAdmin instance

    Returns:
        dict: Complete metadata dictionary
    """
    app_label = model._meta.app_label
    model_name = model._meta.model_name

    # Extract template names
    templates = {
        'change_form_template': getattr(model_admin, 'change_form_template', None),
        'change_list_template': getattr(model_admin, 'change_list_template', None),
        'delete_confirmation_template': getattr(model_admin, 'delete_confirmation_template', None),
        'object_history_template': getattr(model_admin, 'object_history_template', None),
    }

    # Extract list configuration (handle None values)
    ordering = getattr(model_admin, 'ordering', None)
    list_config = {
        'list_display': [str(field) for field in getattr(model_admin, 'list_display', []) or []],
        'list_filter': [str(field) for field in getattr(model_admin, 'list_filter', []) or []],
        'search_fields': [str(field) for field in getattr(model_admin, 'search_fields', []) or []],
        'ordering': [str(field) for field in ordering] if ordering else [],
        'date_hierarchy': getattr(model_admin, 'date_hierarchy', None),
    }

    # Extract fieldsets
    fieldsets_data = _extract_fieldsets_data(model_admin)

    # Extract form configuration
    form_class = getattr(model_admin, 'form', None)
    form_config = {
        'fieldsets': fieldsets_data,
        'readonly_fields': [str(field) for field in getattr(model_admin, 'readonly_fields', [])],
        'custom_form': form_class.__name__ if form_class else None,
        'form_module': form_class.__module__ if form_class else None,
    }

    # Extract inlines
    inlines_data = _extract_inlines_data(model_admin)

    # Extract custom actions
    custom_actions = _extract_custom_actions(model_admin)

    # Extract Media (JS/CSS)
    media_data = _extract_media_data(model_admin)

    # Build flags
    flags = {
        'has_custom_change_form': bool(templates['change_form_template']),
        'has_custom_change_list': bool(templates['change_list_template']),
        'has_custom_media': bool(media_data),
        'has_fieldsets': bool(fieldsets_data),
        'has_inlines': bool(inlines_data),
    }

    # Build complete metadata
    model_metadata = {
        'app_label': app_label,
        'model_name': model_name,
        'verbose_name': str(model._meta.verbose_name),
        'verbose_name_plural': str(model._meta.verbose_name_plural),
        'admin_class': model_admin.__class__.__name__,
        'templates': templates,
        'list_configuration': list_config,
        'form_configuration': form_config,
        'inlines': inlines_data,
        'custom_actions': custom_actions,
        'media': media_data,
        'flags': flags,
    }

    return model_metadata


@extend_schema(
    summary=_("Get admin metadata"),
    description=_("""Retrieve runtime admin metadata for documentation generation.

    This endpoint provides comprehensive metadata about all registered admin model classes,
    including custom templates, fieldsets, inline formsets, list configurations, and media files.

    **Authentication**: Requires either:
    - Admin session authentication (user must be staff)
    - Bearer token authentication (configured via ADMIN_METADATA_API_TOKEN setting)

    **Use Case**: The Help System uses this endpoint to discover runtime admin configurations
    that cannot be determined through static code analysis. This enables accurate documentation
    generation for custom admin interfaces.

    **Filtering**: Optional query parameters allow filtering by app_label and model_name to
    reduce response size when only specific models are needed.

    **Security**: This endpoint is restricted to authenticated admin users only. It exposes
    internal admin configuration details and should never be made publicly accessible.
    """),
    tags=['Help System'],
    parameters=[
        OpenApiParameter(
            name='app_label',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description=_('Filter results to specific Spwig app (e.g., "catalog", "orders")'),
            required=False,
        ),
        OpenApiParameter(
            name='model_name',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description=_('Filter results to specific model within app (e.g., "product", "order")'),
            required=False,
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=AdminMetadataResponseSerializer,
            description=_('Successfully retrieved admin metadata'),
        ),
        401: OpenApiResponse(
            description=_('Authentication required - provide admin credentials or valid API token'),
        ),
        403: OpenApiResponse(
            description=_('Permission denied - user must be staff/admin'),
        ),
    },
)
@api_view(['GET'])
@permission_classes([IsAdminOrHasAPIToken])
def admin_metadata_api(request):
    """
    Get admin metadata for help system documentation discovery

    This endpoint extracts runtime configuration from all registered admin model classes,
    including templates, fieldsets, inlines, and other customizations that are not
    visible through static code analysis.

    Authentication:
        - Session auth: User must be authenticated and have is_staff=True
        - Token auth: Provide 'Authorization: Bearer <token>' header with valid API token

    Query Parameters:
        - app_label (optional): Filter by Spwig app name
        - model_name (optional): Filter by specific model name

    Returns:
        JSON response with metadata for all matching admin model registrations
    """
    # Permission class has already checked authentication

    # Get filter parameters
    app_filter = request.query_params.get('app_label')
    model_filter = request.query_params.get('model_name')

    # Build metadata for all registered ModelAdmins
    models_metadata = []

    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        # Apply filters
        if app_filter and app_label != app_filter:
            continue
        if model_filter and model_name != model_filter:
            continue

        # Build metadata for this model
        try:
            model_metadata = _build_model_metadata(model, model_admin)
            models_metadata.append(model_metadata)
        except Exception as e:
            # Log error but continue processing other models
            # This ensures one broken ModelAdmin doesn't break the entire API
            import logging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Failed to extract metadata for {app_label}.{model_name}: {e}",
                exc_info=True
            )
            continue

    # Build response
    response_data = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'count': len(models_metadata),
        'models': models_metadata,
    }

    return Response(response_data, status=status.HTTP_200_OK)
