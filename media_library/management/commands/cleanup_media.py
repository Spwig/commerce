from django.core.management.base import BaseCommand
from django.db.models import Count
from media_library.models import MediaAsset, MediaThumbnail, MediaUsage
from tqdm import tqdm
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Clean up unused media files and orphaned thumbnails'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--unused-only',
            action='store_true',
            help='Only clean up unused assets (usage_count = 0)',
        )
        parser.add_argument(
            '--orphaned-only',
            action='store_true',
            help='Only clean up orphaned thumbnails',
        )
        parser.add_argument(
            '--missing-files',
            action='store_true',
            help='Clean up assets with missing files',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cleaned without making changes',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Number of items to process at once',
        )
    
    def handle(self, *args, **options):
        self.unused_only = options['unused_only']
        self.orphaned_only = options['orphaned_only']
        self.missing_files = options['missing_files']
        self.dry_run = options['dry_run']
        self.batch_size = options['batch_size']
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        if not any([self.unused_only, self.orphaned_only, self.missing_files]):
            # Run all cleanup tasks if none specified
            self.clean_unused_assets()
            self.clean_orphaned_thumbnails()
            self.clean_missing_files()
        else:
            if self.unused_only:
                self.clean_unused_assets()
            if self.orphaned_only:
                self.clean_orphaned_thumbnails()
            if self.missing_files:
                self.clean_missing_files()
        
        self.stdout.write(self.style.SUCCESS('Cleanup completed'))
    
    def clean_unused_assets(self):
        """Remove assets that are not used anywhere"""
        self.stdout.write('Cleaning unused assets...')
        
        # Find assets with no usage records
        unused_assets = MediaAsset.objects.annotate(
            usage_count_actual=Count('usages')
        ).filter(usage_count_actual=0)
        
        total = unused_assets.count()
        if total == 0:
            self.stdout.write('No unused assets found')
            return
        
        self.stdout.write(f'Found {total} unused assets')
        
        deleted = 0
        with tqdm(total=total, desc="Cleaning unused assets") as pbar:
            for asset in unused_assets.iterator(chunk_size=self.batch_size):
                try:
                    if self.dry_run:
                        self.stdout.write(f'Would delete: {asset.title}')
                    else:
                        # Delete associated files
                        self.delete_asset_files(asset)
                        asset.delete()
                        self.stdout.write(f'Deleted: {asset.title}')
                    
                    deleted += 1
                    pbar.update(1)
                    
                except Exception as e:
                    logger.error(f'Error deleting asset {asset.id}: {e}')
                    self.stdout.write(
                        self.style.ERROR(f'Error deleting {asset.title}: {e}')
                    )
        
        action = 'Would delete' if self.dry_run else 'Deleted'
        self.stdout.write(self.style.SUCCESS(f'{action} {deleted} unused assets'))
    
    def clean_orphaned_thumbnails(self):
        """Remove thumbnails that don't have a corresponding media asset"""
        self.stdout.write('Cleaning orphaned thumbnails...')
        
        # Find thumbnails without valid media assets
        orphaned = MediaThumbnail.objects.filter(media_asset__isnull=True)
        total = orphaned.count()
        
        if total == 0:
            self.stdout.write('No orphaned thumbnails found')
            return
        
        self.stdout.write(f'Found {total} orphaned thumbnails')
        
        if self.dry_run:
            self.stdout.write(f'Would delete {total} orphaned thumbnails')
        else:
            # Delete the thumbnails
            deleted_count = orphaned.delete()[0]
            self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} orphaned thumbnails'))
    
    def clean_missing_files(self):
        """Remove assets where the actual files are missing"""
        self.stdout.write('Cleaning assets with missing files...')
        
        assets = MediaAsset.objects.all()
        total = assets.count()
        
        if total == 0:
            self.stdout.write('No assets to check')
            return
        
        missing_files = []
        
        with tqdm(total=total, desc="Checking for missing files") as pbar:
            for asset in assets.iterator(chunk_size=self.batch_size):
                has_missing = False
                
                # Check original file
                if asset.original_file:
                    try:
                        if not os.path.exists(asset.original_file.path):
                            has_missing = True
                    except (ValueError, OSError):
                        has_missing = True
                else:
                    has_missing = True
                
                # Check WebP file
                if asset.webp_file:
                    try:
                        if not os.path.exists(asset.webp_file.path):
                            has_missing = True
                    except (ValueError, OSError):
                        has_missing = True
                
                if has_missing:
                    missing_files.append(asset)
                
                pbar.update(1)
        
        if not missing_files:
            self.stdout.write('No assets with missing files found')
            return
        
        self.stdout.write(f'Found {len(missing_files)} assets with missing files')
        
        deleted = 0
        for asset in missing_files:
            try:
                if self.dry_run:
                    self.stdout.write(f'Would delete: {asset.title} (missing files)')
                else:
                    asset.delete()
                    self.stdout.write(f'Deleted: {asset.title} (missing files)')
                
                deleted += 1
                
            except Exception as e:
                logger.error(f'Error deleting asset with missing files {asset.id}: {e}')
                self.stdout.write(
                    self.style.ERROR(f'Error deleting {asset.title}: {e}')
                )
        
        action = 'Would delete' if self.dry_run else 'Deleted'
        self.stdout.write(self.style.SUCCESS(f'{action} {deleted} assets with missing files'))
    
    def delete_asset_files(self, asset):
        """Delete all files associated with an asset"""
        try:
            # Delete original file
            if asset.original_file and os.path.exists(asset.original_file.path):
                os.remove(asset.original_file.path)
            
            # Delete WebP file
            if asset.webp_file and os.path.exists(asset.webp_file.path):
                os.remove(asset.webp_file.path)
            
            # Delete thumbnail files
            for thumbnail in asset.thumbnails.all():
                if thumbnail.file and os.path.exists(thumbnail.file.path):
                    os.remove(thumbnail.file.path)
                if thumbnail.webp_file and os.path.exists(thumbnail.webp_file.path):
                    os.remove(thumbnail.webp_file.path)
                    
        except Exception as e:
            logger.error(f'Error deleting files for asset {asset.id}: {e}')