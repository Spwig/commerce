"""
API views for Header/Footer Visual Builder
DRF-compliant REST endpoints for loading, saving, and manipulating header/footer templates

All endpoints require admin authentication and are documented via drf-spectacular.
API tag: Design (per rules_llm.md approved tag list)
"""

import json
import logging
from pathlib import Path

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)
from django.utils.translation import gettext_lazy as _

from core.api.api_descriptions import (
    HEADER_NOT_FOUND,
    FOOTER_NOT_FOUND,
    INVALID_REQUEST,
)

from .header_footer_models import (
    HeaderTemplate, FooterTemplate, Widget,
    WidgetPlacement, Menu
)
from .hf_serializers import (
    WidgetPlacementSerializer,
    WidgetPlacementCreateSerializer,
    WidgetPlacementUpdateSerializer,
    ReorderPlacementsSerializer,
    HeaderBuilderResponseSerializer,
    HeaderBuilderUpdateSerializer,
    HeaderDuplicateSerializer,
    HeaderDuplicateResponseSerializer,
    FooterBuilderResponseSerializer,
    FooterBuilderUpdateSerializer,
    WidgetLibraryItemSerializer,
    HeaderPresetSerializer,
    FooterPresetSerializer,
    ClonePresetSerializer,
    ClonePresetResponseSerializer,
    MenuListSerializer,
    WidgetSchemasResponseSerializer,
    SuccessResponseSerializer,
    ErrorResponseSerializer,
)

logger = logging.getLogger(__name__)


# ============================================================
# Header Builder API
# ============================================================

@extend_schema_view(
    get=extend_schema(
        tags=['Design'],
        summary=_('Get header template for builder'),
        description=_('''
        Load a header template with all widget placements for the visual builder.

        Returns the header configuration including zones and all placed widgets
        with their merged configurations (base config + overrides).

        **Authentication:** Admin user required
        '''),
        responses={
            200: OpenApiResponse(
                response=HeaderBuilderResponseSerializer,
                description=_('Header template data with widget placements')
            ),
            404: OpenApiResponse(description=HEADER_NOT_FOUND),
        }
    ),
    post=extend_schema(
        tags=['Design'],
        summary=_('Update header template'),
        description=_('''
        Update header template properties.

        Supports partial updates - only provided fields will be modified.

        **Authentication:** Admin user required
        '''),
        request=HeaderBuilderUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_('Header updated successfully')
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_('Invalid request data')
            ),
            404: OpenApiResponse(description=HEADER_NOT_FOUND),
        }
    ),
)
class HeaderBuilderAPIView(APIView):
    """Load and update header data for visual builder"""
    permission_classes = [IsAdminUser]

    def get(self, request, header_id):
        """Get header template with all widget placements (draft data for editing)"""
        header = get_object_or_404(HeaderTemplate, pk=header_id)

        # Always build zones from widget placements (source of truth)
        # This ensures changes made via placement API are reflected immediately
        placements = header.widget_placements.filter(
            is_active=True
        ).select_related('widget').order_by('zone', 'order')

        zones_data = {}
        for placement in placements:
            zone = placement.zone
            if zone not in zones_data:
                zones_data[zone] = []

            zones_data[zone].append({
                'id': placement.id,
                'widget_id': placement.widget.id,
                'widget_name': placement.widget.name,
                'widget_type': placement.widget.widget_type,
                'order': placement.order,
                'config': {**placement.widget.config, **placement.override_config},
                'show_on_mobile': placement.widget.show_on_mobile,
                'show_on_tablet': placement.widget.show_on_tablet,
                'show_on_desktop': placement.widget.show_on_desktop,
            })

        return Response({
            'header': {
                'id': header.id,
                'name': header.name,
                'layout_type': header.layout_type,
                'is_sticky': header.is_sticky,
                'has_top_bar': header.has_top_bar,
                'mobile_layout': header.mobile_layout,
                'mobile_menu_position': header.mobile_menu_position,
                'zones': zones_data,
                'zone_overrides': header.zone_overrides,
                'zone_layouts': header.zone_layouts,
                # Notification zone
                'enable_notification_zone': header.enable_notification_zone,
                'notification_zone_config': header.get_notification_zone_config(),
                # Draft/Publish status
                'has_unpublished_changes': header.has_unpublished_changes,
                'published_at': header.published_at.isoformat() if header.published_at else None,
            }
        })

    def post(self, request, header_id):
        """Save header template as draft"""
        header = get_object_or_404(HeaderTemplate, pk=header_id)

        # Save entire request data as draft
        draft_data = request.data

        # Also update the model fields for backwards compatibility
        for field in ['name', 'layout_type', 'is_sticky', 'has_top_bar', 'mobile_layout', 'mobile_menu_position']:
            if field in draft_data:
                setattr(header, field, draft_data[field])

        # Update zone_overrides and zone_layouts if provided
        if 'zone_overrides' in draft_data:
            header.zone_overrides = draft_data['zone_overrides']
        if 'zone_layouts' in draft_data:
            header.zone_layouts = draft_data['zone_layouts']

        # Update notification zone settings if provided
        if 'enable_notification_zone' in draft_data:
            header.enable_notification_zone = draft_data['enable_notification_zone']
        if 'notification_zone_config' in draft_data:
            header.notification_zone_config = draft_data['notification_zone_config']

        # Save as draft
        header.save_draft(draft_data)

        return Response({
            'status': 'draft_saved',
            'message': 'Draft saved successfully',
            'has_unpublished_changes': True
        })


