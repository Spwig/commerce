"""
Custom Fields comprehensive integration tests.

Tests models (CRUD, soft delete lifecycle, auto-slug, caching, get_choices,
content_type sync), admin views (management page, AJAX CRUD, recycle bin,
restore, permanent delete, permissions, AJAX header requirement),
signals (cache invalidation), and URL resolution.
"""

import json

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.test import Client
from django.urls import resolve, reverse

from custom_fields.models import (
    CACHE_KEY_PREFIX,
    SUPPORTED_MODELS,
    CustomFieldDefinition,
    CustomFieldGroup,
    get_supported_content_types,
)
from tests.factories import (
    CustomFieldDefinitionFactory,
    CustomFieldGroupFactory,
    UserFactory,
)

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
def profile_ct(db):
    """ContentType for accounts.CustomerProfile."""
    return ContentType.objects.get(app_label="accounts", model="customerprofile")


@pytest.fixture
def staff_user(db):
    """Staff user for admin views."""
    return UserFactory(staff=True)


@pytest.fixture
def regular_user(db):
    """Non-staff user for permission tests."""
    return UserFactory()


@pytest.fixture
def staff_client(staff_user):
    """Django test Client authenticated as staff."""
    client = Client()
    client.force_login(staff_user)
    return client


@pytest.fixture
def anon_client():
    """Unauthenticated Django test Client."""
    return Client()


@pytest.fixture
def regular_client(regular_user):
    """Django test Client authenticated as non-staff user."""
    client = Client()
    client.force_login(regular_user)
    return client


@pytest.fixture
def group(product_ct):
    """Active custom field group for products."""
    return CustomFieldGroup.objects.create(
        name="Product Attributes",
        slug="product-attributes",
        content_type=product_ct,
        sort_order=0,
        is_active=True,
        show_on_storefront=True,
    )


@pytest.fixture
def second_group(product_ct):
    """Second group for ordering tests."""
    return CustomFieldGroup.objects.create(
        name="External IDs",
        slug="external-ids",
        content_type=product_ct,
        sort_order=1,
        is_active=True,
    )


@pytest.fixture
def text_field_def(group, product_ct):
    """Text field definition."""
    return CustomFieldDefinition.objects.create(
        group=group,
        content_type=product_ct,
        name="Material",
        slug="material",
        field_type="text",
        help_text_value="Product material",
        is_required=False,
        is_active=True,
        show_on_storefront=True,
        sort_order=0,
    )


@pytest.fixture
def select_field_def(group, product_ct):
    """Select field definition with choices."""
    return CustomFieldDefinition.objects.create(
        group=group,
        content_type=product_ct,
        name="Size Category",
        slug="size_category",
        field_type="select",
        validation_config={
            "choices": [
                {"value": "small", "label": "Small"},
                {"value": "medium", "label": "Medium"},
                {"value": "large", "label": "Large"},
            ]
        },
        is_active=True,
        sort_order=1,
    )


@pytest.fixture
def multiselect_field_def(group, product_ct):
    """Multiselect field definition with choices."""
    return CustomFieldDefinition.objects.create(
        group=group,
        content_type=product_ct,
        name="Available Colors",
        slug="available_colors",
        field_type="multiselect",
        validation_config={
            "choices": [
                {"value": "red", "label": "Red"},
                {"value": "blue", "label": "Blue"},
                {"value": "green", "label": "Green"},
            ]
        },
        is_active=True,
        sort_order=2,
    )


@pytest.fixture(autouse=True)
def clear_custom_fields_cache():
    """Clear custom fields cache before and after each test.

    Uses cache.clear() as a safe fallback if the DB transaction
    is broken (e.g., after IntegrityError in a constraint test).
    """
    cache.clear()
    yield
    cache.clear()


def _ajax_post(client, url, data=None):
    """Send AJAX POST with proper headers."""
    return client.post(
        url,
        data=json.dumps(data or {}),
        content_type="application/json",
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )


def _ajax_get(client, url):
    """Send AJAX GET with proper headers."""
    return client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")


# ============================================================
# Model Tests: CustomFieldGroup
# ============================================================


class TestCustomFieldGroupModel:
    def test_create_group(self, product_ct):
        """Groups can be created with basic fields."""
        grp = CustomFieldGroup.objects.create(
            name="Test Group",
            slug="test-group",
            content_type=product_ct,
        )
        assert grp.pk is not None
        assert grp.name == "Test Group"
        assert grp.slug == "test-group"
        assert grp.is_active is True
        assert grp.show_on_storefront is False
        assert grp.sort_order == 0
        assert grp.translations == {}

    def test_str_representation(self, group):
        """__str__ includes name and content type."""
        result = str(group)
        assert "Product Attributes" in result
        assert "product" in result.lower()

    def test_auto_slug_generation(self, product_ct):
        """Slug is auto-generated from name if not provided."""
        grp = CustomFieldGroup(
            name="My Custom Group",
            content_type=product_ct,
        )
        grp.save()
        assert grp.slug == "my-custom-group"

    def test_explicit_slug_preserved(self, product_ct):
        """Explicitly provided slug is not overwritten."""
        grp = CustomFieldGroup.objects.create(
            name="My Custom Group",
            slug="custom-slug",
            content_type=product_ct,
        )
        assert grp.slug == "custom-slug"

    def test_slug_unique_per_content_type(self, product_ct):
        """Same slug cannot be used twice for the same content type."""
        CustomFieldGroup.objects.create(
            name="Group A",
            slug="shared-slug",
            content_type=product_ct,
        )
        with pytest.raises(IntegrityError), transaction.atomic():
            CustomFieldGroup.objects.create(
                name="Group B",
                slug="shared-slug",
                content_type=product_ct,
            )

    def test_same_slug_different_content_types(self, product_ct, category_ct):
        """Same slug is allowed for different content types."""
        CustomFieldGroup.objects.create(
            name="Metadata",
            slug="metadata",
            content_type=product_ct,
        )
        grp2 = CustomFieldGroup.objects.create(
            name="Metadata",
            slug="metadata",
            content_type=category_ct,
        )
        assert grp2.pk is not None

    def test_ordering(self, product_ct):
        """Groups are ordered by content_type, sort_order, name."""
        grp_b = CustomFieldGroup.objects.create(
            name="B Group", slug="b-group", content_type=product_ct, sort_order=1
        )
        grp_a = CustomFieldGroup.objects.create(
            name="A Group", slug="a-group", content_type=product_ct, sort_order=0
        )
        groups = list(CustomFieldGroup.objects.filter(content_type=product_ct))
        assert groups[0].pk == grp_a.pk
        assert groups[1].pk == grp_b.pk

    def test_translations_json_field(self, product_ct):
        """Translations field stores and retrieves JSON correctly."""
        grp = CustomFieldGroup.objects.create(
            name="Product Info",
            slug="product-info",
            content_type=product_ct,
            translations={"de": "Produktinformationen", "fr": "Informations produit"},
        )
        grp.refresh_from_db()
        assert grp.translations["de"] == "Produktinformationen"
        assert grp.translations["fr"] == "Informations produit"


# ============================================================
# Model Tests: CustomFieldGroup Caching
# ============================================================


