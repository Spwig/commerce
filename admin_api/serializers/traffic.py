"""
Web Traffic Analytics Serializers for Admin API

Shape the combined visitor/traffic analytics response so drf-spectacular can
document it. Mirrors the dicts returned by ``geoip.services.analytics_service``.
"""

from rest_framework import serializers


class TrafficOverviewSerializer(serializers.Serializer):
    """High-level visitor KPIs."""

    total_views = serializers.IntegerField()
    human_views = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    bot_views = serializers.IntegerField()
    bounce_rate = serializers.FloatField()
    avg_pages_per_session = serializers.FloatField()


class TrafficTrendsSerializer(serializers.Serializer):
    """Daily time-series (parallel lists, Chart.js shaped)."""

    labels = serializers.ListField(child=serializers.CharField())
    views = serializers.ListField(child=serializers.IntegerField())
    visitors = serializers.ListField(child=serializers.IntegerField())
    bot_views = serializers.ListField(child=serializers.IntegerField())


class TrafficTopPageSerializer(serializers.Serializer):
    """A single most-viewed page row."""

    url_path = serializers.CharField()
    views = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    entries = serializers.IntegerField()


class TrafficGeoSerializer(serializers.Serializer):
    """Visitor distribution for one country."""

    resolved_country = serializers.CharField()
    visitors = serializers.IntegerField()
    page_views = serializers.IntegerField()


class TrafficReferrerSerializer(serializers.Serializer):
    """A single referrer-domain row."""

    referrer = serializers.CharField()
    count = serializers.IntegerField()


class TrafficAnalyticsSerializer(serializers.Serializer):
    """Combined web-analytics payload for the ``data`` envelope key."""

    period = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    overview = TrafficOverviewSerializer()
    traffic_trends = TrafficTrendsSerializer()
    top_pages = TrafficTopPageSerializer(many=True)
    geographic_distribution = TrafficGeoSerializer(many=True)
    referrer_stats = TrafficReferrerSerializer(many=True)


class TrafficAnalyticsResponseSerializer(serializers.Serializer):
    """Full success envelope: ``{success, data}``."""

    success = serializers.BooleanField()
    data = TrafficAnalyticsSerializer()
