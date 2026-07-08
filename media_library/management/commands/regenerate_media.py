from django.core.management.base import BaseCommand
from django.conf import settings
from media_library.models import MediaAsset, MediaThumbnail
from media_library.services import ImageProcessor
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Regenerate WebP versions and thumbnails for existing media assets'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--webp-only',
            action='store_true',
            help='Only regenerate WebP versions',
        )
        parser.add_argument(
            '--thumbnails-only',
            action='store_true',
            help='Only regenerate thumbnails',
        )
        parser.add_argument(
            '--asset-ids',
            nargs='+',
            help='Specific asset IDs to regenerate',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='Number of assets to process at once',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regeneration even if files exist',
        )
    
    def handle(self, *args, **options):
        self.webp_only = options['webp_only']
        self.thumbnails_only = options['thumbnails_only']
        self.asset_ids = options.get('asset_ids')
        self.batch_size = options['batch_size']
        self.force = options['force']
        
        # Get assets to process
        queryset = MediaAsset.objects.all()
        if self.asset_ids:
            queryset = queryset.filter(id__in=self.asset_ids)
        
        total = queryset.count()
        if total == 0:
            self.stdout.write('No assets to process')
            return
        
        self.stdout.write(f'Processing {total} assets...')
        
        processor = ImageProcessor()
        processed = 0
        errors = 0
        
        # Use tqdm for progress bar
        with tqdm(total=total, desc="Processing assets") as pbar:
            for asset in queryset.iterator(chunk_size=self.batch_size):
                try:
                    if not self.thumbnails_only:
                        self.regenerate_webp(asset, processor)
                    
                    if not self.webp_only:
                        self.regenerate_thumbnails(asset, processor)
                    
                    processed += 1
                    pbar.set_postfix({'processed': processed, 'errors': errors})
                    
                except Exception as e:
                    errors += 1
                    logger.error(f'Error processing asset {asset.id}: {e}')
                    self.stdout.write(
                        self.style.ERROR(f'Error processing {asset.title}: {e}')
                    )
                
                pbar.update(1)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Completed! Processed: {processed}, Errors: {errors}'
            )
        )
    
    def regenerate_webp(self, asset, processor):
        """Regenerate WebP version for an asset"""
        if not asset.original_file:
            return
        
        # Skip if WebP already exists and not forcing
        if asset.webp_file and not self.force:
            return
        
        # Skip if original is already WebP
        if asset.mime_type == 'image/webp':
            return
        
        try:
            webp_content = processor.convert_to_webp(asset.original_file)
            if webp_content:
                asset.webp_file.save(f"{asset.id}.webp", webp_content, save=True)
                self.stdout.write(f'Generated WebP for: {asset.title}')
        except Exception as e:
            logger.error(f'Error generating WebP for asset {asset.id}: {e}')
            raise
    
    def regenerate_thumbnails(self, asset, processor):
        """Regenerate thumbnails for an asset"""
        from media_library.models import ImageSizePreset

        if not asset.original_file:
            return

        # Delete existing thumbnails if forcing
        if self.force:
            asset.thumbnails.all().delete()

        # Get thumbnail presets from database (includes crop_mode and padding_color)
        presets = ImageSizePreset.objects.filter(is_active=True)

        for preset in presets:
            # Skip if thumbnail already exists and not forcing
            if not self.force and asset.thumbnails.filter(size_preset=preset.slug).exists():
                continue

            try:
                asset.original_file.seek(0)
                original_content, webp_content = processor.generate_thumbnail(
                    asset.original_file,
                    preset.width,
                    preset.height,
                    crop_mode=preset.crop_mode,
                    padding_color=getattr(preset, 'padding_color', None)
                )

                if original_content:
                    # Delete existing thumbnail for this size
                    MediaThumbnail.objects.filter(
                        media_asset=asset,
                        size_preset=preset.slug
                    ).delete()

                    # Determine file extension based on crop mode
                    ext = 'png' if preset.crop_mode == 'pad' and getattr(preset, 'padding_color', 'transparent') == 'transparent' else 'jpg'

                    # Create new thumbnail
                    thumbnail = MediaThumbnail.objects.create(
                        media_asset=asset,
                        size_preset=preset.slug,
                        width=preset.width,
                        height=preset.height
                    )

                    thumbnail.file.save(
                        f"{asset.id}_{preset.slug}.{ext}",
                        original_content,
                        save=False
                    )

                    if webp_content:
                        thumbnail.webp_file.save(
                            f"{asset.id}_{preset.slug}.webp",
                            webp_content,
                            save=False
                        )

                    thumbnail.save()

            except Exception as e:
                logger.error(f'Error generating {preset.slug} thumbnail for asset {asset.id}: {e}')
                raise

        self.stdout.write(f'Generated thumbnails for: {asset.title}')