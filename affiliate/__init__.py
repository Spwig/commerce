"""
Affiliate Program Management
Enables merchants to create affiliate programs, track referrals, and manage payouts.
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)  # (major, minor, patch)
__component_name__ = "affiliate"
__description__ = "Affiliate program management and commission tracking"
__author__ = "Shop Platform Team"
__requires_platform__ = "1.x"  # Compatible with platform 1.x
__dependencies__ = [
    "core>=1.0.0",
    "accounts>=1.0.0",
    "orders>=1.0.0",
]

default_app_config = "affiliate.apps.AffiliateConfig"
