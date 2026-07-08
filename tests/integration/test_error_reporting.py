"""
Error reporting system integration tests.

Tests the DataSanitizer, ErrorReport model, buffer deduplication,
middleware exception capture, JS error endpoint, and Celery task.
"""

import json
from unittest.mock import patch, MagicMock

import pytest
from django.core.cache import cache
from django.test import Client, RequestFactory
from django.utils import timezone

from tests.factories import UserFactory

pytestmark = [pytest.mark.integration, pytest.mark.core]


# ============================================================
# DataSanitizer Tests (Security-Critical)
# ============================================================


class TestDataSanitizer:
    """Extensive tests for PII masking. Security-critical."""

    def setup_method(self):
        from core.error_reporting.sanitizer import DataSanitizer
        self.sanitizer = DataSanitizer

    # --- Email masking ---

    def test_mask_email_in_text(self):
        text = "User admin@example.com reported an error"
        result = self.sanitizer._mask_emails(text)
        assert 'admin@example.com' not in result
        assert '[EMAIL]' in result

    def test_mask_multiple_emails(self):
        text = "From user@test.com to support@shop.org"
        result = self.sanitizer._mask_emails(text)
        assert 'user@test.com' not in result
        assert 'support@shop.org' not in result
        assert result.count('[EMAIL]') == 2

    def test_mask_email_in_traceback(self):
        tb = 'File "/app/views.py", line 42\n  send_email("customer@gmail.com")'
        result = self.sanitizer.sanitize_traceback(tb)
        assert 'customer@gmail.com' not in result

    # --- IP masking ---

    def test_mask_ipv4(self):
        text = "Request from 192.168.1.100 failed"
        result = self.sanitizer._mask_ips(text)
        assert '192.168.1.100' not in result
        assert '[IP]' in result

    def test_mask_ipv6(self):
        text = "Client 2001:0db8:85a3:0000:0000:8a2e:0370:7334 connected"
        result = self.sanitizer._mask_ips(text)
        assert '2001:0db8' not in result
        assert '[IPV6]' in result

    # --- Phone masking ---

    def test_mask_phone_number(self):
        text = "Contact customer at +1-555-123-4567 for details"
        result = self.sanitizer._sanitize_value(text)
        assert '555-123-4567' not in result
        assert '[PHONE]' in result

    # --- Sensitive key masking ---

    def test_mask_password_in_dict(self):
        data = {'username': 'admin', 'password': 'secret123'}
        result = self.sanitizer.sanitize_dict(data)
        assert result['password'] == '[REDACTED]'
        assert result['username'] == 'admin'

    def test_mask_nested_sensitive_keys(self):
        data = {
            'config': {
                'database_url': 'postgres://user:pass@host/db',
                'api_key': 'sk_live_abc123',
            }
        }
        result = self.sanitizer.sanitize_dict(data)
        assert result['config']['database_url'] == '[REDACTED]'
        assert result['config']['api_key'] == '[REDACTED]'

    def test_mask_token_in_dict(self):
        data = {'jwt_token': 'eyJ...', 'status': 'ok'}
        result = self.sanitizer.sanitize_dict(data)
        assert result['jwt_token'] == '[REDACTED]'
        assert result['status'] == 'ok'

    def test_mask_cookie_in_dict(self):
        data = {'cookie': 'session=abc123', 'method': 'GET'}
        result = self.sanitizer.sanitize_dict(data)
        assert result['cookie'] == '[REDACTED]'

    def test_mask_stripe_key(self):
        data = {'stripe_secret_key': 'sk_live_test123'}
        result = self.sanitizer.sanitize_dict(data)
        assert result['stripe_secret_key'] == '[REDACTED]'

    def test_mask_airwallex_key(self):
        data = {'airwallex_api_key': 'awk_live_test'}
        result = self.sanitizer.sanitize_dict(data)
        assert result['airwallex_api_key'] == '[REDACTED]'

    # --- Header masking ---

    def test_strip_auth_header(self):
        headers = {
            'Authorization': 'Bearer eyJ...',
            'Content-Type': 'application/json',
        }
        result = self.sanitizer.sanitize_headers(headers)
        assert result['Authorization'] == '[REDACTED]'
        assert result['Content-Type'] == 'application/json'

    def test_strip_cookie_header(self):
        headers = {'Cookie': 'sessionid=abc; csrftoken=xyz'}
        result = self.sanitizer.sanitize_headers(headers)
        assert result['Cookie'] == '[REDACTED]'

    def test_sanitize_referer_header(self):
        headers = {'Referer': 'https://shop.com/page?token=secret&page=1'}
        result = self.sanitizer.sanitize_headers(headers)
        assert 'secret' not in result['Referer']
        assert 'page=1' in result['Referer']

    # --- URL masking ---

    def test_redact_token_query_param(self):
        url = 'https://shop.com/callback?token=secret123&page=1'
        result = self.sanitizer.sanitize_url(url)
        assert 'secret123' not in result
        assert 'page=1' in result

    def test_redact_api_key_query_param(self):
        url = 'https://api.com/data?api_key=abc123'
        result = self.sanitizer.sanitize_url(url)
        assert 'abc123' not in result

    def test_mask_email_in_url(self):
        url = 'https://shop.com/search?q=user@example.com'
        result = self.sanitizer.sanitize_url(url)
        assert 'user@example.com' not in result

    # --- Path normalization ---

    def test_normalize_home_path(self):
        text = 'File "/home/merchant/shop/views.py", line 42'
        result = self.sanitizer._normalize_paths(text)
        assert '/home/merchant/' not in result
        assert '[PATH]/' in result

    def test_normalize_opt_path(self):
        text = 'File "/opt/shop-platform/core/views.py"'
        result = self.sanitizer._normalize_paths(text)
        assert '/opt/shop-platform/' not in result

    def test_normalize_mnt_path(self):
        text = 'File "/mnt/data/shop/views.py"'
        result = self.sanitizer._normalize_paths(text)
        assert '/mnt/data/' not in result

    # --- Key=value in traceback ---

    def test_mask_password_in_traceback(self):
        tb = 'django.db.utils.OperationalError: password=mysecretpass host=localhost'
        result = self.sanitizer.sanitize_traceback(tb)
        assert 'mysecretpass' not in result
        assert '[REDACTED]' in result

    def test_mask_database_url_in_traceback(self):
        tb = 'database_url: postgres://user:pass@host:5432/db'
        result = self.sanitizer.sanitize_traceback(tb)
        assert 'postgres://user:pass' not in result

    # --- Combined sanitize_traceback ---

    def test_full_traceback_sanitization(self):
        tb = (
            'Traceback (most recent call last):\n'
            '  File "/home/merchant/shop/views.py", line 42, in process\n'
            '    send_email("admin@shop.com", password="s3cr3t")\n'
            'ConnectionError: Failed to connect to 10.0.0.5:5432\n'
        )
        result = self.sanitizer.sanitize_traceback(tb)
        assert 'admin@shop.com' not in result
        assert '/home/merchant/' not in result
        assert 's3cr3t' not in result
        assert '10.0.0.5' not in result

    # --- List handling in dict ---

    def test_sanitize_list_values(self):
        data = {
            'errors': ['admin@test.com had an error', 'normal message'],
            'items': ['plain text', 'from 192.168.1.1'],
        }
        result = self.sanitizer.sanitize_dict(data)
        assert 'admin@test.com' not in result['errors'][0]
        assert '[EMAIL]' in result['errors'][0]
        assert result['items'][0] == 'plain text'
        assert '192.168.1.1' not in result['items'][1]

    def test_sensitive_key_list_fully_redacted(self):
        """When a key matches sensitive pattern, entire value is redacted regardless of type."""
        data = {'tokens': ['secret1', 'secret2']}
        result = self.sanitizer.sanitize_dict(data)
        assert result['tokens'] == '[REDACTED]'

    def test_sanitize_empty_dict(self):
        result = self.sanitizer.sanitize_dict({})
        assert result == {}

    def test_sanitize_non_dict(self):
        result = self.sanitizer.sanitize_dict('not a dict')
        assert result == 'not a dict'