class TestCustomFieldGroupCaching:
    def test_get_cached_for_content_type_returns_active_groups(self, group, product_ct):
        """Cached method returns only active groups."""
        groups = CustomFieldGroup.get_cached_for_content_type(product_ct)
        assert len(groups) >= 1
        names = [g.name for g in groups]
        assert "Product Attributes" in names

    def test_get_cached_excludes_inactive_groups(self, product_ct):
        """Inactive groups are excluded from cached results."""
        CustomFieldGroup.objects.create(
            name="Active Group",
            slug="active-grp",
            content_type=product_ct,
            is_active=True,
        )
        CustomFieldGroup.objects.create(
            name="Inactive Group",
            slug="inactive-grp",
            content_type=product_ct,
            is_active=False,
        )
        # Invalidate cache to fetch fresh
        CustomFieldDefinition.invalidate_cache(product_ct)
        groups = CustomFieldGroup.get_cached_for_content_type(product_ct)
        names = [g.name for g in groups]
        assert "Active Group" in names
        assert "Inactive Group" not in names

    def test_cached_result_is_reused(self, group, product_ct):
        """Second call returns cached result from the cache layer."""
        # First call populates cache
        result1 = CustomFieldGroup.get_cached_for_content_type(product_ct)
        # Verify cache key now holds data
        cache_key = f"{CACHE_KEY_PREFIX}:groups:{product_ct.pk}"
        cached_data = cache.get(cache_key)
        assert cached_data is not None
        assert len(cached_data) == len(result1)
        # Second call returns same data from cache
        result2 = CustomFieldGroup.get_cached_for_content_type(product_ct)
        assert [g.pk for g in result1] == [g.pk for g in result2]

    def test_cache_key_format(self, product_ct):
        """Cache key follows expected format."""
        expected_key = f"{CACHE_KEY_PREFIX}:groups:{product_ct.pk}"
        # Populate cache
        CustomFieldGroup.get_cached_for_content_type(product_ct)
        # Verify key exists in cache
        assert cache.get(expected_key) is not None

    def test_invalidate_cache_clears_groups(self, group, product_ct):
        """invalidate_cache removes both field and group cache entries."""
        # Populate cache
        CustomFieldGroup.get_cached_for_content_type(product_ct)
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        # Invalidate
        CustomFieldDefinition.invalidate_cache(product_ct)
        # Verify cleared
        groups_key = f"{CACHE_KEY_PREFIX}:groups:{product_ct.pk}"
        fields_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(groups_key) is None
        assert cache.get(fields_key) is None


# ============================================================
# Model Tests: CustomFieldDefinition
# ============================================================


class TestCustomFieldDefinitionModel:
    def test_create_field_definition(self, group, product_ct):
        """Field definitions can be created with all fields."""
        field_def = CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Weight",
            slug="weight_g",
            field_type="number",
            help_text_value="Weight in grams",
            validation_config={"min": 0, "max": 99999},
            is_required=True,
            is_active=True,
            show_on_storefront=True,
            is_translatable=False,
            sort_order=5,
        )
        assert field_def.pk is not None
        assert field_def.field_type == "number"
        assert field_def.is_required is True
        assert field_def.validation_config == {"min": 0, "max": 99999}

    def test_str_representation(self, text_field_def):
        """__str__ includes name, type display, and content type."""
        result = str(text_field_def)
        assert "Material" in result
        assert "Text" in result

    def test_auto_slug_generation_underscore(self, group, product_ct):
        """Auto-slug replaces hyphens with underscores for JSON key compatibility."""
        field_def = CustomFieldDefinition(
            group=group,
            content_type=product_ct,
            name="My Custom Field",
            field_type="text",
        )
        field_def.save()
        assert field_def.slug == "my_custom_field"

    def test_explicit_slug_preserved(self, group, product_ct):
        """Explicitly provided slug is not overwritten."""
        field_def = CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Some Field",
            slug="explicit_slug",
            field_type="text",
        )
        assert field_def.slug == "explicit_slug"

    def test_content_type_auto_sync_from_group(self, group):
        """content_type is auto-set from group if not provided."""
        field_def = CustomFieldDefinition(
            group=group,
            name="Auto CT Field",
            slug="auto_ct_field",
            field_type="text",
        )
        field_def.save()
        assert field_def.content_type_id == group.content_type_id

    def test_slug_unique_per_content_type(self, group, product_ct):
        """Same slug cannot be used twice for the same content type."""
        CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Field A",
            slug="duplicate_slug",
            field_type="text",
        )
        with pytest.raises(IntegrityError), transaction.atomic():
            CustomFieldDefinition.objects.create(
                group=group,
                content_type=product_ct,
                name="Field B",
                slug="duplicate_slug",
                field_type="number",
            )

    def test_same_slug_different_content_types(self, group, product_ct, category_ct):
        """Same slug is allowed for different content types."""
        CustomFieldDefinition.objects.create(
            group=group,
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

    def test_all_field_types(self, group, product_ct):
        """All 12 field types can be created successfully."""
        field_types = [ft[0] for ft in CustomFieldDefinition.FIELD_TYPES]
        assert len(field_types) == 12
        for i, ft in enumerate(field_types):
            field_def = CustomFieldDefinition.objects.create(
                group=group,
                content_type=product_ct,
                name=f"Type {ft}",
                slug=f"type_{ft}_{i}",
                field_type=ft,
            )
            assert field_def.field_type == ft

    def test_default_value_json(self, group, product_ct):
        """default_value stores various JSON types correctly."""
        for value, expected in [
            (False, False),
            (42, 42),
            ("hello", "hello"),
            (["a", "b"], ["a", "b"]),
            (None, None),
        ]:
            field_def = CustomFieldDefinition.objects.create(
                group=group,
                content_type=product_ct,
                name=f"Default {value}",
                slug=f"default_{id(value)}",
                field_type="text",
                default_value=value,
            )
            field_def.refresh_from_db()
            assert field_def.default_value == expected


class TestGetChoices:
    def test_select_field_returns_choices(self, select_field_def):
        """get_choices returns choices list for select fields."""
        choices = select_field_def.get_choices()
        assert len(choices) == 3
        values = [c["value"] for c in choices]
        assert "small" in values
        assert "medium" in values
        assert "large" in values

    def test_multiselect_field_returns_choices(self, multiselect_field_def):
        """get_choices returns choices list for multiselect fields."""
        choices = multiselect_field_def.get_choices()
        assert len(choices) == 3
        values = [c["value"] for c in choices]
        assert "red" in values

    def test_text_field_returns_empty_choices(self, text_field_def):
        """get_choices returns empty list for non-select fields."""
        assert text_field_def.get_choices() == []

    def test_number_field_returns_empty_choices(self, group, product_ct):
        """get_choices returns empty list for number fields."""
        field_def = CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Count",
            slug="count",
            field_type="number",
        )
        assert field_def.get_choices() == []

    def test_select_with_empty_config_returns_empty(self, group, product_ct):
        """get_choices returns empty list when validation_config has no choices."""
        field_def = CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Empty Select",
            slug="empty_select",
            field_type="select",
            validation_config={},
        )
        assert field_def.get_choices() == []


# ============================================================
# Model Tests: CustomFieldDefinition Caching
# ============================================================


class TestCustomFieldDefinitionCaching:
    def test_get_cached_for_content_type_returns_active(self, text_field_def, product_ct):
        """Cached method returns only active field definitions."""
        defs = CustomFieldDefinition.get_cached_for_content_type(product_ct)
        slugs = [d.slug for d in defs]
        assert "material" in slugs

    def test_get_cached_excludes_inactive_fields(self, group, product_ct):
        """Inactive fields are excluded from cached results."""
        CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Active",
            slug="active_f",
            field_type="text",
            is_active=True,
        )
        CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Inactive",
            slug="inactive_f",
            field_type="text",
            is_active=False,
        )
        CustomFieldDefinition.invalidate_cache(product_ct)
        defs = CustomFieldDefinition.get_cached_for_content_type(product_ct)
        slugs = [d.slug for d in defs]
        assert "active_f" in slugs
        assert "inactive_f" not in slugs

    def test_get_cached_for_model(self, text_field_def):
        """get_cached_for_model resolves content type from model class."""
        from catalog.models import Product

        defs = CustomFieldDefinition.get_cached_for_model(Product)
        slugs = [d.slug for d in defs]
        assert "material" in slugs

    def test_cache_key_format(self, product_ct):
        """Cache key follows expected format."""
        expected_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        assert cache.get(expected_key) is not None

    def test_cached_result_is_reused(self, text_field_def, product_ct):
        """Second call returns cached data from the cache layer."""
        result1 = CustomFieldDefinition.get_cached_for_content_type(product_ct)
        # Verify cache key now holds data
        cache_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        cached_data = cache.get(cache_key)
        assert cached_data is not None
        assert len(cached_data) == len(result1)
        # Second call returns same data from cache
        result2 = CustomFieldDefinition.get_cached_for_content_type(product_ct)
        assert [d.pk for d in result1] == [d.pk for d in result2]


