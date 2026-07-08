"""
Management command to create the default theme
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
import json
import hashlib
from pathlib import Path
import zipfile
import tempfile
from django.core.files import File

class Command(BaseCommand):
    help = 'Creates the default theme with comprehensive base tokens'

    def handle(self, *args, **options):
        from design.theme_models import Theme, ThemeBranding

        # Check if default theme already exists
        if Theme.objects.filter(slug='default').exists():
            self.stdout.write(self.style.WARNING('Default theme already exists'))
            return

        # Define comprehensive default tokens
        manifest = {
            "name": "Default Theme",
            "slug": "default",
            "version": "1.0.0",
            "description": "The default shop theme with comprehensive design tokens",
            "author": "Shop Platform",
            "author_email": "themes@shop.com",
            "engine": {
                "min_version": "1.0.0"
            },
            "tokens": {
                "colors": {
                    "primary": "#3B82F6",
                    "primary-light": "#60A5FA",
                    "primary-dark": "#2563EB",
                    "secondary": "#8B5CF6",
                    "secondary-light": "#A78BFA",
                    "secondary-dark": "#7C3AED",
                    "accent": "#EC4899",
                    "accent-light": "#F472B6",
                    "accent-dark": "#DB2777",
                    "success": "#10B981",
                    "success-light": "#34D399",
                    "success-dark": "#059669",
                    "warning": "#F59E0B",
                    "warning-light": "#FBBf24",
                    "warning-dark": "#D97706",
                    "error": "#EF4444",
                    "error-light": "#F87171",
                    "error-dark": "#DC2626",
                    "info": "#3B82F6",
                    "info-light": "#60A5FA",
                    "info-dark": "#2563EB",
                    "text": "#1F2937",
                    "text-light": "#6B7280",
                    "text-muted": "#9CA3AF",
                    "text-inverse": "#FFFFFF",
                    "background": "#FFFFFF",
                    "background-secondary": "#F9FAFB",
                    "background-tertiary": "#F3F4F6",
                    "surface": "#FFFFFF",
                    "surface-secondary": "#F9FAFB",
                    "border": "#E5E7EB",
                    "border-light": "#F3F4F6",
                    "border-dark": "#D1D5DB",
                    "shadow": "rgba(0, 0, 0, 0.1)",
                    "overlay": "rgba(0, 0, 0, 0.5)"
                },
                "typography": {
                    "font-family-heading": "Inter, system-ui, -apple-system, sans-serif",
                    "font-family-body": "Inter, system-ui, -apple-system, sans-serif",
                    "font-family-mono": "Menlo, Monaco, Consolas, monospace",
                    "font-size-xs": "0.75rem",
                    "font-size-sm": "0.875rem",
                    "font-size-base": "1rem",
                    "font-size-lg": "1.125rem",
                    "font-size-xl": "1.25rem",
                    "font-size-2xl": "1.5rem",
                    "font-size-3xl": "1.875rem",
                    "font-size-4xl": "2.25rem",
                    "font-size-5xl": "3rem",
                    "font-size-6xl": "3.75rem",
                    "font-weight-thin": "100",
                    "font-weight-light": "300",
                    "font-weight-normal": "400",
                    "font-weight-medium": "500",
                    "font-weight-semibold": "600",
                    "font-weight-bold": "700",
                    "font-weight-extrabold": "800",
                    "font-weight-black": "900",
                    "line-height-none": "1",
                    "line-height-tight": "1.25",
                    "line-height-snug": "1.375",
                    "line-height-base": "1.5",
                    "line-height-relaxed": "1.625",
                    "line-height-loose": "2",
                    "letter-spacing-tighter": "-0.05em",
                    "letter-spacing-tight": "-0.025em",
                    "letter-spacing-normal": "0",
                    "letter-spacing-wide": "0.025em",
                    "letter-spacing-wider": "0.05em",
                    "letter-spacing-widest": "0.1em"
                },
                "spacing": {
                    "0": "0",
                    "px": "1px",
                    "0.5": "0.125rem",
                    "1": "0.25rem",
                    "1.5": "0.375rem",
                    "2": "0.5rem",
                    "2.5": "0.625rem",
                    "3": "0.75rem",
                    "3.5": "0.875rem",
                    "4": "1rem",
                    "5": "1.25rem",
                    "6": "1.5rem",
                    "7": "1.75rem",
                    "8": "2rem",
                    "9": "2.25rem",
                    "10": "2.5rem",
                    "11": "2.75rem",
                    "12": "3rem",
                    "14": "3.5rem",
                    "16": "4rem",
                    "20": "5rem",
                    "24": "6rem",
                    "28": "7rem",
                    "32": "8rem",
                    "36": "9rem",
                    "40": "10rem",
                    "44": "11rem",
                    "48": "12rem",
                    "52": "13rem",
                    "56": "14rem",
                    "60": "15rem",
                    "64": "16rem",
                    "72": "18rem",
                    "80": "20rem",
                    "96": "24rem"
                },
                "borders": {
                    "width-0": "0",
                    "width-1": "1px",
                    "width-2": "2px",
                    "width-4": "4px",
                    "width-8": "8px",
                    "radius-none": "0",
                    "radius-sm": "0.125rem",
                    "radius-base": "0.25rem",
                    "radius-md": "0.375rem",
                    "radius-lg": "0.5rem",
                    "radius-xl": "0.75rem",
                    "radius-2xl": "1rem",
                    "radius-3xl": "1.5rem",
                    "radius-full": "9999px"
                },
                "shadows": {
                    "none": "none",
                    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                    "base": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
                    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                    "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
                    "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)"
                },
                "animations": {
                    "duration-75": "75ms",
                    "duration-100": "100ms",
                    "duration-150": "150ms",
                    "duration-200": "200ms",
                    "duration-300": "300ms",
                    "duration-500": "500ms",
                    "duration-700": "700ms",
                    "duration-1000": "1000ms",
                    "easing-linear": "linear",
                    "easing-in": "cubic-bezier(0.4, 0, 1, 1)",
                    "easing-out": "cubic-bezier(0, 0, 0.2, 1)",
                    "easing-in-out": "cubic-bezier(0.4, 0, 0.2, 1)"
                },
                "breakpoints": {
                    "xs": "0",
                    "sm": "640px",
                    "md": "768px",
                    "lg": "1024px",
                    "xl": "1280px",
                    "2xl": "1536px"
                },
                "z-index": {
                    "0": "0",
                    "10": "10",
                    "20": "20",
                    "30": "30",
                    "40": "40",
                    "50": "50",
                    "auto": "auto"
                }
            },
            "assets": {
                "css": ["css/default.css"],
                "js": [],
                "images": []
            }
        }

        # Create the default CSS file content
        css_content = self.generate_css_from_tokens(manifest['tokens'])

        # Create a temporary theme package
        with tempfile.TemporaryDirectory() as temp_dir:
            theme_dir = Path(temp_dir) / 'theme'
            theme_dir.mkdir()

            # Write manifest
            manifest_path = theme_dir / 'manifest.json'
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)

            # Create CSS directory and file
            css_dir = theme_dir / 'css'
            css_dir.mkdir()
            css_file = css_dir / 'default.css'
            with open(css_file, 'w') as f:
                f.write(css_content)

            # Create ZIP package
            zip_path = Path(temp_dir) / 'default-theme.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in theme_dir.rglob('*'):
                    if file.is_file():
                        arcname = str(file.relative_to(temp_dir))
                        zipf.write(file, arcname)

            # Calculate checksum
            with open(zip_path, 'rb') as f:
                checksum = hashlib.sha256(f.read()).hexdigest()

            # Create Theme model instance
            with open(zip_path, 'rb') as f:
                theme = Theme.objects.create(
                    name="Default Theme",
                    slug="default",
                    description="The default shop theme with comprehensive design tokens",
                    version="1.0.0",
                    engine_min_version="1.0.0",
                    author="Shop Platform",
                    author_email="themes@shop.com",
                    manifest=manifest,
                    package_file=File(f, name='default-theme.zip'),
                    package_checksum=checksum,
                    is_active=True,
                    is_default=True,
                    installed_at=timezone.now()
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully created default theme: {theme}'))

            # Update existing branding to use this theme
            from design.theme_models import ThemeBranding
            branding = ThemeBranding.objects.first()
            if branding and not branding.theme:
                branding.theme = theme
                branding.save()
                self.stdout.write(self.style.SUCCESS('Updated existing branding to use default theme'))

    def generate_css_from_tokens(self, tokens):
        """Generate CSS from token definitions"""
        css_lines = ['/* Default Theme CSS Variables */\n', ':root {']

        # Process each token category
        for category, values in tokens.items():
            if category in ['colors', 'typography', 'spacing', 'borders', 'shadows', 'animations']:
                css_lines.append(f'\n  /* {category.title()} */')
                for key, value in values.items():
                    css_var = f"--{key.replace('_', '-')}"
                    css_lines.append(f"  {css_var}: {value};")

        css_lines.append('}')

        # Add base styles
        css_lines.extend([
            '\n/* Base Styles */',
            'body {',
            '  font-family: var(--font-family-body);',
            '  font-size: var(--font-size-base);',
            '  line-height: var(--line-height-base);',
            '  color: var(--text);',
            '  background: var(--background);',
            '}',
            '',
            'h1, h2, h3, h4, h5, h6 {',
            '  font-family: var(--font-family-heading);',
            '  font-weight: var(--font-weight-bold);',
            '  line-height: var(--line-height-tight);',
            '  color: var(--text);',
            '}',
            '',
            'a {',
            '  color: var(--primary);',
            '  text-decoration: none;',
            '  transition: color var(--duration-200) var(--easing-in-out);',
            '}',
            '',
            'a:hover {',
            '  color: var(--primary-dark);',
            '}',
        ])

        return '\n'.join(css_lines)