"""
Database router for PgBouncer connection pool prioritization.

Routes queries to either the 'default' (high-priority) or 'background'
(low-priority) database pool based on thread-local context set by
BackgroundDBTask on Celery tasks.

Both pools point to the same physical PostgreSQL database through PgBouncer,
but with different pool sizes to ensure customer-facing traffic is never
starved by background operations.
"""
import threading

_thread_local = threading.local()


def set_db_alias(alias):
    """Set the database alias for the current thread."""
    _thread_local.db_alias = alias


def get_db_alias():
    """Get the database alias for the current thread (default: 'default')."""
    return getattr(_thread_local, 'db_alias', 'default')


def clear_db_alias():
    """Reset the database alias for the current thread."""
    _thread_local.db_alias = 'default'


class BackgroundTaskRouter:
    """
    Routes database operations to the appropriate PgBouncer pool.

    The 'background' alias is activated by BackgroundDBTask on Celery
    tasks. All other traffic (web requests, high-priority tasks) uses the
    'default' alias with the larger connection pool.
    """

    def db_for_read(self, model, **hints):
        return get_db_alias()

    def db_for_write(self, model, **hints):
        return get_db_alias()

    def allow_relation(self, obj1, obj2, **hints):
        # Both aliases point to the same physical database
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Only run migrations on the default database
        return db == 'default'
