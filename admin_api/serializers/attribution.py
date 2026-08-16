"""Revenue attribution serializers for the Admin API.

Shape the attribution dashboard payload for drf-spectacular. The dynamic parts
(``by_model`` keyed by model id, journey/campaign rows) use DictField so the
schema documents the envelope without over-constraining the free-form keys.
"""

from rest_framework import serializers


class AttrPeriodSerializer(serializers.Serializer):
    start = serializers.CharField()
    end = serializers.CharField()
    preset = serializers.CharField()


class AttrTotalsSerializer(serializers.Serializer):
    attributed = serializers.FloatField()
    orders = serializers.IntegerField()
    avg_touches = serializers.FloatField(allow_null=True)


class AttrChannelRowSerializer(serializers.Serializer):
    channel = serializers.CharField()
    revenue = serializers.FloatField()
    orders = serializers.IntegerField()
    share = serializers.FloatField()


class AttributionDataSerializer(serializers.Serializer):
    """The attribution payload (also returned verbatim by the admin dashboard)."""

    period = AttrPeriodSerializer()
    currency = serializers.CharField()
    active_model = serializers.CharField()
    models = serializers.ListField(child=serializers.CharField())
    totals = AttrTotalsSerializer()
    reconciles = serializers.BooleanField()
    # {model_id: {"channels": [channel rows], "timeseries": [{date, channel, revenue}]}}
    by_model = serializers.DictField()
    influenced = serializers.ListField(child=serializers.DictField())
    journeys = serializers.ListField(child=serializers.DictField())
    campaigns = serializers.ListField(child=serializers.DictField())
    meta = serializers.DictField()


class AttributionAnalyticsResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    data = AttributionDataSerializer()
