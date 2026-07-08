"""
License Provider System

Provides integration with external license management platforms.
"""

from catalog.providers.base import BaseLicenseProviderAdapter
from catalog.providers.registry import LicenseProviderRegistry

__all__ = [
    'BaseLicenseProviderAdapter',
    'LicenseProviderRegistry',
]
