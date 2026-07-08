"""
Tests for SlotInjector - Safe Content Injection System

Tests cover:
- Slot syntax parsing and validation
- Component slots with constraints
- HTML slots with sanitization
- Text slots with escaping
- Error handling and fallbacks
- Edge cases and malformed syntax
"""

import pytest
from unittest.mock import Mock, patch

from design.slot_injector import (
    SlotInjector,
    SlotSyntaxError,
    SlotConstraintError,
    SlotDefinition
)
from design.content_sanitizer import ContentSanitizer


@pytest.mark.django_db
class TestSlotInjectorBasics:
    """Test basic slot injector functionality."""

    def test_initialize_injector(self):
        """Test injector initialization."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        assert injector is not None
        assert injector.sanitizer == sanitizer

    def test_empty_template(self):
        """Test injecting into empty template."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        output = injector.inject_slots('', {})
        assert output == ''

    def test_template_without_slots(self):
        """Test template with no slot markers."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '<div>Hello World</div>'
        output = injector.inject_slots(template, {})

        assert output == template


@pytest.mark.django_db
class TestSlotSyntaxParsing:
    """Test slot syntax parsing."""

    def test_parse_basic_slot(self):
        """Test parsing basic slot syntax."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero }}'
        slots = injector.get_slot_definitions(template)

        assert len(slots) == 1
        assert slots[0].name == 'hero'
        assert slots[0].slot_type == 'html'  # Default type
        assert slots[0].max_instances == -1  # Unlimited

    def test_parse_slot_with_type(self):
        """Test parsing slot with explicit type."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:component }}'
        slots = injector.get_slot_definitions(template)

        assert len(slots) == 1
        assert slots[0].name == 'hero'
        assert slots[0].slot_type == 'component'

    def test_parse_slot_with_max_instances(self):
        """Test parsing slot with max instances."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:component|max:1 }}'
        slots = injector.get_slot_definitions(template)

        assert len(slots) == 1
        assert slots[0].max_instances == 1

    def test_parse_slot_unlimited_instances(self):
        """Test parsing slot with unlimited instances."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:widgets|type:component|max:-1 }}'
        slots = injector.get_slot_definitions(template)

        assert len(slots) == 1
        assert slots[0].max_instances == -1

    def test_parse_multiple_slots(self):
        """Test parsing multiple slots in template."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = (
            '{{ slot:header|type:component|max:1 }}'
            '{{ slot:content|type:html }}'
            '{{ slot:footer|type:text }}'
        )
        slots = injector.get_slot_definitions(template)

        assert len(slots) == 3
        assert slots[0].name == 'header'
        assert slots[1].name == 'content'
        assert slots[2].name == 'footer'

    def test_parse_slot_with_whitespace(self):
        """Test parsing slot with extra whitespace."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{  slot:hero  |  type:component  |  max:1  }}'
        slots = injector.get_slot_definitions(template)

        assert len(slots) == 1
        assert slots[0].name == 'hero'


@pytest.mark.django_db
class TestSlotSyntaxValidation:
    """Test slot syntax validation."""

    def test_validate_valid_syntax(self):
        """Test validating correct slot syntax."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:component|max:1 }}'
        errors = injector.validate_slot_syntax(template)

        assert len(errors) == 0

    def test_validate_invalid_slot_type(self):
        """Test validating invalid slot type."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:invalid }}'
        errors = injector.validate_slot_syntax(template)

        assert len(errors) > 0
        assert 'invalid' in errors[0].lower()

    def test_validate_zero_max_instances(self):
        """Test validating zero max instances (invalid)."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:component|max:0 }}'
        errors = injector.validate_slot_syntax(template)

        assert len(errors) > 0
        assert '0' in errors[0]


