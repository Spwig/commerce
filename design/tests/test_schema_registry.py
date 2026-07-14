"""
Unit tests for Page Schema Registry and related models.

Tests cover:
- PageTier model and tier helpers
- ComponentStore model and approval workflow
- TierComponentPermission model and region validation
- PageSchemaRegistry and schema validation logic
"""

import io
import zipfile

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError

from design.models import ComponentStore, PageTier, TierComponentPermission
from design.schema_registry import (
    get_schema_registry,
)

User = get_user_model()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def create_dummy_package_file(component_type="test_component"):
    """Create a dummy ZIP package file for ComponentStore testing.

    Args:
        component_type: Component identifier for package naming

    Returns:
        SimpleUploadedFile: A minimal valid ZIP file for testing
    """
    # Create in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add minimal manifest
        manifest = f'{{"component_type": "{component_type}", "version": "1.0.0"}}'
        zip_file.writestr("manifest.json", manifest)
        # Add dummy template
        zip_file.writestr("template.html", "<div>Test Component</div>")

    zip_buffer.seek(0)
    return SimpleUploadedFile(
        f"{component_type}.zip", zip_buffer.read(), content_type="application/zip"
    )


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def test_user(db):
    """Create a test user for component reviews."""
    return User.objects.create_user(
        username="testreviewer", email="reviewer@test.com", password="testpass123"
    )


@pytest.fixture
def tier_a_checkout(db):
    """Create Tier A (checkout) page configuration."""
    return PageTier.objects.create(
        page_type="test_checkout",
        tier="A",
        display_name="Test Checkout",
        description="Test checkout page",
        schema={
            "regions": {
                "header": {"label": "Header", "locked": True},
                "main": {"label": "Main", "locked": True},
            }
        },
        csp_policy={"script-src": ["'self'"]},
        max_external_scripts=0,
        allows_custom_html=False,
        locked_regions=["header", "main"],
    )


@pytest.fixture
def tier_b_product(db):
    """Create Tier B (product) page configuration."""
    return PageTier.objects.create(
        page_type="test_product",
        tier="B",
        display_name="Test Product Page",
        description="Test product detail page",
        schema={
            "regions": {
                "hero": {"label": "Hero", "locked": False},
                "main": {"label": "Main", "locked": True},
                "sidebar": {"label": "Sidebar", "locked": False},
            }
        },
        csp_policy={"script-src": ["'self'", "'unsafe-inline'"]},
        max_external_scripts=3,
        allows_custom_html=False,
        locked_regions=["main"],
    )


@pytest.fixture
def tier_c_home(db):
    """Create Tier C (home) page configuration."""
    return PageTier.objects.create(
        page_type="test_home",
        tier="C",
        display_name="Test Homepage",
        description="Test homepage",
        schema={
            "regions": {
                "hero": {"label": "Hero", "locked": False},
                "content": {"label": "Content", "locked": False},
            }
        },
        csp_policy={"script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"]},
        max_external_scripts=-1,
        allows_custom_html=True,
        locked_regions=[],
    )


@pytest.fixture
def approved_component(db):
    """Create an approved component."""
    return ComponentStore.objects.create(
        component_type="test_banner",
        display_name="Test Banner",
        version="1.0.0",
        author="Test Author",
        description="A test banner component",
        capabilities=["text_editing", "image_upload"],
        allowed_tiers=["B", "C"],
        render_mode="ssr",
        external_domains=[],
        script_budget_kb=10.5,
        requires_sandbox=False,
        package_file=create_dummy_package_file("test_banner"),
        review_status="approved",
    )


@pytest.fixture
def pending_component(db):
    """Create a pending (not approved) component."""
    return ComponentStore.objects.create(
        component_type="test_pending",
        display_name="Pending Component",
        version="1.0.0",
        author="Test Author",
        capabilities=["text_editing"],
        allowed_tiers=["C"],
        render_mode="csr",
        package_file=create_dummy_package_file("test_pending"),
        review_status="pending",
    )


@pytest.fixture
def tier_permission(db, tier_b_product, approved_component):
    """Create a tier permission linking component to page tier."""
    return TierComponentPermission.objects.create(
        tier=tier_b_product,
        component=approved_component,
        allowed_regions=["hero", "sidebar"],
        max_instances=2,
    )


@pytest.fixture
def schema_registry():
    """Get schema registry instance and clear cache before each test."""
    registry = get_schema_registry()
    registry.clear_cache()
    return registry


# ============================================================================
# PAGE TIER MODEL TESTS
# ============================================================================


