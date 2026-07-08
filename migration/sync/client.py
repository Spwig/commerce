"""
SpwigSyncClient

HTTP client for communicating with a remote Spwig instance's Sync API.
Used by both Settings Sync and Full Migration features.
"""
import logging
import requests
from urllib.parse import urljoin
from django.utils.translation import gettext_lazy as _

from migration.models import SyncConnection

logger = logging.getLogger(__name__)


class SyncClientError(Exception):
    """Raised when a sync client operation fails."""
    pass


class SyncClientConnectionError(SyncClientError):
    """Raised when unable to connect to remote instance."""
    pass


class SyncClientAuthError(SyncClientError):
    """Raised when authentication with remote instance fails."""
    pass


class SpwigSyncClient:
    """
    HTTP client for communicating with a remote Spwig instance's Sync API.
    Handles authentication, retries, and error handling.
    """

    SYNC_API_PREFIX = '/api/sync/'

    def __init__(self, connection: SyncConnection):
        self.connection = connection
        self.base_url = connection.remote_url.rstrip('/')
        self.token = connection.auth_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'SyncToken {self.token}',
            'Accept': 'application/json',
            'User-Agent': 'SpwigSyncClient/1.0',
        })
        self.timeout = (10, 300)  # (connect, read) seconds

    def _url(self, path):
        """Build full URL for an API endpoint."""
        return urljoin(self.base_url, f'{self.SYNC_API_PREFIX}{path.lstrip("/")}')

    def _request(self, method, path, **kwargs):
        """
        Make an authenticated request to the remote Sync API.
        Handles common error responses.
        """
        url = self._url(path)
        kwargs.setdefault('timeout', self.timeout)

        try:
            response = self.session.request(method, url, **kwargs)
        except requests.ConnectionError as e:
            raise SyncClientConnectionError(
                f"Cannot connect to {self.base_url}: {e}"
            )
        except requests.Timeout:
            raise SyncClientConnectionError(
                f"Connection to {self.base_url} timed out"
            )
        except requests.RequestException as e:
            raise SyncClientError(f"Request failed: {e}")

        # Handle auth errors
        if response.status_code == 401:
            raise SyncClientAuthError("Authentication failed. Check the sync token.")
        if response.status_code == 403:
            raise SyncClientAuthError("Access denied. The sync token may lack permissions.")

        # Handle server errors
        if response.status_code >= 500:
            raise SyncClientError(
                f"Remote server error ({response.status_code}): {response.text[:500]}"
            )

        return response

    def _get_json(self, path, **kwargs):
        """GET request that returns JSON."""
        response = self._request('GET', path, **kwargs)
        if response.status_code != 200:
            raise SyncClientError(
                f"Unexpected response ({response.status_code}): {response.text[:500]}"
            )
        return response.json()

    def _post_json(self, path, data=None, **kwargs):
        """POST request with JSON body that returns JSON."""
        response = self._request('POST', path, json=data, **kwargs)
        if response.status_code not in (200, 201):
            raise SyncClientError(
                f"Unexpected response ({response.status_code}): {response.text[:500]}"
            )
        return response.json()

    # ---- Instance Info ----

    def test_connection(self):
        """
        Test connectivity and authentication with the remote instance.

        Returns:
            dict: Remote instance info (version, site_name, categories)
        """
        try:
            return self.get_info()
        except SyncClientError:
            raise
        except Exception as e:
            raise SyncClientConnectionError(f"Connection test failed: {e}")

    def get_info(self):
        """
        Get remote instance information.

        Returns:
            dict: {version, site_name, categories: [...]}
        """
        return self._get_json('info/')

    # ---- Export (read from remote) ----

    def export_category(self, category, page=1, per_page=100, credential_mode='redact'):
        """
        Export data for a specific category from the remote instance.

        Args:
            category: Category key (e.g., 'email_config')
            page: Page number for paginated results
            per_page: Items per page
            credential_mode: 'redact', 'decrypt', or 'skip'

        Returns:
            dict: {items: [...], total: int, page: int, pages: int}
                  or {data: {...}} for singleton categories
        """
        return self._get_json(
            f'export/{category}/',
            params={
                'page': page,
                'per_page': per_page,
                'credential_mode': credential_mode,
            }
        )

    def export_category_all(self, category, credential_mode='redact'):
        """
        Export all data for a category, handling pagination automatically.

        For collection categories, yields individual items across all pages.
        For singleton categories, yields a single dict with the data.

        Yields:
            dict: Individual items from the export
        """
        page = 1
        first_result = self.export_category(
            category, page=page, credential_mode=credential_mode
        )

        # Singleton categories return {data: {...}} instead of {items: [...]}
        if 'data' in first_result and 'items' not in first_result:
            yield first_result['data']
            return

        items = first_result.get('items', [])
        if not items:
            return
        yield from items

        total_pages = first_result.get('pages', 1)
        page += 1
        while page <= total_pages:
            result = self.export_category(
                category, page=page, credential_mode=credential_mode
            )
            items = result.get('items', [])
            if not items:
                break
            yield from items
            page += 1

    def export_count(self, category):
        """
        Get item count for a category on the remote instance.

        Returns:
            int: Number of items
        """
        result = self._get_json(f'export/{category}/count/')
        return result.get('count', 0)

    def stream_media(self, asset_id):
        """
        Stream a media file from the remote instance.

        Args:
            asset_id: Media asset ID on the remote instance

        Returns:
            requests.Response: Streaming response with file content
        """
        return self._request(
            'GET',
            f'export/media/{asset_id}/',
            stream=True,
            timeout=(10, 600)  # longer timeout for media
        )

    # ---- Import (write to remote) ----

    def import_category(self, category, data):
        """
        Import data for a specific category into the remote instance.

        Args:
            category: Category key
            data: dict with items to import

        Returns:
            dict: Import results {synced, skipped, failed, errors}
        """
        return self._post_json(f'import/{category}/', data=data)

    def preview_import(self, category, data):
        """
        Dry-run import to get diff preview without applying changes.

        Args:
            category: Category key
            data: dict with items to preview

        Returns:
            dict: Structured diff {changes: [...], warnings: [...]}
        """
        return self._post_json(f'import/{category}/preview/', data=data)

    def upload_media(self, file_data, metadata):
        """
        Upload a media file to the remote instance.

        Args:
            file_data: File-like object or bytes
            metadata: dict with file metadata (filename, content_type, etc.)

        Returns:
            dict: Upload result {id, path}
        """
        response = self._request(
            'POST',
            'import/media/',
            files={'file': (metadata.get('filename', 'upload'), file_data)},
            data=metadata,
            timeout=(10, 600)
        )
        if response.status_code not in (200, 201):
            raise SyncClientError(
                f"Media upload failed ({response.status_code}): {response.text[:500]}"
            )
        return response.json()

    # ---- Pre-flight (full migration) ----

    def get_preflight_info(self):
        """
        Get pre-flight information from the remote instance.

        Returns:
            dict: {components, counts, media_size, disk_usage}
        """
        return self._get_json('preflight/')

    # ---- Categories ----

    def get_categories(self):
        """
        List available sync categories on the remote instance.

        Returns:
            list: Available category keys with metadata
        """
        return self._get_json('categories/')
