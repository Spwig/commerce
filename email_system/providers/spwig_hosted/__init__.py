"""
Spwig Hosted Mail Provider

Email provider for Spwig-hosted deployments. Sends email through the
centralized Spwig Mail Gateway. Zero configuration required — credentials
are injected during provisioning.
"""

from .provider import SpwigHostedMailProvider

__all__ = ['SpwigHostedMailProvider']
