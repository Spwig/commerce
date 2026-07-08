import os

from django.conf import settings
from django.core.management.base import BaseCommand


# File extensions that benefit from compression
COMPRESSIBLE_EXTENSIONS = {'.css', '.js', '.svg', '.json', '.xml', '.html', '.txt', '.map'}


class Command(BaseCommand):
    help = 'Verify that static assets have pre-compressed Brotli (.br) and gzip (.gz) variants'

    def add_arguments(self, parser):
        parser.add_argument(
            '--top',
            type=int,
            default=10,
            help='Number of largest uncompressed files to show (default: 10)',
        )

    def handle(self, *args, **options):
        static_root = settings.STATIC_ROOT
        if not os.path.exists(static_root):
            self.stderr.write(self.style.ERROR(
                f'STATIC_ROOT does not exist: {static_root}\n'
                f'Run "python manage.py collectstatic" first.'
            ))
            return

        top_n = options['top']
        total_files = 0
        compressible_files = 0
        has_br = 0
        has_gz = 0
        has_both = 0
        original_size = 0
        br_size = 0
        gz_size = 0
        missing_br = []  # (path, size) tuples

        for dirpath, _dirnames, filenames in os.walk(static_root):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                _name, ext = os.path.splitext(filename)

                # Skip compressed variants themselves
                if ext in ('.br', '.gz'):
                    continue

                total_files += 1

                if ext.lower() not in COMPRESSIBLE_EXTENSIONS:
                    continue

                file_size = os.path.getsize(filepath)
                compressible_files += 1
                original_size += file_size

                br_path = filepath + '.br'
                gz_path = filepath + '.gz'
                file_has_br = os.path.exists(br_path)
                file_has_gz = os.path.exists(gz_path)

                if file_has_br:
                    has_br += 1
                    br_size += os.path.getsize(br_path)
                else:
                    missing_br.append((filepath, file_size))

                if file_has_gz:
                    has_gz += 1
                    gz_size += os.path.getsize(gz_path)

                if file_has_br and file_has_gz:
                    has_both += 1

        # Report
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Static Asset Compression Report'))
        self.stdout.write(f'  STATIC_ROOT: {static_root}')
        self.stdout.write(f'  Total files: {total_files}')
        self.stdout.write(f'  Compressible files: {compressible_files}')
        self.stdout.write('')

        if compressible_files == 0:
            self.stdout.write(self.style.WARNING('No compressible files found.'))
            return

        br_pct = (has_br / compressible_files * 100) if compressible_files else 0
        gz_pct = (has_gz / compressible_files * 100) if compressible_files else 0
        both_pct = (has_both / compressible_files * 100) if compressible_files else 0

        self.stdout.write(self.style.MIGRATE_HEADING('Coverage'))
        self.stdout.write(f'  Brotli (.br):  {has_br}/{compressible_files} ({br_pct:.0f}%)')
        self.stdout.write(f'  Gzip (.gz):    {has_gz}/{compressible_files} ({gz_pct:.0f}%)')
        self.stdout.write(f'  Both:          {has_both}/{compressible_files} ({both_pct:.0f}%)')
        self.stdout.write('')

        def fmt_size(size_bytes):
            if size_bytes >= 1024 * 1024:
                return f'{size_bytes / 1024 / 1024:.1f} MB'
            if size_bytes >= 1024:
                return f'{size_bytes / 1024:.1f} KB'
            return f'{size_bytes} B'

        self.stdout.write(self.style.MIGRATE_HEADING('Size Savings'))
        self.stdout.write(f'  Original total:  {fmt_size(original_size)}')
        if has_br and original_size:
            br_saving = (1 - br_size / original_size) * 100
            self.stdout.write(f'  Brotli total:    {fmt_size(br_size)} ({br_saving:.0f}% smaller)')
        if has_gz and original_size:
            gz_saving = (1 - gz_size / original_size) * 100
            self.stdout.write(f'  Gzip total:      {fmt_size(gz_size)} ({gz_saving:.0f}% smaller)')
        self.stdout.write('')

        # Show largest files missing Brotli compression
        if missing_br:
            missing_br.sort(key=lambda x: x[1], reverse=True)
            show = missing_br[:top_n]
            self.stdout.write(self.style.MIGRATE_HEADING(
                f'Top {len(show)} largest files without Brotli'
            ))
            rel_root = str(static_root)
            for filepath, size in show:
                rel_path = filepath[len(rel_root):] if filepath.startswith(rel_root) else filepath
                self.stdout.write(f'  {fmt_size(size):>10}  {rel_path}')
            self.stdout.write('')

        # Overall status
        if br_pct >= 95 and gz_pct >= 95:
            self.stdout.write(self.style.SUCCESS(
                'Compression coverage is excellent. '
                'Static assets are ready for production.'
            ))
        elif br_pct == 0 and gz_pct == 0:
            self.stdout.write(self.style.ERROR(
                'No compressed variants found. '
                'Ensure whitenoise[brotli] is installed and collectstatic has been run.'
            ))
        elif br_pct == 0:
            self.stdout.write(self.style.WARNING(
                'Gzip variants found but no Brotli. '
                'Install the Brotli pip package and re-run collectstatic.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'Partial coverage: {br_pct:.0f}% Brotli, {gz_pct:.0f}% gzip. '
                'Some files may be too small to benefit from compression.'
            ))
