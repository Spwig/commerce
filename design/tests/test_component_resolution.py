"""
Tests for ComponentRegistryService - Component Resolution and Loading

Tests cover:
- Component lookup by type and tier
- Version resolution (latest vs specific)
- Template loading from packages
- Context preparation for rendering
- Caching mechanism
- Fallback handling for missing components
- Permission validation
"""

from unittest.mock import Mock, mock_open, patch

import pytest
from django.core.cache import cache
from django.core.exceptions import ValidationError

from design.component_registry_service import ComponentRegistryService, ComponentResolutionError
from design.models import ComponentStore, TierComponentPermission


@pytest.mark.django_db
class TestComponentRegistryServiceBasics:
    """Test basic component registry service functionality."""

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before and after each test."""
        cache.clear()
        yield
        cache.clear()

    def test_initialize_service(self):
        """Test service initialization."""
        service = ComponentRegistryService()
        assert service is not None
        assert service.schema_registry is not None

    def test_cache_key_building(self):
        """Test cache key generation."""
        service = ComponentRegistryService()

        key1 = service._build_cache_key("banner", "C", "1.0.0")
        assert "banner" in key1
        assert "C" in key1
        assert "1.0.0" in key1

        key2 = service._build_cache_key("banner", "C", None)
        assert "latest" in key2


@pytest.mark.django_db
class TestComponentResolution:
    """Test component resolution functionality."""

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before and after each test."""
        cache.clear()
        yield
        cache.clear()

    def test_resolve_component_basic(self):
        """Test basic component resolution."""
        with patch.object(ComponentRegistryService, "_load_component_from_db") as mock_load:
            with patch.object(ComponentRegistryService, "_cache_component"):
                mock_component = Mock(spec=ComponentStore)
                mock_component.component_type = "banner"
                mock_component.name = "Banner Component"
                mock_component.version = "1.0.0"
                mock_component.package_name = "banner"
                mock_load.return_value = mock_component

                service = ComponentRegistryService()
                result = service.resolve_for_render("banner", "C")

                assert result["component"] == mock_component
                assert "template_path" in result
                assert "assets" in result
                assert "permissions" in result

    def test_resolve_component_with_specific_version(self):
        """Test component resolution with specific version."""
        with patch.object(ComponentRegistryService, "_load_component_from_db") as mock_load:
            with patch.object(ComponentRegistryService, "_cache_component"):
                mock_component = Mock(spec=ComponentStore)
                mock_component.component_type = "banner"
                mock_component.version = "2.0.0"
                mock_component.package_name = "banner"
                mock_load.return_value = mock_component

                service = ComponentRegistryService()
                result = service.resolve_for_render("banner", "C", version="2.0.0")

                assert result["component"].version == "2.0.0"

    def test_resolve_component_not_found(self):
        """Test component resolution when component doesn't exist."""
        with patch.object(ComponentRegistryService, "_load_component_from_db") as mock_load:
            mock_load.side_effect = ComponentStore.DoesNotExist("Not found")

            service = ComponentRegistryService()

            with pytest.raises(ComponentResolutionError, match="not found"):
                service.resolve_for_render("nonexistent", "C")

    def test_resolve_component_with_permission_validation(self):
        """Test component resolution with tier permission validation."""
        with patch.object(ComponentRegistryService, "_load_component_from_db") as mock_load:
            with patch.object(
                ComponentRegistryService, "_validate_tier_permissions"
            ) as mock_validate:
                with patch.object(ComponentRegistryService, "_cache_component"):
                    with patch.object(
                        ComponentRegistryService,
                        "_get_template_path",
                        return_value="/tmp/template.html",
                    ):
                        mock_component = Mock(spec=ComponentStore)
                        mock_component.component_type = "banner"
                        mock_component.package_name = "banner"
                        mock_load.return_value = mock_component

                        service = ComponentRegistryService()
                        result = service.resolve_for_render("banner", "C", page_type="home")

                        # Should call validation when page_type provided
                        mock_validate.assert_called_once()

    def test_resolve_component_permission_denied(self):
        """Test component resolution when permissions deny access."""
        with patch.object(ComponentRegistryService, "_load_component_from_db") as mock_load:
            with patch.object(
                ComponentRegistryService, "_validate_tier_permissions"
            ) as mock_validate:
                mock_component = Mock(spec=ComponentStore)
                mock_component.component_type = "custom_banner"
                mock_component.package_name = "custom_banner"
                mock_load.return_value = mock_component
                mock_validate.side_effect = ValidationError("Not allowed")

                service = ComponentRegistryService()

                with pytest.raises(ComponentResolutionError):
                    service.resolve_for_render("custom_banner", "A", page_type="checkout")


