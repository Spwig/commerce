"""
API views for enhanced menu builder
Provides REST endpoints for menu management with full CRUD operations

Following rules_llm.md API documentation standards with drf-spectacular.
"""

import json
from django.http import JsonResponse
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample,
)

from .header_footer_models import Menu, MenuItem
from .menu_serializers import (
    MenuListSerializer,
    MenuDetailSerializer,
    MenuItemSerializer,
    MenuItemCreateUpdateSerializer,
    MenuReorderSerializer,
)


@extend_schema_view(
    get=extend_schema(
        tags=['Design'],
        summary=_('List all menus'),
        description=_('''
        Returns all menus for the store, ordered by location and name.

        **Use Cases:**
        - Populate menu selector dropdowns in builder interfaces
        - List available menus in admin dashboard

        **Authentication:** Staff session required
        '''),
        responses={
            200: MenuListSerializer(many=True),
            401: OpenApiResponse(description=_('Not authenticated')),
            403: OpenApiResponse(description=_('Permission denied - staff access required')),
        }
    ),
    post=extend_schema(
        tags=['Design'],
        summary=_('Create a new menu'),
        description=_('''
        Creates a new navigation menu.

        **Use Cases:**
        - Create new menu from menu builder
        - Programmatically add menus

        **Authentication:** Staff session required
        '''),
        request=MenuListSerializer,
        responses={
            201: MenuListSerializer,
            400: OpenApiResponse(description=_('Validation error')),
            401: OpenApiResponse(description=_('Not authenticated')),
        }
    )
)
class MenuListAPIView(generics.ListCreateAPIView):
    """List all menus or create a new one"""
    queryset = Menu.objects.all().order_by('location', 'name')
    serializer_class = MenuListSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema_view(
    get=extend_schema(
        tags=['Design'],
        summary=_('Get menu with full item tree'),
        description=_('''
        Returns complete menu details including all items in a nested tree structure.

        The `items_tree` field contains menu items with their children nested,
        suitable for rendering in the visual menu builder.

        **Use Cases:**
        - Load menu data for visual builder
        - Retrieve complete menu structure for rendering

        **Authentication:** Staff session required
        '''),
        responses={
            200: MenuDetailSerializer,
            404: OpenApiResponse(description=_('Menu not found')),
        }
    ),
    put=extend_schema(
        tags=['Design'],
        summary=_('Update menu settings'),
        description=_('''
        Updates menu properties (name, location, display type, styling).

        Does NOT update menu items - use the menu items endpoints for that.

        **Authentication:** Staff session required

        **Side Effects:**
        - Clears cached menu renders
        '''),
        request=MenuDetailSerializer,
        responses={
            200: MenuDetailSerializer,
            400: OpenApiResponse(description=_('Validation error')),
            404: OpenApiResponse(description=_('Menu not found')),
        }
    ),
    patch=extend_schema(
        tags=['Design'],
        summary=_('Partially update menu settings'),
        description=_('''
        Partially updates menu properties.

        **Authentication:** Staff session required
        '''),
        request=MenuDetailSerializer,
        responses={
            200: MenuDetailSerializer,
            400: OpenApiResponse(description=_('Validation error')),
            404: OpenApiResponse(description=_('Menu not found')),
        }
    ),
    delete=extend_schema(
        tags=['Design'],
        summary=_('Delete menu'),
        description=_('''
        Deletes a menu and all its items.

        **Authentication:** Staff session required

        **Warning:** This action cannot be undone.
        '''),
        responses={
            204: OpenApiResponse(description=_('Menu deleted')),
            404: OpenApiResponse(description=_('Menu not found')),
        }
    )
)
class MenuDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a menu"""
    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema_view(
    get=extend_schema(
        tags=['Design'],
        summary=_('Get menu item details'),
        description=_('''
        Returns details of a specific menu item.

        **Authentication:** Staff session required
        '''),
        responses={
            200: MenuItemSerializer,
            404: OpenApiResponse(description=_('Menu item not found')),
        }
    ),
    put=extend_schema(
        tags=['Design'],
        summary=_('Update menu item'),
        description=_('''
        Updates a menu item's properties.

        **Authentication:** Staff session required
        '''),
        request=MenuItemCreateUpdateSerializer,
        responses={
            200: MenuItemSerializer,
            400: OpenApiResponse(description=_('Validation error')),
            404: OpenApiResponse(description=_('Menu item not found')),
        }
    ),
    patch=extend_schema(
        tags=['Design'],
        summary=_('Partially update menu item'),
        description=_('''
        Partially updates a menu item's properties.

        **Authentication:** Staff session required
        '''),
        request=MenuItemCreateUpdateSerializer,
        responses={
            200: MenuItemSerializer,
            400: OpenApiResponse(description=_('Validation error')),
            404: OpenApiResponse(description=_('Menu item not found')),
        }
    ),
    delete=extend_schema(
        tags=['Design'],
        summary=_('Delete menu item'),
        description=_('''
        Deletes a menu item and all its children.

        **Authentication:** Staff session required

        **Warning:** Child items will also be deleted.
        '''),
        responses={
            204: OpenApiResponse(description=_('Menu item deleted')),
            404: OpenApiResponse(description=_('Menu item not found')),
        }
    )
)
class MenuItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a menu item"""
    queryset = MenuItem.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MenuItemCreateUpdateSerializer
        return MenuItemSerializer


