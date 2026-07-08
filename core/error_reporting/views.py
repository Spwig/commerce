"""
Server-side endpoints for receiving JavaScript errors and bug reports.

Follows the same pattern as the CSP report endpoint (/api/csp-report/).
"""

import json
import logging

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.error_reporting.buffer import buffer_js_error
from core.error_reporting.sanitizer import DataSanitizer

logger = logging.getLogger(__name__)

MAX_BODY_SIZE = 65536  # 64 KB
RATE_LIMIT_PER_MINUTE = 30


@csrf_exempt
@require_POST
def receive_js_errors(request):
    """
    Receive JavaScript errors from the browser.

    No authentication required (storefront visitors generate these).
    The endpoint is csrf_exempt since sendBeacon cannot send custom headers.
    """
    try:
        # Reject oversized payloads
        if len(request.body) > MAX_BODY_SIZE:
            return HttpResponse(status=204)

        # Per-IP rate limiting
        ip = request.META.get('REMOTE_ADDR', '')
        cache_key = f'js_error_rate:{ip}'
        count = cache.get(cache_key, 0)
        if count >= RATE_LIMIT_PER_MINUTE:
            return HttpResponse(status=204)
        cache.set(cache_key, count + 1, 60)

        from core.models import SiteSettings

        settings_obj = SiteSettings.get_settings()
        if not settings_obj or not settings_obj.error_reporting_include_js:
            return HttpResponse(status=204)

        body = json.loads(request.body)
        errors = body.get('errors', [])[:20]  # Cap at 20 per request

        status = 'pending' if settings_obj.error_reporting_enabled else 'held'

        for error in errors:
            sanitized = DataSanitizer.sanitize_dict(error)
            buffer_js_error(sanitized, status=status)

    except Exception:
        pass  # Never fail

    return HttpResponse(status=204)


BUG_REPORT_MAX_BODY = 131072  # 128 KB
BUG_REPORT_RATE_LIMIT = 10  # per hour per user
VALID_CONSENT_KEYS = {'console_logs', 'page_url', 'browser_info', 'navigation'}


@require_POST
def submit_bug_report(request):
    """
    Receive a bug report from the admin frontend wizard.
    Staff-only endpoint.
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    # Body size limit
    if len(request.body) > BUG_REPORT_MAX_BODY:
        return JsonResponse({'error': 'Request too large'}, status=413)

    # Per-user rate limiting
    rate_key = f'bug_report_rate:{request.user.pk}'
    rate_count = cache.get(rate_key, 0)
    if rate_count >= BUG_REPORT_RATE_LIMIT:
        return JsonResponse({'error': 'Rate limit exceeded. Try again later.'}, status=429)
    cache.set(rate_key, rate_count + 1, 3600)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Validate required fields
    category = data.get('category', '')
    description = data.get('description', '')
    severity = data.get('severity', '')

    if not all([category, description, severity]):
        return JsonResponse(
            {'error': 'Missing required fields: category, description, severity'},
            status=400,
        )

    from core.models import BugReport

    valid_categories = [c[0] for c in BugReport.CATEGORY_CHOICES]
    valid_severities = [s[0] for s in BugReport.SEVERITY_CHOICES]
    if category not in valid_categories or severity not in valid_severities:
        return JsonResponse({'error': 'Invalid category or severity'}, status=400)

    # Sanitize user-provided text and browser data
    sanitized_description = DataSanitizer._sanitize_value(description)
    browser_data = data.get('browser_data', {})
    if browser_data and isinstance(browser_data, dict):
        sanitized_browser_data = DataSanitizer.sanitize_dict(browser_data)
    else:
        sanitized_browser_data = {}
    # Validate and sanitize consent_flags - whitelist known keys, enforce bool values
    raw_consent = data.get('consent_flags', {})
    if isinstance(raw_consent, dict):
        consent_flags = {
            k: bool(v) for k, v in raw_consent.items()
            if k in VALID_CONSENT_KEYS
        }
    else:
        consent_flags = {}

    # Validate contact_email format if provided
    contact_email = data.get('contact_email', '')[:254]
    if contact_email:
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError as DjangoValidationError
        try:
            validate_email(contact_email)
        except DjangoValidationError:
            contact_email = ''

    report = BugReport.objects.create(
        category=category,
        description=sanitized_description[:2000],
        severity=severity,
        browser_data=sanitized_browser_data,
        consent_flags=consent_flags,
        contact_name=data.get('contact_name', '')[:200],
        contact_email=contact_email,
        contact_consent=bool(data.get('contact_consent', False)),
        submitted_by=request.user,
        page_url=data.get('page_url', '')[:500],
        admin_section=data.get('admin_section', '')[:200],
    )

    # Send immediately via Celery
    from core.error_reporting.tasks import send_bug_report
    send_bug_report.delay(report.id)

    return JsonResponse({'success': True, 'id': report.id}, status=201)
