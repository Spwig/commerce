"""
Admin API URL → scope map (fail-closed)

Maps every ``admin_api`` URL name to the ``core.api_scopes`` scope key a
merchant API token must hold to reach it. Read vs. write is derived from the
HTTP method at enforcement time (safe methods = read, unsafe = write), so a
single scope key per endpoint suffices here.

FAIL-CLOSED CONTRACT: ``core.authentication.APITokenAuthentication`` denies any
token request whose resolved URL name is not present in ``SCOPE_MAP``. A new
endpoint is therefore unreachable by tokens until it is deliberately mapped
here (or explicitly listed in ``TOKEN_FORBIDDEN``). ``test_scope_map`` asserts
that every ``admin_api`` URL name appears in exactly one of the two, so a
forgotten mapping fails the build rather than silently opening or closing an
endpoint.

``TOKEN_FORBIDDEN`` holds endpoints that must NEVER be reachable by a static
API token: session/credential minting (login, 2FA, refresh, logout, password
reset, SSO) and per-device/per-session identity operations (device
registration, push tokens, session revocation). These are inherently tied to
an interactive mobile-app session, not a long-lived integration credential.
"""

# url_name -> scope_key
SCOPE_MAP = {
    # --- Staff & roles ---
    "staff_list": "staff",
    "staff_invite": "staff",
    "staff_update": "staff",
    "staff_delete": "staff",
    "role_list": "staff",
    "role_create": "staff",
    "role_update": "staff",
    "role_delete": "staff",
    "permissions_list": "staff",
    # --- Sales analytics ---
    "dashboard_analytics": "analytics",
    "quick_stats": "analytics",
    "sales_kpi": "analytics",
    "top_products": "analytics",
    "sales_comparison": "analytics",
    "daily_stats": "analytics",
    "sales_hourly": "analytics",
    "product_analytics": "analytics",
    "customer_analytics": "analytics",
    "category_analytics": "analytics",
    "brand_analytics": "analytics",
    "analytics_comparison": "analytics",
    "analytics_export": "analytics",
    # --- Web analytics (new) ---
    "traffic_analytics": "analytics.traffic",
    # --- Inventory ---
    "inventory_dashboard": "inventory",
    "inventory_low_stock": "inventory",
    "inventory_velocity": "inventory",
    "inventory_movements": "inventory",
    "inventory_reorder_suggestions": "inventory",
    "inventory_settings_get": "inventory",
    "inventory_settings_update": "inventory",
    "bulk_stock_adjust": "inventory",
    # --- Orders ---
    "order_list": "orders",
    "order_counts": "orders",
    "batch_documents": "orders",
    "bulk_order_status": "orders",
    "bulk_order_fulfill": "orders",
    "order_detail": "orders",
    "update_order_status": "orders",
    "update_tracking": "orders",
    "cancel_order": "orders",
    "initiate_refund": "orders",
    "order_notes": "orders",
    "add_order_note": "orders",
    "order_invoice_pdf": "orders",
    "order_packing_slip_pdf": "orders",
    "order_pick_list_pdf": "orders",
    # --- Products ---
    "product_list": "products",
    "product_counts": "products",
    "product_by_sku": "products",
    "low_stock_products": "products",
    "warehouse_list": "products",
    "create_product": "products",
    "bulk_create_products": "products",
    "bulk_update_products": "products",
    "product_detail": "products",
    "update_product": "products",
    "delete_product": "products",
    "adjust_stock": "products",
    "update_product_status": "products",
    "upload_product_image": "products",
    "reorder_product_images": "products",
    "delete_product_image": "products",
    "set_primary_image": "products",
    "update_product_image": "products",
    "variant_list": "products",
    "create_variant": "products",
    "update_variant": "products",
    "delete_variant": "products",
    "assign_product_attributes": "products",
    "bulk_price_update": "products",
    "bulk_assign_category": "products",
    "bulk_assign_tags": "products",
    "bulk_sale_update": "products",
    # --- Categories ---
    "category_list": "categories",
    "create_category": "categories",
    "bulk_create_categories": "categories",
    "category_detail": "categories",
    "update_category": "categories",
    "delete_category": "categories",
    "upload_category_image": "categories",
    "delete_category_image": "categories",
    "upload_category_banner": "categories",
    "delete_category_banner": "categories",
    # --- Brands ---
    "brand_list": "brands",
    "create_brand": "brands",
    "bulk_create_brands": "brands",
    "brand_detail": "brands",
    "update_brand": "brands",
    "delete_brand": "brands",
    # --- Attributes ---
    "attribute_list": "attributes",
    "create_attribute": "attributes",
    # --- Customer messages ---
    "message_list": "messages",
    "message_counts": "messages",
    "unread_count": "messages",
    "message_detail": "messages",
    "update_message_status": "messages",
    "reply_to_message": "messages",
    # --- Store settings & branding ---
    "get_settings": "settings",
    "available_languages": "settings",
    "branding_settings_get": "settings",
    "branding_settings_update": "settings",
    "branding_logo_upload": "settings",
}

# Endpoints tokens must never reach (session/credential/device identity).
TOKEN_FORBIDDEN = {
    # Authentication / session minting
    "staff_login",
    "verify_2fa",
    "refresh_token",
    "staff_logout",
    "staff_profile",
    "staff_password_reset_request",
    "staff_password_reset_confirm",
    "accept_invitation",
    # SSO mobile auth
    "sso_config",
    "sso_mobile_authorize",
    "sso_mobile_callback",
    "sso_mobile_token",
    # Per-device / per-session identity operations
    "list_devices",
    "register_device",
    "unregister_device",
    "update_push_token",
    "update_notifications",
    "active_sessions",
    "revoke_session",
}


def required_scope(url_name):
    """Return the scope key required for a url_name, or None if unmapped."""
    return SCOPE_MAP.get(url_name)
