import json
import base64
import logging
from io import BytesIO

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from catalog.models import Product, ConfigurationSlot
from core.models import SiteSettings
from media_library.models import MediaAsset

from .models import SceneConfig, NodeMapping, GeometryAsset, TextureAsset
from .services.glb_parser import parse_glb_from_media_asset

logger = logging.getLogger(__name__)


@staff_member_required
def scene_setup(request, product_id):
    """Main 3D scene manager page."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')
    site_settings = SiteSettings.objects.first()

    # Get or create SceneConfig
    scene, created = SceneConfig.objects.get_or_create(product=product)

    # Auto-upgrade stale node_tree: re-parse GLB if version < current parser version
    CURRENT_NODE_TREE_VERSION = 2
    if (scene.base_model
            and scene.base_model.original_file
            and scene.node_tree.get('version', 0) < CURRENT_NODE_TREE_VERSION):
        try:
            updated_tree = parse_glb_from_media_asset(scene.base_model)
            if 'error' not in updated_tree:
                scene.node_tree = updated_tree
                scene.save(update_fields=['node_tree', 'updated_at'])
                logger.info(
                    "Auto-upgraded node_tree for scene %d (product: %s) to version %d",
                    scene.pk, product.name, CURRENT_NODE_TREE_VERSION,
                )
        except Exception as e:
            logger.warning("Failed to auto-upgrade node_tree for scene %d: %s", scene.pk, e)

    # Load slots with options for the mapping UI
    slots = product.configuration_slots.prefetch_related(
        'options__option_product'
    ).order_by('sort_order')

    # Load existing mappings
    mappings = scene.mappings.select_related('slot_option__slot', 'slot_option__option_product').order_by('sort_order')

    # Load geometry assets
    geometry_assets = scene.geometry_assets.select_related('media_asset').all()

    # Load texture assets
    texture_assets = scene.textures.select_related('media_asset').all()

    # Serialize data for JS
    slots_data = []
    for slot in slots:
        options_data = []
        for opt in slot.options.order_by('sort_order'):
            options_data.append({
                'id': opt.id,
                'product_name': str(opt.option_product.name),
                'variant_name': str(opt.option_variant.name) if opt.option_variant else None,
            })
        slots_data.append({
            'id': slot.id,
            'name': str(slot.name),
            'slug': slot.slug,
            'icon': slot.icon or '',
            'options': options_data,
        })

    mappings_data = []
    for m in mappings:
        mappings_data.append({
            'id': m.id,
            'slot_option_id': m.slot_option_id,
            'slot_name': str(m.slot_option.slot.name),
            'option_name': str(m.slot_option.option_product.name),
            'action_type': m.action_type,
            'target_node': m.target_node,
            'action_data': m.action_data,
            'sort_order': m.sort_order,
        })

    geometry_data = []
    for ga in geometry_assets:
        geometry_data.append({
            'id': ga.id,
            'label': ga.label,
            'media_asset_id': str(ga.media_asset_id),
            'media_asset_title': ga.media_asset.title if ga.media_asset else '',
            'media_url': ga.media_asset.original_file.url if ga.media_asset and ga.media_asset.original_file else '',
            'target_node': ga.target_node,
            'node_data': ga.node_data,
        })

    texture_data = []
    for ta in texture_assets:
        texture_data.append({
            'id': ta.id,
            'label': ta.label,
            'media_asset_id': str(ta.media_asset_id),
            'media_asset_title': ta.media_asset.title if ta.media_asset else '',
            'media_url': ta.media_asset.original_file.url if ta.media_asset and ta.media_asset.original_file else '',
            'texture_type': ta.texture_type,
        })

    scene_data = {
        'base_model_url': scene.base_model.original_file.url if scene.base_model and scene.base_model.original_file else None,
        'base_model_id': str(scene.base_model_id) if scene.base_model_id else None,
        'base_model_title': scene.base_model.title if scene.base_model else '',
        'camera_orbit': scene.camera_orbit,
        'camera_target': scene.camera_target,
        'exposure': scene.exposure,
        'shadow_intensity': scene.shadow_intensity,
        'shadow_softness': scene.shadow_softness,
        'tone_mapping': scene.tone_mapping,
        'bloom_strength': scene.bloom_strength,
        'auto_rotate': scene.auto_rotate,
        'ar_enabled': scene.ar_enabled,
        'background_color': scene.background_color,
        'is_enabled': scene.is_enabled,
        'node_tree': scene.node_tree,
        'environment_image_id': str(scene.environment_image_id) if scene.environment_image_id else None,
        'environment_image_title': scene.environment_image.title if scene.environment_image else '',
        'environment_url': scene.environment_image.original_file.url if scene.environment_image and scene.environment_image.original_file else None,
    }

    context = {
        'product': product,
        'scene': scene,
        'site_settings': site_settings,
        'slots_json': json.dumps(slots_data),
        'mappings_json': json.dumps(mappings_data),
        'geometry_json': json.dumps(geometry_data),
        'texture_json': json.dumps(texture_data),
        'scene_json': json.dumps(scene_data),
    }
    return render(request, 'admin/configurator_3d/scene_setup.html', context)


@staff_member_required
@require_POST
def parse_glb_view(request, product_id):
    """AJAX: Parse a GLB file and return the node tree."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')

    try:
        data = json.loads(request.body)
        media_asset_id = data.get('media_asset_id')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not media_asset_id:
        return JsonResponse({'error': 'media_asset_id required'}, status=400)

    try:
        media_asset = MediaAsset.objects.get(pk=media_asset_id)
    except MediaAsset.DoesNotExist:
        return JsonResponse({'error': 'Media asset not found'}, status=404)

    node_tree = parse_glb_from_media_asset(media_asset)

    # Save to SceneConfig
    scene, _created = SceneConfig.objects.get_or_create(product=product)
    scene.base_model = media_asset
    scene.node_tree = node_tree
    scene.save()

    return JsonResponse({'success': True, 'node_tree': node_tree})