@pytest.mark.django_db
class TestPageTierModel:
    """Test PageTier model functionality."""

    def test_create_page_tier(self, tier_a_checkout):
        """Test creating a page tier."""
        assert tier_a_checkout.page_type == "test_checkout"
        assert tier_a_checkout.tier == "A"
        assert tier_a_checkout.max_external_scripts == 0
        assert tier_a_checkout.allows_custom_html is False

    def test_page_type_unique(self, db, tier_a_checkout):
        """Test that page_type must be unique."""
        with pytest.raises(IntegrityError):
            PageTier.objects.create(
                page_type="test_checkout",  # Duplicate
                tier="B",
                display_name="Duplicate",
            )

    def test_is_tier_a(self, tier_a_checkout):
        """Test is_tier_a() helper method."""
        assert tier_a_checkout.is_tier_a() is True
        assert tier_a_checkout.is_tier_b() is False
        assert tier_a_checkout.is_tier_c() is False

    def test_is_tier_b(self, tier_b_product):
        """Test is_tier_b() helper method."""
        assert tier_b_product.is_tier_a() is False
        assert tier_b_product.is_tier_b() is True
        assert tier_b_product.is_tier_c() is False

    def test_is_tier_c(self, tier_c_home):
        """Test is_tier_c() helper method."""
        assert tier_c_home.is_tier_a() is False
        assert tier_c_home.is_tier_b() is False
        assert tier_c_home.is_tier_c() is True

    def test_get_security_level(self, tier_a_checkout, tier_b_product, tier_c_home):
        """Test get_security_level() method."""
        assert tier_a_checkout.get_security_level() == "System-Critical (Checkout)"
        assert tier_b_product.get_security_level() == "Semi-Critical (Product/Collection)"
        assert tier_c_home.get_security_level() == "Marketing (Full Flexibility)"

    def test_locked_regions_json(self, tier_a_checkout):
        """Test that locked_regions is stored as JSON."""
        assert isinstance(tier_a_checkout.locked_regions, list)
        assert "header" in tier_a_checkout.locked_regions
        assert "main" in tier_a_checkout.locked_regions

    def test_schema_json(self, tier_b_product):
        """Test that schema is stored as JSON."""
        assert isinstance(tier_b_product.schema, dict)
        assert "regions" in tier_b_product.schema
        assert "hero" in tier_b_product.schema["regions"]


# ============================================================================
# COMPONENT STORE MODEL TESTS
# ============================================================================


@pytest.mark.django_db
class TestComponentStoreModel:
    """Test ComponentStore model functionality."""

    def test_create_component(self, approved_component):
        """Test creating a component."""
        assert approved_component.component_type == "test_banner"
        assert approved_component.version == "1.0.0"
        assert approved_component.review_status == "approved"

    def test_component_type_unique(self, db, approved_component):
        """Test that component_type must be unique."""
        with pytest.raises(IntegrityError):
            ComponentStore.objects.create(
                component_type="test_banner",  # Duplicate
                display_name="Duplicate",
                version="2.0.0",
                author="Test",
                render_mode="ssr",
                package_file=create_dummy_package_file("test_banner"),
            )

    def test_is_approved(self, approved_component, pending_component):
        """Test is_approved() method."""
        assert approved_component.is_approved() is True
        assert pending_component.is_approved() is False

    def test_can_use_in_tier(self, approved_component):
        """Test can_use_in_tier() method."""
        assert approved_component.can_use_in_tier("B") is True
        assert approved_component.can_use_in_tier("C") is True
        assert approved_component.can_use_in_tier("A") is False

    def test_has_capability(self, approved_component):
        """Test has_capability() method."""
        assert approved_component.has_capability("text_editing") is True
        assert approved_component.has_capability("image_upload") is True
        assert approved_component.has_capability("video_upload") is False

    def test_capabilities_json(self, approved_component):
        """Test that capabilities is stored as JSON list."""
        assert isinstance(approved_component.capabilities, list)
        assert "text_editing" in approved_component.capabilities

    def test_allowed_tiers_json(self, approved_component):
        """Test that allowed_tiers is stored as JSON list."""
        assert isinstance(approved_component.allowed_tiers, list)
        assert "B" in approved_component.allowed_tiers


# ============================================================================
# TIER COMPONENT PERMISSION MODEL TESTS
# ============================================================================


