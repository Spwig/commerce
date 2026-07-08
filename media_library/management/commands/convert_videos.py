from django.core.management.base import BaseCommand
from django.conf import settings
from media_library.models import MediaAsset
from media_library.video_services import VideoProcessor
import os
import tempfile
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Convert video assets to optimized WebM/AV1 format'

    def add_arguments(self, parser):
        parser.add_argument(
            '--asset-id',
            type=str,
            help='Convert specific asset by ID'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Convert all video assets without converted versions'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reconversion even if converted version exists'
        )
        parser.add_argument(
            '--format',
            type=str,
            default='webm_av1',
            choices=['webm_av1', 'webm_vp9', 'mp4_h265'],
            help='Target format for conversion'
        )
        parser.add_argument(
            '--crf',
            type=int,
            default=30,
            help='CRF value for quality (lower = better, 20-40 typical)'
        )

    def handle(self, *args, **options):
        processor = VideoProcessor()

        # Get videos to process
        if options['asset_id']:
            try:
                assets = [MediaAsset.objects.get(id=options['asset_id'])]
            except MediaAsset.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Asset {options['asset_id']} not found"))
                return
        elif options['all']:
            assets = MediaAsset.objects.filter(mime_type__startswith='video/')
            if not options['force']:
                assets = assets.filter(converted_video='')
        else:
            self.stdout.write(self.style.ERROR("Please specify --asset-id or --all"))
            return

        # Filter to only videos
        assets = [a for a in assets if a.is_video()]

        if not assets:
            self.stdout.write(self.style.WARNING("No video assets to process"))
            return

        self.stdout.write(f"Processing {len(assets)} video(s)...")

        for asset in assets:
            self.stdout.write(f"\nProcessing: {asset.title} ({asset.id})")

            # Skip if already converted (unless forced)
            if asset.converted_video and not options['force']:
                self.stdout.write(self.style.WARNING("  Already has converted version, skipping"))
                continue

            try:
                # Create temp file with original video
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(asset.original_file.name)[1]) as tmp_file:
                    asset.original_file.seek(0)
                    for chunk in asset.original_file.chunks():
                        tmp_file.write(chunk)
                    tmp_path = tmp_file.name

                # Generate poster if missing
                if not asset.poster_image:
                    self.stdout.write("  Generating poster image...")
                    poster_content = processor.extract_thumbnail(tmp_path)
                    if poster_content:
                        asset.poster_image.save(f"{asset.id}_poster.jpg", poster_content, save=True)
                        self.stdout.write(self.style.SUCCESS("  ✓ Poster generated"))

                # Convert video
                self.stdout.write(f"  Converting to {options['format']}...")

                if options['format'] == 'webm_av1':
                    converted_path = processor.convert_to_webm_av1(
                        tmp_path,
                        crf=options['crf'],
                        preset=6  # Balance between speed and compression
                    )
                    output_ext = '.webm'
                elif options['format'] == 'webm_vp9':
                    converted_path = processor.convert_to_webm_vp9(
                        tmp_path,
                        crf=options['crf']
                    )
                    output_ext = '.webm'
                else:  # mp4_h265
                    converted_path = processor.convert_to_mp4_h265(
                        tmp_path,
                        crf=options['crf']
                    )
                    output_ext = '.mp4'

                if converted_path and os.path.exists(converted_path):
                    # Get file sizes for comparison
                    original_size = os.path.getsize(tmp_path)
                    converted_size = os.path.getsize(converted_path)
                    reduction = (1 - converted_size / original_size) * 100

                    # Save converted file
                    with open(converted_path, 'rb') as f:
                        from django.core.files.base import ContentFile
                        content = ContentFile(f.read())
                        asset.converted_video.save(f"{asset.id}{output_ext}", content, save=True)

                    os.unlink(converted_path)

                    self.stdout.write(self.style.SUCCESS(
                        f"  ✓ Converted successfully! "
                        f"Size: {original_size/1024/1024:.1f}MB → {converted_size/1024/1024:.1f}MB "
                        f"({reduction:.1f}% reduction)"
                    ))
                else:
                    self.stdout.write(self.style.ERROR("  ✗ Conversion failed"))

                # Clean up temp file
                os.unlink(tmp_path)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Error: {str(e)}"))
                logger.error(f"Error converting video {asset.id}: {e}")
                continue

        self.stdout.write(self.style.SUCCESS("\n✓ Video conversion complete!"))