"""
Unit tests for TokenResolver and component-scoped token resolution.

Tests cover:
- DesignToken model with component scoping
- TokenResolver 4-level priority cascade
- Component-scoped token resolution
- Cache key generation with component context
- Token filtering by tier, theme, and component
- Cache invalidation fallback
"""

import io
import zipfile

import pytest
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError

from design.models import ComponentStore, DesignToken
from design.theme_models import Theme
from design.token_resolver import (
    TokenResolver,
    get_token_resolver,
    invalidate_token_cache,
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def create_dummy_package_file(component_type="test_component"):
    """Create a dummy ZIP package file for ComponentStore testing."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        manifest = f'{{"component_type": "{component_type}", "version": "1.0.0"}}'
        zip_file.writestr("manifest.json", manifest)
        zip_file.writestr("template.html", "<div>Test Component</div>")

    zip_buffer.seek(0)
    return SimpleUploadedFile(
        f"{component_type}.zip", zip_buffer.read(), content_type="application/zip"
    )


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def theme(db):
    """Create a test theme."""
    return Theme.objects.create(
        name="Test Theme",
        slug="test-theme",
        version="1.0.0",
        author="Test Author",
        is_active=True,
        is_default=False,
    )


@pytest.fixture
def component_hero(db):
    """Create a hero banner component."""
    return ComponentStore.objects.create(
        component_type="hero_banner",
        display_name="Hero Banner",
        version="1.0.0",
        author="Spwig",
        description="Hero banner component",
        package_file=create_dummy_package_file("hero_banner"),
        review_status="approved",
    )


@pytest.fixture
def component_footer(db):
    """Create a footer component."""
    return ComponentStore.objects.create(
        component_type="footer",
        display_name="Footer",
        version="1.0.0",
        author="Spwig",
        description="Footer component",
        package_file=create_dummy_package_file("footer"),
        review_status="approved",
    )


@pytest.fixture
def system_token_primary(db):
    """Create a system-level primary color token."""
    return DesignToken.objects.create(
        name="primary-color",
        token_type="color",
        value="#1E40AF",
        source="system",
        priority_level=4,
        description="System default primary color",
    )


@pytest.fixture
def theme_token_primary(db, theme):
    """Create a theme-level primary color token."""
    return DesignToken.objects.create(
        name="primary-color",
        token_type="color",
        value="#3B82F6",
        source="theme",
        priority_level=2,
        theme=theme,
        description="Theme primary color",
    )


@pytest.fixture
def component_token_primary(db, component_hero):
    """Create a component-level primary color token for hero banner."""
    return DesignToken.objects.create(
        name="primary-color",
        token_type="color",
        value="#60A5FA",
        source="component",
        priority_level=3,
        component=component_hero,
        description="Hero banner primary color",
    )


@pytest.fixture
def brand_builder_token_primary(db):
    """Create a brand builder primary color token."""
    return DesignToken.objects.create(
        name="primary-color",
        token_type="color",
        value="#FF5733",
        source="brand_builder",
        priority_level=1,
        description="Merchant customized primary color",
    )


# ============================================================================
# TOKEN MODEL TESTS
# ============================================================================


@pytest.mark.django_db
class TestDesignTokenModel:
    """Test DesignToken model with component scoping."""

    def test_create_system_token(self, system_token_primary):
        """System tokens can be created without theme or component."""
        assert system_token_primary.name == "primary-color"
        assert system_token_primary.source == "system"
        assert system_token_primary.priority_level == 4
        assert system_token_primary.theme is None
        assert system_token_primary.component is None

    def test_create_theme_token(self, theme_token_primary, theme):
        """Theme tokens require theme reference."""
        assert theme_token_primary.source == "theme"
        assert theme_token_primary.theme == theme
        assert theme_token_primary.component is None

    def test_create_component_token(self, component_token_primary, component_hero):
        """Component tokens require component reference."""
        assert component_token_primary.source == "component"
        assert component_token_primary.component == component_hero
        assert component_token_primary.theme is None

    def test_component_token_unique_per_component(self, component_hero, component_footer):
        """Same token name can exist for different components."""
        # Create primary-color for hero
        token1 = DesignToken.objects.create(
            name="primary-color",
            token_type="color",
            value="#FF0000",
            source="component",
            priority_level=3,
            component=component_hero,
        )

        # Create primary-color for footer (should work)
        token2 = DesignToken.objects.create(
            name="primary-color",
            token_type="color",
            value="#00FF00",
            source="component",
            priority_level=3,
            component=component_footer,
        )

        assert token1.component != token2.component
        assert DesignToken.objects.filter(name="primary-color", source="component").count() == 2

    def test_component_token_unique_within_component(self, component_hero):
        """Same component cannot have duplicate token names."""
        DesignToken.objects.create(
            name="primary-color",
            token_type="color",
            value="#FF0000",
            source="component",
            priority_level=3,
            component=component_hero,
        )

        # Duplicate should raise IntegrityError
        with pytest.raises(IntegrityError):
            DesignToken.objects.create(
                name="primary-color",
                token_type="color",
                value="#00FF00",
                source="component",
                priority_level=3,
                component=component_hero,
            )

    def test_tier_restriction_json(self):
        """Tier restrictions stored as JSON list."""
        token = DesignToken.objects.create(
            name="secure-color",
            token_type="color",
            value="#000000",
            source="system",
            priority_level=4,
            tier_restriction=["A", "B"],
        )

        assert token.tier_restriction == ["A", "B"]
        assert token.is_available_in_tier("A")
        assert token.is_available_in_tier("B")
        assert not token.is_available_in_tier("C")

    def test_helper_methods(
        self,
        system_token_primary,
        theme_token_primary,
        component_token_primary,
        brand_builder_token_primary,
    ):
        """Test token helper methods."""
        assert system_token_primary.is_system_token()
        assert not system_token_primary.is_theme_token()

        assert theme_token_primary.is_theme_token()
        assert not theme_token_primary.is_component_token()

        assert component_token_primary.is_component_token()
        assert not component_token_primary.is_brand_builder()

        assert brand_builder_token_primary.is_brand_builder()
        assert not brand_builder_token_primary.is_system_token()


# ============================================================================
# TOKEN RESOLVER TESTS
# ============================================================================


@pytest.mark.django_db
class TestTokenResolver:
    """Test TokenResolver with component-scoped resolution."""

    def test_resolver_initialization(self, theme, component_hero):
        """Resolver can be initialized with tier, theme, and component."""
        resolver = TokenResolver(page_tier="A", theme=theme, component=component_hero)

        assert resolver.page_tier == "A"
        assert resolver.theme == theme
        assert resolver.component == component_hero

    def test_cache_key_includes_component(self, theme, component_hero):
        """Cache keys include component ID to prevent cross-component cache pollution."""
        resolver1 = TokenResolver(page_tier="A", theme=theme, component=component_hero)
        resolver2 = TokenResolver(page_tier="A", theme=theme, component=None)

        key1 = resolver1._get_cache_key("primary-color")
        key2 = resolver2._get_cache_key("primary-color")

        assert str(component_hero.id) in key1
        assert "none" in key2
        assert key1 != key2

    def test_resolve_system_token_only(self, system_token_primary):
        """Resolver finds system tokens when no higher priority exists."""
        resolver = TokenResolver()
        token = resolver.resolve_token("primary-color")

        assert token == system_token_primary
        assert token.priority_level == 4

    def test_cascade_priority_system_to_brand_builder(
        self,
        system_token_primary,
        theme_token_primary,
        component_token_primary,
        brand_builder_token_primary,
        theme,
        component_hero,
    ):
        """Brand builder token wins over all others (highest priority)."""
        resolver = TokenResolver(page_tier=None, theme=theme, component=component_hero)
        token = resolver.resolve_token("primary-color")

        # Brand Builder (priority 1) should win
        assert token == brand_builder_token_primary
        assert token.priority_level == 1
        assert token.value == "#FF5733"

    def test_cascade_without_brand_builder(
        self,
        system_token_primary,
        theme_token_primary,
        component_token_primary,
        theme,
        component_hero,
    ):
        """Theme token wins when no brand builder exists."""
        resolver = TokenResolver(page_tier=None, theme=theme, component=component_hero)
        token = resolver.resolve_token("primary-color")

        # Theme (priority 2) should win over component (3) and system (4)
        assert token == theme_token_primary
        assert token.priority_level == 2
        assert token.value == "#3B82F6"

    def test_component_scoped_resolution(
        self, system_token_primary, component_hero, component_footer
    ):
        """Component tokens only resolved when component matches."""
        # Create component-specific token for hero
        hero_token = DesignToken.objects.create(
            name="hero-spacing",
            token_type="spacing",
            value="32px",
            source="component",
            priority_level=3,
            component=component_hero,
        )

        # Resolver with hero component finds it
        resolver_hero = TokenResolver(component=component_hero)
        token = resolver_hero.resolve_token("hero-spacing")
        assert token == hero_token

        # Resolver with footer component doesn't find it
        resolver_footer = TokenResolver(component=component_footer)
        token = resolver_footer.resolve_token("hero-spacing")
        assert token is None

        # Resolver without component doesn't find it
        resolver_none = TokenResolver()
        token = resolver_none.resolve_token("hero-spacing")
        assert token is None

    def test_resolve_all_tokens(self, system_token_primary, theme_token_primary, theme):
        """Resolve all tokens returns cascaded tokens."""
        # Create additional system tokens
        DesignToken.objects.create(
            name="secondary-color",
            token_type="color",
            value="#64748B",
            source="system",
            priority_level=4,
        )

        resolver = TokenResolver(theme=theme)
        tokens = resolver.resolve_all_tokens(token_type="color")

        # Should have both primary (theme override) and secondary (system)
        assert "primary-color" in tokens
        assert "secondary-color" in tokens
        assert tokens["primary-color"] == theme_token_primary  # Theme wins
        assert tokens["secondary-color"].source == "system"

    def test_resolve_all_tokens_with_component_filter(self, component_hero):
        """Resolve all tokens filters by component."""
        # Create component-specific tokens
        DesignToken.objects.create(
            name="hero-padding",
            token_type="spacing",
            value="16px",
            source="component",
            priority_level=3,
            component=component_hero,
        )

        # Create system token
        DesignToken.objects.create(
            name="base-padding",
            token_type="spacing",
            value="8px",
            source="system",
            priority_level=4,
        )

        # Resolve with component context
        resolver = TokenResolver(component=component_hero)
        tokens = resolver.resolve_all_tokens(token_type="spacing")

        assert "hero-padding" in tokens
        assert "base-padding" in tokens

    def test_tier_restriction_filtering(self):
        """Tokens restricted to specific tiers are filtered correctly."""
        # Create tier-restricted token (A only)
        DesignToken.objects.create(
            name="secure-color",
            token_type="color",
            value="#000000",
            source="system",
            priority_level=4,
            tier_restriction=["A"],
        )

        # Create unrestricted token
        DesignToken.objects.create(
            name="public-color",
            token_type="color",
            value="#FFFFFF",
            source="system",
            priority_level=4,
        )

        # Tier A resolver finds both
        resolver_a = TokenResolver(page_tier="A")
        assert resolver_a.resolve_token("secure-color") is not None
        assert resolver_a.resolve_token("public-color") is not None

        # Tier C resolver only finds public
        resolver_c = TokenResolver(page_tier="C")
        assert resolver_c.resolve_token("secure-color") is None
        assert resolver_c.resolve_token("public-color") is not None

    def test_get_css_variables(self, system_token_primary):
        """CSS variables generated correctly."""
        resolver = TokenResolver()
        css = resolver.get_css_variables(token_type="color")

        assert ":root {" in css
        assert "--primary-color: #1E40AF;" in css
        assert "}" in css

    def test_get_cascade_for_token(
        self, system_token_primary, theme_token_primary, brand_builder_token_primary, theme
    ):
        """Get full cascade for debugging shows all priority levels."""
        resolver = TokenResolver(theme=theme)
        cascade = resolver.get_cascade_for_token("primary-color")

        # Should have all 3 priority levels (no component token)
        assert len(cascade) == 3
        assert cascade[0] == brand_builder_token_primary  # Priority 1
        assert cascade[1] == theme_token_primary  # Priority 2
        assert cascade[2] == system_token_primary  # Priority 4

    def test_clear_cache(self, system_token_primary):
        """Cache can be cleared manually."""
        resolver = TokenResolver()

        # Prime cache
        token1 = resolver.resolve_token("primary-color")
        assert token1 is not None

        # Clear cache
        resolver.clear_cache()

        # Token still resolves (from DB)
        token2 = resolver.resolve_token("primary-color")
        assert token2 is not None


# ============================================================================
# CACHE TESTS
# ============================================================================


@pytest.mark.django_db
class TestTokenCaching:
    """Test token caching behavior."""

    def test_token_cached_on_first_resolve(self, system_token_primary):
        """First resolve caches the token."""
        cache.clear()
        resolver = TokenResolver()

        # First call hits database
        token1 = resolver.resolve_token("primary-color")

        # Second call hits cache
        token2 = resolver.resolve_token("primary-color")

        assert token1 == token2
        assert token1 == system_token_primary

    def test_invalidate_cache_clears_all_tokens(self, system_token_primary):
        """invalidate_token_cache clears all resolver caches."""
        resolver = TokenResolver()

        # Prime cache
        resolver.resolve_token("primary-color")

        # Invalidate
        invalidate_token_cache()

        # Should still resolve (from DB)
        token = resolver.resolve_token("primary-color")
        assert token == system_token_primary

    def test_cache_keys_isolated_by_context(self, theme, component_hero):
        """Different resolver contexts use different cache keys."""
        token = DesignToken.objects.create(
            name="test-color",
            token_type="color",
            value="#FF0000",
            source="system",
            priority_level=4,
        )

        resolver1 = TokenResolver(page_tier="A", theme=theme)
        resolver2 = TokenResolver(page_tier="B", component=component_hero)

        key1 = resolver1._get_cache_key("test-color")
        key2 = resolver2._get_cache_key("test-color")

        assert key1 != key2


# ============================================================================
# FACTORY FUNCTION TESTS
# ============================================================================


@pytest.mark.django_db
class TestFactoryFunctions:
    """Test module-level factory functions."""

    def test_get_token_resolver_basic(self):
        """Factory function creates resolver."""
        resolver = get_token_resolver()
        assert isinstance(resolver, TokenResolver)
        assert resolver.page_tier is None
        assert resolver.theme is None
        assert resolver.component is None

    def test_get_token_resolver_with_all_params(self, theme, component_hero):
        """Factory function accepts all parameters."""
        resolver = get_token_resolver(page_tier="A", theme=theme, component=component_hero)

        assert resolver.page_tier == "A"
        assert resolver.theme == theme
        assert resolver.component == component_hero
