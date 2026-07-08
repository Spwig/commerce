"""
Error and bug report clients for sending data to the update server.

Reuses the existing UpdateServerConfig JWT authentication.
"""

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class ErrorReportingClient:
    """Sends batched error reports to updates.spwig.com."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Spwig-ErrorReporter/1.0',
            'Content-Type': 'application/json',
        })

    def _ensure_auth(self):
        """Reuse UpdateManager's auth flow for JWT token."""
        from component_updates.services import UpdateManager

        manager = UpdateManager()
        manager._ensure_authenticated()
        self.session.headers['Authorization'] = f'Bearer {manager.config.jwt_token}'
        return manager.config

    def build_payload(self, reports):
        """Build the batch payload from ErrorReport instances."""
        config = self._ensure_auth()
        return {
            'installation_uuid': str(config.installation_uuid),
            'platform_version': getattr(settings, 'PLATFORM_VERSION', 'unknown'),
            'batch_size': len(reports),
            'reports': [
                {
                    'error_type': r.error_type,
                    'fingerprint': r.fingerprint,
                    'occurrence_count': r.occurrence_count,
                    'error_data': r.error_data,
                    'first_seen': r.first_seen.isoformat(),
                    'last_seen': r.last_seen.isoformat(),
                }
                for r in reports
            ],
        }

    def send_batch(self, payload):
        """
        Send a batch of error reports to the update server.

        Returns True on success, False on failure.
        """
        from component_updates.models import UpdateServerConfig

        config = UpdateServerConfig.get_instance()
        url = f"{config.server_url}/api/v1/error-reports/"

        try:
            response = self.session.post(url, json=payload, timeout=30)
            if response.status_code == 201:
                return True
            elif response.status_code == 429:
                logger.warning("Error reporting rate limited by server")
                return False
            else:
                logger.warning(
                    "Error reporting failed: %s %s",
                    response.status_code,
                    response.text[:200],
                )
                return False
        except requests.RequestException as e:
            logger.warning("Error reporting request failed: %s", e)
            return False


class BugReportClient:
    """Sends individual bug reports to updates.spwig.com."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Spwig-BugReporter/1.0',
            'Content-Type': 'application/json',
        })

    def _ensure_auth(self):
        """Reuse UpdateManager's auth flow for JWT token."""
        from component_updates.services import UpdateManager

        manager = UpdateManager()
        manager._ensure_authenticated()
        self.session.headers['Authorization'] = f'Bearer {manager.config.jwt_token}'
        return manager.config

    def build_payload(self, report):
        """Build a single bug report payload."""
        config = self._ensure_auth()
        return {
            'installation_uuid': str(config.installation_uuid),
            'platform_version': getattr(settings, 'PLATFORM_VERSION', 'unknown'),
            'report': {
                'category': report.category,
                'description': report.description,
                'severity': report.severity,
                'browser_data': report.browser_data,
                'consent_flags': report.consent_flags,
                'contact_name': report.contact_name,
                'contact_email': report.contact_email,
                'contact_consent': report.contact_consent,
                'page_url': report.page_url,
                'admin_section': report.admin_section,
                'submitted_at': report.created_at.isoformat(),
            },
        }

    def send(self, payload):
        """Send a bug report to the update server. Returns True on success."""
        from component_updates.models import UpdateServerConfig

        config = UpdateServerConfig.get_instance()
        url = f"{config.server_url}/api/v1/bug-reports/"

        try:
            response = self.session.post(url, json=payload, timeout=30)
            if response.status_code == 201:
                return True
            elif response.status_code == 429:
                logger.warning("Bug report rate limited by server")
                return False
            else:
                logger.warning(
                    "Bug report send failed: %s %s",
                    response.status_code,
                    response.text[:200],
                )
                return False
        except requests.RequestException as e:
            logger.warning("Bug report request failed: %s", e)
            return False
