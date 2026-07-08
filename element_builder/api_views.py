"""
Element Builder API Views

REST API endpoints for custom element management.
Uses page_builder Element model for element tree structure.
All endpoints require admin authentication.
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample,
)
from django.utils.translation import gettext_lazy as _

from .models import CustomElement, ElementBinding
from .serializers import (
    CustomElementListSerializer,
    CustomElementDetailSerializer,
    BindableModelSerializer,
    ThumbnailPresetSerializer,
    ElementCreateSerializer,
    BindingCreateSerializer,
    ElementTreeSerializer,
)
from .registry import BINDABLE_MODELS
from page_builder.models import Element


@extend_schema_view(
    get=extend_schema(
        tags=['Catalog'],
        summary=_('List custom elements'),
        description=_('''
Returns all active custom elements for the store.

**Use Cases:**
- Populate element selection dropdowns
- Display available templates for search results
- List custom elements in page builder element library

**Authentication:** Admin session required
        '''),
        responses={
            200: CustomElementListSerializer(many=True),
            401: OpenApiResponse(description=_('Not authenticated')),
            403: OpenApiResponse(description=_('Permission denied')),
        }
    ),
    post=extend_schema(
        tags=['Catalog'],
        summary=_('Create custom element'),
        description=_('''
Creates a new custom element.

**Use Cases:**
- Create new data-bound UI element from builder
- Programmatically add custom elements

**Authentication:** Admin session required

**Side Effects:**
- Element becomes available in page builder element library
        '''),
        request=CustomElementDetailSerializer,
        responses={
            201: CustomElementDetailSerializer,
            400: OpenApiResponse(description=_('Validation error')),
            401: OpenApiResponse(description=_('Not authenticated')),
            403: OpenApiResponse(description=_('Permission denied')),
        }
    )
)
class CustomElementListAPI(generics.ListCreateAPIView):
    """List all custom elements or create a new one."""
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = CustomElement.objects.all()
        if self.request.method == 'GET':
            # For list view, optionally filter by active status
            is_active = self.request.query_params.get('is_active')
            if is_active is not None:
                queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset.order_by('name')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomElementDetailSerializer
        return CustomElementListSerializer


@extend_schema_view(
    get=extend_schema(
        tags=['Catalog'],
        summary=_('Get custom element details'),
        description=_('''
Returns full details of a custom element including its structure.

**Use Cases:**
- Load element for visual builder
- Retrieve element configuration for rendering

**Authentication:** Admin session required
        '''),
        parameters=[
            OpenApiParameter(
                name='pk',
                type=int,
                location=OpenApiParameter.PATH,
                description=_('Element ID')
            ),
        ],
        responses={
            200: CustomElementDetailSerializer,
            404: OpenApiResponse(description=_('Element not found')),
        }
    ),
    put=extend_schema(
        tags=['Catalog'],
        summary=_('Update custom element'),
        description=_('''
Updates a custom element's structure and properties.

**Use Cases:**
- Save changes from visual builder
- Update element metadata

**Authentication:** Admin session required

**Side Effects:**
- Clears cached renders for this element
        '''),
        request=CustomElementDetailSerializer,
        responses={
            200: CustomElementDetailSerializer,
            400: OpenApiResponse(description=_('Validation error')),
            404: OpenApiResponse(description=_('Element not found')),
        }
    ),
    patch=extend_schema(
        tags=['Catalog'],
        summary=_('Partial update custom element'),
        description=_('''
Partially updates a custom element.

**Use Cases:**
- Update only specific fields
- Toggle active status

**Authentication:** Admin session required
        '''),
        request=CustomElementDetailSerializer,
        responses={
            200: CustomElementDetailSerializer,
            400: OpenApiResponse(description=_('Validation error')),
            404: OpenApiResponse(description=_('Element not found')),
        }
    ),
    delete=extend_schema(
        tags=['Catalog'],
        summary=_('Delete custom element'),
        description=_('''
Permanently deletes a custom element.

**Use Cases:**
- Remove unused elements
- Clean up test elements

**Authentication:** Admin session required

**Warning:** This action cannot be undone. Consider setting is_active=false instead.
        '''),
        responses={
            204: OpenApiResponse(description=_('Element deleted')),
            404: OpenApiResponse(description=_('Element not found')),
        }
    )
)
class CustomElementDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a custom element."""
    queryset = CustomElement.objects.all()
    serializer_class = CustomElementDetailSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(
    tags=['Catalog'],
    summary=_('List bindable models'),
    description=_('''
Returns all models that can be bound to custom elements.

Each model includes:
- `key`: Model identifier (e.g., "catalog.Product")
- `label`: Human-readable name
- `icon`: Font Awesome icon class
- `fields`: Available fields with type info

**Use Cases:**
- Populate model selector in element builder
- Get available fields for binding UI

**Authentication:** Admin session required
    '''),
    responses={
        200: OpenApiResponse(
            response=BindableModelSerializer(many=True),
            description=_('Dictionary of bindable models with their fields'),
            examples=[
                OpenApiExample(
                    'Bindable Models',
                    value={
                        'catalog.Product': {
                            'label': 'Product',
                            'icon': 'fas fa-box',
                            'fields': {
                                'name': {
                                    'type': 'text',
                                    'label': 'Product Name'
                                },
                                'primary_image': {
                                    'type': 'image',
                                    'label': 'Main Image',
                                    'fk_to': 'media_library.MediaAsset',
                                    'computed': True
                                }
                            }
                        }
                    }
                )
            ]
        ),
    }
)
class BindableModelsAPI(APIView):
    """Return available bindable models and their fields."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Convert lazy translations to strings for JSON serialization
        result = {}
        for model_key, config in BINDABLE_MODELS.items():
            result[model_key] = {
                'label': str(config.get('label', model_key)),
                'icon': config.get('icon', 'fas fa-database'),
                'fields': {}
            }
            for field_name, field_config in config.get('fields', {}).items():
                result[model_key]['fields'][field_name] = {
                    'type': field_config.get('type'),
                    'label': str(field_config.get('label', field_name)),
                    'fk_to': field_config.get('fk_to'),
                    'computed': field_config.get('computed', False),
                    'description': str(field_config.get('description', '')) if field_config.get('description') else None,
                    'group': field_config.get('group'),
                }
        return Response(result)


@extend_schema(
    tags=['Catalog'],
    summary=_('List thumbnail presets'),
    description=_('''
Returns available image size presets for thumbnail selection.

**Use Cases:**
- Populate thumbnail size dropdown when binding image fields
- Show available sizes in visual builder

**Authentication:** Admin session required
    '''),
    responses={
        200: ThumbnailPresetSerializer(many=True),
    }
)
class ThumbnailPresetsAPI(APIView):
    """Return available thumbnail size presets."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        try:
            from media_library.models import ImageSizePreset
            presets = list(
                ImageSizePreset.objects.filter(is_active=True).values(
                    'slug', 'name', 'width', 'height'
                )
            )
        except Exception:
            # Fallback presets if ImageSizePreset is not available
            presets = [
                {'slug': 'small', 'name': 'Small', 'width': 150, 'height': 150},
                {'slug': 'medium', 'name': 'Medium', 'width': 300, 'height': 300},
                {'slug': 'large', 'name': 'Large', 'width': 600, 'height': 600},
            ]
        return Response(presets)


