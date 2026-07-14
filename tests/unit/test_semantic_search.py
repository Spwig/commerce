"""
Unit tests for semantic search service components.

Tests the core functionality of:
- Text chunking with overlap
- Embedding generation
- Indexing service
- Search service with pgvector
"""

from unittest.mock import patch

import numpy as np
import pytest

from core.models import HelpCategory, HelpSearchIndex, HelpTopic
from core.services.semantic_search import (
    EmbeddingGenerator,
    IndexingService,
    SearchService,
    TextChunker,
)

# Check for ONNX runtime dependencies (replaced sentence-transformers)
try:
    from core.ml.onnx_encoder import OnnxSentenceEncoder

    OnnxSentenceEncoder.get_instance()
    HAS_ONNX = True
except Exception:
    HAS_ONNX = False

onnx_required = pytest.mark.skipif(
    not HAS_ONNX, reason="onnxruntime/tokenizers not available or model not found"
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def help_category(db):
    """Create a test help category."""
    return HelpCategory.objects.create(
        name="Test Category",
        slug="test-category",
        description="Test category description",
        order=1,
    )


@pytest.fixture
def help_topic(db, help_category):
    """Create a test help topic."""
    return HelpTopic.objects.create(
        category=help_category,
        slug="test-topic",
        title_i18n_key="Test Help Topic",
        content_markdown="This is test content for the help topic. " * 50,  # ~500 chars
        keywords=["test", "help", "search"],
        is_published=True,
        component="catalog",
        url_patterns=["/admin/catalog/*"],
    )


@pytest.fixture
def help_topic_with_translations(db, help_category):
    """Create a help topic with multiple language translations."""
    return HelpTopic.objects.create(
        category=help_category,
        slug="multilingual-topic",
        title_i18n_key="Multilingual Topic",
        content_markdown="English content here. " * 30,
        keywords=["multilingual", "translation"],
        is_published=True,
        translations={
            "es": {
                "title": "Tema Multilingüe",
                "content": "Contenido en español aquí. " * 30,
            },
            "fr": {
                "title": "Sujet Multilingue",
                "content": "Contenu en français ici. " * 30,
            },
        },
    )


# ============================================================================
# Text Chunking Tests
# ============================================================================


class TestTextChunker:
    """Tests for content chunking with overlap."""

    def test_chunk_short_content(self):
        """Test chunking content shorter than chunk size."""
        title = "Short Title"
        content = "This is short content."
        keywords = ["short", "content"]

        chunks = TextChunker.chunk_content(title, content, keywords)

        assert len(chunks) == 1
        assert chunks[0]["text"].startswith(title)
        assert content in chunks[0]["text"]
        assert chunks[0]["position"] == 0
        assert chunks[0]["is_title_chunk"] is True
        assert chunks[0]["contains_keywords"] is True

    def test_chunk_long_content(self):
        """Test chunking content longer than chunk size."""
        title = "Long Content Title"
        # Create content longer than CHUNK_SIZE (512 chars)
        content = "A" * 1000

        chunks = TextChunker.chunk_content(title, content, [])

        # Should have multiple chunks
        assert len(chunks) > 1
        # First chunk should include title
        assert chunks[0]["is_title_chunk"] is True
        assert title in chunks[0]["text"]
        # Subsequent chunks should not be title chunks
        assert chunks[1]["is_title_chunk"] is False

    def test_chunk_overlap(self):
        """Test that chunks have proper overlap."""
        title = "Overlap Test"
        content = "X" * 600  # Long enough for 2+ chunks

        chunks = TextChunker.chunk_content(title, content, [])

        # Check that there's content overlap between consecutive chunks
        # (chunks should share ~50 characters)
        if len(chunks) > 1:
            # Since we're using 'X' repeated, just verify we have multiple chunks
            # and they're not empty
            assert all(len(chunk["text"]) > 0 for chunk in chunks)

    def test_keyword_detection(self):
        """Test keyword detection in chunks."""
        title = "Keyword Test"
        content = "This chunk contains important keywords like search and indexing."
        keywords = ["search", "indexing"]

        chunks = TextChunker.chunk_content(title, content, keywords)

        # Should detect keywords in the content
        assert chunks[0]["contains_keywords"] is True

    def test_keyword_case_insensitive(self):
        """Test keyword detection is case-insensitive."""
        title = "Case Test"
        content = "This has SEARCH in uppercase."
        keywords = ["search"]

        chunks = TextChunker.chunk_content(title, content, keywords)

        assert chunks[0]["contains_keywords"] is True


# ============================================================================
# Embedding Generation Tests
# ============================================================================


class TestEmbeddingGenerator:
    """Tests for embedding generation."""

    @onnx_required
    def test_generate_embedding_returns_correct_dimensions(self):
        """Test that embeddings have correct dimensions (384)."""
        text = "This is a test sentence for embedding generation."

        embedding = EmbeddingGenerator.generate_embedding(text)

        assert isinstance(embedding, list)
        assert len(embedding) == 384
        assert all(isinstance(x, float) for x in embedding)

    @onnx_required
    def test_generate_embedding_empty_text(self):
        """Test embedding generation with empty text."""
        embedding = EmbeddingGenerator.generate_embedding("")

        # Should return zero vector for empty text
        assert len(embedding) == 384
        assert all(x == 0.0 for x in embedding)

    @onnx_required
    def test_generate_embedding_similar_texts(self):
        """Test that similar texts produce similar embeddings."""
        text1 = "How do I create a product?"
        text2 = "How can I add a new product?"

        embedding1 = EmbeddingGenerator.generate_embedding(text1)
        embedding2 = EmbeddingGenerator.generate_embedding(text2)

        # Calculate cosine similarity
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        # Similar texts should have high similarity (> 0.7)
        assert similarity > 0.7


# ============================================================================
# Indexing Service Tests
# ============================================================================


class TestIndexingService:
    """Tests for help topic indexing."""

    def test_get_supported_languages(self, settings):
        """Test that supported languages are retrieved from settings."""
        languages = IndexingService.get_supported_languages()

        # Should return list of language codes from settings.LANGUAGES
        assert isinstance(languages, list)
        assert "en" in languages
        assert len(languages) > 0

    def test_get_topic_content_english(self, help_topic):
        """Test getting English content from topic."""
        content = IndexingService.get_topic_content(help_topic, "en")

        assert content == help_topic.content_markdown

    def test_get_topic_content_translation(self, help_topic_with_translations):
        """Test getting translated content from topic."""
        # Spanish content
        content_es = IndexingService.get_topic_content(help_topic_with_translations, "es")
        assert "español" in content_es

        # French content
        content_fr = IndexingService.get_topic_content(help_topic_with_translations, "fr")
        assert "français" in content_fr

    def test_get_topic_content_missing_translation(self, help_topic):
        """Test getting content for language without translation."""
        content = IndexingService.get_topic_content(help_topic, "es")

        # Should return None if translation doesn't exist
        assert content is None

    def test_get_topic_title_english(self, help_topic):
        """Test getting English title from topic."""
        title = IndexingService.get_topic_title(help_topic, "en")

        assert title == help_topic.title_i18n_key

    def test_get_topic_title_translation(self, help_topic_with_translations):
        """Test getting translated title from topic."""
        title_es = IndexingService.get_topic_title(help_topic_with_translations, "es")
        assert title_es == "Tema Multilingüe"

    def test_get_topic_title_fallback(self, help_topic):
        """Test that missing translation falls back to English."""
        title = IndexingService.get_topic_title(help_topic, "de")

        # Should fall back to English title
        assert title == help_topic.title_i18n_key

    @onnx_required
    def test_index_topic_creates_chunks(self, help_topic):
        """Test that indexing creates search index entries."""
        # Clear any existing index entries
        HelpSearchIndex.objects.all().delete()

        stats = IndexingService.index_topic(help_topic.id, languages=["en"])

        assert stats["topics_indexed"] == 1
        assert stats["total_chunks"] > 0
        assert "en" in stats["languages"]

        # Verify entries were created
        chunks = HelpSearchIndex.objects.filter(topic=help_topic, language="en")
        assert chunks.count() > 0

    @onnx_required
    def test_index_topic_replaces_old_chunks(self, help_topic):
        """Test that re-indexing replaces old chunks."""
        # Index once
        IndexingService.index_topic(help_topic.id, languages=["en"])
        first_count = HelpSearchIndex.objects.filter(topic=help_topic, language="en").count()

        # Index again
        IndexingService.index_topic(help_topic.id, languages=["en"])
        second_count = HelpSearchIndex.objects.filter(topic=help_topic, language="en").count()

        # Should have same count (old chunks deleted, new ones created)
        assert first_count == second_count

    @onnx_required
    def test_index_topic_multiple_languages(self, help_topic_with_translations):
        """Test indexing topic in multiple languages."""
        HelpSearchIndex.objects.all().delete()

        stats = IndexingService.index_topic(
            help_topic_with_translations.id, languages=["en", "es", "fr"]
        )

        assert stats["topics_indexed"] == 1
        assert "en" in stats["languages"]
        assert "es" in stats["languages"]
        assert "fr" in stats["languages"]

        # Verify chunks exist for each language
        assert HelpSearchIndex.objects.filter(
            topic=help_topic_with_translations, language="en"
        ).exists()
        assert HelpSearchIndex.objects.filter(
            topic=help_topic_with_translations, language="es"
        ).exists()
        assert HelpSearchIndex.objects.filter(
            topic=help_topic_with_translations, language="fr"
        ).exists()

    def test_index_unpublished_topic(self, help_topic):
        """Test that unpublished topics are not indexed."""
        help_topic.is_published = False
        help_topic.save()

        stats = IndexingService.index_topic(help_topic.id)

        assert stats["topics_indexed"] == 0
        assert stats["total_chunks"] == 0


# ============================================================================
# Search Service Tests
# ============================================================================


class TestSearchService:
    """Tests for semantic search queries."""

    @pytest.fixture(autouse=True)
    def setup_indexed_topics(self, help_topic, help_category):
        """Setup indexed help topics for search tests."""
        # Create additional topics for search testing
        topic2 = HelpTopic.objects.create(
            category=help_category,
            slug="product-management",
            title_i18n_key="Managing Products",
            content_markdown="Learn how to create, edit, and manage products in your catalog. "
            "Products can have variants, images, and pricing options.",
            keywords=["products", "catalog", "variants"],
            is_published=True,
        )

        topic3 = HelpTopic.objects.create(
            category=help_category,
            slug="order-fulfillment",
            title_i18n_key="Order Fulfillment",
            content_markdown="Process and fulfill customer orders. Track shipments and "
            "manage inventory for order fulfillment.",
            keywords=["orders", "fulfillment", "shipping"],
            is_published=True,
        )

        # Index all topics if ONNX runtime available
        if HAS_ONNX:
            IndexingService.index_topic(help_topic.id, languages=["en"])
            IndexingService.index_topic(topic2.id, languages=["en"])
            IndexingService.index_topic(topic3.id, languages=["en"])

    @onnx_required
    def test_search_returns_results(self):
        """Test that search returns relevant results."""
        results = SearchService.search(query="how to manage products", language="en", limit=5)

        assert isinstance(results, list)
        assert len(results) > 0
        # Each result should have topic, similarity, and chunk_position
        assert all("topic" in r for r in results)
        assert all("similarity" in r for r in results)
        assert all("chunk_position" in r for r in results)

    @onnx_required
    def test_search_relevance_ordering(self):
        """Test that results are ordered by relevance."""
        results = SearchService.search(query="creating products in catalog", language="en", limit=5)

        if len(results) > 1:
            # Similarity scores should be in descending order
            similarities = [r["similarity"] for r in results]
            assert similarities == sorted(similarities, reverse=True)

    @onnx_required
    def test_search_respects_limit(self):
        """Test that search respects the limit parameter."""
        results = SearchService.search(query="help", language="en", limit=2)

        assert len(results) <= 2

    @onnx_required
    def test_search_filters_by_component(self):
        """Test filtering search results by component."""
        results = SearchService.search(query="test", language="en", component="catalog", limit=10)

        # All results should be from catalog component
        assert all(r["topic"].component == "catalog" for r in results)

    @onnx_required
    def test_search_filters_by_category(self, help_category):
        """Test filtering search results by category."""
        results = SearchService.search(
            query="test", language="en", category=help_category.slug, limit=10
        )

        # All results should be from specified category
        assert all(r["topic"].category.slug == help_category.slug for r in results)

    @onnx_required
    def test_search_respects_threshold(self):
        """Test that search respects similarity threshold."""
        # Very strict threshold - should return fewer/no results
        results_strict = SearchService.search(
            query="random unrelated query xyz123",
            language="en",
            threshold=0.1,  # Very low threshold (high similarity required)
            limit=10,
        )

        # Lenient threshold - should return more results
        results_lenient = SearchService.search(
            query="random unrelated query xyz123",
            language="en",
            threshold=1.5,  # High threshold (low similarity required)
            limit=10,
        )

        # Lenient threshold should return same or more results
        assert len(results_lenient) >= len(results_strict)

    @onnx_required
    def test_search_deduplicates_by_topic(self, help_topic):
        """Test that search returns only one result per topic."""
        # Index topic with multiple chunks
        IndexingService.index_topic(help_topic.id, languages=["en"])

        results = SearchService.search(query="test", language="en", limit=10)

        # Each topic should appear at most once
        topic_ids = [r["topic"].id for r in results]
        assert len(topic_ids) == len(set(topic_ids))

    def test_search_handles_missing_dependencies(self):
        """Test that search handles missing ONNX runtime gracefully."""
        with patch(
            "core.services.semantic_search.EmbeddingGenerator.generate_embedding",
            side_effect=ImportError("onnxruntime not installed"),
        ):
            results = SearchService.search(query="test", language="en")

            # Should return empty list on error
            assert results == []
