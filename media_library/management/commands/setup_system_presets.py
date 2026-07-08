from django.core.management.base import BaseCommand
from media_library.models import ImageSizePreset


class Command(BaseCommand):
    help = 'Setup system image size presets'

    # Define all system presets
    # General presets use 'cover' mode (crop to fill)
    # Logo presets use 'pad' mode (preserve all content with transparent padding)
    SYSTEM_PRESETS = [
        # General image presets
        {'name': 'Thumbnail', 'display_name': 'Thumbnail', 'slug': 'thumbnail', 'width': 150, 'height': 150, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 10, 'description': 'Small thumbnails for lists and grids'},
        {'name': 'Small', 'display_name': 'Small', 'slug': 'small', 'width': 300, 'height': 300, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 20, 'description': 'Small images for cards and previews'},
        {'name': 'Medium', 'display_name': 'Medium', 'slug': 'medium', 'width': 600, 'height': 600, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 30, 'description': 'Medium images for content areas'},
        {'name': 'Large', 'display_name': 'Large', 'slug': 'large', 'width': 1200, 'height': 1200, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 40, 'description': 'Large images for detail views'},
        {'name': 'Gallery', 'display_name': 'Gallery', 'slug': 'gallery', 'width': 800, 'height': 800, 'crop_mode': 'cover', 'quality': 90, 'sort_order': 50},
        {'name': 'Hero', 'display_name': 'Hero', 'slug': 'hero', 'width': 1920, 'height': 1080, 'crop_mode': 'cover', 'quality': 90, 'sort_order': 60, 'description': 'Full-width hero banner images'},
        {'name': 'Banner', 'display_name': 'Banner', 'slug': 'banner', 'width': 1200, 'height': 400, 'crop_mode': 'cover', 'quality': 90, 'sort_order': 70, 'description': 'Wide banner images'},
        {'name': 'Card', 'display_name': 'Card', 'slug': 'card', 'width': 400, 'height': 300, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 80},
        {'name': 'Avatar', 'display_name': 'Avatar', 'slug': 'avatar', 'width': 200, 'height': 200, 'crop_mode': 'crop', 'quality': 85, 'sort_order': 90},
        # Product-specific presets
        {'name': 'Product Listing', 'display_name': 'Product Listing', 'slug': 'product_listing', 'width': 400, 'height': 400, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 100, 'description': 'Optimized for product grid and collection pages'},
        {'name': 'Product Detail', 'display_name': 'Product Detail', 'slug': 'product_detail', 'width': 1200, 'height': 1200, 'crop_mode': 'cover', 'quality': 90, 'sort_order': 110, 'description': 'High resolution for product detail pages'},
        {'name': 'Product Thumbnail', 'display_name': 'Product Thumbnail', 'slug': 'product_thumbnail', 'width': 100, 'height': 100, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 120, 'description': 'Small product thumbnails for mini cart and order items'},
        # Category presets
        {'name': 'Category Banner', 'display_name': 'Category Banner', 'slug': 'category_banner', 'width': 1920, 'height': 480, 'crop_mode': 'cover', 'quality': 90, 'sort_order': 130, 'description': 'Wide banners for category pages'},
        {'name': 'Category Thumbnail', 'display_name': 'Category Thumbnail', 'slug': 'category_thumbnail', 'width': 300, 'height': 200, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 140, 'description': 'Category preview images for listings'},
        # Logo presets - use 'pad' mode to preserve full logo content
        {'name': 'Logo Header', 'display_name': 'Logo Header', 'slug': 'logo_header', 'width': 300, 'height': 80, 'crop_mode': 'pad', 'padding_color': 'transparent', 'quality': 90, 'sort_order': 200, 'description': 'Site logo for header (preserves full logo)'},
        {'name': 'Logo Footer', 'display_name': 'Logo Footer', 'slug': 'logo_footer', 'width': 200, 'height': 60, 'crop_mode': 'pad', 'padding_color': 'transparent', 'quality': 90, 'sort_order': 210, 'description': 'Site logo for footer (preserves full logo)'},
        {'name': 'Logo Email', 'display_name': 'Logo Email', 'slug': 'logo_email', 'width': 400, 'height': 100, 'crop_mode': 'pad', 'padding_color': 'transparent', 'quality': 90, 'sort_order': 220, 'description': 'Site logo for email headers (preserves full logo)'},
        {'name': 'Logo Square', 'display_name': 'Logo Square', 'slug': 'logo_square', 'width': 160, 'height': 160, 'crop_mode': 'pad', 'padding_color': 'transparent', 'quality': 90, 'sort_order': 230, 'description': 'Site logo square variant (preserves full logo)'},
        {'name': 'Brand Logo', 'display_name': 'Brand Logo', 'slug': 'brand_logo', 'width': 200, 'height': 100, 'crop_mode': 'pad', 'padding_color': 'transparent', 'quality': 90, 'sort_order': 240, 'description': 'Brand/manufacturer logos (preserves full logo)'},
        # Announcement presets
        {'name': 'Announcement Banner', 'display_name': 'Announcement Banner', 'slug': 'announcement_banner', 'width': 800, 'height': 300, 'crop_mode': 'cover', 'quality': 90, 'sort_order': 300, 'description': 'Announcement modal banner image (above/below content)'},
        {'name': 'Announcement Background', 'display_name': 'Announcement Background', 'slug': 'announcement_background', 'width': 1200, 'height': 800, 'crop_mode': 'cover', 'quality': 85, 'sort_order': 310, 'description': 'Announcement modal background image (behind text with overlay)'},
        # Favicon presets - use 'pad' mode to preserve aspect ratio with transparent padding
        {'name': 'Favicon 16x16', 'display_name': 'Favicon 16x16', 'slug': 'favicon-16', 'width': 16, 'height': 16, 'crop_mode': 'pad', 'padding_color': 'transparent', 'quality': 90, 'sort_order': 400, 'description': 'Small favicon for browser tabs (16x16 PNG with transparency)'},
        {'name': 'Favicon 32x32', 'display_name': 'Favicon 32x32', 'slug': 'favicon-32', 'width': 32, 'height': 32, 'crop_mode': 'pad', 'padding_color': 'transparent', 'quality': 90, 'sort_order': 410, 'description': 'Standard favicon for browser tabs (32x32 PNG with transparency)'},
        {'name': 'Favicon 180x180', 'display_name': 'Favicon 180x180', 'slug': 'favicon-180', 'width': 180, 'height': 180, 'crop_mode': 'pad', 'padding_color': 'transparent', 'quality': 90, 'sort_order': 420, 'description': 'Apple touch icon for iOS home screen (180x180 PNG with transparency)'},
    ]

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for preset_data in self.SYSTEM_PRESETS:
            preset, created = ImageSizePreset.objects.get_or_create(
                slug=preset_data['slug'],
                defaults={
                    **preset_data,
                    'is_system_preset': True,
                    'is_active': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created system preset: {preset.name} ({preset.width}x{preset.height})')
                )
            else:
                # Update existing presets with new fields (display_name, sort_order, description)
                changed = False
                for field in ('display_name', 'sort_order', 'description'):
                    new_val = preset_data.get(field)
                    if new_val is not None and getattr(preset, field, None) != new_val:
                        # Only update if field is empty or is a new field
                        if not getattr(preset, field, None):
                            setattr(preset, field, new_val)
                            changed = True
                if not preset.is_system_preset:
                    preset.is_system_preset = True
                    changed = True
                if changed:
                    preset.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated system preset: {preset.name} ({preset.width}x{preset.height})')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⊙ Already up to date: {preset.name} ({preset.width}x{preset.height})')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Complete! Created {created_count}, updated {updated_count} system presets.')
        )