# ============================================================
# Header Publish/Discard API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Publish header template'),
    description=_('''
    Publish the current draft of a header template, making it live on the storefront.

    Copies draft_data to published_data and updates the published_at timestamp.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            response=SuccessResponseSerializer,
            description=_('Header published successfully')
        ),
        404: OpenApiResponse(description=HEADER_NOT_FOUND),
    }
)
class HeaderPublishAPIView(APIView):
    """Publish header draft to make it live"""
    permission_classes = [IsAdminUser]

    def post(self, request, header_id):
        """Publish current draft"""
        header = get_object_or_404(HeaderTemplate, pk=header_id)
        header.publish(user=request.user)

        return Response({
            'status': 'published',
            'message': 'Header published successfully',
            'published_at': header.published_at.isoformat() if header.published_at else None,
            'has_unpublished_changes': False
        })


@extend_schema(
    tags=['Design'],
    summary=_('Discard header draft changes'),
    description=_('''
    Discard all unpublished changes and revert draft to the published state.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            description=_('Draft discarded, reverted to published state')
        ),
        404: OpenApiResponse(description=HEADER_NOT_FOUND),
    }
)
class HeaderDiscardAPIView(APIView):
    """Discard header draft and revert to published state"""
    permission_classes = [IsAdminUser]

    def post(self, request, header_id):
        """Discard draft and revert to published"""
        header = get_object_or_404(HeaderTemplate, pk=header_id)
        header.discard_draft()

        return Response({
            'status': 'discarded',
            'message': 'Draft discarded, reverted to published state',
            'draft_data': header.draft_data,
            'has_unpublished_changes': False
        })


# ============================================================
# Footer Builder API
# ============================================================

