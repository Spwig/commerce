"""
Slot Injector - Safe Content Injection System

Provides safe injection of merchant content into theme layout slots with:
- Mustache-style slot syntax parsing
- Type validation (component, html, text)
- Constraint enforcement (max instances, allowed types)
- Content sanitization integration
- Error handling for malformed slots

Slot Syntax:
    {{ slot:slot_name|type:component|max:1 }}
    {{ slot:widgets|type:component|max:-1 }}
    {{ slot:content|type:html }}
    {{ slot:text|type:text }}

Usage:
    injector = SlotInjector(sanitizer)
    output = injector.inject_slots(template, slot_data)
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from .content_sanitizer import ContentSanitizer

logger = logging.getLogger(__name__)


class SlotSyntaxError(Exception):
    """Raised when slot syntax is malformed"""
    pass


class SlotConstraintError(Exception):
    """Raised when slot constraints are violated"""
    pass


@dataclass
class SlotDefinition:
    """Parsed slot definition from template."""
    name: str
    slot_type: str  # 'component', 'html', 'text'
    max_instances: int  # -1 = unlimited
    raw_syntax: str  # Original slot marker


class SlotInjector:
    """
    Safe content injection system for theme layout slots.

    Provides:
    - Slot syntax parsing and validation
    - Content type validation
    - Constraint enforcement (max instances)
    - Content sanitization
    - Error handling with fallbacks

    Example:
        >>> sanitizer = ContentSanitizer(tier='C')
        >>> injector = SlotInjector(sanitizer)
        >>> template = '<div>{{ slot:hero|type:component|max:1 }}</div>'
        >>> slot_data = {'hero': [{'type': 'banner', 'data': {}}]}
        >>> output = injector.inject_slots(template, slot_data)
    """

    # Slot syntax regex pattern
    # Matches: {{ slot:name|type:component|max:1 }}
    # Allows whitespace around pipes and values
    SLOT_PATTERN = re.compile(
        r'\{\{\s*slot:\s*(?P<name>\w+)'
        r'(?:\s*\|\s*type:\s*(?P<type>\w+))?'
        r'(?:\s*\|\s*max:\s*(?P<max>-?\d+))?\s*\}\}',
        re.MULTILINE
    )

    # Valid slot types
    VALID_TYPES = ['component', 'html', 'text']

    # Default values
    DEFAULT_TYPE = 'html'
    DEFAULT_MAX_INSTANCES = -1  # Unlimited

    def __init__(self, sanitizer: ContentSanitizer):
        """
        Initialize slot injector with content sanitizer.

        Args:
            sanitizer: ContentSanitizer instance for sanitizing slot content
        """
        self.sanitizer = sanitizer
        logger.debug(f"SlotInjector initialized with tier {sanitizer.tier}")

    def inject_slots(
        self,
        template: str,
        slot_data: Dict[str, Any]
    ) -> str:
        """
        Inject content into all slots in template.

        Args:
            template: Template string with slot markers
            slot_data: Dict mapping slot names to content
                - For 'component' slots: list of component configs
                - For 'html' slots: HTML string
                - For 'text' slots: plain text string

        Returns:
            Template with all slots replaced by content

        Raises:
            SlotConstraintError: If slot constraints are violated (wrong data type, exceeds max)

        Note:
            SlotSyntaxError (malformed template syntax) is handled gracefully and returns
            fallback output instead of raising an exception. This helps with template authoring.

        Example:
            >>> template = '{{ slot:hero|type:component|max:1 }}'
            >>> slot_data = {'hero': [{'type': 'banner'}]}
            >>> output = injector.inject_slots(template, slot_data)
        """
        if not template:
            return ''

        try:
            # Parse slots (catch syntax errors for graceful degradation)
            slots = self._parse_slots(template)
        except SlotSyntaxError as e:
            # Template syntax errors - return fallback with error message
            # This is more user-friendly for template authoring than crashing
            logger.warning(f"Slot syntax error: {e}")
            return self._get_fallback_output(template, str(e))

        # Validate slot data (let constraint errors propagate - these are programming errors)
        self._validate_slot_data(slots, slot_data)

        try:
            # Replace each slot with content
            # Only catch unexpected rendering errors here
            output = template
            for slot in slots:
                content = self._render_slot_content(slot, slot_data.get(slot.name))
                output = output.replace(slot.raw_syntax, content)

            return output

        except Exception as e:
            # Only catch unexpected rendering errors, not validation errors
            logger.error(f"Slot rendering failed: {e}", exc_info=True)
            # Return template with error comments instead of crashing
            return self._get_fallback_output(template, str(e))

    def validate_slot_syntax(self, template: str) -> List[str]:
        """
        Validate all slot syntax in template without injecting content.

        Args:
            template: Template string to validate

        Returns:
            List of error messages (empty if all valid)

        Example:
            >>> errors = injector.validate_slot_syntax(template)
            >>> if errors:
            ...     print("Invalid slots:", errors)
        """
        errors = []

        try:
            slots = self._parse_slots(template)

            for slot in slots:
                # Check slot type is valid
                if slot.slot_type not in self.VALID_TYPES:
                    errors.append(
                        f"Invalid slot type '{slot.slot_type}' in {slot.raw_syntax}. "
                        f"Must be one of: {', '.join(self.VALID_TYPES)}"
                    )

                # Check max instances is valid
                if slot.max_instances == 0:
                    errors.append(
                        f"Invalid max instances '0' in {slot.raw_syntax}. "
                        f"Use -1 for unlimited or positive number."
                    )

        except SlotSyntaxError as e:
            errors.append(str(e))

        return errors

    def get_slot_definitions(self, template: str) -> List[SlotDefinition]:
        """
        Get all slot definitions from template.

        Args:
            template: Template string

        Returns:
            List of SlotDefinition objects

        Example:
            >>> slots = injector.get_slot_definitions(template)
            >>> for slot in slots:
            ...     print(f"{slot.name}: {slot.slot_type}, max={slot.max_instances}")
        """
        return self._parse_slots(template)

    # Private methods

    def _parse_slots(self, template: str) -> List[SlotDefinition]:
        """
        Parse all slot markers in template.

        Args:
            template: Template string

        Returns:
            List of SlotDefinition objects

        Raises:
            SlotSyntaxError: If slot syntax is malformed
        """
        # First check for malformed slot patterns (anything that looks like a slot but doesn't match)
        # This helps catch typos like {{ slot:name|typo:value }}
        malformed_pattern = re.compile(r'\{\{\s*slot:[^}]*\}\}')
        all_slot_like = list(malformed_pattern.finditer(template))

        # Parse valid slots
        slots = []
        matches = self.SLOT_PATTERN.finditer(template)
        valid_positions = set()

        for match in matches:
            try:
                slot = self._parse_slot_match(match)
                slots.append(slot)
                valid_positions.add(match.start())
            except Exception as e:
                raise SlotSyntaxError(
                    f"Malformed slot syntax at position {match.start()}: {e}"
                )

        # Check if there are any slot-like patterns that didn't match the valid pattern
        for slot_like in all_slot_like:
            if slot_like.start() not in valid_positions:
                raise SlotSyntaxError(
                    f"Invalid slot syntax at position {slot_like.start()}: {slot_like.group(0)}"
                )

        logger.debug(f"Parsed {len(slots)} slots from template")
        return slots

    def _parse_slot_match(self, match: re.Match) -> SlotDefinition:
        """
        Parse a single slot regex match into SlotDefinition.

        Args:
            match: Regex match object

        Returns:
            SlotDefinition object
        """
        name = match.group('name')
        slot_type = match.group('type') or self.DEFAULT_TYPE
        max_str = match.group('max')

        # Parse max instances
        if max_str is not None:
            try:
                max_instances = int(max_str)
            except ValueError:
                raise SlotSyntaxError(f"Invalid max value: {max_str}")
        else:
            max_instances = self.DEFAULT_MAX_INSTANCES

        # Validate slot type
        if slot_type not in self.VALID_TYPES:
            raise SlotSyntaxError(
                f"Invalid slot type '{slot_type}'. "
                f"Must be one of: {', '.join(self.VALID_TYPES)}"
            )

        return SlotDefinition(
            name=name,
            slot_type=slot_type,
            max_instances=max_instances,
            raw_syntax=match.group(0)
        )

    def _validate_slot_data(
        self,
        slots: List[SlotDefinition],
        slot_data: Dict[str, Any]
    ) -> None:
        """
        Validate that slot data conforms to slot constraints.

        Args:
            slots: List of slot definitions
            slot_data: Slot content data

        Raises:
            SlotConstraintError: If constraints are violated
        """
        for slot in slots:
            data = slot_data.get(slot.name)

            # Skip validation if no data provided (optional slots)
            if data is None:
                continue

            # Validate component slots
            if slot.slot_type == 'component':
                if not isinstance(data, list):
                    raise SlotConstraintError(
                        f"Slot '{slot.name}' expects list of components, "
                        f"got {type(data).__name__}"
                    )

                # Check max instances
                if slot.max_instances > 0 and len(data) > slot.max_instances:
                    raise SlotConstraintError(
                        f"Slot '{slot.name}' allows max {slot.max_instances} components, "
                        f"got {len(data)}"
                    )

            # Validate HTML/text slots
            elif slot.slot_type in ['html', 'text']:
                if not isinstance(data, str):
                    raise SlotConstraintError(
                        f"Slot '{slot.name}' expects string content, "
                        f"got {type(data).__name__}"
                    )

    def _render_slot_content(
        self,
        slot: SlotDefinition,
        data: Any
    ) -> str:
        """
        Render content for a single slot.

        Args:
            slot: Slot definition
            data: Content data for this slot

        Returns:
            Rendered HTML for slot
        """
        # No data provided - return empty
        if data is None:
            logger.debug(f"No data for slot '{slot.name}', rendering empty")
            return ''

        try:
            # Render based on slot type
            if slot.slot_type == 'component':
                return self._render_component_slot(slot, data)
            elif slot.slot_type == 'html':
                return self._render_html_slot(slot, data)
            elif slot.slot_type == 'text':
                return self._render_text_slot(slot, data)
            else:
                logger.warning(f"Unknown slot type: {slot.slot_type}")
                return ''

        except Exception as e:
            logger.error(f"Failed to render slot '{slot.name}': {e}", exc_info=True)
            return f'<!-- Slot {slot.name} failed to render: {e} -->'

    def _render_component_slot(
        self,
        slot: SlotDefinition,
        components: List[Dict[str, Any]]
    ) -> str:
        """
        Render component slot with list of components.

        Args:
            slot: Slot definition
            components: List of component configs

        Returns:
            Rendered HTML for all components
        """
        if not isinstance(components, list):
            logger.warning(
                f"Component slot '{slot.name}' expects list, got {type(components).__name__}"
            )
            return ''

        # Render each component (placeholder for now)
        # Task 2 (ComponentRegistryService) will handle actual rendering
        rendered = []
        for i, component_config in enumerate(components):
            component_type = component_config.get('type', 'unknown')
            component_data = component_config.get('data', {})

            # For now, return placeholder comment
            # This will be replaced with actual component rendering
            rendered.append(
                f'<!-- Component: {component_type} (data: {component_data}) -->'
            )

        return '\n'.join(rendered)

    def _render_html_slot(self, slot: SlotDefinition, html: str) -> str:
        """
        Render HTML slot with sanitization.

        Args:
            slot: Slot definition
            html: Raw HTML content

        Returns:
            Sanitized HTML
        """
        if not isinstance(html, str):
            logger.warning(
                f"HTML slot '{slot.name}' expects string, got {type(html).__name__}"
            )
            return ''

        # Sanitize HTML before injection
        sanitized = self.sanitizer.sanitize_html(html)

        logger.debug(f"Sanitized HTML slot '{slot.name}' ({len(html)} -> {len(sanitized)} bytes)")
        return sanitized

    def _render_text_slot(self, slot: SlotDefinition, text: str) -> str:
        """
        Render text slot (plain text, no HTML).

        Args:
            slot: Slot definition
            text: Plain text content

        Returns:
            Escaped text safe for HTML
        """
        if not isinstance(text, str):
            logger.warning(
                f"Text slot '{slot.name}' expects string, got {type(text).__name__}"
            )
            return ''

        # Escape HTML entities to prevent injection
        import html
        escaped = html.escape(text)

        return escaped

    def _get_fallback_output(self, template: str, error: str) -> str:
        """
        Generate fallback output when slot injection fails.

        Args:
            template: Original template
            error: Error message

        Returns:
            Template with error comments
        """
        return (
            f'<!-- Slot injection failed: {error} -->\n'
            f'{template}'
        )