@extend_schema(
    tags=['Element Builder'],
    summary=_('Add element to custom element tree'),
    description=_('''
Creates a new page_builder Element and adds it to the custom element's tree.

**Use Cases:**
- Add elements in visual builder
- Build custom element structure

**Authentication:** Admin session required
    '''),
    request=ElementCreateSerializer,
    responses={
        201: OpenApiResponse(description=_('Element created')),
        400: OpenApiResponse(description=_('Validation error')),
        404: OpenApiResponse(description=_('Custom element or parent not found')),
    }
)
class ElementTreeAddAPI(APIView):
    """Add element to a custom element's tree."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        custom_element = get_object_or_404(CustomElement, pk=pk)
        serializer = ElementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        parent_id = data.get('parent_id')

        # Determine parent element
        if parent_id:
            parent = get_object_or_404(Element, pk=parent_id)
        elif custom_element.root_element:
            parent = custom_element.root_element
        else:
            parent = None

        # Create the new element
        # Note: Element requires a page, but for custom elements we use a null page
        # The element belongs to the custom element tree, not a page
        new_element = Element.objects.create(
            page=None,
            parent_element=parent,
            element_type=data['element_type'],
            content=data.get('content', {}),
            order=data.get('order', 0),
            is_active=True,
        )

        # If this is the first element and no root exists, set as root
        if not custom_element.root_element:
            custom_element.root_element = new_element
            custom_element.save(update_fields=['root_element'])

        return Response({
            'id': new_element.id,
            'element_type': new_element.element_type,
            'content': new_element.content,
            'order': new_element.order,
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Element Builder'],
    summary=_('Update element in custom element tree'),
    description=_('''
Updates an element's content or properties in the custom element tree.

**Use Cases:**
- Edit element content in visual builder
- Update element order

**Authentication:** Admin session required
    '''),
    responses={
        200: OpenApiResponse(description=_('Element updated')),
        404: OpenApiResponse(description=_('Element not found')),
    }
)
class ElementTreeUpdateAPI(APIView):
    """Update an element in a custom element's tree."""
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk, element_id):
        custom_element = get_object_or_404(CustomElement, pk=pk)
        element = get_object_or_404(Element, pk=element_id)

        # Update allowed fields
        if 'content' in request.data:
            element.content = request.data['content']
        if 'order' in request.data:
            element.order = request.data['order']
        if 'is_active' in request.data:
            element.is_active = request.data['is_active']

        element.save()

        return Response({
            'id': element.id,
            'element_type': element.element_type,
            'content': element.content,
            'order': element.order,
        })


