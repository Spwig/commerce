"""
Management command to download carrier logos from worldvectorlogo.com

Usage:
    python manage.py download_carrier_logos [options]

Options:
    --limit N          Process only first N carriers
    --slug SLUG        Process only specific carrier slug
    --skip-existing    Skip carriers that already have logos
    --dry-run          Show what would be downloaded without downloading
"""

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from shipping.models import CarrierPreset
from PIL import Image
from io import BytesIO
import requests
import time


class Command(BaseCommand):
    help = 'Download and process carrier logos from worldvectorlogo.com'

    # Mapping of carrier slugs to worldvectorlogo.com identifiers
    LOGO_MAP = {
        # Global carriers
        'dhl-sg': 'dhl',
        'dhl-jp': 'dhl',
        'dhl-ae': 'dhl',
        'fedex-sg': 'fedex',
        'fedex-jp': 'fedex',
        'fedex-us': 'fedex',
        'fedex-ca': 'fedex',
        'ups-sg': 'ups-logo',
        'ups-us': 'ups-logo',
        'ups-ca': 'ups-logo',
        'aramex-sg': 'aramex',
        'aramex-ae': 'aramex',
        'aramex-au': 'aramex',
        'aramex-nz': 'aramex',
        'aramex-za': 'aramex',
        'aramex-eg': 'aramex',
        'aramex-sa': 'aramex',

        # Singapore
        'ninjavan-sg': 'ninja-van',
        'singpost': 'singapore-post',
        'jtexpress-sg': 'jt-express',
        'qxpress': 'qxpress',

        # Malaysia
        'poslaju': 'pos-malaysia',
        'jtexpress-my': 'jt-express',
        'ninjavan-my': 'ninja-van',
        'citylink': 'citylink-express',
        'gdex': 'gdex',

        # Indonesia
        'jne': 'jne',
        'pos-indonesia': 'pos-indonesia',
        'tiki': 'tiki',
        'jtexpress-id': 'jt-express',
        'sicepat': 'sicepat',

        # Philippines
        'lbc': 'lbc-express',
        '2go': '2go',
        'jtexpress-ph': 'jt-express',
        'ninjavan-ph': 'ninja-van',
        'jrs': 'jrs-express',

        # Thailand
        'thailand-post': 'thailand-post',
        'kerry-express': 'kerry-express',
        'jtexpress-th': 'jt-express',
        'flash-express': 'flash-express',
        'ninjavan-th': 'ninja-van',

        # Vietnam
        'vnpost': 'vietnam-post',
        'viettel-post': 'viettel-post',

        # India
        'india-post': 'india-post',
        'blue-dart': 'blue-dart',
        'dtdc': 'dtdc',
        'delhivery': 'delhivery',

        # Japan
        'japan-post': 'japan-post',
        'yamato': 'yamato-transport',
        'sagawa': 'sagawa-express',

        # Australia
        'australia-post': 'australia-post',
        'startrack': 'startrack',
        'sendle': 'sendle',

        # United States
        'usps': 'usps',
        'ontrac': 'ontrac',

        # Canada
        'canada-post': 'canada-post',
        'purolator': 'purolator',

        # UK
        'royal-mail': 'royal-mail',
        'parcelforce': 'parcelforce',
        'dpd-uk': 'dpd',
        'evri': 'evri',
        'yodel': 'yodel',

        # Europe
        'dhl-paket': 'deutsche-post',
        'dpd-de': 'dpd',
        'hermes-de': 'hermes',
        'gls-de': 'gls',
        'colissimo': 'la-poste',
        'chronopost': 'chronopost',
        'postnl': 'postnl',
        'bpost': 'bpost',
        'postnord-se': 'postnord',
        'postnord-no': 'postnord',
        'postnord-dk': 'postnord',
        'posti': 'posti',
        'correos': 'correos',
        'poste-italiane': 'poste-italiane',

        # Add more as needed...
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Process only first N carriers',
        )
        parser.add_argument(
            '--slug',
            type=str,
            help='Process only specific carrier slug',
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip carriers that already have logos',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be downloaded without downloading',
        )

    def handle(self, *args, **options):
        limit = options.get('limit')
        slug_filter = options.get('slug')
        skip_existing = options.get('skip_existing', False)
        dry_run = options.get('dry_run', False)

        # Build queryset
        queryset = CarrierPreset.objects.filter(is_system=True)

        if slug_filter:
            queryset = queryset.filter(slug=slug_filter)

        if skip_existing:
            queryset = queryset.filter(logo='')

        if limit:
            queryset = queryset[:limit]

        total = queryset.count()

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No files will be downloaded'))

        self.stdout.write(f'\n📥 Processing {total} carrier(s)\n')

        success_count = 0
        skip_count = 0
        fail_count = 0

        for i, carrier in enumerate(queryset, 1):
            # Check if logo mapping exists
            logo_id = self.LOGO_MAP.get(carrier.slug)

            if not logo_id:
                self.stdout.write(
                    f'[{i}/{total}] ⚠️  {carrier.name} ({carrier.slug}) - No logo mapping'
                )
                skip_count += 1
                continue

            if dry_run:
                self.stdout.write(
                    f'[{i}/{total}] 🔍 {carrier.name} ({carrier.slug}) → {logo_id}'
                )
                success_count += 1
                continue

            # Download and process logo
            try:
                logo_content = self.download_logo(logo_id)

                if logo_content:
                    # Process the logo (resize, add padding)
                    processed_logo = self.process_logo(logo_content)

                    # Save to carrier
                    filename = f'{carrier.slug}.webp'
                    carrier.logo.save(filename, ContentFile(processed_logo), save=True)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[{i}/{total}] ✅ {carrier.name} ({carrier.slug}) → {logo_id}'
                        )
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        f'[{i}/{total}] ❌ {carrier.name} ({carrier.slug}) - Download failed'
                    )
                    fail_count += 1

                # Rate limiting
                time.sleep(1)

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'[{i}/{total}] ❌ {carrier.name} ({carrier.slug}) - Error: {e}'
                    )
                )
                fail_count += 1

        # Summary
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS('✅ LOGO DOWNLOAD COMPLETE'))
        self.stdout.write('=' * 80)
        self.stdout.write(f'\nResults:')
        self.stdout.write(f'  ✅ Success: {success_count}/{total}')
        self.stdout.write(f'  ⚠️  Skipped: {skip_count}/{total}')
        self.stdout.write(f'  ❌ Failed: {fail_count}/{total}\n')

    def download_logo(self, logo_id):
        """Download logo from worldvectorlogo.com"""
        # Try SVG first
        svg_url = f'https://worldvectorlogo.com/logo/{logo_id}.svg'

        try:
            response = requests.get(svg_url, timeout=10)
            if response.status_code == 200:
                # Return SVG content as-is
                return response.content
        except requests.RequestException:
            pass

        # Try PNG fallback
        png_url = f'https://worldvectorlogo.com/download/logo/{logo_id}.png'

        try:
            response = requests.get(png_url, timeout=10)
            if response.status_code == 200:
                return response.content
        except requests.RequestException:
            pass

        return None

    def process_logo(self, logo_content):
        """
        Process logo to fit within 200x200px canvas with transparent background.

        - Keeps SVG as-is
        - Converts raster images to WebP
        - Maintains aspect ratio
        - Centers on 200x200 canvas with transparent padding
        """
        # Check if SVG
        if logo_content.startswith(b'<?xml') or logo_content.startswith(b'<svg'):
            # Return SVG as-is (no processing needed)
            return logo_content

        # Process raster image
        try:
            img = Image.open(BytesIO(logo_content))

            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # Resize to fit within 180x180 (leaving 20px total padding)
            img.thumbnail((180, 180), Image.Resampling.LANCZOS)

            # Create 200x200 transparent canvas
            canvas = Image.new('RGBA', (200, 200), (0, 0, 0, 0))

            # Center logo on canvas
            x = (200 - img.width) // 2
            y = (200 - img.height) // 2
            canvas.paste(img, (x, y), img)

            # Save as WebP
            output = BytesIO()
            canvas.save(output, 'WEBP', quality=90)
            return output.getvalue()

        except Exception as e:
            self.stderr.write(f'Error processing image: {e}')
            return None