@pytest.mark.django_db
class TestComponentSlots:
    """Test component slot injection."""

    def test_inject_single_component(self):
        """Test injecting single component into slot."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:component|max:1 }}'
        slot_data = {
            'hero': [
                {'type': 'banner', 'data': {'title': 'Welcome'}}
            ]
        }

        output = injector.inject_slots(template, slot_data)

        assert 'Component: banner' in output
        assert '{{ slot:hero' not in output  # Slot replaced

    def test_inject_multiple_components(self):
        """Test injecting multiple components into slot."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:widgets|type:component|max:-1 }}'
        slot_data = {
            'widgets': [
                {'type': 'newsletter', 'data': {}},
                {'type': 'social', 'data': {}}
            ]
        }

        output = injector.inject_slots(template, slot_data)

        assert 'Component: newsletter' in output
        assert 'Component: social' in output

    def test_inject_component_exceeds_max(self):
        """Test injecting more components than max allowed."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:component|max:1 }}'
        slot_data = {
            'hero': [
                {'type': 'banner1', 'data': {}},
                {'type': 'banner2', 'data': {}}  # Exceeds max
            ]
        }

        with pytest.raises(SlotConstraintError, match='max 1'):
            injector.inject_slots(template, slot_data)

    def test_inject_component_wrong_type(self):
        """Test injecting wrong data type for component slot."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:component|max:1 }}'
        slot_data = {
            'hero': 'not a list'  # Should be list
        }

        with pytest.raises(SlotConstraintError, match='expects list'):
            injector.inject_slots(template, slot_data)

    def test_inject_empty_component_list(self):
        """Test injecting empty component list."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|type:component|max:1 }}'
        slot_data = {
            'hero': []  # Empty list
        }

        output = injector.inject_slots(template, slot_data)

        assert output == ''  # Should render empty


@pytest.mark.django_db
class TestHTMLSlots:
    """Test HTML slot injection with sanitization."""

    def test_inject_safe_html(self):
        """Test injecting safe HTML content."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:content|type:html }}'
        slot_data = {
            'content': '<p>Hello <strong>World</strong></p>'
        }

        output = injector.inject_slots(template, slot_data)

        assert '<p>Hello <strong>World</strong></p>' in output

    def test_inject_html_with_script(self):
        """Test that script tags are sanitized."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:content|type:html }}'
        slot_data = {
            'content': '<p>Safe</p><script>alert("XSS")</script>'
        }

        output = injector.inject_slots(template, slot_data)

        assert '<p>Safe</p>' in output
        assert '<script' not in output  # Script removed

    def test_inject_html_wrong_type(self):
        """Test injecting wrong data type for HTML slot."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:content|type:html }}'
        slot_data = {
            'content': 123  # Should be string
        }

        with pytest.raises(SlotConstraintError, match='expects string'):
            injector.inject_slots(template, slot_data)

    def test_inject_html_tier_a_restrictions(self):
        """Test HTML sanitization with Tier A restrictions."""
        sanitizer = ContentSanitizer(tier='A')  # Most restrictive
        injector = SlotInjector(sanitizer)

        template = '{{ slot:content|type:html }}'
        slot_data = {
            'content': '<div><h1>Title</h1><p>Text</p></div>'
        }

        output = injector.inject_slots(template, slot_data)

        # Tier A blocks div and h1
        assert '<div' not in output.lower()
        assert '<h1' not in output.lower()
        # But allows p
        assert '<p>Text</p>' in output


@pytest.mark.django_db
class TestTextSlots:
    """Test text slot injection with escaping."""

    def test_inject_plain_text(self):
        """Test injecting plain text."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:message|type:text }}'
        slot_data = {
            'message': 'Hello World'
        }

        output = injector.inject_slots(template, slot_data)

        assert output == 'Hello World'

    def test_inject_text_with_html_entities(self):
        """Test that HTML entities are escaped."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:message|type:text }}'
        slot_data = {
            'message': '<p>This should be escaped</p>'
        }

        output = injector.inject_slots(template, slot_data)

        # HTML should be escaped
        assert '&lt;p&gt;' in output
        assert '&lt;/p&gt;' in output
        assert '<p>' not in output  # No actual HTML tags

    def test_inject_text_with_special_chars(self):
        """Test text with special characters."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:message|type:text }}'
        slot_data = {
            'message': 'Price: $100 & free shipping'
        }

        output = injector.inject_slots(template, slot_data)

        assert 'Price: $100 &amp; free shipping' in output

    def test_inject_text_wrong_type(self):
        """Test injecting wrong data type for text slot."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:message|type:text }}'
        slot_data = {
            'message': ['not', 'a', 'string']
        }

        with pytest.raises(SlotConstraintError, match='expects string'):
            injector.inject_slots(template, slot_data)