@pytest.mark.django_db
class TestTierComponentPermissionModel:
    """Test TierComponentPermission model functionality."""

    def test_create_permission(self, tier_permission):
        """Test creating a tier permission."""
        assert tier_permission.tier.page_type == "test_product"
        assert tier_permission.component.component_type == "test_banner"
        assert tier_permission.max_instances == 2

    def test_unique_together(self, db, tier_b_product, approved_component, tier_permission):
        """Test that tier+component combination must be unique."""
        with pytest.raises(IntegrityError):
            TierComponentPermission.objects.create(
                tier=tier_b_product, component=approved_component, allowed_regions=["main"]
            )

    def test_is_unlimited(self, tier_permission):
        """Test is_unlimited() method."""
        assert tier_permission.is_unlimited() is False

        tier_permission.max_instances = -1
        assert tier_permission.is_unlimited() is True

    def test_allows_region(self, tier_permission):
        """Test allows_region() method."""
        assert tier_permission.allows_region("hero") is True
        assert tier_permission.allows_region("sidebar") is True
        assert tier_permission.allows_region("main") is False

    def test_allows_region_empty_list(self, db, tier_b_product, approved_component):
        """Test that empty allowed_regions allows all regions."""
        perm = TierComponentPermission.objects.create(
            tier=tier_b_product,
            component=approved_component,
            allowed_regions=[],  # Empty = all regions
            max_instances=-1,
        )
        assert perm.allows_region("any_region") is True
        assert perm.allows_region("another_region") is True


# ============================================================================
# PAGE SCHEMA REGISTRY TESTS
# ============================================================================


