"""
Element Registry System for Page Builder

This module provides functionality to discover, register, and manage
modular page builder elements with their own translations and configurations.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Category display order for the visual builder sidebar
CATEGORY_DISPLAY_ORDER = [
    ('layout', 'Layout'),
    ('basic', 'Basic Elements'),
    ('content', 'Content'),
    ('media', 'Media'),
    ('forms', 'Forms'),
    ('marketing', 'Marketing'),
    ('ecommerce', 'E-Commerce'),
    ('social', 'Social'),
    ('custom', 'Custom Elements'),  # Custom elements from element_builder
]


class ElementConfig:
    """Represents configuration for a single page builder element."""
    
    def __init__(self, element_type: str, config_data: Dict[str, Any], base_path: Path):
        self.element_type = element_type
        self.base_path = base_path
        self.config_data = config_data
        
        # Extract common properties
        self.name = config_data.get('name', element_type.title())
        self.description = config_data.get('description', '')
        self.version = config_data.get('version', '1.0.0')
        self.category = config_data.get('category', 'general')
        self.icon = config_data.get('icon', 'fa-cube')
        self.author = config_data.get('author', 'Unknown')
        self.tags = config_data.get('tags', [])
        self.supports_translation = config_data.get('supports_translation', False)
        self.translation_domain = config_data.get('translation_domain', element_type)
        self.template_file = config_data.get('template_file', 'template.html')
        self.properties = config_data.get('properties', {})
        self.translations = config_data.get('translations', {})

        # JavaScript dependencies for this element
        self.scripts = config_data.get('scripts', [])

        # CSS dependencies for this element (external stylesheets)
        self.css_files = config_data.get('css_files', [])

        # Element Builder primitive flag - if True, element is available in element_builder
        self.element_builder_primitive = config_data.get('element_builder_primitive', False)
    
    @property
    def template_path(self) -> str:
        """Get the template path for this element."""
        return f"page_builder/elements/{self.element_type}/{self.template_file}"
    
    @property
    def locale_path(self) -> Path:
        """Get the locale directory path for this element."""
        return self.base_path / 'locale'
    
    def get_translated_name(self, language_code: str = None) -> str:
        """Get the translated name for the current language."""
        if not language_code:
            from django.utils.translation import get_language
            language_code = get_language() or 'en'
        
        # Try to get translation from config first
        if language_code in self.translations:
            return self.translations[language_code].get('name', self.name)
        
        # Fallback to base name
        return self.name
    
    def get_translated_description(self, language_code: str = None) -> str:
        """Get the translated description for the current language."""
        if not language_code:
            from django.utils.translation import get_language
            language_code = get_language() or 'en'
        
        # Try to get translation from config first
        if language_code in self.translations:
            return self.translations[language_code].get('description', self.description)
        
        # Fallback to base description
        return self.description
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert element config to dictionary for JSON serialization."""
        return {
            'element_type': self.element_type,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'category': self.category,
            'icon': self.icon,
            'author': self.author,
            'tags': self.tags,
            'supports_translation': self.supports_translation,
            'translation_domain': self.translation_domain,
            'template_path': self.template_path,
            'properties': self.properties,
            'translations': self.translations,
            'scripts': self.scripts,
            'css_files': self.css_files,
        }


class CustomElementConfig:
    """
    Represents a custom element created in element_builder.
    Provides the same interface as ElementConfig but backed by a database record.
    """

    def __init__(self, custom_element):
        """
        Initialize from a CustomElement model instance.

        Args:
            custom_element: element_builder.models.CustomElement instance
        """
        self.custom_element = custom_element
        self.element_type = f"custom_{custom_element.slug}"
        self.name = custom_element.name
        self.description = custom_element.description
        self.version = '1.0.0'
        self.category = 'custom'
        self.icon = custom_element.icon
        self.author = 'Merchant'
        self.tags = ['custom', custom_element.category]
        self.supports_translation = False
        self.translation_domain = self.element_type
        self.properties = {}
        self.translations = {}
        self.scripts = []  # Custom elements use underlying element scripts
        self.css_files = []  # Custom elements use underlying element CSS

    @property
    def template_path(self) -> str:
        """Get the wrapper template path for custom elements."""
        return 'element_builder/custom_element_wrapper.html'

    @property
    def locale_path(self) -> Path:
        """Custom elements don't have locale paths."""
        return Path('/nonexistent')

    @property
    def is_custom(self) -> bool:
        """Indicate this is a custom element from element_builder."""
        return True

    @property
    def target_model(self) -> str:
        """Get the target model for data binding."""
        return self.custom_element.target_model

    def get_translated_name(self, language_code: str = None) -> str:
        """Get the element name (custom elements don't have translations yet)."""
        return self.name

    def get_translated_description(self, language_code: str = None) -> str:
        """Get the element description."""
        return self.description

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'element_type': self.element_type,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'category': self.category,
            'icon': self.icon,
            'author': self.author,
            'tags': self.tags,
            'supports_translation': self.supports_translation,
            'translation_domain': self.translation_domain,
            'template_path': self.template_path,
            'properties': self.properties,
            'translations': self.translations,
            'scripts': self.scripts,
            'css_files': self.css_files,
            'is_custom': True,
            'custom_element_id': self.custom_element.pk,
            'target_model': self.target_model,
        }


