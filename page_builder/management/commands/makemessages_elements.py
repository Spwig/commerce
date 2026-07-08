"""
Django management command for generating translation messages for page builder elements.

This command extends Django's makemessages functionality to work with the modular
element structure and provides element-specific translation management.
"""

import os
import sys
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.makemessages import Command as MakeMessagesCommand
from django.conf import settings
from django.utils.translation import gettext as _
from page_builder.element_registry import get_registry


class Command(BaseCommand):
    help = 'Generate translation files for page builder elements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--element',
            type=str,
            help='Generate translations for specific element only'
        )
        
        parser.add_argument(
            '--locale',
            action='append',
            default=[],
            help='Locale(s) to process (e.g., en, es, fr). Can be used multiple times.'
        )
        
        parser.add_argument(
            '--all-locales',
            action='store_true',
            help='Process all configured locales'
        )
        
        parser.add_argument(
            '--domain',
            default='django',
            help='Translation domain (default: django)'
        )
        
        parser.add_argument(
            '--extension',
            dest='extensions',
            action='append',
            default=[],
            help='File extensions to examine (default: html,txt,py). Can be used multiple times.'
        )
        
        parser.add_argument(
            '--ignore',
            action='append',
            dest='ignore_patterns',
            default=[],
            help='Ignore files or directories matching this glob-style pattern. Can be used multiple times.'
        )
        
        parser.add_argument(
            '--no-default-ignore',
            action='store_false',
            dest='use_default_ignore_patterns',
            help='Don\'t ignore the common glob-style patterns (\'CVS\', \'.*\', \'*~\', \'*.pyc\').'
        )
        
        parser.add_argument(
            '--no-wrap',
            action='store_true',
            help='Don\'t break long message lines into several lines.'
        )
        
        parser.add_argument(
            '--no-location',
            action='store_true',
            help='Don\'t write \'#: filename:line\' lines.'
        )
        
        parser.add_argument(
            '--keep-pot',
            action='store_true',
            help='Keep .pot file after creating .po files.'
        )

    def handle(self, *args, **options):
        registry = get_registry()
        
        # Get target element(s)
        target_element = options.get('element')
        if target_element:
            elements_to_process = {target_element: registry.get_element(target_element)}
            if not elements_to_process[target_element]:
                raise CommandError(f'Element "{target_element}" not found.')
        else:
            elements_to_process = registry.get_all_elements()
        
        if not elements_to_process:
            self.stdout.write(self.style.WARNING('No elements found to process.'))
            return
        
        # Determine locales to process
        locales = options.get('locale', [])
        if options.get('all_locales'):
            locales = [lang_code for lang_code, _ in settings.LANGUAGES]
        elif not locales:
            # Default to all configured locales
            locales = [lang_code for lang_code, _ in settings.LANGUAGES]
        
        # Set default extensions if none provided
        extensions = options.get('extensions', [])
        if not extensions:
            extensions = ['html', 'txt', 'py']
        
        # Process each element
        for element_type, element_config in elements_to_process.items():
            if not element_config.supports_translation:
                self.stdout.write(
                    self.style.WARNING(f'Skipping {element_type}: translation not supported')
                )
                continue
            
            self.stdout.write(f'\nProcessing element: {element_type}')
            
            # Ensure locale directories exist
            element_locale_dir = element_config.locale_path
            for locale in locales:
                locale_dir = element_locale_dir / locale / 'LC_MESSAGES'
                locale_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate translations for this element
            self._generate_element_translations(
                element_config, 
                locales, 
                options
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTranslation generation complete for {len(elements_to_process)} elements.')
        )

    def _generate_element_translations(self, element_config, locales, options):
        """Generate translation files for a specific element."""
        element_dir = element_config.base_path
        element_type = element_config.element_type
        
        # Prepare makemessages options
        makemessages_options = {
            'verbosity': options.get('verbosity', 1),
            'interactive': False,
            'domain': options.get('domain', 'django'),
            'extensions': options.get('extensions', ['html', 'txt', 'py']),
            'ignore_patterns': options.get('ignore_patterns', []),
            'use_default_ignore_patterns': options.get('use_default_ignore_patterns', True),
            'no_wrap': options.get('no_wrap', False),
            'no_location': options.get('no_location', False),
            'keep_pot': options.get('keep_pot', False),
        }
        
        # Save current working directory
        original_cwd = os.getcwd()
        
        try:
            # Change to element directory
            os.chdir(str(element_dir))
            
            for locale in locales:
                self.stdout.write(f'  Generating {locale} translation for {element_type}...')
                
                # Set up makemessages command for this locale
                makemessages_cmd = MakeMessagesCommand()
                makemessages_cmd.stdout = self.stdout
                makemessages_cmd.stderr = self.stderr
                makemessages_cmd.style = self.style
                
                # Update options for this locale
                locale_options = makemessages_options.copy()
                locale_options['locale'] = [locale]
                
                try:
                    # Run makemessages for this element and locale
                    makemessages_cmd.handle(**locale_options)
                    
                    # Check if po file was created
                    po_file = element_dir / 'locale' / locale / 'LC_MESSAGES' / f'{locale_options["domain"]}.po'
                    if po_file.exists():
                        self.stdout.write(
                            self.style.SUCCESS(f'    ✓ Created: {po_file.relative_to(element_dir)}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'    ? No translations found for {locale}')
                        )
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'    ✗ Failed to generate {locale}: {e}')
                    )
        
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

    def _compile_element_translations(self, element_config, locales):
        """Compile translation files for an element (optional step)."""
        from django.core.management import call_command
        
        element_dir = element_config.base_path
        original_cwd = os.getcwd()
        
        try:
            os.chdir(str(element_dir))
            
            for locale in locales:
                po_file = element_dir / 'locale' / locale / 'LC_MESSAGES' / 'django.po'
                if po_file.exists():
                    try:
                        call_command('compilemessages', locale=[locale], verbosity=0)
                        self.stdout.write(f'    ✓ Compiled {locale} translation')
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'    ✗ Failed to compile {locale}: {e}')
                        )
        finally:
            os.chdir(original_cwd)