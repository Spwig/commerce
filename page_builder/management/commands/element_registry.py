"""
Django management command for managing the page builder element registry.
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from page_builder.element_registry import get_registry
import json


class Command(BaseCommand):
    help = 'Manage page builder element registry'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['list', 'reload', 'info', 'validate'],
            help='Action to perform'
        )
        
        parser.add_argument(
            '--element',
            type=str,
            help='Element type for info/validate actions'
        )
        
        parser.add_argument(
            '--category',
            type=str,
            help='Filter by category for list action'
        )
        
        parser.add_argument(
            '--format',
            choices=['table', 'json'],
            default='table',
            help='Output format'
        )

    def handle(self, *args, **options):
        registry = get_registry()
        action = options['action']
        
        try:
            if action == 'list':
                self.list_elements(registry, options)
            elif action == 'reload':
                self.reload_registry(registry)
            elif action == 'info':
                self.show_element_info(registry, options)
            elif action == 'validate':
                self.validate_elements(registry, options)
        except Exception as e:
            raise CommandError(f'Command failed: {e}')

    def list_elements(self, registry, options):
        """List all available elements."""
        category_filter = options.get('category')
        output_format = options.get('format', 'table')
        
        if category_filter:
            elements = registry.get_elements_by_category(category_filter)
            elements_dict = {elem.element_type: elem for elem in elements}
        else:
            elements_dict = registry.get_all_elements()
        
        if output_format == 'json':
            data = []
            for element_type, element in elements_dict.items():
                data.append(element.to_dict())
            self.stdout.write(json.dumps(data, indent=2))
        else:
            # Table format
            if not elements_dict:
                self.stdout.write(self.style.WARNING('No elements found.'))
                return
            
            self.stdout.write(self.style.SUCCESS(f'\nFound {len(elements_dict)} elements:\n'))
            
            # Header
            self.stdout.write(
                f"{'Type':<20} {'Name':<25} {'Version':<10} {'Category':<15} {'Translation':<12}"
            )
            self.stdout.write('-' * 85)
            
            # Elements
            for element_type, element in sorted(elements_dict.items()):
                translation_status = '✓' if element.supports_translation else '✗'
                self.stdout.write(
                    f"{element_type:<20} {element.name:<25} {element.version:<10} "
                    f"{element.category:<15} {translation_status:<12}"
                )

    def reload_registry(self, registry):
        """Reload the element registry."""
        self.stdout.write('Reloading element registry...')
        
        registry.reload()
        elements = registry.get_all_elements()
        
        self.stdout.write(
            self.style.SUCCESS(f'Registry reloaded successfully. Found {len(elements)} elements.')
        )

    def show_element_info(self, registry, options):
        """Show detailed information about a specific element."""
        element_type = options.get('element')
        if not element_type:
            raise CommandError('Element type is required for info action. Use --element=TYPE')
        
        element = registry.get_element(element_type)
        if not element:
            raise CommandError(f'Element "{element_type}" not found.')
        
        output_format = options.get('format', 'table')
        
        if output_format == 'json':
            self.stdout.write(json.dumps(element.to_dict(), indent=2))
        else:
            # Detailed table format
            self.stdout.write(self.style.SUCCESS(f'\nElement Information: {element_type}\n'))
            
            info_data = [
                ('Type', element.element_type),
                ('Name', element.name),
                ('Description', element.description),
                ('Version', element.version),
                ('Category', element.category),
                ('Author', element.author),
                ('Icon', element.icon),
                ('Template Path', element.template_path),
                ('Supports Translation', '✓' if element.supports_translation else '✗'),
                ('Translation Domain', element.translation_domain if element.supports_translation else 'N/A'),
                ('Tags', ', '.join(element.tags) if element.tags else 'None'),
            ]
            
            for label, value in info_data:
                self.stdout.write(f"{label:<20}: {value}")
            
            # Properties
            if element.properties:
                self.stdout.write(f"\nProperties ({len(element.properties)}):")
                for prop_name, prop_config in element.properties.items():
                    prop_type = prop_config.get('type', 'unknown')
                    prop_label = prop_config.get('label', prop_name)
                    required = ' (required)' if prop_config.get('required', False) else ''
                    translatable = ' (translatable)' if prop_config.get('translatable', False) else ''
                    self.stdout.write(f"  {prop_name:<20}: {prop_label} [{prop_type}]{required}{translatable}")
            
            # Available translations
            if element.translations:
                self.stdout.write(f"\nAvailable Translations:")
                for lang_code, translation in element.translations.items():
                    translated_name = translation.get('name', element.name)
                    self.stdout.write(f"  {lang_code:<10}: {translated_name}")

    def validate_elements(self, registry, options):
        """Validate element configurations and templates."""
        element_type = options.get('element')
        
        if element_type:
            # Validate specific element
            elements_to_validate = {element_type: registry.get_element(element_type)}
            if not elements_to_validate[element_type]:
                raise CommandError(f'Element "{element_type}" not found.')
        else:
            # Validate all elements
            elements_to_validate = registry.get_all_elements()
        
        self.stdout.write('Validating elements...\n')
        
        valid_count = 0
        invalid_count = 0
        
        for element_type, element in elements_to_validate.items():
            if element is None:
                self.stdout.write(
                    self.style.ERROR(f"✗ {element_type}: Element not found")
                )
                invalid_count += 1
                continue
            
            # Validate template
            template_valid = registry.validate_element_template(element_type)
            
            # Validate configuration
            config_issues = []
            
            # Check required fields
            if not element.name:
                config_issues.append("Missing name")
            
            if not element.element_type:
                config_issues.append("Missing element_type")
            
            if element.supports_translation and not element.locale_path.exists():
                config_issues.append("Translation support enabled but no locale directory found")
            
            # Overall validation result
            is_valid = template_valid and not config_issues
            
            if is_valid:
                self.stdout.write(
                    self.style.SUCCESS(f"✓ {element_type}: Valid")
                )
                valid_count += 1
            else:
                issues = []
                if not template_valid:
                    issues.append("Template not found")
                issues.extend(config_issues)
                
                self.stdout.write(
                    self.style.ERROR(f"✗ {element_type}: {', '.join(issues)}")
                )
                invalid_count += 1
        
        # Summary
        total = valid_count + invalid_count
        self.stdout.write(f"\nValidation Summary:")
        self.stdout.write(f"Total elements: {total}")
        self.stdout.write(self.style.SUCCESS(f"Valid: {valid_count}"))
        if invalid_count > 0:
            self.stdout.write(self.style.ERROR(f"Invalid: {invalid_count}"))
        else:
            self.stdout.write("All elements are valid!")