@extend_schema(
    tags=['Element Builder'],
    summary=_('Delete element from custom element tree'),
    description=_('''
Removes an element and its children from the custom element tree.

**Use Cases:**
- Delete elements in visual builder
- Clean up unused elements

**Authentication:** Admin session required
    '''),
    responses={
        204: OpenApiResponse(description=_('Element deleted')),
        404: OpenApiResponse(description=_('Element not found')),
    }
)
class ElementTreeDeleteAPI(APIView):
    """Delete an element from a custom element's tree."""
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk, element_id):
        custom_element = get_object_or_404(CustomElement, pk=pk)
        element = get_object_or_404(Element, pk=element_id)

        # If deleting root element, clear the reference
        if custom_element.root_element_id == element.id:
            custom_element.root_element = None
            custom_element.save(update_fields=['root_element'])

        # Delete element (cascades to children via on_delete)
        element.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['Element Builder'],
    summary=_('Set element binding'),
    description=_('''
Creates or updates a data binding for an element.

**Use Cases:**
- Bind element content field to model field
- Configure thumbnail presets for image bindings

**Authentication:** Admin session required
    '''),
    request=BindingCreateSerializer,
    responses={
        200: OpenApiResponse(description=_('Binding saved')),
        404: OpenApiResponse(description=_('Element not found')),
    }
)
class ElementBindingAPI(APIView):
    """Manage element data bindings."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        """Create or update a binding."""
        custom_element = get_object_or_404(CustomElement, pk=pk)
        serializer = BindingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        element = get_object_or_404(Element, pk=data['element_id'])

        # Create or update binding
        binding, created = ElementBinding.objects.update_or_create(
            custom_element=custom_element,
            element=element,
            content_field=data['content_field'],
            defaults={
                'model_field': data['model_field'],
                'thumbnail_preset': data.get('thumbnail_preset', ''),
            }
        )

        return Response({
            'id': binding.id,
            'element_id': binding.element_id,
            'content_field': binding.content_field,
            'model_field': binding.model_field,
            'thumbnail_preset': binding.thumbnail_preset,
            'created': created,
        })

    def delete(self, request, pk):
        """Delete a binding."""
        custom_element = get_object_or_404(CustomElement, pk=pk)
        element_id = request.query_params.get('element_id')
        content_field = request.query_params.get('content_field')

        if not element_id or not content_field:
            return Response(
                {'error': 'element_id and content_field are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = ElementBinding.objects.filter(
            custom_element=custom_element,
            element_id=element_id,
            content_field=content_field,
        ).delete()

        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Binding not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@extend_schema(
    tags=['Element Builder'],
    summary=_('Clear all bindings for a custom element'),
    description=_('''
Deletes all element bindings for a custom element.

**Use Cases:**
- Clear bindings when changing target model
- Reset element to static content

**Authentication:** Admin session required
    '''),
    responses={
        204: OpenApiResponse(description=_('All bindings cleared')),
        404: OpenApiResponse(description=_('Custom element not found')),
    }
)
class ElementBindingClearAPI(APIView):
    """Clear all bindings for a custom element."""
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        """Delete all bindings for this custom element."""
        custom_element = get_object_or_404(CustomElement, pk=pk)

        deleted_count, _ = ElementBinding.objects.filter(
            custom_element=custom_element
        ).delete()

        return Response({
            'deleted': deleted_count,
            'message': f'Cleared {deleted_count} binding(s)'
        }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Element Builder'],
    summary=_('Get page builder element primitives'),
    description=_('''
Returns available page_builder element types for building custom elements.

**Use Cases:**
- Populate element picker in visual builder
- Get element configuration for rendering

**Authentication:** Admin session required
    '''),
    responses={
        200: OpenApiResponse(description=_('List of element types with config')),
    }
)
class ElementPrimitivesAPI(APIView):
    """Return available page_builder element types."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from page_builder.element_registry import get_registry

        registry = get_registry()
        primitives = []

        # Ensure registry is loaded
        if not registry._loaded:
            registry.discover_elements()

        # Get elements marked as primitives for element_builder
        for element_type, element_config in registry._elements.items():
            # Skip custom elements (those created in element_builder)
            if element_type.startswith('custom_'):
                continue

            # Only include elements marked as element_builder primitives
            if not getattr(element_config, 'element_builder_primitive', False):
                continue

            primitives.append({
                'type': element_type,
                'name': element_config.name,
                'icon': element_config.icon,
                'category': element_config.category,
                'description': getattr(element_config, 'description', ''),
                'default_content': getattr(element_config, 'default_content', {}),
            })

        # Sort by category then name for consistent display
        primitives.sort(key=lambda x: (x['category'], x['name']))

        return Response(primitives)