@staff_member_required
@require_POST
def save_scene_config(request, product_id):
    """AJAX: Save scene viewer settings."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')
    scene, _created = SceneConfig.objects.get_or_create(product=product)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Update fields
    for field in ['camera_orbit', 'camera_target', 'background_color', 'tone_mapping']:
        if field in data:
            setattr(scene, field, data[field])

    for field in ['exposure', 'shadow_intensity', 'shadow_softness', 'bloom_strength']:
        if field in data:
            setattr(scene, field, float(data[field]))

    for field in ['auto_rotate', 'ar_enabled', 'is_enabled']:
        if field in data:
            setattr(scene, field, bool(data[field]))

    if 'environment_image_id' in data:
        env_id = data['environment_image_id']
        if env_id:
            try:
                scene.environment_image = MediaAsset.objects.get(pk=env_id)
            except MediaAsset.DoesNotExist:
                pass
        else:
            scene.environment_image = None

    scene.save()
    return JsonResponse({'success': True})


@staff_member_required
def list_mappings(request, product_id):
    """AJAX: List all mappings for a product's scene."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')
    try:
        scene = product.scene_3d
    except SceneConfig.DoesNotExist:
        return JsonResponse({'mappings': []})

    mappings = scene.mappings.select_related(
        'slot_option__slot', 'slot_option__option_product'
    ).order_by('sort_order')

    data = []
    for m in mappings:
        data.append({
            'id': m.id,
            'slot_option_id': m.slot_option_id,
            'slot_name': str(m.slot_option.slot.name),
            'option_name': str(m.slot_option.option_product.name),
            'action_type': m.action_type,
            'target_node': m.target_node,
            'action_data': m.action_data,
            'sort_order': m.sort_order,
        })

    return JsonResponse({'mappings': data})


