"""
Semantic Search Service for Help System

Provides semantic search capabilities using ONNX Runtime and pgvector.
Supports chunking, embedding generation, indexing, and similarity search.

Runtime dependencies (lightweight):
- onnxruntime (~50MB) for model inference
- tokenizers (~5MB) for text tokenization
- pgvector for PostgreSQL vector similarity search

Pre-computed embeddings are loaded from a fixture file at startup.
Only search query encoding happens at runtime via ONNX.
"""

import logging
from typing import List, Dict, Optional, Any
import numpy as np
from django.conf import settings
from django.db.models import Q
from pgvector.django import CosineDistance

from core.models import HelpTopic, HelpSearchIndex

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates embeddings for text using ONNX Runtime."""

    @staticmethod
    def generate_embedding(text: str) -> List[float]:
        """
        Generate 384-dimensional embedding for text.

        Args:
            text: Input text

        Returns:
            List of 384 floats
        """
        from core.ml.onnx_encoder import OnnxSentenceEncoder
        encoder = OnnxSentenceEncoder.get_instance()
        embedding_array = encoder.encode(text)
        # Convert numpy array to Python list for JSON serialization
        return embedding_array.tolist()


class TextChunker:
    """Chunks text into segments for indexing."""

    CHUNK_SIZE = 512  # characters
    CHUNK_OVERLAP = 50  # characters

    @staticmethod
    def chunk_content(title: str, content: str, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Chunk document into overlapping segments.

        Args:
            title: Document title
            content: Document content (markdown)
            keywords: List of keywords for detection

        Returns:
            List of chunk dictionaries with metadata
        """
        chunks = []
        keywords_lower = [k.lower() for k in (keywords or [])]

        # First chunk: title + beginning of content
        title_text = f"{title}\n\n"
        first_chunk_content_length = TextChunker.CHUNK_SIZE - len(title_text)
        first_chunk_text = title_text + content[:first_chunk_content_length]

        chunks.append({
            'text': first_chunk_text,
            'position': 0,
            'is_title_chunk': True,
            'contains_keywords': any(kw in first_chunk_text.lower() for kw in keywords_lower)
        })

        # Subsequent chunks with overlap
        start = first_chunk_content_length
        chunk_number = 1

        while start < len(content):
            # Start with overlap from previous chunk
            chunk_start = max(0, start - TextChunker.CHUNK_OVERLAP)
            chunk_end = start + TextChunker.CHUNK_SIZE

            chunk_text = content[chunk_start:chunk_end]

            if chunk_text.strip():  # Only add non-empty chunks
                chunks.append({
                    'text': chunk_text,
                    'position': chunk_number,
                    'is_title_chunk': False,
                    'contains_keywords': any(kw in chunk_text.lower() for kw in keywords_lower)
                })
                chunk_number += 1

            start = chunk_end

        return chunks