@pytest.mark.django_db
class TestComponentTemplateLoading:
    """Test component template loading."""

    def test_load_template_file_exists(self):
        """Test loading template when file exists."""
        mock_template_content = '<div class="banner">{{ title }}</div>'

        with patch("builtins.open", mock_open(read_data=mock_template_content)):
            with patch("os.path.exists", return_value=True):
                mock_component = Mock(spec=ComponentStore)
                mock_component.component_type = "banner"
                mock_component.version = "1.0.0"
                mock_component.package_name = "banner"

                service = ComponentRegistryService()
                template = service.load_component_template(mock_component)

                assert template == mock_template_content

    def test_load_template_file_not_exists(self):
        """Test loading template when file doesn't exist returns fallback."""
        with patch("os.path.exists", return_value=False):
            mock_component = Mock(spec=ComponentStore)
            mock_component.component_type = "banner"
            mock_component.name = "Banner"
            mock_component.version = "1.0.0"
            mock_component.package_name = "banner"

            service = ComponentRegistryService()
            template = service.load_component_template(mock_component)

            # Should return fallback template
            assert "component-fallback" in template
            assert "banner" in template

    def test_fallback_template_generation(self):
        """Test fallback template generation."""
        mock_component = Mock(spec=ComponentStore)
        mock_component.component_type = "test_component"
        mock_component.name = "Test Component"
        mock_component.version = "1.0.0"

        service = ComponentRegistryService()
        fallback = service._get_fallback_template(mock_component)

        assert "component-fallback" in fallback
        assert "Test Component" in fallback
        assert "test_component" in fallback
        assert "1.0.0" in fallback


@pytest.mark.django_db
class TestComponentContextPreparation:
    """Test component context preparation."""

    def test_prepare_context_basic(self):
        """Test basic context preparation."""
        mock_component = Mock(spec=ComponentStore)
        mock_component.component_type = "banner"
        mock_component.name = "Banner Component"
        mock_component.version = "1.0.0"

        instance_data = {"title": "Welcome", "subtitle": "to our store"}

        page_context = {"tier": "C", "page_type": "home", "user_id": 123}

        service = ComponentRegistryService()
        context = service.prepare_component_context(mock_component, instance_data, page_context)

        assert context["component"]["type"] == "banner"
        assert context["component"]["name"] == "Banner Component"
        assert context["title"] == "Welcome"
        assert context["subtitle"] == "to our store"
        assert context["tier"] == "C"
        assert context["page_type"] == "home"
        assert context["user_id"] == 123

    def test_prepare_context_instance_data_overrides_page_context(self):
        """Test that instance data takes precedence over page context."""
        mock_component = Mock(spec=ComponentStore)
        mock_component.component_type = "banner"
        mock_component.name = "Banner"
        mock_component.version = "1.0.0"

        instance_data = {"title": "Instance Title"}

        page_context = {
            "tier": "C",
            "title": "Page Title",  # Should be overridden
        }

        service = ComponentRegistryService()
        context = service.prepare_component_context(mock_component, instance_data, page_context)

        assert context["title"] == "Instance Title"  # Instance data wins


@pytest.mark.django_db
class TestComponentCaching:
    """Test component caching mechanism."""

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before and after each test."""
        cache.clear()
        yield
        cache.clear()

    def test_component_caching(self):
        """Test that components are cached after first load."""
        with patch.object(ComponentRegistryService, "_load_component_from_db") as mock_load:
            with patch.object(ComponentRegistryService, "_get_cached_component") as mock_get_cache:
                with patch.object(ComponentRegistryService, "_cache_component") as mock_set_cache:
                    mock_component = Mock(spec=ComponentStore)
                    mock_component.component_type = "banner"
                    mock_component.version = "1.0.0"
                    mock_component.package_name = "banner"
                    mock_load.return_value = mock_component

                    # First call: cache miss
                    mock_get_cache.side_effect = [None, mock_component]

                    service = ComponentRegistryService()

                    # First call should load from DB
                    result1 = service.resolve_for_render("banner", "C")
                    assert mock_load.call_count == 1
                    assert mock_set_cache.call_count == 1  # Should cache

                    # Second call should use cache
                    result2 = service.resolve_for_render("banner", "C")
                    assert mock_load.call_count == 1  # Should not call DB again

    def test_cache_key_uniqueness(self):
        """Test that different tiers/versions have different cache keys."""
        service = ComponentRegistryService()

        key1 = service._build_cache_key("banner", "A", "1.0.0")
        key2 = service._build_cache_key("banner", "B", "1.0.0")
        key3 = service._build_cache_key("banner", "A", "2.0.0")

        assert key1 != key2  # Different tiers
        assert key1 != key3  # Different versions


@pytest.mark.django_db
class TestFallbackHandling:
    """Test fallback handling for missing components."""

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before and after each test."""
        cache.clear()
        yield
        cache.clear()

    def test_get_fallback_component(self):
        """Test fallback component generation."""
        service = ComponentRegistryService()
        fallback = service.get_fallback_component("missing_component")

        assert fallback["component"].component_type == "missing_component"
        assert fallback["is_fallback"] is True
        assert "Missing" in fallback["component"].name

    def test_fallback_has_required_fields(self):
        """Test that fallback component has all required fields."""
        service = ComponentRegistryService()
        fallback = service.get_fallback_component("test")

        assert "component" in fallback
        assert "template_path" in fallback
        assert "assets" in fallback
        assert "permissions" in fallback
        assert "is_fallback" in fallback


