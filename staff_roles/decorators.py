"""Capability gates for hand-written admin views.

Reach for these instead of a bare ``@staff_member_required`` whenever a custom
admin view — an AJAX filter endpoint, a dashboard, a POST action — reads or
mutates merchant data. ``staff_member_required`` only proves *"is a staff
user"*; it does not prove the user may perform *this* action. These decorators
resolve through the ``StaffRole`` category model, the same way the mobile Admin
API's ``category_permission()`` and Django admin's ``has_perm()`` do.

Superusers pass automatically (``has_category_access`` short-circuits), so a
single-owner store sees zero friction while the gate stays enforceable for
multi-staff and enterprise installs.

Usage — pair with ``@staff_member_required`` (which still handles the login
redirect); order doesn't matter::

    @staff_member_required
    @requires_category("catalog", "view", ajax=True)
    def filter_products(request):
        ...

    @staff_member_required
    @requires_permission("orders.change_order")
    def reopen_order(request, pk):
        ...

    @staff_member_required
    @any_staff  # intentionally open to every staff user — documents the choice
    def staff_home(request):
        ...

The permission-coverage check (``scripts/permission_coverage.py``, run in
pre-commit + CI) recognises all three as valid gates.
"""

from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from staff_roles.services import has_category_access


def _forbidden(ajax):
    if ajax:
        return JsonResponse({"error": "forbidden"}, status=403)
    raise PermissionDenied


def requires_category(category, level="view", *, ajax=False):
    """Require ``level`` ("view" or "full") access on a permission ``category``.

    ``category`` is a key from ``staff_roles.categories.PERMISSION_CATEGORIES``
    (e.g. "catalog", "orders", "customers"). Prefer this over a raw permission
    check — it matches what a merchant sees in the role editor. Set ``ajax=True``
    on XHR endpoints to return a JSON 403 instead of raising ``PermissionDenied``.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not has_category_access(request.user, category, level):
                return _forbidden(ajax)
            return view_func(request, *args, **kwargs)

        _wrapped.spwig_permission_gate = ("category", category, level)
        return _wrapped

    return decorator


def requires_permission(*perms, ajax=False):
    """Require the user to hold every Django permission in ``perms``.

    Use when a precise model permission (``"catalog.view_brand"``) fits better
    than a whole category. Superusers pass automatically (Django's ``has_perm``).
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not all(request.user.has_perm(p) for p in perms):
                return _forbidden(ajax)
            return view_func(request, *args, **kwargs)

        _wrapped.spwig_permission_gate = ("permission", perms)
        return _wrapped

    return decorator


def any_staff(view_func):
    """Mark a staff view as *intentionally* open to every staff user.

    Use sparingly — a shared dashboard or a non-sensitive lookup. It grants no
    access on its own (``@staff_member_required`` already did that); it records
    the decision so the permission-coverage check treats the view as reviewed
    rather than forgotten.
    """
    view_func.spwig_permission_gate = ("any_staff",)
    return view_func
