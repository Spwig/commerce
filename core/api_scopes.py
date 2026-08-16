"""
API Token Scope Registry

Canonical definition of the access scopes a merchant API token
(``core.APIToken``) can be granted. Each scope gates a group of admin API
endpoints (see ``admin_api.scope_map.SCOPE_MAP``) at a read or read/write
level.

This registry is the single source of truth used by BOTH:
- the token admin form (which scopes are offered), and
- ``core.authentication.APITokenAuthentication`` (which scopes are valid).

Scope groups mirror the merchant-facing permission categories in
``staff_roles.categories.PERMISSION_CATEGORIES`` so the two concepts read
consistently in the admin.

HQ-only scopes carry ``hq_only=True`` and are filtered out by
``get_available_scopes()`` on any install where ``SPWIG_IS_HQ`` is false, so
they never appear in the public AGPL build or its generated OpenAPI schema.
"""

from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Group labels for the admin UI. Keys are referenced by each scope's "group".
SCOPE_GROUPS = {
    "analytics": _("Analytics"),
    "catalog": _("Catalog"),
    "orders": _("Orders"),
    "customers": _("Customers"),
    "store": _("Store & Settings"),
    "access": _("Users & Access"),
}

# scope_key -> metadata
#   label:          human label shown in the admin picker and summary
#   group:          key into SCOPE_GROUPS for admin grouping
#   description:    what the scope grants (shown in the picker)
#   supports_write: whether a read/write level is offered (read-only if False)
#   hq_only:        only available when SPWIG_IS_HQ is true
SCOPE_REGISTRY = {
    # --- Analytics ---
    "analytics": {
        "label": _("Sales Analytics"),
        "group": "analytics",
        "description": _(
            "Read sales dashboards, KPIs, product/customer/category analytics, "
            "comparisons and exports."
        ),
        "supports_write": False,
        "hq_only": False,
    },
    "analytics.traffic": {
        "label": _("Web Analytics"),
        "group": "analytics",
        "description": _(
            "Read visitor and traffic analytics: overview, trends, top pages, "
            "geography and referrers."
        ),
        "supports_write": False,
        "hq_only": False,
    },
    "analytics.attribution": {
        "label": _("Revenue Attribution"),
        "group": "analytics",
        "description": _(
            "Read multi-touch revenue attribution: per-model channel breakdown, "
            "time-series, journeys and campaign performance."
        ),
        "supports_write": False,
        "hq_only": False,
    },
    # --- Catalog ---
    "products": {
        "label": _("Products"),
        "group": "catalog",
        "description": _(
            "Products, variants, images, stock adjustments and product attribute assignment."
        ),
        "supports_write": True,
        "hq_only": False,
    },
    "categories": {
        "label": _("Categories"),
        "group": "catalog",
        "description": _("Product categories, including images and banners."),
        "supports_write": True,
        "hq_only": False,
    },
    "brands": {
        "label": _("Brands"),
        "group": "catalog",
        "description": _("Product brands."),
        "supports_write": True,
        "hq_only": False,
    },
    "attributes": {
        "label": _("Attributes"),
        "group": "catalog",
        "description": _("Product attribute definitions."),
        "supports_write": True,
        "hq_only": False,
    },
    "inventory": {
        "label": _("Inventory"),
        "group": "catalog",
        "description": _(
            "Inventory dashboards, stock velocity, movements, reorder "
            "suggestions and inventory settings."
        ),
        "supports_write": True,
        "hq_only": False,
    },
    # --- Orders ---
    "orders": {
        "label": _("Orders"),
        "group": "orders",
        "description": _(
            "Orders, order notes, status/tracking updates, cancellations, "
            "refunds and order documents (invoice, packing slip, pick list)."
        ),
        "supports_write": True,
        "hq_only": False,
    },
    # --- Customers ---
    "messages": {
        "label": _("Customer Messages"),
        "group": "customers",
        "description": _(
            "Customer messages from contact forms and order notes, including "
            "status updates and replies."
        ),
        "supports_write": True,
        "hq_only": False,
    },
    # --- Store & Settings ---
    "settings": {
        "label": _("Store Settings"),
        "group": "store",
        "description": _("Store settings, available languages and branding (name, colours, logo)."),
        "supports_write": True,
        "hq_only": False,
    },
    # --- Users & Access ---
    "staff": {
        "label": _("Staff & Roles"),
        "group": "access",
        "description": _("Staff accounts, invitations, roles and the permission catalogue."),
        "supports_write": True,
        "hq_only": False,
    },
}


def get_available_scopes():
    """
    Return the scope registry filtered for this install.

    HQ-only scopes are excluded unless ``SPWIG_IS_HQ`` is true, so a public
    (default) build never offers or validates a scope it cannot honour.

    Returns:
        dict: subset of SCOPE_REGISTRY keyed by scope_key.
    """
    hq = getattr(settings, "SPWIG_IS_HQ", False)
    return {key: meta for key, meta in SCOPE_REGISTRY.items() if hq or not meta["hq_only"]}


def is_scope_available(scope_key):
    """Whether a scope key exists and is available on this install."""
    return scope_key in get_available_scopes()


def get_scopes_grouped():
    """
    Available scopes organised by group for the admin picker.

    Returns:
        list of (group_label, [ (scope_key, meta), ... ]) preserving
        SCOPE_GROUPS order.
    """
    available = get_available_scopes()
    grouped = []
    for group_key, group_label in SCOPE_GROUPS.items():
        items = [(key, meta) for key, meta in available.items() if meta["group"] == group_key]
        if items:
            grouped.append((group_label, items))
    return grouped