# ============================================================
# ErrorReport Model Tests
# ============================================================


@pytest.mark.django_db
class TestErrorReportModel:
    """Tests for ErrorReport model and fingerprinting."""

    def test_compute_fingerprint_deterministic(self):
        from core.models import ErrorReport
        fp1 = ErrorReport.compute_fingerprint('ValueError', 'File "/app/views.py", line 10')
        fp2 = ErrorReport.compute_fingerprint('ValueError', 'File "/app/views.py", line 10')
        assert fp1 == fp2
        assert len(fp1) == 64  # SHA-256 hex

    def test_compute_fingerprint_different_errors(self):
        from core.models import ErrorReport
        fp1 = ErrorReport.compute_fingerprint('ValueError', 'File "/app/views.py", line 10')
        fp2 = ErrorReport.compute_fingerprint('TypeError', 'File "/app/views.py", line 10')
        assert fp1 != fp2

    def test_create_error_report(self):
        from core.models import ErrorReport
        report = ErrorReport.objects.create(
            error_type='python',
            status='pending',
            fingerprint='a' * 64,
            error_data={'exception_type': 'ValueError', 'message': 'test'},
        )
        assert report.occurrence_count == 1
        assert str(report) == 'Python Exception: ValueError (1x)'

    def test_str_with_missing_data(self):
        from core.models import ErrorReport
        report = ErrorReport(error_type='python', error_data={})
        assert 'Unknown' in str(report)