@pytest.mark.django_db
class TestOptionalSlots:
    """Test optional slots (no data provided)."""

    def test_optional_slot_no_data(self):
        """Test slot with no data renders empty."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '<div>{{ slot:optional|type:html }}</div>'
        slot_data = {}  # No data for 'optional' slot

        output = injector.inject_slots(template, slot_data)

        assert output == '<div></div>'

    def test_multiple_slots_some_optional(self):
        """Test multiple slots where some have data and some don't."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = (
            '{{ slot:required|type:html }}'
            '{{ slot:optional|type:html }}'
        )
        slot_data = {
            'required': '<p>Content</p>'
            # 'optional' not provided
        }

        output = injector.inject_slots(template, slot_data)

        assert '<p>Content</p>' in output


@pytest.mark.django_db
class TestErrorHandling:
    """Test error handling and fallbacks."""

    def test_malformed_slot_syntax(self):
        """Test handling malformed slot syntax."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:hero|invalid:syntax }}'
        slot_data = {}

        # Should not crash, return fallback
        output = injector.inject_slots(template, slot_data)

        assert 'failed' in output.lower() or 'error' in output.lower()

    def test_slot_render_error_fallback(self):
        """Test that slot render errors return fallback."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:test|type:html }}'

        # Mock sanitize_html to raise exception
        with patch.object(sanitizer, 'sanitize_html', side_effect=Exception('Test error')):
            slot_data = {'test': '<p>Content</p>'}
            output = injector.inject_slots(template, slot_data)

            # Should contain error comment
            assert '<!-- Slot test failed to render' in output


@pytest.mark.django_db
class TestComplexTemplates:
    """Test complex templates with multiple slots."""

    def test_template_with_mixed_slot_types(self):
        """Test template with different slot types."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = (
            '<header>{{ slot:header|type:component|max:1 }}</header>'
            '<main>{{ slot:content|type:html }}</main>'
            '<footer>{{ slot:copyright|type:text }}</footer>'
        )

        slot_data = {
            'header': [{'type': 'logo', 'data': {}}],
            'content': '<p>Welcome to our store</p>',
            'copyright': '© 2025 Our Store'
        }

        output = injector.inject_slots(template, slot_data)

        assert 'Component: logo' in output
        assert '<p>Welcome to our store</p>' in output
        assert '© 2025 Our Store' in output
        assert '<header>' in output
        assert '<main>' in output
        assert '<footer>' in output

    def test_nested_html_with_slots(self):
        """Test complex nested HTML structure with slots."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = (
            '<div class="container">'
            '  <div class="row">'
            '    {{ slot:col1|type:html }}'
            '    {{ slot:col2|type:html }}'
            '  </div>'
            '</div>'
        )

        slot_data = {
            'col1': '<div class="col">Column 1</div>',
            'col2': '<div class="col">Column 2</div>'
        }

        output = injector.inject_slots(template, slot_data)

        assert '<div class="container">' in output
        assert 'Column 1' in output
        assert 'Column 2' in output


@pytest.mark.django_db
class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_slot_name_with_numbers(self):
        """Test slot name containing numbers."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:widget_1|type:html }}'
        slot_data = {'widget_1': '<p>Test</p>'}

        output = injector.inject_slots(template, slot_data)

        assert '<p>Test</p>' in output

    def test_slot_name_with_underscores(self):
        """Test slot name with underscores."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:main_content|type:html }}'
        slot_data = {'main_content': '<p>Test</p>'}

        output = injector.inject_slots(template, slot_data)

        assert '<p>Test</p>' in output

    def test_very_long_html_content(self):
        """Test injecting very long HTML content."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:content|type:html }}'
        long_html = '<p>' + ('Test ' * 1000) + '</p>'
        slot_data = {'content': long_html}

        output = injector.inject_slots(template, slot_data)

        assert 'Test ' in output
        assert len(output) > 1000

    def test_unicode_content(self):
        """Test injecting Unicode content."""
        sanitizer = ContentSanitizer(tier='C')
        injector = SlotInjector(sanitizer)

        template = '{{ slot:message|type:text }}'
        slot_data = {'message': 'Hello 世界 🌍'}

        output = injector.inject_slots(template, slot_data)

        assert 'Hello 世界 🌍' in output
