"""
API Endpoint Health Audit Runner

Checks API endpoints via plain HTTP (no browser needed).
Verifies endpoints exist, respond, and don't crash.
"""

import requests as http_requests

from tests.audit.engine import AuditReport, PageResult, print_result_line, visit_url_http

# ── Endpoint definitions ─────────────────────────────────────

# Unauthenticated endpoints that should return 200
HEALTH_ENDPOINTS = [
    {"url": "/health/", "label": "Health check", "expected": [200]},
    {"url": "/health/live/", "label": "Liveness probe", "expected": [200]},
    {"url": "/health/ready/", "label": "Readiness probe", "expected": [200]},
]

# Public endpoints (may return various success codes)
PUBLIC_ENDPOINTS = [
    {"url": "/api/translation/health/", "label": "Translation health", "expected": [200]},
    {"url": "/api/store/info/", "label": "Store info"},
    {"url": "/api/catalog/products/", "label": "Catalog products API"},
    {"url": "/api/blog/posts/", "label": "Blog posts API"},
    {"url": "/api/currencies/active/", "label": "Active currencies API"},
]

# Endpoints that require authentication (should not return 500 or 404)
AUTH_ENDPOINTS = [
    {"url": "/api/cart/", "label": "Cart API", "auth": "customer"},
    {"url": "/api/checkout/", "label": "Checkout API", "auth": "customer"},
    {"url": "/api/accounts/profile/", "label": "Account profile API", "auth": "customer"},
    {"url": "/health/detailed/", "label": "Detailed health", "auth": "admin"},
]


def _get_session(base_url: str, username: str, password: str) -> http_requests.Session:
    """Create an authenticated session via Django admin login."""
    session = http_requests.Session()
    # Get CSRF token
    login_url = f"{base_url}/en/admin/login/"
    resp = session.get(login_url)
    csrf = session.cookies.get("csrftoken", "")

    # Login
    session.post(
        login_url,
        data={
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": csrf,
        },
        headers={"Referer": login_url},
    )

    return session


def run_api_audit(
    base_url: str = "http://localhost:8000",
    username: str = "admin",
    password: str = "admin123",
    verbose: bool = True,
) -> AuditReport:
    """
    Run API endpoint health audit.
    Checks that endpoints exist and don't crash (no 500s, no 404s).
    """
    all_endpoints = (
        [dict(e, group="health") for e in HEALTH_ENDPOINTS]
        + [dict(e, group="public") for e in PUBLIC_ENDPOINTS]
        + [dict(e, group="auth") for e in AUTH_ENDPOINTS]
    )

    if verbose:
        print(f"  Checking {len(all_endpoints)} API endpoints\n")

    # Create sessions
    anon_session = http_requests.Session()
    auth_session = _get_session(base_url, username, password)

    results: list[PageResult] = []
    for i, ep in enumerate(all_endpoints, 1):
        needs_auth = ep.get("auth")
        session = auth_session if needs_auth else anon_session
        expected = ep.get("expected")

        result = visit_url_http(
            url=ep["url"],
            base_url=base_url,
            label=ep["label"],
            category="api",
            session=session,
            expected_statuses=expected,
        )

        # For endpoints without explicit expected statuses,
        # flag 500s and 404s as errors
        if not expected and result.status_code:
            if result.status_code >= 500:
                if not result.console_errors:
                    result.console_errors.append(f"Server error: {result.status_code}")
            elif result.status_code == 404 and not result.console_errors:
                result.console_errors.append("Endpoint not found: 404")

        results.append(result)
        if verbose:
            print_result_line(i, len(all_endpoints), result)

    return AuditReport(category="api", results=results)
