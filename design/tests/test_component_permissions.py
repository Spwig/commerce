"""
Tests for component_permissions - Permission template system.

Tests cover:
- Permission template application
- Template validation
- Permission copying
- Permission removal
- Permission summaries
- All predefined templates (system, marketing, product, checkout, content, restricted)
"""

import pytest

from design.component_permissions import (
    apply_permission_template,
    copy_permissions,
    get_available_templates,
    remove_all_permissions,
    get_permission_summary,
    PERMISSION_TEMPLATES,
)
from design.models import ComponentStore, PageTier, TierComponentPermission


@pytest.fixture(autouse=True)
def cleanup_page_tiers(db):
    """Clean up PageTier objects before each test to avoid conflicts."""
    # Delete all PageTier objects before the test
    PageTier.objects.all().delete()
    yield
    # Clean up after test as well
    PageTier.objects.all().delete()


@pytest.fixture
def tier_a(db):
    """Create Tier A."""
    return PageTier.objects.create(
        page_type='permissions_test_checkout',
        tier='A',
        display_name='Test Checkout (Permissions)',
        description='Tier A for permissions testing',
        schema={'regions': {}}
    )


@pytest.fixture
def tier_b(db):
    """Create Tier B."""
    return PageTier.objects.create(
        page_type='permissions_test_product',
        tier='B',
        display_name='Test Product (Permissions)',
        description='Tier B for permissions testing',
        schema={'regions': {}}
    )


@pytest.fixture
def tier_c(db):
    """Create Tier C."""
    return PageTier.objects.create(
        page_type='permissions_test_home',
        tier='C',
        display_name='Test Home (Permissions)',
        description='Tier C for permissions testing',
        schema={'regions': {}}
    )


@pytest.fixture
def sample_component(db):
    """Create a sample component."""
    return ComponentStore.objects.create(
        component_type='test_banner',
        display_name='Test Banner',
        version='1.0.0',
        author='Test Author',
        description='Test component',
        review_status='approved',
        render_mode='server',
    )


@pytest.fixture
def component_with_permissions(sample_component, tier_a, tier_b, tier_c):
    """Create a component with existing permissions."""
    TierComponentPermission.objects.create(
        tier=tier_a,
        component=sample_component,
        allowed_regions=[],
        max_instances=-1
    )
    TierComponentPermission.objects.create(
        tier=tier_b,
        component=sample_component,
        allowed_regions=['header'],
        max_instances=2
    )
    return sample_component


@pytest.mark.django_db
class TestPermissionTemplates:
    """Test permission template constants."""

    def test_all_templates_defined(self):
        """Test that all expected templates are defined."""
        expected_templates = ['system', 'marketing', 'product', 'checkout', 'content', 'restricted']

        for template_name in expected_templates:
            assert template_name in PERMISSION_TEMPLATES

    def test_templates_have_required_fields(self):
        """Test that all templates have required fields."""
        required_fields = ['description', 'allowed_tiers', 'allowed_regions', 'max_instances']

        for template_name, template_config in PERMISSION_TEMPLATES.items():
            for field in required_fields:
                assert field in template_config, f"Template '{template_name}' missing field '{field}'"

    def test_system_template_allows_all_tiers(self):
        """Test that system template allows all tiers."""
        assert PERMISSION_TEMPLATES['system']['allowed_tiers'] == ['A', 'B', 'C']
        assert PERMISSION_TEMPLATES['system']['max_instances'] == -1

    def test_marketing_template_tier_c_only(self):
        """Test that marketing template is Tier C only."""
        assert PERMISSION_TEMPLATES['marketing']['allowed_tiers'] == ['C']
        assert PERMISSION_TEMPLATES['marketing']['max_instances'] == -1

    def test_product_template_tier_b_and_c(self):
        """Test that product template is Tier B and C."""
        assert PERMISSION_TEMPLATES['product']['allowed_tiers'] == ['B', 'C']

    def test_checkout_template_tier_a_only(self):
        """Test that checkout template is Tier A only."""
        assert PERMISSION_TEMPLATES['checkout']['allowed_tiers'] == ['A']
        assert PERMISSION_TEMPLATES['checkout']['max_instances'] == 1

    def test_restricted_template_tier_a_and_b(self):
        """Test that restricted template is Tier A and B only."""
        assert PERMISSION_TEMPLATES['restricted']['allowed_tiers'] == ['A', 'B']


