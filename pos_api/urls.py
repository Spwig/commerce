from django.urls import path

from pos_api.views import (
    auth,
    cart,
    catalog,
    checkout,
    customer,
    inventory,
    loyalty,
    orders,
    receipts,
    reports,
    sync,
    terminal,
    terminal_provider,
    webauthn,
)

app_name = "pos_api"

urlpatterns = [
    # Authentication
    path("auth/login/", auth.pos_login, name="pos_login"),
    path("auth/refresh/", auth.pos_refresh_token, name="pos_refresh"),
    path("auth/logout/", auth.pos_logout, name="pos_logout"),
    # Terminal management
    path("terminals/register/", terminal.register_terminal, name="terminal_register"),
    path("terminals/config/", terminal.terminal_config, name="terminal_config"),
    path("terminals/heartbeat/", terminal.terminal_heartbeat, name="terminal_heartbeat"),
    path(
        "terminals/display-pairing/",
        terminal.generate_display_pairing_code,
        name="terminal_display_pairing",
    ),
    path("terminals/managers/", terminal.list_managers, name="terminal_managers"),
    path("terminals/unlock/", terminal.verify_unlock_pin, name="terminal_unlock"),
    path("terminals/lock-event/", terminal.log_lock_event, name="terminal_lock_event"),
    path("terminals/unlock-card/", terminal.verify_unlock_card, name="terminal_unlock_card"),
    path("staff/register-card/", terminal.register_staff_card, name="staff_register_card"),
    path("staff/remove-card/", terminal.remove_staff_card, name="staff_remove_card"),
    path("staff/set-pin/", terminal.set_staff_pin, name="staff_set_pin"),
    path("receipt-template/", terminal.receipt_template, name="receipt_template"),
    path("promo-slides/", terminal.promo_slides, name="promo_slides"),
    # Catalog
    path("products/", catalog.product_list, name="product_list"),
    path("products/<int:product_id>/", catalog.product_detail, name="product_detail"),
    path("products/barcode/<str:barcode>/", catalog.barcode_lookup, name="barcode_lookup"),
    path("categories/", catalog.category_list, name="category_list"),
    # Cart
    path("cart/", cart.get_cart, name="cart_get"),
    path("cart/items/", cart.add_to_cart, name="cart_add_item"),
    path("cart/items/<int:item_id>/", cart.update_cart_item, name="cart_update_item"),
    path("cart/items/<int:item_id>/remove/", cart.remove_cart_item, name="cart_remove_item"),
    path("cart/voucher/", cart.apply_voucher, name="cart_apply_voucher"),
    path("cart/voucher/remove/", cart.remove_voucher, name="cart_remove_voucher"),
    path("cart/gift-card/", cart.apply_gift_card, name="cart_apply_gift_card"),
    path("cart/clear/", cart.clear_cart, name="cart_clear"),
    # Manual discounts
    path("cart/items/<int:item_id>/discount/", cart.apply_item_discount, name="cart_item_discount"),
    path(
        "cart/items/<int:item_id>/discount/remove/",
        cart.remove_item_discount,
        name="cart_item_discount_remove",
    ),
    path("cart/manual-discount/", cart.apply_cart_discount, name="cart_manual_discount"),
    path(
        "cart/manual-discount/remove/",
        cart.remove_cart_discount,
        name="cart_manual_discount_remove",
    ),
    path("cart/discount/verify-pin/", cart.verify_manager_pin, name="cart_verify_manager_pin"),
    path("cart/discount/approve/", cart.approve_discount, name="cart_approve_discount"),
    # Parked carts
    path("cart/park/", cart.park_cart, name="cart_park"),
    path("cart/parked/", cart.list_parked_carts, name="cart_parked_list"),
    path(
        "cart/parked/<int:parked_id>/restore/", cart.restore_parked_cart, name="cart_parked_restore"
    ),
    path("cart/parked/<int:parked_id>/", cart.delete_parked_cart, name="cart_parked_delete"),
    # Checkout
    path("checkout/cash/", checkout.checkout_cash, name="checkout_cash"),
    path("checkout/card/", checkout.checkout_card, name="checkout_card"),
    path("checkout/terminal-card/", checkout.checkout_terminal_card, name="checkout_terminal_card"),
    path("checkout/gift-card/", checkout.checkout_gift_card, name="checkout_gift_card"),
    path(
        "checkout/gift-card/balance/",
        checkout.check_gift_card_balance,
        name="checkout_gift_card_balance",
    ),
    path("checkout/split/", checkout.checkout_split, name="checkout_split"),
    # Terminal Provider (integrated card readers)
    path(
        "terminal-provider/config/",
        terminal_provider.provider_config,
        name="terminal_provider_config",
    ),
    path(
        "terminal-provider/connection-token/",
        terminal_provider.connection_token,
        name="terminal_provider_connection_token",
    ),
    path(
        "terminal-provider/readers/",
        terminal_provider.list_readers,
        name="terminal_provider_readers",
    ),
    path(
        "terminal-provider/create-payment-intent/",
        terminal_provider.create_payment_intent,
        name="terminal_provider_create_intent",
    ),
    path(
        "terminal-provider/capture/",
        terminal_provider.capture_payment,
        name="terminal_provider_capture",
    ),
    path(
        "terminal-provider/cancel/",
        terminal_provider.cancel_payment,
        name="terminal_provider_cancel",
    ),
    path(
        "terminal-provider/initiate-cloud-payment/",
        terminal_provider.initiate_cloud_payment,
        name="terminal_provider_cloud_payment",
    ),
    path(
        "terminal-provider/payment-status/<str:transaction_id>/",
        terminal_provider.check_payment_status,
        name="terminal_provider_payment_status",
    ),
    path(
        "terminal-provider/cancel-cloud-payment/",
        terminal_provider.cancel_cloud_payment,
        name="terminal_provider_cancel_cloud",
    ),
    # Inventory
    path("inventory/", inventory.stock_levels, name="inventory_list"),
    path("inventory/<int:product_id>/", inventory.stock_detail, name="inventory_detail"),
    path(
        "inventory/<int:product_id>/all-locations/",
        inventory.cross_location_stock,
        name="inventory_cross_location",
    ),
    path("inventory/adjust/", inventory.adjust_stock, name="inventory_adjust"),
    path("inventory/movements/", inventory.stock_movements, name="inventory_movements"),
    # Customers
    path("customers/search/", customer.customer_search, name="customer_search"),
    path("customers/", customer.customer_create, name="customer_create"),
    path("customers/<int:customer_id>/", customer.customer_detail, name="customer_detail"),
    # Orders
    path("orders/", orders.order_list, name="order_list"),
    path("orders/cashiers/", orders.cashier_list, name="order_cashiers"),
    path("orders/<int:order_id>/", orders.order_detail, name="order_detail"),
    path("orders/<int:order_id>/receipt/", orders.order_receipt, name="order_receipt"),
    path("orders/<int:order_id>/refund/", orders.refund_order, name="order_refund"),
    path("orders/<int:order_id>/void/", orders.void_order, name="order_void"),
    path(
        "orders/<int:order_id>/send-receipt/",
        receipts.send_digital_receipt,
        name="order_send_receipt",
    ),
    path(
        "orders/<int:order_id>/receipt-status/",
        receipts.receipt_status,
        name="order_receipt_status",
    ),
    # Sync
    path("sync/products/", sync.product_delta_sync, name="sync_products"),
    path("sync/customers/", sync.customer_sync, name="sync_customers"),
    path("sync/offline-transactions/", sync.upload_offline_transactions, name="sync_offline"),
    path("sync/status/", sync.sync_status, name="sync_status"),
    path("sync/version/", sync.sync_version, name="sync_version"),
    path(
        "sync/stock-adjustments/",
        sync.upload_offline_stock_adjustments,
        name="sync_stock_adjustments",
    ),
    path("sync/orders/", sync.order_sync, name="sync_orders"),
    # Shifts
    path("shifts/current/", reports.current_shift_summary, name="shift_current"),
    path("shifts/open/", reports.open_shift, name="shift_open"),
    path("shifts/close/", reports.close_shift, name="shift_close"),
    path("shifts/cash-movement/", reports.record_cash_movement, name="shift_cash_movement"),
    # Loyalty
    path("loyalty/member/<int:customer_id>/", loyalty.loyalty_member, name="loyalty_member"),
    path("loyalty/preview/<int:customer_id>/", loyalty.loyalty_preview, name="loyalty_preview"),
    # WebAuthn (biometric unlock)
    path(
        "webauthn/register/begin/", webauthn.webauthn_register_begin, name="webauthn_register_begin"
    ),
    path(
        "webauthn/register/complete/",
        webauthn.webauthn_register_complete,
        name="webauthn_register_complete",
    ),
    path(
        "webauthn/authenticate/begin/",
        webauthn.webauthn_authenticate_begin,
        name="webauthn_authenticate_begin",
    ),
    path(
        "webauthn/authenticate/complete/",
        webauthn.webauthn_authenticate_complete,
        name="webauthn_authenticate_complete",
    ),
    # Reports
    path("reports/daily/", reports.daily_report, name="report_daily"),
    path("reports/top-products/", reports.top_products, name="report_top_products"),
]
