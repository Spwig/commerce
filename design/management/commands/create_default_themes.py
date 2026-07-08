"""
Management command to create 5 default theme presets
Creates professional themes for different store types

Reads tokens from components/themes/{slug}/tokens.json
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files import File
from django.conf import settings
import json
import hashlib
from pathlib import Path
import zipfile
import tempfile


class Command(BaseCommand):
    help = 'Creates default theme presets for all bundled themes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreate themes even if they exist (deletes and recreates)',
        )

    def handle(self, *args, **options):
        from design.theme_models import Theme

        force = options.get('force', False)

        themes_to_create = [
            self.get_starter_theme(),
            self.get_elegant_shop_theme(),
            self.get_modern_shop_theme(),
            self.get_modern_dark_theme(),
            self.get_tech_theme(),
            self.get_apparel_theme(),
            self.get_space_theme(),
            self.get_botanica_theme(),
            self.get_artisan_theme(),
            self.get_nature_theme(),
            self.get_bold_theme(),
            self.get_vivid_theme(),
        ]

        created_count = 0
        updated_count = 0
        for theme_data in themes_to_create:
            existing = Theme.objects.filter(slug=theme_data['slug']).first()
            if existing:
                if force:
                    existing.delete()
                    self.stdout.write(self.style.WARNING(f"Deleted existing theme '{theme_data['slug']}'"))
                else:
                    self.stdout.write(self.style.WARNING(f"Theme '{theme_data['slug']}' already exists, skipping (use --force to recreate)"))
                    continue

            theme = self.create_theme_package(theme_data)
            if theme:
                if force and existing:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"✓ Recreated: {theme.name}"))
                else:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"✓ Created: {theme.name}"))

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully created {created_count} and recreated {updated_count} theme presets"))

    def load_tokens_from_filesystem(self, slug: str) -> dict:
        """Load tokens from installed theme or dev components directory."""
        # Try installed location first (Docker / production)
        installed_path = Path(settings.BASE_DIR) / 'components_data' / 'static' / 'design' / 'themes' / slug / 'current' / 'theme' / 'tokens.json'
        if installed_path.exists():
            with open(installed_path, 'r') as f:
                return json.load(f)

        # Fall back to dev source (spwig-components project, flat layout)
        components_dir = Path(getattr(settings, 'SPWIG_COMPONENTS_DIR', settings.BASE_DIR / 'components'))
        dev_path = components_dir / 'themes' / slug / 'tokens.json'
        if dev_path.exists():
            with open(dev_path, 'r') as f:
                return json.load(f)
        return None

    def load_css_from_filesystem(self, slug: str) -> str:
        """Load pre-generated CSS from installed theme or dev components directory."""
        # Try installed location first (Docker / production)
        installed_path = Path(settings.BASE_DIR) / 'components_data' / 'static' / 'design' / 'themes' / slug / 'current' / 'theme' / 'css' / 'theme.css'
        if installed_path.exists():
            with open(installed_path, 'r') as f:
                return f.read()

        # Fall back to dev source (spwig-components project, flat layout)
        components_dir = Path(getattr(settings, 'SPWIG_COMPONENTS_DIR', settings.BASE_DIR / 'components'))
        dev_path = components_dir / 'themes' / slug / 'css' / 'tokens.css'
        if dev_path.exists():
            with open(dev_path, 'r') as f:
                return f.read()
        return None

    def create_theme_package(self, theme_data):
        """Create a complete theme package with manifest, tokens, and CSS"""
        from design.theme_models import Theme

        manifest = theme_data['manifest']
        tokens = theme_data['tokens']

        with tempfile.TemporaryDirectory() as temp_dir:
            theme_dir = Path(temp_dir) / 'theme'
            theme_dir.mkdir()

            # Write manifest.json
            manifest_path = theme_dir / 'manifest.json'
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)

            # Write tokens.json
            tokens_path = theme_dir / 'tokens.json'
            with open(tokens_path, 'w') as f:
                json.dump(tokens, f, indent=2)

            # Create CSS directory and theme.css
            # Use pre-generated tokens.css from filesystem (has correct --theme- prefix)
            css_dir = theme_dir / 'css'
            css_dir.mkdir()
            css_file = css_dir / 'theme.css'
            css_content = self.load_css_from_filesystem(theme_data['slug'])
            if not css_content:
                # Fallback to generating CSS if filesystem file doesn't exist
                self.stdout.write(self.style.WARNING(
                    f"No tokens.css found for {theme_data['slug']}, using generated CSS"
                ))
                css_content = self.generate_css_from_tokens(tokens, theme_data['slug'])
            with open(css_file, 'w') as f:
                f.write(css_content)

            # Create ZIP package
            zip_filename = f"{theme_data['slug']}.zip"
            zip_path = Path(temp_dir) / zip_filename
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
                # Set Starter Theme as default
                is_default = (manifest['slug'] == 'starter')

                theme = Theme.objects.create(
                    name=manifest['name'],
                    slug=manifest['slug'],
                    description=manifest['description'],
                    version=manifest['version'],
                    engine_min_version=manifest['engine']['min'],
                    author=manifest['author'],
                    author_email=manifest['author_email'],
                    manifest=manifest,
                    package_file=File(f, name=zip_filename),
                    package_checksum=checksum,
                    is_active=True,
                    is_default=is_default,
                    installed_at=timezone.now()
                )

            # Ensure ComponentRegistry entry exists for theme management page
            self._ensure_component_registry(theme_data, manifest)

            # Set as active theme in GlobalDesignSettings if it's the default
            # and no active theme has been explicitly set yet
            if is_default:
                try:
                    from design.models import GlobalDesignSettings
                    settings_obj = GlobalDesignSettings.get_settings()
                    if not settings_obj.active_theme_id:
                        settings_obj.active_theme = theme
                        settings_obj.save(update_fields=['active_theme'])
                        self.stdout.write(self.style.SUCCESS(
                            f"  Set '{theme.slug}' as active theme in GlobalDesignSettings"
                        ))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f"  Could not set active theme in GlobalDesignSettings: {e}"
                    ))

            return theme

    def _ensure_component_registry(self, theme_data, manifest):
        """Ensure a ComponentRegistry entry exists so the theme appears in the unified theme management page."""
        from component_updates.models import ComponentRegistry

        slug = theme_data['slug']
        existing = ComponentRegistry.objects.filter(
            component_type='theme', slug=slug
        ).first()

        if not existing:
            ComponentRegistry.objects.create(
                component_type='theme',
                slug=slug,
                name=manifest['name'],
                description=manifest.get('description', ''),
                current_version=manifest.get('version', '1.0.0'),
                latest_version=manifest.get('version', '1.0.0'),
                update_available=False,
                author=manifest.get('author', 'Spwig'),
                author_details={
                    'name': manifest.get('author', 'Spwig'),
                    'email': manifest.get('author_email', 'themes@spwig.com'),
                    'verified': True,
                },
                locked=False,
            )

    def generate_css_from_tokens(self, tokens, theme_slug):
        """Generate CSS with all token variables using --theme- prefix.

        Note: This is a fallback method. Prefer using pre-generated tokens.css
        from components/themes/{slug}/css/tokens.css which is generated
        by the generate_tokens_css management command.
        """
        css_lines = [
            f'/* {theme_slug} Theme - Generated CSS Variables */',
            '/* DO NOT EDIT - Generated from tokens.json */',
            '',
            ':root {',
        ]

        # Colors
        if 'colors' in tokens:
            css_lines.append('  /* Colors */')
            for key, value in tokens['colors'].items():
                css_var = f"--theme-color-{key.replace('_', '-')}"
                css_lines.append(f"  {css_var}: {value};")
            css_lines.append('')

        # Typography
        if 'typography' in tokens:
            css_lines.append('  /* Typography */')
            for key, value in tokens['typography'].items():
                css_var = f"--theme-{key.replace('_', '-')}"
                css_lines.append(f"  {css_var}: {value};")
            css_lines.append('')

        # Spacing
        if 'spacing' in tokens:
            css_lines.append('  /* Spacing */')
            for key, value in tokens['spacing'].items():
                css_var = f"--theme-space-{key}"
                css_lines.append(f"  {css_var}: {value};")
            css_lines.append('')

        # Borders
        if 'borders' in tokens:
            css_lines.append('  /* Borders */')
            for key, value in tokens['borders'].items():
                if key.startswith('width'):
                    css_var = f"--theme-border-{key.replace('_', '-')}"
                else:
                    css_var = f"--theme-{key.replace('_', '-')}"
                css_lines.append(f"  {css_var}: {value};")
            css_lines.append('')

        # Shadows
        if 'shadows' in tokens:
            css_lines.append('  /* Shadows */')
            for key, value in tokens['shadows'].items():
                css_var = f"--theme-shadow-{key}"
                css_lines.append(f"  {css_var}: {value};")
            css_lines.append('')

        # Transitions (was animations)
        if 'transitions' in tokens:
            css_lines.append('  /* Transitions */')
            for key, value in tokens['transitions'].items():
                css_var = f"--theme-transition-{key.replace('_', '-')}"
                css_lines.append(f"  {css_var}: {value};")
            css_lines.append('')
        elif 'animations' in tokens:
            # Legacy support for animations key
            css_lines.append('  /* Animations */')
            for key, value in tokens['animations'].items():
                css_var = f"--theme-transition-{key.replace('_', '-')}"
                css_lines.append(f"  {css_var}: {value};")
            css_lines.append('')

        # Menu tokens
        if 'menu' in tokens:
            css_lines.append('  /* Menu */')
            for key, value in tokens['menu'].items():
                css_var = f"--theme-menu-{key.replace('_', '-')}"
                css_lines.append(f"  {css_var}: {value};")
            css_lines.append('')

        # Element tokens (Page Builder)
        if 'elements' in tokens:
            css_lines.append('  /* Element Tokens (Page Builder) */')
            category_order = [
                ('hero', 'Hero Section'),
                ('button', 'Button'),
                ('card', 'Card'),
                ('divider', 'Divider'),
                ('form', 'Form'),
                ('accordion', 'Accordion'),
                ('modal', 'Modal'),
                ('countdown', 'Countdown'),
                ('testimonial', 'Testimonial'),
                ('blog', 'Blog'),
                ('product', 'Product'),
                ('voucher', 'Voucher'),
                ('heading', 'Heading'),
                ('image', 'Image'),
                ('gallery', 'Gallery'),
            ]
            for category, display_name in category_order:
                if category in tokens['elements']:
                    css_lines.append(f'  /* {display_name} */')
                    for key, value in tokens['elements'][category].items():
                        css_lines.append(f'  --theme-element-{category}-{key}: {value};')
                    css_lines.append('')

        css_lines.append('}')
        css_lines.append('')

        # Add base theme styles
        css_lines.extend([
            '/* Base Theme Styles */',
            'body {',
            '  font-family: var(--theme-font-family-body);',
            '  font-size: var(--theme-font-size-base);',
            '  line-height: var(--theme-line-height-base);',
            '  color: var(--theme-color-text);',
            '  background: var(--theme-color-background);',
            '}',
            '',
            'h1, h2, h3, h4, h5, h6 {',
            '  font-family: var(--theme-font-family-heading);',
            '  font-weight: var(--theme-font-weight-bold);',
            '  line-height: var(--theme-line-height-tight);',
            '  color: var(--theme-color-text);',
            '}',
        ])

        return '\n'.join(css_lines)

    def get_starter_theme(self):
        """Starter Theme - Clean, minimal base theme with all element tokens"""
        slug = 'starter'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Starter Theme',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Clean, minimal base theme. A great starting point for customization.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,  # Include tokens in manifest for DesignToken sync
            },
            'tokens': tokens,
        }

    def get_elegant_shop_theme(self):
        """Elegant Shop - Ultra minimal light theme (Spwig default)"""
        slug = 'elegant-shop'
        # Load tokens from filesystem (includes element tokens)
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Elegant Shop',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Ultra minimal, clean light theme with premium aesthetics. Perfect for luxury and high-end brands.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,  # Include tokens in manifest for DesignToken sync
            },
            'tokens': tokens,
        }

    def get_modern_shop_theme(self):
        """Modern Shop - Contemporary light e-commerce theme"""
        slug = 'modern-shop'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Modern Shop',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Clean, modern light theme perfect for contemporary e-commerce stores.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,  # Include tokens in manifest for DesignToken sync
            },
            'tokens': tokens,
        }

    def get_modern_dark_theme(self):
        """Modern Dark - Dark version of Modern Shop"""
        slug = 'modern-dark'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Modern Dark',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Sleek dark theme with vibrant accents. Perfect for modern tech-savvy audiences.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,  # Include tokens in manifest for DesignToken sync
            },
            'tokens': tokens,
        }

    def get_tech_theme(self):
        """Tech Theme - Dark futuristic theme"""
        slug = 'tech-theme'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Tech Theme',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Futuristic dark theme with electric accents. Perfect for electronics and tech stores.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,  # Include tokens in manifest for DesignToken sync
            },
            'tokens': tokens,
        }

    def get_apparel_theme(self):
        """Apparel Theme - Fashion-focused light theme"""
        slug = 'apparel-theme'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Apparel Theme',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Elegant fashion theme with warm tones. Perfect for clothing and fashion stores.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,  # Include tokens in manifest for DesignToken sync
            },
            'tokens': tokens,
        }

    def get_space_theme(self):
        """Space Theme - Deep dark void with electric lime energy"""
        slug = 'space-theme'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Space Theme',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Deep space void meets electric lime energy. A dark, angular theme for tech stores, gaming, and high-impact brands.',
                'author': 'Spwig',
                'author_email': 'support@spwig.com',
                'license': 'Proprietary',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/tokens.css', 'css/theme.css']},
                'tokens': tokens,
            },
            'tokens': tokens,
        }

    def get_botanica_theme(self):
        """Botanica - Warm botanical luxury for beauty, cosmetics & wellness"""
        slug = 'botanica'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Botanica',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Warm, botanical luxury theme with dusty rose accents and elegant serif headings. Perfect for beauty, cosmetics, skincare, wellness, and spa brands.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,
            },
            'tokens': tokens,
        }

    def get_artisan_theme(self):
        """Artisan - Warm rustic-modern for food, beverage & craft"""
        slug = 'artisan'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Artisan',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Warm, rustic-modern theme with rich earth tones and elegant serif headings. Perfect for food, beverage, bakeries, cafes, wine shops, and artisan craft stores.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,
            },
            'tokens': tokens,
        }

    def get_nature_theme(self):
        """Nature - Natural organic for home, garden & eco-friendly"""
        slug = 'nature'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Nature',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Natural, organic theme with sage greens and earthy tones. Perfect for home decor, garden, furniture, eco-friendly products, candles, and wellness brands.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,
            },
            'tokens': tokens,
        }

    def get_bold_theme(self):
        """Bold - High-contrast angular for sports, outdoor & fitness"""
        slug = 'bold'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Bold',
                'slug': slug,
                'version': '1.0.0',
                'description': 'High-contrast, action-oriented theme with electric orange and sharp edges. Perfect for sporting goods, gym equipment, outdoor gear, fitness supplements, and activewear.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,
            },
            'tokens': tokens,
        }

    def get_vivid_theme(self):
        """Vivid - Playful colorful for kids, toys & creative"""
        slug = 'vivid'
        tokens = self.load_tokens_from_filesystem(slug)
        if not tokens:
            self.stdout.write(self.style.ERROR(f"Could not load tokens for {slug} from filesystem"))
            tokens = {}

        return {
            'slug': slug,
            'manifest': {
                'name': 'Vivid',
                'slug': slug,
                'version': '1.0.0',
                'description': 'Playful, colorful theme with vibrant purple and sunny accents. Perfect for toy stores, kids clothing, art supplies, party supplies, and creative goods.',
                'author': 'Spwig',
                'author_email': 'themes@spwig.com',
                'license': 'MIT',
                'engine': {'min': '1.0.0'},
                'assets': {'css': ['css/theme.css']},
                'tokens': tokens,
            },
            'tokens': tokens,
        }
