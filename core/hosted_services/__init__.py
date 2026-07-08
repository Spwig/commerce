"""
Client-side view of Spwig-hosted service usage.

Polls each hosted service's ``/api/v1/usage/`` endpoint on a 5-minute Django
cache. Consumed by the admin dashboard tile, the 80% banner context
processor, and the 90% Celery beat email task.

Public API:
    from core.hosted_services import get_usage_snapshot, get_tier_config
"""

from .usage import get_usage_snapshot, refresh_usage_snapshot
from .tiers import get_tier_config

__all__ = ['get_usage_snapshot', 'refresh_usage_snapshot', 'get_tier_config']
