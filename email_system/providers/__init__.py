"""
Email Provider System

This module provides a pluggable provider architecture for email sending.
Follows the component-based pattern from exchange_rates and shipping systems.
"""

from email_system.providers.base import (
    EmailAttachment,
    EmailInlineImage,
    EmailMessage,
    EmailProviderAuthError,
    EmailProviderBase,
    EmailProviderError,
    EmailProviderRateLimitError,
    EmailProviderValidationError,
    SendResult,
)
from email_system.providers.registry import ProviderRegistry

__all__ = [
    "EmailProviderBase",
    "EmailMessage",
    "SendResult",
    "EmailAttachment",
    "EmailInlineImage",
    "EmailProviderError",
    "EmailProviderAuthError",
    "EmailProviderRateLimitError",
    "EmailProviderValidationError",
    "ProviderRegistry",
]
