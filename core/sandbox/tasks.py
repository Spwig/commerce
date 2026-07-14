"""
Sandbox Celery tasks.

Handles async operations like forwarding tamper reports to the update server.
"""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def report_tamper_to_server(self, event: str, url: str, ip: str):
    """
    Forward a sandbox banner tamper event to the Spwig update server.

    This alerts Spwig that an installation attempted to hide/remove
    the sandbox banner without having a production license.
    """
    try:
        from component_updates.models import UpdateServerConfig

        config = UpdateServerConfig.get_instance()
        if not config.server_url:
            logger.debug("No update server configured, skipping tamper report")
            return

        import requests

        payload = {
            "installation_uuid": str(config.installation_uuid) if config.installation_uuid else "",
            "event": event,
            "url": url,
            "ip": ip,
        }

        response = requests.post(
            f"{config.server_url.rstrip('/')}/api/v1/installations/tamper-report/",
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            logger.info(f"Tamper report sent to update server: event={event}")
        else:
            logger.warning(f"Update server returned {response.status_code} for tamper report")

    except Exception as exc:
        logger.error(f"Failed to send tamper report: {exc}")
        raise self.retry(exc=exc)
