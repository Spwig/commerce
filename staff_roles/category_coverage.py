"""Category-coverage guard.

Every admin-registered model should be reachable by a merchant through the
permission-category system (``PERMISSION_CATEGORIES``) — otherwise only a
superuser can manage it. This module finds models that no category covers and
compares them to a curated allowlist of models that are *intentionally*
superuser-only (auth internals, Celery schedules, ops/migration tooling, etc.).

A model is "covered" when at least one of its ``view/add/change/delete``
permissions appears in some category's permission list. The check fails when an
admin-registered model is neither covered nor allowlisted — catching the drift
that creeps in when a new model ships without being slotted into a category.
"""

from __future__ import annotations

from pathlib import Path

ALLOWLIST_PATH = Path(__file__).resolve().parent / "category_coverage_allowlist.txt"

_ACTIONS = ("view", "add", "change", "delete")


def covered_permissions() -> set[str]:
    """All ``app_label.codename`` strings referenced by any category."""
    from staff_roles.categories import PERMISSION_CATEGORIES

    covered: set[str] = set()
    for meta in PERMISSION_CATEGORIES.values():
        perms = meta.get("permissions", {})
        for level in ("view", "full"):
            covered.update(perms.get(level, []))
    return covered


def _model_label(model) -> str:
    return f"{model._meta.app_label}.{model._meta.model_name}"


def find_uncovered() -> list[str]:
    """Return 'app_label.model_name' for every registered model no category covers."""
    from django.contrib import admin

    covered = covered_permissions()
    out = []
    for model in admin.site._registry:
        meta = model._meta
        perms = {f"{meta.app_label}.{a}_{meta.model_name}" for a in _ACTIONS}
        if not (perms & covered):
            out.append(_model_label(model))
    return sorted(out)


def load_allowlist() -> set[str]:
    if not ALLOWLIST_PATH.exists():
        return set()
    return {
        line.strip()
        for line in ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def write_allowlist(entries: list[str]) -> None:
    header = (
        "# Models that are INTENTIONALLY superuser-only (no permission category).\n"
        "# The category-coverage check fails on any admin model that is neither in a\n"
        "# category nor listed here. Add a model to a category in categories.py to make\n"
        "# it delegatable; add it here only when superuser-only is the deliberate choice.\n"
    )
    ALLOWLIST_PATH.write_text(header + "\n".join(entries) + "\n", encoding="utf-8")


def violations() -> list[str]:
    """Uncovered models that aren't on the allowlist (i.e. real gaps)."""
    return sorted(set(find_uncovered()) - load_allowlist())


def stale_allowlist() -> list[str]:
    """Allowlist entries that are now covered (safe to remove)."""
    return sorted(load_allowlist() - set(find_uncovered()))
