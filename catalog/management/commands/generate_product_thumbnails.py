"""
Management command to generate thumbnails and WebP versions for product images
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Product, ProductImage
from media_library.models import MediaAsset, MediaThumbnail, ImageSizePreset
from media_library.services import ImageProcessor
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Generate thumbnails and WebP versions for all product images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--regenerate',
            action='store_true',
            help='Regenerate thumbnails even if they already exist',
        )

    def handle(self, *args, **options):
        regenerate = options['regenerate']

        # Get all media assets used by products
        product_images = ProductImage.objects.select_related('media_asset').all()
        media_assets = set()

        for img in product_images:
            if img.media_asset:
                media_assets.add(img.media_asset)

        self.stdout.write(f'Found {len(media_assets)} unique media assets used by products\n')

        if not media_assets:
            self.stdout.write(self.style.WARNING('No product images found'))
            return

        processor = ImageProcessor()
        # Get image size presets from database (configurable in Media Library → Image Size Presets)
        image_presets = list(ImageSizePreset.objects.filter(is_active=True))

        processed_count = 0
        skipped_count = 0
        error_count = 0

        for asset in tqdm(media_assets, desc="Processing images"):
            try:
                # Skip if not an image
                if not asset.is_image():
                    skipped_count += 1
                    continue

                # Generate WebP if it doesn't exist
                if not asset.webp_file and asset.original_file:
                    try:
                        webp_content = processor.convert_to_webp(asset.original_file)
                        if webp_content:
                            filename = f"{asset.id}.webp"
                            asset.webp_file.save(filename, webp_content, save=True)
                            self.stdout.write(f'  Generated WebP for {asset.title}')
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'  Failed to generate WebP for {asset.title}: {e}'))

                # Generate thumbnails
                for preset in image_presets:
                    # Check if thumbnail already exists
                    existing = MediaThumbnail.objects.filter(
                        media_asset=asset,
                        size_preset=preset.slug
                    ).first()

                    if existing and not regenerate:
                        continue

                    # Delete existing if regenerating
                    if existing and regenerate:
                        existing.delete()

                    # Generate thumbnail
                    try:
                        original_content, webp_content = processor.generate_thumbnail(
                            asset.original_file,
                            preset.width,
                            preset.height,
                            crop_mode=preset.crop_mode
                        )

                        if original_content:
                            thumbnail = MediaThumbnail.objects.create(
                                media_asset=asset,
                                size_preset=preset.slug,
                                width=preset.width,
                                height=preset.height
                            )
                            thumbnail.file.save(f"{asset.id}_{preset.slug}.jpg", original_content, save=False)
                            if webp_content:
                                thumbnail.webp_file.save(f"{asset.id}_{preset.slug}.webp", webp_content, save=False)
                            thumbnail.save()

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'  Failed to generate {preset.slug} thumbnail for {asset.title}: {e}'))
                        error_count += 1
                        continue

                processed_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing asset {asset.id}: {e}'))
                error_count += 1

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✅ Processing complete!'))
        self.stdout.write(f'  Processed: {processed_count}')
        self.stdout.write(f'  Skipped: {skipped_count}')
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f'  Errors: {error_count}'))
        self.stdout.write('='*50)
