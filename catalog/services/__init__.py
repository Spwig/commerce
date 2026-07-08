"""
Catalog services package.

This package contains service classes for business logic related to the catalog app.
"""

from .license_generator import LicenseKeyGenerator
from .license_sync import LicenseProviderService
from .webhook_dispatcher import LicenseWebhookDispatcher, LicenseWebhookEvents
from catalog.providers.base import BaseLicenseProviderAdapter
from catalog.providers.registry import LicenseProviderRegistry
from .fulfillment import FulfillmentService, InsufficientStockError, fulfillment_service
from .stock_reservation import StockReservationService

__all__ = [
    'LicenseKeyGenerator',
    'LicenseProviderService',
    'LicenseWebhookDispatcher',
    'LicenseWebhookEvents',
    'BaseLicenseProviderAdapter',
    'LicenseProviderRegistry',
    'FulfillmentService',
    'InsufficientStockError',
    'fulfillment_service',
    'StockReservationService',
]
