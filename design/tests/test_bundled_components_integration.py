"""
Integration Tests for Bundled Components
Tests the complete workflow of theme installation with bundled components.
"""

import json
import shutil
import tempfile
import zipfile
from pathlib import Path

import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from design.theme_service import ThemeService
from design.theme_models import Theme, ThemeInstallation
from design.models import ComponentStore
from component_updates.models import ComponentRegistry

User = get_user_model()


class TestBundledComponentsIntegration(TestCase):
    """Integration tests for bundled components workflow"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass'
        )
        self.client.login(username='admin', password='adminpass')

        self.temp_dir = Path(tempfile.mkdtemp())
        self.service = ThemeService()

    def tearDown(self):
        """Clean up temporary files"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def create_complete_theme_package(self):
        """Create a complete theme package with all features"""
        theme_dir = self.temp_dir / 'complete-theme'
        theme_dir.mkdir(parents=True, exist_ok=True)

        # Theme manifest with bundled components
        manifest = {
            'name': 'complete-theme',
            'version': '1.0.0',
            'display_name': 'Complete Theme',
            'description': 'A complete theme with bundled components',
            'author': 'Spwig',
            'license': 'MIT',
            'bundled_components': [
                {
                    'type': 'header',
                    'name': 'main_header',
                    'path': 'components/headers/main_header'
                },
                {
                    'type': 'footer',
                    'name': 'main_footer',
                    'path': 'components/footers/main_footer'
                },
                {
                    'type': 'section',
                    'name': 'hero_section',
                    'path': 'components/sections/hero_section'
                }
            ]
        }

        with open(theme_dir / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)

        # Create bundled components
        for comp_ref in manifest['bundled_components']:
            comp_dir = theme_dir / comp_ref['path']
            comp_dir.mkdir(parents=True, exist_ok=True)

            # Component manifest
            comp_manifest = {
                'name': comp_ref['name'],
                'version': '1.0.0',
                'display_name': comp_ref['name'].replace('_', ' ').title(),
                'description': f"Bundled {comp_ref['type']} component",
                'component_type': comp_ref['type'],
                'author': 'Spwig',
            }
            with open(comp_dir / 'manifest.json', 'w') as f:
                json.dump(comp_manifest, f, indent=2)

            # Component template
            with open(comp_dir / 'template.html', 'w') as f:
                f.write(f'<div class="{comp_ref["type"]}">{comp_ref["name"]}</div>')

            # Component schema
            comp_schema = {
                'settings': [
                    {
                        'id': f'{comp_ref["name"]}_setting',
                        'type': 'text',
                        'label': 'Component Setting',
                        'default': 'default value'
                    }
                ]
            }
            with open(comp_dir / 'schema.json', 'w') as f:
                json.dump(comp_schema, f, indent=2)

        # Create ZIP package
        zip_path = self.temp_dir / 'complete-theme-1.0.0.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in theme_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(theme_dir)
                    zipf.write(file_path, arcname)

        return zip_path

    def test_full_theme_installation_workflow(self):
        """Test complete workflow: install theme -> extract components -> verify registry"""
        # Create theme package
        package_path = self.create_complete_theme_package()

        # Create Theme instance
        theme = Theme.objects.create(
            slug='complete-theme',
            name='Complete Theme',
            version='1.0.0',
            author='Spwig'
        )

        # Install theme with bundled components
        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('complete-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Verify theme installation
        self.assertTrue(Theme.objects.filter(slug='complete-theme').exists())

        # Verify all components were extracted
        components = ComponentStore.objects.filter(source_theme=theme)
        self.assertEqual(components.count(), 3)

        # Verify component types
        component_types = set(comp.component_type for comp in components)
        self.assertEqual(component_types, {'header', 'footer', 'section'})

        # Verify all components are in registry
        registry_entries = ComponentRegistry.objects.filter(
            slug__in=['main_header', 'main_footer', 'hero_section']
        )
        self.assertEqual(registry_entries.count(), 3)

        # Verify all components are approved
        for comp in components:
            self.assertEqual(comp.review_status, 'approved')

    def test_theme_with_components_shows_in_ui(self):
        """Test that theme with bundled components displays correctly in UI"""
        # Create and install theme
        package_path = self.create_complete_theme_package()

        theme = Theme.objects.create(
            slug='complete-theme',
            name='Complete Theme',
            version='1.0.0',
            author='Spwig'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('complete-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Create ComponentRegistry entry for the theme
        ComponentRegistry.objects.create(
            component_type='theme',
            slug='complete-theme',
            name='Complete Theme',
            description='A complete theme with bundled components',
            current_version='1.0.0',
            latest_version='1.0.0',
            author='Spwig'
        )

        # Access unified theme management view
        response = self.client.get(reverse('design:unified_theme_management'))
        self.assertEqual(response.status_code, 200)

        # Verify theme appears in context
        themes = response.context['themes']
        theme_slugs = [t['slug'] for t in themes]
        self.assertIn('complete-theme', theme_slugs)

        # Find our theme in the list
        our_theme = next(t for t in themes if t['slug'] == 'complete-theme')

        # Verify bundled components info is included
        self.assertIn('bundled_components', our_theme)
        self.assertIn('bundled_component_count', our_theme)
        self.assertEqual(our_theme['bundled_component_count'], 3)

    def test_get_theme_components_ajax_endpoint(self):
        """Test AJAX endpoint for getting theme components"""
        # Create and install theme
        package_path = self.create_complete_theme_package()

        theme = Theme.objects.create(
            slug='complete-theme',
            name='Complete Theme',
            version='1.0.0',
            author='Spwig'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('complete-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Test AJAX endpoint
        url = reverse('design:get_theme_components', kwargs={'slug': 'complete-theme'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue(data['success'])
        self.assertEqual(data['theme_slug'], 'complete-theme')
        self.assertEqual(data['component_count'], 3)
        self.assertEqual(len(data['components']), 3)

        # Verify component data structure
        component = data['components'][0]
        self.assertIn('id', component)
        self.assertIn('component_type', component)
        self.assertIn('slug', component)
        self.assertIn('display_name', component)
        self.assertIn('version', component)
        self.assertIn('is_installed', component)

    def test_get_component_details_ajax_endpoint(self):
        """Test AJAX endpoint for getting component details"""
        # Create and install theme
        package_path = self.create_complete_theme_package()

        theme = Theme.objects.create(
            slug='complete-theme',
            name='Complete Theme',
            version='1.0.0',
            author='Spwig'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('complete-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Get a component
        component = ComponentStore.objects.filter(source_theme=theme).first()

        # Test AJAX endpoint
        url = reverse('design:get_component_details', kwargs={'component_id': component.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue(data['success'])
        self.assertIn('component', data)

        comp_data = data['component']
        self.assertEqual(comp_data['id'], component.id)
        self.assertEqual(comp_data['slug'], component.slug)
        self.assertEqual(comp_data['version'], component.version)
        self.assertIn('source_theme', comp_data)
        self.assertEqual(comp_data['source_theme']['slug'], 'complete-theme')

    def test_component_lifecycle_with_theme(self):
        """Test component lifecycle tied to theme"""
        # Create and install theme
        package_path = self.create_complete_theme_package()

        theme = Theme.objects.create(
            slug='complete-theme',
            name='Complete Theme',
            version='1.0.0',
            author='Spwig'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('complete-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Verify components exist
        self.assertEqual(ComponentStore.objects.filter(source_theme=theme).count(), 3)

        # Delete theme
        theme.delete()

        # Components should still exist (SET_NULL behavior)
        # But their source_theme should be None
        orphaned_components = ComponentStore.objects.filter(
            slug__in=['main_header', 'main_footer', 'hero_section']
        )
        self.assertEqual(orphaned_components.count(), 3)

        for comp in orphaned_components:
            self.assertIsNone(comp.source_theme)

    def test_reinstall_theme_updates_components(self):
        """Test reinstalling theme with updated components"""
        # First installation
        package_path = self.create_complete_theme_package()

        theme = Theme.objects.create(
            slug='complete-theme',
            name='Complete Theme',
            version='1.0.0',
            author='Spwig'
        )

        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('complete-theme-1.0.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        initial_count = ComponentStore.objects.filter(source_theme=theme).count()

        # Update theme version
        theme.version = '1.1.0'
        theme.save()

        # Reinstall with same components
        with open(package_path, 'rb') as f:
            package_file = SimpleUploadedFile('complete-theme-1.1.0.zip', f.read())
            self.service.extract_bundled_components(theme, package_file, self.user)

        # Should not create duplicates
        final_count = ComponentStore.objects.filter(source_theme=theme).count()
        self.assertEqual(initial_count, final_count)

    def test_multiple_themes_with_overlapping_components(self):
        """Test multiple themes bundling similar components"""
        # Create two themes
        theme1 = Theme.objects.create(
            slug='theme-one',
            name='Theme One',
            version='1.0.0',
            author='Spwig'
        )

        theme2 = Theme.objects.create(
            slug='theme-two',
            name='Theme Two',
            version='1.0.0',
            author='Spwig'
        )

        # Create components for theme1
        ComponentStore.objects.create(
            component_type='header',
            slug='shared_header',
            display_name='Shared Header',
            description='Shared header component',
            version='1.0.0',
            author='Spwig',
            review_status='approved',
            source_theme=theme1
        )

        # Create components for theme2 (same slug but different theme)
        ComponentStore.objects.create(
            component_type='header',
            slug='shared_header_v2',
            display_name='Shared Header V2',
            description='Different version of shared header',
            version='2.0.0',
            author='Spwig',
            review_status='approved',
            source_theme=theme2
        )

        # Both should exist independently
        self.assertEqual(theme1.bundled_component_count, 1)
        self.assertEqual(theme2.bundled_component_count, 1)

        # Total components
        total_components = ComponentStore.objects.filter(
            source_theme__in=[theme1, theme2]
        ).count()
        self.assertEqual(total_components, 2)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
