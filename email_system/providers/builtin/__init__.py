"""
Built-in SMTP Server Provider

Default email provider that works out-of-the-box with zero configuration.
Uses the platform's built-in SMTP server with DKIM signing.
"""

from .provider import BuiltinSMTPProvider

__all__ = ["BuiltinSMTPProvider"]
