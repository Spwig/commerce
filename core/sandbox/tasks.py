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

        api_version = (config.api_version or "v1").strip("/")
        response = requests.post(
            f"{config.server_url.rstrip('/')}/api/{api_version}/installations/tamper-report/",
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            logger.info(f"Tamper report sent to update server: event={event}")
        elif 400 <= response.status_code < 500 and response.status_code != 429:
            # Client errors (bad request, unauthorized, etc.) won't succeed on
            # a retry, so log and stop rather than exhausting the retry budget.
            logger.warning(
                f"Update server rejected tamper report with {response.status_code}; not retrying"
            )
        else:
            # Transient failures (5xx, 429) — raise so the exception reaches
            # self.retry below and the report is re-sent.
            response.raise_for_status()

    except Exception as exc:
        logger.error(f"Failed to send tamper report: {exc}")
        raise self.retry(exc=exc)
