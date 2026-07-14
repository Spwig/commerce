"""
Shared i18n-ready API description constants.

Common OpenApiResponse description strings used across multiple API views.
Centralized here to avoid duplication and ensure consistent translations.
"""

from django.utils.translation import gettext_lazy as _

# Common HTTP error responses
AUTH_REQUIRED = _("Authentication required")
INVALID_AUTH_TOKEN = _("Invalid or missing authentication token")
PERMISSION_DENIED = _("Permission denied")
NOT_AUTHENTICATED = _("Not authenticated")
NOT_FOUND = _("Not found")
INVALID_REQUEST = _("Invalid request")
VALIDATION_ERROR = _("Validation error")
INTERNAL_SERVER_ERROR = _("Internal server error")
RATE_LIMIT_EXCEEDED = _("Rate limit exceeded")
INVALID_TOKEN = _("Invalid token")

# Access control
STAFF_ACCESS_REQUIRED = _("Staff access required")
POS_LICENSE_REQUIRED = _("POS license required")

# Common resource responses
PRODUCT_NOT_FOUND = _("Product not found")
ORDER_NOT_FOUND = _("Order not found")
PAGE_NOT_FOUND = _("Page not found")
MENU_NOT_FOUND = _("Menu not found")
MENU_ITEM_NOT_FOUND = _("Menu item not found")
HEADER_NOT_FOUND = _("Header not found")
FOOTER_NOT_FOUND = _("Footer not found")
ELEMENT_NOT_FOUND = _("Element not found")
ENDPOINT_NOT_FOUND = _("Endpoint not found")
TERMINAL_NOT_FOUND = _("Terminal not found")
CUSTOMER_NOT_FOUND = _("Customer not found")
SUBSCRIPTION_NOT_FOUND = _("Subscription not found")

# Common shift/POS responses
NO_OPEN_SHIFT = _("No open shift found")