# ============================================================
# Model Tests: Soft Delete Lifecycle
# ============================================================


class TestSoftDeleteLifecycle:
    def test_soft_delete_group(self, group, staff_user):
        """Soft deleting a group sets is_deleted, deleted_at, deleted_by."""
        group.delete(user=staff_user)
        group_from_db = CustomFieldGroup.all_objects.get(pk=group.pk)
        assert group_from_db.is_deleted is True
        assert group_from_db.deleted_at is not None
        assert group_from_db.deleted_by == staff_user

    def test_soft_deleted_group_hidden_from_default_manager(self, group, staff_user):
        """Soft-deleted groups are hidden from default manager queries."""
        pk = group.pk
        group.delete(user=staff_user)
        assert not CustomFieldGroup.objects.filter(pk=pk).exists()
        # But accessible via all_objects
        assert CustomFieldGroup.all_objects.filter(pk=pk).exists()

    def test_soft_delete_field(self, text_field_def, staff_user):
        """Soft deleting a field sets is_deleted, deleted_at, deleted_by."""
        text_field_def.delete(user=staff_user)
        field_from_db = CustomFieldDefinition.all_objects.get(pk=text_field_def.pk)
        assert field_from_db.is_deleted is True
        assert field_from_db.deleted_at is not None
        assert field_from_db.deleted_by == staff_user

    def test_restore_group(self, group, staff_user):
        """Restoring a group clears is_deleted, deleted_at, deleted_by."""
        group.delete(user=staff_user)
        group_deleted = CustomFieldGroup.all_objects.get(pk=group.pk)
        group_deleted.restore()
        group_restored = CustomFieldGroup.objects.get(pk=group.pk)
        assert group_restored.is_deleted is False
        assert group_restored.deleted_at is None
        assert group_restored.deleted_by is None

    def test_restore_field(self, text_field_def, staff_user):
        """Restoring a field clears is_deleted, deleted_at, deleted_by."""
        text_field_def.delete(user=staff_user)
        field_deleted = CustomFieldDefinition.all_objects.get(pk=text_field_def.pk)
        field_deleted.restore()
        field_restored = CustomFieldDefinition.objects.get(pk=text_field_def.pk)
        assert field_restored.is_deleted is False
        assert field_restored.deleted_at is None
        assert field_restored.deleted_by is None

    def test_hard_delete_group(self, group):
        """Hard deleting a group removes it from the database entirely."""
        pk = group.pk
        group.hard_delete()
        assert not CustomFieldGroup.all_objects.filter(pk=pk).exists()

    def test_hard_delete_field(self, text_field_def):
        """Hard deleting a field removes it from the database entirely."""
        pk = text_field_def.pk
        text_field_def.hard_delete()
        assert not CustomFieldDefinition.all_objects.filter(pk=pk).exists()

    def test_soft_delete_without_user(self, group):
        """Soft delete without user still sets is_deleted but deleted_by is None."""
        group.delete()
        group_from_db = CustomFieldGroup.all_objects.get(pk=group.pk)
        assert group_from_db.is_deleted is True
        assert group_from_db.deleted_at is not None
        assert group_from_db.deleted_by is None


# ============================================================
# Model Tests: Utility functions
# ============================================================


class TestUtilityFunctions:
    def test_get_supported_content_types(self):
        """get_supported_content_types returns IDs for all 4 supported models."""
        ct_ids = get_supported_content_types()
        assert len(ct_ids) == 4
        # Verify all IDs are integers
        for ct_id in ct_ids:
            assert isinstance(ct_id, int)

    def test_supported_models_list(self):
        """SUPPORTED_MODELS has exactly 4 entries."""
        assert len(SUPPORTED_MODELS) == 4
        assert "catalog.product" in SUPPORTED_MODELS
        assert "catalog.category" in SUPPORTED_MODELS
        assert "orders.order" in SUPPORTED_MODELS
        assert "accounts.customerprofile" in SUPPORTED_MODELS


# ============================================================
# View Tests: Management Page
# ============================================================


class TestManagementView:
    def test_management_page_loads_for_staff(self, staff_client):
        """Management page returns 200 for staff users."""
        resp = staff_client.get("/en/admin/custom-fields/")
        assert resp.status_code == 200

    def test_management_page_has_model_tabs(self, staff_client):
        """Management page context includes model_tabs."""
        resp = staff_client.get("/en/admin/custom-fields/")
        assert "model_tabs" in resp.context
        tab_ids = [t["id"] for t in resp.context["model_tabs"]]
        assert "catalog_product" in tab_ids

    def test_management_page_has_field_type_choices(self, staff_client):
        """Management page context includes field_type_choices."""
        resp = staff_client.get("/en/admin/custom-fields/")
        assert "field_type_choices" in resp.context
        types = [ft[0] for ft in resp.context["field_type_choices"]]
        assert "text" in types
        assert "select" in types
        assert "color" in types

    def test_management_page_shows_deleted_count(self, staff_client, group, staff_user):
        """Management page shows count of deleted items for recycle bin badge."""
        group.delete(user=staff_user)
        resp = staff_client.get("/en/admin/custom-fields/")
        assert resp.context["deleted_count"] >= 1

    def test_management_page_shows_groups_and_field_counts(
        self, staff_client, group, text_field_def, select_field_def, product_ct
    ):
        """Management page shows groups with field counts per model tab."""
        resp = staff_client.get("/en/admin/custom-fields/")
        product_tab = next(t for t in resp.context["model_tabs"] if t["id"] == "catalog_product")
        assert product_tab["field_count"] >= 2
        assert product_tab["content_type_id"] == product_ct.pk

    def test_management_page_blocked_for_non_staff(self, regular_client):
        """Management page redirects non-staff users to login."""
        resp = regular_client.get("/en/admin/custom-fields/")
        assert resp.status_code == 302
        assert "login" in resp.url.lower() or "/admin/" in resp.url

    def test_management_page_blocked_for_anonymous(self, anon_client):
        """Management page redirects anonymous users."""
        resp = anon_client.get("/en/admin/custom-fields/")
        assert resp.status_code == 302


# ============================================================
# View Tests: Group CRUD (AJAX)
# ============================================================