@pytest.mark.django_db
class TestPageSchemaRegistry:
    """Test PageSchemaRegistry functionality."""

    def test_get_page_tier(self, schema_registry, tier_b_product):
        """Test retrieving page tier from registry."""
        tier = schema_registry.get_page_tier("test_product")
        assert tier is not None
        assert tier.tier == "B"
        assert tier.page_type == "test_product"

    def test_get_page_tier_not_found(self, schema_registry):
        """Test retrieving non-existent page tier."""
        tier = schema_registry.get_page_tier("nonexistent")
        assert tier is None

    def test_get_allowed_components(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test getting allowed components for a page."""
        components = schema_registry.get_allowed_components("test_product")
        assert len(components) == 1
        assert components[0].component_type == "test_banner"

    def test_get_allowed_components_excludes_pending(
        self, schema_registry, tier_b_product, pending_component
    ):
        """Test that pending components are excluded."""
        # Create permission for pending component
        TierComponentPermission.objects.create(
            tier=tier_b_product, component=pending_component, allowed_regions=["hero"]
        )

        components = schema_registry.get_allowed_components("test_product")
        # Should be empty because pending_component is not approved
        component_types = [c.component_type for c in components]
        assert "test_pending" not in component_types

    def test_get_allowed_regions(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test getting allowed regions for a component."""
        regions = schema_registry.get_allowed_regions("test_product", "test_banner")
        assert "hero" in regions
        assert "sidebar" in regions
        assert "main" not in regions

    def test_is_region_locked(self, schema_registry, tier_b_product):
        """Test checking if region is locked."""
        assert schema_registry.is_region_locked("test_product", "main") is True
        assert schema_registry.is_region_locked("test_product", "hero") is False
        assert schema_registry.is_region_locked("test_product", "sidebar") is False

    def test_validate_component_placement_success(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test successful component placement validation."""
        valid, error = schema_registry.validate_component_placement(
            page_type="test_product", component_type="test_banner", region="hero", instance_count=1
        )
        assert valid is True
        assert error is None

    def test_validate_component_placement_locked_region(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test placement in locked region fails."""
        valid, error = schema_registry.validate_component_placement(
            page_type="test_product",
            component_type="test_banner",
            region="main",  # Locked region
            instance_count=1,
        )
        assert valid is False
        assert "locked" in error.lower()

    def test_validate_component_placement_wrong_region(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test placement in disallowed region fails."""
        # tier_permission only allows 'hero' and 'sidebar', not 'main'
        # But 'main' is also locked, so it should fail with locked error first
        # Let's try a non-existent region instead
        valid, error = schema_registry.validate_component_placement(
            page_type="test_product",
            component_type="test_banner",
            region="footer",  # Not in allowed_regions
            instance_count=1,
        )
        assert valid is False
        assert "not allowed in region" in error

    def test_validate_component_placement_too_many_instances(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test exceeding max instances fails."""
        valid, error = schema_registry.validate_component_placement(
            page_type="test_product",
            component_type="test_banner",
            region="hero",
            instance_count=5,  # Max is 2
        )
        assert valid is False
        assert "exceeds max instances" in error

    def test_validate_component_placement_not_approved(
        self, schema_registry, tier_b_product, pending_component
    ):
        """Test that unapproved components fail validation."""
        # Create permission for pending component
        TierComponentPermission.objects.create(
            tier=tier_b_product, component=pending_component, allowed_regions=["hero"]
        )

        valid, error = schema_registry.validate_component_placement(
            page_type="test_product", component_type="test_pending", region="hero", instance_count=1
        )
        assert valid is False
        assert "not allowed" in error.lower()

    def test_validate_page_schema_success(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test successful full page schema validation."""
        layout_data = {
            "regions": {
                "hero": [{"component": "test_banner", "config": {}}],
                "sidebar": [{"component": "test_banner", "config": {}}],
            }
        }
        valid, errors = schema_registry.validate_page_schema("test_product", layout_data)
        assert valid is True
        assert len(errors) == 0

    def test_validate_page_schema_locked_region(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test that locked regions fail validation."""
        layout_data = {
            "regions": {
                "main": [  # Locked region
                    {"component": "test_banner", "config": {}}
                ]
            }
        }
        valid, errors = schema_registry.validate_page_schema("test_product", layout_data)
        assert valid is False
        assert any("locked" in err.lower() for err in errors)

    def test_validate_page_schema_missing_component_field(self, schema_registry, tier_b_product):
        """Test that missing component field fails validation."""
        layout_data = {
            "regions": {
                "hero": [
                    {"config": {}}  # Missing 'component' field
                ]
            }
        }
        valid, errors = schema_registry.validate_page_schema("test_product", layout_data)
        assert valid is False
        assert any("missing" in err.lower() for err in errors)

    def test_validate_page_schema_invalid_structure(self, schema_registry, tier_b_product):
        """Test that invalid schema structure fails validation."""
        # Missing 'regions' key
        layout_data = {"invalid": "structure"}
        valid, errors = schema_registry.validate_page_schema("test_product", layout_data)
        assert valid is False
        assert any("regions" in err.lower() for err in errors)

    def test_get_schema_for_page(
        self, schema_registry, tier_b_product, approved_component, tier_permission
    ):
        """Test getting full schema for a page."""
        schema = schema_registry.get_schema_for_page("test_product")
        assert schema["page_type"] == "test_product"
        assert schema["tier"] == "B"
        assert schema["display_name"] == "Test Product Page"
        assert "locked_regions" in schema
        assert "allowed_components" in schema
        assert len(schema["allowed_components"]) == 1

    def test_cache_clearing(self, schema_registry, tier_b_product):
        """Test cache clearing functionality."""
        # First call loads from DB
        tier1 = schema_registry.get_page_tier("test_product")
        assert tier1 is not None

        # Clear cache
        schema_registry.clear_cache("test_product")

        # Should still work (loads from DB again)
        tier2 = schema_registry.get_page_tier("test_product")
        assert tier2 is not None
        assert tier2.page_type == tier1.page_type

    def test_singleton_instance(self):
        """Test that get_schema_registry returns singleton instance."""
        registry1 = get_schema_registry()
        registry2 = get_schema_registry()
        assert registry1 is registry2


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


@pytest.mark.django_db
class TestSchemaRegistryIntegration:
    """Integration tests for complete workflows."""

    def test_tier_a_strict_enforcement(self, schema_registry, tier_a_checkout, approved_component):
        """Test that Tier A enforces strict security."""
        # Create permission for Tier A
        TierComponentPermission.objects.create(
            tier=tier_a_checkout, component=approved_component, allowed_regions=["header"]
        )

        # Tier A should have no external scripts
        assert tier_a_checkout.max_external_scripts == 0
        assert tier_a_checkout.allows_custom_html is False

        # All regions should be locked
        for region in tier_a_checkout.locked_regions:
            assert schema_registry.is_region_locked("test_checkout", region) is True

    def test_tier_c_flexible_enforcement(self, schema_registry, tier_c_home, approved_component):
        """Test that Tier C allows maximum flexibility."""
        # Create permission for Tier C
        TierComponentPermission.objects.create(
            tier=tier_c_home, component=approved_component, allowed_regions=["hero", "content"]
        )

        # Tier C should allow custom HTML and unlimited scripts
        assert tier_c_home.max_external_scripts == -1
        assert tier_c_home.allows_custom_html is True

        # No locked regions
        assert len(tier_c_home.locked_regions) == 0

    def test_component_review_workflow(self, db, test_user):
        """Test component approval workflow."""
        # Create pending component
        component = ComponentStore.objects.create(
            component_type="workflow_test",
            display_name="Workflow Test",
            version="1.0.0",
            author="Test",
            render_mode="ssr",
            package_file=create_dummy_package_file("workflow_test"),
            review_status="pending",
        )

        assert component.is_approved() is False

        # Approve component
        component.review_status = "approved"
        component.reviewed_by = test_user
        component.save()

        assert component.is_approved() is True
        assert component.reviewed_by == test_user
