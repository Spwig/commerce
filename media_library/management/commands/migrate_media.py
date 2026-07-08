from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.files.base import ContentFile
from media_library.models import MediaAsset, MediaFolder, Tag
from media_library.services import ImageProcessor
from catalog.models import Product, Category, Brand
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Migrate existing image files to media library'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without making changes',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Number of items to process at once',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force migration even if assets already exist',
        )
    
    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.batch_size = options['batch_size']
        self.force = options['force']
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Create default folders
        self.create_default_folders()
        
        # Migrate product images
        self.migrate_product_images()
        
        # Migrate category images
        self.migrate_category_images()
        
        # Migrate brand logos
        self.migrate_brand_logos()
        
        self.stdout.write(self.style.SUCCESS('Migration completed successfully'))
    
    def create_default_folders(self):
        """Create default folder structure"""
        folders = [
            ('products', 'Product Images'),
            ('categories', 'Category Images'),
            ('brands', 'Brand Logos'),
        ]
        
        for slug, name in folders:
            if not self.dry_run:
                folder, created = MediaFolder.objects.get_or_create(
                    slug=slug,
                    defaults={'name': name}
                )
                if created:
                    self.stdout.write(f'Created folder: {name}')
            else:
                self.stdout.write(f'Would create folder: {name}')
    
    def migrate_product_images(self):
        """Migrate product images from existing Product model"""
        self.stdout.write('Migrating product images...')
        
        products = Product.objects.filter(image__isnull=False).exclude(image='')
        total = products.count()
        
        if total == 0:
            self.stdout.write('No product images to migrate')
            return
        
        self.stdout.write(f'Found {total} products with images')
        
        folder = None
        if not self.dry_run:
            folder = MediaFolder.objects.get(slug='products')
        
        processor = ImageProcessor()
        migrated = 0
        
        for product in products.iterator(chunk_size=self.batch_size):
            try:
                # Check if already migrated
                if not self.force and hasattr(product, 'media_asset') and product.media_asset:
                    continue
                
                if self.dry_run:
                    self.stdout.write(f'Would migrate: {product.name} - {product.image.name}')
                    migrated += 1
                    continue
                
                with transaction.atomic():
                    # Create media asset
                    asset = MediaAsset(
                        title=f'{product.name} - Main Image',
                        alt_text=product.name,
                        description=f'Main image for {product.name}',
                        folder=folder,
                        is_public=True
                    )
                    
                    # Copy the file
                    if product.image and os.path.exists(product.image.path):
                        with open(product.image.path, 'rb') as img_file:
                            content = ContentFile(img_file.read())
                            asset.original_file.save(
                                os.path.basename(product.image.name),
                                content,
                                save=False
                            )
                        
                        # Process the image (extract metadata, generate WebP, etc.)
                        asset.width, asset.height = processor.get_image_dimensions(asset.original_file)
                        asset.file_size = asset.original_file.size
                        asset.metadata = processor.extract_metadata(asset.original_file)
                        asset.focal_point_x, asset.focal_point_y = processor.calculate_focal_point(asset.original_file)
                        
                        # Detect mime type
                        from PIL import Image
                        img = Image.open(asset.original_file)
                        asset.mime_type = f"image/{img.format.lower()}"
                        
                        asset.save()
                        
                        # Generate WebP and thumbnails
                        self.process_asset_files(asset, processor)
                        
                        # Link to product (you'll need to add this field to Product model)
                        # product.media_asset = asset
                        # product.save()
                        
                        migrated += 1
                        self.stdout.write(f'Migrated: {product.name}')
                    
            except Exception as e:
                logger.error(f'Error migrating product image {product.id}: {e}')
                self.stdout.write(
                    self.style.ERROR(f'Failed to migrate: {product.name} - {e}')
                )
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {migrated} product images'))
    
    def migrate_category_images(self):
        """Migrate category images"""
        self.stdout.write('Migrating category images...')
        
        categories = Category.objects.filter(image__isnull=False).exclude(image='')
        total = categories.count()
        
        if total == 0:
            self.stdout.write('No category images to migrate')
            return
        
        self.stdout.write(f'Found {total} categories with images')
        
        folder = None
        if not self.dry_run:
            folder = MediaFolder.objects.get(slug='categories')
        
        processor = ImageProcessor()
        migrated = 0
        
        for category in categories.iterator(chunk_size=self.batch_size):
            try:
                if self.dry_run:
                    self.stdout.write(f'Would migrate: {category.name} - {category.image.name}')
                    migrated += 1
                    continue
                
                with transaction.atomic():
                    asset = MediaAsset(
                        title=f'{category.name} - Category Image',
                        alt_text=category.name,
                        description=f'Image for {category.name} category',
                        folder=folder,
                        is_public=True
                    )
                    
                    if category.image and os.path.exists(category.image.path):
                        with open(category.image.path, 'rb') as img_file:
                            content = ContentFile(img_file.read())
                            asset.original_file.save(
                                os.path.basename(category.image.name),
                                content,
                                save=False
                            )
                        
                        # Process the image
                        asset.width, asset.height = processor.get_image_dimensions(asset.original_file)
                        asset.file_size = asset.original_file.size
                        asset.metadata = processor.extract_metadata(asset.original_file)
                        
                        from PIL import Image
                        img = Image.open(asset.original_file)
                        asset.mime_type = f"image/{img.format.lower()}"
                        
                        asset.save()
                        
                        # Generate WebP and thumbnails
                        self.process_asset_files(asset, processor)
                        
                        migrated += 1
                        self.stdout.write(f'Migrated: {category.name}')
                    
            except Exception as e:
                logger.error(f'Error migrating category image {category.id}: {e}')
                self.stdout.write(
                    self.style.ERROR(f'Failed to migrate: {category.name} - {e}')
                )
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {migrated} category images'))
    
    def migrate_brand_logos(self):
        """Migrate brand logos"""
        self.stdout.write('Migrating brand logos...')
        
        brands = Brand.objects.filter(logo__isnull=False).exclude(logo='')
        total = brands.count()
        
        if total == 0:
            self.stdout.write('No brand logos to migrate')
            return
        
        self.stdout.write(f'Found {total} brands with logos')
        
        folder = None
        if not self.dry_run:
            folder = MediaFolder.objects.get(slug='brands')
        
        processor = ImageProcessor()
        migrated = 0
        
        for brand in brands.iterator(chunk_size=self.batch_size):
            try:
                if self.dry_run:
                    self.stdout.write(f'Would migrate: {brand.name} - {brand.logo.name}')
                    migrated += 1
                    continue
                
                with transaction.atomic():
                    asset = MediaAsset(
                        title=f'{brand.name} - Logo',
                        alt_text=f'{brand.name} logo',
                        description=f'Logo for {brand.name} brand',
                        folder=folder,
                        is_public=True
                    )
                    
                    if brand.logo and os.path.exists(brand.logo.path):
                        with open(brand.logo.path, 'rb') as img_file:
                            content = ContentFile(img_file.read())
                            asset.original_file.save(
                                os.path.basename(brand.logo.name),
                                content,
                                save=False
                            )
                        
                        # Process the image
                        asset.width, asset.height = processor.get_image_dimensions(asset.original_file)
                        asset.file_size = asset.original_file.size
                        asset.metadata = processor.extract_metadata(asset.original_file)
                        
                        from PIL import Image
                        img = Image.open(asset.original_file)
                        asset.mime_type = f"image/{img.format.lower()}"
                        
                        asset.save()
                        
                        # Generate WebP and thumbnails
                        self.process_asset_files(asset, processor)
                        
                        migrated += 1
                        self.stdout.write(f'Migrated: {brand.name}')
                    
            except Exception as e:
                logger.error(f'Error migrating brand logo {brand.id}: {e}')
                self.stdout.write(
                    self.style.ERROR(f'Failed to migrate: {brand.name} - {e}')
                )
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {migrated} brand logos'))
    
    def process_asset_files(self, asset, processor):
        """Generate WebP and thumbnails for an asset"""
        try:
            # Generate WebP version
            if processor.webp_quality and asset.mime_type != 'image/webp':
                webp_content = processor.convert_to_webp(asset.original_file)
                if webp_content:
                    asset.webp_file.save(f"{asset.id}.webp", webp_content, save=True)
            
            # Generate thumbnails using ImageSizePreset for crop_mode and padding_color
            from media_library.models import MediaThumbnail, ImageSizePreset
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
                    
        except Exception as e:
            logger.error(f'Error processing asset files for {asset.id}: {e}')