class TestCreateGroupView:
    def test_create_group_success(self, staff_client, product_ct):
        """Group can be created via AJAX POST."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/groups/create/",
            {
                "name": "Shipping Details",
                "content_type_id": product_ct.pk,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["group"]["name"] == "Shipping Details"
        assert data["group"]["slug"] == "shipping-details"
        assert CustomFieldGroup.objects.filter(name="Shipping Details").exists()

    def test_create_group_with_storefront_flag(self, staff_client, product_ct):
        """Group can be created with show_on_storefront=True."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/groups/create/",
            {
                "name": "Public Info",
                "content_type_id": product_ct.pk,
                "show_on_storefront": True,
            },
        )
        data = resp.json()
        assert data["success"] is True
        assert data["group"]["show_on_storefront"] is True

    def test_create_group_requires_ajax_header(self, staff_client, product_ct):
        """Creating a group without X-Requested-With header returns 400."""
        resp = staff_client.post(
            "/en/admin/custom-fields/groups/create/",
            data=json.dumps({"name": "Test", "content_type_id": product_ct.pk}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_create_group_requires_post(self, staff_client, product_ct):
        """GET request to create_group endpoint is rejected."""
        resp = _ajax_get(staff_client, "/en/admin/custom-fields/groups/create/")
        assert resp.status_code == 405

    def test_create_group_requires_staff(self, regular_client, product_ct):
        """Non-staff user is redirected from create_group."""
        resp = _ajax_post(
            regular_client,
            "/en/admin/custom-fields/groups/create/",
            {
                "name": "No Access",
                "content_type_id": product_ct.pk,
            },
        )
        assert resp.status_code == 302

    def test_create_group_invalid_content_type(self, staff_client):
        """Creating a group with invalid content_type_id returns error."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/groups/create/",
            {
                "name": "Bad CT",
                "content_type_id": 99999,
            },
        )
        assert resp.status_code == 400
        assert resp.json()["success"] is False


class TestUpdateGroupView:
    def test_update_group_name(self, staff_client, group):
        """Group name can be updated via AJAX POST."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/update/",
            {"name": "Updated Name"},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        group.refresh_from_db()
        assert group.name == "Updated Name"

    def test_update_group_sort_order(self, staff_client, group):
        """Group sort_order can be updated."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/update/",
            {"sort_order": 5},
        )
        assert resp.json()["success"] is True
        group.refresh_from_db()
        assert group.sort_order == 5

    def test_update_group_show_on_storefront(self, staff_client, group):
        """Group show_on_storefront can be toggled."""
        original = group.show_on_storefront
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/update/",
            {"show_on_storefront": not original},
        )
        assert resp.json()["success"] is True
        group.refresh_from_db()
        assert group.show_on_storefront is (not original)

    def test_update_group_is_active(self, staff_client, group):
        """Group is_active can be toggled (deactivation, not deletion)."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/update/",
            {"is_active": False},
        )
        assert resp.json()["success"] is True
        group.refresh_from_db()
        assert group.is_active is False

    def test_update_nonexistent_group(self, staff_client):
        """Updating a nonexistent group returns 404."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/groups/99999/update/",
            {"name": "Ghost"},
        )
        assert resp.status_code == 404

    def test_update_group_requires_ajax_header(self, staff_client, group):
        """Update without X-Requested-With header returns 400."""
        resp = staff_client.post(
            f"/en/admin/custom-fields/groups/{group.pk}/update/",
            data=json.dumps({"name": "No Ajax"}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_update_group_requires_post(self, staff_client, group):
        """GET request to update_group is rejected."""
        resp = _ajax_get(staff_client, f"/en/admin/custom-fields/groups/{group.pk}/update/")
        assert resp.status_code == 405

    def test_update_group_partial(self, staff_client, group):
        """Only specified fields are updated; others remain unchanged."""
        original_storefront = group.show_on_storefront
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/update/",
            {"name": "Only Name Changed"},
        )
        assert resp.json()["success"] is True
        group.refresh_from_db()
        assert group.name == "Only Name Changed"
        assert group.show_on_storefront == original_storefront


class TestDeleteGroupView:
    def test_delete_group_soft_deletes(self, staff_client, group):
        """Deleting a group sets is_deleted=True via SoftDeleteModel."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/delete/",
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        group_from_db = CustomFieldGroup.all_objects.get(pk=group.pk)
        assert group_from_db.is_deleted is True

    def test_delete_group_cascades_to_fields(self, staff_client, group, text_field_def):
        """Deleting a group also soft-deletes its fields."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/delete/",
        )
        assert resp.json()["success"] is True
        field_from_db = CustomFieldDefinition.all_objects.get(pk=text_field_def.pk)
        assert field_from_db.is_deleted is True

    def test_delete_group_hidden_from_default_manager(self, staff_client, group):
        """Deleted group is no longer visible via default manager."""
        pk = group.pk
        _ajax_post(staff_client, f"/en/admin/custom-fields/groups/{pk}/delete/")
        assert not CustomFieldGroup.objects.filter(pk=pk).exists()

    def test_delete_nonexistent_group(self, staff_client):
        """Deleting a nonexistent group returns 404."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/groups/99999/delete/",
        )
        assert resp.status_code == 404

    def test_delete_group_requires_ajax_header(self, staff_client, group):
        """Delete without AJAX header returns 400."""
        resp = staff_client.post(
            f"/en/admin/custom-fields/groups/{group.pk}/delete/",
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_delete_group_requires_post(self, staff_client, group):
        """GET request to delete_group is rejected."""
        resp = _ajax_get(staff_client, f"/en/admin/custom-fields/groups/{group.pk}/delete/")
        assert resp.status_code == 405


# ============================================================
# View Tests: Field CRUD (AJAX)
# ============================================================


class TestCreateFieldView:
    def test_create_field_success(self, staff_client, group):
        """Field can be created via AJAX POST."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "Brand Name",
                "field_type": "text",
                "help_text": "Enter the brand name",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["field"]["name"] == "Brand Name"
        assert data["field"]["slug"] == "brand_name"
        assert data["field"]["field_type"] == "text"

    def test_create_field_auto_slug(self, staff_client, group):
        """Created field gets auto-generated slug with underscores."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "My Special Field",
                "field_type": "text",
            },
        )
        data = resp.json()
        assert data["field"]["slug"] == "my_special_field"

    def test_create_field_with_options(self, staff_client, group):
        """Field with all optional parameters can be created."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "Priority Level",
                "field_type": "select",
                "help_text": "Select priority",
                "is_required": True,
                "show_on_storefront": True,
                "is_translatable": False,
                "validation_config": {
                    "choices": [
                        {"value": "low", "label": "Low"},
                        {"value": "high", "label": "High"},
                    ]
                },
            },
        )
        data = resp.json()
        assert data["success"] is True
        assert data["field"]["is_required"] is True
        assert data["field"]["show_on_storefront"] is True

    def test_create_field_with_default_value(self, staff_client, group):
        """Field with a default_value can be created."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "Is Active Item",
                "field_type": "boolean",
                "default_value": True,
            },
        )
        assert resp.json()["success"] is True
        field = CustomFieldDefinition.objects.get(slug="is_active_item")
        assert field.default_value is True

    def test_create_field_empty_default_value_becomes_none(self, staff_client, group):
        """Empty string default_value is stored as None."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "Empty Default",
                "field_type": "text",
                "default_value": "",
            },
        )
        assert resp.json()["success"] is True
        field = CustomFieldDefinition.objects.get(slug="empty_default")
        assert field.default_value is None

    def test_create_field_legacy_text_validation(self, staff_client, group):
        """Legacy flat validation keys are built into validation_config for text."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "Legacy Text",
                "field_type": "text",
                "max_length": "500",
                "min_length": "10",
            },
        )
        assert resp.json()["success"] is True
        field = CustomFieldDefinition.objects.get(slug="legacy_text")
        assert field.validation_config["max_length"] == 500
        assert field.validation_config["min_length"] == 10

    def test_create_field_legacy_number_validation(self, staff_client, group):
        """Legacy flat validation keys are built into validation_config for number."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "Legacy Number",
                "field_type": "number",
                "min": 0,
                "max": 100,
            },
        )
        assert resp.json()["success"] is True
        field = CustomFieldDefinition.objects.get(slug="legacy_number")
        assert field.validation_config["min"] == 0.0
        assert field.validation_config["max"] == 100.0

    def test_create_field_legacy_select_choices(self, staff_client, group):
        """Legacy flat choices key is built into validation_config for select."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "Legacy Select",
                "field_type": "select",
                "choices": [{"value": "a", "label": "A"}, {"value": "b", "label": "B"}],
            },
        )
        assert resp.json()["success"] is True
        field = CustomFieldDefinition.objects.get(slug="legacy_select")
        assert len(field.validation_config["choices"]) == 2

    def test_create_field_content_type_from_group(self, staff_client, group):
        """Created field inherits content_type from its group."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "Inherited CT",
                "field_type": "text",
            },
        )
        assert resp.json()["success"] is True
        field = CustomFieldDefinition.objects.get(slug="inherited_ct")
        assert field.content_type_id == group.content_type_id

    def test_create_field_requires_ajax_header(self, staff_client, group):
        """Creating a field without AJAX header returns 400."""
        resp = staff_client.post(
            "/en/admin/custom-fields/fields/create/",
            data=json.dumps({"group_id": group.pk, "name": "No Ajax", "field_type": "text"}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_create_field_requires_post(self, staff_client):
        """GET request to create_field is rejected."""
        resp = _ajax_get(staff_client, "/en/admin/custom-fields/fields/create/")
        assert resp.status_code == 405

    def test_create_field_requires_staff(self, regular_client, group):
        """Non-staff user is redirected from create_field."""
        resp = _ajax_post(
            regular_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": group.pk,
                "name": "No Access",
                "field_type": "text",
            },
        )
        assert resp.status_code == 302

    def test_create_field_invalid_group(self, staff_client):
        """Creating a field with invalid group_id returns error."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/create/",
            {
                "group_id": 99999,
                "name": "Bad Group",
                "field_type": "text",
            },
        )
        assert resp.status_code == 400
        assert resp.json()["success"] is False


