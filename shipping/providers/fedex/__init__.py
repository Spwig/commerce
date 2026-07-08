"""
FedEx Shipping Provider

OAuth 2.0 authenticated shipping provider for FedEx API.
Supports rate calculation, label generation, and tracking.

Version: 1.0.0
"""
from shipping.providers.fedex.auth import FedExOAuthClient, create_oauth_client
from shipping.providers.fedex.provider import FedExProvider

__all__ = ['FedExProvider', 'FedExOAuthClient', 'create_oauth_client']
__version__ = '1.0.0'