class IndexingService:
    """Handles indexing of help topics."""

    @staticmethod
    def get_supported_languages() -> List[str]:
        """
        Get all supported languages from Django settings.

        Returns:
            List of language codes (e.g., ['en', 'es', 'fr', ...])
        """
        return [lang for lang, name in settings.LANGUAGES]

    @staticmethod
    def get_topic_content(topic: HelpTopic, language: str) -> Optional[str]:
        """
        Get content for a topic in a specific language.

        Args:
            topic: HelpTopic instance
            language: Language code

        Returns:
            Content string or None if not available
        """
        if language == 'en':
            # English content from content_markdown field
            return topic.content_markdown

        # Translated content from translations JSONField
        if topic.translations and language in topic.translations:
            translation = topic.translations[language]
            if isinstance(translation, dict) and 'content' in translation:
                return translation['content']

        return None

    @staticmethod
    def get_topic_title(topic: HelpTopic, language: str) -> str:
        """
        Get title for a topic in a specific language.

        Args:
            topic: HelpTopic instance
            language: Language code

        Returns:
            Title string
        """
        if language == 'en':
            # Use title_i18n_key as title for English
            return topic.title_i18n_key

        # Translated title from translations JSONField
        if topic.translations and language in topic.translations:
            translation = topic.translations[language]
            if isinstance(translation, dict) and 'title' in translation:
                return translation['title']

        # Fallback to English title
        return topic.title_i18n_key

    @staticmethod
    def index_topic(topic_id: int, languages: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Index a single topic in specified languages.

        Args:
            topic_id: ID of the HelpTopic to index
            languages: List of language codes to index (None = all languages)

        Returns:
            Dictionary with indexing statistics
        """
        try:
            topic = HelpTopic.objects.get(pk=topic_id, is_published=True)
        except HelpTopic.DoesNotExist:
            logger.warning(f"Topic {topic_id} not found or not published")
            return {'topics_indexed': 0, 'total_chunks': 0, 'languages': []}

        if languages is None:
            languages = IndexingService.get_supported_languages()

        total_chunks = 0
        indexed_languages = []

        for language in languages:
            content = IndexingService.get_topic_content(topic, language)
            if not content:
                logger.debug(f"No content for topic {topic.slug} in language {language}")
                continue

            title = IndexingService.get_topic_title(topic, language)

            # Delete existing chunks for this topic+language
            HelpSearchIndex.objects.filter(topic=topic, language=language).delete()

            # Generate chunks
            chunks = TextChunker.chunk_content(
                title=title,
                content=content,
                keywords=topic.keywords or []
            )

            # Generate embeddings and create index entries
            search_index_entries = []
            for chunk_data in chunks:
                embedding = EmbeddingGenerator.generate_embedding(chunk_data['text'])

                search_index_entries.append(HelpSearchIndex(
                    topic=topic,
                    language=language,
                    chunk_text=chunk_data['text'],
                    chunk_position=chunk_data['position'],
                    embedding=embedding,
                    is_title_chunk=chunk_data['is_title_chunk'],
                    contains_keywords=chunk_data['contains_keywords']
                ))

            # Batch create
            HelpSearchIndex.objects.bulk_create(search_index_entries)

            total_chunks += len(search_index_entries)
            indexed_languages.append(language)
            logger.info(f"Indexed topic {topic.slug} [{language}]: {len(search_index_entries)} chunks")

        return {
            'topics_indexed': 1 if indexed_languages else 0,
            'total_chunks': total_chunks,
            'languages': indexed_languages
        }

    @staticmethod
    def index_all_topics(languages: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Index all published topics in specified languages.

        Args:
            languages: List of language codes to index (None = all languages)

        Returns:
            Dictionary with indexing statistics
        """
        if languages is None:
            languages = IndexingService.get_supported_languages()

        topics = HelpTopic.objects.filter(is_published=True)
        total_topics_indexed = 0
        total_chunks = 0

        for topic in topics:
            stats = IndexingService.index_topic(topic.id, languages=languages)
            total_topics_indexed += stats['topics_indexed']
            total_chunks += stats['total_chunks']

        return {
            'topics_indexed': total_topics_indexed,
            'total_chunks': total_chunks,
            'languages': languages
        }


class SearchService:
    """Handles semantic search queries."""

    @staticmethod
    def search(
        query: str,
        language: str = 'en',
        component: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 10,
        threshold: float = 0.4
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search on help topics.

        Args:
            query: Search query text
            language: Language code to search in
            component: Filter by component name (optional)
            category: Filter by category slug (optional)
            limit: Maximum number of results to return
            threshold: Similarity threshold (0-2, lower = more similar)

        Returns:
            List of dictionaries with 'topic', 'similarity', 'chunk_position'
        """
        try:
            # Generate query embedding
            query_embedding = EmbeddingGenerator.generate_embedding(query)

            # Build queryset
            qs = HelpSearchIndex.objects.annotate(
                distance=CosineDistance('embedding', query_embedding)
            ).filter(
                language=language,
                distance__lt=threshold,
                topic__is_published=True
            ).select_related('topic', 'topic__category')

            # Apply filters
            if component:
                qs = qs.filter(topic__component=component)
            if category:
                qs = qs.filter(topic__category__slug=category)

            # Get results ordered by similarity (lower distance = higher similarity)
            # Fetch extra results for deduplication
            results = qs.order_by('distance')[:limit * 3]

            # Deduplicate by topic (keep best matching chunk per topic)
            seen_topics = {}
            for result in results:
                topic_id = result.topic_id
                if topic_id not in seen_topics:
                    # Boost scores for title chunks and keyword chunks
                    adjusted_distance = result.distance
                    if result.is_title_chunk:
                        adjusted_distance -= 0.1  # Boost title chunks
                    if result.contains_keywords:
                        adjusted_distance -= 0.05  # Boost keyword chunks

                    # Convert distance to similarity score (0-1, higher = more similar)
                    # Cosine distance ranges from 0-2, similarity is inverse
                    similarity = 1 - (adjusted_distance / 2)
                    similarity = max(0.0, min(1.0, similarity))  # Clamp to 0-1

                    seen_topics[topic_id] = {
                        'topic': result.topic,
                        'similarity': similarity,
                        'chunk_position': result.chunk_position
                    }

            # Return top N results
            top_results = sorted(
                seen_topics.values(),
                key=lambda x: x['similarity'],
                reverse=True
            )[:limit]

            return top_results

        except ImportError:
            logger.error("onnxruntime or tokenizers not installed for semantic search")
            return []
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