# ============================================================
# Buffer Deduplication Tests
# ============================================================


@pytest.mark.django_db
class TestBufferDeduplication:
    """Tests for error buffer dedup logic."""

    def test_buffer_python_error_creates_report(self):
        from core.models import ErrorReport
        from core.error_reporting.buffer import buffer_python_error

        error_data = {
            'exception_type': 'ValueError',
            'traceback': 'File "/app/views.py", line 10\nValueError: bad value',
        }
        buffer_python_error(error_data, status='pending')

        assert ErrorReport.objects.count() == 1
        report = ErrorReport.objects.first()
        assert report.error_type == 'python'
        assert report.occurrence_count == 1

    def test_buffer_dedup_increments_count(self):
        from core.models import ErrorReport
        from core.error_reporting.buffer import buffer_python_error

        error_data = {
            'exception_type': 'ValueError',
            'traceback': 'File "/app/views.py", line 10\nValueError: bad value',
        }
        buffer_python_error(error_data, status='pending')
        buffer_python_error(error_data, status='pending')

        assert ErrorReport.objects.count() == 1
        report = ErrorReport.objects.first()
        assert report.occurrence_count == 2

    def test_different_errors_create_separate_reports(self):
        from core.models import ErrorReport
        from core.error_reporting.buffer import buffer_python_error

        buffer_python_error({
            'exception_type': 'ValueError',
            'traceback': 'File "/app/views.py", line 10',
        })
        buffer_python_error({
            'exception_type': 'TypeError',
            'traceback': 'File "/app/models.py", line 20',
        })

        assert ErrorReport.objects.count() == 2

    def test_buffer_js_error(self):
        from core.models import ErrorReport
        from core.error_reporting.buffer import buffer_js_error

        buffer_js_error({
            'message': 'Uncaught TypeError: undefined is not a function',
            'stack': 'at /static/js/app.js:42:10',
        })

        assert ErrorReport.objects.count() == 1
        assert ErrorReport.objects.first().error_type == 'javascript'

    def test_buffer_cap_enforced(self):
        from core.models import ErrorReport
        from core.error_reporting.buffer import buffer_python_error, MAX_PENDING_REPORTS

        # Create reports just over the cap
        for i in range(MAX_PENDING_REPORTS + 5):
            ErrorReport.objects.create(
                error_type='python',
                status='pending',
                fingerprint=f'{i:064d}',
                error_data={'exception_type': f'Error{i}'},
            )

        # Trigger cap enforcement
        buffer_python_error({
            'exception_type': 'NewError',
            'traceback': 'File "/app.py", line 1',
        })

        assert ErrorReport.objects.filter(status='pending').count() <= MAX_PENDING_REPORTS + 1


# ============================================================
# Middleware Tests
# ============================================================


@pytest.mark.django_db
class TestErrorReportingMiddleware:
    """Tests for the process_exception middleware."""

    def test_middleware_captures_500_error(self, site_settings):
        from core.models import ErrorReport
        from core.middleware.error_reporting import ErrorReportingMiddleware

        middleware = ErrorReportingMiddleware(get_response=lambda r: None)
        factory = RequestFactory()
        request = factory.get('/test/')
        request.META['HTTP_USER_AGENT'] = 'TestAgent/1.0'

        middleware.process_exception(request, ValueError('test error'))

        assert ErrorReport.objects.filter(error_type='python').exists()
        report = ErrorReport.objects.first()
        assert 'ValueError' in report.error_data.get('exception_type', '')

    def test_middleware_respects_opt_out(self, site_settings):
        from core.models import ErrorReport, SiteSettings
        from core.middleware.error_reporting import ErrorReportingMiddleware

        SiteSettings.objects.filter(pk=site_settings.pk).update(error_reporting_enabled=False)
        site_settings.refresh_from_db()
        cache.delete('error_reporting:site_settings')

        middleware = ErrorReportingMiddleware(get_response=lambda r: None)
        factory = RequestFactory()
        request = factory.get('/test/')
        request.META['HTTP_USER_AGENT'] = 'TestAgent/1.0'

        middleware.process_exception(request, ValueError('test'))

        # Should be held, not pending
        reports = ErrorReport.objects.all()
        assert reports.exists()
        assert reports.first().status == 'held'

    def test_middleware_never_causes_secondary_failure(self, site_settings):
        """Middleware should never cause a 500 itself."""
        from core.middleware.error_reporting import ErrorReportingMiddleware
        from django.test import RequestFactory

        middleware = ErrorReportingMiddleware(get_response=lambda r: None)
        factory = RequestFactory()
        request = factory.get('/test/')

        # Even if sanitizer throws, middleware should not raise
        with patch(
            'core.error_reporting.sanitizer.DataSanitizer.sanitize_traceback',
            side_effect=RuntimeError('sanitizer broke'),
        ):
            result = middleware.process_exception(request, ValueError('test'))
            assert result is None  # Never interferes with Django's handling


