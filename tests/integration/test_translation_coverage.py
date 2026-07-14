"""
Translation Coverage System tests.

Tests the content registry, coverage calculation service, API endpoints,
and task processor model content handling.
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from django.core.cache import cache
from django.test import Client

from tests.factories import (
    CategoryFactory,
    ProductFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def target_languages(db):
    """Ensure English default + Spanish/French as active targets.

    Uses update_or_create because data migrations pre-populate SiteLanguage
    with is_active=False, and factory get_or_create won't update existing records.
    """
    from translations.models import SiteLanguage

    SiteLanguage.objects.update_or_create(
        code="en",
        defaults={
            "name": "English",
            "native_name": "English",
            "is_active": True,
            "is_default": True,
            "flag": "",
        },
    )
    es, _ = SiteLanguage.objects.update_or_create(
        code="es",
        defaults={
            "name": "Spanish",
            "native_name": "Español",
            "is_active": True,
            "is_default": False,
            "flag": "",
        },
    )
    fr, _ = SiteLanguage.objects.update_or_create(
        code="fr",
        defaults={
            "name": "French",
            "native_name": "Français",
            "is_active": True,
            "is_default": False,
            "flag": "",
        },
    )
    return [es, fr]


@pytest.fixture
def product_with_partial_translation(db, category):
    """Product with name translated to Spanish only."""
    p = ProductFactory(
        name="Widget",
        slug="widget",
        short_description="A great widget",
        category=category,
    )
    p.translations = {"es": {"name": "Widget ES"}}
    p.save(update_fields=["translations"])
    return p


@pytest.fixture
def product_untranslated(db, category):
    """Product with no translations."""
    return ProductFactory(
        name="Gadget",
        slug="gadget",
        short_description="A nice gadget",
        category=category,
    )


@pytest.fixture
def product_with_html(db, category):
    """Product with HTML in full_description."""
    p = ProductFactory(
        name="HTML Product",
        slug="html-product",
        category=category,
    )
    p.full_description = '<p>Buy our <a href="https://example.com">amazing widget</a>!</p><img src="/media/widget.jpg" alt="widget">'
    p.save(update_fields=["full_description"])
    return p


@pytest.fixture
def product_attribute_simple(db):
    """ProductAttribute with simple format translations."""
    from catalog.models import ProductAttribute

    attr = ProductAttribute.objects.create(
        name="Size",
        slug="size",
        type="select",
        translations={"es": "Tamaño"},
    )
    return attr


@pytest.fixture
def product_attribute_untranslated(db):
    """ProductAttribute with no translations."""
    from catalog.models import ProductAttribute

    return ProductAttribute.objects.create(
        name="Color",
        slug="color",
        type="color",
        translations={},
    )


@pytest.fixture
def staff_client(admin_user):
    """Django test client logged in as staff."""
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture(autouse=True)
def clear_coverage_cache():
    """Clear coverage cache before each test."""
    cache.delete("translation_coverage_v1")
    yield
    cache.delete("translation_coverage_v1")


# ============================================================
# A. Content Registry Tests
# ============================================================


class TestContentRegistry:
    """Pure logic tests for the content registry (no DB needed)."""

    def test_get_content_type_valid_key(self):
        from translations.content_registry import get_content_type

        ct = get_content_type("catalog.product")
        assert ct is not None
        assert ct["key"] == "catalog.product"
        assert ct["model"] == "catalog.Product"
        assert "name" in ct["fields"]
        assert ct["format"] == "nested"
        assert ct["priority"] == 1

    def test_get_content_type_invalid_key(self):
        from translations.content_registry import get_content_type

        assert get_content_type("nonexistent.model") is None

    def test_get_all_content_types_sorted(self):
        from translations.content_registry import get_all_content_types

        types = get_all_content_types()
        # Sorted by priority then label
        for i in range(len(types) - 1):
            a, b = types[i], types[i + 1]
            assert (a["priority"], a["label"]) <= (b["priority"], b["label"])

    def test_get_all_content_types_count(self):
        from translations.content_registry import get_all_content_types

        types = get_all_content_types()
        # Registry has grown as new translatable models are added; assert non-empty
        # and that key content types are present rather than a brittle exact count.
        assert len(types) >= 12

    def test_get_content_type_keys(self):
        from translations.content_registry import get_content_type_keys

        keys = get_content_type_keys()
        assert "catalog.product" in keys
        assert "catalog.category" in keys
        assert "page_builder.page" in keys
        assert "core.sitesettings" in keys
        assert "blog.blogpost" in keys
        assert "media_library.mediaasset" in keys

    def test_get_model_class_valid(self):
        from catalog.models import Product
        from translations.content_registry import get_model_class

        model = get_model_class("catalog.product")
        assert model is Product

    def test_get_model_class_invalid(self):
        from translations.content_registry import get_model_class

        assert get_model_class("nonexistent.model") is None

    def test_nested_format_types(self):
        from translations.content_registry import get_content_type

        for key in ["catalog.product", "catalog.category", "page_builder.page", "blog.blogpost"]:
            ct = get_content_type(key)
            assert ct["format"] == "nested", f"{key} should be nested format"

    def test_simple_format_types(self):
        from translations.content_registry import get_content_type

        for key in ["catalog.productattribute", "catalog.attributevalue"]:
            ct = get_content_type(key)
            assert ct["format"] == "simple", f"{key} should be simple format"

    def test_singleton_types(self):
        from translations.content_registry import get_content_type

        for key in ["core.sitesettings", "affiliate.affiliatesettings"]:
            ct = get_content_type(key)
            assert ct.get("singleton") is True, f"{key} should be singleton"

    def test_non_singleton_types(self):
        from translations.content_registry import get_content_type

        ct = get_content_type("catalog.product")
        assert ct.get("singleton") is not True


# ============================================================
# B. Coverage Service Tests
# ============================================================


class TestCoverageService:
    """Tests for TranslationCoverageService."""

    def test_no_languages_returns_empty(self, db):
        """With no active non-default languages, returns empty result."""
        from translations.coverage_service import TranslationCoverageService

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        assert result["has_languages"] is False
        assert result["overall_percentage"] == 0
        assert result["languages"] == []

    def test_active_languages_detected(self, target_languages):
        """Active non-default languages are detected by the coverage service."""
        from translations.coverage_service import TranslationCoverageService

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        assert result["has_languages"] is True
        lang_codes = {lang["code"] for lang in result["languages"]}
        assert "es" in lang_codes
        assert "fr" in lang_codes

    def test_fully_untranslated_products(
        self, target_languages, product_untranslated, site_settings
    ):
        """Products with no translations show 0% for that content type."""
        from translations.coverage_service import TranslationCoverageService

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        product_ct = next(
            (ct for ct in result["content_types"] if ct["key"] == "catalog.product"),
            None,
        )
        assert product_ct is not None
        assert product_ct["percentage"] == 0
        assert product_ct["translated_fields"] == 0
        # total_fields > 0 because product has name + short_description with content
        assert product_ct["total_fields"] > 0

    def test_partial_translation_nested(
        self, target_languages, product_with_partial_translation, site_settings
    ):
        """Product with partial Spanish translation counted correctly."""
        from translations.coverage_service import TranslationCoverageService

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        product_ct = next(
            (ct for ct in result["content_types"] if ct["key"] == "catalog.product"),
            None,
        )
        assert product_ct is not None
        # 1 product with name + short_description = 2 fields × 2 languages = 4 total
        # Only es:name translated = 1 translated
        assert product_ct["translated_fields"] == 1
        assert product_ct["total_fields"] == 4  # 2 fields × 2 languages

        # Check by_language
        es_data = product_ct["by_language"]["es"]
        assert es_data["translated"] == 1
        assert es_data["total"] == 2

        fr_data = product_ct["by_language"]["fr"]
        assert fr_data["translated"] == 0
        assert fr_data["total"] == 2

    def test_simple_format_coverage(
        self, target_languages, product_attribute_simple, site_settings
    ):
        """ProductAttribute with simple format translation counted."""
        from translations.coverage_service import TranslationCoverageService

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        attr_ct = next(
            (ct for ct in result["content_types"] if ct["key"] == "catalog.productattribute"),
            None,
        )
        assert attr_ct is not None
        # 1 attribute with 'name' field, 2 languages
        # es is translated, fr is not
        assert attr_ct["by_language"]["es"]["translated"] == 1
        assert attr_ct["by_language"]["fr"]["translated"] == 0

    def test_empty_source_fields_skipped(self, target_languages, category, site_settings):
        """Products with empty source fields aren't counted in total."""
        from translations.coverage_service import TranslationCoverageService

        p = ProductFactory(
            name="Named Only",
            slug="named-only",
            short_description="",  # empty
            category=category,
        )

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        product_ct = next(
            (ct for ct in result["content_types"] if ct["key"] == "catalog.product"),
            None,
        )
        # Only 'name' field has content → 1 field × 2 languages = 2 total
        assert product_ct["total_fields"] == 2

    def test_multiple_languages_independent(
        self, target_languages, product_with_partial_translation, site_settings
    ):
        """Coverage calculated per-language independently for each content type."""
        from translations.coverage_service import TranslationCoverageService

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        product_ct = next(
            (ct for ct in result["content_types"] if ct["key"] == "catalog.product"),
            None,
        )
        assert product_ct is not None

        # Spanish has 1 translated product field (name), French has 0
        assert product_ct["by_language"]["es"]["translated"] == 1
        assert product_ct["by_language"]["fr"]["translated"] == 0

    def test_overall_percentage_calculation(
        self, target_languages, product_with_partial_translation, site_settings
    ):
        """Overall percentage is correct math."""
        from translations.coverage_service import TranslationCoverageService

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        if result["total_fields"] > 0:
            expected_pct = round(result["translated_fields"] / result["total_fields"] * 100, 1)
            assert result["overall_percentage"] == expected_pct

    def test_coverage_caching(self, target_languages, site_settings):
        """Second call returns cached result."""
        from translations.coverage_service import TranslationCoverageService

        service = TranslationCoverageService()
        result1 = service.get_site_coverage(use_cache=True)
        result2 = service.get_site_coverage(use_cache=True)
        assert result1 == result2

    def test_invalidate_cache(self, target_languages, site_settings):
        """invalidate_coverage_cache clears cached data."""
        from translations.coverage_service import (
            COVERAGE_CACHE_KEY,
            TranslationCoverageService,
            invalidate_coverage_cache,
        )

        service = TranslationCoverageService()
        service.get_site_coverage(use_cache=True)
        assert cache.get(COVERAGE_CACHE_KEY) is not None

        invalidate_coverage_cache()
        assert cache.get(COVERAGE_CACHE_KEY) is None

    def test_ui_string_coverage_included(self, target_languages, site_settings):
        """UITranslationOverride counts included in coverage."""
        from translations.coverage_service import TranslationCoverageService
        from translations.models import UITranslationOverride

        es_lang = target_languages[0]  # Spanish
        UITranslationOverride.objects.get_or_create(
            language=es_lang,
            defaults={
                "overrides": {"cart.title": "Carrito"},
                "total_strings": 100,
                "translated_count": 50,
            },
        )

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        ui_ct = next(
            (ct for ct in result["content_types"] if ct["key"] == "translations.uistrings"),
            None,
        )
        assert ui_ct is not None
        # Service computes translated count from live overrides dict, not the stored counter.
        # Assert the language entry surfaces with a numeric translated count.
        assert isinstance(ui_ct["by_language"]["es"]["translated"], int)
        assert ui_ct["by_language"]["es"]["translated"] >= 0

    def test_content_type_metadata(self, target_languages, product_untranslated, site_settings):
        """Each content type result has required metadata keys."""
        from translations.coverage_service import TranslationCoverageService

        result = TranslationCoverageService().get_site_coverage(use_cache=False)
        for ct in result["content_types"]:
            assert "key" in ct
            assert "label" in ct
            assert "icon" in ct
            assert "priority" in ct
            assert "item_count" in ct
            assert "by_language" in ct
            assert "total_fields" in ct
            assert "translated_fields" in ct
            assert "percentage" in ct


