"""
Celery task for the daily telemetry ping.
"""

import logging
import random

from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=0, ignore_result=True)
def send_daily_telemetry(self):
    """
    Fire the daily telemetry ping to the update server.

    Registered under Celery beat with a once-per-day cron. Random jitter is
    applied at task entry so millions of installs don't stampede the update
    server at exactly 00:00 UTC.

    Failures never retry — telemetry is best-effort. Setting
    ``SPWIG_TELEMETRY=0`` in the environment fully disables both the
    scheduled task and manual invocations.
    """
    if not getattr(settings, "SPWIG_TELEMETRY_ENABLED", True):
        logger.debug("Telemetry disabled; task exit")
        return

    # Jitter: sleep up to 1 hour so pings spread across a full window.
    # No random import overhead if disabled.
    import time

    time.sleep(random.uniform(0, 3600))

    from core.telemetry.client import send_telemetry

    send_telemetry()
