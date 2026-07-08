"""
Social Connector Framework for Blog Auto-Sharing.

Provides a base interface for social media connectors that can be
packaged and distributed via the upgrade server.

"""
from .base import BaseSocialConnector, SocialConnectorRegistry

__all__ = ['BaseSocialConnector', 'SocialConnectorRegistry']