@extend_schema(
    tags=['Element Builder'],
    summary=_('Get element configuration'),
    description=_('''
Returns full config.json data for a specific element type.

Includes tabs, properties, base_properties for PropertyRenderer integration.

**Use Cases:**
- Load element config for PropertyRenderer in visual builder
- Get property definitions for element editing

**Authentication:** Admin session required
    '''),
    parameters=[
        OpenApiParameter(
            name='element_type',
            type=str,
            location=OpenApiParameter.PATH,
            description=_('Element type identifier (e.g., "heading", "image", "container")')
        ),
    ],
    responses={
        200: OpenApiResponse(description=_('Element configuration with tabs and properties')),
        404: OpenApiResponse(description=_('Element type not found')),
    }
)
class ElementConfigAPI(APIView):
    """Return full config.json for an element type."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, element_type):
        from page_builder.element_registry import get_registry

        registry = get_registry()

        # Ensure registry is loaded
        if not registry._loaded:
            registry.discover_elements()

        element_config = registry.get_element(element_type)

        if not element_config:
            return Response(
                {'error': f'Element type "{element_type}" not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Build response with all config data needed for PropertyRenderer
        return Response({
            'type': element_type,
            'name': element_config.name,
            'icon': element_config.icon,
            'category': element_config.category,
            'description': getattr(element_config, 'description', ''),
            'tabs': getattr(element_config, 'tabs', []),
            'base_properties': getattr(element_config, 'base_properties', True),
            'default_content': getattr(element_config, 'default_content', {}),
        })


@extend_schema(
    tags=['Element Builder'],
    summary=_('Apply container layout preset'),
    description=_('''
Applies a layout preset to a container element, creating child columns.

**Available Layouts:**
- `full-width`: Single full-width column
- `2-equal`: Two equal columns (50/50)
- `2-col-33-66`: 1/3 + 2/3 columns
- `2-col-66-33`: 2/3 + 1/3 columns
- `3-equal`: Three equal columns
- `3-col-25-50-25`: 1/4 + 1/2 + 1/4 columns
- `4-equal`: Four equal columns

**Use Cases:**
- Initialize a container with a column layout
- Set up multi-column layouts in custom elements

**Authentication:** Admin session required
    '''),
    responses={
        200: OpenApiResponse(description=_('Layout applied successfully')),
        400: OpenApiResponse(description=_('Invalid layout type')),
        404: OpenApiResponse(description=_('Element not found')),
    }
)
class ContainerLayoutAPI(APIView):
    """Apply a layout preset to a container element."""
    permission_classes = [permissions.IsAdminUser]

    LAYOUT_CONFIGS = {
        'full-width': [{'flex': '1 1 100%'}],
        '2-equal': [{'flex': '1 1 0'}, {'flex': '1 1 0'}],
        '2-col-33-66': [{'flex': '1 1 0'}, {'flex': '2 1 0'}],
        '2-col-66-33': [{'flex': '2 1 0'}, {'flex': '1 1 0'}],
        '3-equal': [{'flex': '1 1 0'}, {'flex': '1 1 0'}, {'flex': '1 1 0'}],
        '3-col-25-50-25': [{'flex': '1 1 0'}, {'flex': '2 1 0'}, {'flex': '1 1 0'}],
        '4-equal': [{'flex': '1 1 0'}, {'flex': '1 1 0'}, {'flex': '1 1 0'}, {'flex': '1 1 0'}],
    }

    def post(self, request, pk, element_id):
        custom_element = get_object_or_404(CustomElement, pk=pk)
        container = get_object_or_404(Element, pk=element_id)

        layout_type = request.data.get('layout_type')
        if layout_type not in self.LAYOUT_CONFIGS:
            return Response(
                {'error': f'Invalid layout type: {layout_type}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        config = self.LAYOUT_CONFIGS[layout_type]

        # Create child containers for each column
        for i, col_config in enumerate(config):
            Element.objects.create(
                page=None,
                element_type='container',
                parent_element=container,
                order=i,
                is_active=True,
                content={
                    'layout': 'flex',
                    'direction': 'column',
                    'gap': '16px',
                    'flex': col_config['flex'],
                    'layout_initialized': True,
                }
            )

        # Mark parent container as initialized with row layout
        if container.content is None:
            container.content = {}
        container.content.update({
            'layout': 'flex',
            'direction': 'row',
            'gap': '24px',
            'layout_initialized': True,
        })
        container.save(update_fields=['content'])

        return Response({
            'status': 'ok',
            'layout_type': layout_type,
            'columns_created': len(config),
        })


@extend_schema(
    tags=['Element Builder'],
    summary=_('Move element to new parent/position'),
    description=_('''
Moves an element to a new parent container and/or position.

**Use Cases:**
- Reorder elements via drag-and-drop
- Move elements between containers
- Re-parent elements in the tree

**Authentication:** Admin session required
    '''),
    responses={
        200: OpenApiResponse(description=_('Element moved successfully')),
        404: OpenApiResponse(description=_('Element or parent not found')),
    }
)
class ElementMoveAPI(APIView):
    """Move an element to a new parent and/or position."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk, element_id):
        custom_element = get_object_or_404(CustomElement, pk=pk)
        element = get_object_or_404(Element, pk=element_id)

        new_parent_id = request.data.get('parent_id')
        new_order = request.data.get('order', 0)

        old_parent = element.parent_element

        # Update parent
        if new_parent_id:
            new_parent = get_object_or_404(Element, pk=new_parent_id)
            element.parent_element = new_parent
        else:
            element.parent_element = None

        element.order = new_order
        element.save(update_fields=['parent_element', 'order'])

        # Reorder siblings in the new parent
        self._reorder_siblings(element)

        # Also reorder siblings in the old parent if it changed
        if old_parent and old_parent != element.parent_element:
            self._reorder_old_parent_siblings(old_parent)

        return Response({
            'status': 'ok',
            'element_id': element.id,
            'new_parent_id': new_parent_id,
            'new_order': new_order,
        })

    def _reorder_siblings(self, element):
        """Reorder siblings to ensure sequential ordering."""
        if element.parent_element:
            siblings = Element.objects.filter(
                parent_element=element.parent_element
            ).exclude(pk=element.pk).order_by('order')
        else:
            # Top-level elements (no parent)
            siblings = Element.objects.filter(
                parent_element__isnull=True,
                page__isnull=True
            ).exclude(pk=element.pk).order_by('order')

        # Reorder siblings to fill gaps
        order = 0
        for sibling in siblings:
            if order == element.order:
                order += 1  # Skip the slot for the moved element
            if sibling.order != order:
                sibling.order = order
                sibling.save(update_fields=['order'])
            order += 1

    def _reorder_old_parent_siblings(self, old_parent):
        """Reorder siblings in the old parent after an element was removed."""
        siblings = Element.objects.filter(
            parent_element=old_parent
        ).order_by('order')

        for i, sibling in enumerate(siblings):
            if sibling.order != i:
                sibling.order = i
                sibling.save(update_fields=['order'])


