"""
Address Validation with Mismatch Detection

Integrates autocomplete (OpenStreetMap) with provider-specific validation
(e.g., Australia Post) to detect and flag address discrepancies.

Usage:
    from address_autocomplete.validation import AddressValidator

    validator = AddressValidator()
    result = await validator.validate_australian_address(
        user_input={
            "address1": "2 Macquarie St",
            "city": "Sydney",
            "state": "NSW",
            "postcode": "2000",
            "country": "AU"
        },
        provider_account_id=1  # Australia Post provider account
    )

    if result['has_mismatch']:
        print(f"Warning: {result['mismatch_reason']}")
        print(f"User entered: {result['user_address']}")
        print(f"Validated: {result['validated_address']}")
"""

import hashlib
import logging
from dataclasses import asdict, dataclass
from typing import Any

from django.core.cache import cache

from .services import AutocompleteClient

logger = logging.getLogger(__name__)


@dataclass
class AddressValidationResult:
    """Result of address validation with mismatch detection"""

    is_valid: bool
    has_mismatch: bool
    confidence: float  # 0.0 to 1.0

    # Original user input
    user_address: dict[str, str]

    # Validated address from provider (Australia Post, etc.)
    validated_address: dict[str, str] | None = None

    # Autocomplete suggestion (OSM data)
    autocomplete_suggestion: dict[str, str] | None = None

    # Mismatch details
    mismatch_fields: list[str] = None
    mismatch_reason: str | None = None

    # Suggestions for correction
    suggestions: list[dict[str, str]] = None

    # Provider-specific data
    provider_response: dict[str, Any] | None = None

    # Validation errors
    errors: list[str] = None

    def __post_init__(self):
        if self.mismatch_fields is None:
            self.mismatch_fields = []
        if self.suggestions is None:
            self.suggestions = []
        if self.errors is None:
            self.errors = []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def get_user_friendly_message(self) -> str:
        """Get user-friendly validation message"""
        if not self.is_valid:
            return f"Invalid address: {', '.join(self.errors)}"

        if not self.has_mismatch:
            return "Address validated successfully"

        if self.mismatch_reason:
            return f"Address verified but {self.mismatch_reason}"

        fields = ", ".join(self.mismatch_fields)
        return f"Address verified with minor differences in: {fields}"