@staff_member_required
@require_POST
def save_mapping(request, product_id):
    """AJAX: Create or update a node mapping."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')
    scene, _created = SceneConfig.objects.get_or_create(product=product)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    mapping_id = data.get('id')
    slot_option_id = data.get('slot_option_id')
    action_type = data.get('action_type')
    target_node = data.get('target_node')
    action_data = data.get('action_data', {})
    sort_order = data.get('sort_order', 0)

    if not all([slot_option_id, action_type, target_node]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if action_type not in dict(NodeMapping.ACTION_TYPES):
        return JsonResponse({'error': 'Invalid action_type'}, status=400)

    if mapping_id:
        try:
            mapping = NodeMapping.objects.get(pk=mapping_id, scene_config=scene)
        except NodeMapping.DoesNotExist:
            return JsonResponse({'error': 'Mapping not found'}, status=404)
        mapping.slot_option_id = slot_option_id
        mapping.action_type = action_type
        mapping.target_node = target_node
        mapping.action_data = action_data
        mapping.sort_order = sort_order
        mapping.save()
    else:
        mapping = NodeMapping.objects.create(
            scene_config=scene,
            slot_option_id=slot_option_id,
            action_type=action_type,
            target_node=target_node,
            action_data=action_data,
            sort_order=sort_order,
        )

    return JsonResponse({
        'success': True,
        'mapping': {
            'id': mapping.id,
            'slot_option_id': mapping.slot_option_id,
            'action_type': mapping.action_type,
            'target_node': mapping.target_node,
            'action_data': mapping.action_data,
            'sort_order': mapping.sort_order,
        }
    })


@staff_member_required
@require_POST
def delete_mapping(request, product_id, mapping_id):
    """AJAX: Delete a node mapping (scoped to product)."""
    mapping = get_object_or_404(
        NodeMapping,
        pk=mapping_id,
        scene_config__product_id=product_id,
        scene_config__product__product_type='configurable',
    )
    mapping.delete()
    return JsonResponse({'success': True})


@staff_member_required
@require_POST
def save_geometry_asset(request, product_id):
    """AJAX: Create or update a geometry asset."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')
    scene, _created = SceneConfig.objects.get_or_create(product=product)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    asset_id = data.get('id')
    label = data.get('label', '')
    media_asset_id = data.get('media_asset_id')
    target_node = data.get('target_node', '')

    if not media_asset_id:
        return JsonResponse({'error': 'media_asset_id required'}, status=400)

    try:
        media_asset = MediaAsset.objects.get(pk=media_asset_id)
    except MediaAsset.DoesNotExist:
        return JsonResponse({'error': 'Media asset not found'}, status=404)

    # Parse GLB to get node data
    node_data = parse_glb_from_media_asset(media_asset)

    if asset_id:
        try:
            ga = GeometryAsset.objects.get(pk=asset_id, scene_config=scene)
        except GeometryAsset.DoesNotExist:
            return JsonResponse({'error': 'Geometry asset not found'}, status=404)
        ga.label = label
        ga.media_asset = media_asset
        ga.target_node = target_node
        ga.node_data = node_data
        ga.save()
    else:
        ga = GeometryAsset.objects.create(
            scene_config=scene,
            label=label,
            media_asset=media_asset,
            target_node=target_node,
            node_data=node_data,
        )

    return JsonResponse({
        'success': True,
        'geometry_asset': {
            'id': ga.id,
            'label': ga.label,
            'media_asset_id': str(ga.media_asset_id),
            'media_asset_title': ga.media_asset.title,
            'media_url': ga.media_asset.original_file.url if ga.media_asset.original_file else '',
            'target_node': ga.target_node,
            'node_data': ga.node_data,
        }
    })


@staff_member_required
@require_POST
def delete_geometry_asset(request, product_id, asset_id):
    """AJAX: Delete a geometry asset (scoped to product)."""
    ga = get_object_or_404(
        GeometryAsset,
        pk=asset_id,
        scene_config__product_id=product_id,
        scene_config__product__product_type='configurable',
    )
    ga.delete()
    return JsonResponse({'success': True})


