"""
Custom Fields integration tests.

Tests field definitions API, model mixin behavior, validators,
and admin CRUD operations.
"""

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from custom_fields.models import CustomFieldDefinition, CustomFieldGroup
from custom_fields.validators import validate_custom_field_value
from tests.factories import ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.custom_fields]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def product_ct(db):
    """ContentType for catalog.Product."""
    return ContentType.objects.get(app_label="catalog", model="product")


@pytest.fixture
def category_ct(db):
    """ContentType for catalog.Category."""
    return ContentType.objects.get(app_label="catalog", model="category")


@pytest.fixture
def order_ct(db):
    """ContentType for orders.Order."""
    return ContentType.objects.get(app_label="orders", model="order")


@pytest.fixture
def field_group(product_ct):
    """A custom field group for products."""
    return CustomFieldGroup.objects.create(
        name="Test Group",
        slug="test-group",
        content_type=product_ct,
        sort_order=0,
        is_active=True,
    )


@pytest.fixture
def text_field(field_group, product_ct):
    """A text custom field definition."""
    return CustomFieldDefinition.objects.create(
        group=field_group,
        content_type=product_ct,
        name="External ID",
        slug="external_id",
        field_type="text",
        help_text_value="ID from external system",
        is_required=False,
        is_active=True,
        show_on_storefront=True,
        sort_order=0,
    )


@pytest.fixture
def number_field(field_group, product_ct):
    """A number custom field definition."""
    return CustomFieldDefinition.objects.create(
        group=field_group,
        content_type=product_ct,
        name="Weight Override",
        slug="weight_override",
        field_type="number",
        help_text_value="Override weight in grams",
        validation_config={"min": 0, "max": 99999},
        is_required=False,
        is_active=True,
        sort_order=1,
    )


@pytest.fixture
def select_field(field_group, product_ct):
    """A select custom field definition."""
    return CustomFieldDefinition.objects.create(
        group=field_group,
        content_type=product_ct,
        name="Material",
        slug="material",
        field_type="select",
        validation_config={
            "choices": [
                {"value": "cotton", "label": "Cotton"},
                {"value": "silk", "label": "Silk"},
                {"value": "wool", "label": "Wool"},
            ]
        },
        is_required=False,
        is_active=True,
        sort_order=2,
    )


@pytest.fixture
def boolean_field(field_group, product_ct):
    """A boolean custom field definition."""
    return CustomFieldDefinition.objects.create(
        group=field_group,
        content_type=product_ct,
        name="Handmade",
        slug="handmade",
        field_type="boolean",
        default_value=False,
        is_active=True,
        sort_order=3,
    )


# ============================================================
# Model Mixin Tests
# ============================================================


class TestCustomFieldsMixin:
    def test_get_custom_field_value_returns_stored_value(self, site_settings, category, text_field):
        """Stored custom field values are returned correctly."""
        product = ProductFactory(
            category=category,
            custom_fields={"external_id": "EXT-001"},
        )
        assert product.get_custom_field_value("external_id") == "EXT-001"

    def test_get_custom_field_value_returns_default_when_missing(
        self, site_settings, category, boolean_field
    ):
        """Fields not yet set return the definition default."""
        product = ProductFactory(category=category, custom_fields={})
        assert product.get_custom_field_value("handmade") is False

    def test_get_custom_field_value_returns_none_for_unknown_slug(self, site_settings, category):
        """Unknown field slugs return None (or the provided default)."""
        product = ProductFactory(category=category, custom_fields={})
        assert product.get_custom_field_value("nonexistent") is None
        assert product.get_custom_field_value("nonexistent", "fallback") == "fallback"

    def test_set_custom_field_value(self, site_settings, category, text_field):
        """set_custom_field_value updates the JSON field."""
        product = ProductFactory(category=category)
        product.set_custom_field_value("external_id", "EXT-002")
        product.save()
        product.refresh_from_db()
        assert product.custom_fields["external_id"] == "EXT-002"

    def test_custom_fields_default_to_empty_dict(self, site_settings, category):
        """New records have an empty custom_fields dict."""
        product = ProductFactory(category=category)
        assert product.custom_fields == {}

    def test_json_field_queryable(self, site_settings, category, text_field):
        """Custom field values can be queried via Django ORM."""
        from catalog.models import Product

        p1 = ProductFactory(
            category=category,
            custom_fields={"external_id": "EXT-100"},
        )
        p2 = ProductFactory(
            category=category,
            custom_fields={"external_id": "EXT-200"},
        )
        results = Product.objects.filter(custom_fields__external_id="EXT-100")
        assert p1 in results
        assert p2 not in results


# ============================================================
# Validator Tests
# ============================================================


