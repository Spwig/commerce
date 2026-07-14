"""License key generation service with template support"""

import re
import secrets
from datetime import datetime

from django.core.exceptions import ValidationError


class LicenseKeyGenerator:
    """Service for generating license keys using templates"""

    def generate(self, template, context: dict) -> str:
        """
        Generate a license key using template or default format.

        Args:
            template: LicenseKeyTemplate instance (None = use default)
            context: Dict with order_id, product_sku, etc.

        Returns:
            Generated license key string
        """
        if template is None:
            return self._generate_default()

        pattern = template.pattern
        key = self._process_pattern(pattern, template, context)

        # Validate length
        if len(key) < template.min_length:
            raise ValidationError(f"Generated key is too short: {len(key)} < {template.min_length}")
        if len(key) > template.max_length:
            raise ValidationError(f"Generated key is too long: {len(key)} > {template.max_length}")

        return key

    def _process_pattern(self, pattern: str, template, context: dict) -> str:
        """Process pattern and replace all placeholders"""

        # Replace static placeholders
        if template.prefix:
            pattern = pattern.replace("{PREFIX}", template.prefix)
        if template.suffix:
            pattern = pattern.replace("{SUFFIX}", template.suffix)

        # Replace context placeholders
        if "order_id" in context:
            pattern = pattern.replace("{ORDER_ID}", str(context["order_id"]))
        if "product_sku" in context:
            pattern = pattern.replace("{PRODUCT_SKU}", context["product_sku"])

        # Replace date placeholders
        pattern = self._process_date_placeholders(pattern)

        # Replace RANDOM placeholders
        pattern = self._process_random_placeholders(pattern, template.character_set)

        # Replace CHECKSUM placeholders (must be last)
        pattern = self._process_checksum_placeholders(pattern)

        return pattern

    def _process_random_placeholders(self, pattern: str, charset: str) -> str:
        """Replace {RANDOM:N} with N random characters"""

        def replacer(match):
            length = int(match.group(1))
            return "".join(secrets.choice(charset) for _ in range(length))

        return re.sub(r"\{RANDOM:(\d+)\}", replacer, pattern)

    def _process_checksum_placeholders(self, pattern: str) -> str:
        """Replace {CHECKSUM:N} with N-digit Luhn checksum"""

        def replacer(match):
            length = int(match.group(1))
            # Calculate checksum from current pattern state (without placeholders)
            checksum = self._calculate_luhn_checksum(pattern)
            return str(checksum).zfill(length)[-length:]

        return re.sub(r"\{CHECKSUM:(\d+)\}", replacer, pattern)

    def _process_date_placeholders(self, pattern: str) -> str:
        """Replace {DATE:FORMAT} with formatted current date"""

        def replacer(match):
            format_code = match.group(1)
            now = datetime.now()
            # Map common formats
            formats = {
                "YYMMDD": now.strftime("%y%m%d"),
                "YYYYMMDD": now.strftime("%Y%m%d"),
                "YY": now.strftime("%y"),
                "YYYY": now.strftime("%Y"),
                "MM": now.strftime("%m"),
                "DD": now.strftime("%d"),
            }
            return formats.get(format_code, format_code)

        return re.sub(r"\{DATE:([A-Z]+)\}", replacer, pattern)

    def _calculate_luhn_checksum(self, value: str) -> int:
        """Calculate Luhn (mod-10) checksum"""
        # Remove non-alphanumeric
        clean = re.sub(r"[^A-Z0-9]", "", value.upper())

        # Convert to digits (A=10, B=11, ..., Z=35)
        digits = []
        for char in clean:
            if char.isdigit():
                digits.append(int(char))
            else:
                digits.append(ord(char) - ord("A") + 10)

        # Luhn algorithm
        total = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit

        return (10 - (total % 10)) % 10

    def _generate_default(self) -> str:
        """Generate default format key (backward compatibility)"""
        from catalog.models import LicenseKey

        return LicenseKey.generate_license_key()

    def validate(self, key: str, template) -> bool:
        """
        Validate a license key against template rules.

        Args:
            key: License key to validate
            template: Template to validate against (None = default validation)

        Returns:
            True if valid, False otherwise
        """
        if template is None:
            # Default validation (basic format check)
            return len(key) >= 20 and "-" in key

        # Check length
        if len(key) < template.min_length or len(key) > template.max_length:
            return False

        # Check prefix/suffix
        if template.prefix and not key.startswith(template.prefix):
            return False
        if template.suffix and not key.endswith(template.suffix):
            return False

        # Checksum verification
        return not ("{CHECKSUM:" in template.pattern and not self._verify_checksum(key, template))

    def _verify_checksum(self, key: str, template) -> bool:
        """Verify embedded Luhn checksum in a license key.

        During generation, _process_checksum_placeholders computes Luhn on
        the pattern string that still contains the {CHECKSUM:N} placeholder.
        To verify, we reconstruct that same string by replacing the checksum
        digits back with the original placeholder, then recompute Luhn.
        """
        pattern = template.pattern

        # Build a regex from the pattern to locate the checksum position
        regex_pattern = re.escape(pattern)

        # Track each {CHECKSUM:N} — its digit length and original placeholder text
        checksum_info = []  # list of (length, original_placeholder)

        def checksum_replacer(match):
            length = int(match.group(1))
            placeholder = "{CHECKSUM:" + match.group(1) + "}"
            checksum_info.append((length, placeholder))
            return f"(\\d{{{length}}})"

        regex_pattern = re.sub(r"\\{CHECKSUM:(\d+)\\}", checksum_replacer, regex_pattern)

        # Replace other placeholders with bounded character-class quantifiers
        # to avoid ReDoS from ambiguous adjacent .+? groups
        charset_escaped = re.escape(template.character_set)

        def random_replacer(match):
            length = int(match.group(1))
            return f"[{charset_escaped}]{{{length}}}"

        regex_pattern = re.sub(r"\\{RANDOM:(\d+)\\}", random_replacer, regex_pattern)
        regex_pattern = re.sub(r"\\{[A-Z_]+(?::[^\\}]+)?\\}", ".+?", regex_pattern)

        match = re.fullmatch(regex_pattern, key)
        if not match:
            return False

        # Extract and verify each embedded checksum
        for i, (length, placeholder) in enumerate(checksum_info):
            embedded = match.group(i + 1)
            # Reconstruct the string as it was when Luhn was computed:
            # replace checksum digits with the original {CHECKSUM:N} placeholder
            reconstructed = key[: match.start(i + 1)] + placeholder + key[match.end(i + 1) :]
            expected = str(self._calculate_luhn_checksum(reconstructed)).zfill(length)[-length:]
            if embedded != expected:
                return False

        return True
