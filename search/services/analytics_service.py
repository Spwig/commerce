"""
Search analytics service.

Provides methods for aggregating and analyzing search data,
trending queries, zero-result tracking, and dashboard statistics.
"""

import csv
import io
from datetime import date, timedelta
from typing import Any

from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncDate, TruncHour
from django.utils import timezone


class AnalyticsService:
    """
    Service for search analytics aggregation and reporting.

    Provides trending queries, zero-result analysis, click-through rates,
    and dashboard statistics.
    """

    def get_trending_queries(
        self, days: int = 7, limit: int = 10, language: str = None, engine_slug: str = None
    ) -> list[dict]:
        """
        Get trending search queries.

        Returns queries sorted by search volume with growth indicators.
        """
        from ..models import SearchQuery

        # Calculate date range
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        prev_start = start_date - timedelta(days=days)

        # Base queryset
        queryset = SearchQuery.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
        )

        if language:
            queryset = queryset.filter(language=language)
        if engine_slug:
            queryset = queryset.filter(engine__slug=engine_slug)

        # Get current period stats
        current_stats = (
            queryset.values("query_normalized")
            .annotate(
                count=Count("id"),
                avg_results=Avg("result_count"),
            )
            .order_by("-count")[: limit * 2]
        )  # Get more to filter

        # Get previous period for comparison
        prev_queryset = SearchQuery.objects.filter(
            created_at__gte=prev_start,
            created_at__lt=start_date,
        )
        if language:
            prev_queryset = prev_queryset.filter(language=language)
        if engine_slug:
            prev_queryset = prev_queryset.filter(engine__slug=engine_slug)

        prev_counts = dict(
            prev_queryset.values("query_normalized")
            .annotate(count=Count("id"))
            .values_list("query_normalized", "count")
        )

        results = []
        for stat in current_stats[:limit]:
            query = stat["query_normalized"]
            current_count = stat["count"]
            prev_count = prev_counts.get(query, 0)

            # Calculate growth
            if prev_count > 0:
                growth = ((current_count - prev_count) / prev_count) * 100
            elif current_count > 0:
                growth = 100.0  # New query
            else:
                growth = 0.0

            results.append(
                {
                    "query": query,
                    "count": current_count,
                    "avg_results": round(stat["avg_results"] or 0, 1),
                    "previous_count": prev_count,
                    "growth_percent": round(growth, 1),
                    "trend": "up" if growth > 10 else ("down" if growth < -10 else "stable"),
                }
            )

        return results

    def get_zero_result_queries(
        self, days: int = 7, limit: int = 20, language: str = None
    ) -> list[dict]:
        """
        Get queries that returned zero results.

        These are potential opportunities for adding synonyms or content.
        """
        from ..models import SearchQuery

        start_date = timezone.now() - timedelta(days=days)

        queryset = SearchQuery.objects.filter(
            created_at__gte=start_date,
            is_zero_result=True,
        )

        if language:
            queryset = queryset.filter(language=language)

        return list(
            queryset.values("query_normalized")
            .annotate(
                count=Count("id"),
            )
            .order_by("-count")[:limit]
            .values("query_normalized", "count")
        )

    def get_click_through_rate(
        self, query_id: int = None, query_normalized: str = None, days: int = 7
    ) -> float:
        """
        Calculate click-through rate for a query or overall.

        CTR = (queries with clicks / total queries) * 100
        """
        from ..models import SearchQuery

        start_date = timezone.now() - timedelta(days=days)

        queryset = SearchQuery.objects.filter(
            created_at__gte=start_date,
            result_count__gt=0,  # Only count queries with results
        )

        if query_id:
            queryset = queryset.filter(pk=query_id)
        elif query_normalized:
            queryset = queryset.filter(query_normalized=query_normalized)

        total_queries = queryset.count()
        if total_queries == 0:
            return 0.0

        queries_with_clicks = queryset.filter(clicks__isnull=False).distinct().count()

        return round((queries_with_clicks / total_queries) * 100, 2)

    def get_dashboard_stats(
        self, date_from: date = None, date_to: date = None, engine_slug: str = None
    ) -> dict[str, Any]:
        """
        Get dashboard statistics for the specified date range.

        Returns comprehensive stats for the analytics dashboard.
        """
        from ..models import SearchClick, SearchQuery

        # Default to last 30 days
        if not date_to:
            date_to = timezone.now().date()
        if not date_from:
            date_from = date_to - timedelta(days=30)

        # Convert to datetime for comparison
        start_dt = timezone.make_aware(
            timezone.datetime.combine(date_from, timezone.datetime.min.time())
        )
        end_dt = timezone.make_aware(
            timezone.datetime.combine(date_to, timezone.datetime.max.time())
        )

        # Base queryset
        queryset = SearchQuery.objects.filter(
            created_at__gte=start_dt,
            created_at__lte=end_dt,
        )

        if engine_slug:
            queryset = queryset.filter(engine__slug=engine_slug)

        # Calculate stats
        total_searches = queryset.count()
        unique_queries = queryset.values("query_normalized").distinct().count()
        zero_result_count = queryset.filter(is_zero_result=True).count()
        zero_result_rate = (zero_result_count / total_searches * 100) if total_searches > 0 else 0

        avg_response_time = queryset.aggregate(avg=Avg("response_time_ms"))["avg"] or 0

        # Click-through rate
        queries_with_results = queryset.filter(result_count__gt=0).count()
        queries_with_clicks = queryset.filter(clicks__isnull=False).distinct().count()
        ctr = (queries_with_clicks / queries_with_results * 100) if queries_with_results > 0 else 0

        # Top queries
        top_queries = list(
            queryset.values("query_normalized")
            .annotate(
                count=Count("id"),
                avg_results=Avg("result_count"),
            )
            .order_by("-count")[:10]
        )

        # Searches by day for chart
        searches_by_day = list(
            queryset.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # Language distribution
        language_distribution = list(
            queryset.values("language").annotate(count=Count("id")).order_by("-count")
        )

        # Top clicked content types
        top_clicked_types = list(
            SearchClick.objects.filter(search_query__in=queryset.values("id"))
            .values("content_type__model")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        return {
            "total_searches": total_searches,
            "unique_queries": unique_queries,
            "zero_result_count": zero_result_count,
            "zero_result_rate": round(zero_result_rate, 2),
            "avg_response_time_ms": round(avg_response_time, 0),
            "click_through_rate": round(ctr, 2),
            "top_queries": top_queries,
            "searches_by_day": searches_by_day,
            "language_distribution": language_distribution,
            "top_clicked_types": top_clicked_types,
            "date_from": str(date_from),
            "date_to": str(date_to),
        }

    def get_query_details(self, query_normalized: str, days: int = 30) -> dict[str, Any]:
        """
        Get detailed analytics for a specific query.
        """
        from ..models import SearchClick, SearchQuery

        start_date = timezone.now() - timedelta(days=days)

        queryset = SearchQuery.objects.filter(
            query_normalized=query_normalized,
            created_at__gte=start_date,
        )

        total_searches = queryset.count()
        zero_results = queryset.filter(is_zero_result=True).count()

        # Searches over time
        searches_by_day = list(
            queryset.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # Avg results and response time
        aggregates = queryset.aggregate(
            avg_results=Avg("result_count"),
            avg_response=Avg("response_time_ms"),
        )

        # Click distribution
        clicks = SearchClick.objects.filter(search_query__in=queryset)
        click_positions = list(
            clicks.values("position").annotate(count=Count("id")).order_by("position")
        )

        # Most clicked items
        most_clicked = list(
            clicks.values("content_type__model", "object_id")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        return {
            "query": query_normalized,
            "total_searches": total_searches,
            "zero_result_count": zero_results,
            "zero_result_rate": round(zero_results / total_searches * 100, 2)
            if total_searches > 0
            else 0,
            "avg_result_count": round(aggregates["avg_results"] or 0, 1),
            "avg_response_time_ms": round(aggregates["avg_response"] or 0, 0),
            "searches_by_day": searches_by_day,
            "click_positions": click_positions,
            "most_clicked": most_clicked,
        }

    def get_search_volume_by_hour(self, days: int = 7) -> list[dict]:
        """
        Get search volume aggregated by hour of day.

        Useful for understanding peak search times.
        """
        from ..models import SearchQuery

        start_date = timezone.now() - timedelta(days=days)

        return list(
            SearchQuery.objects.filter(created_at__gte=start_date)
            .annotate(hour=TruncHour("created_at"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )

    def export_analytics(self, date_from: date, date_to: date, format: str = "csv") -> bytes:
        """
        Export analytics data as CSV.

        Returns bytes of the CSV file.
        """
        from ..models import SearchQuery

        start_dt = timezone.make_aware(
            timezone.datetime.combine(date_from, timezone.datetime.min.time())
        )
        end_dt = timezone.make_aware(
            timezone.datetime.combine(date_to, timezone.datetime.max.time())
        )

        queryset = (
            SearchQuery.objects.filter(
                created_at__gte=start_dt,
                created_at__lte=end_dt,
            )
            .values("query_normalized")
            .annotate(
                search_count=Count("id"),
                avg_results=Avg("result_count"),
                zero_result_count=Count("id", filter=Q(is_zero_result=True)),
                avg_response_time=Avg("response_time_ms"),
            )
            .order_by("-search_count")
        )

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(
            [
                "Query",
                "Search Count",
                "Avg Results",
                "Zero Results",
                "Zero Result Rate (%)",
                "Avg Response Time (ms)",
            ]
        )

        # Data rows
        for row in queryset:
            zero_rate = (
                row["zero_result_count"] / row["search_count"] * 100
                if row["search_count"] > 0
                else 0
            )
            writer.writerow(
                [
                    row["query_normalized"],
                    row["search_count"],
                    round(row["avg_results"] or 0, 1),
                    row["zero_result_count"],
                    round(zero_rate, 1),
                    round(row["avg_response_time"] or 0, 0),
                ]
            )

        return output.getvalue().encode("utf-8")

    def suggest_synonyms(self, min_searches: int = 5, days: int = 30) -> list[dict]:
        """
        Suggest synonyms based on zero-result queries that are
        similar to successful queries.

        Returns suggestions for improving search coverage.
        """
        from ..models import SearchQuery
        from .fuzzy_service import FuzzyService

        fuzzy = FuzzyService()
        start_date = timezone.now() - timedelta(days=days)

        # Get zero-result queries with enough volume
        zero_results = list(
            SearchQuery.objects.filter(
                created_at__gte=start_date,
                is_zero_result=True,
            )
            .values("query_normalized")
            .annotate(count=Count("id"))
            .filter(count__gte=min_searches)
            .order_by("-count")[:50]
        )

        # Get successful queries
        successful = list(
            SearchQuery.objects.filter(
                created_at__gte=start_date,
                result_count__gt=0,
            )
            .values("query_normalized")
            .annotate(
                count=Count("id"),
                avg_results=Avg("result_count"),
            )
            .filter(count__gte=min_searches)
            .order_by("-count")[:200]
        )

        successful_queries = [q["query_normalized"] for q in successful]

        suggestions = []
        for zr in zero_results:
            query = zr["query_normalized"]

            # Find similar successful queries
            similar = fuzzy.find_similar(query, successful_queries, threshold=0.7, max_results=3)

            if similar:
                suggestions.append(
                    {
                        "zero_result_query": query,
                        "search_count": zr["count"],
                        "similar_successful": [
                            {
                                "query": s[0],
                                "similarity": round(s[1], 2),
                            }
                            for s in similar
                        ],
                        "suggestion": f"Consider adding '{query}' as a synonym for '{similar[0][0]}'",
                    }
                )

        return suggestions

    def get_conversion_analytics(self, days: int = 30) -> dict[str, Any]:
        """
        Get search-to-conversion analytics.

        Tracks how searches lead to conversions (if order tracking is available).
        """
        # This is a placeholder for future integration with orders
        # Would require tracking session from search to checkout
        return {
            "message": "Conversion tracking requires order session integration",
            "searches_leading_to_cart": 0,
            "searches_leading_to_order": 0,
            "conversion_rate": 0,
        }
