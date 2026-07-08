"""
Sync API Views

Server-side REST endpoints for Spwig-to-Spwig sync.
Each Spwig instance exposes these endpoints so remote instances can read/write data.
"""
import json
import logging

from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.contrib.admin.views.decorators import staff_member_required

from core.models import APIToken
from core.utils.api_tokens import create_api_token, revoke_token, get_active_tokens_by_type

from .authentication import authenticate_sync_request, SyncTokenAuthError
from .category_registry import (
    SYNC_CATEGORIES, get_categories_for_feature, FEATURE_BOTH
)

logger = logging.getLogger(__name__)


def sync_auth_required(view_func):
    """Decorator that enforces SyncToken authentication."""
    from functools import wraps

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            api_token = authenticate_sync_request(request)
            request.sync_token = api_token
        except SyncTokenAuthError as e:
            return JsonResponse({'error': str(e)}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_serializer(category_key):
    """Lazy-load a category serializer by key."""
    from .serializers import get_serializer_for_category
    return get_serializer_for_category(category_key)


# ========================================================================
# Instance Info Endpoints (SyncToken auth)
# ========================================================================

@csrf_exempt
@require_GET
@sync_auth_required
def sync_info(request):
    """
    GET /api/sync/info/
    Returns instance information: version, site name, available categories.
    """
    try:
        from core.models import SiteSettings
        site_settings = SiteSettings.objects.first()
        site_name = site_settings.site_name if site_settings else 'Spwig Store'
    except Exception:
        site_name = 'Spwig Store'

    version = getattr(settings, 'SPWIG_VERSION', None) or getattr(settings, 'VERSION', 'unknown')

    # List available categories
    categories = []
    for key, config in SYNC_CATEGORIES.items():
        categories.append({
            'key': key,
            'label': str(config['label']),
            'group': config.get('group', ''),
            'has_credentials': config.get('has_credentials', False),
            'has_files': config.get('has_files', False),
            'feature': config.get('feature', FEATURE_BOTH),
        })

    return JsonResponse({
        'version': version,
        'site_name': site_name,
        'categories': categories,
    })


@csrf_exempt
@require_GET
@sync_auth_required
def sync_categories(request):
    """
    GET /api/sync/categories/
    List available sync categories with item counts.
    """
    feature_type = request.GET.get('feature', 'settings_sync')
    categories = get_categories_for_feature(feature_type)

    result = []
    for key, config in categories.items():
        try:
            serializer = _get_serializer(key)
            count = serializer.get_count() if serializer else 0
        except Exception:
            count = 0

        result.append({
            'key': key,
            'label': str(config['label']),
            'description': str(config.get('description', '')),
            'group': config.get('group', ''),
            'count': count,
            'has_credentials': config.get('has_credentials', False),
            'has_files': config.get('has_files', False),
            'production_warning': str(config['production_warning']) if config.get('production_warning') else None,
            'dependencies': config.get('dependencies', []),
        })

    return JsonResponse({'categories': result})


# ========================================================================
# Export Endpoints (SyncToken auth)
# ========================================================================

@csrf_exempt
@require_GET
@sync_auth_required
def sync_export(request, category):
    """
    GET /api/sync/export/<category>/
    Export data for a specific category.
    """
    if category not in SYNC_CATEGORIES:
        return JsonResponse({'error': f'Unknown category: {category}'}, status=404)

    credential_mode = request.GET.get('credential_mode', 'redact')
    if credential_mode not in ('decrypt', 'redact', 'skip'):
        credential_mode = 'redact'

    try:
        page = max(1, int(request.GET.get('page', 1)))
        per_page = min(max(1, int(request.GET.get('per_page', 100))), 500)
    except (ValueError, TypeError):
        page, per_page = 1, 100

    try:
        serializer = _get_serializer(category)
        if not serializer:
            return JsonResponse({'error': f'No serializer for category: {category}'}, status=500)

        data = serializer.export(credential_mode=credential_mode)

        # Handle pagination for collections
        if data.get('sync_type') == 'collection' and isinstance(data.get('items'), list):
            items = data['items']
            total = len(items)
            start = (page - 1) * per_page
            end = start + per_page
            data['items'] = items[start:end]
            data['page'] = page
            data['per_page'] = per_page
            data['pages'] = (total + per_page - 1) // per_page

        return JsonResponse(data)

    except Exception as e:
        logger.error(f"Export error for {category}: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
@sync_auth_required
def sync_export_count(request, category):
    """
    GET /api/sync/export/<category>/count/
    Get item count for a category.
    """
    if category not in SYNC_CATEGORIES:
        return JsonResponse({'error': f'Unknown category: {category}'}, status=404)

    try:
        serializer = _get_serializer(category)
        count = serializer.get_count() if serializer else 0
        return JsonResponse({'category': category, 'count': count})
    except Exception as e:
        logger.error(f"Count error for {category}: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
@sync_auth_required
def sync_media_export(request, asset_id):
    """
    GET /api/sync/export/media/<asset_id>/
    Stream a media file for download.
    """
    from media_library.models import MediaAsset

    try:
        asset = MediaAsset.objects.get(pk=asset_id)
    except MediaAsset.DoesNotExist:
        return JsonResponse({'error': 'Media asset not found'}, status=404)

    if not asset.original_file:
        return JsonResponse({'error': 'Asset has no file'}, status=404)

    from .media_transfer import stream_media_file
    import mimetypes
    import os

    content_type = mimetypes.guess_type(asset.original_file.name)[0] or 'application/octet-stream'

    response = StreamingHttpResponse(
        stream_media_file(asset.original_file),
        content_type=content_type,
    )
    # Sanitize filename to prevent header injection
    safe_filename = os.path.basename(asset.original_file.name).replace('"', '_')
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'

    try:
        response['Content-Length'] = asset.original_file.size
    except Exception:
        pass

    return response


# ========================================================================
# Import Endpoints (SyncToken auth)
# ========================================================================

@csrf_exempt
@require_POST
@sync_auth_required
def sync_import(request, category):
    """
    POST /api/sync/import/<category>/
    Import data for a specific category.
    """
    if category not in SYNC_CATEGORIES:
        return JsonResponse({'error': f'Unknown category: {category}'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    sync_mode = data.get('sync_mode', 'additive')
    if sync_mode not in ('additive', 'mirror'):
        sync_mode = 'additive'

    try:
        serializer = _get_serializer(category)
        if not serializer:
            return JsonResponse({'error': f'No serializer for category: {category}'}, status=500)

        result = serializer.import_data(data, dry_run=False, sync_mode=sync_mode)
        return JsonResponse(result)

    except Exception as e:
        logger.error(f"Import error for {category}: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
@sync_auth_required
def sync_import_preview(request, category):
    """
    POST /api/sync/import/<category>/preview/
    Dry-run import -- returns diff without applying changes.
    """
    if category not in SYNC_CATEGORIES:
        return JsonResponse({'error': f'Unknown category: {category}'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    try:
        serializer = _get_serializer(category)
        if not serializer:
            return JsonResponse({'error': f'No serializer for category: {category}'}, status=500)

        diff = serializer.generate_diff(data)
        return JsonResponse(diff)

    except Exception as e:
        logger.error(f"Preview error for {category}: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
@sync_auth_required
def sync_media_import(request):
    """
    POST /api/sync/import/media/
    Upload a media file (multipart form).
    """
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({'error': 'No file provided'}, status=400)

    target_path = request.POST.get('target_path', '')
    expected_checksum = request.POST.get('checksum')

    from .media_transfer import import_media_file

    result = import_media_file(
        uploaded_file.read(),
        target_path or uploaded_file.name,
        expected_checksum=expected_checksum,
    )

    status_code = 201 if result['success'] else 400
    return JsonResponse(result, status=status_code)


# ========================================================================
# Pre-flight Endpoint (SyncToken auth)
# ========================================================================

@csrf_exempt
@require_GET
@sync_auth_required
def sync_preflight(request):
    """
    GET /api/sync/preflight/
    Returns pre-flight information for full migration planning.
    """
    import shutil

    # Installed components
    components = []
    try:
        from component_updates.models import ComponentRegistry
        for comp in ComponentRegistry.objects.all():
            components.append({
                'slug': comp.slug,
                'name': comp.name,
                'version': comp.version,
                'component_type': comp.component_type,
            })
    except Exception:
        pass

    # Data counts per category
    counts = {}
    for key in SYNC_CATEGORIES:
        try:
            serializer = _get_serializer(key)
            counts[key] = serializer.get_count() if serializer else 0
        except Exception:
            counts[key] = 0

    # Media total size
    media_size = 0
    try:
        from .media_transfer import get_media_total_size
        media_size = get_media_total_size()
    except Exception:
        pass

    # Disk usage
    disk_usage = {}
    try:
        media_root = str(settings.MEDIA_ROOT)
        usage = shutil.disk_usage(media_root)
        disk_usage = {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
        }
    except Exception:
        pass

    version = getattr(settings, 'SPWIG_VERSION', None) or getattr(settings, 'VERSION', 'unknown')

    return JsonResponse({
        'version': version,
        'components': components,
        'counts': counts,
        'media_size': media_size,
        'disk_usage': disk_usage,
    })


# ========================================================================
# Token Management Endpoints (Admin session auth, NOT SyncToken)
# ========================================================================

@staff_member_required
@require_GET
def sync_token_list(request):
    """
    GET /api/sync/tokens/
    List active sync tokens (requires admin login).
    """
    tokens = get_active_tokens_by_type(APIToken.TOKEN_TYPE_SYNC)
    token_list = []
    for t in tokens:
        token_list.append({
            'id': t.id,
            'name': t.name,
            'token_preview': t.token[:8] + '...',
            'created_at': t.created_at.isoformat(),
            'last_used_at': t.last_used_at.isoformat() if t.last_used_at else None,
            'expires_at': t.expires_at.isoformat() if t.expires_at else None,
            'usage_count': t.usage_count,
            'is_active': t.is_active,
        })

    return JsonResponse({'tokens': token_list})


@staff_member_required
@require_POST
def sync_token_generate(request):
    """
    POST /api/sync/tokens/generate/
    Generate a new sync token (requires admin login).
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}

    name = data.get('name', 'Sync Token')
    description = data.get('description', '')

    # Parse optional expiry
    expires_at = None
    if data.get('expires_in_days'):
        from django.utils import timezone
        from datetime import timedelta
        expires_at = timezone.now() + timedelta(days=int(data['expires_in_days']))

    token = create_api_token(
        name=name,
        token_type=APIToken.TOKEN_TYPE_SYNC,
        description=description,
        created_by=request.user,
        expires_at=expires_at,
    )

    return JsonResponse({
        'id': token.id,
        'name': token.name,
        'token': token.token,  # Full token shown only on creation
        'created_at': token.created_at.isoformat(),
        'expires_at': token.expires_at.isoformat() if token.expires_at else None,
    }, status=201)


@staff_member_required
@require_POST
def sync_token_revoke(request, token_id):
    """
    POST /api/sync/tokens/<id>/revoke/
    Revoke a sync token (requires admin login).
    Only allows revoking tokens of type 'sync'.
    """
    # Verify the token is actually a sync token before revoking
    try:
        token = APIToken.objects.get(pk=token_id)
        if token.token_type != APIToken.TOKEN_TYPE_SYNC:
            return JsonResponse({'error': 'Token is not a sync token'}, status=403)
    except APIToken.DoesNotExist:
        return JsonResponse({'error': 'Token not found'}, status=404)

    success = revoke_token(token_id)
    if success:
        return JsonResponse({'status': 'revoked'})
    return JsonResponse({'error': 'Failed to revoke token'}, status=500)
