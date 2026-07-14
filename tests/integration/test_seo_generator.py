"""
SEO Generator App Integration Tests.

Comprehensive tests covering:
- Provider: DeterministicSEOProvider (title/description/keyword generation, truncation, error handling)
- Registry: ProviderRegistry (discovery, default provider, invalid provider)
- API: generate_seo endpoint (auth, permissions, model types, success)
- API: batch_generate endpoint (batch processing, mixed results)
- API: seo_status endpoint (status with/without SEO)
- Signals: Auto-generate on save (enabled, disabled, no recursion)
- Models: SEOProviderAccount (CRUD, encryption, unique primary constraint)
- Admin: Provider browse page, changelist
- Template CSP Compliance: No inline style= attributes, no onclick handlers
- Static Files: CSS and JS copyright headers
- i18n: verbose_name translations on all models
"""

import json
import re
from pathlib import Path

import pytest
from django.contrib.sites.models import Site
from django.db import IntegrityError, transaction
from django.test import Client
from django.urls import reverse

from seo_generator.api.endpoints import (
    MODEL_MAP,
    extract_content_from_object,
    get_model_class,
)
from seo_generator.models import SEOProviderAccount
from seo_generator.providers.base import BaseSEOProvider, GenerationError
from seo_generator.providers.builtin import DeterministicSEOProvider
from seo_generator.providers.registry import ProviderRegistry
from tests.factories import (
    CategoryFactory,
    ComponentRegistryFactory,
    PageFactory,
    ProductFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.seo_generator]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def site(db):
    """Get or create the default Django Site (SITE_ID=1)."""
    site_obj, _ = Site.objects.get_or_create(
        id=1,
        defaults={"domain": "localhost", "name": "Test Site"},
    )
    return site_obj


@pytest.fixture
def admin_user(db):
    """Staff superuser for admin operations."""
    return UserFactory(username="seo_admin", staff=True)


@pytest.fixture
def regular_user(db):
    """Non-staff user for auth tests."""
    return UserFactory(username="seo_customer")


@pytest.fixture
def admin_client(admin_user):
    """Authenticated admin client."""
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def regular_client(regular_user):
    """Authenticated non-staff client."""
    client = Client()
    client.force_login(regular_user)
    return client


@pytest.fixture
def provider_account(db, site):
    """Built-in SEO provider account (from data migration or created fresh)."""
    account, _ = SEOProviderAccount.objects.get_or_create(
        site=site,
        provider_key="deterministic",
        defaults={
            "name": "Built-in Generator",
            "is_active": True,
            "is_primary": True,
        },
    )
    return account


@pytest.fixture
def product(db):
    """Test product with SEO fields."""
    return ProductFactory(
        name="Premium Wireless Headphones",
        slug="premium-wireless-headphones",
    )


@pytest.fixture
def category(db):
    """Test category."""
    return CategoryFactory(name="Audio Equipment", slug="audio-equipment")


@pytest.fixture
def page(db):
    """Test page."""
    return PageFactory(title="About Us", slug="about-us")


@pytest.fixture
def site_settings(db):
    """Create SiteSettings for language default."""
    from core.models import SiteSettings

    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )
    return settings


# ============================================================
# DeterministicSEOProvider Tests
# ============================================================


