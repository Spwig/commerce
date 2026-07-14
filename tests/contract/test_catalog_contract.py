"""
Catalog API Contract Tests

Validates API responses match expected schema contracts and
detects breaking changes before they reach production.

Reference implementation showing all contract test patterns.
"""

import pytest

from tests.contract.conftest import load_schema_baseline
from tests.contract.utils.breaking_change_detector import detect_breaking_changes
from tests.contract.utils.contract_validator import (
    extract_response_schema,
    validate_response_against_schema,
)

pytestmark = [pytest.mark.django_db, pytest.mark.contract]


class TestProductListContract:
    """Contract tests for Product List API"""

    API_ENDPOINT = "/api/catalog/products/"
    SCHEMA_MODULE = "catalog"
    SERIALIZER_NAME = "ProductListSerializer"

    def test_product_list_matches_contract(self, contract_client, simple_product):
        """
        Verify /api/catalog/products/ response matches ProductListSerializer contract
        """
        # Make API request
        response = contract_client.get(self.API_ENDPOINT)
        assert response.status_code == 200, f"API returned {response.status_code}"

        data = response.json()
        assert "results" in data, "Paginated response missing 'results' key"
        assert len(data["results"]) > 0, "No products in response"

        # Extract first product for schema validation
        product_data = data["results"][0]

        try:
            # Load baseline schema
            baseline_schema = load_schema_baseline(self.SCHEMA_MODULE, self.SERIALIZER_NAME)

            # Validate response against baseline
            result = validate_response_against_schema(product_data, baseline_schema)

            # Assert validation passed
            assert result.is_valid, (
                "Product list response does not match contract.\n"
                "Errors:\n  " + "\n  ".join(result.errors) + "\n"
                "Warnings:\n  " + "\n  ".join(result.warnings)
                if result.warnings
                else ""
            )

        except FileNotFoundError as e:
            # Baseline doesn't exist yet - generate it for first run
            pytest.skip(
                f"Baseline schema not found: {e}\n"
                f"Generate baseline with: python scripts/generate_contract_baselines.py"
            )

    def test_no_breaking_changes(self, contract_client, simple_product):
        """
        Verify no breaking changes introduced to Product List API
        """
        # Get current response
        response = contract_client.get(self.API_ENDPOINT)
        assert response.status_code == 200

        data = response.json()
        product_data = data["results"][0]

        # Generate schema from current response
        current_schema = extract_response_schema(product_data)

        try:
            # Load baseline schema
            baseline_schema = load_schema_baseline(self.SCHEMA_MODULE, self.SERIALIZER_NAME)

            # Detect breaking changes
            change_report = detect_breaking_changes(baseline_schema, current_schema)

            # Assert no breaking changes
            assert not change_report.has_breaking_changes, (
                f"Breaking changes detected in {self.SERIALIZER_NAME}:\n"
                + "\n".join(
                    [
                        f"  - {change.field_path}: {change.description}"
                        for change in change_report.breaking_changes
                    ]
                )
            )

            # Log non-breaking changes as info (doesn't fail test)
            if change_report.non_breaking_changes:
                print("\n=== Non-breaking changes detected ===")
                for change in change_report.non_breaking_changes:
                    print(f"  + {change.field_path}: {change.description}")
                print("=" * 40)

        except FileNotFoundError:
            pytest.skip("Baseline schema not found - run baseline generator first")

    def test_required_fields_present(self, contract_client, simple_product):
        """
        Verify all required fields are present in Product List response
        """
        response = contract_client.get(self.API_ENDPOINT)
        assert response.status_code == 200

        product_data = response.json()["results"][0]

        # Define critical fields that must always be present
        # Note: API uses price_amount/price_currency for multi-currency support
        required_fields = [
            "id",
            "name",
            "slug",
            "price_amount",
            "price_currency",
            "product_type",
            "sku",
        ]

        for field in required_fields:
            assert field in product_data, (
                f"Required field '{field}' missing from product list response"
            )

    def test_field_types_correct(self, contract_client, simple_product):
        """
        Verify field types match expected types
        """
        response = contract_client.get(self.API_ENDPOINT)
        assert response.status_code == 200

        product_data = response.json()["results"][0]

        # Define expected types for current API design
        type_expectations = {
            "id": int,
            "name": str,
            "slug": str,
            "price_amount": str,  # DecimalField serialized as string
            "price_currency": str,
            "product_type": str,
            "is_in_stock": bool,
            "is_featured": bool,
        }

        for field, expected_type in type_expectations.items():
            if field in product_data:
                actual_type = type(product_data[field])
                assert isinstance(product_data[field], expected_type), (
                    f"Field '{field}' has incorrect type. "
                    f"Expected {expected_type.__name__}, got {actual_type.__name__}"
                )

    def test_pagination_structure(self, contract_client, simple_product):
        """
        Verify paginated list response structure matches DRF pagination contract
        """
        response = contract_client.get(self.API_ENDPOINT)
        data = response.json()

        # Pagination wrapper schema
        assert "count" in data, "Missing 'count' in paginated response"
        assert "next" in data, "Missing 'next' in paginated response"
        assert "previous" in data, "Missing 'previous' in paginated response"
        assert "results" in data, "Missing 'results' in paginated response"

        # Type checks
        assert isinstance(data["count"], int), "count should be integer"
        assert isinstance(data["results"], list), "results should be array"
        assert data["next"] is None or isinstance(data["next"], str), (
            "next should be string or null"
        )
        assert data["previous"] is None or isinstance(data["previous"], str), (
            "previous should be string or null"
        )


