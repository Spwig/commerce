"""
Root-level pytest fixtures — apply to every collected test regardless
of which app the test file lives in.

Keep this small. App-scoped fixtures belong in the corresponding
app/tests/conftest.py. Anything here becomes global.
"""

import pytest


@pytest.fixture(autouse=True)
def _bypass_license_acceptance_middleware(monkeypatch):
    """
    Short-circuit LicenseAcceptanceMiddleware so tests hitting storefront /
    admin paths don't get redirected to /license/accept/.

    The middleware gates real installs on first boot until the merchant
    clicks through. Tests never do — stub `is_accepted()` and
    `needs_reacceptance()` so every request passes through.

    Applies to ALL tests, including app-level suites (catalog/tests/,
    referrals/tests/, shipping/tests/ etc.) that don't inherit
    tests/conftest.py.
    """
    from core import license_acceptance as la

    class _StubService:
        def is_accepted(self):
            return True

        def needs_reacceptance(self):
            return (False, None)

    monkeypatch.setattr(la, "get_license_acceptance_service", lambda: _StubService())