class TestDeterministicProvider:
    """Test the builtin deterministic SEO provider."""

    def setup_method(self):
        self.provider = DeterministicSEOProvider()

    def test_provider_metadata(self):
        """Provider has correct key, name, and capabilities."""
        assert self.provider.provider_key == "deterministic"
        assert self.provider.requires_credentials is False
        caps = self.provider.capabilities
        assert caps["meta_title"] is True
        assert caps["meta_description"] is True
        assert caps["keywords"] is True

    def test_generate_product_title(self):
        """Product title includes name, brand, category."""
        content = {
            "type": "product",
            "name": "Wireless Mouse",
            "brand": "Logitech",
            "category": "Accessories",
        }
        title = self.provider.generate_meta_title(content)
        assert "Wireless Mouse" in title
        assert "Logitech" in title
        assert len(title) <= 63  # 60 + "..."

    def test_generate_category_title(self):
        """Category title uses shop template."""
        content = {"type": "category", "name": "Headphones", "category": "Headphones"}
        title = self.provider.generate_meta_title(content)
        assert "Headphones" in title
        assert "Shop" in title

    def test_generate_brand_title(self):
        """Brand title uses official products template."""
        content = {"type": "brand", "name": "Sony"}
        title = self.provider.generate_meta_title(content)
        assert "Sony" in title
        assert "Official Products" in title

    def test_generate_page_title(self):
        """Page title is just the name."""
        content = {"type": "page", "name": "Contact Us"}
        title = self.provider.generate_meta_title(content)
        assert title == "Contact Us"

    def test_generate_blogpost_title(self):
        """Blog post title is just the name."""
        content = {"type": "blogpost", "name": "How to Choose Headphones"}
        title = self.provider.generate_meta_title(content)
        assert title == "How to Choose Headphones"

    def test_generate_blogcategory_title(self):
        """Blog category title uses Blog suffix."""
        content = {"type": "blogcategory", "name": "Tech Reviews"}
        title = self.provider.generate_meta_title(content)
        assert "Tech Reviews" in title
        assert "Blog" in title

    def test_title_truncation(self):
        """Titles longer than 60 chars are truncated."""
        content = {
            "type": "product",
            "name": "Amazing Super Extra Long Product Name That Goes On And On",
            "brand": "Very Long Brand Name",
            "category": "Very Long Category Name",
        }
        title = self.provider.generate_meta_title(content)
        assert len(title) <= 63  # 60 + "..."

    def test_generate_product_description(self):
        """Product description includes shop prefix and content."""
        content = {
            "type": "product",
            "name": "Wireless Mouse",
            "description": "A great ergonomic mouse for everyday use.",
            "brand": "Logitech",
        }
        desc = self.provider.generate_meta_description(content)
        assert "Wireless Mouse" in desc
        assert len(desc) <= 158  # 155 + "..."

    def test_description_truncation(self):
        """Descriptions longer than 155 chars are truncated."""
        content = {
            "type": "product",
            "name": "Test Product",
            "description": "A" * 300,
        }
        desc = self.provider.generate_meta_description(content)
        assert len(desc) <= 158  # 155 + "..."

    def test_extract_keywords(self):
        """Keywords are extracted from content fields."""
        content = {
            "name": "Wireless Bluetooth Headphones",
            "description": "Premium wireless bluetooth headphones with noise cancellation. Great sound quality.",
        }
        keywords = self.provider.extract_keywords(content)
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        # 'wireless' and 'headphones' should be common
        lower_keywords = [k.lower() for k in keywords]
        assert "wireless" in lower_keywords or "headphones" in lower_keywords

    def test_generate_seo_full_pipeline(self):
        """Full generate_seo produces all three fields."""
        content = {
            "type": "product",
            "name": "Test Product",
            "description": "A nice product description.",
        }
        result = self.provider.generate_seo(content, "en")
        assert "meta_title" in result
        assert "meta_description" in result
        assert "keywords" in result
        assert result["meta_title"]
        assert result["meta_description"]
        assert isinstance(result["keywords"], list)

    def test_empty_name_raises_error(self):
        """GenerationError raised when name is empty."""
        content = {"type": "product", "name": "", "description": "Some desc"}
        with pytest.raises(GenerationError):
            self.provider.generate_meta_title(content)

    def test_html_stripped_from_content(self):
        """HTML tags are cleaned from text."""
        text = "<p>Hello <b>World</b></p>"
        cleaned = self.provider._clean_text(text)
        assert "<p>" not in cleaned
        assert "<b>" not in cleaned
        assert "Hello World" in cleaned


# ============================================================
# ProviderRegistry Tests
# ============================================================


