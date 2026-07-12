"""
Platform version - single source of truth.

This module exists to avoid circular imports between settings.py and __init__.py.
Both files import the version from here.
"""

__version__ = "1.5.9"
__version_info__ = (1, 5, 9)