@extend_schema(
    tags=['Design'],
    summary=_('Create menu item'),
    description=_('''
    Creates a new menu item.

    **Item Types:**
    - `link`: Standard link with URL
    - `page`: Link to a Page (uses page_reference)
    - `category`: Link to a Category (uses category_reference)
    - `custom_url`: Custom URL link
    - `divider`: Visual divider/separator
    - `header`: Section header (non-clickable)
    - `widget`: Widget item (login/logout, cart, account)

    **Authentication:** Staff session required
    '''),
    request=MenuItemCreateUpdateSerializer,
    responses={
        201: MenuItemSerializer,
        400: OpenApiResponse(description=_('Validation error')),
        401: OpenApiResponse(description=_('Not authenticated')),
    }
)
class MenuItemCreateAPIView(generics.CreateAPIView):
    """Create a new menu item"""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        return MenuItemCreateUpdateSerializer


@extend_schema(
    tags=['Design'],
    summary=_('Reorder menu items'),
    description=_('''
    Batch reorder menu items, supporting drag-and-drop operations.

    Accepts an array of item updates with new order and parent values.

    **Request Body:**
    ```json
    {
        "items": [
            {"id": 1, "order": 0, "parent_id": null},
            {"id": 2, "order": 1, "parent_id": null},
            {"id": 3, "order": 0, "parent_id": 2}
        ]
    }
    ```

    **Use Cases:**
    - Save drag-and-drop reordering from visual builder
    - Batch update item hierarchy

    **Authentication:** Staff session required
    '''),
    request=MenuReorderSerializer,
    responses={
        200: OpenApiResponse(
            description=_('Items reordered successfully'),
            examples=[
                OpenApiExample(
                    'Success',
                    value={'success': True, 'updated_count': 3}
                )
            ]
        ),
        400: OpenApiResponse(description=_('Validation error')),
    }
)
class MenuItemsReorderAPIView(APIView):
    """Reorder menu items (drag-and-drop support)"""
    permission_classes = [permissions.IsAdminUser]

    @transaction.atomic
    def post(self, request):
        serializer = MenuReorderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        items_data = serializer.validated_data['items']
        updated_count = 0

        for item_data in items_data:
            item_id = item_data['id']
            try:
                item = MenuItem.objects.get(pk=item_id)
                item.order = item_data['order']
                item.parent_id = item_data.get('parent_id')
                item.save(update_fields=['order', 'parent_id'])
                updated_count += 1
            except MenuItem.DoesNotExist:
                continue

        return Response({
            'success': True,
            'updated_count': updated_count
        })