@staff_member_required
def list_textures(request, product_id):
    """AJAX: List all texture assets for a product's scene."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')
    try:
        scene = product.scene_3d
    except SceneConfig.DoesNotExist:
        return JsonResponse({'textures': []})

    textures = scene.textures.select_related('media_asset').all()

    data = []
    for ta in textures:
        data.append({
            'id': ta.id,
            'label': ta.label,
            'media_asset_id': str(ta.media_asset_id),
            'media_asset_title': ta.media_asset.title if ta.media_asset else '',
            'media_url': ta.media_asset.original_file.url if ta.media_asset and ta.media_asset.original_file else '',
            'texture_type': ta.texture_type,
            'texture_type_display': ta.get_texture_type_display(),
        })

    return JsonResponse({'textures': data})


@staff_member_required
@require_POST
def save_texture_asset(request, product_id):
    """AJAX: Create or update a texture asset."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')
    scene, _created = SceneConfig.objects.get_or_create(product=product)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    asset_id = data.get('id')
    label = data.get('label', '')
    media_asset_id = data.get('media_asset_id')
    texture_type = data.get('texture_type', 'base_color')

    if not media_asset_id:
        return JsonResponse({'error': 'media_asset_id required'}, status=400)

    if texture_type not in dict(TextureAsset.TEXTURE_TYPES):
        return JsonResponse({'error': 'Invalid texture_type'}, status=400)

    try:
        media_asset = MediaAsset.objects.get(pk=media_asset_id)
    except MediaAsset.DoesNotExist:
        return JsonResponse({'error': 'Media asset not found'}, status=404)

    if asset_id:
        try:
            ta = TextureAsset.objects.get(pk=asset_id, scene_config=scene)
        except TextureAsset.DoesNotExist:
            return JsonResponse({'error': 'Texture asset not found'}, status=404)
        ta.label = label
        ta.media_asset = media_asset
        ta.texture_type = texture_type
        ta.save()
    else:
        ta = TextureAsset.objects.create(
            scene_config=scene,
            label=label,
            media_asset=media_asset,
            texture_type=texture_type,
        )

    return JsonResponse({
        'success': True,
        'texture_asset': {
            'id': ta.id,
            'label': ta.label,
            'media_asset_id': str(ta.media_asset_id),
            'media_asset_title': ta.media_asset.title,
            'media_url': ta.media_asset.original_file.url if ta.media_asset.original_file else '',
            'texture_type': ta.texture_type,
            'texture_type_display': ta.get_texture_type_display(),
        }
    })


@staff_member_required
@require_POST
def delete_texture_asset(request, product_id, asset_id):
    """AJAX: Delete a texture asset (scoped to product)."""
    ta = get_object_or_404(
        TextureAsset,
        pk=asset_id,
        scene_config__product_id=product_id,
        scene_config__product__product_type='configurable',
    )
    ta.delete()
    return JsonResponse({'success': True})


@staff_member_required
@require_POST
def capture_thumbnail(request, product_id):
    """AJAX: Save a canvas screenshot as the scene thumbnail."""
    product = get_object_or_404(Product, pk=product_id, product_type='configurable')
    scene, _created = SceneConfig.objects.get_or_create(product=product)

    try:
        data = json.loads(request.body)
        image_data = data.get('image_data')  # base64 PNG
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not image_data:
        return JsonResponse({'error': 'image_data required'}, status=400)

    # Limit base64 payload to ~10MB decoded (approx 13.3MB encoded)
    MAX_THUMBNAIL_SIZE = 14 * 1024 * 1024
    if len(image_data) > MAX_THUMBNAIL_SIZE:
        return JsonResponse({'error': 'Image data too large'}, status=400)

    try:
        # Strip data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',', 1)[1]

        image_bytes = base64.b64decode(image_data)
        file_obj = BytesIO(image_bytes)
        file_obj.name = f'3d_thumbnail_{product_id}.png'

        from django.core.files.uploadedfile import InMemoryUploadedFile
        upload = InMemoryUploadedFile(
            file=file_obj,
            field_name='file',
            name=file_obj.name,
            content_type='image/png',
            size=len(image_bytes),
            charset=None,
        )

        # Create a MediaAsset for the thumbnail
        from PIL import Image
        img = Image.open(BytesIO(image_bytes))

        asset = MediaAsset.objects.create(
            title=f'3D Thumbnail - {product.name}',
            original_file=upload,
            file_size=len(image_bytes),
            width=img.width,
            height=img.height,
            mime_type='image/png',
            uploaded_by=request.user,
        )

        scene.thumbnail = asset
        scene.save()

        return JsonResponse({'success': True, 'thumbnail_url': asset.original_file.url})

    except Exception as e:
        logger.error("Error capturing 3D thumbnail: %s", e, exc_info=True)
        return JsonResponse({'error': _('An error occurred while capturing the thumbnail. Please try again.')}, status=500)
