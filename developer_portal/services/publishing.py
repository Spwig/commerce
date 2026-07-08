"""
Publishing Bridge Service
Handles communication with the upgrade server to publish approved components.
Uses the existing X-API-KEY authentication mechanism.
"""

import json
import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)

# Upgrade server internal API base URL
UPGRADE_SERVER_URL = getattr(settings, 'UPGRADE_SERVER_URL', 'https://updates.spwig.com')
UPGRADE_SERVER_API_KEY = getattr(settings, 'UPGRADE_SERVER_INTERNAL_API_KEY', '')


class PublishingService:
    """Handles publishing approved components to the upgrade server."""

    def __init__(self):
        self.base_url = UPGRADE_SERVER_URL
        self.api_key = UPGRADE_SERVER_API_KEY
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-KEY': self.api_key,
        })

    def ensure_author(self, developer_profile):
        """
        Create or update the Author record on the upgrade server.
        Returns the author slug on success, None on failure.
        """
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/internal/authors/',
                json={
                    'slug': developer_profile.developer_slug,
                    'name': developer_profile.display_name,
                    'homepage': developer_profile.website,
                    'description': developer_profile.bio,
                    'is_verified': False,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data.get('slug', developer_profile.developer_slug)
        except requests.RequestException as e:
            logger.error(
                'Failed to create/update author on upgrade server: %s',
                str(e),
            )
            return None

    def publish_component(self, submission):
        """
        Publish an approved component submission to the upgrade server.
        Creates/updates Component and ComponentVersion records and uploads the package.

        Returns dict with:
            success (bool)
            component_slug (str)
            version_id (int)
            error (str, optional)
        """
        result = {
            'success': False,
            'component_slug': '',
            'version_id': None,
            'error': '',
        }

        developer = submission.developer

        # Ensure author exists on upgrade server
        if not developer.upgrade_server_author_slug:
            author_slug = self.ensure_author(developer)
            if not author_slug:
                result['error'] = 'Failed to create author on upgrade server.'
                return result
            developer.upgrade_server_author_slug = author_slug
            developer.save(update_fields=['upgrade_server_author_slug'])

        try:
            # Upload the package with metadata
            submission.package_file.seek(0)
            files = {
                'package': (
                    f'{submission.component_slug}-{submission.version}.zip',
                    submission.package_file,
                    'application/zip',
                ),
            }
            data = {
                'component_slug': submission.component_slug,
                'component_name': submission.component_name,
                'version': submission.version,
                'component_type': submission.component_type,
                'author_slug': developer.upgrade_server_author_slug,
                'description': submission.description,
                'changelog': submission.changelog,
                'manifest': json.dumps(submission.manifest_data) if submission.manifest_data else '',
                'submission_id': str(submission.pk),
            }

            response = self.session.post(
                f'{self.base_url}/api/v1/internal/components/publish/',
                data=data,
                files=files,
                timeout=120,
            )
            response.raise_for_status()

            response_data = response.json()
            result['success'] = True
            result['component_slug'] = response_data.get('component', {}).get('slug', submission.component_slug)
            result['version_id'] = response_data.get('version', {}).get('id')

        except requests.RequestException as e:
            logger.error(
                'Failed to publish %s "%s" v%s to upgrade server: %s',
                submission.component_type,
                submission.component_slug,
                submission.version,
                str(e),
            )
            result['error'] = f'Failed to publish to upgrade server: {str(e)}'

        return result

    def get_author_download_stats(self, author_slug):
        """
        Fetch download statistics for a developer from the upgrade server.
        Returns dict with download counts per component.
        """
        try:
            response = self.session.get(
                f'{self.base_url}/api/v1/internal/analytics/{author_slug}/',
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(
                'Failed to fetch analytics for author "%s": %s',
                author_slug,
                str(e),
            )
            return {'total_downloads': 0, 'components': []}