@extend_schema(
    tags=['Design'],
    summary=_('Get available link sources for quick-add'),
    description=_('''
    Returns available pages and categories for quick-adding as menu items.

    **Query Parameters:**
    - `type`: Filter by source type (`pages`, `categories`, or `all`)
    - `search`: Search term to filter results

    **Use Cases:**
    - Populate quick-add panel in menu builder
    - Search for pages/categories to add as menu items

    **Authentication:** Staff session required
    '''),
    parameters=[
        OpenApiParameter(
            name='type',
            type=str,
            enum=['all', 'pages', 'categories'],
            description=_('Type of sources to return'),
            default='all'
        ),
        OpenApiParameter(
            name='search',
            type=str,
            description=_('Search term to filter results')
        ),
    ],
    responses={
        200: OpenApiResponse(
            description=_('Available link sources'),
            examples=[
                OpenApiExample(
                    'Response',
                    value={
                        'pages': [
                            {'id': 1, 'title': 'Home', 'slug': 'home', 'url': '/'},
                            {'id': 2, 'title': 'About', 'slug': 'about', 'url': '/about/'}
                        ],
                        'categories': [
                            {'id': 1, 'name': 'Electronics', 'slug': 'electronics', 'parent_id': None},
                            {'id': 2, 'name': 'Phones', 'slug': 'phones', 'parent_id': 1}
                        ]
                    }
                )
            ]
        ),
    }
)
class QuickAddSourcesAPIView(APIView):
    """Get available pages and categories for quick-add"""
    permission_classes = [permissions.IsAdminUser]

    # Maximum items to return per request
    RESULT_LIMIT = 50

    def get(self, request):
        source_type = request.query_params.get('type', 'all')
        search = request.query_params.get('search', '')

        result = {}

        # Get pages
        if source_type in ('all', 'pages'):
            from page_builder.models import Page
            pages_qs = Page.objects.filter(status='published')
            if search:
                pages_qs = pages_qs.filter(
                    Q(title__icontains=search) |
                    Q(slug__icontains=search)
                )
            # Get total count before limiting
            pages_total = pages_qs.count()
            result['pages'] = list(pages_qs.values(
                'id', 'title', 'slug', 'page_type'
            )[:self.RESULT_LIMIT])
            result['pages_total'] = pages_total
            result['pages_has_more'] = pages_total > self.RESULT_LIMIT

            # Add URL for each page
            for page in result['pages']:
                try:
                    page_obj = Page.objects.get(pk=page['id'])
                    page['url'] = page_obj.get_absolute_url()
                except:
                    page['url'] = f"/{page['slug']}/"

        # Get categories
        if source_type in ('all', 'categories'):
            from catalog.models import Category
            categories_qs = Category.objects.filter(is_active=True)
            if search:
                categories_qs = categories_qs.filter(
                    Q(name__icontains=search) |
                    Q(slug__icontains=search)
                )
            # Get total count before limiting
            categories_total = categories_qs.count()
            result['categories'] = list(categories_qs.values(
                'id', 'name', 'slug', 'parent_id'
            )[:self.RESULT_LIMIT])
            result['categories_total'] = categories_total
            result['categories_has_more'] = categories_total > self.RESULT_LIMIT

            # Add URL for each category
            for cat in result['categories']:
                try:
                    cat_obj = Category.objects.get(pk=cat['id'])
                    cat['url'] = cat_obj.get_absolute_url()
                except:
                    cat['url'] = f"/category/{cat['slug']}/"

        return Response(result)


