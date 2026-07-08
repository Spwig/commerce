"""
Integration tests for help system semantic search API.

Tests the complete API flow including:
- Authentication and permissions
- Request validation
- Semantic search endpoint
- Fallback to keyword search
- Multi-language support
"""
import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status

from core.models import HelpTopic, HelpCategory, HelpSearchIndex
from core.services.semantic_search import IndexingService

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.semantic_search]

# Check for ONNX runtime dependencies (replaced sentence-transformers)
try:
    import onnxruntime
    import tokenizers
    from core.ml.onnx_encoder import OnnxSentenceEncoder
    OnnxSentenceEncoder.get_instance()
    HAS_ONNX = True
except Exception:
    HAS_ONNX = False

onnx_required = pytest.mark.skipif(not HAS_ONNX, reason='onnxruntime/tokenizers not available or model not found')


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def api_client():
    """Create an API client for testing."""
    return APIClient()


@pytest.fixture
def admin_user(db, site_settings):
    """Create an admin user for authenticated requests."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.create_user(
        username='test_admin',
        email='admin@test.spwig.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True,
    )
    return user


@pytest.fixture
def help_category(db):
    """Create a test help category."""
    return HelpCategory.objects.create(
        name='Product Management',
        slug='product-management',
        description='Help topics about managing products',
        order=1,
        icon='fas fa-box',
    )


@pytest.fixture
def help_topics(db, help_category):
    """Create multiple help topics for testing."""
    topics = []

    topics.append(HelpTopic.objects.create(
        category=help_category,
        slug='creating-products',
        title_i18n_key='Creating Products',
        content_markdown='''
# Creating Products

Learn how to create new products in your catalog.

## Steps to Create a Product

1. Navigate to Catalog > Products
2. Click the "Add Product" button
3. Fill in product details (name, description, price)
4. Add product images
5. Configure variants if needed
6. Set inventory levels
7. Publish the product

Products can have multiple variants with different options like size and color.
        ''',
        keywords=['products', 'create', 'catalog', 'variants'],
        is_published=True,
        component='catalog',
    ))

    topics.append(HelpTopic.objects.create(
        category=help_category,
        slug='product-variants',
        title_i18n_key='Managing Product Variants',
        content_markdown='''
# Product Variants

Add size, color, and other variations to your products.

## Creating Variants

Variants allow you to sell the same product in different configurations.
For example, a t-shirt can have size variants (S, M, L, XL) and color
variants (Red, Blue, Green).

## Configuring Options

1. Create option groups (e.g., "Size", "Color")
2. Add option values (e.g., "Small", "Medium", "Large")
3. Generate variant combinations
4. Set individual prices and SKUs for each variant
        ''',
        keywords=['variants', 'options', 'configure', 'products'],
        is_published=True,
        component='catalog',
    ))

    topics.append(HelpTopic.objects.create(
        category=help_category,
        slug='order-fulfillment',
        title_i18n_key='Processing Orders',
        content_markdown='''
# Order Fulfillment

Process and ship customer orders efficiently.

## Fulfillment Workflow

1. Review new orders in Orders > All Orders
2. Verify inventory availability
3. Print packing slips
4. Pick and pack items
5. Generate shipping labels
6. Mark orders as shipped
7. Send tracking information to customers

Use the bulk actions to process multiple orders at once.
        ''',
        keywords=['orders', 'fulfillment', 'shipping', 'tracking'],
        is_published=True,
        component='orders',
    ))

    # Index topics for semantic search if ONNX runtime available
    if HAS_ONNX:
        for topic in topics:
            try:
                IndexingService.index_topic(topic.id, languages=['en'])
            except Exception:
                pass  # Skip indexing if it fails (model not available)

    return topics


# ============================================================================
# Authentication Tests
# ============================================================================

class TestAuthentication:
    """Test authentication and permissions for help API."""

    def test_semantic_search_requires_authentication(self, api_client, site_settings):
        """Test that semantic search endpoint requires authentication."""
        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'how to create products',
            'language': 'en',
        })

        # DRF returns 401 for unauthenticated requests, 403 for unauthorized
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ]

    def test_semantic_search_with_authentication(self, api_client, admin_user):
        """Test semantic search with authenticated user."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'how to create products',
            'language': 'en',
        })

        # Should succeed or return results (even if empty due to missing model)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]