@extend_schema_view(
    get=extend_schema(
        tags=['Design'],
        summary=_('Get footer template for builder'),
        description=_('''
        Load a footer template with all widget placements for the visual builder.

        Returns the footer configuration including zones and all placed widgets
        with their merged configurations (base config + overrides).

        **Authentication:** Admin user required
        '''),
        responses={
            200: OpenApiResponse(
                response=FooterBuilderResponseSerializer,
                description=_('Footer template data with widget placements')
            ),
            404: OpenApiResponse(description=FOOTER_NOT_FOUND),
        }
    ),
    post=extend_schema(
        tags=['Design'],
        summary=_('Update footer template'),
        description=_('''
        Update footer template properties.

        Supports partial updates - only provided fields will be modified.

        **Authentication:** Admin user required
        '''),
        request=FooterBuilderUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_('Footer updated successfully')
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_('Invalid request data')
            ),
            404: OpenApiResponse(description=FOOTER_NOT_FOUND),
        }
    ),
)
class FooterBuilderAPIView(APIView):
    """Load and update footer data for visual builder"""
    permission_classes = [IsAdminUser]

    def get(self, request, footer_id):
        """Get footer template with all widget placements (draft data for editing)"""
        footer = get_object_or_404(FooterTemplate, pk=footer_id)

        # Always build zones from widget placements (source of truth)
        # This ensures changes made via placement API are reflected immediately
        placements = footer.widget_placements.filter(
            is_active=True
        ).select_related('widget').order_by('zone', 'order')

        zones_data = {}
        for placement in placements:
            zone = placement.zone
            if zone not in zones_data:
                zones_data[zone] = []

            zones_data[zone].append({
                'id': placement.id,
                'widget_id': placement.widget.id,
                'widget_name': placement.widget.name,
                'widget_type': placement.widget.widget_type,
                'order': placement.order,
                'config': {**placement.widget.config, **placement.override_config},
                'show_on_mobile': placement.widget.show_on_mobile,
                'show_on_tablet': placement.widget.show_on_tablet,
                'show_on_desktop': placement.widget.show_on_desktop,
            })

        return Response({
            'footer': {
                'id': footer.id,
                'name': footer.name,
                'layout_type': footer.layout_type,
                'column_count': footer.column_count,
                'has_bottom_bar': footer.has_bottom_bar,
                'background_color': footer.background_color,
                'text_color': footer.text_color,
                'zones': zones_data,
                'zone_overrides': getattr(footer, 'zone_overrides', {}),
                'zone_layouts': getattr(footer, 'zone_layouts', {}),
                # Draft/Publish status
                'has_unpublished_changes': footer.has_unpublished_changes,
                'published_at': footer.published_at.isoformat() if footer.published_at else None,
            }
        })

    def post(self, request, footer_id):
        """Save footer template as draft"""
        footer = get_object_or_404(FooterTemplate, pk=footer_id)

        # Save entire request data as draft
        draft_data = request.data

        # Also update the model fields for backwards compatibility
        for field in ['name', 'layout_type', 'column_count', 'has_bottom_bar',
                      'background_color', 'text_color']:
            if field in draft_data:
                setattr(footer, field, draft_data[field])

        # Save as draft
        footer.save_draft(draft_data)

        return Response({
            'status': 'draft_saved',
            'message': 'Draft saved successfully',
            'has_unpublished_changes': True
        })


# ============================================================
# Footer Publish/Discard API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Publish footer template'),
    description=_('''
    Publish the current draft of a footer template, making it live on the storefront.

    Copies draft_data to published_data and updates the published_at timestamp.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            response=SuccessResponseSerializer,
            description=_('Footer published successfully')
        ),
        404: OpenApiResponse(description=FOOTER_NOT_FOUND),
    }
)
class FooterPublishAPIView(APIView):
    """Publish footer draft to make it live"""
    permission_classes = [IsAdminUser]

    def post(self, request, footer_id):
        """Publish current draft"""
        footer = get_object_or_404(FooterTemplate, pk=footer_id)
        footer.publish(user=request.user)

        return Response({
            'status': 'published',
            'message': 'Footer published successfully',
            'published_at': footer.published_at.isoformat() if footer.published_at else None,
            'has_unpublished_changes': False
        })


@extend_schema(
    tags=['Design'],
    summary=_('Discard footer draft changes'),
    description=_('''
    Discard all unpublished changes and revert draft to the published state.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            description=_('Draft discarded, reverted to published state')
        ),
        404: OpenApiResponse(description=FOOTER_NOT_FOUND),
    }
)
class FooterDiscardAPIView(APIView):
    """Discard footer draft and revert to published state"""
    permission_classes = [IsAdminUser]

    def post(self, request, footer_id):
        """Discard draft and revert to published"""
        footer = get_object_or_404(FooterTemplate, pk=footer_id)
        footer.discard_draft()

        return Response({
            'status': 'discarded',
            'message': 'Draft discarded, reverted to published state',
            'draft_data': footer.draft_data,
            'has_unpublished_changes': False
        })


# ============================================================
# Widget Placement API
# ============================================================

