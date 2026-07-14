"""
Fuzzy matching service for typo tolerance.

Provides spelling correction suggestions and fuzzy term matching.
"""

from functools import lru_cache

from django.db.models import Count


class FuzzyService:
    """
    Service for fuzzy string matching and spelling correction.

    Uses Levenshtein distance for similarity calculations.
    Can use rapidfuzz if available, falls back to simple implementation.
    """

    def __init__(self):
        self._rapidfuzz_available = None

    @property
    def rapidfuzz_available(self) -> bool:
        """Check if rapidfuzz is available."""
        if self._rapidfuzz_available is None:
            try:
                import rapidfuzz  # noqa: F401

                self._rapidfuzz_available = True
            except ImportError:
                self._rapidfuzz_available = False
        return self._rapidfuzz_available

    def levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate the Levenshtein distance between two strings.

        Uses dynamic programming approach.
        """
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)

        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # j+1 instead of j since previous_row and current_row are one character longer
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def similarity_ratio(self, s1: str, s2: str) -> float:
        """
        Calculate similarity ratio between two strings (0-1).

        1.0 means identical, 0.0 means completely different.
        """
        if self.rapidfuzz_available:
            from rapidfuzz import fuzz

            return fuzz.ratio(s1, s2) / 100.0

        # Fallback to Levenshtein-based similarity
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        distance = self.levenshtein_distance(s1.lower(), s2.lower())
        max_len = max(len(s1), len(s2))
        return 1.0 - (distance / max_len)

    def is_fuzzy_match(
        self, query: str, target: str, threshold: float = 0.8, max_edits: int = 2
    ) -> bool:
        """
        Check if query fuzzy-matches target.

        Returns True if similarity is above threshold and edits are within max_edits.
        """
        query_lower = query.lower()
        target_lower = target.lower()

        # Exact match
        if query_lower == target_lower:
            return True

        # Check edit distance
        distance = self.levenshtein_distance(query_lower, target_lower)
        if distance > max_edits:
            return False

        # Check similarity threshold
        similarity = self.similarity_ratio(query_lower, target_lower)
        return similarity >= threshold

    def find_similar(
        self, query: str, candidates: list[str], threshold: float = 0.8, max_results: int = 5
    ) -> list[tuple[str, float]]:
        """
        Find similar terms from a list of candidates.

        Returns list of (term, similarity_score) tuples, sorted by score descending.
        """
        if self.rapidfuzz_available:
            from rapidfuzz import fuzz, process

            # Use rapidfuzz for efficient matching
            results = process.extract(
                query,
                candidates,
                scorer=fuzz.ratio,
                limit=max_results * 2,  # Get more to filter by threshold
            )
            # Filter by threshold and convert score to 0-1
            return [
                (term, score / 100.0) for term, score, _ in results if score / 100.0 >= threshold
            ][:max_results]

        # Fallback to manual comparison
        similarities = []
        query_lower = query.lower()

        for candidate in candidates:
            similarity = self.similarity_ratio(query_lower, candidate.lower())
            if similarity >= threshold:
                similarities.append((candidate, similarity))

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:max_results]

    def suggest_correction(self, query: str, language: str = "en") -> str | None:
        """
        Suggest a spelling correction based on known terms.

        Uses previous successful search queries as a dictionary.
        """
        from ..models import SearchQuery, SearchSettings

        settings = SearchSettings.get_settings()
        if not settings.fuzzy_enabled:
            return None

        # Get popular queries that returned results
        popular_queries = (
            SearchQuery.objects.filter(
                result_count__gt=0,
                language=language,
            )
            .values("query_normalized")
            .annotate(count=Count("id"))
            .filter(
                count__gte=2  # At least 2 occurrences
            )
            .order_by("-count")[:500]
        )

        candidates = [q["query_normalized"] for q in popular_queries]

        if not candidates:
            return None

        # Find similar terms
        similar = self.find_similar(
            query, candidates, threshold=float(settings.fuzzy_threshold), max_results=1
        )

        if similar:
            suggestion = similar[0][0]
            # Don't suggest if it's the same as the query
            if suggestion.lower() != query.lower():
                return suggestion

        return None

    def get_phonetic_matches(
        self, query: str, candidates: list[str], max_results: int = 5
    ) -> list[str]:
        """
        Find phonetically similar matches using Soundex or Metaphone.

        This is a simplified implementation - for production use,
        consider using jellyfish or phonetics libraries.
        """

        # Simple Soundex implementation
        def soundex(name: str) -> str:
            name = name.upper()
            if not name:
                return ""

            # Keep first letter
            soundex_code = name[0]

            # Mapping for Soundex
            mapping = {
                "BFPV": "1",
                "CGJKQSXZ": "2",
                "DT": "3",
                "L": "4",
                "MN": "5",
                "R": "6",
            }

            # Convert remaining letters
            for char in name[1:]:
                for letters, digit in mapping.items():
                    if char in letters:
                        if digit != soundex_code[-1]:
                            soundex_code += digit
                        break

            # Pad with zeros or truncate
            soundex_code = soundex_code[:4].ljust(4, "0")
            return soundex_code

        query_soundex = soundex(query)
        matches = []

        for candidate in candidates:
            if soundex(candidate) == query_soundex:
                matches.append(candidate)
                if len(matches) >= max_results:
                    break

        return matches

    @lru_cache(maxsize=1000)  # noqa: B019  # service is per-request; cache freed with instance
    def cached_similarity(self, s1: str, s2: str) -> float:
        """Cached version of similarity_ratio for repeated comparisons."""
        return self.similarity_ratio(s1, s2)

    def batch_find_similar(
        self, queries: list[str], candidates: list[str], threshold: float = 0.8
    ) -> dict:
        """
        Find similar terms for multiple queries efficiently.

        Returns dict mapping each query to its similar candidates.
        """
        results = {}

        if self.rapidfuzz_available:
            from rapidfuzz import fuzz, process

            for query in queries:
                matches = process.extract(query, candidates, scorer=fuzz.ratio, limit=5)
                results[query] = [
                    (term, score / 100.0)
                    for term, score, _ in matches
                    if score / 100.0 >= threshold
                ]
        else:
            for query in queries:
                results[query] = self.find_similar(query, candidates, threshold)

        return results
