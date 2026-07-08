import json

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Q
from .models import ImageSizePreset, MediaAsset


@staff_member_required
@require_GET
def filter_image_size_presets(request):
    """AJAX endpoint for filtering image size presets."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    crop_mode = request.GET.get('crop_mode', '').strip()
    is_active = request.GET.get('is_active', '').strip()
    preset_type = request.GET.get('preset_type', '').strip()

    # Build queryset
    queryset = ImageSizePreset.objects.all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    if crop_mode:
        queryset = queryset.filter(crop_mode=crop_mode)

    if is_active == 'true':
        queryset = queryset.filter(is_active=True)
    elif is_active == 'false':
        queryset = queryset.filter(is_active=False)

    if preset_type == 'system':
        queryset = queryset.filter(is_system_preset=True)
    elif preset_type == 'custom':
        queryset = queryset.filter(is_system_preset=False)

    # Order by system presets first, then name
    queryset = queryset.order_by('-is_system_preset', 'name')

    # Render results
    html = render_to_string(
        'admin/media_library/imagesizepreset/partials/preset_cards.html',
        {'presets': queryset},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count()
    })


@staff_member_required
@require_GET
def filter_media_assets(request):
    """AJAX endpoint for filtering media assets."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    mime_type = request.GET.get('mime_type', '').strip()
    folder_id = request.GET.get('folder', '').strip()
    is_public = request.GET.get('is_public', '').strip()

    # Build queryset
    queryset = MediaAsset.objects.select_related('folder', 'uploaded_by').prefetch_related('tags').all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(alt_text__icontains=search) |
            Q(description__icontains=search) |
            Q(tags__name__icontains=search)
        ).distinct()

    if mime_type:
        queryset = queryset.filter(mime_type=mime_type)

    if folder_id:
        if folder_id == 'none':
            queryset = queryset.filter(folder__isnull=True)
        else:
            queryset = queryset.filter(folder_id=folder_id)

    if is_public == 'true':
        queryset = queryset.filter(is_public=True)
    elif is_public == 'false':
        queryset = queryset.filter(is_public=False)

    # Order by created_at descending (newest first)
    queryset = queryset.order_by('-created_at')

    # Render results
    html = render_to_string(
        'admin/media_library/mediaasset/partials/asset_cards.html',
        {'assets': queryset},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count()
    })


@staff_member_required
def image_processing_view(request):
    """Standalone Image Processing admin page."""
    from core.models import SiteSettings

    site_settings = SiteSettings.objects.first()
    context = {
        'title': 'Image Processing',
        'site_settings': site_settings,
        'has_permission': True,
        'is_popup': False,
    }
    return render(request, 'admin/media_library/image_processing.html', context)


@staff_member_required
@require_GET
def thumbnail_sizes_api(request):
    """API endpoint for thumbnail sizes configuration."""
    db_sizes = ImageSizePreset.get_sizes_dict()

    sizes_with_meta = []
    for preset in ImageSizePreset.objects.all().order_by('sort_order', 'name'):
        sizes_with_meta.append({
            'id': preset.id,
            'name': preset.slug,
            'display_name': preset.display_name or preset.name,
            'width': preset.width,
            'height': preset.height,
            'description': preset.description,
            'is_active': preset.is_active,
            'sort_order': preset.sort_order,
            'is_system_preset': preset.is_system_preset,
            'crop_mode': preset.crop_mode,
            'quality': preset.quality,
        })

    return JsonResponse({
        'thumbnail_sizes': db_sizes,
        'sizes_detail': sizes_with_meta,
        'has_db_sizes': len(sizes_with_meta) > 0
    })


@staff_member_required
def save_thumbnail_sizes_api(request):
    """API endpoint to save thumbnail size changes."""
    from django.utils.text import slugify

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
        updates = data.get('updates', [])
        creates = data.get('creates', [])

        for update_data in updates:
            preset_id = update_data['id']
            preset = ImageSizePreset.objects.get(id=preset_id)

            if not preset.is_system_preset:
                preset.name = update_data.get('display_name', preset.name)
                preset.display_name = update_data.get('display_name', preset.display_name)
                preset.slug = update_data.get('name', preset.slug)

            preset.width = update_data['width']
            preset.height = update_data['height']
            preset.description = update_data.get('description', preset.description)
            preset.is_active = update_data['is_active']
            preset.sort_order = update_data.get('sort_order', preset.sort_order)
            preset.save()

        for create_data in creates:
            display_name = create_data.get('display_name', create_data.get('name', ''))
            slug = slugify(create_data.get('name', display_name))
            ImageSizePreset.objects.create(
                name=display_name,
                display_name=display_name,
                slug=slug,
                width=create_data['width'],
                height=create_data['height'],
                description=create_data.get('description', ''),
                is_active=create_data.get('is_active', True),
                sort_order=create_data.get('sort_order', 0),
                is_system_preset=False
            )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@staff_member_required
def delete_thumbnail_size_api(request, size_id):
    """API endpoint to delete a thumbnail size."""
    if request.method != 'DELETE':
        return JsonResponse({'success': False, 'error': 'DELETE method required'}, status=405)

    try:
        preset = ImageSizePreset.objects.get(id=size_id)

        if preset.is_system_preset:
            return JsonResponse({
                'success': False,
                'error': 'System presets cannot be deleted'
            }, status=403)

        preset.delete()
        return JsonResponse({'success': True})

    except ImageSizePreset.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image size preset not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@staff_member_required
@require_GET
def image_stats_api(request):
    """API endpoint for image library statistics."""
    from .models import MediaThumbnail
    from catalog.models import ProductImage

    total_images = MediaAsset.objects.filter(mime_type__startswith='image/').count()
    product_images = ProductImage.objects.count()
    total_thumbnails = MediaThumbnail.objects.count()
    webp_images = MediaAsset.objects.exclude(webp_file='').count()

    return JsonResponse({
        'total_images': total_images,
        'product_images': product_images,
        'total_thumbnails': total_thumbnails,
        'webp_images': webp_images
    })


@staff_member_required
def regenerate_thumbnails_view(request):
    """Start thumbnail regeneration process using Celery."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST method required'}, status=405)

    try:
        from core.tasks import regenerate_thumbnails_task
        task = regenerate_thumbnails_task.delay()

        return JsonResponse({
            'success': True,
            'message': 'Thumbnail regeneration started',
            'task_id': task.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_GET
def regenerate_thumbnails_status_view(request):
    """Get status of thumbnail regeneration."""
    from django.core.cache import cache

    status = cache.get('thumbnail_regeneration_status', {
        'complete': True,
        'progress': 100,
        'processed': 0,
        'total': 0,
        'message': 'No regeneration in progress'
    })

    last_regeneration = cache.get('thumbnail_last_regeneration', None)
    if last_regeneration:
        status['last_regeneration'] = last_regeneration

    return JsonResponse(status)
