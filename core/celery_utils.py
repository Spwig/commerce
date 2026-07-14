"""
Celery utilities for database connection pool routing.

Provides a task base class that routes Celery tasks to the low-priority
'background' PgBouncer pool, ensuring background operations don't starve
customer-facing database connections.
"""

import logging

from celery import Task
from django.conf import settings

logger = logging.getLogger(__name__)


class BackgroundDBTask(Task):
    """
    Celery task base class that routes DB queries to the 'background' pool.

    Usage in task definitions:
        @shared_task(base=BackgroundDBTask, name='...')
        def my_background_task():
            # All DB queries in this task use the low-priority pool
            ...

    Only activates when PgBouncer is configured (PGBOUNCER_HOST is set).
    In development mode (no PgBouncer), falls through to the default database.
    """

    def __call__(self, *args, **kwargs):
        if "background" in settings.DATABASES:
            from core.db_router import clear_db_alias, set_db_alias

            set_db_alias("background")
            try:
                return super().__call__(*args, **kwargs)
            finally:
                clear_db_alias()
        else:
            return super().__call__(*args, **kwargs)