class AddressValidator:
    """
    Address validation with multi-source verification

    Combines autocomplete (OSM) with provider-specific validation
    to detect and flag address discrepancies.
    """

    def __init__(self):
        self.autocomplete = AutocompleteClient()
        self._cache_ttl = 3600  # 1 hour

    def _get_cache_key(self, operation: str, data: dict[str, Any]) -> str:
        """Generate cache key"""
        data_str = "-".join(f"{k}:{v}" for k, v in sorted(data.items()) if v)
        hash_key = hashlib.md5(data_str.encode()).hexdigest()
        return f"address_validation:{operation}:{hash_key}"

    def _normalize_field(self, value: str | None) -> str:
        """Normalize field for comparison"""
        if not value:
            return ""
        return str(value).strip().upper().replace(".", "").replace(",", "")

    def _compare_fields(
        self, user_value: str | None, validated_value: str | None, field_name: str
    ) -> bool:
        """
        Compare two field values

        Returns True if they match (or are close enough)
        """
        if not user_value and not validated_value:
            return True

        if not user_value or not validated_value:
            return False

        # Normalize both values
        user_norm = self._normalize_field(user_value)
        validated_norm = self._normalize_field(validated_value)

        # Exact match
        if user_norm == validated_norm:
            return True

        # For postcodes, check if one is substring of other (e.g., "2000" vs "2000-1234")
        if field_name == "postcode":
            return user_norm in validated_norm or validated_norm in user_norm

        # For states, check abbreviations
        if field_name == "state":
            state_mappings = {
                "NSW": ["NEW SOUTH WALES", "NSW"],
                "VIC": ["VICTORIA", "VIC"],
                "QLD": ["QUEENSLAND", "QLD"],
                "SA": ["SOUTH AUSTRALIA", "SA"],
                "WA": ["WESTERN AUSTRALIA", "WA"],
                "TAS": ["TASMANIA", "TAS"],
                "NT": ["NORTHERN TERRITORY", "NT"],
                "ACT": ["AUSTRALIAN CAPITAL TERRITORY", "ACT"],
            }
            for _abbr, full_names in state_mappings.items():
                if user_norm in full_names and validated_norm in full_names:
                    return True

        # For streets, allow minor differences (ST vs STREET, RD vs ROAD)
        if field_name in ["address1", "address2"]:
            street_abbr = {
                "ST": "STREET",
                "RD": "ROAD",
                "AVE": "AVENUE",
                "DR": "DRIVE",
                "CT": "COURT",
                "PL": "PLACE",
                "CL": "CLOSE",
                "CR": "CRESCENT",
                "LN": "LANE",
                "WAY": "WAY",
                "PDE": "PARADE",
                "BLVD": "BOULEVARD",
                "HWY": "HIGHWAY",
            }

            user_words = user_norm.split()
            validated_words = validated_norm.split()

            # Replace abbreviations
            for i, word in enumerate(user_words):
                if word in street_abbr:
                    user_words[i] = street_abbr[word]

            for i, word in enumerate(validated_words):
                if word in street_abbr:
                    validated_words[i] = street_abbr[word]

            # Compare after normalization
            if " ".join(user_words) == " ".join(validated_words):
                return True

        return False

    async def validate_australian_address(
        self,
        user_input: dict[str, str],
        provider_account_id: int,
        include_autocomplete: bool = True,
    ) -> AddressValidationResult:
        """
        Validate Australian address with mismatch detection

        Args:
            user_input: User-entered address data with fields:
                - address1: Street address
                - address2: Apartment/suite (optional)
                - city: City/suburb name
                - state: State code (NSW, VIC, etc.)
                - postcode: Postal code
                - country: Country code (AU)
            provider_account_id: Australia Post provider account ID
            include_autocomplete: Whether to get autocomplete suggestions

        Returns:
            AddressValidationResult with validation details and mismatches
        """
        # Check cache
        cache_key = self._get_cache_key("australian", user_input)
        cached = cache.get(cache_key)
        if cached:
            return AddressValidationResult(**cached)

        # Get autocomplete suggestion if requested
        autocomplete_suggestion = None
        if include_autocomplete:
            query = f"{user_input.get('address1', '')}, {user_input.get('city', '')}"
            autocomplete_result = self.autocomplete.autocomplete(
                query=query, country_bias="au", limit=1
            )

            if autocomplete_result.get("suggestions"):
                first = autocomplete_result["suggestions"][0]
                components = first.get("components", {})

                autocomplete_suggestion = {
                    "address1": f"{components.get('house_number', '')} {components.get('road', '')}".strip(),
                    "city": components.get("suburb") or components.get("city", ""),
                    "state": components.get("state", ""),
                    "postcode": components.get("postcode", ""),
                    "country": "AU",
                }

        # Validate with Australia Post
        try:
            # Import here to avoid circular dependency
            from shipping.models import ShippingProviderAccount

            provider = ShippingProviderAccount.objects.get(id=provider_account_id)
            australia_post = provider.get_provider_instance()

            # Validate suburb and postcode
            validation_result = await australia_post.validate_suburb(
                suburb=user_input.get("city", ""),
                postcode=user_input.get("postcode", ""),
                state=user_input.get("state", ""),
            )

            if not validation_result.get("valid"):
                # Invalid according to Australia Post
                result = AddressValidationResult(
                    is_valid=False,
                    has_mismatch=False,
                    confidence=0.0,
                    user_address=user_input,
                    autocomplete_suggestion=autocomplete_suggestion,
                    errors=[validation_result.get("error", "Invalid suburb/postcode combination")],
                    provider_response=validation_result,
                )

                # Add suggestions if available
                if validation_result.get("suggestions"):
                    result.suggestions = validation_result["suggestions"]

                cache.set(cache_key, result.to_dict(), self._cache_ttl)
                return result

            # Valid according to Australia Post
            validated_address = {
                "address1": user_input.get(
                    "address1", ""
                ),  # Australia Post doesn't validate street address
                "city": validation_result.get("locality", user_input.get("city", "")),
                "state": validation_result.get("state", user_input.get("state", "")),
                "postcode": validation_result.get("postcode", user_input.get("postcode", "")),
                "country": "AU",
            }

            # Detect mismatches
            mismatches = []

            if not self._compare_fields(user_input.get("city"), validated_address["city"], "city"):
                mismatches.append("city")

            if not self._compare_fields(
                user_input.get("state"), validated_address["state"], "state"
            ):
                mismatches.append("state")

            if not self._compare_fields(
                user_input.get("postcode"), validated_address["postcode"], "postcode"
            ):
                mismatches.append("postcode")

            # Build mismatch reason
            mismatch_reason = None
            if mismatches:
                if "city" in mismatches:
                    mismatch_reason = f"suburb should be '{validated_address['city']}' instead of '{user_input.get('city')}'"
                elif "postcode" in mismatches:
                    mismatch_reason = f"postcode should be '{validated_address['postcode']}' instead of '{user_input.get('postcode')}'"
                elif "state" in mismatches:
                    mismatch_reason = f"state should be '{validated_address['state']}' instead of '{user_input.get('state')}'"

            result = AddressValidationResult(
                is_valid=True,
                has_mismatch=len(mismatches) > 0,
                confidence=1.0 if not mismatches else 0.85,
                user_address=user_input,
                validated_address=validated_address,
                autocomplete_suggestion=autocomplete_suggestion,
                mismatch_fields=mismatches,
                mismatch_reason=mismatch_reason,
                provider_response=validation_result,
            )

            cache.set(cache_key, result.to_dict(), self._cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Address validation error: {e}")
            result = AddressValidationResult(
                is_valid=False,
                has_mismatch=False,
                confidence=0.0,
                user_address=user_input,
                autocomplete_suggestion=autocomplete_suggestion,
                errors=[str(e)],
            )
            return result

    async def validate_international_address(
        self, user_input: dict[str, str]
    ) -> AddressValidationResult:
        """
        Validate international address using autocomplete only

        Args:
            user_input: User-entered address data

        Returns:
            AddressValidationResult
        """
        # Build query
        query_parts = [
            user_input.get("address1", ""),
            user_input.get("city", ""),
            user_input.get("postcode", ""),
            user_input.get("country", ""),
        ]
        query = ", ".join(filter(None, query_parts))

        # Get autocomplete suggestions
        autocomplete_result = self.autocomplete.autocomplete(query=query, limit=3)

        suggestions = []
        if autocomplete_result.get("suggestions"):
            for suggestion in autocomplete_result["suggestions"]:
                components = suggestion.get("components", {})
                suggestions.append(
                    {
                        "address1": f"{components.get('house_number', '')} {components.get('road', '')}".strip(),
                        "city": components.get("city") or components.get("suburb", ""),
                        "state": components.get("state", ""),
                        "postcode": components.get("postcode", ""),
                        "country": components.get("country", ""),
                    }
                )

        # For international addresses, we can't definitively validate
        # without provider-specific APIs, so we return based on autocomplete
        is_valid = len(suggestions) > 0
        confidence = suggestions[0].get("confidence", 0.8) if is_valid else 0.0

        result = AddressValidationResult(
            is_valid=is_valid,
            has_mismatch=False,
            confidence=confidence,
            user_address=user_input,
            autocomplete_suggestion=suggestions[0] if suggestions else None,
            suggestions=suggestions,
            errors=[] if is_valid else ["Could not find matching address"],
        )

        return result