@extend_schema(
    tags=['Design'],
    summary=_('Get rendered menu preview HTML'),
    description=_('''
    Returns rendered HTML preview of a menu for the visual builder.

    **Query Parameters:**
    - `display_type`: Override the menu's display type for preview
    - `device`: Device type for responsive preview (`desktop`, `tablet`, `mobile`)
    - `popup`: Set to `1` for full-page popup preview with device frames

    **Use Cases:**
    - Live preview in menu builder (JSON mode)
    - Full-screen popup preview (popup mode)

    **Authentication:** Staff session required
    '''),
    parameters=[
        OpenApiParameter(
            name='display_type',
            type=str,
            enum=['horizontal', 'vertical', 'dropdown', 'mega', 'accordion'],
            description=_('Override display type for preview')
        ),
        OpenApiParameter(
            name='device',
            type=str,
            enum=['desktop', 'tablet', 'mobile'],
            description=_('Device type for responsive preview'),
            default='desktop'
        ),
        OpenApiParameter(
            name='popup',
            type=str,
            enum=['0', '1'],
            description=_('Return full popup HTML page instead of JSON'),
            default='0'
        ),
    ],
    responses={
        200: OpenApiResponse(
            description=_('Rendered menu HTML'),
            examples=[
                OpenApiExample(
                    'Response',
                    value={
                        'html': '<nav class="menu-preview">...</nav>',
                        'item_count': 5
                    }
                )
            ]
        ),
        404: OpenApiResponse(description=_('Menu not found')),
    }
)
class MenuPreviewAPIView(APIView):
    """Generate live preview HTML for menu"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        from django.http import HttpResponse
        from .theme_utils import get_active_theme
        from .theme_models import ThemeBranding

        menu = get_object_or_404(Menu, pk=pk)
        display_type = request.query_params.get('display_type', menu.display_type)
        device = request.query_params.get('device', 'desktop')
        popup = request.query_params.get('popup', '0') == '1'

        # Get menu items
        menu_items = menu.get_items()

        # Get theme CSS URLs for popup mode
        theme_css_url = None
        brand_css_url = None
        base_css_url = None

        if popup:
            from django.conf import settings
            base_css_url = f"{settings.STATIC_URL}css/base.css"

            active_theme = get_active_theme()
            if active_theme:
                theme_css_url = active_theme.get_css_url()

            branding = ThemeBranding.objects.first()
            if branding:
                brand_css_url = branding.get_css_url()

        context = {
            'menu': menu,
            'menu_items': menu_items,
            'display_type': display_type,
            'device': device,
            'popup_mode': popup,
            'theme_css_url': theme_css_url,
            'brand_css_url': brand_css_url,
            'base_css_url': base_css_url,
            'request': request,
        }

        # If popup mode, return full HTML page
        if popup:
            try:
                html = render_to_string(
                    'design/menu_builder/preview_popup.html',
                    context
                )
                return HttpResponse(html, content_type='text/html')
            except Exception as e:
                return HttpResponse(
                    f'<html><body><h1>Preview Error</h1><p>{str(e)}</p></body></html>',
                    content_type='text/html',
                    status=500
                )

        # Standard JSON response for AJAX preview
        try:
            html = render_to_string(
                'design/menu_builder/partials/menu_preview.html',
                context
            )
        except Exception as e:
            html = f'<div class="menu-preview-error">Preview error: {str(e)}</div>'

        return Response({
            'html': html,
            'item_count': menu.items.filter(is_active=True).count()
        })


@extend_schema(
    tags=['Design'],
    summary=_('Get or update menu design tokens'),
    description=_('''
    Gets or updates menu design tokens stored in ThemeBranding.

    These tokens control overall menu styling (colors, spacing, typography)
    and are shared between the Branding app and Menu Builder.

    **GET Parameters:**
    - No parameters required

    **POST Body:**
    ```json
    {
        "tokens": {
            "text-color": "#333",
            "text-hover-color": "var(--color-primary)",
            "background-hover": "var(--color-primary)",
            "item-gap": "var(--space-2)"
        }
    }
    ```

    **Use Cases:**
    - Load menu tokens in menu builder
    - Save menu styling changes from menu builder
    - Sync menu tokens between Branding app and Menu Builder

    **Authentication:** Staff session required
    '''),
    responses={
        200: OpenApiResponse(
            description=_('Menu tokens'),
            examples=[
                OpenApiExample(
                    'Response',
                    value={
                        'tokens': {
                            'text-color': '#333',
                            'text-hover-color': 'var(--color-primary)',
                            'background-hover': 'var(--color-primary)',
                            'item-gap': 'var(--space-2)'
                        }
                    }
                )
            ]
        ),
    }
)
class MenuTokensAPIView(APIView):
    """Get or update menu design tokens from ThemeBranding"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """Get current menu tokens"""
        from .theme_models import ThemeBranding

        branding = ThemeBranding.objects.first()
        if not branding:
            return Response({'tokens': {}})

        # Get menu tokens from component_overrides
        overrides = branding.component_overrides or {}
        menu_tokens = overrides.get('menu', {})

        return Response({'tokens': menu_tokens})

    def post(self, request):
        """Update menu tokens"""
        from .theme_models import ThemeBranding

        tokens = request.data.get('tokens', {})

        # Get or create ThemeBranding
        branding, created = ThemeBranding.objects.get_or_create(pk=1)

        # Update component_overrides with menu tokens
        overrides = branding.component_overrides or {}

        if tokens:
            overrides['menu'] = tokens
        else:
            # Remove menu from overrides if empty
            overrides.pop('menu', None)

        branding.component_overrides = overrides
        branding.save()

        # Regenerate CSS with new tokens
        branding.generate_css()

        return Response({
            'success': True,
            'tokens': tokens
        })


@extend_schema(
    tags=['Design'],
    summary=_('Save complete menu structure'),
    description=_('''
    Saves the complete menu structure including all items from the visual builder.

    This endpoint accepts a nested tree structure and reconciles it with the database,
    creating, updating, and deleting items as needed.

    **Use Cases:**
    - Save entire menu from visual builder
    - Bulk import menu structure

    **Authentication:** Staff session required

    **Warning:** Items not included in the request will be deleted.
    '''),
    request=OpenApiResponse(
        description=_('Menu structure to save'),
        examples=[
            OpenApiExample(
                'Request',
                value={
                    'menu': {
                        'name': 'Main Navigation',
                        'display_type': 'horizontal',
                        'global_style': {},
                        'mobile_config': {}
                    },
                    'items': [
                        {
                            'id': 1,
                            'title': 'Home',
                            'item_type': 'page',
                            'page_reference_id': 1,
                            'order': 0,
                            'children': []
                        }
                    ]
                }
            )
        ]
    ),
    responses={
        200: OpenApiResponse(
            description=_('Menu saved successfully'),
            examples=[
                OpenApiExample(
                    'Success',
                    value={
                        'success': True,
                        'menu_id': 1,
                        'items_created': 2,
                        'items_updated': 3,
                        'items_deleted': 1
                    }
                )
            ]
        ),
        400: OpenApiResponse(description=_('Validation error')),
        404: OpenApiResponse(description=_('Menu not found')),
    }
)
class MenuSaveStructureAPIView(APIView):
    """Save complete menu structure from visual builder"""
    permission_classes = [permissions.IsAdminUser]

    @transaction.atomic
    def post(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)

        menu_data = request.data.get('menu', {})
        items_data = request.data.get('items', [])

        # Update menu properties
        if menu_data:
            for field in ['name', 'display_type', 'location', 'global_style', 'mobile_config', 'custom_css', 'css_classes']:
                if field in menu_data:
                    setattr(menu, field, menu_data[field])
            menu.save()

        # Track statistics
        stats = {
            'items_created': 0,
            'items_updated': 0,
            'items_deleted': 0,
        }

        # Get existing item IDs
        existing_ids = set(menu.items.values_list('id', flat=True))
        processed_ids = set()

        def process_items(items, parent=None):
            """Recursively process menu items"""
            for idx, item_data in enumerate(items):
                item_id = item_data.get('id')
                children = item_data.pop('children', [])

                # Prepare item fields
                item_fields = {
                    'menu': menu,
                    'parent': parent,
                    'order': idx,
                    'title': item_data.get('title', ''),
                    'item_type': item_data.get('item_type', 'link'),
                    'url': item_data.get('url', ''),
                    'target': item_data.get('target', '_self'),
                    'icon': item_data.get('icon', ''),
                    'badge_text': item_data.get('badge_text', ''),
                    'badge_color': item_data.get('badge_color', ''),
                    'style_config': item_data.get('style_config', {}),
                    'widget_config': item_data.get('widget_config', {}),
                    'tree_config': item_data.get('tree_config', {}),
                    'visibility_rules': item_data.get('visibility_rules', []),
                    'css_classes': item_data.get('css_classes', ''),
                    'is_active': item_data.get('is_active', True),
                }

                # Handle references
                if item_data.get('page_reference_id'):
                    item_fields['page_reference_id'] = item_data['page_reference_id']
                if item_data.get('category_reference_id'):
                    item_fields['category_reference_id'] = item_data['category_reference_id']

                if item_id and item_id in existing_ids:
                    # Update existing item
                    MenuItem.objects.filter(pk=item_id).update(**item_fields)
                    item = MenuItem.objects.get(pk=item_id)
                    processed_ids.add(item_id)
                    stats['items_updated'] += 1
                else:
                    # Create new item
                    item = MenuItem.objects.create(**item_fields)
                    processed_ids.add(item.id)
                    stats['items_created'] += 1

                # Process children
                if children:
                    process_items(children, parent=item)

        # Process all items
        process_items(items_data)

        # Delete items not in the new structure
        items_to_delete = existing_ids - processed_ids
        if items_to_delete:
            MenuItem.objects.filter(pk__in=items_to_delete).delete()
            stats['items_deleted'] = len(items_to_delete)

        return Response({
            'success': True,
            'menu_id': menu.id,
            **stats
        })
