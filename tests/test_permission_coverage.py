"""Unit tests for the permission-coverage guard (scripts/permission_coverage.py).

Pure-logic tests over source strings — no Django needed. They pin the contract:
a staff view with no capability gate is flagged; any recognised gate clears it.
"""

import importlib.util
from pathlib import Path

_PC_PATH = Path(__file__).resolve().parent.parent / "scripts" / "permission_coverage.py"
_spec = importlib.util.spec_from_file_location("permission_coverage", _PC_PATH)
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)


def _flagged(src):
    return pc.find_ungated_in_source(src, "app/views.py")


def test_bare_staff_member_required_is_flagged():
    src = (
        "@staff_member_required\n"
        "def filter_things(request):\n"
        "    return render(request, 't.html')\n"
    )
    assert _flagged(src) == ["app/views.py::filter_things"]


def test_requires_category_clears_it():
    src = (
        "@staff_member_required\n"
        "@requires_category('catalog', 'view', ajax=True)\n"
        "def filter_things(request):\n"
        "    return render(request, 't.html')\n"
    )
    assert _flagged(src) == []


def test_requires_permission_clears_it():
    src = (
        "@staff_member_required\n"
        "@requires_permission('catalog.view_brand')\n"
        "def filter_things(request):\n"
        "    return x\n"
    )
    assert _flagged(src) == []


def test_any_staff_marker_clears_it():
    src = "@staff_member_required\n@any_staff\ndef staff_home(request):\n    return x\n"
    assert _flagged(src) == []


def test_inline_has_perm_clears_it():
    src = (
        "@staff_member_required\n"
        "def filter_things(request):\n"
        "    if not request.user.has_perm('catalog.view_brand'):\n"
        "        return JsonResponse({'error': 'forbidden'}, status=403)\n"
        "    return x\n"
    )
    assert _flagged(src) == []


def test_inline_has_category_access_clears_it():
    src = (
        "@staff_member_required\n"
        "def dashboard(request):\n"
        "    if not has_category_access(request.user, 'analytics'):\n"
        "        raise PermissionDenied\n"
        "    return x\n"
    )
    assert _flagged(src) == []


def test_view_without_staff_decorator_is_ignored():
    src = "@login_required\ndef public_thing(request):\n    return x\n"
    assert _flagged(src) == []


def test_permission_required_decorator_clears_it():
    src = (
        "@staff_member_required\n"
        "@permission_required('vouchers.add_vouchercode')\n"
        "def import_codes(request):\n"
        "    return x\n"
    )
    assert _flagged(src) == []


def test_only_ungated_functions_are_reported_in_a_mixed_module():
    src = (
        "@staff_member_required\n"
        "def ungated(request):\n"
        "    return x\n"
        "\n"
        "@staff_member_required\n"
        "@requires_category('orders', 'full')\n"
        "def gated(request):\n"
        "    return x\n"
    )
    assert _flagged(src) == ["app/views.py::ungated"]
