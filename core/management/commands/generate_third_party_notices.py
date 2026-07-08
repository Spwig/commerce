"""
Management command to generate THIRD_PARTY_NOTICES.txt from installed packages.

Run this before Docker builds to ensure the attributions file is up to date.

Usage:
    python manage.py generate_third_party_notices
    python manage.py generate_third_party_notices --output /custom/path.txt
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate THIRD_PARTY_NOTICES.txt from installed Python packages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output', '-o',
            type=str,
            default=None,
            help='Output file path (default: BASE_DIR/THIRD_PARTY_NOTICES.txt)',
        )
        parser.add_argument(
            '--requirements',
            type=str,
            default=None,
            help='Path to requirements.txt (default: BASE_DIR/requirements.txt)',
        )

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)
        output_path = Path(options['output']) if options['output'] else base_dir / 'THIRD_PARTY_NOTICES.txt'
        requirements_path = Path(options['requirements']) if options['requirements'] else base_dir / 'requirements.txt'

        # Ensure pip-licenses is available
        self.stdout.write("Checking pip-licenses availability...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'piplicenses', '--version'],
                capture_output=True, check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.stdout.write(self.style.WARNING("Installing pip-licenses..."))
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pip-licenses', '--quiet'],
                check=True,
            )

        # Generate raw license data
        self.stdout.write("Collecting license data from installed packages...")
        result = subprocess.run(
            [
                sys.executable, '-m', 'piplicenses',
                '--format=json',
                '--with-urls',
                '--with-description',
                '--with-license-file',
                '--no-license-path',
            ],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            self.stderr.write(self.style.ERROR(f"pip-licenses failed: {result.stderr}"))
            return

        all_packages = json.loads(result.stdout)
        self.stdout.write(f"Found {len(all_packages)} installed packages")

        # Parse requirements.txt for direct dependencies
        direct_deps = set()
        if requirements_path.exists():
            with open(requirements_path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    m = re.match(r'^([a-zA-Z0-9_.-]+)', line)
                    if m:
                        direct_deps.add(self._normalize(m.group(1)))

        # Categorize
        direct = []
        transitive = []
        normalized_direct = {d.replace('-', '') for d in direct_deps}
        for pkg in all_packages:
            name_norm = self._normalize(pkg.get('Name', ''))
            if name_norm in direct_deps or name_norm.replace('-', '') in normalized_direct:
                direct.append(pkg)
            else:
                transitive.append(pkg)

        direct.sort(key=lambda p: p['Name'].lower())
        transitive.sort(key=lambda p: p['Name'].lower())

        # License type summary
        license_counts = {}
        for pkg in all_packages:
            lic_key = self._classify_license(pkg.get('License', 'UNKNOWN'))
            license_counts[lic_key] = license_counts.get(lic_key, 0) + 1

        # Build output
        self.stdout.write("Generating notices file...")
        content = self._build_notices(direct, transitive, license_counts)

        output_path.write_text(content, encoding='utf-8')
        size_kb = len(content.encode('utf-8')) / 1024
        self.stdout.write(self.style.SUCCESS(
            f"Written: {output_path} "
            f"({len(direct)} direct + {len(transitive)} transitive deps, "
            f"{size_kb:.0f} KB)"
        ))

    @staticmethod
    def _normalize(name):
        return name.lower().replace('_', '-').replace('.', '-')

    @staticmethod
    def _classify_license(lic):
        if 'MIT' in lic:
            return 'MIT'
        if 'BSD' in lic:
            return 'BSD'
        if 'Apache' in lic:
            return 'Apache 2.0'
        if 'PSF' in lic or 'Python' in lic:
            return 'PSF'
        if 'LGPL' in lic:
            return 'LGPL'
        if 'GPL' in lic:
            return 'GPL'
        if 'ISC' in lic:
            return 'ISC'
        if 'MPL' in lic:
            return 'MPL'
        return lic

    def _build_notices(self, direct, transitive, license_counts):
        lines = []
        sep = "=" * 78
        dash = "-" * 78

        lines.append(sep)
        lines.append("THIRD-PARTY SOFTWARE NOTICES AND ATTRIBUTIONS")
        lines.append(sep)
        lines.append("")
        lines.append("Spwig eCommerce Platform")
        lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}")
        lines.append("")
        lines.append("This file lists the third-party software packages used by the Spwig")
        lines.append("eCommerce Platform, along with their respective licenses.")
        lines.append("")

        # Summary table
        lines.append(dash)
        lines.append("LICENSE SUMMARY")
        lines.append(dash)
        lines.append("")
        summary = sorted(license_counts.items(), key=lambda x: -x[1])
        total = sum(v for _, v in summary)
        lines.append(f"{'License Type':<40} {'Count':>6} {'%':>6}")
        lines.append(f"{'-'*40} {'-'*6} {'-'*6}")
        for lic, count in summary:
            pct = f"{count/total*100:.1f}%"
            lines.append(f"{lic:<40} {count:>6} {pct:>6}")
        lines.append(f"{'-'*40} {'-'*6} {'-'*6}")
        lines.append(f"{'TOTAL':<40} {total:>6}")
        lines.append("")

        # Direct dependencies
        lines.append(sep)
        lines.append(f"DIRECT DEPENDENCIES ({len(direct)} packages)")
        lines.append(sep)
        lines.append("")
        lines.append("These packages are explicitly required by Spwig and listed in")
        lines.append("requirements.txt.")
        lines.append("")
        self._write_packages(lines, direct)

        # Transitive dependencies
        lines.append("")
        lines.append(sep)
        lines.append(f"TRANSITIVE DEPENDENCIES ({len(transitive)} packages)")
        lines.append(sep)
        lines.append("")
        lines.append("These packages are indirect dependencies required by the direct")
        lines.append("dependencies listed above.")
        lines.append("")
        self._write_packages(lines, transitive)

        lines.append("")
        lines.append(sep)
        lines.append("END OF THIRD-PARTY NOTICES")
        lines.append(sep)

        return '\n'.join(lines)

    @staticmethod
    def _write_packages(lines, packages):
        for pkg in packages:
            lines.append("-" * 78)
            lines.append(f"Package:  {pkg.get('Name', '')} {pkg.get('Version', '')}")
            lines.append(f"License:  {pkg.get('License', 'UNKNOWN')}")
            url = pkg.get('URL', '')
            if url:
                lines.append(f"URL:      {url}")
            desc = pkg.get('Description', '')
            if desc:
                lines.append(f"About:    {desc[:120]}")
            lines.append("")

            license_text = pkg.get('LicenseText', '').strip()
            if license_text and license_text != 'UNKNOWN':
                for lt_line in license_text.split('\n'):
                    lines.append(f"  {lt_line}")
                lines.append("")