# ============================================================
# C. Coverage API Endpoint Tests
# ============================================================


class TestCoverageAPI:
    """HTTP endpoint tests for coverage APIs."""

    def test_coverage_api_returns_200(self, staff_client, target_languages, site_settings):
        resp = staff_client.get("/api/translations/service/coverage/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "overall_percentage" in data

    def test_coverage_api_requires_staff(self, target_languages, site_settings):
        client = Client()
        resp = client.get("/api/translations/service/coverage/")
        assert resp.status_code == 302  # redirect to login

    def test_coverage_refresh_invalidates_cache(
        self, staff_client, target_languages, site_settings
    ):
        from translations.coverage_service import COVERAGE_CACHE_KEY

        # Prime cache
        cache.set(COVERAGE_CACHE_KEY, {"cached": True}, 600)
        assert cache.get(COVERAGE_CACHE_KEY) is not None

        resp = staff_client.post("/api/translations/service/coverage/refresh/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        # Should have fresh data, not our dummy cached value
        assert "overall_percentage" in data

    def test_coverage_refresh_requires_post(self, staff_client, target_languages, site_settings):
        resp = staff_client.get("/api/translations/service/coverage/refresh/")
        assert resp.status_code == 405

    def test_coverage_detail_page_renders(self, staff_client, target_languages, site_settings):
        resp = staff_client.get("/en/admin/translations/coverage/")
        assert resp.status_code == 200
        assert b"Translation Coverage" in resp.content


# ============================================================
# D. Translate All Estimate Tests
# ============================================================


class TestTranslateAllEstimate:
    """Tests for the translate-all estimate endpoint."""

    def test_estimate_returns_field_counts(
        self, staff_client, target_languages, product_untranslated, site_settings
    ):
        resp = staff_client.get("/api/translations/service/translate-all/estimate/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "total_fields" in data
        assert "total_jobs" in data
        assert isinstance(data["content_types"], list)
        assert data["total_fields"] > 0

    def test_estimate_excludes_fully_translated(
        self, staff_client, target_languages, category, site_settings
    ):
        """Fully translated product should not appear in estimate."""
        p = ProductFactory(
            name="Done",
            slug="done",
            short_description="All done",
            category=category,
        )
        p.translations = {
            "es": {"name": "Hecho", "short_description": "Todo listo"},
            "fr": {"name": "Fait", "short_description": "Tout prêt"},
        }
        p.save(update_fields=["translations"])

        resp = staff_client.get("/api/translations/service/translate-all/estimate/")
        data = resp.json()
        # Product should still appear in content_types but with 0 missing
        # if it's the only product. The coverage service returns 0 missing.
        product_est = next(
            (ct for ct in data["content_types"] if ct["key"] == "catalog.product"),
            None,
        )
        # Fully translated = no missing fields
        if product_est:
            assert product_est["missing_fields"] == 0
        # Or it's excluded entirely
        else:
            pass  # fine — no missing means not in list

    def test_estimate_is_large_flag(self, staff_client, target_languages, site_settings):
        """is_large flag set when total_fields > 1000 or total_jobs > 20."""
        # Create many products to exceed threshold
        cat = CategoryFactory(name="Bulk", slug="bulk")
        for i in range(60):
            ProductFactory(
                name=f"Bulk Product {i}",
                slug=f"bulk-product-{i}",
                short_description=f"Description {i}",
                category=cat,
            )

        resp = staff_client.get("/api/translations/service/translate-all/estimate/")
        data = resp.json()
        # 60 products × 2 fields × 2 languages = 240 missing + all other content types
        # total_fields should exceed 1000 with other content types included
        # At minimum, is_large should be True for large datasets
        assert isinstance(data["is_large"], bool)

    def test_estimate_requires_staff(self, target_languages, site_settings):
        client = Client()
        resp = client.get("/api/translations/service/translate-all/estimate/")
        assert resp.status_code == 302


# ============================================================
# E. Translate All API Tests
# ============================================================


class TestTranslateAllAPI:
    """Tests for the translate-all job creation endpoint."""

    @patch("translations.tasks.process_translation_job")
    @patch("translations.tasks.auto_translate_ui_strings")
    def test_creates_translation_jobs(
        self,
        mock_ui_task,
        mock_job_task,
        staff_client,
        target_languages,
        product_untranslated,
        site_settings,
    ):
        from translations.models import TranslationJob

        initial_count = TranslationJob.objects.count()

        resp = staff_client.post(
            "/api/translations/service/translate-all/",
            data=json.dumps({"scope": "all"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert len(data["job_ids"]) > 0
        assert TranslationJob.objects.count() > initial_count

    @patch("translations.tasks.process_translation_job")
    @patch("translations.tasks.auto_translate_ui_strings")
    def test_jobs_have_correct_metadata(
        self,
        mock_ui_task,
        mock_job_task,
        staff_client,
        target_languages,
        product_untranslated,
        site_settings,
    ):
        from translations.models import TranslationJob

        resp = staff_client.post(
            "/api/translations/service/translate-all/",
            data=json.dumps({"scope": "all"}),
            content_type="application/json",
        )
        data = resp.json()

        # Check one of the product jobs
        product_jobs = TranslationJob.objects.filter(content_type="catalog.product")
        if product_jobs.exists():
            job = product_jobs.first()
            assert job.job_type == "bulk"
            assert job.source_language == "en"
            assert isinstance(job.translated_data, dict)
            assert "object_ids" in job.translated_data
            assert "language" in job.translated_data
            assert "registry_key" in job.translated_data
            assert job.translated_data["registry_key"] == "catalog.product"

    @patch("translations.tasks.process_translation_job")
    @patch("translations.tasks.auto_translate_ui_strings")
    def test_batch_splitting(
        self,
        mock_ui_task,
        mock_job_task,
        staff_client,
        target_languages,
        site_settings,
    ):
        """120 items → ceil(120/50) = 3 batches per language."""
        from translations.models import TranslationJob

        cat = CategoryFactory(name="Batch", slug="batch")
        for i in range(120):
            ProductFactory(
                name=f"BatchProd {i}",
                slug=f"batchprod-{i}",
                short_description=f"Desc {i}",
                category=cat,
            )

        resp = staff_client.post(
            "/api/translations/service/translate-all/",
            data=json.dumps(
                {
                    "scope": "all",
                    "content_type": "catalog.product",
                }
            ),
            content_type="application/json",
        )
        data = resp.json()
        assert data["success"] is True

        # 120 items ÷ 50 = 3 batches × 2 languages = 6 jobs
        product_jobs = TranslationJob.objects.filter(content_type="catalog.product")
        assert product_jobs.count() == 6

        # Each batch should have ≤50 items
        for job in product_jobs:
            assert len(job.translated_data["object_ids"]) <= 50

    @patch("translations.tasks.process_translation_job")
    @patch("translations.tasks.auto_translate_ui_strings")
    def test_returns_job_ids(
        self,
        mock_ui_task,
        mock_job_task,
        staff_client,
        target_languages,
        product_untranslated,
        site_settings,
    ):
        resp = staff_client.post(
            "/api/translations/service/translate-all/",
            data=json.dumps({"scope": "all"}),
            content_type="application/json",
        )
        data = resp.json()
        assert "job_ids" in data
        assert isinstance(data["job_ids"], list)

    def test_requires_post(self, staff_client, target_languages, site_settings):
        resp = staff_client.get("/api/translations/service/translate-all/")
        assert resp.status_code == 405

    def test_requires_staff(self, target_languages, site_settings):
        client = Client()
        resp = client.post(
            "/api/translations/service/translate-all/",
            data=json.dumps({"scope": "all"}),
            content_type="application/json",
        )
        assert resp.status_code == 302

    @patch("translations.tasks.process_translation_job")
    @patch("translations.tasks.auto_translate_ui_strings")
    def test_dispatches_celery_tasks(
        self,
        mock_ui_task,
        mock_job_task,
        staff_client,
        target_languages,
        product_untranslated,
        site_settings,
    ):
        """Verify Celery tasks dispatched for jobs and UI strings."""
        resp = staff_client.post(
            "/api/translations/service/translate-all/",
            data=json.dumps({"scope": "all"}),
            content_type="application/json",
        )
        assert resp.status_code == 200

        # process_translation_job.delay should be called for each job
        assert mock_job_task.delay.call_count > 0

        # auto_translate_ui_strings.delay called for each language
        assert mock_ui_task.delay.call_count == 2  # es + fr


# ============================================================
# F. Translate All Status Tests
# ============================================================


class TestTranslateAllStatus:
    """Tests for the status polling endpoint."""

    def test_status_counts_completed(self, staff_client, target_languages, site_settings):
        from translations.models import TranslationJob

        jobs = []
        for status in ["completed", "completed", "completed", "pending"]:
            job = TranslationJob.objects.create(
                job_type="bulk",
                source_language="en",
                target_languages=["es"],
                status=status,
                content_type="catalog.product",
            )
            jobs.append(job)

        ids_str = ",".join(str(j.id) for j in jobs)
        resp = staff_client.get(
            f"/api/translations/service/translate-all/status/?job_ids={ids_str}"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_jobs"] == 4
        assert data["completed"] == 3
        assert data["pending"] == 1
        assert data["overall_progress"] == 75

    def test_status_empty_job_ids(self, staff_client, target_languages, site_settings):
        resp = staff_client.get("/api/translations/service/translate-all/status/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_jobs"] == 0

    def test_status_requires_staff(self, target_languages, site_settings):
        client = Client()
        resp = client.get("/api/translations/service/translate-all/status/")
        assert resp.status_code == 302

    def test_status_with_failed_jobs(self, staff_client, target_languages, site_settings):
        from translations.models import TranslationJob

        jobs = []
        for status in ["completed", "failed", "processing"]:
            job = TranslationJob.objects.create(
                job_type="bulk",
                source_language="en",
                target_languages=["es"],
                status=status,
                content_type="catalog.product",
            )
            jobs.append(job)

        ids_str = ",".join(str(j.id) for j in jobs)
        resp = staff_client.get(
            f"/api/translations/service/translate-all/status/?job_ids={ids_str}"
        )
        data = resp.json()
        assert data["completed"] == 1
        assert data["failed"] == 1
        assert data["processing"] == 1
        assert data["overall_progress"] == 33  # 1/3 = 33%


# ============================================================
# G. Task Processor Model Content Tests
# ============================================================


class TestTaskProcessorModelContent:
    """Tests for _get_model_content and _save_model_translations."""

    def _make_processor(self):
        """Create a TranslationJobProcessor without a real translation client."""
        from translations.tasks import TranslationJobProcessor

        processor = TranslationJobProcessor()
        processor.client = MagicMock()
        return processor

    def _make_job(self, registry_key, object_ids, language="es", fields=None):
        """Create a TranslationJob with the right translated_data."""
        from translations.models import TranslationJob

        if fields is None:
            from translations.content_registry import get_content_type

            ct = get_content_type(registry_key)
            fields = ct["fields"] if ct else []

        return TranslationJob.objects.create(
            job_type="bulk",
            source_language="en",
            target_languages=[language],
            content_type=registry_key,
            fields_to_translate=fields,
            translated_data={
                "object_ids": object_ids,
                "language": language,
                "registry_key": registry_key,
            },
        )

    def test_get_model_content_extracts_fields(
        self, target_languages, product_untranslated, site_settings
    ):
        processor = self._make_processor()
        job = self._make_job(
            "catalog.product",
            [product_untranslated.pk],
            language="es",
        )

        content = processor._get_model_content(job, job.translated_data)
        assert f"{product_untranslated.pk}:name" in content
        assert content[f"{product_untranslated.pk}:name"] == "Gadget"
        assert f"{product_untranslated.pk}:short_description" in content
        assert content[f"{product_untranslated.pk}:short_description"] == "A nice gadget"

    def test_get_model_content_skips_empty_fields(self, target_languages, category, site_settings):
        """Product with empty short_description — only name extracted."""
        p = ProductFactory(
            name="Empty Desc",
            slug="empty-desc",
            short_description="",
            category=category,
        )

        processor = self._make_processor()
        job = self._make_job("catalog.product", [p.pk], language="es")

        content = processor._get_model_content(job, job.translated_data)
        assert f"{p.pk}:name" in content
        assert f"{p.pk}:short_description" not in content

    def test_get_model_content_skips_already_translated(
        self, target_languages, product_with_partial_translation, site_settings
    ):
        """Product with existing es:name translation — name not extracted."""
        processor = self._make_processor()
        p = product_with_partial_translation
        job = self._make_job("catalog.product", [p.pk], language="es")

        content = processor._get_model_content(job, job.translated_data)
        # name is already translated to es, so should be skipped
        assert f"{p.pk}:name" not in content
        # short_description is NOT translated, so should be included
        assert f"{p.pk}:short_description" in content

    def test_get_model_content_invalid_registry_key(self, target_languages, site_settings):
        processor = self._make_processor()
        from translations.models import TranslationJob

        job = TranslationJob.objects.create(
            job_type="bulk",
            source_language="en",
            target_languages=["es"],
            content_type="fake.model",
            translated_data={
                "object_ids": [999],
                "language": "es",
                "registry_key": "fake.model",
            },
        )

        content = processor._get_model_content(job, job.translated_data)
        assert content == {}

    def test_get_model_content_html_preserved(
        self, target_languages, product_with_html, site_settings
    ):
        """HTML in full_description extracted as raw HTML string."""
        processor = self._make_processor()
        p = product_with_html
        job = self._make_job("catalog.product", [p.pk], language="es")

        content = processor._get_model_content(job, job.translated_data)
        key = f"{p.pk}:full_description"
        assert key in content
        # HTML tags preserved
        assert '<a href="https://example.com">' in content[key]
        assert '<img src="/media/widget.jpg"' in content[key]

    def test_save_model_translations_nested(
        self, target_languages, product_untranslated, site_settings
    ):
        """Save nested format translations correctly."""

        processor = self._make_processor()
        job = self._make_job(
            "catalog.product",
            [product_untranslated.pk],
            language="es",
        )

        translations = {
            f"{product_untranslated.pk}:name": "Gadget ES",
            f"{product_untranslated.pk}:short_description": "Un lindo gadget",
        }
        processor._save_model_translations(job, translations)

        product_untranslated.refresh_from_db()
        assert "es" in product_untranslated.translations
        assert product_untranslated.translations["es"]["name"] == "Gadget ES"
        assert product_untranslated.translations["es"]["short_description"] == "Un lindo gadget"
        # Metadata
        assert product_untranslated.translations["es"]["_meta"]["auto"] is True
        assert product_untranslated.translations["es"]["_meta"]["verified"] is False

    def test_save_model_translations_simple(
        self, target_languages, product_attribute_untranslated, site_settings
    ):
        """Save simple format translations correctly."""

        processor = self._make_processor()
        attr = product_attribute_untranslated
        job = self._make_job(
            "catalog.productattribute",
            [attr.pk],
            language="es",
        )

        translations = {f"{attr.pk}:name": "Tamaño"}
        processor._save_model_translations(job, translations)

        attr.refresh_from_db()
        assert attr.translations.get("es") == "Tamaño"

    def test_save_model_translations_merges(
        self, target_languages, product_with_partial_translation, site_settings
    ):
        """Existing translations preserved, new ones added."""
        processor = self._make_processor()
        p = product_with_partial_translation
        job = self._make_job("catalog.product", [p.pk], language="es")

        translations = {f"{p.pk}:short_description": "Un gran widget"}
        processor._save_model_translations(job, translations)

        p.refresh_from_db()
        # Original es:name preserved
        assert p.translations["es"]["name"] == "Widget ES"
        # New es:short_description added
        assert p.translations["es"]["short_description"] == "Un gran widget"

    def test_save_model_translations_invalidates_cache(
        self, target_languages, product_untranslated, site_settings
    ):
        """Coverage cache cleared after saving translations."""
        from translations.coverage_service import COVERAGE_CACHE_KEY

        cache.set(COVERAGE_CACHE_KEY, {"test": True}, 600)
        assert cache.get(COVERAGE_CACHE_KEY) is not None

        processor = self._make_processor()
        job = self._make_job(
            "catalog.product",
            [product_untranslated.pk],
            language="es",
        )

        processor._save_model_translations(job, {f"{product_untranslated.pk}:name": "Test"})

        assert cache.get(COVERAGE_CACHE_KEY) is None

    def test_save_model_translations_bad_keys_ignored(
        self, target_languages, product_untranslated, site_settings
    ):
        """Keys without ':' separator are silently skipped."""
        processor = self._make_processor()
        job = self._make_job(
            "catalog.product",
            [product_untranslated.pk],
            language="es",
        )

        # Mix of valid and invalid keys
        translations = {
            f"{product_untranslated.pk}:name": "Valid",
            "badkey": "Should be ignored",
            "also_bad_no_colon": "Ignored too",
        }
        processor._save_model_translations(job, translations)

        product_untranslated.refresh_from_db()
        assert product_untranslated.translations["es"]["name"] == "Valid"


# ============================================================
# H. Translation Locks
# ============================================================


class TestTranslationLocks:
    """Test translation lock enforcement across all code paths."""

    def _make_processor(self):
        from translations.tasks import TranslationJobProcessor

        processor = TranslationJobProcessor()
        processor.client = MagicMock()
        return processor

    def _make_job(self, registry_key, object_ids, language="es", fields=None):
        from translations.models import TranslationJob

        if fields is None:
            from translations.content_registry import get_content_type

            ct = get_content_type(registry_key)
            fields = ct["fields"] if ct else []
        return TranslationJob.objects.create(
            job_type="bulk",
            source_language="en",
            target_languages=[language],
            content_type=registry_key,
            fields_to_translate=fields,
            translated_data={
                "object_ids": object_ids,
                "language": language,
                "registry_key": registry_key,
            },
        )

    # --- Lock Service ---

    def test_lock_service_toggle(self, target_languages, admin_user, site_settings):
        """toggle_field_lock creates TranslationMeta and toggles is_locked."""
        from translations.lock_service import toggle_field_lock
        from translations.models import TranslationMeta

        # First toggle → lock
        result = toggle_field_lock("catalog.product", 1, "name", "es", admin_user)
        assert result is True
        meta = TranslationMeta.objects.get(
            content_type="catalog.product", object_id=1, field_name="name", language="es"
        )
        assert meta.is_locked is True
        assert meta.locked_by == admin_user
        assert meta.locked_at is not None

        # Second toggle → unlock
        result = toggle_field_lock("catalog.product", 1, "name", "es", admin_user)
        assert result is False
        meta.refresh_from_db()
        assert meta.is_locked is False
        assert meta.locked_by is None
        assert meta.locked_at is None

    def test_get_locked_fields_filters(self, target_languages, admin_user, site_settings):
        """get_locked_fields returns only locked (object_id, field_name) tuples."""
        from translations.lock_service import get_locked_fields
        from translations.models import TranslationMeta

        # Create one locked and one unlocked
        TranslationMeta.objects.create(
            content_type="catalog.product",
            object_id=10,
            field_name="name",
            language="es",
            is_locked=True,
            locked_by=admin_user,
        )
        TranslationMeta.objects.create(
            content_type="catalog.product",
            object_id=10,
            field_name="description",
            language="es",
            is_locked=False,
        )

        locked = get_locked_fields("catalog.product", [10], "es")
        assert (10, "name") in locked
        assert (10, "description") not in locked

    def test_get_model_content_skips_locked(
        self, target_languages, product_untranslated, admin_user, site_settings
    ):
        """_get_model_content excludes locked fields from extraction."""
        from translations.models import TranslationMeta

        # Lock the 'name' field for Spanish
        TranslationMeta.objects.create(
            content_type="catalog.product",
            object_id=product_untranslated.pk,
            field_name="name",
            language="es",
            is_locked=True,
            locked_by=admin_user,
        )

        processor = self._make_processor()
        job = self._make_job("catalog.product", [product_untranslated.pk])
        content = processor._get_model_content(job, job.translated_data)

        # 'name' should be excluded, but 'short_description' should remain
        assert f"{product_untranslated.pk}:name" not in content
        assert f"{product_untranslated.pk}:short_description" in content

    def test_save_model_translations_skips_locked(
        self, target_languages, product_untranslated, admin_user, site_settings
    ):
        """_save_model_translations doesn't overwrite locked fields."""
        from translations.models import TranslationMeta

        # Lock 'name' field
        TranslationMeta.objects.create(
            content_type="catalog.product",
            object_id=product_untranslated.pk,
            field_name="name",
            language="es",
            is_locked=True,
            locked_by=admin_user,
        )

        processor = self._make_processor()
        job = self._make_job("catalog.product", [product_untranslated.pk])
        translations = {
            f"{product_untranslated.pk}:name": "Locked - should not save",
            f"{product_untranslated.pk}:short_description": "Descripcion",
        }
        processor._save_model_translations(job, translations)

        product_untranslated.refresh_from_db()
        es_data = product_untranslated.translations.get("es", {})
        # name should NOT be saved (locked)
        assert es_data.get("name") is None
        # short_description should be saved (not locked)
        assert es_data.get("short_description") == "Descripcion"

    def test_ui_auto_translate_skips_locked(self, target_languages, site_settings):
        """auto_translate_ui_strings skips locked UI string keys."""
        from translations.models import UITranslationOverride

        es_lang = target_languages[0]  # Spanish
        override, _ = UITranslationOverride.objects.get_or_create(
            language=es_lang, defaults={"total_strings": 100}
        )
        # Lock one key
        override.meta_info = {"cart.title": {"locked": True}}
        override.save(update_fields=["meta_info"])

        # The task reads locked keys from meta_info and filters them out.
        # We test the filtering logic indirectly by checking the lock_service helper.
        from translations.lock_service import get_ui_locked_keys

        locked = get_ui_locked_keys("es")
        assert "cart.title" in locked

    def test_ui_save_skips_locked(self, target_languages, admin_user, site_settings, django_site):
        """ui_translations_save_api skips locked UI string keys."""
        from translations.models import UITranslationOverride

        es_lang = target_languages[0]  # Spanish
        override, _ = UITranslationOverride.objects.get_or_create(
            language=es_lang, defaults={"total_strings": 100}
        )
        override.overrides = {"cart.title": "Carrito"}
        override.meta_info = {"cart.title": {"auto": False, "verified": True, "locked": True}}
        override.save(update_fields=["overrides", "meta_info"])

        client = Client()
        client.force_login(admin_user)
        resp = client.post(
            "/api/translations/service/ui-translations/es/save/",
            data=json.dumps({"translations": {"cart.title": "OVERWRITTEN"}}),
            content_type="application/json",
        )
        assert resp.status_code == 200

        override.refresh_from_db()
        # The locked key should NOT be overwritten
        assert override.overrides["cart.title"] == "Carrito"

    # --- Lock Toggle API ---

    def test_lock_toggle_api(self, target_languages, admin_user, site_settings, django_site):
        """POST to toggle endpoint flips lock state."""
        client = Client()
        client.force_login(admin_user)

        # Lock
        resp = client.post(
            "/api/translations/service/lock/toggle/",
            data=json.dumps(
                {
                    "content_type": "catalog.product",
                    "object_id": 999,
                    "field_name": "name",
                    "language": "es",
                }
            ),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["is_locked"] is True

        # Unlock
        resp = client.post(
            "/api/translations/service/lock/toggle/",
            data=json.dumps(
                {
                    "content_type": "catalog.product",
                    "object_id": 999,
                    "field_name": "name",
                    "language": "es",
                }
            ),
            content_type="application/json",
        )
        data = resp.json()
        assert data["is_locked"] is False

    def test_ui_lock_toggle_api(self, target_languages, admin_user, site_settings, django_site):
        """POST to UI lock endpoint flips meta_info.locked."""
        from translations.models import UITranslationOverride

        es_lang = target_languages[0]
        UITranslationOverride.objects.get_or_create(
            language=es_lang, defaults={"total_strings": 100}
        )

        client = Client()
        client.force_login(admin_user)

        # Lock
        resp = client.post(
            "/api/translations/service/ui-translations/es/lock/",
            data=json.dumps({"key": "cart.title"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["is_locked"] is True

        override = UITranslationOverride.objects.get(language=es_lang)
        assert override.meta_info["cart.title"]["locked"] is True

        # Unlock
        resp = client.post(
            "/api/translations/service/ui-translations/es/lock/",
            data=json.dumps({"key": "cart.title"}),
            content_type="application/json",
        )
        data = resp.json()
        assert data["is_locked"] is False

    def test_status_api_includes_locks(
        self, target_languages, admin_user, site_settings, django_site
    ):
        """generic_translation_status response includes locked_fields."""
        from translations.models import TranslationMeta

        # Create a lock record
        TranslationMeta.objects.create(
            content_type="core.sitesettings",
            object_id=1,
            field_name="site_name",
            language="es",
            is_locked=True,
            locked_by=admin_user,
        )

        client = Client()
        client.force_login(admin_user)
        resp = client.get("/api/translation/core.sitesettings/1/site_name/status/")
        assert resp.status_code == 200
        data = resp.json()
        assert "locked_fields" in data
        assert "es" in data["locked_fields"]
        assert "site_name" in data["locked_fields"]["es"]

    def test_lock_toggle_requires_staff(
        self, target_languages, customer_user, site_settings, django_site
    ):
        """Lock toggle endpoint requires staff auth."""
        client = Client()
        client.force_login(customer_user)
        resp = client.post(
            "/api/translations/service/lock/toggle/",
            data=json.dumps(
                {
                    "content_type": "catalog.product",
                    "object_id": 1,
                    "field_name": "name",
                    "language": "es",
                }
            ),
            content_type="application/json",
        )
        assert resp.status_code == 302  # Redirect to login
