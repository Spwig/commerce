"""
Tests for the ``core.hosted_services`` module — usage snapshot, tier
config poller, and the 90% quota email task.
"""

from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# usage._normalise — shape reduction
# ---------------------------------------------------------------------------


def test_normalise_prefers_month_over_minute():
    from core.hosted_services.usage import _normalise
    raw = {
        'tier': 'community',
        'minute': {'current': 4, 'limit': 60},
        'month': {'current': 3241, 'limit': 10000},
    }
    result = _normalise('geoip', raw)
    assert result['primary_window']['label'] == 'this month'
    assert result['primary_window']['current'] == 3241
    assert result['primary_window']['pct'] == 32.4


def test_normalise_falls_back_to_day():
    from core.hosted_services.usage import _normalise
    raw = {
        'tier': 'community',
        'minute': {'current': 3, 'limit': 20},
        'day': {'current': 250, 'limit': 500},
    }
    result = _normalise('geocoder', raw)
    assert result['primary_window']['label'] == 'today'
    assert result['primary_window']['pct'] == 50.0


def test_normalise_falls_back_to_minute_when_only_minute_present():
    from core.hosted_services.usage import _normalise
    raw = {'tier': 'standard', 'minute': {'current': 100, 'limit': 1000}}
    result = _normalise('geoip', raw)
    assert result['primary_window']['label'] == 'this minute'
    assert result['primary_window']['pct'] == 10.0


def test_normalise_over_limit_flag():
    from core.hosted_services.usage import _normalise
    raw = {'tier': 'community', 'minute': {'current': 60, 'limit': 60}}
    result = _normalise('geoip', raw)
    assert result['over_limit'] is True


def test_normalise_error_response():
    from core.hosted_services.usage import _normalise
    result = _normalise('push', {'error': 'unreachable'})
    assert result['error'] == 'unreachable'
    assert result['primary_window'] is None
    assert result['over_limit'] is False


def test_normalise_push_legacy_hourly_shape():
    """Push /usage/ still returns the old shape for paid installs."""
    from core.hosted_services.usage import _normalise
    raw = {
        'installation_uuid': 'x', 'tier': 'standard',
        'rate_limit': 1000, 'requests_this_hour': 150,
        'remaining': 850, 'reset_in_seconds': 900,
    }
    result = _normalise('push', raw)
    assert result['primary_window']['label'] == 'this hour'
    assert result['primary_window']['current'] == 150
    assert result['primary_window']['pct'] == 15.0


# ---------------------------------------------------------------------------
# get_usage_snapshot — merges the three services
# ---------------------------------------------------------------------------


def test_get_usage_snapshot_returns_none_when_cache_cold():
    """``get_usage_snapshot`` is a *read* — never fetches inline. When
    the cache is cold (no beat run yet) it must return None so the
    admin request thread doesn't stall on outbound HTTPS."""
    from django.core.cache import cache
    from core.hosted_services import usage, get_usage_snapshot

    cache.delete(usage.CACHE_KEY)
    with patch.object(usage, '_fetch_geoip_usage') as f1, \
         patch.object(usage, '_fetch_geocoder_usage') as f2, \
         patch.object(usage, '_fetch_push_usage') as f3:
        result = get_usage_snapshot()
        f1.assert_not_called()
        f2.assert_not_called()
        f3.assert_not_called()
    assert result is None


def test_snapshot_aggregates_pct_and_over_flags(settings):
    from django.core.cache import cache
    from core.hosted_services import usage

    cache.delete(usage.CACHE_KEY)

    with patch.object(usage, '_fetch_geoip_usage', return_value={
        'tier': 'community',
        'minute': {'current': 0, 'limit': 60},
        'month': {'current': 8500, 'limit': 10000},  # 85% → over 80
    }), patch.object(usage, '_fetch_geocoder_usage', return_value={
        'tier': 'community',
        'minute': {'current': 0, 'limit': 20},
        'day': {'current': 40, 'limit': 500},   # 8%
    }), patch.object(usage, '_fetch_push_usage', return_value={
        'tier': 'community',
        'requests_this_hour': 0, 'rate_limit': 100,
    }), patch('core.hosted_services.tiers.get_tier_config', return_value={
        'services': {}, 'upgrade_url': 'https://example.com/upgrade/',
    }):
        snap = usage.refresh_usage_snapshot()

    assert snap['any_over_80']  is True
    assert snap['any_over_100'] is False
    assert snap['geoip']['primary_window']['pct']    == 85.0
    assert snap['geocoder']['primary_window']['pct'] == 8.0
    assert snap['upgrade_url'] == 'https://example.com/upgrade/'