class TestValidators:
    def _make_field_def(self, field_type, config=None, required=False, name="Test"):
        """Create a mock field definition for validation testing."""
        from types import SimpleNamespace

        return SimpleNamespace(
            field_type=field_type,
            validation_config=config or {},
            is_required=required,
            name=name,
        )

    def test_text_valid(self):
        """Text validation passes for a simple string."""
        fd = self._make_field_def("text")
        result = validate_custom_field_value(fd, "Hello world")
        assert result == "Hello world"

    def test_text_max_length(self):
        """Text validation fails if value exceeds max_length."""
        fd = self._make_field_def("text", {"max_length": 100})
        with pytest.raises(ValidationError):
            validate_custom_field_value(fd, "x" * 101)

    def test_number_valid(self):
        """Number validation coerces string to int."""
        fd = self._make_field_def("number")
        result = validate_custom_field_value(fd, "42")
        assert result == 42

    def test_number_out_of_range(self):
        """Number validation fails if outside min/max."""
        fd = self._make_field_def("number", {"min": 0, "max": 100})
        with pytest.raises(ValidationError):
            validate_custom_field_value(fd, "150")

    def test_decimal_valid(self):
        """Decimal validation coerces string to float."""
        fd = self._make_field_def("decimal")
        result = validate_custom_field_value(fd, "3.14")
        assert result == 3.14

    def test_boolean_true_values(self):
        """Boolean validation accepts truthy values."""
        fd = self._make_field_def("boolean")
        for truthy in [True, "true", "1", "on", "yes"]:
            result = validate_custom_field_value(fd, truthy)
            assert result is True

    def test_boolean_false_values(self):
        """Boolean validation returns False for falsy values."""
        fd = self._make_field_def("boolean")
        for falsy in [False, "false", "0"]:
            result = validate_custom_field_value(fd, falsy)
            assert result is False

    def test_select_valid_choice(self):
        """Select validation passes for a valid choice."""
        fd = self._make_field_def("select", {"choices": [{"value": "a"}, {"value": "b"}]})
        result = validate_custom_field_value(fd, "a")
        assert result == "a"

    def test_select_invalid_choice(self):
        """Select validation fails for an invalid choice."""
        fd = self._make_field_def("select", {"choices": [{"value": "a"}, {"value": "b"}]})
        with pytest.raises(ValidationError):
            validate_custom_field_value(fd, "z")

    def test_email_valid(self):
        """Email validation passes for a valid email."""
        fd = self._make_field_def("email")
        result = validate_custom_field_value(fd, "test@example.com")
        assert result == "test@example.com"

    def test_email_invalid(self):
        """Email validation fails for an invalid email."""
        fd = self._make_field_def("email")
        with pytest.raises(ValidationError):
            validate_custom_field_value(fd, "not-an-email")

    def test_url_valid(self):
        """URL validation passes for a valid URL."""
        fd = self._make_field_def("url")
        result = validate_custom_field_value(fd, "https://example.com")
        assert result == "https://example.com"

    def test_empty_non_required_returns_empty(self):
        """Empty string values pass through for non-required fields."""
        fd = self._make_field_def("text")
        result = validate_custom_field_value(fd, "")
        assert result == ""

    def test_required_field_rejects_empty(self):
        """Required fields reject empty values."""
        fd = self._make_field_def("text", required=True)
        with pytest.raises(ValidationError):
            validate_custom_field_value(fd, "")


# ============================================================
# Model Tests
# ============================================================


class TestCustomFieldModels:
    def test_group_creation(self, product_ct):
        """Groups can be created with a content type."""
        group = CustomFieldGroup.objects.create(
            name="Shipping Info",
            slug="shipping-info",
            content_type=product_ct,
        )
        assert "Shipping Info" in str(group)
        assert group.is_active is True

    def test_field_definition_creation(self, field_group, product_ct):
        """Field definitions can be created with validation config."""
        field = CustomFieldDefinition.objects.create(
            group=field_group,
            content_type=product_ct,
            name="Max Width",
            slug="max_width",
            field_type="decimal",
            validation_config={"min": 0, "max": 1000},
        )
        assert "Max Width" in str(field)
        assert field.is_active is True

    def test_slug_unique_per_content_type(self, field_group, product_ct):
        """Two fields can't share the same slug for the same content type."""
        CustomFieldDefinition.objects.create(
            group=field_group,
            content_type=product_ct,
            name="Field One",
            slug="unique_slug",
            field_type="text",
        )
        with pytest.raises(IntegrityError):
            CustomFieldDefinition.objects.create(
                group=field_group,
                content_type=product_ct,
                name="Field Two",
                slug="unique_slug",
                field_type="text",
            )

    def test_same_slug_different_content_type(self, field_group, product_ct, category_ct):
        """Same slug is allowed for different content types."""
        CustomFieldDefinition.objects.create(
            group=field_group,
            content_type=product_ct,
            name="Priority",
            slug="priority",
            field_type="number",
        )
        cat_group = CustomFieldGroup.objects.create(
            name="Cat Group",
            slug="cat-group",
            content_type=category_ct,
        )
        field2 = CustomFieldDefinition.objects.create(
            group=cat_group,
            content_type=category_ct,
            name="Priority",
            slug="priority",
            field_type="number",
        )
        assert field2.pk is not None

    def test_get_cached_for_content_type(self, text_field, product_ct):
        """Cached retrieval returns active definitions."""
        defs = CustomFieldDefinition.get_cached_for_content_type(product_ct)
        slugs = [d.slug for d in defs]
        assert "external_id" in slugs

    def test_inactive_fields_excluded(self, field_group, product_ct):
        """Inactive field definitions are excluded from cached results."""
        CustomFieldDefinition.objects.create(
            group=field_group,
            content_type=product_ct,
            name="Hidden Field",
            slug="hidden_field",
            field_type="text",
            is_active=False,
        )
        # Invalidate cache
        CustomFieldDefinition.invalidate_cache(product_ct)
        defs = CustomFieldDefinition.get_cached_for_content_type(product_ct)
        slugs = [d.slug for d in defs]
        assert "hidden_field" not in slugs