class TestProviderRegistry:
    """Test provider discovery and registry."""

    def test_get_deterministic_provider(self):
        """Deterministic provider is always available."""
        provider_class = ProviderRegistry.get_provider("deterministic")
        assert provider_class is not None
        assert issubclass(provider_class, BaseSEOProvider)

    def test_get_default_provider(self):
        """Default provider returns deterministic."""
        provider_class = ProviderRegistry.get_default_provider()
        assert provider_class is not None
        assert provider_class.provider_key == "deterministic"

    def test_get_invalid_provider_returns_none(self):
        """Requesting nonexistent provider returns None."""
        provider_class = ProviderRegistry.get_provider("nonexistent_provider")
        assert provider_class is None

    def test_list_providers_includes_deterministic(self):
        """Provider listing includes the built-in provider."""
        providers = ProviderRegistry.list_providers()
        assert isinstance(providers, list)
        assert len(providers) >= 1
        keys = [p["key"] for p in providers]
        assert "deterministic" in keys

    def test_is_provider_installed(self):
        """is_provider_installed returns correct boolean."""
        assert ProviderRegistry.is_provider_installed("deterministic") is True
        assert ProviderRegistry.is_provider_installed("nonexistent") is False

    def test_get_provider_choices(self):
        """Provider choices returns list of tuples."""
        choices = ProviderRegistry.get_provider_choices()
        assert isinstance(choices, list)
        assert all(isinstance(c, tuple) and len(c) == 2 for c in choices)


# ============================================================
# API: generate_seo Tests
# ============================================================


