"""
POS Terminal Providers Package

Provides a registry for terminal payment providers:
- Built-in providers (manual) are registered automatically
- Component-based providers (stripe_terminal) are discovered from ComponentRegistry

The registry uses lazy discovery - providers are loaded on first access.
"""
from .registry import TerminalProviderRegistry
from .base import TerminalProviderBase

# These are kept for backwards compatibility / direct import
# but providers are discovered dynamically from ComponentRegistry
from .manual import ManualTerminalProvider

# Re-export for convenience
__all__ = [
    'TerminalProviderRegistry',
    'TerminalProviderBase',
    'ManualTerminalProvider',
]
