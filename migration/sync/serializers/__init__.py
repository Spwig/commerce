"""
Sync serializers for each data category.
Each serializer handles export, import, diff, snapshot, and restore.
"""
import importlib
import logging

logger = logging.getLogger(__name__)


def get_serializer_for_category(category_key, sync_job=None, sync_step=None):
    """
    Load and instantiate the serializer for a sync category.

    Args:
        category_key: Category key from the registry
        sync_job: Optional SyncJob instance for context
        sync_step: Optional SyncStep instance for context

    Returns:
        BaseSyncSerializer instance, or None if not found
    """
    from migration.sync.category_registry import SYNC_CATEGORIES

    config = SYNC_CATEGORIES.get(category_key)
    if not config:
        logger.error(f"Unknown sync category: {category_key}")
        return None

    serializer_path = config.get('serializer')
    if not serializer_path:
        logger.error(f"No serializer configured for category: {category_key}")
        return None

    try:
        # Split into module path and class name
        module_path, class_name = serializer_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        serializer_class = getattr(module, class_name)
        return serializer_class(sync_job=sync_job, sync_step=sync_step)
    except (ImportError, AttributeError) as e:
        logger.warning(f"Could not load serializer for {category_key}: {e}")
        return None
