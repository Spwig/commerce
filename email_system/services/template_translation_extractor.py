"""
Template Translation String Extractor

Extracts translatable text from email templates and reconstructs them after translation.
This solves the problem of sending massive MJML templates to the AI translation service
which causes timeouts.

Strategy:
1. Extract all translatable text strings from template
2. Create placeholders in template structure
3. Send only text strings to translation service
4. Reconstruct template with translated strings
"""

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TranslatableString:
    """A string that needs translation with its context"""

    key: str  # Unique identifier (e.g., "text_001")
    text: str  # The actual text to translate
    context: str  # Where it appears (for translator reference)


class TemplateTranslationExtractor:
    """
    Extracts translatable strings from email templates and reconstructs them.
    """

    # Patterns for translatable content
    PATTERNS = [
        # MJML text content: <mj-text>Translatable text</mj-text>
        # Use non-greedy match and ensure we don't cross major boundaries
        (r"(<mj-text[^>]*>)([^<{]+(?:\{\{[^}]+\}\}[^<{]*)*?)(</mj-text>)", "mjml_text"),
        # MJML button text: <mj-button>Click here</mj-button>
        (r"(<mj-button[^>]*>)([^<]+)(</mj-button>)", "mjml_button"),
        # HTML comments that are descriptive: <!-- Header -->
        (r"(<!-- )([A-Za-z\s]{3,30})( -->)", "html_comment"),
        # Title attributes: title="Shipping Address"
        (r'(title=")([^"]{3,100})(")', "title_attr"),
        # Text parameter in includes: text="View Order"
        (r'(text=")([^"]{3,100})(")', "text_attr"),
        # Strong tags: <strong>Label:</strong>
        (r"(<strong>)([^<]{1,50})(</strong>)", "strong_tag"),
    ]

    # Patterns to NEVER translate
    PRESERVE_PATTERNS = [
        r"\{\{[^}]+\}\}",  # Django variables: {{ variable }}
        r"\{%[^%]+%\}",  # Django tags: {% tag %}
        r"<mj-[^>]+>",  # MJML tags
        r"</mj-[^>]+>",  # MJML closing tags
        r"#[0-9a-fA-F]{3,6}",  # Color codes: #fff, #ffffff
        r"\d+px",  # Pixel values: 28px
        r"https?://[^\s]+",  # URLs
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email addresses
    ]

    def __init__(self):
        self.string_counter = 0
        self.strings_map = {}  # Maps placeholder -> TranslatableString

    def extract_from_template(
        self, template_type: str, subject: str, html_content: str, text_content: str
    ) -> tuple[dict, dict]:
        """
        Extract translatable strings from all template parts.

        Args:
            template_type: Type of template for context
            subject: Email subject line
            html_content: MJML/HTML content
            text_content: Plain text content

        Returns:
            Tuple of (templates_with_placeholders, translatable_strings)
        """
        self.string_counter = 0
        self.strings_map = {}

        # Extract from subject (simple case)
        subject_with_placeholders, subject_strings = self._extract_from_text(
            subject, context=f"{template_type}/subject"
        )

        # Extract from HTML content
        html_with_placeholders, html_strings = self._extract_from_html(
            html_content, context=f"{template_type}/html"
        )

        # Extract from text content
        text_with_placeholders, text_strings = self._extract_from_text(
            text_content, context=f"{template_type}/text", preserve_structure=True
        )

        # Combine all strings
        all_strings = {**subject_strings, **html_strings, **text_strings}

        templates = {
            "subject": subject_with_placeholders,
            "html_content": html_with_placeholders,
            "text_content": text_with_placeholders,
        }

        return templates, all_strings

    def _extract_from_html(self, html: str, context: str) -> tuple[str, dict]:
        """Extract translatable strings from HTML/MJML content"""
        result = html
        strings = {}

        for pattern, pattern_type in self.PATTERNS:
            matches = list(re.finditer(pattern, result, re.DOTALL))

            for match in reversed(matches):  # Reverse to maintain positions
                prefix = match.group(1)
                content = match.group(2)
                suffix = match.group(3)

                # Check if content should be translated
                if self._should_translate(content):
                    # Create placeholder
                    placeholder_key = self._get_next_key()
                    placeholder = f"__TRANSLATE_{placeholder_key}__"

                    # Store translatable string
                    strings[placeholder_key] = TranslatableString(
                        key=placeholder_key,
                        text=content.strip(),
                        context=f"{context}/{pattern_type}",
                    )

                    # Replace in result
                    result = (
                        result[: match.start()]
                        + prefix
                        + placeholder
                        + suffix
                        + result[match.end() :]
                    )

        return result, strings

    def _extract_from_text(
        self, text: str, context: str, preserve_structure: bool = False
    ) -> tuple[str, dict]:
        """
        Extract translatable strings from plain text.

        For plain text emails, we extract line by line but preserve Django tags.
        """
        if not text:
            return text, {}

        strings = {}

        # For subject lines or simple text without Django tags
        if not preserve_structure:
            # Check if entire text should be translated
            if self._should_translate(text):
                placeholder_key = self._get_next_key()
                placeholder = f"__TRANSLATE_{placeholder_key}__"

                strings[placeholder_key] = TranslatableString(
                    key=placeholder_key, text=text.strip(), context=context
                )

                return placeholder, strings
            else:
                return text, strings

        # For structured text content, process line by line
        lines = text.split("\n")
        result_lines = []

        for line in lines:
            # Skip Django tags
            if re.search(r"\{%.*%\}", line):
                result_lines.append(line)
                continue

            # Skip lines that are only variables
            if re.match(r"^\s*\{\{.*\}\}\s*$", line):
                result_lines.append(line)
                continue

            # Skip empty lines
            if not line.strip():
                result_lines.append(line)
                continue

            # Check if line has translatable content
            if self._should_translate(line):
                placeholder_key = self._get_next_key()
                placeholder = f"__TRANSLATE_{placeholder_key}__"

                strings[placeholder_key] = TranslatableString(
                    key=placeholder_key, text=line.strip(), context=f"{context}/line"
                )

                # Preserve indentation
                indent = len(line) - len(line.lstrip())
                result_lines.append(" " * indent + placeholder)
            else:
                result_lines.append(line)

        return "\n".join(result_lines), strings

    def _should_translate(self, text: str) -> bool:
        """
        Determine if text should be translated.

        Returns False if:
        - Text is empty or whitespace
        - Text is only Django variables/tags
        - Text contains only preserved patterns (URLs, emails, etc.)
        """
        if not text or not text.strip():
            return False

        # Check if only contains preserve patterns
        for pattern in self.PRESERVE_PATTERNS:
            # If the entire text matches a preserve pattern, don't translate
            if re.fullmatch(pattern, text.strip()):
                return False

        # Check if contains any translatable text (letters)
        # Must have at least 2 consecutive letters to be translatable
        return re.search(r"[A-Za-z]{2,}", text)

    def _get_next_key(self) -> str:
        """Generate next unique placeholder key"""
        self.string_counter += 1
        return f"{self.string_counter:03d}"

    def reconstruct_template(
        self, templates_with_placeholders: dict, translated_strings: dict[str, str]
    ) -> dict:
        """
        Reconstruct templates with translated strings.

        Args:
            templates_with_placeholders: Templates with __TRANSLATE_XXX__ placeholders
            translated_strings: Dict mapping placeholder keys to translated text

        Returns:
            Dict with subject, html_content, text_content in target language
        """
        result = {}

        for field, template_text in templates_with_placeholders.items():
            # Replace all placeholders with translated text
            reconstructed = template_text

            for key, translated_text in translated_strings.items():
                placeholder = f"__TRANSLATE_{key}__"
                reconstructed = reconstructed.replace(placeholder, translated_text)

            result[field] = reconstructed

        return result

    def prepare_for_translation(
        self, translatable_strings: dict[str, TranslatableString]
    ) -> dict[str, str]:
        """
        Prepare strings for translation service.

        Returns dict mapping keys to text for translation API.
        """
        return {key: string_obj.text for key, string_obj in translatable_strings.items()}

    def validate_translation(
        self, original_strings: dict[str, TranslatableString], translated_strings: dict[str, str]
    ) -> list[str]:
        """
        Validate that translation preserved important elements.

        Returns list of warnings (empty if all good).
        """
        warnings = []

        for key, original in original_strings.items():
            if key not in translated_strings:
                warnings.append(f"Missing translation for key {key}")
                continue

            original_text = original.text
            translated_text = translated_strings[key]

            # Check for preserved patterns (variables, tags)
            for pattern in self.PRESERVE_PATTERNS:
                original_matches = set(re.findall(pattern, original_text))
                translated_matches = set(re.findall(pattern, translated_text))

                if original_matches != translated_matches:
                    warnings.append(
                        f"Key {key}: Variables/tags changed. "
                        f"Original: {original_matches}, Translated: {translated_matches}"
                    )

        return warnings