@pytest.mark.django_db
class TestApplyPermissionTemplate:
    """Test apply_permission_template function."""

    def test_apply_system_template(self, sample_component, tier_a, tier_b, tier_c):
        """Test applying system template creates permissions for all tiers."""
        permissions = apply_permission_template(sample_component, 'system')

        assert len(permissions) == 3
        assert sample_component.tier_permissions.count() == 3

        # Check that all tiers are included
        tier_ids = [p.tier.tier for p in permissions]
        assert 'A' in tier_ids
        assert 'B' in tier_ids
        assert 'C' in tier_ids

    def test_apply_marketing_template(self, sample_component, tier_a, tier_b, tier_c):
        """Test applying marketing template creates permission for Tier C only."""
        permissions = apply_permission_template(sample_component, 'marketing')

        assert len(permissions) == 1
        assert permissions[0].tier.tier == 'C'
        assert permissions[0].max_instances == -1

    def test_apply_product_template(self, sample_component, tier_a, tier_b, tier_c):
        """Test applying product template creates permissions for Tier B and C."""
        permissions = apply_permission_template(sample_component, 'product')

        assert len(permissions) == 2
        tier_ids = [p.tier.tier for p in permissions]
        assert 'B' in tier_ids
        assert 'C' in tier_ids
        assert 'A' not in tier_ids

    def test_apply_checkout_template(self, sample_component, tier_a, tier_b, tier_c):
        """Test applying checkout template creates permission for Tier A only."""
        permissions = apply_permission_template(sample_component, 'checkout')

        assert len(permissions) == 1
        assert permissions[0].tier.tier == 'A'
        assert permissions[0].max_instances == 1  # Single instance

    def test_apply_content_template(self, sample_component, tier_a, tier_b, tier_c):
        """Test applying content template creates permissions for all tiers."""
        permissions = apply_permission_template(sample_component, 'content')

        assert len(permissions) == 3
        assert sample_component.tier_permissions.count() == 3

    def test_apply_restricted_template(self, sample_component, tier_a, tier_b, tier_c):
        """Test applying restricted template creates permissions for Tier A and B only."""
        permissions = apply_permission_template(sample_component, 'restricted')

        assert len(permissions) == 2
        tier_ids = [p.tier.tier for p in permissions]
        assert 'A' in tier_ids
        assert 'B' in tier_ids
        assert 'C' not in tier_ids

    def test_apply_template_with_override_max_instances(self, sample_component, tier_a, tier_b, tier_c):
        """Test applying template with override settings."""
        permissions = apply_permission_template(
            sample_component,
            'system',
            override_settings={'max_instances': 5}
        )

        # All permissions should have max_instances=5
        for perm in permissions:
            assert perm.max_instances == 5

    def test_apply_template_with_override_regions(self, sample_component, tier_a, tier_b, tier_c):
        """Test applying template with region override."""
        permissions = apply_permission_template(
            sample_component,
            'marketing',
            override_settings={'allowed_regions': ['header', 'footer']}
        )

        assert permissions[0].allowed_regions == ['header', 'footer']

    def test_apply_template_deletes_existing_permissions(self, component_with_permissions, tier_a, tier_b, tier_c):
        """Test that applying template deletes existing permissions."""
        # Component starts with 2 permissions
        assert component_with_permissions.tier_permissions.count() == 2

        # Apply new template
        apply_permission_template(component_with_permissions, 'checkout')

        # Should now have only 1 permission (Tier A)
        assert component_with_permissions.tier_permissions.count() == 1
        assert component_with_permissions.tier_permissions.first().tier.tier == 'A'

    def test_apply_invalid_template_raises_error(self, sample_component):
        """Test that applying invalid template raises ValueError."""
        with pytest.raises(ValueError, match='Invalid template'):
            apply_permission_template(sample_component, 'nonexistent_template')

    def test_apply_template_skips_nonexistent_tiers(self, sample_component, tier_a):
        """Test that template application skips tiers that don't exist in database."""
        # Only tier_a exists, but system template requires A, B, C
        permissions = apply_permission_template(sample_component, 'system')

        # Should only create permission for tier A (the only one that exists)
        assert len(permissions) == 1
        assert permissions[0].tier.tier == 'A'


