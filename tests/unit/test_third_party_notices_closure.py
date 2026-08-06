"""Unit tests for the production-dependency-closure logic behind
THIRD_PARTY_NOTICES.txt.

The generator must attribute exactly the packages that ship in the production
image — i.e. the requirements.txt roots plus their transitive *runtime*
dependencies — and must NOT leak dev-only tooling (pytest, ruff, playwright,
...) into the notices just because it happens to be installed in the venv that
runs the command. This test locks that behaviour in: it was previously broken
(every installed package was listed), which over-attributed dev tools as shipped
third-party software.
"""

from pathlib import Path

from django.conf import settings

from core.management.commands.generate_third_party_notices import Command


def test_prod_closure_includes_runtime_and_excludes_dev_tooling():
    requirements = Path(settings.BASE_DIR) / "requirements.txt"
    roots, closure = Command()._compute_prod_closure(requirements)

    # packaging is available in CI/dev, so the closure must compute (not fall
    # back to "all installed").
    assert closure is not None
    assert requirements.exists()

    # Roots are read straight from requirements.txt.
    assert "django" in roots

    # Runtime dependencies (direct + transitive) belong in the closure.
    for pkg in ("django", "celery", "redis", "gunicorn"):
        assert pkg in closure, f"{pkg} must be in the production dependency closure"

    # Dev-only tooling lives in requirements-dev.txt and must be excluded even
    # though it is installed in the test/dev venv.
    for pkg in ("pytest", "ruff", "playwright"):
        assert pkg not in closure, f"{pkg} is dev-only and must be excluded from notices"

    # The closure is a strict subset of what's installed (dev deps dropped).
    assert roots.issubset(closure)