# ---------------------------------------------------------------------------
# tiers.get_tier_config — cached, fails gracefully
# ---------------------------------------------------------------------------


def test_tier_config_returns_empty_on_error(settings):
    from django.core.cache import cache
    from core.hosted_services import tiers

    cache.delete(tiers.CACHE_KEY)

    with patch('core.hosted_services.tiers.requests.get',
               side_effect=Exception('no dns')):
        cfg = tiers.get_tier_config()
    assert cfg == {'services': {}, 'upgrade_url': 'https://updates.spwig.com/upgrade/'}


# ---------------------------------------------------------------------------
# tasks.check_hosted_service_quotas — 90% email once per month per service
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_quota_email_fires_once_per_month(settings):
    """First 90% cross triggers email; second run same month does not."""
    from django.core.cache import cache
    from core.hosted_services import tasks
    from core.models import SiteSettings

    SiteSettings.objects.get_or_create(pk=1, defaults={'admin_email': 'a@example.com'})

    # Ensure previous month's cache doesn't interfere
    cache.delete(tasks._sent_key('geoip'))

    snapshot_over_90 = {
        'geoip': {
            'service': 'geoip', 'tier': 'community',
            'primary_window': {'label': 'this month', 'current': 9500, 'limit': 10000, 'pct': 95.0},
            'over_limit': False, 'error': None,
        },
        'geocoder': {
            'service': 'geocoder', 'tier': 'community',
            'primary_window': {'label': 'today', 'current': 100, 'limit': 500, 'pct': 20.0},
            'over_limit': False, 'error': None,
        },
        'push': {
            'service': 'push', 'tier': 'community',
            'primary_window': None, 'over_limit': False, 'error': None,
        },
        'any_over_80': True, 'any_over_100': False,
        'upgrade_url': 'https://updates.spwig.com/upgrade/',
    }

    with patch('core.license.get_license_manager') as get_lm, \
         patch('core.hosted_services.refresh_usage_snapshot',
               return_value=snapshot_over_90), \
         patch('core.hosted_services.tasks._send_quota_email') as send_mock:
        get_lm.return_value.is_community.return_value = True

        # First call — email fires for geoip
        tasks.check_hosted_service_quotas()
        assert send_mock.call_count == 1
        args, _ = send_mock.call_args
        _to, triggered, _url = args
        assert len(triggered) == 1
        assert triggered[0]['service'] == 'geoip'

        # Second call in the same month — no re-send
        tasks.check_hosted_service_quotas()
        assert send_mock.call_count == 1

    cache.delete(tasks._sent_key('geoip'))


@pytest.mark.django_db
def test_quota_email_skipped_for_paid_installs():
    """Non-Community edition should never trigger the quota email."""
    from core.hosted_services import tasks

    with patch('core.license.get_license_manager') as get_lm, \
         patch('core.hosted_services.refresh_usage_snapshot') as snap_mock, \
         patch('core.hosted_services.tasks._send_quota_email') as send_mock:
        get_lm.return_value.is_community.return_value = False
        tasks.check_hosted_service_quotas()
        snap_mock.assert_not_called()
        send_mock.assert_not_called()


@pytest.mark.django_db
def test_quota_email_skipped_when_no_admin_email(settings):
    """No admin_email → no email attempt."""
    from django.core.cache import cache
    from core.hosted_services import tasks
    from core.models import SiteSettings

    # Community license but SiteSettings.admin_email is blank
    if SiteSettings.objects.filter(pk=1).exists():
        SiteSettings.objects.filter(pk=1).update(admin_email='')
    cache.delete(tasks._sent_key('geoip'))

    with patch('core.license.get_license_manager') as get_lm, \
         patch('core.hosted_services.refresh_usage_snapshot') as snap_mock, \
         patch('core.hosted_services.tasks._send_quota_email') as send_mock:
        get_lm.return_value.is_community.return_value = True
        tasks.check_hosted_service_quotas()
        # We short-circuit before fetching the snapshot
        snap_mock.assert_not_called()
        send_mock.assert_not_called()
