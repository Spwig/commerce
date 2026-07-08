"""
DEPRECATED: Legacy Middleware File

This file is deprecated and maintained only for backwards compatibility.
All middleware classes have been moved to the core/middleware/ package.

Migration:
- Old: 'core.middleware.LicenseEnforcementMiddleware'
- New: 'core.middleware.license.LicenseEnforcementMiddleware'

This file will be removed in a future version.
"""

import warnings

# Import from new location for backwards compatibility
from core.middleware.license import LicenseEnforcementMiddleware

# Emit deprecation warning
warnings.warn(
    "Importing from 'core.middleware' is deprecated. "
    "Use 'core.middleware.license' or 'core.middleware.currency' instead.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ['LicenseEnforcementMiddleware']