@extend_schema_view(
    post=extend_schema(
        tags=['Design'],
        summary=_('Create widget placement'),
        description=_('''
        Add a widget to a header or footer zone.

        Must specify either `header_id` or `footer_id` (not both).

        **Authentication:** Admin user required
        '''),
        request=WidgetPlacementCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=WidgetPlacementSerializer,
                description=_('Widget placement created')
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_('Invalid request data')
            ),
        }
    ),
    put=extend_schema(
        tags=['Design'],
        summary=_('Update widget placement'),
        description=_('''
        Update an existing widget placement.

        Supports partial updates for zone, order, is_active, and override_config.

        **Authentication:** Admin user required
        '''),
        request=WidgetPlacementUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_('Placement updated')
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_('Invalid request data')
            ),
            404: OpenApiResponse(description=_('Placement not found')),
        }
    ),
    delete=extend_schema(
        tags=['Design'],
        summary=_('Delete widget placement'),
        description=_('''
        Remove a widget from its zone.

        **Authentication:** Admin user required
        '''),
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_('Placement deleted')
            ),
            404: OpenApiResponse(description=_('Placement not found')),
        }
    ),
)
class WidgetPlacementAPIView(APIView):
    """CRUD operations for widget placements"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Create a new widget placement"""
        serializer = WidgetPlacementCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        widget = get_object_or_404(Widget, pk=data['widget_id'])

        placement = WidgetPlacement(
            widget=widget,
            zone=data['zone'],
            order=data.get('order', 0),
            is_active=data.get('is_active', True),
            override_config=data.get('override_config', {}),
        )

        # Set header or footer
        if data.get('header_id'):
            placement.header_id = data['header_id']
        else:
            placement.footer_id = data['footer_id']

        placement.save()

        return Response({
            'placement': {
                'id': placement.id,
                'widget_id': placement.widget.id,
                'widget_name': placement.widget.name,
                'widget_type': placement.widget.widget_type,
                'zone': placement.zone,
                'order': placement.order,
            }
        }, status=status.HTTP_201_CREATED)

    def put(self, request, placement_id=None):
        """Update widget placement"""
        if not placement_id:
            return Response(
                {'error': 'placement_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        placement = get_object_or_404(WidgetPlacement, pk=placement_id)
        serializer = WidgetPlacementUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        for field in ['zone', 'order', 'is_active', 'override_config']:
            if field in data:
                setattr(placement, field, data[field])

        placement.save()

        # Update widget-level visibility fields if provided
        widget_visibility_changed = False
        for field in ['show_on_mobile', 'show_on_tablet', 'show_on_desktop']:
            if field in request.data:
                setattr(placement.widget, field, request.data[field])
                widget_visibility_changed = True
        if widget_visibility_changed:
            placement.widget.save(update_fields=['show_on_mobile', 'show_on_tablet', 'show_on_desktop'])

        return Response({'message': 'Placement updated'})

    def delete(self, request, placement_id=None):
        """Delete widget placement"""
        if not placement_id:
            return Response(
                {'error': 'placement_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        placement = get_object_or_404(WidgetPlacement, pk=placement_id)
        placement.delete()

        return Response({'message': 'Placement deleted'})


# ============================================================
# Reorder Placements API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Reorder widget placements'),
    description=_('''
    Update the order of multiple widget placements within a zone.

    Accepts a list of placement IDs with their new order values.
    All updates are performed atomically in a single transaction.

    **Authentication:** Admin user required
    '''),
    request=ReorderPlacementsSerializer,
    responses={
        200: OpenApiResponse(
            response=SuccessResponseSerializer,
            description=_('Placements reordered')
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=_('Invalid request data')
        ),
    }
)
class ReorderPlacementsAPIView(APIView):
    """Reorder widget placements within a zone"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Update order of multiple placements"""
        serializer = ReorderPlacementsSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        placement_orders = serializer.validated_data.get('placements', [])

        with transaction.atomic():
            for item in placement_orders:
                WidgetPlacement.objects.filter(
                    pk=item['id']
                ).update(order=item['order'])

        return Response({'message': 'Placements reordered'})


# ============================================================
# Widget Library API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Get widget library'),
    description=_('''
    Get all available widgets for the builder's widget library panel.

    Returns widgets grouped by type (logo, menu, search, cart, etc.).
    Each widget includes its base configuration and visibility settings.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            description=_('Widgets grouped by type')
        ),
    }
)
class WidgetLibraryAPIView(APIView):
    """Get available widgets for library panel"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Return all active widgets grouped by type"""
        widgets = Widget.objects.filter(is_active=True).order_by('widget_type', 'name')

        # Group by widget type
        grouped = {}
        for widget in widgets:
            widget_type = widget.widget_type
            if widget_type not in grouped:
                grouped[widget_type] = []

            grouped[widget_type].append({
                'id': widget.id,
                'name': widget.name,
                'type': widget.widget_type,
                'type_display': widget.get_widget_type_display(),
                'config': widget.config,
                'show_on_mobile': widget.show_on_mobile,
                'show_on_tablet': widget.show_on_tablet,
                'show_on_desktop': widget.show_on_desktop,
            })

        return Response({'widgets': grouped})


# ============================================================
# Widget Schemas API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Get widget property schemas'),
    description=_('''
    Get JSON schemas defining widget property panel configuration.

    Schemas are loaded from JSON files in `design/templates/design/widgets/`.
    Each schema defines the property groups and fields for a widget type's
    configuration panel in the visual builder.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            response=WidgetSchemasResponseSerializer,
            description=_('Widget schemas keyed by type')
        ),
    }
)
class WidgetSchemasAPIView(APIView):
    """Serve widget property schemas from JSON files"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Return all widget schemas as JSON"""
        schemas = {}
        widgets_dir = Path(__file__).parent / 'templates' / 'design' / 'widgets'

        for json_file in widgets_dir.glob('*.json'):
            try:
                widget_type = json_file.stem  # e.g., "logo" from "logo.json"
                with open(json_file, 'r', encoding='utf-8') as f:
                    schemas[widget_type] = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading widget schema {json_file}: {e}")
                continue

        return Response({'schemas': schemas})


# ============================================================
# Preset Gallery API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Get preset templates'),
    description=_('''
    Get available preset templates for headers or footers.

    Presets are pre-configured templates that can be cloned to create
    new headers/footers with predefined layouts and widget configurations.

    **Authentication:** Admin user required
    '''),
    parameters=[
        OpenApiParameter(
            name='template_type',
            location=OpenApiParameter.PATH,
            description=_('Type of template: "header" or "footer"'),
            required=True,
            type=str,
            enum=['header', 'footer']
        )
    ],
    responses={
        200: OpenApiResponse(description=_('List of preset templates')),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=_('Invalid template_type')
        ),
    }
)
class PresetGalleryAPIView(APIView):
    """Get preset header/footer templates"""
    permission_classes = [IsAdminUser]

    def get(self, request, template_type):
        """Get presets for header or footer"""
        if template_type == 'header':
            presets = HeaderTemplate.objects.filter(is_preset=True, is_active=True)
            serializer = HeaderPresetSerializer(presets, many=True)
        elif template_type == 'footer':
            presets = FooterTemplate.objects.filter(is_preset=True, is_active=True)
            serializer = FooterPresetSerializer(presets, many=True)
        else:
            return Response(
                {'error': 'Invalid template_type. Must be "header" or "footer"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'presets': serializer.data})


# ============================================================
# Clone Preset API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Clone a preset template'),
    description=_('''
    Create a new header or footer by cloning a preset template.

    Copies all widget placements and configurations from the preset.
    The new template will not be marked as default or preset.

    **Authentication:** Admin user required
    '''),
    parameters=[
        OpenApiParameter(
            name='template_type',
            location=OpenApiParameter.PATH,
            description=_('Type of template: "header" or "footer"'),
            required=True,
            type=str,
            enum=['header', 'footer']
        ),
        OpenApiParameter(
            name='preset_id',
            location=OpenApiParameter.PATH,
            description=_('ID of the preset to clone'),
            required=True,
            type=int
        )
    ],
    request=ClonePresetSerializer,
    responses={
        201: OpenApiResponse(
            response=ClonePresetResponseSerializer,
            description=_('New template created from preset')
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=_('Invalid request or clone failed')
        ),
        404: OpenApiResponse(description=_('Preset not found')),
    }
)
class ClonePresetAPIView(APIView):
    """Clone a preset template"""
    permission_classes = [IsAdminUser]

    def post(self, request, template_type, preset_id):
        """Clone preset and return new template ID"""
        serializer = ClonePresetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_name = serializer.validated_data.get('name', 'Copy of Preset')

        if template_type == 'header':
            return self._clone_header(request, preset_id, new_name)
        elif template_type == 'footer':
            return self._clone_footer(request, preset_id, new_name)
        else:
            return Response(
                {'error': 'Invalid template_type. Must be "header" or "footer"'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _clone_header(self, request, preset_id, new_name):
        """Clone a header preset"""
        preset = get_object_or_404(HeaderTemplate, pk=preset_id, is_preset=True)

        # Generate unique slug
        base_slug = slugify(new_name) or 'header'
        unique_slug = f"{base_slug}-{int(time.time())}"

        # Clone the header
        new_header = HeaderTemplate.objects.create(
            name=new_name,
            slug=unique_slug,
            description=preset.description,
            layout_type=preset.layout_type,
            is_sticky=preset.is_sticky,
            sticky_offset=preset.sticky_offset,
            has_top_bar=preset.has_top_bar,
            top_bar_content=preset.top_bar_content,
            zones=preset.zones,
            zone_overrides=preset.zone_overrides,
            zone_layouts=preset.zone_layouts,
            mobile_layout=preset.mobile_layout,
            mobile_menu_position=preset.mobile_menu_position,
            custom_css=preset.custom_css,
            css_classes=preset.css_classes,
            enable_notification_zone=preset.enable_notification_zone,
            notification_zone_config=preset.notification_zone_config,
            is_active=True,
            is_preset=False,
            created_by=request.user,
        )

        # Clone widget placements
        for placement in preset.widget_placements.all():
            WidgetPlacement.objects.create(
                widget=placement.widget,
                header=new_header,
                zone=placement.zone,
                order=placement.order,
                override_config=placement.override_config,
                is_active=placement.is_active,
            )

        return Response(
            {'id': new_header.id, 'name': new_header.name},
            status=status.HTTP_201_CREATED
        )

    def _clone_footer(self, request, preset_id, new_name):
        """Clone a footer preset"""
        preset = get_object_or_404(FooterTemplate, pk=preset_id, is_preset=True)

        # Generate unique slug
        base_slug = slugify(new_name) or 'footer'
        unique_slug = f"{base_slug}-{int(time.time())}"

        # Clone the footer
        new_footer = FooterTemplate.objects.create(
            name=new_name,
            slug=unique_slug,
            description=preset.description,
            layout_type=preset.layout_type,
            column_count=preset.column_count,
            zones=preset.zones,
            has_bottom_bar=preset.has_bottom_bar,
            bottom_bar_content=preset.bottom_bar_content,
            custom_css=preset.custom_css,
            css_classes=preset.css_classes,
            background_color=preset.background_color,
            text_color=preset.text_color,
            is_active=True,
            is_preset=False,
            created_by=request.user,
        )

        # Clone widget placements
        for placement in preset.widget_placements.all():
            WidgetPlacement.objects.create(
                widget=placement.widget,
                footer=new_footer,
                zone=placement.zone,
                order=placement.order,
                override_config=placement.override_config,
                is_active=placement.is_active,
            )

        return Response(
            {'id': new_footer.id, 'name': new_footer.name},
            status=status.HTTP_201_CREATED
        )


# ============================================================
# Menu List API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('List available menus'),
    description=_('''
    Get all active menus for widget configuration dropdowns.

    Used by the menu widget to select which menu to display.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            response=MenuListSerializer(many=True),
            description=_('List of active menus')
        ),
    }
)
class MenuListAPIView(APIView):
    """List all menus for widget configuration dropdowns"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Get list of all menus"""
        menus = Menu.objects.filter(is_active=True)
        serializer = MenuListSerializer(menus, many=True)
        return Response(serializer.data)


# ============================================================
# Header Management APIs
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Duplicate header template'),
    description=_('''
    Create a copy of an existing header template.

    Copies all settings and widget placements. The new header will not
    be marked as default or preset.

    **Authentication:** Admin user required
    '''),
    request=HeaderDuplicateSerializer,
    responses={
        201: OpenApiResponse(
            response=HeaderDuplicateResponseSerializer,
            description=_('Header duplicated successfully')
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=_('Duplication failed')
        ),
        404: OpenApiResponse(description=HEADER_NOT_FOUND),
    }
)
class DuplicateHeaderAPIView(APIView):
    """Duplicate a header template with all widget placements"""
    permission_classes = [IsAdminUser]

    def post(self, request, header_id):
        """Duplicate header and return new header ID"""
        header = get_object_or_404(HeaderTemplate, pk=header_id)

        serializer = HeaderDuplicateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_name = serializer.validated_data.get('name', f'Copy of {header.name}')

        # Generate unique slug
        base_slug = slugify(new_name) or 'header'
        unique_slug = f"{base_slug}-{int(time.time())}"

        # Clone the header
        new_header = HeaderTemplate.objects.create(
            name=new_name,
            slug=unique_slug,
            description=header.description,
            layout_type=header.layout_type,
            is_sticky=header.is_sticky,
            sticky_offset=header.sticky_offset,
            has_top_bar=header.has_top_bar,
            top_bar_content=header.top_bar_content,
            zones=header.zones,
            zone_overrides=header.zone_overrides,
            zone_layouts=header.zone_layouts,
            mobile_layout=header.mobile_layout,
            mobile_menu_position=header.mobile_menu_position,
            custom_css=header.custom_css,
            css_classes=header.css_classes,
            enable_notification_zone=header.enable_notification_zone,
            notification_zone_config=header.notification_zone_config,
            is_active=True,
            is_default=False,
            is_preset=False,
            created_by=request.user,
        )

        # Clone widget placements
        for placement in header.widget_placements.all():
            WidgetPlacement.objects.create(
                widget=placement.widget,
                header=new_header,
                zone=placement.zone,
                order=placement.order,
                override_config=placement.override_config,
                is_active=placement.is_active,
            )

        return Response({
            'id': new_header.id,
            'name': new_header.name,
            'message': f'Header "{header.name}" duplicated successfully as "{new_header.name}"'
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Design'],
    summary=_('Delete header template'),
    description=_('''
    Delete a header template after validation checks.

    Will fail if:
    - The header is the site default
    - The header is in use by pages

    Widget placements are deleted via cascade.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            response=SuccessResponseSerializer,
            description=_('Header deleted successfully')
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=_('Cannot delete (default or in use)')
        ),
        404: OpenApiResponse(description=HEADER_NOT_FOUND),
    }
)
class DeleteHeaderAPIView(APIView):
    """Delete a header template with validation checks"""
    permission_classes = [IsAdminUser]

    def delete(self, request, header_id):
        """Delete header after validation"""
        header = get_object_or_404(HeaderTemplate, pk=header_id)

        # Check if this is the default header
        if header.is_default:
            return Response({
                'error': 'cannot_delete_default',
                'message': 'This is the default header. Please set another header as default before deleting this one.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if any pages are using this header
        pages_using = list(header.pages.values_list('title', flat=True)[:10])
        page_count = header.pages.count()

        if page_count > 0:
            if page_count > 10:
                pages_using.append(f'... and {page_count - 10} more')

            return Response({
                'error': 'header_in_use',
                'message': f'This header is used by {page_count} page(s). Please assign a different header to these pages before deleting.',
                'pages': pages_using
            }, status=status.HTTP_400_BAD_REQUEST)

        # Safe to delete
        header_name = header.name
        header.delete()

        return Response({
            'message': f'Header "{header_name}" has been deleted successfully.'
        })


@extend_schema(
    tags=['Design'],
    summary=_('Set default header'),
    description=_('''
    Set a header template as the site default.

    The previously default header will be automatically unset.

    **Authentication:** Admin user required
    '''),
    responses={
        200: OpenApiResponse(
            response=SuccessResponseSerializer,
            description=_('Header set as default')
        ),
        404: OpenApiResponse(description=HEADER_NOT_FOUND),
    }
)
class SetDefaultHeaderAPIView(APIView):
    """Set a header template as the site default"""
    permission_classes = [IsAdminUser]

    def post(self, request, header_id):
        """Set header as default"""
        header = get_object_or_404(HeaderTemplate, pk=header_id)

        # Check if already default
        if header.is_default:
            return Response({
                'message': f'"{header.name}" is already the default header.'
            })

        # Set as default (model's save() will clear other defaults)
        header.is_default = True
        header.save()

        return Response({
            'message': f'"{header.name}" is now the default header for your site.'
        })


# ============================================================
# Site Logo API
# ============================================================

@extend_schema_view(
    get=extend_schema(
        tags=['Design'],
        summary=_('Get site logo for builder'),
        description=_('''
        Get the current site logo URL and metadata for the header/footer builder.

        Used by the logo widget to display the site logo when "Use Site Logo" is enabled.

        **Authentication:** Admin user required
        '''),
        responses={
            200: OpenApiResponse(
                description=_('Site logo data'),
                response={
                    'type': 'object',
                    'properties': {
                        'has_logo': {'type': 'boolean'},
                        'logo_url': {'type': 'string', 'nullable': True},
                        'logo_url_footer': {'type': 'string', 'nullable': True},
                        'logo_url_original': {'type': 'string', 'nullable': True},
                        'is_svg': {'type': 'boolean'},
                        'asset_id': {'type': 'string', 'nullable': True},
                    },
                }
            ),
        }
    ),
    post=extend_schema(
        tags=['Design'],
        summary=_('Update site logo from widget'),
        description=_('''
        Update the site logo from a logo widget upload.

        When a merchant uploads a new logo in the header/footer builder logo widget,
        this endpoint allows syncing that logo to the site settings.

        **Authentication:** Admin user required
        '''),
        request={
            'type': 'object',
            'properties': {
                'asset_id': {'type': 'string', 'description': 'Media asset UUID'},
            },
            'required': ['asset_id'],
        },
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description=_('Site logo updated')
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description=_('Missing asset_id')
            ),
            404: OpenApiResponse(description=_('Asset or settings not found')),
        }
    ),
)
class SiteLogoAPIView(APIView):
    """API for site logo operations in the header/footer builder"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Get current site logo URL and metadata"""
        from core.models import SiteSettings
        settings = SiteSettings.get_settings()

        if not settings or not settings.site_logo:
            return Response({'logo_url': None, 'has_logo': False})

        return Response({
            'has_logo': True,
            'logo_url': settings.get_site_logo_url('header'),
            'logo_url_footer': settings.get_site_logo_url('footer'),
            'logo_url_original': settings.get_site_logo_url('original'),
            'is_svg': settings.site_logo.mime_type == 'image/svg+xml',
            'asset_id': str(settings.site_logo.id),
        })

    def post(self, request):
        """Update site logo from widget (when custom logo is uploaded)"""
        from core.models import SiteSettings
        from media_library.models import MediaAsset

        asset_id = request.data.get('asset_id')
        if not asset_id:
            return Response({'error': 'asset_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            asset = MediaAsset.objects.get(id=asset_id)
        except MediaAsset.DoesNotExist:
            return Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)

        settings = SiteSettings.get_settings()
        if not settings:
            return Response({'error': 'Site settings not found'}, status=status.HTTP_404_NOT_FOUND)

        settings.site_logo = asset
        settings.save()

        return Response({
            'success': True,
            'logo_url': settings.get_site_logo_url('header'),
            'message': 'Site logo updated successfully',
        })


# ============================================================
# Widget Preview API
# ============================================================

@extend_schema(
    tags=['Design'],
    summary=_('Render widget preview'),
    description=_('''
    Render a widget with given configuration for real-time preview in the builder.

    Uses the same Django templates as the storefront to ensure visual consistency.
    This ensures the preview always matches the actual appearance.

    **Authentication:** Admin user required
    '''),
    request={
        'type': 'object',
        'properties': {
            'widget_type': {'type': 'string', 'description': 'Widget type (menu, logo, search, etc.)'},
            'config': {'type': 'object', 'description': 'Widget configuration'},
        },
        'required': ['widget_type'],
    },
    responses={
        200: OpenApiResponse(
            description=_('Rendered widget HTML'),
            response={
                'type': 'object',
                'properties': {
                    'html': {'type': 'string', 'description': 'Rendered HTML'},
                },
            }
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=_('Missing widget_type parameter')
        ),
    }
)
class WidgetPreviewAPIView(APIView):
    """Render widget HTML for builder preview using actual templates"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Render widget with given configuration"""
        from .widget_preview_service import WidgetPreviewRenderer

        widget_type = request.data.get('widget_type')
        config = request.data.get('config', {})

        if not widget_type:
            return Response(
                {'error': 'widget_type is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        renderer = WidgetPreviewRenderer()
        html = renderer.render(widget_type, config, request)

        return Response({'html': html})
