"""Regression: admin_api mutation endpoints must gate on the right category.

The staff-permissions audit found single-object write endpoints (order refund /
status, stock adjust, product & category CRUD, message replies) gated only by
IsStaffWithWritePermission — i.e. any staffer with "Full" on *any* one category
could drive them. A1 swapped each write to category_permission(cat, "full"),
which DRF exposes as a permission class named ``Has_<cat>_full``. This test
fails if a gate is dropped or points at the wrong category — and guards that the
GET reads in the same files were left on the coarse gate (not over-restricted).
"""

import importlib

import pytest

# (module, function, expected category) — the write endpoints A1 gated.
GATED = (
    [
        ("admin_api.views.orders", fn, "orders")
        for fn in (
            "add_order_note",
            "update_order_status",
            "update_tracking",
            "cancel_order",
            "initiate_refund",
        )
    ]
    + [
        ("admin_api.views.products", fn, "catalog")
        for fn in (
            "adjust_stock",
            "update_product_status",
            "upload_product_image",
            "delete_product_image",
            "set_primary_image",
            "reorder_product_images",
            "update_product_image",
            "create_product",
            "update_product",
            "delete_product",
            "bulk_create_products",
            "bulk_update_products",
        )
    ]
    + [
        ("admin_api.views.categories", fn, "catalog")
        for fn in (
            "create_category",
            "update_category",
            "delete_category",
            "bulk_create_categories",
            "upload_category_image",
            "upload_category_banner",
            "delete_category_image",
            "delete_category_banner",
        )
    ]
    + [
        ("admin_api.views.attributes", fn, "catalog")
        for fn in ("create_attribute", "assign_product_attributes")
    ]
    + [
        ("admin_api.views.variants", fn, "catalog")
        for fn in ("create_variant", "update_variant", "delete_variant")
    ]
    + [
        ("admin_api.views.messages", fn, "customers")
        for fn in ("update_message_status", "reply_to_message")
    ]
)

# GET endpoints in the same files — must NOT have been tightened to category-full.
READS_STAY_COARSE = [
    ("admin_api.views.orders", "order_list"),
    ("admin_api.views.orders", "order_detail"),
    ("admin_api.views.products", "product_list"),
    ("admin_api.views.products", "product_detail"),
]


def _permission_names(module, func_name):
    view = getattr(importlib.import_module(module), func_name)
    return [c.__name__ for c in view.cls.permission_classes]


@pytest.mark.parametrize(
    "module, func, category", GATED, ids=[f"{m.split('.')[-1]}:{f}" for m, f, _ in GATED]
)
def test_mutation_endpoint_requires_category_full(module, func, category):
    names = _permission_names(module, func)
    assert f"Has_{category}_full" in names, (
        f"{module}.{func} must require category '{category}' full; got {names}"
    )


@pytest.mark.parametrize(
    "module, func", READS_STAY_COARSE, ids=[f"{m.split('.')[-1]}:{f}" for m, f in READS_STAY_COARSE]
)
def test_read_endpoint_not_over_restricted(module, func):
    names = _permission_names(module, func)
    assert not any(n.endswith("_full") for n in names), (
        f"{module}.{func} is a GET read and must stay on the coarse gate, not category-full; got {names}"
    )
