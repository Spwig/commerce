"""
Shared test utilities for the Spwig test pipeline.
"""

import os
import re
import time
from contextlib import contextmanager
from decimal import Decimal

# Ceiling for Playwright waits in browser E2E. Deliberately generous: shared CI
# runners are markedly slower than a dev machine, and the golden checkout flows
# were previously capped *below* Playwright's 30s default (10–20s), which flaked
# the advisory ``e2e-golden`` job red on slow runs even though every flow is
# correct. A timeout is a ceiling, not a sleep — raising it never slows a passing
# run, it only stops a slow-but-correct flow from being killed prematurely.
# Override with ``SPWIG_E2E_TIMEOUT_MS`` (e.g. to tighten locally).
E2E_TIMEOUT_MS = int(os.environ.get("SPWIG_E2E_TIMEOUT_MS", "45000"))


def parse_money(text: str) -> Decimal:
    """
    Parse a money string like '$35.00', 'Free', '€19.99' into a Decimal.
    Returns Decimal('0') for 'Free' or empty strings.
    """
    if not text or text.strip().lower() == "free":
        return Decimal("0.00")
    cleaned = re.sub(r"[^\d.]", "", text.strip())
    return Decimal(cleaned) if cleaned else Decimal("0.00")


def assert_totals(actual: dict, expected: dict, tolerance: Decimal = Decimal("0.01")):
    """
    Assert that actual totals match expected within tolerance.

    Usage:
        assert_totals(
            checkout.get_summary(),
            {'subtotal': '25.00', 'shipping': '5.99', 'total': '30.99'}
        )
    """
    for key, expected_val in expected.items():
        actual_val = actual.get(key)
        if actual_val is None:
            raise AssertionError(f"Missing key '{key}' in actual totals: {actual}")
        actual_dec = parse_money(str(actual_val))
        expected_dec = Decimal(str(expected_val))
        diff = abs(actual_dec - expected_dec)
        if diff > tolerance:
            raise AssertionError(
                f"Total '{key}' mismatch: expected {expected_dec}, got {actual_dec} "
                f"(diff={diff}, tolerance={tolerance}). Full actual: {actual}"
            )


@contextmanager
def measure_time():
    """
    Context manager that measures elapsed time in milliseconds.

    Usage:
        with measure_time() as timer:
            do_something()
        assert timer.elapsed_ms < 1000
    """
    timer = type("Timer", (), {"elapsed_ms": 0})()
    start = time.monotonic()
    yield timer
    timer.elapsed_ms = (time.monotonic() - start) * 1000


# ============================================================
# POS Helpers
# ============================================================


def assert_pos_error(response, error_code, http_status=None):
    """
    Assert a POS API error response.

    POS error format: {success: false, error: {code: 'ERROR_CODE', message: '...'}}
    """
    if http_status is not None:
        assert response.status_code == http_status, (
            f"Expected HTTP {http_status}, got {response.status_code}: {response.content}"
        )
    data = response.json()
    assert data.get("success") is False, f"Expected success=false, got: {data}"
    assert data.get("error", {}).get("code") == error_code, (
        f"Expected error code '{error_code}', got: {data.get('error')}"
    )
    return data


def assert_pos_success(response, http_status=200):
    """
    Assert a POS API success response and return the data.
    """
    assert response.status_code == http_status, (
        f"Expected HTTP {http_status}, got {response.status_code}: {response.content}"
    )
    data = response.json()
    assert data.get("success") is True, f"Expected success=true, got: {data}"
    return data


def make_pos_auth_headers(token, terminal_uuid=None):
    """Build HTTP headers dict for POS API authentication."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
    if terminal_uuid:
        headers["HTTP_X_TERMINAL_UUID"] = str(terminal_uuid)
    return headers