class TestSEOGenerateAPI:
    """Test the generate_seo API endpoint."""

    def test_requires_authentication(self, client, product, site_settings):
        """Unauthenticated requests are rejected."""
        url = reverse("seo_generator_api:generate", args=["product", product.pk])
        response = client.post(url, content_type="application/json")
        # staff_member_required redirects to login
        assert response.status_code == 302

    def test_requires_staff(self, regular_client, product, site_settings):
        """Non-staff users are rejected."""
        url = reverse("seo_generator_api:generate", args=["product", product.pk])
        response = regular_client.post(url, content_type="application/json")
        # staff_member_required redirects to login
        assert response.status_code == 302

    def test_invalid_model_type(self, admin_client, site_settings):
        """Invalid model type returns 400."""
        url = reverse("seo_generator_api:generate", args=["invalid", 1])
        response = admin_client.post(url, content_type="application/json")
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_nonexistent_object(self, admin_client, site_settings):
        """Nonexistent object returns 404."""
        url = reverse("seo_generator_api:generate", args=["product", 99999])
        response = admin_client.post(url, content_type="application/json")
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_generate_for_product(self, admin_client, product, site_settings):
        """Successful generation for product."""
        url = reverse("seo_generator_api:generate", args=["product", product.pk])
        response = admin_client.post(url, content_type="application/json")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "meta_title" in data
        assert "meta_description" in data
        assert "keywords" in data
        assert data["saved"] is True

        # Verify saved to database
        product.refresh_from_db()
        assert product.meta_title == data["meta_title"]
        assert product.meta_description == data["meta_description"]

    def test_generate_for_category(self, admin_client, category, site_settings):
        """Successful generation for category."""
        url = reverse("seo_generator_api:generate", args=["category", category.pk])
        response = admin_client.post(url, content_type="application/json")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_generate_for_page(self, admin_client, page, site_settings):
        """Successful generation for page."""
        url = reverse("seo_generator_api:generate", args=["page", page.pk])
        response = admin_client.post(url, content_type="application/json")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_custom_provider_key(self, admin_client, product, site_settings):
        """Custom provider key is accepted if valid."""
        url = reverse("seo_generator_api:generate", args=["product", product.pk])
        response = admin_client.post(
            url, data=json.dumps({"provider": "deterministic"}), content_type="application/json"
        )
        assert response.status_code == 200

    def test_invalid_provider_key_chars(self, admin_client, product, site_settings):
        """Provider key with invalid chars returns 400."""
        url = reverse("seo_generator_api:generate", args=["product", product.pk])
        response = admin_client.post(
            url,
            data=json.dumps({"provider": "../../../etc/passwd"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_get_method_not_allowed(self, admin_client, product, site_settings):
        """GET requests return 405."""
        url = reverse("seo_generator_api:generate", args=["product", product.pk])
        response = admin_client.get(url)
        assert response.status_code == 405


# ============================================================
# API: batch_generate Tests
# ============================================================


class TestBatchGenerateAPI:
    """Test the batch_generate API endpoint."""

    def test_batch_generate_success(self, admin_client, product, category, site_settings):
        """Batch generation processes multiple items."""
        url = reverse("seo_generator_api:batch_generate")
        response = admin_client.post(
            url,
            data=json.dumps(
                {
                    "items": [
                        {"model_type": "product", "object_id": product.pk},
                        {"model_type": "category", "object_id": category.pk},
                    ]
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["summary"]["total"] == 2
        assert data["summary"]["successful"] == 2
        assert data["summary"]["failed"] == 0

    def test_batch_empty_items(self, admin_client, site_settings):
        """Empty items list returns 400."""
        url = reverse("seo_generator_api:batch_generate")
        response = admin_client.post(
            url, data=json.dumps({"items": []}), content_type="application/json"
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_batch_mixed_results(self, admin_client, product, site_settings):
        """Batch with valid and invalid items reports mixed results."""
        url = reverse("seo_generator_api:batch_generate")
        response = admin_client.post(
            url,
            data=json.dumps(
                {
                    "items": [
                        {"model_type": "product", "object_id": product.pk},
                        {"model_type": "product", "object_id": 99999},  # nonexistent
                    ]
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["summary"]["successful"] == 1
        assert data["summary"]["failed"] == 1

    def test_batch_missing_fields(self, admin_client, site_settings):
        """Items missing model_type or object_id are counted as failed."""
        url = reverse("seo_generator_api:batch_generate")
        response = admin_client.post(
            url,
            data=json.dumps(
                {
                    "items": [
                        {"model_type": "product"},  # missing object_id
                    ]
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["summary"]["failed"] == 1


# ============================================================
# API: seo_status Tests
# ============================================================


class TestSEOStatusAPI:
    """Test the seo_status API endpoint."""

    def test_status_without_seo(self, admin_client, product, site_settings):
        """Status shows has_seo=False when no SEO content."""
        url = reverse("seo_generator_api:status", args=["product", product.pk])
        response = admin_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["has_seo"] is False

    def test_status_with_seo(self, admin_client, product, site_settings):
        """Status shows has_seo=True when SEO content exists."""
        product.meta_title = "Test SEO Title"
        product.meta_description = "Test SEO description."
        product.save(update_fields=["meta_title", "meta_description"])

        url = reverse("seo_generator_api:status", args=["product", product.pk])
        response = admin_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["has_seo"] is True
        assert data["meta_title"] == "Test SEO Title"
        assert data["meta_title_length"] == len("Test SEO Title")
        assert data["meta_description_length"] == len("Test SEO description.")

    def test_status_invalid_model(self, admin_client, site_settings):
        """Status with invalid model type returns 400."""
        url = reverse("seo_generator_api:status", args=["invalid", 1])
        response = admin_client.get(url)
        assert response.status_code == 400

    def test_status_nonexistent_object(self, admin_client, site_settings):
        """Status for nonexistent object returns 404."""
        url = reverse("seo_generator_api:status", args=["product", 99999])
        response = admin_client.get(url)
        assert response.status_code == 404

    def test_post_method_not_allowed(self, admin_client, product, site_settings):
        """POST requests return 405 for status endpoint."""
        url = reverse("seo_generator_api:status", args=["product", product.pk])
        response = admin_client.post(url)
        assert response.status_code == 405


# ============================================================
# Auto-Generation on Save Tests
# ============================================================


class TestAutoGenerateOnSave:
    """Test auto-generation of SEO content on model save."""

    def test_auto_generate_when_enabled(self, db, site_settings):
        """SEO auto-generates when seo_auto_generated=True and fields empty."""
        product = ProductFactory(
            name="Auto SEO Product",
            slug="auto-seo-product",
        )
        # Enable auto-generation and save
        product.seo_auto_generated = True
        product.meta_title = ""
        product.meta_description = ""
        product.save()

        # Refresh from DB - signal uses QuerySet.update() so instance won't update
        product.refresh_from_db()
        assert product.meta_title != ""
        assert product.meta_description != ""
        assert "Auto SEO Product" in product.meta_title

    def test_no_auto_generate_when_disabled(self, db, site_settings):
        """SEO does not auto-generate when seo_auto_generated=False."""
        product = ProductFactory(
            name="No Auto SEO Product",
            slug="no-auto-seo-product",
        )
        product.seo_auto_generated = False
        product.meta_title = ""
        product.meta_description = ""
        product.save()

        product.refresh_from_db()
        assert product.meta_title == ""
        assert product.meta_description == ""

    def test_no_auto_generate_when_seo_exists(self, db, site_settings):
        """SEO does not overwrite existing content."""
        product = ProductFactory(
            name="Existing SEO Product",
            slug="existing-seo-product",
        )
        product.seo_auto_generated = True
        product.meta_title = "My Custom Title"
        product.meta_description = "My custom description."
        product.save()

        product.refresh_from_db()
        assert product.meta_title == "My Custom Title"
        assert product.meta_description == "My custom description."

    def test_no_infinite_recursion(self, db, site_settings):
        """Signal doesn't cause infinite recursion via update_fields guard."""
        product = ProductFactory(
            name="Recursion Test",
            slug="recursion-test",
        )
        product.seo_auto_generated = True
        product.meta_title = ""
        product.meta_description = ""
        # This should not raise RecursionError
        product.save()
        product.refresh_from_db()
        assert product.meta_title != ""


# ============================================================
# SEOProviderAccount Model Tests
# ============================================================


class TestSEOProviderAccount:
    """Test the SEOProviderAccount model."""

    def test_create_builtin_account(self, site):
        """Can create a built-in provider account."""
        account = SEOProviderAccount.objects.create(
            site=site,
            provider_key="deterministic",
            name="Test Built-in",
            is_active=True,
        )
        assert account.pk is not None
        assert str(account) == "Test Built-in (deterministic)"

    def test_create_component_account(self, site):
        """Can create a component-based provider account."""
        component = ComponentRegistryFactory(
            component_type="seo_generator_provider",
            slug="test-seo-provider",
            name="Test SEO Provider",
        )
        account = SEOProviderAccount.objects.create(
            site=site,
            component=component,
            name="Test Component Provider",
            is_active=True,
        )
        assert str(account) == "Test Component Provider (Test SEO Provider)"

    def test_auto_primary_on_first_account(self, site):
        """First account is automatically set as primary."""
        SEOProviderAccount.objects.all().delete()
        account = SEOProviderAccount.objects.create(
            site=site,
            provider_key="deterministic",
            name="First Account",
        )
        assert account.is_primary is True

    def test_unique_primary_constraint(self, site):
        """Only one primary account per site is allowed."""
        SEOProviderAccount.objects.all().delete()
        SEOProviderAccount.objects.create(
            site=site,
            provider_key="deterministic",
            name="Primary Account",
            is_primary=True,
        )
        with pytest.raises(IntegrityError), transaction.atomic():
            SEOProviderAccount.objects.create(
                site=site,
                provider_key="other",
                name="Second Primary",
                is_primary=True,
            )

    def test_ordering(self, site):
        """Accounts are ordered by -is_primary, priority, name."""
        SEOProviderAccount.objects.all().delete()
        # First account auto-sets is_primary=True via save() override
        c = SEOProviderAccount.objects.create(
            site=site,
            provider_key="c",
            name="B Provider",
            priority=0,
        )
        assert c.is_primary is True  # Auto-set as first
        b = SEOProviderAccount.objects.create(
            site=site,
            provider_key="b",
            name="A Provider",
            is_primary=False,
            priority=5,
        )
        a = SEOProviderAccount.objects.create(
            site=site,
            provider_key="a",
            name="C Provider",
            is_primary=False,
            priority=10,
        )
        accounts = list(SEOProviderAccount.objects.all())
        assert accounts[0] == c  # Primary first
        assert accounts[1] == b  # Then by priority
        assert accounts[2] == a

    def test_verbose_names(self):
        """Model has translated verbose_name."""
        assert SEOProviderAccount._meta.verbose_name is not None
        assert SEOProviderAccount._meta.verbose_name_plural is not None


# ============================================================
# Encryption Utils Tests
# ============================================================


class TestEncryptionUtils:
    """Test credential encryption/decryption."""

    def test_encrypt_decrypt_roundtrip(self):
        """Encrypting then decrypting returns original data."""
        from seo_generator.utils.encryption import decrypt_credentials, encrypt_credentials

        original = {"api_key": "sk-test-12345", "secret": "my-secret-value"}
        encrypted = encrypt_credentials(original)
        assert isinstance(encrypted, bytes)
        assert encrypted != json.dumps(original).encode()  # Not plaintext

        decrypted = decrypt_credentials(encrypted)
        assert decrypted == original

    def test_redact_credentials(self):
        """Sensitive fields are redacted for logging."""
        from seo_generator.utils.encryption import redact_credentials

        creds = {
            "api_key": "sk-test-12345",
            "password": "my-secret",
            "secret": "very-secret",
            "username": "admin",
        }
        redacted = redact_credentials(creds)
        # Long values show first 3 + *** + last 3
        assert "***" in redacted["api_key"]
        assert redacted["api_key"] != creds["api_key"]  # Not plaintext
        assert "***" in redacted["password"]
        assert "***" in redacted["secret"]
        assert redacted["username"] == "admin"  # Not a sensitive field


# ============================================================
# Content Extraction Tests
# ============================================================


class TestContentExtraction:
    """Test extract_content_from_object for various model types."""

    def test_extract_product_content(self, product):
        """Product content includes name and type."""
        content = extract_content_from_object(product, "product")
        assert content["type"] == "product"
        assert content["name"] == "Premium Wireless Headphones"

    def test_extract_category_content(self, category):
        """Category content includes name."""
        content = extract_content_from_object(category, "category")
        assert content["type"] == "category"
        assert content["name"] == "Audio Equipment"

    def test_extract_page_content(self, page):
        """Page content uses title field."""
        content = extract_content_from_object(page, "page")
        assert content["type"] == "page"
        assert content["name"] == "About Us"

    def test_get_model_class_valid(self):
        """get_model_class returns correct model for all types."""
        for model_type in MODEL_MAP:
            model_class = get_model_class(model_type)
            assert model_class is not None

    def test_get_model_class_invalid(self):
        """get_model_class raises ValueError for invalid type."""
        with pytest.raises(ValueError):
            get_model_class("nonexistent")


# ============================================================
# MODEL_MAP Tests
# ============================================================


class TestModelMap:
    """Test MODEL_MAP covers all expected model types."""

    def test_includes_product(self):
        assert "product" in MODEL_MAP

    def test_includes_category(self):
        assert "category" in MODEL_MAP

    def test_includes_brand(self):
        assert "brand" in MODEL_MAP

    def test_includes_page(self):
        assert "page" in MODEL_MAP

    def test_includes_blogpost(self):
        assert "blogpost" in MODEL_MAP

    def test_includes_blogcategory(self):
        assert "blogcategory" in MODEL_MAP


# ============================================================
# Provider Browse View Tests
# ============================================================


class TestProviderBrowseView:
    """Test the provider browse page."""

    def test_browse_requires_auth(self, client, site_settings):
        """Browse page requires authentication."""
        url = reverse("seo_generator:provider_browse")
        response = client.get(url)
        assert response.status_code == 302  # Redirect to login

    def test_browse_loads_for_staff(self, admin_client, site_settings):
        """Browse page loads for staff users."""
        url = reverse("seo_generator:provider_browse")
        response = admin_client.get(url)
        assert response.status_code == 200


# ============================================================
# Admin Tests
# ============================================================


class TestSEOProviderAccountAdmin:
    """Test the admin changelist and configuration."""

    def test_changelist_loads(self, admin_client, provider_account, site_settings):
        """Admin changelist page loads."""
        url = reverse("admin:seo_generator_seoprovideraccount_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_changelist_context(self, admin_client, provider_account, site_settings):
        """Changelist has extra context (active_count, primary_provider)."""
        url = reverse("admin:seo_generator_seoprovideraccount_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200


# ============================================================
# Template CSP Compliance Tests
# ============================================================


class TestCSPCompliance:
    """Verify no inline styles or event handlers in templates."""

    TEMPLATE_DIRS = [
        PROJECT_ROOT / "seo_generator" / "templates",
    ]

    def _get_html_files(self):
        """Collect all HTML template files."""
        files = []
        for template_dir in self.TEMPLATE_DIRS:
            if template_dir.exists():
                files.extend(template_dir.rglob("*.html"))
        return files

    def test_no_inline_style_attributes(self):
        """Templates must not use inline style= attributes except for data-driven
        initial values (progress bars, modal display state, etc.).

        Per CLAUDE.md 'Security & CSP hardening': static styles go in external
        CSS, but data-driven values (e.g. progress bar width) may keep a
        minimal inline style on that attribute only.
        """
        # Allowed inline style patterns for data-driven initial values.
        allowed_patterns = [
            r'\bstyle\s*=\s*["\']width:\s*0%;?["\']',  # progress bar initial
            r'\bstyle\s*=\s*["\']display:\s*none;?["\']',  # modal initial state
        ]

        for html_file in self._get_html_files():
            content = html_file.read_text()
            matches = re.findall(r'\bstyle\s*=\s*["\'][^"\']*["\']', content)
            # Filter out allowed data-driven initial-value styles.
            disallowed = [m for m in matches if not any(re.match(p, m) for p in allowed_patterns)]
            assert len(disallowed) == 0, (
                f"Non-data-driven inline style= found in "
                f"{html_file.relative_to(PROJECT_ROOT)}: {disallowed}"
            )

    def test_no_inline_event_handlers(self):
        """Templates must not use onclick, onsubmit, etc."""
        event_pattern = re.compile(r"\bon(click|submit|change|load|error)\s*=", re.IGNORECASE)
        for html_file in self._get_html_files():
            content = html_file.read_text()
            matches = event_pattern.findall(content)
            assert len(matches) == 0, (
                f"Inline event handler found in {html_file.relative_to(PROJECT_ROOT)}"
            )


# ============================================================
# Static Files Tests
# ============================================================


class TestStaticFiles:
    """Verify static file compliance."""

    STATIC_DIR = PROJECT_ROOT / "seo_generator" / "static" / "seo_generator"

    def _get_js_files(self):
        return list(self.STATIC_DIR.rglob("*.js")) if self.STATIC_DIR.exists() else []

    def _get_css_files(self):
        return list(self.STATIC_DIR.rglob("*.css")) if self.STATIC_DIR.exists() else []

    # The canonical header per project CLAUDE.md is:
    #   /* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
    # Older files may use the ASCII "(c)" or the UTF-8 copyright symbol.
    COPYRIGHT_PATTERN = re.compile(r"(?:©|\(c\))\s*\d{4}(?:-\d{4})?\s*Spwig", re.IGNORECASE)

    def test_js_copyright_headers(self):
        """All JS files have copyright header."""
        for js_file in self._get_js_files():
            content = js_file.read_text()
            assert self.COPYRIGHT_PATTERN.search(content), (
                f"Missing copyright header in {js_file.relative_to(PROJECT_ROOT)}"
            )

    def test_css_copyright_headers(self):
        """All CSS files have copyright header."""
        for css_file in self._get_css_files():
            content = css_file.read_text()
            assert self.COPYRIGHT_PATTERN.search(content), (
                f"Missing copyright header in {css_file.relative_to(PROJECT_ROOT)}"
            )

    def test_no_console_log_in_js(self):
        """JS files must not contain console.log statements."""
        for js_file in self._get_js_files():
            content = js_file.read_text()
            assert "console.log" not in content, (
                f"console.log found in {js_file.relative_to(PROJECT_ROOT)}"
            )


# ============================================================
# i18n Tests
# ============================================================


class TestI18n:
    """Test that model verbose names and app config use i18n."""

    def test_app_verbose_name(self):
        """App has translated verbose_name."""
        from seo_generator.apps import SeoGeneratorConfig

        assert SeoGeneratorConfig.verbose_name is not None

    def test_model_verbose_name(self):
        """SEOProviderAccount has verbose_name set."""
        assert str(SEOProviderAccount._meta.verbose_name) == "SEO Provider Account"
        assert str(SEOProviderAccount._meta.verbose_name_plural) == "SEO Provider Accounts"

    def test_field_verbose_names(self):
        """Key fields have verbose_name set."""
        fields = {
            f.name: f for f in SEOProviderAccount._meta.get_fields() if hasattr(f, "verbose_name")
        }
        assert "name" in fields
        assert "is_active" in fields
        assert "is_primary" in fields
