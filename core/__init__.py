"""
Shop Platform Core
Self-hosted e-commerce platform with modular component architecture.
"""

from core.version import __version__, __version_info__

default_app_config = 'core.apps.CoreConfig'

# Initialize Celery app
from .celery import app as celery_app

__all__ = ('celery_app',)