class TestUpdateFieldView:
    def test_update_field_name(self, staff_client, text_field_def):
        """Field name can be updated."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            {"name": "Updated Material"},
        )
        assert resp.json()["success"] is True
        text_field_def.refresh_from_db()
        assert text_field_def.name == "Updated Material"

    def test_update_field_help_text(self, staff_client, text_field_def):
        """Field help_text can be updated."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            {"help_text": "New help text"},
        )
        assert resp.json()["success"] is True
        text_field_def.refresh_from_db()
        assert text_field_def.help_text_value == "New help text"

    def test_update_field_multiple_attributes(self, staff_client, text_field_def):
        """Multiple field attributes can be updated at once."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            {
                "is_required": True,
                "show_on_storefront": False,
                "sort_order": 10,
                "is_translatable": True,
            },
        )
        assert resp.json()["success"] is True
        text_field_def.refresh_from_db()
        assert text_field_def.is_required is True
        assert text_field_def.show_on_storefront is False
        assert text_field_def.sort_order == 10
        assert text_field_def.is_translatable is True

    def test_update_field_validation_config(self, staff_client, text_field_def):
        """Field validation_config can be replaced."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            {"validation_config": {"max_length": 200}},
        )
        assert resp.json()["success"] is True
        text_field_def.refresh_from_db()
        assert text_field_def.validation_config == {"max_length": 200}

    def test_update_field_default_value(self, staff_client, text_field_def):
        """Field default_value can be updated."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            {"default_value": "Cotton"},
        )
        assert resp.json()["success"] is True
        text_field_def.refresh_from_db()
        assert text_field_def.default_value == "Cotton"

    def test_update_field_empty_default_value_becomes_none(self, staff_client, text_field_def):
        """Empty string default_value is stored as None."""
        text_field_def.default_value = "Old Value"
        text_field_def.save()
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            {"default_value": ""},
        )
        assert resp.json()["success"] is True
        text_field_def.refresh_from_db()
        assert text_field_def.default_value is None

    def test_update_field_is_active(self, staff_client, text_field_def):
        """Field is_active can be toggled."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            {"is_active": False},
        )
        assert resp.json()["success"] is True
        text_field_def.refresh_from_db()
        assert text_field_def.is_active is False

    def test_update_nonexistent_field(self, staff_client):
        """Updating a nonexistent field returns 404."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/99999/update/",
            {"name": "Ghost"},
        )
        assert resp.status_code == 404

    def test_update_field_requires_ajax_header(self, staff_client, text_field_def):
        """Update without AJAX header returns 400."""
        resp = staff_client.post(
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            data=json.dumps({"name": "No Ajax"}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_update_field_requires_post(self, staff_client, text_field_def):
        """GET request to update_field is rejected."""
        resp = _ajax_get(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
        )
        assert resp.status_code == 405


class TestDeleteFieldView:
    def test_delete_field_soft_deletes(self, staff_client, text_field_def):
        """Deleting a field sets is_deleted=True."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/delete/",
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        field_from_db = CustomFieldDefinition.all_objects.get(pk=text_field_def.pk)
        assert field_from_db.is_deleted is True

    def test_delete_field_hidden_from_default_manager(self, staff_client, text_field_def):
        """Deleted field is no longer visible via default manager."""
        pk = text_field_def.pk
        _ajax_post(staff_client, f"/en/admin/custom-fields/fields/{pk}/delete/")
        assert not CustomFieldDefinition.objects.filter(pk=pk).exists()

    def test_delete_nonexistent_field(self, staff_client):
        """Deleting a nonexistent field returns 404."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/99999/delete/",
        )
        assert resp.status_code == 404

    def test_delete_field_requires_ajax_header(self, staff_client, text_field_def):
        """Delete without AJAX header returns 400."""
        resp = staff_client.post(
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/delete/",
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_delete_field_requires_post(self, staff_client, text_field_def):
        """GET request to delete_field is rejected."""
        resp = _ajax_get(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/delete/",
        )
        assert resp.status_code == 405


# ============================================================
# View Tests: Get Field Detail (AJAX GET)
# ============================================================


class TestGetFieldDetailView:
    def test_get_field_detail(self, staff_client, text_field_def):
        """Field detail returns all field attributes."""
        resp = _ajax_get(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/",
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        field = data["field"]
        assert field["id"] == text_field_def.pk
        assert field["name"] == "Material"
        assert field["slug"] == "material"
        assert field["field_type"] == "text"
        assert field["help_text"] == "Product material"
        assert field["group_id"] == text_field_def.group_id

    def test_get_field_detail_includes_validation_config(self, staff_client, select_field_def):
        """Field detail includes validation_config with choices."""
        resp = _ajax_get(
            staff_client,
            f"/en/admin/custom-fields/fields/{select_field_def.pk}/",
        )
        data = resp.json()
        assert "validation_config" in data["field"]
        assert len(data["field"]["validation_config"]["choices"]) == 3

    def test_get_nonexistent_field_detail(self, staff_client):
        """Getting detail for nonexistent field returns 404."""
        resp = _ajax_get(staff_client, "/en/admin/custom-fields/fields/99999/")
        assert resp.status_code == 404

    def test_get_field_detail_requires_ajax_header(self, staff_client, text_field_def):
        """Field detail without AJAX header returns 400."""
        resp = staff_client.get(
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/",
        )
        assert resp.status_code == 400

    def test_get_field_detail_rejects_post(self, staff_client, text_field_def):
        """POST request to field_detail is rejected (GET only)."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/",
        )
        assert resp.status_code == 405


# ============================================================
# View Tests: Reorder Fields (AJAX)
# ============================================================


