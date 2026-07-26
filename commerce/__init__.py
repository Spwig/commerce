"""
Shared commerce service layer.

Pricing, reservation and order placement, callable without a Django request
or HTTP session, so that the storefront, POS and any future non-browser
client all price a cart through exactly one code path.

This is a plain Python package, deliberately not a Django app: it owns no
models and no migrations. It reads the existing domain models and delegates
every calculation to the services that already own it -- `TaxService`,
`ShippingRuleService`, `StockReservationService`, `CheckoutService`.

The rule that keeps it honest: **nothing in here may invent a price.** If a
number is not obtainable from an existing service, it does not belong here.
"""

from commerce.dto import (
    QuoteLine,
    QuoteRequest,
    QuoteResult,
    ShippingQuote,
    TaxComponent,
)
from commerce.errors import CommerceError, QuoteDriftError
from commerce.ordering import (
    OrderPlacementService,
    PlacementRequest,
    PlacementResult,
)
from commerce.pricing import PricingService

__all__ = [
    "CommerceError",
    "OrderPlacementService",
    "PlacementRequest",
    "PlacementResult",
    "PricingService",
    "QuoteDriftError",
    "QuoteLine",
    "QuoteRequest",
    "QuoteResult",
    "ShippingQuote",
    "TaxComponent",
]
