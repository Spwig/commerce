"""Whether to skip or replace records an import has already created.

Step 3's "Skip existing items" checkbox controls what happens when an import
finds a record it (or an earlier run of it) already created for the current
platform, matched by the source system's external ID. On — the default —
means leave it alone; that is also the behaviour Retry depends on to avoid
duplicating a catalogue on a second attempt. Off means replace it with a
fresh import of the current source data.

"Replace" is delete, then let the unmodified creation code that follows run
again — not a field-by-field update. Recreating reuses the exact same tested
creation path a fresh import uses, rather than a second field-mapping path
that would have to be kept in permanent lock-step with the first. For a
product alone that means subscription, digital, add-on, bundle, gift-card,
composite and booking detection, images, variants and stock items; keeping
two copies of that correct forever is a larger risk than one delete call.
ProductVariant.product is CASCADE, so replacing a product's variants and
stock items falls out of deleting the product — nothing else needs to know
about skip_existing.

Deleting can fail, and that is by design: PROTECT foreign keys guard exactly
the rows a rollback also protects — a product on a real order, a category
holding a live product, a customer who has since placed a genuine order. When
a delete is blocked the record is kept exactly as skip_existing=True would
have kept it, and reported as skipped, rather than the import crashing or the
protected data being destroyed.
"""

import logging

from django.db import transaction
from django.db.models import ProtectedError

logger = logging.getLogger(__name__)


def should_skip_existing(connection_config) -> bool:
    """Read the Step 3 setting. Defaults to True — the long-established behaviour."""
    return (connection_config or {}).get("skip_existing", True)


def try_replace_existing(existing) -> bool:
    """Hard-delete `existing` so the caller can create a replacement in its place.

    Returns True once the row is gone — the caller should fall through to its
    normal creation code. Returns False if a PROTECT reference blocked the
    delete: `existing` is untouched, and the caller should treat this exactly
    like skip_existing=True — keep it, count it as skipped.

    Always deletes via the model's base manager, not `existing.delete()`.
    Product's default manager soft-deletes; calling the instance method
    there would flip a flag rather than remove the row, and the flagged row
    would still collide with the next create() on external_id or SKU.

    The delete runs in its own nested `transaction.atomic()` — a savepoint —
    regardless of whether the caller is already inside one. Callers that wrap
    this together with the record's recreation (so a failed create rolls the
    delete back too) rely on that: a caught ProtectedError still marks the
    *current* transaction unusable for further queries in Django, even though
    it was caught. Without its own savepoint here, that would poison the
    caller's outer atomic block and turn the very next query — the create —
    into a TransactionManagementError instead of the ProtectedError we meant
    to handle.
    """
    model = type(existing)
    try:
        with transaction.atomic():
            model._base_manager.filter(pk=existing.pk).delete()
        return True
    except ProtectedError:
        logger.info(
            "Kept %s %s instead of replacing it for a re-import — something "
            "else in the store still depends on it.",
            model.__name__,
            existing.pk,
        )
        return False