class TestReorderFieldsView:
    def test_reorder_fields(self, staff_client, text_field_def, select_field_def, product_ct):
        """Fields can be reordered via AJAX POST."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/reorder/",
            {
                "content_type_id": product_ct.pk,
                "fields": [
                    {"id": text_field_def.pk, "sort_order": 10},
                    {"id": select_field_def.pk, "sort_order": 5},
                ],
            },
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        text_field_def.refresh_from_db()
        select_field_def.refresh_from_db()
        assert text_field_def.sort_order == 10
        assert select_field_def.sort_order == 5

    def test_reorder_invalidates_cache(self, staff_client, text_field_def, product_ct):
        """Reordering fields invalidates the cache."""
        # Populate cache
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        cache_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(cache_key) is not None
        # Reorder
        _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/reorder/",
            {
                "content_type_id": product_ct.pk,
                "fields": [{"id": text_field_def.pk, "sort_order": 99}],
            },
        )
        # Cache should be invalidated
        assert cache.get(cache_key) is None

    def test_reorder_requires_ajax_header(self, staff_client):
        """Reorder without AJAX header returns 400."""
        resp = staff_client.post(
            "/en/admin/custom-fields/fields/reorder/",
            data=json.dumps({"fields": []}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_reorder_requires_post(self, staff_client):
        """GET request to reorder is rejected."""
        resp = _ajax_get(staff_client, "/en/admin/custom-fields/fields/reorder/")
        assert resp.status_code == 405


# ============================================================
# View Tests: Recycle Bin
# ============================================================


class TestRecycleBinView:
    def test_recycle_bin_loads_for_staff(self, staff_client):
        """Recycle bin page returns 200 for staff users."""
        resp = staff_client.get("/en/admin/custom-fields/recycle-bin/")
        assert resp.status_code == 200

    def test_recycle_bin_shows_deleted_groups(self, staff_client, group, staff_user):
        """Recycle bin lists soft-deleted groups."""
        group.delete(user=staff_user)
        resp = staff_client.get("/en/admin/custom-fields/recycle-bin/")
        assert resp.status_code == 200
        deleted_groups = list(resp.context["deleted_groups"])
        group_ids = [g.pk for g in deleted_groups]
        assert group.pk in group_ids

    def test_recycle_bin_shows_deleted_fields(self, staff_client, text_field_def, staff_user):
        """Recycle bin lists soft-deleted fields."""
        text_field_def.delete(user=staff_user)
        resp = staff_client.get("/en/admin/custom-fields/recycle-bin/")
        deleted_fields = list(resp.context["deleted_fields"])
        field_ids = [f.pk for f in deleted_fields]
        assert text_field_def.pk in field_ids

    def test_recycle_bin_blocked_for_non_staff(self, regular_client):
        """Recycle bin redirects non-staff users."""
        resp = regular_client.get("/en/admin/custom-fields/recycle-bin/")
        assert resp.status_code == 302

    def test_recycle_bin_blocked_for_anonymous(self, anon_client):
        """Recycle bin redirects anonymous users."""
        resp = anon_client.get("/en/admin/custom-fields/recycle-bin/")
        assert resp.status_code == 302

    def test_recycle_bin_empty_when_nothing_deleted(self, staff_client):
        """Recycle bin shows empty lists when nothing is deleted."""
        resp = staff_client.get("/en/admin/custom-fields/recycle-bin/")
        assert list(resp.context["deleted_groups"]) == []
        assert list(resp.context["deleted_fields"]) == []


# ============================================================
# View Tests: Restore from Recycle Bin
# ============================================================


class TestRestoreGroupView:
    def test_restore_group(self, staff_client, group, staff_user):
        """Restoring a group clears is_deleted and restores to active queries."""
        group.delete(user=staff_user)
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/restore/",
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        group_restored = CustomFieldGroup.objects.get(pk=group.pk)
        assert group_restored.is_deleted is False

    def test_restore_group_also_restores_fields(
        self, staff_client, group, text_field_def, staff_user
    ):
        """Restoring a group also restores its soft-deleted fields."""
        group.delete(user=staff_user)
        text_field_def.delete(user=staff_user)
        _ajax_post(staff_client, f"/en/admin/custom-fields/groups/{group.pk}/restore/")
        field_restored = CustomFieldDefinition.objects.get(pk=text_field_def.pk)
        assert field_restored.is_deleted is False

    def test_restore_group_invalidates_cache(self, staff_client, group, staff_user, product_ct):
        """Restoring a group invalidates the cache."""
        group.delete(user=staff_user)
        # Populate cache
        CustomFieldGroup.get_cached_for_content_type(product_ct)
        # Restore
        _ajax_post(staff_client, f"/en/admin/custom-fields/groups/{group.pk}/restore/")
        cache_key = f"{CACHE_KEY_PREFIX}:groups:{product_ct.pk}"
        assert cache.get(cache_key) is None

    def test_restore_nonexistent_group(self, staff_client):
        """Restoring a nonexistent group returns 404."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/groups/99999/restore/",
        )
        assert resp.status_code == 404

    def test_restore_non_deleted_group(self, staff_client, group):
        """Restoring a non-deleted group returns 404."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/restore/",
        )
        assert resp.status_code == 404

    def test_restore_group_requires_ajax_header(self, staff_client, group, staff_user):
        """Restore without AJAX header returns 400."""
        group.delete(user=staff_user)
        resp = staff_client.post(
            f"/en/admin/custom-fields/groups/{group.pk}/restore/",
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_restore_group_requires_post(self, staff_client, group, staff_user):
        """GET request to restore is rejected."""
        group.delete(user=staff_user)
        resp = _ajax_get(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/restore/",
        )
        assert resp.status_code == 405


class TestRestoreFieldView:
    def test_restore_field(self, staff_client, text_field_def, staff_user):
        """Restoring a field clears is_deleted."""
        text_field_def.delete(user=staff_user)
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/restore/",
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        field_restored = CustomFieldDefinition.objects.get(pk=text_field_def.pk)
        assert field_restored.is_deleted is False

    def test_restore_field_invalidates_cache(
        self, staff_client, text_field_def, staff_user, product_ct
    ):
        """Restoring a field invalidates the cache."""
        text_field_def.delete(user=staff_user)
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/restore/",
        )
        cache_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(cache_key) is None

    def test_restore_nonexistent_field(self, staff_client):
        """Restoring a nonexistent field returns 404."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/99999/restore/",
        )
        assert resp.status_code == 404

    def test_restore_non_deleted_field(self, staff_client, text_field_def):
        """Restoring a non-deleted field returns 404."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/restore/",
        )
        assert resp.status_code == 404


# ============================================================
# View Tests: Permanent Delete
# ============================================================


class TestPermanentDeleteGroupView:
    def test_permanent_delete_group(self, staff_client, group, staff_user):
        """Permanently deleting a group removes it from the database."""
        group.delete(user=staff_user)
        pk = group.pk
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{pk}/permanent-delete/",
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert not CustomFieldGroup.all_objects.filter(pk=pk).exists()

    def test_permanent_delete_group_also_deletes_fields(
        self, staff_client, group, text_field_def, staff_user
    ):
        """Permanently deleting a group also permanently deletes its fields."""
        group.delete(user=staff_user)
        field_pk = text_field_def.pk
        _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/permanent-delete/",
        )
        assert not CustomFieldDefinition.all_objects.filter(pk=field_pk).exists()

    def test_permanent_delete_invalidates_cache(self, staff_client, group, staff_user, product_ct):
        """Permanent delete invalidates the cache."""
        group.delete(user=staff_user)
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/permanent-delete/",
        )
        cache_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(cache_key) is None

    def test_permanent_delete_nonexistent_group(self, staff_client):
        """Permanently deleting nonexistent group returns 404."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/groups/99999/permanent-delete/",
        )
        assert resp.status_code == 404

    def test_permanent_delete_non_deleted_group(self, staff_client, group):
        """Cannot permanently delete a group that is not soft-deleted."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/permanent-delete/",
        )
        assert resp.status_code == 404

    def test_permanent_delete_requires_ajax_header(self, staff_client, group, staff_user):
        """Permanent delete without AJAX header returns 400."""
        group.delete(user=staff_user)
        resp = staff_client.post(
            f"/en/admin/custom-fields/groups/{group.pk}/permanent-delete/",
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_permanent_delete_requires_post(self, staff_client, group, staff_user):
        """GET request to permanent delete is rejected."""
        group.delete(user=staff_user)
        resp = _ajax_get(
            staff_client,
            f"/en/admin/custom-fields/groups/{group.pk}/permanent-delete/",
        )
        assert resp.status_code == 405


class TestPermanentDeleteFieldView:
    def test_permanent_delete_field(self, staff_client, text_field_def, staff_user):
        """Permanently deleting a field removes it from the database."""
        text_field_def.delete(user=staff_user)
        pk = text_field_def.pk
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{pk}/permanent-delete/",
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert not CustomFieldDefinition.all_objects.filter(pk=pk).exists()

    def test_permanent_delete_field_invalidates_cache(
        self, staff_client, text_field_def, staff_user, product_ct
    ):
        """Permanent field delete invalidates the cache."""
        text_field_def.delete(user=staff_user)
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/permanent-delete/",
        )
        cache_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(cache_key) is None

    def test_permanent_delete_nonexistent_field(self, staff_client):
        """Permanently deleting nonexistent field returns 404."""
        resp = _ajax_post(
            staff_client,
            "/en/admin/custom-fields/fields/99999/permanent-delete/",
        )
        assert resp.status_code == 404

    def test_permanent_delete_non_deleted_field(self, staff_client, text_field_def):
        """Cannot permanently delete a field that is not soft-deleted."""
        resp = _ajax_post(
            staff_client,
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/permanent-delete/",
        )
        assert resp.status_code == 404


# ============================================================
# Signal Tests: Cache Invalidation
# ============================================================


class TestCacheInvalidationSignals:
    def test_field_save_invalidates_cache(self, group, product_ct):
        """Saving a field definition triggers cache invalidation via signal."""
        # Populate cache
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        cache_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(cache_key) is not None
        # Create a new field (triggers post_save)
        CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Signal Test",
            slug="signal_test",
            field_type="text",
        )
        # Cache should be cleared by signal
        assert cache.get(cache_key) is None

    def test_field_update_invalidates_cache(self, text_field_def, product_ct):
        """Updating a field definition triggers cache invalidation."""
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        cache_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(cache_key) is not None
        text_field_def.name = "Updated Name"
        text_field_def.save()
        assert cache.get(cache_key) is None

    def test_field_hard_delete_invalidates_cache(self, text_field_def, product_ct):
        """Hard-deleting a field triggers post_delete signal for cache invalidation."""
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        cache_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(cache_key) is not None
        text_field_def.hard_delete()
        assert cache.get(cache_key) is None

    def test_group_save_invalidates_cache(self, product_ct):
        """Saving a group triggers cache invalidation via signal."""
        # Populate group cache
        CustomFieldGroup.get_cached_for_content_type(product_ct)
        cache_key = f"{CACHE_KEY_PREFIX}:groups:{product_ct.pk}"
        assert cache.get(cache_key) is not None
        # Create new group (triggers post_save)
        CustomFieldGroup.objects.create(
            name="Signal Group",
            slug="signal-group",
            content_type=product_ct,
        )
        assert cache.get(cache_key) is None

    def test_group_update_invalidates_cache(self, group, product_ct):
        """Updating a group triggers cache invalidation."""
        CustomFieldGroup.get_cached_for_content_type(product_ct)
        cache_key = f"{CACHE_KEY_PREFIX}:groups:{product_ct.pk}"
        assert cache.get(cache_key) is not None
        group.name = "Updated Group"
        group.save()
        assert cache.get(cache_key) is None

    def test_group_hard_delete_invalidates_cache(self, group, product_ct):
        """Hard-deleting a group triggers post_delete signal for cache invalidation."""
        CustomFieldGroup.get_cached_for_content_type(product_ct)
        cache_key = f"{CACHE_KEY_PREFIX}:groups:{product_ct.pk}"
        assert cache.get(cache_key) is not None
        group.hard_delete()
        assert cache.get(cache_key) is None

    def test_group_signal_invalidates_both_caches(self, group, product_ct):
        """Group signal invalidates both group and field caches."""
        CustomFieldGroup.get_cached_for_content_type(product_ct)
        CustomFieldDefinition.get_cached_for_content_type(product_ct)
        groups_key = f"{CACHE_KEY_PREFIX}:groups:{product_ct.pk}"
        fields_key = f"{CACHE_KEY_PREFIX}:fields:{product_ct.pk}"
        assert cache.get(groups_key) is not None
        assert cache.get(fields_key) is not None
        group.name = "Trigger Signal"
        group.save()
        assert cache.get(groups_key) is None
        assert cache.get(fields_key) is None


# ============================================================
# URL Resolution Tests
# ============================================================


class TestURLResolution:
    def test_management_url_resolves(self):
        """Management URL resolves to the correct view."""
        url = reverse("custom_fields:management")
        assert url == "/en/admin/custom-fields/"
        match = resolve("/en/admin/custom-fields/")
        assert match.url_name == "management"

    def test_recycle_bin_url_resolves(self):
        """Recycle bin URL resolves correctly."""
        url = reverse("custom_fields:recycle_bin")
        assert url == "/en/admin/custom-fields/recycle-bin/"
        match = resolve("/en/admin/custom-fields/recycle-bin/")
        assert match.url_name == "recycle_bin"

    def test_create_group_url_resolves(self):
        """Create group URL resolves correctly."""
        url = reverse("custom_fields:create_group")
        assert url == "/en/admin/custom-fields/groups/create/"

    def test_update_group_url_resolves(self):
        """Update group URL resolves correctly."""
        url = reverse("custom_fields:update_group", kwargs={"group_id": 1})
        assert url == "/en/admin/custom-fields/groups/1/update/"

    def test_delete_group_url_resolves(self):
        """Delete group URL resolves correctly."""
        url = reverse("custom_fields:delete_group", kwargs={"group_id": 1})
        assert url == "/en/admin/custom-fields/groups/1/delete/"

    def test_restore_group_url_resolves(self):
        """Restore group URL resolves correctly."""
        url = reverse("custom_fields:restore_group", kwargs={"group_id": 1})
        assert url == "/en/admin/custom-fields/groups/1/restore/"

    def test_permanent_delete_group_url_resolves(self):
        """Permanent delete group URL resolves correctly."""
        url = reverse("custom_fields:permanent_delete_group", kwargs={"group_id": 1})
        assert url == "/en/admin/custom-fields/groups/1/permanent-delete/"

    def test_create_field_url_resolves(self):
        """Create field URL resolves correctly."""
        url = reverse("custom_fields:create_field")
        assert url == "/en/admin/custom-fields/fields/create/"

    def test_field_detail_url_resolves(self):
        """Field detail URL resolves correctly."""
        url = reverse("custom_fields:field_detail", kwargs={"field_id": 1})
        assert url == "/en/admin/custom-fields/fields/1/"

    def test_update_field_url_resolves(self):
        """Update field URL resolves correctly."""
        url = reverse("custom_fields:update_field", kwargs={"field_id": 1})
        assert url == "/en/admin/custom-fields/fields/1/update/"

    def test_delete_field_url_resolves(self):
        """Delete field URL resolves correctly."""
        url = reverse("custom_fields:delete_field", kwargs={"field_id": 1})
        assert url == "/en/admin/custom-fields/fields/1/delete/"

    def test_restore_field_url_resolves(self):
        """Restore field URL resolves correctly."""
        url = reverse("custom_fields:restore_field", kwargs={"field_id": 1})
        assert url == "/en/admin/custom-fields/fields/1/restore/"

    def test_permanent_delete_field_url_resolves(self):
        """Permanent delete field URL resolves correctly."""
        url = reverse("custom_fields:permanent_delete_field", kwargs={"field_id": 1})
        assert url == "/en/admin/custom-fields/fields/1/permanent-delete/"

    def test_reorder_fields_url_resolves(self):
        """Reorder fields URL resolves correctly."""
        url = reverse("custom_fields:reorder_fields")
        assert url == "/en/admin/custom-fields/fields/reorder/"

    def test_all_url_names_in_namespace(self):
        """All expected URL names exist in the custom_fields namespace."""
        expected_names = [
            "management",
            "recycle_bin",
            "create_group",
            "update_group",
            "delete_group",
            "restore_group",
            "permanent_delete_group",
            "create_field",
            "field_detail",
            "update_field",
            "delete_field",
            "restore_field",
            "permanent_delete_field",
            "reorder_fields",
        ]
        for name in expected_names:
            try:
                # Some URLs require kwargs, just verify they don't raise NoReverseMatch
                if "group" in name and name != "create_group":
                    reverse(f"custom_fields:{name}", kwargs={"group_id": 1})
                elif "field" in name and name not in ("create_field", "reorder_fields"):
                    reverse(f"custom_fields:{name}", kwargs={"field_id": 1})
                else:
                    reverse(f"custom_fields:{name}")
            except Exception as e:
                pytest.fail(f"URL name 'custom_fields:{name}' failed to resolve: {e}")


# ============================================================
# Security Tests: Permission enforcement across all mutating endpoints
# ============================================================


class TestSecurityEnforcement:
    @pytest.fixture
    def endpoints_post(self, group, text_field_def, staff_user, product_ct):
        """All POST-requiring endpoints with test data."""
        group.delete(user=staff_user)
        text_field_def.delete(user=staff_user)
        return [
            (
                "/en/admin/custom-fields/groups/create/",
                {"name": "T", "content_type_id": product_ct.pk},
            ),
            (f"/en/admin/custom-fields/groups/{group.pk}/update/", {"name": "U"}),
            (f"/en/admin/custom-fields/groups/{group.pk}/restore/", {}),
            (f"/en/admin/custom-fields/groups/{group.pk}/permanent-delete/", {}),
            (f"/en/admin/custom-fields/fields/{text_field_def.pk}/restore/", {}),
            (f"/en/admin/custom-fields/fields/{text_field_def.pk}/permanent-delete/", {}),
            ("/en/admin/custom-fields/fields/reorder/", {"fields": []}),
        ]

    def test_anonymous_user_blocked_from_all_ajax_endpoints(
        self, anon_client, group, text_field_def, staff_user, product_ct
    ):
        """Anonymous users are redirected from all AJAX endpoints."""
        group.delete(user=staff_user)
        text_field_def.delete(user=staff_user)

        endpoints = [
            "/en/admin/custom-fields/groups/create/",
            f"/en/admin/custom-fields/groups/{group.pk}/update/",
            f"/en/admin/custom-fields/groups/{group.pk}/delete/",
            f"/en/admin/custom-fields/groups/{group.pk}/restore/",
            f"/en/admin/custom-fields/groups/{group.pk}/permanent-delete/",
            "/en/admin/custom-fields/fields/create/",
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/delete/",
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/restore/",
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/permanent-delete/",
            "/en/admin/custom-fields/fields/reorder/",
        ]
        for url in endpoints:
            resp = _ajax_post(anon_client, url, {})
            assert resp.status_code == 302, f"Anonymous user not redirected for {url}"

    def test_non_staff_blocked_from_all_ajax_endpoints(
        self, regular_client, group, text_field_def, staff_user, product_ct
    ):
        """Non-staff users are redirected from all AJAX endpoints."""
        group.delete(user=staff_user)
        text_field_def.delete(user=staff_user)

        endpoints = [
            "/en/admin/custom-fields/groups/create/",
            f"/en/admin/custom-fields/groups/{group.pk}/update/",
            f"/en/admin/custom-fields/groups/{group.pk}/delete/",
            f"/en/admin/custom-fields/groups/{group.pk}/restore/",
            f"/en/admin/custom-fields/groups/{group.pk}/permanent-delete/",
            "/en/admin/custom-fields/fields/create/",
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/",
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/delete/",
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/restore/",
            f"/en/admin/custom-fields/fields/{text_field_def.pk}/permanent-delete/",
            "/en/admin/custom-fields/fields/reorder/",
        ]
        for url in endpoints:
            resp = _ajax_post(regular_client, url, {})
            assert resp.status_code == 302, f"Non-staff not redirected for {url}"

    def test_ajax_header_required_for_all_mutating_endpoints(
        self, staff_client, group, text_field_def, staff_user, product_ct
    ):
        """All mutating AJAX endpoints reject requests without X-Requested-With."""
        # Prepare soft-deleted items for restore/permanent-delete endpoints
        deleted_group = CustomFieldGroup.objects.create(
            name="Deletable",
            slug="deletable-for-test",
            content_type=product_ct,
        )
        deleted_group.delete(user=staff_user)
        deleted_field = CustomFieldDefinition.objects.create(
            group=group,
            content_type=product_ct,
            name="Deletable Field",
            slug="deletable_field_test",
            field_type="text",
        )
        deleted_field.delete(user=staff_user)

        endpoints = [
            (
                "/en/admin/custom-fields/groups/create/",
                {"name": "T", "content_type_id": product_ct.pk},
            ),
            (f"/en/admin/custom-fields/groups/{group.pk}/update/", {"name": "U"}),
            (f"/en/admin/custom-fields/groups/{group.pk}/delete/", {}),
            (f"/en/admin/custom-fields/groups/{deleted_group.pk}/restore/", {}),
            (f"/en/admin/custom-fields/groups/{deleted_group.pk}/permanent-delete/", {}),
            (
                "/en/admin/custom-fields/fields/create/",
                {"group_id": group.pk, "name": "T", "field_type": "text"},
            ),
            (f"/en/admin/custom-fields/fields/{text_field_def.pk}/update/", {"name": "U"}),
            (f"/en/admin/custom-fields/fields/{text_field_def.pk}/delete/", {}),
            (f"/en/admin/custom-fields/fields/{deleted_field.pk}/restore/", {}),
            (f"/en/admin/custom-fields/fields/{deleted_field.pk}/permanent-delete/", {}),
            ("/en/admin/custom-fields/fields/reorder/", {"fields": []}),
        ]
        for url, data in endpoints:
            resp = staff_client.post(
                url,
                data=json.dumps(data),
                content_type="application/json",
                # Intentionally NOT sending HTTP_X_REQUESTED_WITH
            )
            assert resp.status_code == 400, (
                f"Expected 400 for {url} without AJAX header, got {resp.status_code}"
            )


# ============================================================
# Factory Tests
# ============================================================


class TestFactories:
    def test_custom_field_group_factory(self, product_ct):
        """CustomFieldGroupFactory creates valid groups."""
        group = CustomFieldGroupFactory()
        assert group.pk is not None
        assert group.is_active is True
        assert group.content_type is not None

    def test_custom_field_definition_factory(self, product_ct):
        """CustomFieldDefinitionFactory creates valid definitions."""
        field_def = CustomFieldDefinitionFactory()
        assert field_def.pk is not None
        assert field_def.field_type == "text"
        assert field_def.is_active is True
        assert field_def.content_type == field_def.group.content_type

    def test_factory_select_trait(self, product_ct):
        """CustomFieldDefinitionFactory select trait creates select with choices."""
        field_def = CustomFieldDefinitionFactory(select=True)
        assert field_def.field_type == "select"
        choices = field_def.get_choices()
        assert len(choices) == 3

    def test_factory_required_trait(self, product_ct):
        """CustomFieldDefinitionFactory required trait sets is_required=True."""
        field_def = CustomFieldDefinitionFactory(required=True)
        assert field_def.is_required is True

    def test_factory_storefront_trait(self, product_ct):
        """CustomFieldDefinitionFactory storefront trait sets show_on_storefront=True."""
        field_def = CustomFieldDefinitionFactory(storefront=True)
        assert field_def.show_on_storefront is True

    def test_factory_boolean_trait(self, product_ct):
        """CustomFieldDefinitionFactory boolean trait sets field_type and default_value."""
        field_def = CustomFieldDefinitionFactory(boolean=True)
        assert field_def.field_type == "boolean"
        assert field_def.default_value is False

    def test_factory_number_trait(self, product_ct):
        """CustomFieldDefinitionFactory number trait sets field_type."""
        field_def = CustomFieldDefinitionFactory(number=True)
        assert field_def.field_type == "number"

    def test_factory_decimal_trait(self, product_ct):
        """CustomFieldDefinitionFactory decimal trait sets field_type."""
        field_def = CustomFieldDefinitionFactory(decimal=True)
        assert field_def.field_type == "decimal"
