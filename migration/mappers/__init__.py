"""
Data Mappers
Transform external platform data to internal format
"""

from .base import BaseMapper
from .woocommerce import (
    WooCommerceCategoryMapper,
    WooCommerceCustomerMapper,
    WooCommerceOrderMapper,
    WooCommerceProductMapper,
)

__all__ = [
    "BaseMapper",
    "WooCommerceCategoryMapper",
    "WooCommerceProductMapper",
    "WooCommerceCustomerMapper",
    "WooCommerceOrderMapper",
]