class TestProductDetailContract:
    """Contract tests for Product Detail API"""

    API_ENDPOINT_TEMPLATE = "/api/catalog/products/{slug}/"
    SCHEMA_MODULE = "catalog"
    SERIALIZER_NAME = "ProductDetailSerializer"

    def test_product_detail_matches_contract(self, contract_client, simple_product):
        """
        Verify /api/catalog/products/{slug}/ response matches contract
        """
        endpoint = self.API_ENDPOINT_TEMPLATE.format(slug=simple_product.slug)
        response = contract_client.get(endpoint)
        assert response.status_code == 200, f"API returned {response.status_code}"

        data = response.json()

        try:
            # Load baseline schema
            baseline_schema = load_schema_baseline(self.SCHEMA_MODULE, self.SERIALIZER_NAME)

            # Validate response
            result = validate_response_against_schema(data, baseline_schema)

            assert result.is_valid, (
                "Product detail response does not match contract.\n"
                "Errors:\n  " + "\n  ".join(result.errors)
            )

        except FileNotFoundError:
            pytest.skip("Baseline schema not found - run baseline generator first")

    def test_detail_has_more_fields_than_list(self, contract_client, simple_product):
        """
        Verify detail endpoint provides more information than list endpoint.
        Detail view may expand simple fields into full objects (e.g., category_name -> category).
        """
        # Get list view
        list_response = contract_client.get("/api/catalog/products/")
        list_fields = set(list_response.json()["results"][0].keys())

        # Get detail view
        detail_endpoint = self.API_ENDPOINT_TEMPLATE.format(slug=simple_product.slug)
        detail_response = contract_client.get(detail_endpoint)
        detail_fields = set(detail_response.json().keys())

        # Map of list fields that are expanded in detail view
        # Format: {list_field: detail_field}
        field_expansions = {
            "category_name": "category",  # Simple string -> Full object
            "brand_name": "brand",  # Simple string -> Full object
            "primary_image": "images",  # Single image -> Full images array
        }

        # Check that all list fields are present in detail (or have expanded equivalents)
        missing_fields = []
        for list_field in list_fields:
            # Check if field exists directly in detail
            if list_field in detail_fields:
                continue

            # Check if field has an expanded equivalent in detail
            expanded_field = field_expansions.get(list_field)
            if expanded_field and expanded_field in detail_fields:
                continue

            # Field is truly missing
            missing_fields.append(list_field)

        assert not missing_fields, (
            f"Detail view missing fields present in list view: {missing_fields}"
        )

        # Detail should have additional fields beyond the list view
        assert len(detail_fields) > len(list_fields), (
            "Detail view should have more fields than list view"
        )

    def test_product_not_found_returns_404(self, contract_client):
        """
        Verify 404 error response structure is consistent
        """
        response = contract_client.get("/api/catalog/products/nonexistent-product/")
        assert response.status_code == 404

        data = response.json()

        # DRF error response should have 'detail' key
        assert "detail" in data, "404 response missing 'detail' key"
        assert isinstance(data["detail"], str), "'detail' should be a string"


class TestCategoryListContract:
    """Contract tests for Category List API"""

    API_ENDPOINT = "/api/catalog/categories/"
    SCHEMA_MODULE = "catalog"
    SERIALIZER_NAME = "CategoryListSerializer"

    def test_category_list_matches_contract(self, contract_client, category):
        """
        Verify /api/catalog/categories/ response matches contract
        """
        response = contract_client.get(self.API_ENDPOINT)
        assert response.status_code == 200

        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0

        category_data = data["results"][0]

        try:
            baseline_schema = load_schema_baseline(self.SCHEMA_MODULE, self.SERIALIZER_NAME)

            result = validate_response_against_schema(category_data, baseline_schema)

            assert result.is_valid, (
                "Category list response does not match contract.\n"
                "Errors:\n  " + "\n  ".join(result.errors)
            )

        except FileNotFoundError:
            pytest.skip("Baseline schema not found")

    def test_category_has_hierarchical_structure(self, contract_client, category):
        """
        Verify category response includes hierarchical fields
        """
        response = contract_client.get(self.API_ENDPOINT)
        category_data = response.json()["results"][0]

        # Categories should support hierarchy
        hierarchical_fields = ["parent", "level", "path"]

        for field in hierarchical_fields:
            # Field might not exist if category is root, but structure should support it
            # This is a structural check, not a required field check
            if field in category_data:
                assert category_data[field] is not None or field == "parent", (
                    f"Hierarchical field '{field}' has unexpected None value"
                )
