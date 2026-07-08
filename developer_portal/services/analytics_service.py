"""
Analytics Service
Handles fetching analytics data and managing review responses
with the upgrade server's internal API.
"""

import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)

UPGRADE_SERVER_URL = getattr(settings, 'UPGRADE_SERVER_URL', 'https://updates.spwig.com')
UPGRADE_SERVER_API_KEY = getattr(settings, 'UPGRADE_SERVER_INTERNAL_API_KEY', '')


class AnalyticsService:
    """Wraps upgrade server internal API calls for analytics and reviews."""

    def __init__(self):
        self.base_url = UPGRADE_SERVER_URL
        self.api_key = UPGRADE_SERVER_API_KEY
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-KEY': self.api_key,
        })

    def get_author_analytics(self, author_slug, days=30):
        """
        Fetch download analytics for an author from the upgrade server.
        Returns dict with total_downloads, components list, daily_downloads.
        """
        try:
            response = self.session.get(
                f'{self.base_url}/api/v1/internal/analytics/{author_slug}/',
                params={'days': days},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(
                'Failed to fetch analytics for author "%s": %s',
                author_slug, str(e),
            )
            return None

    def get_author_reviews(self, author_slug, page=1, page_size=50):
        """
        Fetch all reviews for an author's components (paginated).
        Returns dict with results list, count, page, pages.
        """
        try:
            response = self.session.get(
                f'{self.base_url}/api/v1/internal/analytics/{author_slug}/reviews/',
                params={'page': page, 'page_size': page_size},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(
                'Failed to fetch reviews for author "%s": %s',
                author_slug, str(e),
            )
            return None

    def get_author_components(self, author_slug, page=1, page_size=100):
        """
        Fetch all published components for an author from the marketplace browse API.
        Returns dict with results list, count, page, pages.
        """
        try:
            response = self.session.get(
                f'{self.base_url}/api/v1/internal/marketplace/browse/',
                params={
                    'author': author_slug,
                    'page': page,
                    'page_size': page_size,
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(
                'Failed to fetch components for author "%s": %s',
                author_slug, str(e),
            )
            return None

    def get_component_detail(self, component_slug):
        """
        Fetch full component details including version history.
        Returns dict with versions array, author info (including logo_url), etc.
        """
        try:
            response = self.session.get(
                f'{self.base_url}/api/v1/internal/marketplace/component/{component_slug}/',
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(
                'Failed to fetch component detail for "%s": %s',
                component_slug, str(e),
            )
            return None

    def push_review_response(self, review_id, author_slug, response_text):
        """
        Push a developer response to the upgrade server.
        Returns True on success, False on failure.
        """
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/internal/marketplace/reviews/{review_id}/respond/',
                json={
                    'author_slug': author_slug,
                    'response': response_text,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data.get('success', False)
        except requests.RequestException as e:
            logger.error(
                'Failed to push review response for review %s: %s',
                review_id, str(e),
            )
            return False