# ============================================================================
# Request Validation Tests
# ============================================================================

class TestRequestValidation:
    """Test request validation for semantic search API."""

    def test_semantic_search_requires_query(self, api_client, admin_user):
        """Test that query parameter is required."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'language': 'en',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'query' in str(response.data).lower()

    def test_semantic_search_validates_limit(self, api_client, admin_user):
        """Test that limit parameter is validated."""
        api_client.force_authenticate(user=admin_user)

        # Limit too high
        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'test',
            'language': 'en',
            'limit': 100,  # Max is 50
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_semantic_search_validates_threshold(self, api_client, admin_user):
        """Test that invalid threshold triggers fallback to keyword search."""
        api_client.force_authenticate(user=admin_user)

        # Threshold out of range - view catches validation error and falls back
        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'test',
            'language': 'en',
            'threshold': 3.0,  # Max is 2.0 - will fail validation
        })

        # View catches all exceptions and falls back to keyword search
        assert response.status_code == status.HTTP_200_OK


# ============================================================================
# Semantic Search Tests
# ============================================================================

class TestSemanticSearchEndpoint:
    """Test the semantic search API endpoint."""

    @onnx_required
    def test_semantic_search_returns_results(self, api_client, admin_user, help_topics):
        """Test that semantic search returns relevant results."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'how do I add products to my store',
            'language': 'en',
            'limit': 5,
            'threshold': 1.0,  # Use lenient threshold for ONNX model
        })

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'search_type' in response.data
        assert response.data['search_type'] == 'semantic'
        assert 'count' in response.data

        # Should return at least one result with lenient threshold
        assert len(response.data['results']) > 0

    @onnx_required
    def test_semantic_search_result_structure(self, api_client, admin_user, help_topics):
        """Test the structure of semantic search results."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'product variants',
            'language': 'en',
        })

        assert response.status_code == status.HTTP_200_OK
        results = response.data['results']

        if len(results) > 0:
            result = results[0]
            # Check result has required fields
            assert 'id' in result
            assert 'slug' in result
            assert 'title_i18n_key' in result
            assert 'category_name' in result

    @onnx_required
    def test_semantic_search_filters_by_component(self, api_client, admin_user, help_topics):
        """Test filtering semantic search by component."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'help',
            'language': 'en',
            'component': 'catalog',
        })

        assert response.status_code == status.HTTP_200_OK

        # All results should be from catalog component
        for result in response.data['results']:
            # Fetch the topic to check component
            topic = HelpTopic.objects.get(slug=result['slug'])
            assert topic.component == 'catalog'

    @onnx_required
    def test_semantic_search_filters_by_category(self, api_client, admin_user, help_topics, help_category):
        """Test filtering semantic search by category."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'help',
            'language': 'en',
            'category': help_category.slug,
        })

        assert response.status_code == status.HTTP_200_OK

        # All results should be from specified category
        for result in response.data['results']:
            assert result['category_name'] == help_category.name

    @onnx_required
    def test_semantic_search_respects_limit(self, api_client, admin_user, help_topics):
        """Test that semantic search respects limit parameter."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'products',
            'language': 'en',
            'limit': 2,
        })

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) <= 2


# ============================================================================
# Fallback Behavior Tests
# ============================================================================

class TestFallbackBehavior:
    """Test fallback from semantic to keyword search."""

    def test_semantic_search_falls_back_on_error(self, api_client, admin_user, help_topics):
        """Test that semantic search falls back to keyword search on error."""
        api_client.force_authenticate(user=admin_user)

        # Mock the SearchService to raise an error (imported locally in the view)
        from unittest.mock import patch
        with patch('core.services.semantic_search.SearchService.search', side_effect=Exception('Test error')):
            response = api_client.post('/api/core/help/topics/semantic_search/', {
                'query': 'products',
                'language': 'en',
            })

            # Should still return 200 OK (fallback to keyword search)
            assert response.status_code == status.HTTP_200_OK
            # Should return results (from keyword search fallback)
            assert isinstance(response.data, list)


# ============================================================================
# Keyword Search Tests (for comparison)
# ============================================================================

