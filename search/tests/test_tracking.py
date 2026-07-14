"""
Search tracking tests.

Covers:
  - SearchResultsAPIView returns `search_query_id` in the response so
    headless frontends can attribute clicks to the originating search.
  - SearchService.track_click accepts a bare model name for content_type
    (in addition to the existing "app_label.model" form) so headless
    callers don't need to know Django app labels.
  - Track-click integration end-to-end via POST /api/search/click/.
"""

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from search.models import (
    SearchClick,
    SearchEngine,
    SearchQuery,
    SearchSettings,
)
from search.services.search_service import SearchService

User = get_user_model()


def _ensure_site_and_settings():
    """Ensure Django Site, SiteSettings, SearchSettings, and a search engine exist."""
    Site.objects.get_or_create(pk=1, defaults={"domain": "testserver", "name": "Test"})
    from core.models import SiteSettings as CoreSiteSettings

    if not CoreSiteSettings.objects.filter(pk=1).exists():
        CoreSiteSettings.objects.create(
            pk=1,
            site_name="Test Store",
            admin_email="test@test.spwig.com",
            default_currency="USD",
        )
    # Search settings singleton — force tracking enabled (prior runs may have
    # left state with tracking disabled when using --keepdb).
    settings = SearchSettings.get_settings()
    settings.track_search_queries = True
    settings.track_clicks = True
    settings.save()
    # At least one active engine slugged 'shop'
    SearchEngine.objects.get_or_create(
        slug="shop",
        defaults={"name": "Shop Search", "is_active": True, "content_types": ["product"]},
    )


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class TrackQueryReturnValueTest(TestCase):
    """SearchService.track_query returns the created SearchQuery instance."""

    def setUp(self):
        _ensure_site_and_settings()

    def test_track_query_returns_search_query_instance(self):
        service = SearchService()
        sq = service.track_query(
            query="vitamin c serum",
            result_count=12,
            language="en",
            engine_slug="shop",
            response_time_ms=45,
            user=None,
            session_key="test-session-abc",
        )
        self.assertIsInstance(sq, SearchQuery)
        self.assertIsNotNone(sq.id)
        self.assertEqual(sq.query, "vitamin c serum")
        self.assertEqual(sq.result_count, 12)
        self.assertEqual(sq.session_key, "test-session-abc")

    def test_track_query_returns_none_when_tracking_disabled(self):
        settings = SearchSettings.get_settings()
        settings.track_search_queries = False
        settings.save()
        service = SearchService()
        sq = service.track_query(
            query="anything",
            result_count=5,
        )
        self.assertIsNone(sq)


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class TrackClickContentTypeLenienceTest(TestCase):
    """track_click accepts bare model name OR 'app_label.model'."""

    def setUp(self):
        _ensure_site_and_settings()
        self.service = SearchService()
        self.search_query = self.service.track_query(
            query="serum",
            result_count=3,
            session_key="sess-1",
        )
        self.assertIsNotNone(self.search_query)

    def test_track_click_accepts_bare_model_name(self):
        """Bare 'product' should resolve to catalog.Product ContentType."""
        ok = self.service.track_click(
            search_query_id=self.search_query.id,
            content_type_str="product",
            object_id=999,
            position=0,
            session_key="sess-1",
        )
        self.assertTrue(ok)
        click = SearchClick.objects.filter(search_query=self.search_query).first()
        self.assertIsNotNone(click)
        self.assertEqual(click.content_type.model, "product")
        self.assertEqual(click.object_id, 999)
        self.assertEqual(click.position, 0)

    def test_track_click_accepts_app_label_model_form(self):
        ok = self.service.track_click(
            search_query_id=self.search_query.id,
            content_type_str="catalog.product",
            object_id=1234,
            position=2,
            session_key="sess-1",
        )
        self.assertTrue(ok)
        click = SearchClick.objects.filter(
            search_query=self.search_query,
            object_id=1234,
        ).first()
        self.assertIsNotNone(click)
        self.assertEqual(click.content_type.model, "product")
        self.assertEqual(click.position, 2)

    def test_track_click_returns_false_for_unknown_model(self):
        ok = self.service.track_click(
            search_query_id=self.search_query.id,
            content_type_str="definitely_not_a_model",
            object_id=1,
        )
        self.assertFalse(ok)
        # No click row created
        self.assertEqual(
            SearchClick.objects.filter(
                search_query=self.search_query,
                object_id=1,
            ).count(),
            0,
        )

    def test_track_click_returns_false_for_unknown_search_query(self):
        ok = self.service.track_click(
            search_query_id=999999,
            content_type_str="product",
            object_id=1,
        )
        self.assertFalse(ok)


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class SearchResultsApiReturnsQueryIdTest(TestCase):
    """GET /api/search/results/ should expose search_query_id in response."""

    def setUp(self):
        _ensure_site_and_settings()
        self.client = APIClient()

    def test_response_includes_search_query_id(self):
        resp = self.client.get("/api/search/results/", {"q": "serum"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_query_id", resp.data)
        # A SearchQuery row with that id must exist
        qid = resp.data["search_query_id"]
        self.assertIsNotNone(qid)
        self.assertTrue(SearchQuery.objects.filter(pk=qid).exists())

    def test_empty_query_returns_no_search_query_id(self):
        """Empty queries short-circuit before tracking — no ID should be returned."""
        resp = self.client.get("/api/search/results/", {"q": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("search_query_id", resp.data)

    def test_disabled_tracking_returns_no_query_id(self):
        settings = SearchSettings.get_settings()
        settings.track_search_queries = False
        settings.save()
        resp = self.client.get("/api/search/results/", {"q": "serum"})
        self.assertEqual(resp.status_code, 200)
        # search_query_id should be absent when tracking is off
        self.assertNotIn("search_query_id", resp.data)

    def test_disabled_tracking_does_not_create_session(self):
        """When tracking is disabled, the view must not save a new session
        — otherwise a botnet could flood the django_session table by
        pumping search queries even with tracking off."""
        from django.contrib.sessions.models import Session

        settings = SearchSettings.get_settings()
        settings.track_search_queries = False
        settings.save()

        session_count_before = Session.objects.count()
        resp = self.client.get("/api/search/results/", {"q": "serum"})
        self.assertEqual(resp.status_code, 200)
        # No new session row should have been created
        self.assertEqual(Session.objects.count(), session_count_before)

    def test_short_query_below_min_length_is_rejected(self):
        """Queries below SearchSettings.min_query_length must be rejected
        before any tracking or DB work — to prevent search_query / session
        table flooding via short-query spam."""
        settings = SearchSettings.get_settings()
        settings.min_query_length = 2
        settings.save()

        # 1-char query is below the minimum
        resp = self.client.get("/api/search/results/", {"q": "a"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total_count"], 0)
        self.assertNotIn("search_query_id", resp.data)
        # No SearchQuery row created
        self.assertFalse(SearchQuery.objects.filter(query="a").exists())

        # 2-char query meets the minimum
        resp = self.client.get("/api/search/results/", {"q": "ab"})
        self.assertEqual(resp.status_code, 200)
        # search_query_id should be present for queries that hit the tracker
        self.assertIn("search_query_id", resp.data)


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class TrackClickApiEndpointTest(TestCase):
    """POST /api/search/click/ accepts bare model names."""

    def setUp(self):
        _ensure_site_and_settings()
        self.client = APIClient()
        service = SearchService()
        self.search_query = service.track_query(query="serum", result_count=1)

    def test_click_with_bare_model_name_succeeds(self):
        resp = self.client.post(
            "/api/search/click/",
            {
                "search_query_id": self.search_query.id,
                "content_type": "product",
                "object_id": 42,
                "position": 0,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get("success"))
        self.assertEqual(
            SearchClick.objects.filter(
                search_query=self.search_query,
                object_id=42,
            ).count(),
            1,
        )

    def test_click_with_missing_fields_is_rejected(self):
        resp = self.client.post(
            "/api/search/click/",
            {"search_query_id": self.search_query.id},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