# ============================================================
# API Tests
# ============================================================


class TestCustomFieldsAPI:
    def test_list_definitions_requires_auth(self, api_client):
        """API requires authentication."""
        resp = api_client.get("/api/custom-fields/definitions/")
        assert resp.status_code in (401, 403)

    def test_list_definitions_authenticated(self, admin_client, text_field, number_field):
        """Authenticated users can list definitions."""
        resp = admin_client.get("/api/custom-fields/definitions/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] >= 2

    def test_filter_by_model(self, admin_client, text_field, category_ct):
        """Definitions can be filtered by model name."""
        # Create a category field
        cat_group = CustomFieldGroup.objects.create(
            name="Cat Attrs",
            slug="cat-attrs",
            content_type=category_ct,
        )
        CustomFieldDefinition.objects.create(
            group=cat_group,
            content_type=category_ct,
            name="Display Order",
            slug="display_order",
            field_type="number",
        )

        resp = admin_client.get("/api/custom-fields/definitions/?model=product")
        data = resp.json()
        slugs = [r["slug"] for r in data["results"]]
        assert "external_id" in slugs
        assert "display_order" not in slugs

    def test_definition_detail(self, admin_client, text_field):
        """Single definition can be retrieved by ID."""
        resp = admin_client.get(f"/api/custom-fields/definitions/{text_field.pk}/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["slug"] == "external_id"
        assert data["field_type"] == "text"
        assert data["group_name"] == "Test Group"

    def test_definition_includes_choices_for_select(self, admin_client, select_field):
        """Select field definitions include choices in the response."""
        resp = admin_client.get(f"/api/custom-fields/definitions/{select_field.pk}/")
        data = resp.json()
        assert len(data["choices"]) == 3
        values = [c["value"] for c in data["choices"]]
        assert "cotton" in values
        assert "silk" in values


# ============================================================
# Admin Management View Tests
# ============================================================


class TestAdminManagement:
    def test_management_page_accessible(self, admin_user):
        """Management page loads for staff users."""
        from django.test import Client

        client = Client()
        client.force_login(admin_user)
        resp = client.get("/en/admin/custom-fields/")
        assert resp.status_code == 200

    def test_create_group_via_ajax(self, admin_user, product_ct):
        """Groups can be created via AJAX POST."""
        import json as json_mod

        from django.test import Client

        client = Client()
        client.force_login(admin_user)
        resp = client.post(
            "/en/admin/custom-fields/groups/create/",
            data=json_mod.dumps(
                {
                    "name": "New Group",
                    "content_type_id": product_ct.pk,
                }
            ),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert CustomFieldGroup.objects.filter(name="New Group").exists()

    def test_create_field_via_ajax(self, admin_user, field_group, product_ct):
        """Fields can be created via AJAX POST."""
        import json as json_mod

        from django.test import Client

        client = Client()
        client.force_login(admin_user)
        resp = client.post(
            "/en/admin/custom-fields/fields/create/",
            data=json_mod.dumps(
                {
                    "group_id": field_group.pk,
                    "name": "Test AJAX Field",
                    "field_type": "text",
                    "help_text": "Created via test",
                }
            ),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert CustomFieldDefinition.objects.filter(slug="test_ajax_field").exists()

    def test_delete_group_soft_deletes(self, admin_user, field_group):
        """Deleting a group soft-deletes it via SoftDeleteModel (is_deleted=True)."""
        from django.test import Client

        client = Client()
        client.force_login(admin_user)
        resp = client.post(
            f"/en/admin/custom-fields/groups/{field_group.pk}/delete/",
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert resp.status_code == 200
        # delete_group() calls SoftDeleteModel.delete(user=) which sets is_deleted=True.
        # Row is filtered out of default manager -- refetch via all_objects.
        refreshed = CustomFieldGroup.all_objects.get(pk=field_group.pk)
        assert refreshed.is_deleted is True