class ElementRegistry:
    """Registry for managing page builder elements."""

    def __init__(self):
        self._elements: Dict[str, ElementConfig] = {}
        self._categories: Dict[str, List[str]] = {}
        self._loaded = False
        self._base_properties: Optional[Dict[str, Any]] = None

    def _load_base_properties(self) -> Optional[Dict[str, Any]]:
        """Load the universal base properties configuration."""
        if self._base_properties is not None:
            return self._base_properties

        base_path = Path(settings.BASE_DIR) / 'page_builder' / 'templates' / 'page_builder' / 'elements' / '_base' / 'base_properties.json'

        if not base_path.exists():
            logger.debug(f"Base properties not found: {base_path}")
            return None

        try:
            with open(base_path, 'r', encoding='utf-8') as f:
                self._base_properties = json.load(f)
            logger.info("Loaded base properties configuration")
            return self._base_properties
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load base properties: {e}")
            return None

    def _deep_copy_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Create a deep copy of a dictionary."""
        import copy
        return copy.deepcopy(d)

    def _merge_with_base(self, element_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge element config with base properties based on inheritance settings."""
        base = self._load_base_properties()
        if not base:
            return element_config

        # Check inheritance settings - default to True for backward compatibility
        inherit_base = element_config.get('inherit_base', True)
        if not inherit_base:
            return element_config

        disabled_props = set(element_config.get('disable_base_properties', []))
        overrides = element_config.get('override_base_properties', {})

        # Deep copy base properties to avoid modifying the cached base
        base_tabs = self._deep_copy_dict(base.get('tabs', {}))
        base_props = self._deep_copy_dict(base.get('properties', {}))

        # Filter out disabled properties from base tabs
        for tab_key, tab_config in base_tabs.items():
            if 'properties' in tab_config:
                tab_config['properties'] = {
                    prop_key: prop_config
                    for prop_key, prop_config in tab_config['properties'].items()
                    if prop_key not in disabled_props
                }

        # Filter out disabled properties from base properties
        base_props = {
            prop_key: prop_config
            for prop_key, prop_config in base_props.items()
            if prop_key not in disabled_props
        }

        # Apply overrides to base properties
        for prop_key, override_config in overrides.items():
            if prop_key in base_props:
                base_props[prop_key].update(override_config)
            # Also update in tabs
            for tab_config in base_tabs.values():
                if 'properties' in tab_config and prop_key in tab_config['properties']:
                    tab_config['properties'][prop_key].update(override_config)

        # Merge tabs: start with base tabs, then add/merge element's own tabs
        merged_tabs = base_tabs.copy()
        element_tabs = element_config.get('tabs', {})

        for tab_key, tab_config in element_tabs.items():
            if tab_key in merged_tabs:
                # Merge with existing base tab - element's properties take precedence
                existing_props = merged_tabs[tab_key].get('properties', {})
                element_props = tab_config.get('properties', {})
                merged_props = {**existing_props, **element_props}
                merged_tabs[tab_key] = {**merged_tabs[tab_key], **tab_config}
                merged_tabs[tab_key]['properties'] = merged_props
            else:
                # Add new tab from element
                merged_tabs[tab_key] = tab_config

        # Sort tabs by order if specified
        sorted_tabs = dict(sorted(
            merged_tabs.items(),
            key=lambda x: x[1].get('order', 999)
        ))

        # Merge properties: base properties + element properties (element takes precedence)
        element_props = element_config.get('properties', {})
        merged_props = {**base_props, **element_props}

        # Build final config
        result = element_config.copy()
        result['tabs'] = sorted_tabs
        result['properties'] = merged_props

        # Remove inheritance-related keys from final config (they're not needed after merge)
        result.pop('inherit_base', None)
        result.pop('disable_base_properties', None)
        result.pop('override_base_properties', None)

        return result
    
    def discover_elements(self, force_reload: bool = False) -> None:
        """Discover all available elements from the filesystem."""
        cache_key = 'page_builder_elements_registry'

        # Skip caching in DEBUG mode for immediate config updates during development
        use_cache = not settings.DEBUG

        # In DEBUG mode, always re-read from filesystem for immediate config changes
        # In production, use cache and in-memory flag to avoid repeated disk reads
        if use_cache and not force_reload and not self._loaded:
            # Try to load from cache first (production only)
            cached_data = cache.get(cache_key)
            if cached_data:
                self._elements = cached_data.get('elements', {})
                self._categories = cached_data.get('categories', {})
                self._loaded = True
                return
        elif use_cache and self._loaded and not force_reload:
            # Already loaded in memory (production)
            return
        
        # Clear existing data
        self._elements.clear()
        self._categories.clear()
        
        # Get the elements directory
        elements_dir = Path(settings.BASE_DIR) / 'page_builder' / 'templates' / 'page_builder' / 'elements'
        
        if not elements_dir.exists():
            logger.warning(f"Elements directory not found: {elements_dir}")
            return
        
        # Scan for element directories
        for element_path in elements_dir.iterdir():
            if not element_path.is_dir():
                continue

            element_type = element_path.name

            # Skip special directories like _base
            if element_type.startswith('_'):
                logger.debug(f"Skipping special directory: {element_type}")
                continue

            config_file = element_path / 'config.json'

            # Skip if no config file or if it's an old-style element
            if not config_file.exists():
                logger.debug(f"Skipping element {element_type}: no config.json found")
                continue

            try:
                # Load element configuration
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)

                # Merge with base properties (inheritance system)
                config_data = self._merge_with_base(config_data)

                # Create element config object
                element_config = ElementConfig(element_type, config_data, element_path)
                
                # Register the element
                self._elements[element_type] = element_config
                
                # Add to category
                category = element_config.category
                if category not in self._categories:
                    self._categories[category] = []
                self._categories[category].append(element_type)
                
                logger.info(f"Registered element: {element_type} (v{element_config.version})")
                
            except (json.JSONDecodeError, KeyError, IOError) as e:
                logger.error(f"Failed to load element {element_type}: {e}")
                continue
        
        # Discover custom elements from database
        self._discover_custom_elements()

        # Cache the results (production only)
        if use_cache:
            cache_data = {
                'elements': self._elements,
                'categories': self._categories
            }
            cache.set(cache_key, cache_data, timeout=3600)  # Cache for 1 hour

        self._loaded = True
        logger.info(f"Element discovery complete. Found {len(self._elements)} elements in {len(self._categories)} categories.")

    def _discover_custom_elements(self) -> None:
        """Discover custom elements from element_builder database."""
        try:
            # Check if Django apps are ready before accessing database
            from django.apps import apps
            if not apps.ready:
                logger.debug("Django apps not ready yet, skipping custom element discovery")
                return

            from element_builder.models import CustomElement

            for custom_el in CustomElement.objects.filter(is_active=True, root_element__isnull=False):
                element_type = f"custom_{custom_el.slug}"

                # Create a CustomElementConfig (wrapper around ElementConfig for DB elements)
                config = CustomElementConfig(custom_el)

                # Register the element
                self._elements[element_type] = config

                # Add to 'custom' category
                if 'custom' not in self._categories:
                    self._categories['custom'] = []
                self._categories['custom'].append(element_type)

                logger.info(f"Registered custom element: {element_type}")

        except ImportError:
            logger.debug("element_builder app not installed, skipping custom elements")
        except Exception as e:
            logger.warning(f"Error discovering custom elements: {e}")
    
    def get_element(self, element_type: str) -> Optional[ElementConfig]:
        """Get a specific element configuration."""
        if not self._loaded:
            self.discover_elements()
        
        return self._elements.get(element_type)
    
    def get_all_elements(self) -> Dict[str, ElementConfig]:
        """Get all registered elements."""
        if not self._loaded:
            self.discover_elements()
        
        return self._elements.copy()
    
    def get_elements_by_category(self, category: str) -> List[ElementConfig]:
        """Get all elements in a specific category."""
        if not self._loaded:
            self.discover_elements()
        
        element_types = self._categories.get(category, [])
        return [self._elements[element_type] for element_type in element_types if element_type in self._elements]
    
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        if not self._loaded:
            self.discover_elements()
        
        return list(self._categories.keys())
    
    def get_elements_for_visual_builder(self) -> Dict[str, Any]:
        """Get elements formatted for the visual builder interface."""
        if not self._loaded:
            self.discover_elements()

        categories = {}

        for category, element_types in self._categories.items():
            category_elements = []

            for element_type in element_types:
                if element_type in self._elements:
                    element = self._elements[element_type]
                    category_elements.append({
                        'type': element.element_type,
                        'name': element.get_translated_name(),
                        'description': element.get_translated_description(),
                        'icon': element.icon,
                        'tags': element.tags,
                        'properties': element.properties
                    })

            if category_elements:
                categories[category] = {
                    'name': category.title(),
                    'elements': category_elements
                }

        return categories

    def get_element_metadata(self) -> Dict[str, Any]:
        """Return minimal metadata (icon, name, defaults) for all elements, keyed by type."""
        if not self._loaded:
            self.discover_elements()
        return {
            etype: {
                'icon': el.icon,
                'name': el.get_translated_name(),
                'defaults': el.config_data.get('defaults', {}) if hasattr(el, 'config_data') else {},
            }
            for etype, el in self._elements.items()
        }

    def get_elements_for_sidebar(self) -> List[Dict[str, Any]]:
        """Get elements formatted for the visual builder sidebar, ordered by category."""
        if not self._loaded:
            self.discover_elements()

        result = []
        processed_categories = set()

        # Process categories in display order
        for category_key, display_name in CATEGORY_DISPLAY_ORDER:
            if category_key in self._categories:
                element_types = self._categories[category_key]
                category_elements = []

                for element_type in sorted(element_types):
                    if element_type in self._elements:
                        element = self._elements[element_type]
                        category_elements.append({
                            'type': element.element_type,
                            'name': element.get_translated_name(),
                            'description': element.get_translated_description(),
                            'icon': element.icon,
                            'tags': element.tags,
                        })

                if category_elements:
                    result.append({
                        'key': category_key,
                        'display_name': display_name,
                        'elements': category_elements
                    })
                processed_categories.add(category_key)

        # Add any remaining categories not in display order
        for category_key, element_types in self._categories.items():
            if category_key not in processed_categories:
                category_elements = []

                for element_type in sorted(element_types):
                    if element_type in self._elements:
                        element = self._elements[element_type]
                        category_elements.append({
                            'type': element.element_type,
                            'name': element.get_translated_name(),
                            'description': element.get_translated_description(),
                            'icon': element.icon,
                            'tags': element.tags,
                        })

                if category_elements:
                    result.append({
                        'key': category_key,
                        'display_name': category_key.title(),
                        'elements': category_elements
                    })

        return result
    
    def validate_element_template(self, element_type: str) -> bool:
        """Validate that an element's template exists and can be loaded."""
        element = self.get_element(element_type)
        if not element:
            return False
        
        try:
            get_template(element.template_path)
            return True
        except TemplateDoesNotExist:
            logger.error(f"Template not found for element {element_type}: {element.template_path}")
            return False
    
    def get_element_locale_paths(self) -> List[str]:
        """Get all element locale paths for Django settings."""
        if not self._loaded:
            self.discover_elements()
        
        locale_paths = []
        
        for element in self._elements.values():
            if element.supports_translation and element.locale_path.exists():
                locale_paths.append(str(element.locale_path))
        
        return locale_paths
    
    def reload(self) -> None:
        """Force reload all elements from filesystem."""
        logger.info("Reloading element registry...")
        cache.delete('page_builder_elements_registry')
        self._loaded = False
        self._base_properties = None  # Clear cached base properties
        self.discover_elements(force_reload=True)


# Global registry instance
registry = ElementRegistry()


def get_registry() -> ElementRegistry:
    """Get the global element registry instance."""
    return registry


def get_element(element_type: str) -> Optional[ElementConfig]:
    """Convenience function to get an element configuration."""
    return registry.get_element(element_type)


def get_all_elements() -> Dict[str, ElementConfig]:
    """Convenience function to get all elements."""
    return registry.get_all_elements()


def get_elements_by_category(category: str) -> List[ElementConfig]:
    """Convenience function to get elements by category."""
    return registry.get_elements_by_category(category)


def reload_elements() -> None:
    """Convenience function to reload all elements."""
    registry.reload()