@extend_schema(
    tags=['Element Builder'],
    summary=_('Render element preview'),
    description=_('''
Renders an element from the custom element tree as HTML for visual preview.

**Use Cases:**
- Display visual preview of elements in the builder canvas
- Preview custom element with bound data

**Authentication:** Admin session required
    '''),
    parameters=[
        OpenApiParameter(
            name='pk',
            type=int,
            location=OpenApiParameter.PATH,
            description=_('Custom element ID')
        ),
        OpenApiParameter(
            name='element_id',
            type=int,
            location=OpenApiParameter.PATH,
            description=_('Element ID to render (optional - renders root if not provided)'),
            required=False
        ),
    ],
    responses={
        200: OpenApiResponse(description=_('Rendered HTML preview')),
        404: OpenApiResponse(description=_('Element not found')),
    }
)
class ElementPreviewAPI(APIView):
    """Render element HTML for visual preview."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk, element_id=None):
        from django.template.loader import get_template
        from django.template import TemplateDoesNotExist, TemplateSyntaxError, Context
        from django.core.cache import cache
        import logging

        logger = logging.getLogger(__name__)

        custom_element = get_object_or_404(CustomElement, pk=pk)

        # Determine which element to render
        if element_id:
            element = get_object_or_404(Element, pk=element_id)
        elif custom_element.root_element:
            element = custom_element.root_element
        else:
            return Response({
                'html': '<div class="preview-empty">No elements to preview</div>',
                'element_id': None
            })

        # Get preview context with mock data if model-bound
        preview_context = self._get_preview_context(custom_element, request)

        # Apply data bindings if we have a model instance
        model_instance = preview_context.get('model_instance')
        if model_instance:
            self._apply_bindings_to_tree(element, custom_element, model_instance)

        template_name = 'element_builder/element_preview_wrapper.html'

        # Clear any cached version of this template to ensure fresh render
        try:
            # Try pattern-based delete (django-redis)
            cache.delete_pattern('theme_template_*element_preview_wrapper*')
        except (AttributeError, NotImplementedError):
            # Fallback: just clear the specific key if we can guess it
            cache.delete(f'theme_template_default_{template_name}')

        try:
            # Load and compile the template fresh
            template = get_template(template_name)

            # Log detailed template info for debugging
            origin_info = "unknown"
            if hasattr(template, 'origin') and template.origin:
                origin_info = str(template.origin.name) if hasattr(template.origin, 'name') else str(template.origin)
            logger.info(f"Template loaded: {template_name}")
            logger.info(f"Template origin: {origin_info}")
            logger.info(f"Template type: {type(template)}")

            # Build the context properly
            context = {
                'element': element,
                'custom_element': custom_element,
                'request': request,
                **preview_context
            }

            # Render the template
            html = template.render(context, request)

            # Sanity check - if we see template syntax in output, something is wrong
            if '{#' in html or '{%' in html:
                logger.error(f"Template {template_name} was not processed - raw content returned")
                html = f'''<div class="preview-error">
                    Template rendering error: Template was not processed correctly.
                    Check that templatetags (element_tags) are loading properly.
                </div>'''

        except TemplateDoesNotExist as e:
            logger.error(f"Template not found: {template_name} - {e}")
            html = f'<div class="preview-error">Template not found: {template_name}</div>'
        except TemplateSyntaxError as e:
            logger.error(f"Template syntax error in {template_name}: {e}")
            html = f'<div class="preview-error">Template syntax error: {str(e)}</div>'
        except Exception as e:
            import traceback
            logger.exception(f"Error rendering preview for element {element.id}")
            html = f'''<div class="preview-error">
                Error rendering preview: {str(e)}
                <pre style="font-size: 10px; margin-top: 8px;">{traceback.format_exc()}</pre>
            </div>'''

        return Response({
            'html': html,
            'element_id': element.id
        })

    def _get_preview_context(self, custom_element, request):
        """Build context for element preview, including mock model data."""
        context = {
            'is_preview': True,
            'model_instance': None,
        }

        # If a preview item ID is provided in query params, load it
        preview_item_id = request.query_params.get('preview_item_id')
        if preview_item_id and custom_element.target_model:
            try:
                from django.apps import apps
                app_label, model_name = custom_element.target_model.split('.')
                model_class = apps.get_model(app_label, model_name)
                context['model_instance'] = model_class.objects.get(pk=preview_item_id)
            except Exception:
                pass  # Use mock data if item not found

        return context

    def _apply_bindings_to_tree(self, element, custom_element, model_instance, bindings=None):
        """
        Recursively apply data bindings to all elements in the tree.

        Modifies element.content in-place with resolved values from the model instance.
        Also caches children on element.cached_children to avoid re-fetching from DB.
        Changes are not saved to the database - they're only for this render cycle.
        """
        from .services.field_resolver import resolve_field_value

        # Get all bindings once at the root level
        if bindings is None:
            bindings = list(custom_element.bindings.all())

        # Apply bindings to this element
        element_bindings = [b for b in bindings if b.element_id == element.id]
        if element_bindings:
            # Ensure content is a mutable dict
            if element.content is None:
                element.content = {}
            elif not isinstance(element.content, dict):
                element.content = dict(element.content)

            for binding in element_bindings:
                value = resolve_field_value(
                    model_instance,
                    binding.model_field,
                    binding.thumbnail_preset
                )
                if value:
                    element.content[binding.content_field] = value
                else:
                    # Show placeholder for empty bound fields in preview
                    # This helps merchants understand the field is bound but has no data
                    field_label = binding.model_field.replace('_', ' ').title()
                    if binding.content_field in ('src', 'image', 'url'):
                        # For image/URL fields, use a placeholder image or leave empty
                        element.content[binding.content_field] = ''
                        element.content['empty_binding_label'] = f'No {field_label}'
                    else:
                        # For text fields, show a clear placeholder message
                        element.content[binding.content_field] = f'[No {field_label}]'
                    # Mark element as having empty preview content for styling
                    element.has_empty_preview = True

        # Prefetch children and cache them on the element
        # This avoids re-fetching from DB during template rendering
        children = list(element.child_elements.all())
        element.cached_children = children

        # Recursively apply to children
        for child in children:
            self._apply_bindings_to_tree(child, custom_element, model_instance, bindings)