@pytest.mark.django_db
class TestCopyPermissions:
    """Test copy_permissions function."""

    def test_copy_permissions_basic(self, component_with_permissions, db, tier_a, tier_b):
        """Test copying permissions from one component to another."""
        target_component = ComponentStore.objects.create(
            component_type='target_component',
            display_name='Target Component',
            version='1.0.0',
            author='Test',
            description='Target',
            review_status='approved',
        )

        # Source has 2 permissions
        assert component_with_permissions.tier_permissions.count() == 2

        # Copy permissions
        new_permissions = copy_permissions(component_with_permissions, target_component)

        # Target should now have 2 permissions
        assert len(new_permissions) == 2
        assert target_component.tier_permissions.count() == 2

    def test_copy_permissions_preserves_settings(self, component_with_permissions, db, tier_a, tier_b):
        """Test that copy_permissions preserves allowed_regions and max_instances."""
        target_component = ComponentStore.objects.create(
            component_type='target',
            display_name='Target',
            version='1.0.0',
            author='Test',
            description='Target',
            review_status='approved',
        )

        copy_permissions(component_with_permissions, target_component)

        # Find the permission with header region restriction
        target_perm = target_component.tier_permissions.get(tier__tier='B')

        # Should preserve settings from source
        assert target_perm.allowed_regions == ['header']
        assert target_perm.max_instances == 2

    def test_copy_permissions_deletes_existing_on_target(self, component_with_permissions, db, tier_a, tier_b, tier_c):
        """Test that copy_permissions deletes existing permissions on target."""
        target_component = ComponentStore.objects.create(
            component_type='target',
            display_name='Target',
            version='1.0.0',
            author='Test',
            description='Target',
            review_status='approved',
        )

        # Add existing permission to target
        TierComponentPermission.objects.create(
            tier=tier_c,
            component=target_component,
            allowed_regions=[],
            max_instances=-1
        )

        assert target_component.tier_permissions.count() == 1

        # Copy permissions (source has tier A and B)
        copy_permissions(component_with_permissions, target_component)

        # Target should now have 2 permissions (A and B), not 3
        assert target_component.tier_permissions.count() == 2
        tier_ids = [p.tier.tier for p in target_component.tier_permissions.all()]
        assert 'C' not in tier_ids

    def test_copy_permissions_from_component_with_no_permissions(self, sample_component, db):
        """Test copying from component with no permissions."""
        target_component = ComponentStore.objects.create(
            component_type='target',
            display_name='Target',
            version='1.0.0',
            author='Test',
            description='Target',
            review_status='approved',
        )

        new_permissions = copy_permissions(sample_component, target_component)

        assert len(new_permissions) == 0
        assert target_component.tier_permissions.count() == 0


