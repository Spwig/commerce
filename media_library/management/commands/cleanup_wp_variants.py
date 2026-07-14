"""
Cleanup WordPress image size variants that were imported as separate MediaAsset records.

WordPress generates multiple size variants for each uploaded image (e.g., image-300x169.jpg,
image-768x432.jpg, image-1024x575.jpg). During WooCommerce migration, these were imported as
separate MediaAsset records instead of only importing the original.

This command identifies and removes these orphaned variant assets.
"""

import logging

from django.core.management.base import BaseCommand

from media_library.models import MediaAsset, MediaThumbnail

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Remove WordPress image size variants imported as separate MediaAsset records"

    # Matches titles ending with dimensions like " 300X169", " 1024X575", " 1536X863"
    VARIANT_TITLE_REGEX = r"\d+X\d+$"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN — no changes will be made\n"))

        # Find variant assets by title pattern
        variant_assets = MediaAsset.objects.filter(title__regex=self.VARIANT_TITLE_REGEX)
        total_variants = variant_assets.count()

        if total_variants == 0:
            self.stdout.write(
                self.style.SUCCESS("No WordPress size variants found. Nothing to clean up.")
            )
            return

        self.stdout.write(f"Found {total_variants} potential WordPress size variant assets\n")

        # Verify none are referenced by products or blog posts
        from django.apps import apps

        referenced_ids = set()

        # Check ProductImage references
        try:
            ProductImage = apps.get_model("catalog", "ProductImage")
            product_refs = ProductImage.objects.filter(media_asset__in=variant_assets).values_list(
                "media_asset_id", flat=True
            )
            referenced_ids.update(product_refs)
        except LookupError:
            pass

        # Check BlogPost featured_image references
        try:
            BlogPost = apps.get_model("blog", "BlogPost")
            blog_refs = BlogPost.objects.filter(featured_image__in=variant_assets).values_list(
                "featured_image_id", flat=True
            )
            referenced_ids.update(blog_refs)
        except LookupError:
            pass

        # Check MediaUsage references
        from media_library.models import MediaUsage

        usage_refs = MediaUsage.objects.filter(media_asset__in=variant_assets).values_list(
            "media_asset_id", flat=True
        )
        referenced_ids.update(usage_refs)

        if referenced_ids:
            self.stdout.write(
                self.style.WARNING(
                    f"  Skipping {len(referenced_ids)} variant(s) that are referenced by other models"
                )
            )
            variant_assets = variant_assets.exclude(id__in=referenced_ids)

        deletable_count = variant_assets.count()
        self.stdout.write(f"  {deletable_count} variant assets are safe to delete\n")

        if deletable_count == 0:
            return

        # Count associated thumbnails
        thumbnail_count = MediaThumbnail.objects.filter(media_asset__in=variant_assets).count()
        self.stdout.write(f"  {thumbnail_count} associated thumbnails will also be deleted\n")

        if dry_run:
            # Show sample of what would be deleted
            self.stdout.write("\nSample of assets to delete:")
            for asset in variant_assets[:10]:
                self.stdout.write(f'  - "{asset.title}" ({asset.file_size} bytes)')
            if deletable_count > 10:
                self.stdout.write(f"  ... and {deletable_count - 10} more")
            return

        # Delete files from storage, then records
        deleted_files = 0
        deleted_thumbs = 0

        for asset in variant_assets.prefetch_related("thumbnails").iterator(chunk_size=100):
            # Delete thumbnail files
            for thumb in asset.thumbnails.all():
                if thumb.file:
                    thumb.file.delete(save=False)
                if thumb.webp_file:
                    thumb.webp_file.delete(save=False)
                deleted_thumbs += 1

            # Delete asset files
            if asset.original_file:
                asset.original_file.delete(save=False)
            if asset.webp_file:
                asset.webp_file.delete(save=False)
            deleted_files += 1

        # Bulk delete records (thumbnails cascade from asset FK)
        variant_assets.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCleanup complete:"
                f"\n  Deleted {deleted_files} variant assets"
                f"\n  Deleted {deleted_thumbs} associated thumbnails"
            )
        )
