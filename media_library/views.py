from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
import logging

from .models import MediaAsset, MediaFolder, Tag, MediaThumbnail, MediaProcessingJob
from .serializers import (
    MediaAssetListSerializer,
    MediaAssetDetailSerializer,
    MediaAssetCreateSerializer,
    MediaAssetUpdateSerializer,
    MediaFolderSerializer,
    TagSerializer,
    BulkOperationSerializer,
    MediaProcessingJobSerializer
)
from .services import ImageProcessor

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(tags=['Media Library'], summary=_("List media assets")),
    retrieve=extend_schema(tags=['Media Library'], summary=_("Get media asset details")),
    create=extend_schema(tags=['Media Library'], summary=_("Upload new media asset")),
    update=extend_schema(tags=['Media Library'], summary=_("Update media asset")),
    partial_update=extend_schema(tags=['Media Library'], summary=_("Partially update media asset")),
    destroy=extend_schema(tags=['Media Library'], summary=_("Delete media asset")),
    bulk_operations=extend_schema(tags=['Media Library'], summary=_("Perform bulk operations")),
    regenerate_thumbnails=extend_schema(tags=['Media Library'], summary=_("Regenerate thumbnails")),
    regenerate_webp=extend_schema(tags=['Media Library'], summary=_("Regenerate WebP version")),
    stream=extend_schema(tags=['Media Library'], summary=_("Stream video content")),
    track_usage=extend_schema(tags=['Media Library'], summary=_("Track asset usage")),
    deleted=extend_schema(tags=['Media Library'], summary=_("Get deleted assets")),
    restore=extend_schema(tags=['Media Library'], summary=_("Restore deleted assets")),
    permanent_delete=extend_schema(tags=['Media Library'], summary=_("Permanently delete assets")),
    empty_recycle_bin=extend_schema(tags=['Media Library'], summary=_("Empty recycle bin")),
    stats=extend_schema(tags=['Media Library'], summary=_("Get asset statistics")),
    set_poster=extend_schema(
        tags=['Media Library'],
        summary=_("Set poster image for asset"),
        description=_("Set a poster/thumbnail image for a media asset (videos and 3D models). "
                    "Upload a poster file via multipart form data. Requires authentication."),
        responses={
            200: OpenApiResponse(description=_("Poster image set successfully")),
            400: OpenApiResponse(description=_("No poster file provided")),
        },
    ),
)
class MediaAssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing media assets
    """
    queryset = MediaAsset.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'alt_text', 'description', 'tags__name']
    ordering_fields = ['created_at', 'title', 'file_size', 'usage_count']
    ordering = ['-created_at']
    filterset_fields = ['mime_type', 'folder', 'is_public', 'tags']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MediaAssetListSerializer
        elif self.action == 'create':
            return MediaAssetCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return MediaAssetUpdateSerializer
        return MediaAssetDetailSerializer
    
    def get_queryset(self):
        queryset = MediaAsset.objects.select_related('folder', 'uploaded_by').prefetch_related('tags', 'thumbnails')

        # Filter by mime type (supports startswith for filtering by type category)
        mime_type_startswith = self.request.query_params.get('mime_type__startswith')
        if mime_type_startswith:
            queryset = queryset.filter(mime_type__startswith=mime_type_startswith)

        # Filter by folder path if provided
        folder_path = self.request.query_params.get('folder_path')
        if folder_path:
            if folder_path == 'root':
                queryset = queryset.filter(folder__isnull=True)
            else:
                queryset = queryset.filter(folder__path=folder_path)

        # Filter by multiple tags
        tag_names = self.request.query_params.getlist('tag_names')
        if tag_names:
            queryset = queryset.filter(tags__name__in=tag_names).distinct()

        # Filter by file size range
        min_size = self.request.query_params.get('min_size')
        max_size = self.request.query_params.get('max_size')
        if min_size:
            queryset = queryset.filter(file_size__gte=int(min_size))
        if max_size:
            queryset = queryset.filter(file_size__lte=int(max_size))

        # Filter by dimensions
        min_width = self.request.query_params.get('min_width')
        max_width = self.request.query_params.get('max_width')
        min_height = self.request.query_params.get('min_height')
        max_height = self.request.query_params.get('max_height')

        if min_width:
            queryset = queryset.filter(width__gte=int(min_width))
        if max_width:
            queryset = queryset.filter(width__lte=int(max_width))
        if min_height:
            queryset = queryset.filter(height__gte=int(min_height))
        if max_height:
            queryset = queryset.filter(height__lte=int(max_height))

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def regenerate_thumbnails(self, request, pk=None):
        """Regenerate thumbnails for a specific asset"""
        from media_library.models import ImageSizePreset

        asset = self.get_object()

        try:
            processor = ImageProcessor()

            # Delete existing thumbnails
            asset.thumbnails.all().delete()

            # Generate new thumbnails using ImageSizePreset for crop_mode and padding_color
            presets = ImageSizePreset.objects.filter(is_active=True)

            for preset in presets:
                asset.original_file.seek(0)
                original_content, webp_content = processor.generate_thumbnail(
                    asset.original_file,
                    preset.width,
                    preset.height,
                    crop_mode=preset.crop_mode,
                    padding_color=getattr(preset, 'padding_color', None)
                )

                if original_content:
                    # Determine file extension based on crop mode
                    ext = 'png' if preset.crop_mode == 'pad' and getattr(preset, 'padding_color', 'transparent') == 'transparent' else 'jpg'
                    thumbnail = MediaThumbnail.objects.create(
                        media_asset=asset,
                        size_preset=preset.slug,
                        width=preset.width,
                        height=preset.height
                    )
                    thumbnail.file.save(f"{asset.id}_{preset.slug}.{ext}", original_content, save=False)
                    if webp_content:
                        thumbnail.webp_file.save(f"{asset.id}_{preset.slug}.webp", webp_content, save=False)
                    thumbnail.save()

            return Response({'message': _('Thumbnails regenerated successfully')})

        except Exception as e:
            logger.error(f"Error regenerating thumbnails for asset {pk}: {e}")
            return Response(
                {'error': _('Failed to regenerate thumbnails')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def regenerate_webp(self, request, pk=None):
        """Regenerate WebP version for a specific asset"""
        asset = self.get_object()
        
        try:
            processor = ImageProcessor()
            
            if asset.original_file and asset.mime_type != 'image/webp':
                webp_content = processor.convert_to_webp(asset.original_file)
                if webp_content:
                    asset.webp_file.save(f"{asset.id}.webp", webp_content, save=True)
                    return Response({'message': _('WebP version regenerated successfully')})
                else:
                    return Response(
                        {'error': _('Failed to generate WebP version')},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': _('Asset is already WebP or has no original file')},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"Error regenerating WebP for asset {pk}: {e}")
            return Response(
                {'error': _('Failed to regenerate WebP version')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def set_poster(self, request, pk=None):
        """Set a poster/thumbnail image for a media asset (videos and 3D models)"""
        asset = self.get_object()

        poster_file = request.FILES.get('poster')
        if not poster_file:
            return Response(
                {'error': _('No poster file provided')},
                status=status.HTTP_400_BAD_REQUEST
            )

        asset.poster_image.save(
            f"{asset.id}_poster.{poster_file.name.split('.')[-1]}",
            poster_file,
            save=True
        )

        return Response({
            'success': True,
            'poster_url': asset.poster_image.url
        })

    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        """Stream video content"""
        asset = self.get_object()

        if not asset.is_video():
            return Response(
                {'error': _('This asset is not a video')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Determine which video file to serve
        format_param = request.GET.get('format', 'webm')
        video_file = None

        # Always prefer the optimized converted version if available
        if asset.converted_video:
            # We have a converted version (should be WebM/AV1)
            if format_param == 'webm' or not format_param:
                # Default: serve the optimized WebM version
                video_file = asset.converted_video
                logger.info(f"Serving optimized WebM version for asset {pk}")
            elif format_param == 'mp4':
                # Fallback requested: serve original if it's mp4, otherwise still use converted
                if asset.original_file and asset.mime_type == 'video/mp4':
                    video_file = asset.original_file
                    logger.info(f"Serving original MP4 for asset {pk}")
                else:
                    # Original is not mp4, serve converted anyway
                    video_file = asset.converted_video
                    logger.info(f"Original not MP4, serving WebM for asset {pk}")
        else:
            # No converted version available, serve original
            video_file = asset.original_file
            logger.warning(f"No converted video for asset {pk}, serving original")

        if not video_file:
            return Response(
                {'error': _('Video file not found')},
                status=status.HTTP_404_NOT_FOUND
            )

        # Stream the video file
        from django.http import FileResponse
        import mimetypes

        # Determine content type
        content_type, _ = mimetypes.guess_type(video_file.name)
        if not content_type:
            content_type = 'video/mp4' if format_param == 'mp4' else 'video/webm'

        # Open file for streaming
        try:
            from django.http import HttpResponse
            import os

            # Get file path and size
            file_path = video_file.path if hasattr(video_file, 'path') else video_file.name
            file_size = video_file.size

            # Log what we're trying to serve
            logger.info(f"Streaming video: {file_path}, size: {file_size}, format: {format_param}")

            # Handle range requests for video seeking
            range_header = request.META.get('HTTP_RANGE', None)

            if range_header:
                # Parse range header
                import re
                range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
                if range_match:
                    start = int(range_match.group(1))
                    end = int(range_match.group(2)) if range_match.group(2) else file_size - 1

                    # Ensure end doesn't exceed file size
                    end = min(end, file_size - 1)

                    # Open file and seek to start
                    file_handle = video_file.open('rb')
                    file_handle.seek(start)

                    # Read the requested range
                    chunk_size = end - start + 1
                    data = file_handle.read(chunk_size)
                    file_handle.close()

                    # Create partial content response
                    response = HttpResponse(
                        data,
                        content_type=content_type,
                        status=206  # Partial Content
                    )
                    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                    response['Accept-Ranges'] = 'bytes'
                    response['Content-Length'] = str(chunk_size)
                else:
                    # Invalid range, serve full file
                    response = FileResponse(
                        video_file.open('rb'),
                        content_type=content_type,
                        as_attachment=False
                    )
                    response['Accept-Ranges'] = 'bytes'
                    response['Content-Length'] = str(file_size)
            else:
                # No range request, serve full file
                response = FileResponse(
                    video_file.open('rb'),
                    content_type=content_type,
                    as_attachment=False
                )
                response['Accept-Ranges'] = 'bytes'
                response['Content-Length'] = str(file_size)

            # Add CORS headers if needed
            response['Access-Control-Allow-Origin'] = '*'
            response['Cache-Control'] = 'no-cache'

            return response

        except Exception as e:
            logger.error(f"Error streaming video for asset {pk}: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': _('Failed to stream video')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def track_usage(self, request, pk=None):
        """Track usage of a media asset"""
        asset = self.get_object()
        
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')
        field_name = request.data.get('field_name')
        
        if not all([content_type, object_id, field_name]):
            return Response(
                {'error': _('content_type, object_id, and field_name are required')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create or update usage record
        from .models import MediaUsage
        usage, created = MediaUsage.objects.get_or_create(
            media_asset=asset,
            content_type=content_type,
            object_id=object_id,
            field_name=field_name
        )
        
        # Update asset usage stats
        asset.usage_count = asset.usages.count()
        asset.last_used_at = timezone.now()
        asset.save(update_fields=['usage_count', 'last_used_at'])
        
        return Response({'message': _('Usage tracked successfully')})
    
    @action(detail=False, methods=['post'])
    def bulk_operations(self, request):
        """Perform bulk operations on multiple assets"""
        serializer = BulkOperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        asset_ids = data['asset_ids']
        action = data['action']
        
        # Get assets
        assets = MediaAsset.objects.filter(id__in=asset_ids)
        if not assets.exists():
            return Response({'error': _('No valid assets found')}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            if action == 'delete':
                count = assets.count()
                # Use soft delete instead of hard delete
                for asset in assets:
                    asset.delete(user=request.user)  # This will call the soft delete method
                return Response({'message': _(f'Deleted {count} assets successfully')})
            
            elif action == 'move_to_folder':
                folder_id = data.get('folder_id')
                folder = None
                if folder_id:
                    folder = get_object_or_404(MediaFolder, id=folder_id)
                
                assets.update(folder=folder)
                return Response({'message': _(f'Moved {assets.count()} assets successfully')})
            
            elif action == 'add_tags':
                tag_ids = data['tag_ids']
                tags = Tag.objects.filter(id__in=tag_ids)
                
                for asset in assets:
                    asset.tags.add(*tags)
                
                return Response({'message': _(f'Added tags to {assets.count()} assets successfully')})
            
            elif action == 'remove_tags':
                tag_ids = data['tag_ids']
                tags = Tag.objects.filter(id__in=tag_ids)
                
                for asset in assets:
                    asset.tags.remove(*tags)
                
                return Response({'message': _(f'Removed tags from {assets.count()} assets successfully')})
            
            elif action == 'toggle_public':
                # Toggle public status for each asset
                for asset in assets:
                    asset.is_public = not asset.is_public
                    asset.save(update_fields=['is_public'])
                
                return Response({'message': _(f'Toggled public status for {assets.count()} assets successfully')})
            
        except Exception as e:
            logger.error(f"Error performing bulk operation {action}: {e}")
            return Response(
                {'error': _(f'Failed to perform {action}')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        """Get soft-deleted assets (recycle bin)"""
        # Use the all_objects manager to get deleted items with related data
        deleted_assets = MediaAsset.all_objects.filter(is_deleted=True).select_related('folder', 'uploaded_by').prefetch_related('tags', 'thumbnails').order_by('-deleted_at')

        page = self.paginate_queryset(deleted_assets)
        if page is not None:
            serializer = MediaAssetListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = MediaAssetListSerializer(deleted_assets, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def restore(self, request):
        """Restore soft-deleted assets"""
        asset_ids = request.data.get('asset_ids', [])

        if not asset_ids:
            return Response({'error': _('No assets specified')}, status=status.HTTP_400_BAD_REQUEST)

        # Get deleted assets
        assets = MediaAsset.all_objects.filter(id__in=asset_ids, is_deleted=True)

        if not assets.exists():
            return Response({'error': _('No deleted assets found')}, status=status.HTTP_404_NOT_FOUND)

        # Restore each asset
        count = 0
        for asset in assets:
            asset.restore()
            count += 1

        return Response({'message': _(f'Restored {count} assets successfully')})

    @action(detail=False, methods=['post'])
    def permanent_delete(self, request):
        """Permanently delete soft-deleted assets"""
        asset_ids = request.data.get('asset_ids', [])

        if not asset_ids:
            return Response({'error': _('No assets specified')}, status=status.HTTP_400_BAD_REQUEST)

        # Get deleted assets
        assets = MediaAsset.all_objects.filter(id__in=asset_ids, is_deleted=True)

        if not assets.exists():
            return Response({'error': _('No deleted assets found')}, status=status.HTTP_404_NOT_FOUND)

        # Permanently delete each asset
        count = assets.count()
        for asset in assets:
            asset.hard_delete()

        return Response({'message': _(f'Permanently deleted {count} assets')})

    @action(detail=False, methods=['post'])
    def empty_recycle_bin(self, request):
        """Empty the entire recycle bin (delete all soft-deleted assets)"""
        # Require admin permission for this operation
        if not request.user.is_staff:
            return Response({'error': _('Admin permission required')}, status=status.HTTP_403_FORBIDDEN)

        # Get all deleted assets
        deleted_assets = MediaAsset.all_objects.filter(is_deleted=True)
        count = deleted_assets.count()

        if count == 0:
            return Response({'message': _('Recycle bin is already empty')})

        # Permanently delete all
        for asset in deleted_assets:
            asset.hard_delete()

        return Response({'message': _(f'Permanently deleted {count} assets from recycle bin')})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get media library statistics"""
        total_assets = MediaAsset.objects.count()
        total_size = MediaAsset.objects.aggregate(
            total=Sum('file_size')
        )['total'] or 0
        
        # Group by mime type
        by_type = MediaAsset.objects.values('mime_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Recent uploads
        recent = MediaAsset.objects.order_by('-created_at')[:10]
        recent_data = MediaAssetListSerializer(recent, many=True).data
        
        return Response({
            'total_assets': total_assets,
            'total_size': total_size,
            'total_size_display': self._format_file_size(total_size),
            'by_mime_type': list(by_type),
            'recent_uploads': recent_data
        })
    
    def _format_file_size(self, bytes_size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} PB"


@extend_schema_view(
    list=extend_schema(tags=['Media Library'], summary=_("List media folders")),
    retrieve=extend_schema(tags=['Media Library'], summary=_("Get folder details")),
    create=extend_schema(tags=['Media Library'], summary=_("Create new folder")),
    update=extend_schema(tags=['Media Library'], summary=_("Update folder")),
    partial_update=extend_schema(tags=['Media Library'], summary=_("Partially update folder")),
    destroy=extend_schema(tags=['Media Library'], summary=_("Delete folder")),
    tree=extend_schema(tags=['Media Library'], summary=_("Get folder tree structure"))
)
class MediaFolderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing media folders
    """
    queryset = MediaFolder.objects.all()
    serializer_class = MediaFolderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'path', 'description']
    ordering = ['path']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get folder tree structure"""
        folders = MediaFolder.objects.select_related('parent').prefetch_related('children')
        
        # Build tree structure
        tree = []
        folder_dict = {}
        
        # First pass: create all nodes
        for folder in folders:
            folder_data = MediaFolderSerializer(folder).data
            folder_data['children'] = []
            folder_dict[folder.id] = folder_data
        
        # Second pass: build tree
        for folder in folders:
            folder_data = folder_dict[folder.id]
            if folder.parent_id:
                parent_data = folder_dict.get(folder.parent_id)
                if parent_data:
                    parent_data['children'].append(folder_data)
            else:
                tree.append(folder_data)
        
        return Response(tree)


@extend_schema_view(
    list=extend_schema(tags=['Media Library'], summary=_("List tags")),
    retrieve=extend_schema(tags=['Media Library'], summary=_("Get tag details")),
    create=extend_schema(tags=['Media Library'], summary=_("Create new tag")),
    update=extend_schema(tags=['Media Library'], summary=_("Update tag")),
    partial_update=extend_schema(tags=['Media Library'], summary=_("Partially update tag")),
    destroy=extend_schema(tags=['Media Library'], summary=_("Delete tag")),
    popular=extend_schema(tags=['Media Library'], summary=_("Get popular tags"))
)
class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular tags by usage count"""
        limit = int(request.query_params.get('limit', 20))
        
        tags = Tag.objects.annotate(
            usage_count=Count('assets')
        ).filter(usage_count__gt=0).order_by('-usage_count')[:limit]
        
        return Response(TagSerializer(tags, many=True).data)


@extend_schema(tags=['Media Library'], summary=_("Track upload progress"))
def upload_progress(request):
    """
    View to track upload progress (for AJAX uploads)
    """
    if request.method != 'POST':
        return JsonResponse({'error': _('POST required')}, status=405)

    # This would typically work with a task queue like Celery
    # For now, return a simple response
    return JsonResponse({
        'status': 'processing',
        'progress': 100,
        'message': _('Upload complete')
    })


@extend_schema_view(
    list=extend_schema(tags=['Media Library'], summary=_("List processing jobs")),
    retrieve=extend_schema(tags=['Media Library'], summary=_("Get job details")),
    active=extend_schema(tags=['Media Library'], summary=_("Get active jobs")),
    cancel=extend_schema(tags=['Media Library'], summary=_("Cancel processing job"))
)
class MediaProcessingJobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for tracking media processing jobs
    """
    queryset = MediaProcessingJob.objects.all()
    serializer_class = MediaProcessingJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter jobs by current user and optionally by status"""
        queryset = MediaProcessingJob.objects.filter(user=self.request.user)

        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter active jobs
        active_only = self.request.query_params.get('active', 'false').lower() == 'true'
        if active_only:
            queryset = queryset.filter(
                status__in=['pending', 'uploading', 'processing', 'converting', 'generating_thumbnails']
            )

        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """List processing jobs with summary statistics"""
        queryset = self.get_queryset()

        # Get statistics
        stats = {
            'total': queryset.count(),
            'active': queryset.filter(
                status__in=['pending', 'uploading', 'processing', 'converting', 'generating_thumbnails']
            ).count(),
            'completed': queryset.filter(status='completed').count(),
            'failed': queryset.filter(status='failed').count(),
        }

        # Paginate results
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.serialize_jobs(page)
            return self.get_paginated_response({
                'stats': stats,
                'jobs': data
            })

        data = self.serialize_jobs(queryset)
        return Response({
            'stats': stats,
            'jobs': data
        })

    def retrieve(self, request, pk=None):
        """Get detailed information about a specific job"""
        try:
            job = self.get_queryset().get(pk=pk)
        except MediaProcessingJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        data = self.serialize_job_detail(job)
        return Response(data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active and recently completed jobs for polling"""
        # Get jobs that are active or were completed in the last 30 seconds
        from datetime import timedelta
        from django.utils import timezone

        thirty_seconds_ago = timezone.now() - timedelta(seconds=30)

        queryset = MediaProcessingJob.objects.filter(user=request.user).filter(
            models.Q(status__in=['pending', 'uploading', 'processing', 'converting', 'generating_thumbnails']) |
            models.Q(status='completed', completed_at__gte=thirty_seconds_ago) |
            models.Q(status='failed', completed_at__gte=thirty_seconds_ago)
        ).order_by('-created_at')

        data = self.serialize_jobs(queryset)
        return Response({'jobs': data})

    def serialize_jobs(self, jobs):
        """Serialize job list"""
        return [{
            'id': str(job.id),
            'job_type': job.job_type,
            'status': job.status,
            'progress': job.progress,
            'filename': job.filename,
            'file_size': job.file_size,
            'status_message': job.status_message,
            'created_at': job.created_at.isoformat(),
            'is_active': job.is_active,
        } for job in jobs]

    def serialize_job_detail(self, job):
        """Serialize detailed job information"""
        data = {
            'id': str(job.id),
            'job_type': job.job_type,
            'job_type_display': job.get_job_type_display(),
            'status': job.status,
            'status_display': job.get_status_display(),
            'progress': job.progress,
            'status_message': job.status_message,
            'filename': job.filename,
            'file_size': job.file_size,
            'mime_type': job.mime_type,
            'created_at': job.created_at.isoformat(),
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
            'duration': job.duration,
            'error_message': job.error_message,
            'is_active': job.is_active,
            'is_complete': job.is_complete,
            'is_failed': job.is_failed,
        }

        # Include media asset if available
        if job.media_asset:
            data['media_asset'] = {
                'id': str(job.media_asset.id),
                'title': job.media_asset.title,
                'url': job.media_asset.get_display_url(),
                'thumbnail': job.media_asset.get_thumbnail('small') if job.media_asset.is_image() else None,
            }

        return data

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active jobs for the current user"""
        jobs = self.get_queryset().filter(
            status__in=['pending', 'uploading', 'processing', 'converting', 'generating_thumbnails']
        )

        data = self.serialize_jobs(jobs)
        return Response({
            'count': len(data),
            'jobs': data
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a processing job"""
        try:
            job = self.get_queryset().get(pk=pk)
        except MediaProcessingJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        if not job.is_active:
            return Response(
                {'error': 'Job is not active and cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        job.status = 'cancelled'
        job.status_message = 'Cancelled by user'
        job.completed_at = timezone.now()
        job.save()

        return Response({'message': 'Job cancelled successfully'})


from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import serializers as drf_serializers
from drf_spectacular.utils import inline_serializer
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist


class MediaFieldAutoSaveAPIView(APIView):
    """
    Generic auto-save endpoint for ForeignKey fields to MediaAsset.

    This allows admin forms to save MediaAsset FK fields immediately on selection,
    without requiring the entire form to be saved. Useful for preventing data loss
    when other form validations fail.

    Can be used by any admin form that wants instant save on media selection.

    POST params:
        app_label: Django app label (e.g., 'core')
        model_name: Model name (e.g., 'sitesettings')
        pk: Instance primary key
        field: Field name (e.g., 'site_logo')
        asset_id: MediaAsset UUID or null to clear
    """
    permission_classes = [IsAdminUser]

    # Whitelist of allowed model.field combinations for security
    # Add new entries as needed: ('app_label', 'model_name'): ['field1', 'field2']
    ALLOWED_FIELDS = {
        ('core', 'sitesettings'): ['site_logo', 'favicon'],
        ('catalog', 'category'): ['image_asset', 'banner_asset'],
        ('blog', 'blogpost'): ['featured_image', 'og_image'],
    }

    @extend_schema(
        tags=['Media Library'],
        summary=_("Auto-save media field value"),
        description=_("Auto-save a MediaAsset ForeignKey field on any whitelisted model. "
                    "Saves immediately on selection without requiring full form submission. "
                    "Admin users only. Only whitelisted model.field combinations are allowed."),
        request=inline_serializer(
            name='MediaAutoSaveRequest',
            fields={
                'app_label': drf_serializers.CharField(help_text='Django app label (e.g., "core")'),
                'model_name': drf_serializers.CharField(help_text='Model name (e.g., "sitesettings")'),
                'pk': drf_serializers.CharField(help_text='Instance primary key'),
                'field': drf_serializers.CharField(help_text='Field name (e.g., "site_logo")'),
                'asset_id': drf_serializers.UUIDField(required=False, allow_null=True, help_text='MediaAsset UUID or null to clear'),
            }
        ),
        responses={
            200: OpenApiResponse(description=_("Field saved successfully")),
            400: OpenApiResponse(description=_("Missing required parameters or field is not FK to MediaAsset")),
            403: OpenApiResponse(description=_("Field not whitelisted for auto-save")),
            404: OpenApiResponse(description=_("Model, field, instance, or media asset not found")),
        },
    )
    def post(self, request):
        app_label = request.data.get('app_label')
        model_name = request.data.get('model_name')
        pk = request.data.get('pk')
        field_name = request.data.get('field')
        asset_id = request.data.get('asset_id')

        # Validate required params
        if not all([app_label, model_name, pk, field_name]):
            return Response(
                {'error': _('Missing required parameters: app_label, model_name, pk, field')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Security: Check if this model.field is whitelisted
        allowed_fields = self.ALLOWED_FIELDS.get((app_label, model_name.lower()), [])
        if field_name not in allowed_fields:
            logger.warning(
                f"Auto-save attempt blocked for non-whitelisted field: "
                f"{app_label}.{model_name}.{field_name} by user {request.user}"
            )
            return Response(
                {'error': _('Field not allowed for auto-save')},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get model class
        try:
            model_class = apps.get_model(app_label, model_name)
        except LookupError:
            return Response(
                {'error': _('Model not found')},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate field exists and is ForeignKey to MediaAsset
        try:
            field = model_class._meta.get_field(field_name)
            if not (field.is_relation and field.related_model == MediaAsset):
                return Response(
                    {'error': _('Field must be ForeignKey to MediaAsset')},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except FieldDoesNotExist:
            return Response(
                {'error': _('Field not found on model')},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get instance
        try:
            instance = model_class.objects.get(pk=pk)
        except model_class.DoesNotExist:
            return Response(
                {'error': _('Instance not found')},
                status=status.HTTP_404_NOT_FOUND
            )

        # Set or clear the field using QuerySet.update() to bypass model's save() method
        # This avoids triggering full_clean() which some models (like SiteSettings) call in save()
        if asset_id:
            try:
                asset = MediaAsset.objects.get(id=asset_id)
            except MediaAsset.DoesNotExist:
                return Response(
                    {'error': _('Media asset not found')},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Use QuerySet.update() to bypass model save() and full_clean()
            model_class.objects.filter(pk=pk).update(**{field_name: asset})
        else:
            model_class.objects.filter(pk=pk).update(**{field_name: None})

        logger.info(
            f"Auto-saved {app_label}.{model_name}(pk={pk}).{field_name} = {asset_id} "
            f"by user {request.user}"
        )

        return Response({
            'success': True,
            'app_label': app_label,
            'model_name': model_name,
            'pk': str(pk),
            'field': field_name,
            'asset_id': str(asset_id) if asset_id else None,
        })


# =============================================================================
# CKEditor 5 Media Library Upload
# =============================================================================

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


@require_POST
@login_required
def ckeditor_media_library_upload(request):
    """
    CKEditor 5 upload endpoint that routes uploads through the Media Library.

    Accepts CKEditor's upload format (POST with 'upload' file field) and creates
    a MediaAsset with full processing (WebP conversion, thumbnails, metadata).

    Returns JSON: {"url": "..."} on success, {"error": {"message": "..."}} on failure.
    """
    if not request.user.is_staff:
        return JsonResponse(
            {"error": {"message": "Permission denied."}},
            status=403
        )

    uploaded_file = request.FILES.get('upload')
    if not uploaded_file:
        return JsonResponse(
            {"error": {"message": "No file uploaded."}},
            status=400
        )

    # Security: Check for blocked file types (HTML, SVG)
    import os
    from django.conf import settings

    filename = uploaded_file.name.lower()
    _, ext = os.path.splitext(filename)
    ext = ext.lstrip('.')  # Remove leading dot

    blocked_extensions = settings.MEDIA_LIBRARY_SETTINGS.get('BLOCKED_EXTENSIONS', [])
    if ext in blocked_extensions:
        return JsonResponse(
            {"error": {"message": f"File type '.{ext}' is not allowed for security reasons."}},
            status=400
        )

    # Validate it's an image
    from PIL import Image as PILImage
    try:
        uploaded_file.seek(0)
        PILImage.open(uploaded_file).verify()
        uploaded_file.seek(0)
    except Exception:
        return JsonResponse(
            {"error": {"message": "Invalid image file."}},
            status=400
        )

    try:
        from .serializers import MediaAssetCreateSerializer

        title = uploaded_file.name.rsplit('.', 1)[0] if '.' in uploaded_file.name else uploaded_file.name

        serializer = MediaAssetCreateSerializer(
            data={'original_file': uploaded_file, 'title': title},
            context={'request': request}
        )

        if serializer.is_valid():
            asset = serializer.save(uploaded_by=request.user)
            return JsonResponse({"url": asset.get_display_url()})
        else:
            logger.error(f"CKEditor upload validation failed: {serializer.errors}")
            return JsonResponse(
                {"error": {"message": "Upload validation failed."}},
                status=400
            )
    except Exception as e:
        logger.error(f"CKEditor media library upload failed: {e}")
        return JsonResponse(
            {"error": {"message": "Upload failed. Please try again."}},
            status=500
        )