@pytest.mark.django_db
class TestGetAvailableTemplates:
    """Test get_available_templates function."""

    def test_returns_all_templates(self):
        """Test that get_available_templates returns all templates."""
        templates = get_available_templates()

        assert 'system' in templates
        assert 'marketing' in templates
        assert 'product' in templates
        assert 'checkout' in templates
        assert 'content' in templates
        assert 'restricted' in templates

    def test_returns_descriptions(self):
        """Test that get_available_templates returns descriptions."""
        templates = get_available_templates()

        # Each template should have a description
        for template_name, description in templates.items():
            assert isinstance(description, str)
            assert len(description) > 0

    def test_template_count(self):
        """Test that get_available_templates returns expected number of templates."""
        templates = get_available_templates()

        assert len(templates) == 6  # system, marketing, product, checkout, content, restricted


@pytest.mark.django_db
class TestRemoveAllPermissions:
    """Test remove_all_permissions function."""

    def test_remove_all_permissions(self, component_with_permissions):
        """Test removing all permissions from a component."""
        # Component starts with 2 permissions
        assert component_with_permissions.tier_permissions.count() == 2

        deleted_count = remove_all_permissions(component_with_permissions)

        assert deleted_count == 2
        assert component_with_permissions.tier_permissions.count() == 0

    def test_remove_permissions_from_component_with_no_permissions(self, sample_component):
        """Test removing permissions from component that has none."""
        deleted_count = remove_all_permissions(sample_component)

        assert deleted_count == 0
        assert sample_component.tier_permissions.count() == 0

    def test_remove_all_permissions_returns_count(self, component_with_permissions):
        """Test that remove_all_permissions returns number of deleted permissions."""
        deleted_count = remove_all_permissions(component_with_permissions)

        assert isinstance(deleted_count, int)
        assert deleted_count >= 0


@pytest.mark.django_db
class TestGetPermissionSummary:
    """Test get_permission_summary function."""

    def test_summary_for_component_with_permissions(self, component_with_permissions):
        """Test getting permission summary for component with permissions."""
        summary = get_permission_summary(component_with_permissions)

        assert summary['tier_count'] == 2
        assert summary['allowed_tiers'] == ['A', 'B']
        assert summary['has_restrictions'] is True  # Has region and max_instances restrictions

    def test_summary_for_component_without_permissions(self, sample_component):
        """Test getting permission summary for component without permissions."""
        summary = get_permission_summary(sample_component)

        assert summary['tier_count'] == 0
        assert summary['allowed_tiers'] == []
        assert summary['has_restrictions'] is False

    def test_summary_detects_region_restrictions(self, sample_component, tier_a):
        """Test that summary detects region restrictions."""
        TierComponentPermission.objects.create(
            tier=tier_a,
            component=sample_component,
            allowed_regions=['header'],
            max_instances=-1
        )

        summary = get_permission_summary(sample_component)

        assert summary['has_restrictions'] is True

    def test_summary_detects_max_instances_restrictions(self, sample_component, tier_a):
        """Test that summary detects max_instances restrictions."""
        TierComponentPermission.objects.create(
            tier=tier_a,
            component=sample_component,
            allowed_regions=[],
            max_instances=5
        )

        summary = get_permission_summary(sample_component)

        assert summary['has_restrictions'] is True

    def test_summary_no_restrictions_with_unlimited(self, sample_component, tier_a):
        """Test that summary shows no restrictions for unlimited permissions."""
        TierComponentPermission.objects.create(
            tier=tier_a,
            component=sample_component,
            allowed_regions=[],
            max_instances=-1
        )

        summary = get_permission_summary(sample_component)

        assert summary['has_restrictions'] is False

    def test_summary_tiers_are_sorted(self, sample_component, tier_a, tier_b, tier_c):
        """Test that allowed_tiers in summary are sorted."""
        # Create permissions in non-alphabetical order
        for tier in [tier_c, tier_a, tier_b]:
            TierComponentPermission.objects.create(
                tier=tier,
                component=sample_component,
                allowed_regions=[],
                max_instances=-1
            )

        summary = get_permission_summary(sample_component)

        # Should be sorted A, B, C
        assert summary['allowed_tiers'] == ['A', 'B', 'C']
