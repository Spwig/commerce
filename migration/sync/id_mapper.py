"""
ID Mapper

Maps source instance IDs to target instance IDs during full migration.
Ensures relational integrity when importing data with foreign key dependencies.
"""

import logging

logger = logging.getLogger(__name__)


class IDMapper:
    """
    Maintains a mapping of source IDs to target IDs across categories.
    Used during full migration to resolve foreign key references.

    Example:
        mapper = IDMapper()
        mapper.add('catalog.Category', source_id=42, target_id=7)
        target_id = mapper.get('catalog.Category', source_id=42)  # returns 7
    """

    def __init__(self):
        # {model_key: {source_id: target_id}}
        self._maps = {}

    def add(self, model_key, source_id, target_id):
        """
        Record a source->target ID mapping.

        Args:
            model_key: Model identifier (e.g., 'catalog.Category')
            source_id: ID on the source instance
            target_id: ID on the target instance (this instance)
        """
        if model_key not in self._maps:
            self._maps[model_key] = {}
        self._maps[model_key][source_id] = target_id

    def get(self, model_key, source_id, default=None):
        """
        Look up the target ID for a source ID.

        Args:
            model_key: Model identifier
            source_id: ID on the source instance
            default: Value to return if mapping not found

        Returns:
            Target ID or default
        """
        return self._maps.get(model_key, {}).get(source_id, default)

    def has(self, model_key, source_id):
        """Check if a mapping exists."""
        return source_id in self._maps.get(model_key, {})

    def get_map(self, model_key):
        """Get the full mapping dict for a model."""
        return self._maps.get(model_key, {})

    def get_all_target_ids(self, model_key):
        """Get all target IDs for a model (for rollback)."""
        return list(self._maps.get(model_key, {}).values())

    def count(self, model_key=None):
        """Count mapped items, optionally filtered by model."""
        if model_key:
            return len(self._maps.get(model_key, {}))
        return sum(len(m) for m in self._maps.values())

    def to_dict(self):
        """Serialize to a dict for storage in SyncStep.diff_data."""
        return {
            model_key: {str(k): v for k, v in mapping.items()}
            for model_key, mapping in self._maps.items()
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize from a dict (from SyncStep.diff_data)."""
        mapper = cls()
        for model_key, mapping in data.items():
            mapper._maps[model_key] = {_parse_id(k): v for k, v in mapping.items()}
        return mapper

    def resolve_fk(self, model_key, source_id):
        """
        Resolve a foreign key reference from source to target.
        Logs a warning if the mapping is missing.

        Args:
            model_key: Model identifier for the related model
            source_id: Source ID of the related object

        Returns:
            Target ID or None
        """
        if source_id is None:
            return None

        target_id = self.get(model_key, source_id)
        if target_id is None:
            logger.warning(f"Missing ID mapping for {model_key} source_id={source_id}")
        return target_id


def _parse_id(id_value):
    """Parse an ID value that may be string or int."""
    try:
        return int(id_value)
    except (ValueError, TypeError):
        return id_value
