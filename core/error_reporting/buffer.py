"""
Error report buffering with deduplication.

Buffers error reports locally before batch transmission.
Deduplicates by fingerprint to avoid storing the same error repeatedly.
"""

import logging

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)

MAX_PENDING_REPORTS = 500


def buffer_python_error(error_data, status="pending"):
    """Buffer a Python error, deduplicating by fingerprint."""
    from core.models import ErrorReport

    fingerprint = ErrorReport.compute_fingerprint(
        error_data.get("exception_type", ""),
        error_data.get("traceback", ""),
    )

    # Try to increment existing pending/held report with same fingerprint
    updated = ErrorReport.objects.filter(
        fingerprint=fingerprint,
        status__in=["pending", "held"],
    ).update(
        occurrence_count=models.F("occurrence_count") + 1,
        last_seen=timezone.now(),
        error_data=error_data,
    )

    if not updated:
        ErrorReport.objects.create(
            error_type="python",
            status=status,
            fingerprint=fingerprint,
            error_data=error_data,
        )

    _enforce_buffer_cap()


def buffer_js_error(error_data, status="pending"):
    """Buffer a JavaScript error, deduplicating by fingerprint."""
    from core.models import ErrorReport

    fingerprint = ErrorReport.compute_fingerprint(
        error_data.get("message", ""),
        error_data.get("stack", ""),
    )

    updated = ErrorReport.objects.filter(
        fingerprint=fingerprint,
        status__in=["pending", "held"],
    ).update(
        occurrence_count=models.F("occurrence_count") + 1,
        last_seen=timezone.now(),
        error_data=error_data,
    )

    if not updated:
        ErrorReport.objects.create(
            error_type="javascript",
            status=status,
            fingerprint=fingerprint,
            error_data=error_data,
        )

    _enforce_buffer_cap()


def _enforce_buffer_cap():
    """Keep no more than MAX_PENDING_REPORTS buffered reports. Delete oldest if exceeded."""
    from core.models import ErrorReport

    count = ErrorReport.objects.filter(status__in=["pending", "held"]).count()
    if count > MAX_PENDING_REPORTS:
        excess_ids = list(
            ErrorReport.objects.filter(status__in=["pending", "held"])
            .order_by("first_seen")
            .values_list("id", flat=True)[: count - MAX_PENDING_REPORTS]
        )
        ErrorReport.objects.filter(id__in=excess_ids).delete()