# ============================================================
# JS Error Endpoint Tests
# ============================================================


@pytest.mark.django_db
class TestJSErrorEndpoint:
    """Tests for the /api/error-reports/js/ endpoint."""

    def setup_method(self):
        cache.clear()

    def test_receives_js_errors(self, site_settings):
        from core.models import ErrorReport

        client = Client()
        payload = {
            'errors': [
                {
                    'type': 'error',
                    'message': 'Uncaught TypeError',
                    'source': '/static/js/app.js',
                    'lineno': 42,
                    'stack': 'TypeError: x is not a function\n    at /static/js/app.js:42:10',
                    'url': '/en/products/',
                    'user_agent': 'Mozilla/5.0',
                    'timestamp': '2026-01-01T00:00:00Z',
                }
            ]
        }
        response = client.post(
            '/api/error-reports/js/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        assert response.status_code == 204
        assert ErrorReport.objects.filter(error_type='javascript').count() == 1

    def test_caps_at_20_errors(self, site_settings):
        from core.models import ErrorReport

        client = Client()
        errors = [
            {'message': f'Error {i}', 'stack': f'at line {i}'}
            for i in range(30)
        ]
        response = client.post(
            '/api/error-reports/js/',
            data=json.dumps({'errors': errors}),
            content_type='application/json',
        )
        assert response.status_code == 204
        assert ErrorReport.objects.count() <= 20

    def test_returns_204_when_disabled(self, site_settings):
        from core.models import SiteSettings
        SiteSettings.objects.filter(pk=site_settings.pk).update(error_reporting_include_js=False)
        site_settings.refresh_from_db()

        client = Client()
        response = client.post(
            '/api/error-reports/js/',
            data=json.dumps({'errors': [{'message': 'test'}]}),
            content_type='application/json',
        )
        assert response.status_code == 204
        from core.models import ErrorReport
        assert ErrorReport.objects.count() == 0

    def test_rejects_oversized_payload(self, site_settings):
        from core.models import ErrorReport

        client = Client()
        # Create a payload over 64KB
        oversized = json.dumps({'errors': [{'message': 'x' * 70000}]})
        response = client.post(
            '/api/error-reports/js/',
            data=oversized,
            content_type='application/json',
        )
        assert response.status_code == 204
        assert ErrorReport.objects.count() == 0

    def test_rate_limits_per_ip(self, site_settings):
        from core.error_reporting.views import RATE_LIMIT_PER_MINUTE

        client = Client()
        payload = json.dumps({'errors': [{'message': 'test'}]})
        # Exhaust the rate limit
        for _ in range(RATE_LIMIT_PER_MINUTE):
            client.post('/api/error-reports/js/', data=payload, content_type='application/json')

        from core.models import ErrorReport
        count_before = ErrorReport.objects.count()
        # Next request should be rate-limited (still returns 204 but doesn't buffer)
        client.post('/api/error-reports/js/', data=payload, content_type='application/json')
        assert ErrorReport.objects.count() == count_before

    def test_never_fails(self, site_settings):
        client = Client()
        # Send malformed data
        response = client.post(
            '/api/error-reports/js/',
            data='not json',
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_sanitizes_email_in_error(self, site_settings):
        from core.models import ErrorReport

        client = Client()
        payload = {
            'errors': [{
                'message': 'Error for user@secret.com',
                'stack': '',
            }]
        }
        client.post(
            '/api/error-reports/js/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        report = ErrorReport.objects.first()
        assert 'user@secret.com' not in json.dumps(report.error_data)


# ============================================================
# Celery Task Tests
# ============================================================


@pytest.mark.django_db
class TestFlushErrorReportsTask:
    """Tests for the Celery batch transmission task."""

    def test_disabled_when_reporting_off(self, site_settings):
        from core.models import SiteSettings
        from core.error_reporting.tasks import flush_error_reports

        SiteSettings.objects.filter(pk=site_settings.pk).update(error_reporting_enabled=False)
        site_settings.refresh_from_db()

        result = flush_error_reports()
        assert result['status'] == 'disabled'

    def test_empty_when_no_reports(self, site_settings):
        from core.error_reporting.tasks import flush_error_reports

        result = flush_error_reports()
        assert result['status'] == 'empty'

    def test_sends_pending_reports(self, site_settings):
        from core.models import ErrorReport
        from core.error_reporting.tasks import flush_error_reports

        ErrorReport.objects.create(
            error_type='python',
            status='pending',
            fingerprint='a' * 64,
            error_data={'exception_type': 'ValueError'},
        )

        with patch('core.error_reporting.client.ErrorReportingClient') as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.build_payload.return_value = {'reports': []}
            mock_instance.send_batch.return_value = True

            result = flush_error_reports()

        assert result['status'] == 'sent'
        assert result['sent'] == 1
        report = ErrorReport.objects.first()
        assert report.status == 'sent'
        assert report.sent_at is not None

    def test_leaves_pending_on_failure(self, site_settings):
        from core.models import ErrorReport
        from core.error_reporting.tasks import flush_error_reports

        ErrorReport.objects.create(
            error_type='python',
            status='pending',
            fingerprint='b' * 64,
            error_data={'exception_type': 'TypeError'},
        )

        with patch('core.error_reporting.client.ErrorReportingClient') as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.build_payload.return_value = {'reports': []}
            mock_instance.send_batch.return_value = False

            result = flush_error_reports()

        assert result['status'] == 'failed'
        assert ErrorReport.objects.first().status == 'pending'

    def test_does_not_send_held_reports(self, site_settings):
        from core.models import ErrorReport
        from core.error_reporting.tasks import flush_error_reports

        ErrorReport.objects.create(
            error_type='python',
            status='held',
            fingerprint='c' * 64,
            error_data={'exception_type': 'Error'},
        )

        result = flush_error_reports()
        assert result['status'] == 'empty'


# ============================================================
# SiteSettings Integration
# ============================================================


@pytest.mark.django_db
class TestSiteSettingsFields:
    """Test that the new SiteSettings fields exist and default correctly."""

    def test_error_reporting_defaults(self, site_settings):
        assert site_settings.error_reporting_enabled is True
        assert site_settings.error_reporting_include_js is True

    def test_can_disable_error_reporting(self, site_settings):
        from core.models import SiteSettings
        SiteSettings.objects.filter(pk=site_settings.pk).update(error_reporting_enabled=False)
        site_settings.refresh_from_db()
        assert site_settings.error_reporting_enabled is False


# ============================================================
# Admin Tests
# ============================================================


@pytest.mark.django_db
class TestErrorReportAdmin:
    """Test the ErrorReport admin interface."""

    def test_changelist_loads(self, site_settings):
        admin_user = UserFactory(is_staff=True, is_superuser=True)
        client = Client()
        client.force_login(admin_user)
        response = client.get('/en/admin/core/errorreport/')
        assert response.status_code == 200

    def test_submit_action(self, site_settings):
        from core.models import ErrorReport

        admin_user = UserFactory(is_staff=True, is_superuser=True)
        report = ErrorReport.objects.create(
            error_type='python',
            status='held',
            fingerprint='d' * 64,
            error_data={'exception_type': 'Error'},
        )

        client = Client()
        client.force_login(admin_user)
        response = client.post('/en/admin/core/errorreport/', {
            'action': 'submit_selected',
            '_selected_action': [report.pk],
        })
        assert response.status_code in (200, 302)
        report.refresh_from_db()
        assert report.status == 'pending'

    def test_dismiss_action(self, site_settings):
        from core.models import ErrorReport

        admin_user = UserFactory(is_staff=True, is_superuser=True)
        report = ErrorReport.objects.create(
            error_type='python',
            status='held',
            fingerprint='e' * 64,
            error_data={'exception_type': 'Error'},
        )

        client = Client()
        client.force_login(admin_user)
        response = client.post('/en/admin/core/errorreport/', {
            'action': 'dismiss_selected',
            '_selected_action': [report.pk],
        })
        assert response.status_code in (200, 302)
        assert ErrorReport.objects.filter(pk=report.pk).count() == 0
