"""
WordPress REST API client for blog content migration.

This client fetches blog posts, categories, tags, and media from WordPress sites.
It uses the WordPress REST API (wp-json/wp/v2) which is separate from WooCommerce API.
"""
import requests
from requests.auth import HTTPBasicAuth
import time
import logging
from typing import List, Dict, Callable, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class WordPressAPIClient:
    """
    WordPress REST API client for fetching blog content.

    Features:
    - Automatic pagination handling (X-WP-Total, X-WP-TotalPages headers)
    - Rate limiting with respectful delays
    - Progress callbacks for TQDM integration
    - Optional authentication for private posts
    """

    def __init__(
        self,
        site_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize WordPress API client.

        Args:
            site_url: WordPress site URL (e.g., https://example.com)
            username: Optional WordPress username (for private content)
            password: Optional application password (WordPress 5.6+)
            timeout: Request timeout in seconds
        """
        self.site_url = site_url.rstrip('/')
        self.base_url = f"{self.site_url}/wp-json/wp/v2"
        self.timeout = timeout
        self.session = requests.Session()

        # Set up authentication if provided
        if username and password:
            self.session.auth = HTTPBasicAuth(username, password)

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # Minimum 100ms between requests

        # Cache the source domain for image filtering
        parsed = urlparse(self.site_url)
        self.source_domain = parsed.netloc

    def test_connection(self) -> bool:
        """
        Test API connection by fetching site info.

        Returns:
            bool: True if connection successful
        """
        try:
            response = self._request('GET', '')
            return response.status_code == 200
        except Exception as e:
            logger.error(f"WordPress connection test failed: {e}")
            return False

    def get_source_domain(self) -> str:
        """
        Get the source domain for image filtering.

        Returns:
            str: Domain name (e.g., 'example.com')
        """
        return self.source_domain

    def get_total_counts(self) -> Dict[str, int]:
        """
        Get total counts for posts, categories, and tags.

        Returns:
            Dict with counts: {'posts': 50, 'categories': 10, 'tags': 25}
        """
        counts = {}

        endpoints = {
            'posts': '/posts',
            'categories': '/categories',
            'tags': '/tags',
        }

        for key, endpoint in endpoints.items():
            try:
                response = self.session.head(
                    f"{self.base_url}{endpoint}",
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    counts[key] = int(response.headers.get('X-WP-Total', 0))
                else:
                    counts[key] = 0
            except Exception as e:
                logger.error(f"Failed to get count for {key}: {e}")
                counts[key] = 0

        return counts

    # Paginated fetch methods

    def fetch_all_posts(
        self,
        progress_callback: Optional[Callable] = None,
        status: str = 'publish'
    ) -> List[Dict]:
        """
        Fetch all blog posts with pagination.

        Args:
            progress_callback: Optional callback(current, total) for progress tracking
            status: Post status filter ('publish', 'draft', 'any')

        Returns:
            List of post dictionaries
        """
        params = {'status': status} if status != 'any' else {}
        return self._fetch_all_paginated('/posts', progress_callback, extra_params=params)

    def fetch_all_categories(
        self,
        progress_callback: Optional[Callable] = None
    ) -> List[Dict]:
        """
        Fetch all blog categories with pagination.

        Args:
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of category dictionaries
        """
        return self._fetch_all_paginated('/categories', progress_callback)

    def fetch_all_tags(
        self,
        progress_callback: Optional[Callable] = None
    ) -> List[Dict]:
        """
        Fetch all blog tags with pagination.

        Args:
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of tag dictionaries
        """
        return self._fetch_all_paginated('/tags', progress_callback)

    # Single item fetch methods

    def fetch_media(self, media_id: int) -> Optional[Dict]:
        """
        Fetch a single media item (for featured images).

        Args:
            media_id: WordPress media attachment ID

        Returns:
            Media dictionary or None if not found
        """
        try:
            response = self._request('GET', f'/media/{media_id}')
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Media {media_id} not found: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Failed to fetch media {media_id}: {e}")
            return None

    def fetch_post(self, post_id: int) -> Optional[Dict]:
        """
        Fetch a single post by ID.

        Args:
            post_id: WordPress post ID

        Returns:
            Post dictionary or None if not found
        """
        try:
            response = self._request('GET', f'/posts/{post_id}')
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Post {post_id} not found: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Failed to fetch post {post_id}: {e}")
            return None

    def fetch_category(self, category_id: int) -> Optional[Dict]:
        """
        Fetch a single category by ID.

        Args:
            category_id: WordPress category ID

        Returns:
            Category dictionary or None if not found
        """
        try:
            response = self._request('GET', f'/categories/{category_id}')
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to fetch category {category_id}: {e}")
            return None

    def fetch_tag(self, tag_id: int) -> Optional[Dict]:
        """
        Fetch a single tag by ID.

        Args:
            tag_id: WordPress tag ID

        Returns:
            Tag dictionary or None if not found
        """
        try:
            response = self._request('GET', f'/tags/{tag_id}')
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to fetch tag {tag_id}: {e}")
            return None

    # Core methods

    def _fetch_all_paginated(
        self,
        endpoint: str,
        progress_callback: Optional[Callable] = None,
        extra_params: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Fetch all items with automatic pagination.

        Uses WordPress pagination headers:
        - X-WP-Total: Total number of items
        - X-WP-TotalPages: Total number of pages

        Args:
            endpoint: API endpoint (e.g., '/posts')
            progress_callback: Optional callback(current, total)
            extra_params: Additional query parameters

        Returns:
            List of all items
        """
        all_items = []
        page = 1
        per_page = 100  # WordPress default max
        total_items = None
        total_pages = None

        while True:
            params = {
                'page': page,
                'per_page': per_page,
                **(extra_params or {})
            }

            response = self._request('GET', endpoint, params=params)

            if response.status_code != 200:
                if response.status_code == 400 and page > 1:
                    # Likely "rest_post_invalid_page_number" - we've gone past the end
                    break
                logger.error(f"Failed to fetch {endpoint} page {page}: {response.status_code}")
                break

            # Get pagination info from headers
            if total_items is None:
                total_items = int(response.headers.get('X-WP-Total', 0))
                total_pages = int(response.headers.get('X-WP-TotalPages', 1))
                logger.info(f"Fetching {total_items} items from {endpoint} ({total_pages} pages)")

            # Get items from this page
            items = response.json()
            if not items:
                break

            all_items.extend(items)

            # Update progress
            if progress_callback:
                progress_callback(len(all_items), total_items)

            # Check if we have more pages
            if page >= total_pages:
                break

            page += 1

        logger.info(f"Fetched {len(all_items)} items from {endpoint}")
        return all_items

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        max_retries: int = 3
    ) -> requests.Response:
        """
        Make HTTP request with retry logic and rate limiting.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            max_retries: Maximum number of retry attempts

        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"

        for attempt in range(max_retries):
            try:
                # Rate limiting: wait if needed
                self._rate_limit_wait()

                # Make request
                response = self.session.request(
                    method,
                    url,
                    params=params,
                    timeout=self.timeout
                )

                # Update last request time
                self.last_request_time = time.time()

                # Handle rate limiting (429 status)
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue

                # Success or non-retryable error
                return response

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(
                        f"Request timeout. Retrying in {wait_time}s... "
                        f"(attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Request timeout after {max_retries} attempts")
                    raise

            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Connection error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Connection error after {max_retries} attempts")
                    raise

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise

        # Should not reach here
        raise Exception(f"Failed to complete request after {max_retries} attempts")

    def _rate_limit_wait(self):
        """Wait if needed to respect rate limits."""
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
