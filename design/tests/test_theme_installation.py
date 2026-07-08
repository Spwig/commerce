"""
Unit Tests for Theme Installation with Bundled Components
Tests the theme installation flow including component extraction and registration.
"""

import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from design.theme_service import ThemeService
from design.theme_models import Theme, ThemeInstallation
from design.models import ComponentStore
from component_updates.models import ComponentRegistry

User = get_user_model()


class TestThemeInstallationWithBundledComponents(TestCase):
    """Test theme installation extracts and installs bundled components"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123'
        )
        self.temp_dir = Path(tempfile.mkdtemp())
        self.service = ThemeService()

    def tearDown(self):
        """Clean up temporary files"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def create_test_theme_package(self, include_components=True, component_count=2):
        """
        Helper method to create a test theme package with bundled components.

        Args:
            include_components: Whether to include bundled components
            component_count: Number of components to bundle

        Returns:
            Path to the created ZIP file
        """
        theme_dir = self.temp_dir / 'test-theme'
        theme_dir.mkdir(parents=True, exist_ok=True)

        # Create theme manifest
        manifest = {
            'name': 'test-theme',
            'version': '1.0.0',
            'display_name': 'Test Theme',
            'description': 'A test theme with bundled components',
            'author': 'Test Author',
            'license': 'MIT',
        }

        if include_components:
            manifest['bundled_components'] = []

            for i in range(component_count):
                component_name = f'test_component_{i + 1}'
                component_type = 'header' if i == 0 else 'footer'
                component_path = f'components/{component_type}s/{component_name}'

                # Add to manifest
                manifest['bundled_components'].append({
                    'type': component_type,
                    'name': component_name,
                    'path': component_path
                })

                # Create component files
                comp_dir = theme_dir / component_path
                comp_dir.mkdir(parents=True, exist_ok=True)

                # Component manifest
                comp_manifest = {
                    'name': component_name,
                    'version': '1.0.0',
                    'display_name': f'Test Component {i + 1}',
                    'description': f'Test component {i + 1}',
                    'component_type': component_type,
                    'author': 'Test Author',
                }
                with open(comp_dir / 'manifest.json', 'w') as f:
                    json.dump(comp_manifest, f, indent=2)

                # Component template
                with open(comp_dir / 'template.html', 'w') as f:
                    f.write(f'<div>Test {component_type} {i + 1}</div>')

                # Component schema
                comp_schema = {
                    'settings': [
                        {
                            'id': 'test_setting',
                            'type': 'text',
                            'label': 'Test Setting',
                            'default': 'test value'
                        }
                    ]
                }
                with open(comp_dir / 'schema.json', 'w') as f:
                    json.dump(comp_schema, f, indent=2)

        # Write theme manifest
        with open(theme_dir / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)

        # Create theme package ZIP
        zip_path = self.temp_dir / 'test-theme-1.0.0.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in theme_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(theme_dir)
                    zipf.write(file_path, arcname)

        return zip_path

    def test_extract_bundled_components_success(self):
        """Test successful extraction of bundled components"""
        # Create theme package with 2 components
        package_path = self.create_test_theme_package(include_components=True, component_count=2)

        # Create a Theme instance
        theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

        # Extract bundled components
        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('test-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Verify components were created in ComponentStore
        components = ComponentStore.objects.filter(source_theme=theme)
        self.assertEqual(components.count(), 2)

        # Verify component details
        header_component = components.filter(component_type='header').first()
        self.assertIsNotNone(header_component)
        self.assertEqual(header_component.slug, 'test_component_1')
        self.assertEqual(header_component.version, '1.0.0')
        self.assertEqual(header_component.review_status, 'approved')  # Auto-approved

        footer_component = components.filter(component_type='footer').first()
        self.assertIsNotNone(footer_component)
        self.assertEqual(footer_component.slug, 'test_component_2')
        self.assertEqual(footer_component.version, '1.0.0')

    def test_extract_bundled_components_creates_registry_entries(self):
        """Test that bundled components are registered in ComponentRegistry"""
        package_path = self.create_test_theme_package(include_components=True, component_count=2)

        theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('test-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Verify ComponentRegistry entries
        registry_entries = ComponentRegistry.objects.filter(
            component_type__in=['header', 'footer']
        )
        self.assertEqual(registry_entries.count(), 2)

        # Verify registry details
        header_registry = registry_entries.filter(component_type='header').first()
        self.assertIsNotNone(header_registry)
        self.assertEqual(header_registry.current_version, '1.0.0')
        self.assertTrue(header_registry.name.startswith('Test Component'))

    def test_extract_bundled_components_no_components(self):
        """Test theme with no bundled components"""
        package_path = self.create_test_theme_package(include_components=False)

        theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('test-theme-1.0.0.zip', f.read())
            # Should not raise error
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Verify no components were created
        components = ComponentStore.objects.filter(source_theme=theme)
        self.assertEqual(components.count(), 0)

    def test_extract_bundled_components_invalid_component(self):
        """Test extraction handles invalid components gracefully"""
        # Create package with valid components
        package_path = self.create_test_theme_package(include_components=True, component_count=2)

        # Modify package to corrupt one component
        with zipfile.ZipFile(package_path, 'a') as zipf:
            # Remove schema.json from first component to make it invalid
            zipf.remove('components/headers/test_component_1/schema.json')

        theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('test-theme-1.0.0.zip', f.read())
            # Should continue even if one component is invalid
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Only valid component should be created
        components = ComponentStore.objects.filter(source_theme=theme)
        self.assertEqual(components.count(), 1)
        self.assertEqual(components.first().component_type, 'footer')

    def test_theme_bundled_component_methods(self):
        """Test Theme model methods for bundled components"""
        theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

        # Create some bundled components
        for i in range(3):
            ComponentStore.objects.create(
                component_type='section',
                slug=f'test_section_{i}',
                display_name=f'Test Section {i}',
                description='Test section component',
                version='1.0.0',
                author='Test Author',
                review_status='approved',
                source_theme=theme
            )

        # Test get_bundled_components()
        components = theme.get_bundled_components()
        self.assertEqual(components.count(), 3)

        # Test bundled_component_count property
        self.assertEqual(theme.bundled_component_count, 3)

        # Test get_bundled_component_info()
        info = theme.get_bundled_component_info()
        self.assertEqual(len(info), 3)
        self.assertEqual(info[0]['component_type'], 'section')
        self.assertEqual(info[0]['version'], '1.0.0')
        self.assertTrue(info[0]['is_installed'])

    def test_component_checksum_calculation(self):
        """Test that component checksums are calculated correctly"""
        package_path = self.create_test_theme_package(include_components=True, component_count=1)

        theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('test-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        component = ComponentStore.objects.filter(source_theme=theme).first()
        self.assertIsNotNone(component)
        self.assertIsNotNone(component.checksum)
        self.assertTrue(component.checksum.startswith('sha256:'))

    def test_duplicate_component_handling(self):
        """Test handling of duplicate component installations"""
        package_path = self.create_test_theme_package(include_components=True, component_count=1)

        theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

        # Install components twice
        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('test-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('test-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Should not create duplicates
        components = ComponentStore.objects.filter(source_theme=theme)
        self.assertEqual(components.count(), 1)

    def test_component_auto_approval(self):
        """Test that bundled components are automatically approved"""
        package_path = self.create_test_theme_package(include_components=True, component_count=2)

        theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('test-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # All components should be auto-approved
        components = ComponentStore.objects.filter(source_theme=theme)
        for component in components:
            self.assertEqual(component.review_status, 'approved')


class TestThemeModelBundledComponentIntegration(TestCase):
    """Test Theme model integration with bundled components"""

    def setUp(self):
        """Set up test fixtures"""
        self.theme = Theme.objects.create(
            slug='test-theme',
            name='Test Theme',
            version='1.0.0',
            author='Test Author'
        )

    def test_theme_with_no_bundled_components(self):
        """Test theme with no bundled components"""
        self.assertEqual(self.theme.bundled_component_count, 0)
        self.assertEqual(len(self.theme.get_bundled_component_info()), 0)

    def test_theme_with_multiple_component_types(self):
        """Test theme with multiple types of bundled components"""
        # Create components of different types
        component_types = ['header', 'footer', 'section', 'utility']
        for comp_type in component_types:
            ComponentStore.objects.create(
                component_type=comp_type,
                slug=f'test_{comp_type}',
                display_name=f'Test {comp_type.title()}',
                description=f'Test {comp_type} component',
                version='1.0.0',
                author='Test Author',
                review_status='approved',
                source_theme=self.theme
            )

        self.assertEqual(self.theme.bundled_component_count, 4)

        info = self.theme.get_bundled_component_info()
        types_in_info = [comp['component_type'] for comp in info]
        self.assertEqual(set(types_in_info), set(component_types))

    def test_component_source_theme_relationship(self):
        """Test bidirectional relationship between theme and components"""
        # Create bundled components
        comp1 = ComponentStore.objects.create(
            component_type='header',
            slug='test_header',
            display_name='Test Header',
            description='Test header component',
            version='1.0.0',
            author='Test Author',
            review_status='approved',
            source_theme=self.theme
        )

        # Test forward relationship (Theme -> Components)
        self.assertIn(comp1, self.theme.get_bundled_components())

        # Test reverse relationship (Component -> Theme)
        self.assertEqual(comp1.source_theme, self.theme)
        self.assertEqual(comp1.source_theme.slug, 'test-theme')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