@pytest.mark.django_db
class TestComponentDatabaseLoading:
    """Test loading components from database."""

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before and after each test."""
        cache.clear()
        yield
        cache.clear()

    def test_load_component_latest_version(self):
        """Test loading latest version of component."""
        # Create mock components in database
        with patch.object(ComponentStore.objects, "filter") as mock_filter:
            mock_queryset = Mock()
            mock_queryset.order_by.return_value = mock_queryset
            mock_component = Mock(spec=ComponentStore)
            mock_component.component_type = "banner"
            mock_component.version = "2.0.0"
            mock_queryset.first.return_value = mock_component
            mock_filter.return_value = mock_queryset

            service = ComponentRegistryService()
            component = service._load_component_from_db("banner", "C", version=None)

            assert component.version == "2.0.0"
            # Should order by -created_at to get latest
            mock_queryset.order_by.assert_called_with("-created_at")

    def test_load_component_specific_version(self):
        """Test loading specific version of component."""
        with patch.object(ComponentStore.objects, "filter") as mock_filter:
            # Create two mock querysets for chaining
            mock_queryset1 = Mock()
            mock_queryset2 = Mock()
            mock_component = Mock(spec=ComponentStore)
            mock_component.component_type = "banner"
            mock_component.version = "1.0.0"

            # First filter returns queryset1, which chains to queryset2, which has first()
            mock_filter.return_value = mock_queryset1
            mock_queryset1.filter.return_value = mock_queryset2
            mock_queryset2.first.return_value = mock_component

            service = ComponentRegistryService()
            component = service._load_component_from_db("banner", "C", version="1.0.0")

            assert component.version == "1.0.0"

    def test_load_component_not_found_raises_error(self):
        """Test loading nonexistent component raises DoesNotExist."""
        with patch.object(ComponentStore.objects, "filter") as mock_filter:
            mock_queryset = Mock()
            mock_queryset.order_by.return_value = mock_queryset
            mock_queryset.first.return_value = None  # Not found
            mock_filter.return_value = mock_queryset

            service = ComponentRegistryService()

            with pytest.raises(ComponentStore.DoesNotExist):
                service._load_component_from_db("nonexistent", "C")


@pytest.mark.django_db
class TestComponentPermissions:
    """Test component permission handling."""

    def test_get_component_permissions(self):
        """Test retrieving component permissions for tier."""
        with patch.object(TierComponentPermission.objects, "filter") as mock_filter:
            mock_permission = Mock()
            mock_permission.allowed_regions = ["header", "footer"]
            mock_permission.max_instances = 1
            mock_permission.is_locked = False

            mock_queryset = Mock()
            mock_queryset.first.return_value = mock_permission
            mock_filter.return_value = mock_queryset

            mock_component = Mock(spec=ComponentStore)
            mock_component.component_type = "banner"

            service = ComponentRegistryService()
            permissions = service._get_component_permissions(mock_component, "C")

            assert permissions["allowed_regions"] == ["header", "footer"]
            assert permissions["max_instances"] == 1
            assert permissions["is_locked"] is False

    def test_get_component_permissions_not_found(self):
        """Test retrieving permissions when none exist."""
        with patch.object(TierComponentPermission.objects, "filter") as mock_filter:
            mock_queryset = Mock()
            mock_queryset.first.return_value = None
            mock_filter.return_value = mock_queryset

            mock_component = Mock(spec=ComponentStore)
            service = ComponentRegistryService()
            permissions = service._get_component_permissions(mock_component, "C")

            assert permissions == {}
