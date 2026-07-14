"""
Create default image size presets for media library
"""

from django.core.management.base import BaseCommand

from media_library.models import ImageSizePreset


class Command(BaseCommand):
    help = "Create default image size presets"

    def handle(self, *args, **options):
        presets = [
            {
                "name": "Thumbnail",
                "slug": "thumbnail",
                "width": 150,
                "height": 150,
                "crop_mode": "cover",
                "quality": 85,
                "description": "Small thumbnail for listings",
            },
            {
                "name": "Small",
                "slug": "small",
                "width": 300,
                "height": 300,
                "crop_mode": "cover",
                "quality": 85,
                "description": "Small product image",
            },
            {
                "name": "Medium",
                "slug": "medium",
                "width": 600,
                "height": 600,
                "crop_mode": "contain",
                "quality": 85,
                "description": "Medium product image",
            },
            {
                "name": "Large",
                "slug": "large",
                "width": 1200,
                "height": 1200,
                "crop_mode": "contain",
                "quality": 90,
                "description": "Large product image for zoom",
            },
            {
                "name": "Gallery",
                "slug": "gallery",
                "width": 800,
                "height": 800,
                "crop_mode": "contain",
                "quality": 85,
                "description": "Gallery display size",
            },
        ]

        created_count = 0
        updated_count = 0

        for preset_data in presets:
            preset, created = ImageSizePreset.objects.update_or_create(
                slug=preset_data["slug"], defaults=preset_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Created preset: {preset.name} ({preset.width}x{preset.height})"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"↻ Updated preset: {preset.name} ({preset.width}x{preset.height})"
                    )
                )

        self.stdout.write()
        self.stdout.write(
            self.style.SUCCESS(
                f"Complete! Created {created_count}, Updated {updated_count} presets"
            )
        )