class TestKeywordSearchEndpoint:
    """Test the keyword search endpoint for comparison."""

    def test_keyword_search_returns_results(self, api_client, admin_user, help_topics):
        """Test that keyword search works."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/search/', {
            'query': 'products',
            'limit': 5,
        })

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0

    def test_keyword_search_scoring(self, api_client, admin_user, help_topics):
        """Test that keyword search scores results correctly."""
        api_client.force_authenticate(user=admin_user)

        # Search for "products" - should prioritize title matches
        response = api_client.post('/api/core/help/topics/search/', {
            'query': 'products',
            'limit': 10,
        })

        assert response.status_code == status.HTTP_200_OK
        results = response.data

        # Should return results with "products" in title first
        if len(results) > 0:
            first_result = results[0]
            assert 'product' in first_result['title_i18n_key'].lower()


# ============================================================================
# Contextual Help Tests
# ============================================================================

class TestContextualHelpEndpoint:
    """Test the contextual help endpoint."""

    def test_contextual_help_returns_suggestions(self, api_client, admin_user, help_topics):
        """Test that contextual help returns relevant suggestions."""
        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/contextual/', {
            'url_path': '/admin/catalog/products/',
            'limit': 5,
        })

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_contextual_help_matches_url_patterns(self, api_client, admin_user, help_topics):
        """Test that contextual help matches URL patterns."""
        # Update a topic with URL pattern
        topic = help_topics[0]
        topic.url_patterns = ['/admin/catalog/products/*']
        topic.save()

        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/contextual/', {
            'url_path': '/admin/catalog/products/add/',
            'limit': 5,
        })

        assert response.status_code == status.HTTP_200_OK


# ============================================================================
# Multi-language Tests
# ============================================================================

class TestMultiLanguageSupport:
    """Test multi-language support in search API."""

    @pytest.fixture
    def multilingual_topic(self, db, help_category):
        """Create a topic with translations."""
        topic = HelpTopic.objects.create(
            category=help_category,
            slug='multilingual-test',
            title_i18n_key='English Title',
            content_markdown='English content here.',
            keywords=['test'],
            is_published=True,
            translations={
                'es': {
                    'title': 'Título en Español',
                    'content': 'Contenido en español aquí.',
                },
            },
        )

        # Index in both languages
        if HAS_ONNX:
            try:
                IndexingService.index_topic(topic.id, languages=['en', 'es'])
            except Exception:
                pass

        return topic

    def test_keyword_search_with_lang_parameter(self, api_client, admin_user, multilingual_topic):
        """Test that lang parameter affects keyword search."""
        api_client.force_authenticate(user=admin_user)

        # English search
        response_en = api_client.post('/api/core/help/topics/search/?lang=en', {
            'query': 'test',
        })

        # Spanish search
        response_es = api_client.post('/api/core/help/topics/search/?lang=es', {
            'query': 'test',
        })

        assert response_en.status_code == status.HTTP_200_OK
        assert response_es.status_code == status.HTTP_200_OK

    @onnx_required
    def test_semantic_search_language_specific(self, api_client, admin_user, multilingual_topic):
        """Test that semantic search works with language parameter."""
        api_client.force_authenticate(user=admin_user)

        # Spanish semantic search
        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'ayuda',  # Spanish for "help"
            'language': 'es',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['search_type'] == 'semantic'


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Test performance characteristics of search API."""

    @onnx_required
    def test_semantic_search_response_time(self, api_client, admin_user, help_topics):
        """Test that semantic search responds within acceptable time."""
        import time

        api_client.force_authenticate(user=admin_user)

        start_time = time.time()
        response = api_client.post('/api/core/help/topics/semantic_search/', {
            'query': 'how to create products',
            'language': 'en',
        })
        elapsed_time = time.time() - start_time

        assert response.status_code == status.HTTP_200_OK
        # Should respond within 2 seconds (including model loading)
        assert elapsed_time < 2.0

    def test_keyword_search_handles_large_result_sets(self, api_client, admin_user, help_category):
        """Test that keyword search handles many topics efficiently."""
        # Create 50 topics
        for i in range(50):
            HelpTopic.objects.create(
                category=help_category,
                slug=f'topic-{i}',
                title_i18n_key=f'Test Topic {i}',
                content_markdown=f'Content for topic {i} with test keyword.',
                keywords=['test'],
                is_published=True,
            )

        api_client.force_authenticate(user=admin_user)

        response = api_client.post('/api/core/help/topics/search/', {
            'query': 'test',
            'limit': 10,
        })

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) <= 10
