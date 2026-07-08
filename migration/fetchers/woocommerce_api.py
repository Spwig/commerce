"""
WooCommerce REST API v3 client with rate limiting and pagination
"""
import requests
from requests.auth import HTTPBasicAuth
import time
import logging
from typing import List, Dict, Callable, Optional
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class WooCommerceAPIClient:
    """
    WooCommerce REST API v3 client

    Features:
    - Automatic pagination handling
    - Rate limiting (respects X-WC-Store-API-* headers)
    - Retry logic with exponential backoff
    - Progress callbacks for TQDM integration
    """

    def __init__(self, store_url: str, consumer_key: str, consumer_secret: str, timeout: int = 30):
        """
        Initialize WooCommerce API client

        Args:
            store_url: Store URL (e.g., https://yourstore.com)
            consumer_key: WooCommerce REST API consumer key (ck_xxx)
            consumer_secret: WooCommerce REST API consumer secret (cs_xxx)
            timeout: Request timeout in seconds
        """
        self.store_url = store_url.rstrip('/')
        self.base_url = f"{self.store_url}/wp-json/wc/v3"
        self.auth = HTTPBasicAuth(consumer_key, consumer_secret)
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = self.auth

        # Rate limiting
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
        self.last_request_time = 0
        self.min_request_interval = 0.1  # Minimum 100ms between requests

    def test_connection(self) -> dict:
        """
        Test API connection with a short timeout (no retries).

        Returns:
            dict with 'success' (bool) and optionally 'error' (str)
        """
        url = f"{self.base_url}/system_status"
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return {'success': True}
            elif response.status_code == 401:
                return {'success': False, 'error': 'Invalid API credentials (401 Unauthorized)'}
            elif response.status_code == 403:
                return {'success': False, 'error': 'Access denied. Check API key permissions (403 Forbidden)'}
            elif response.status_code == 404:
                return {'success': False, 'error': 'WooCommerce REST API not found (404). Is WooCommerce installed and active?'}
            else:
                return {'success': False, 'error': f'Unexpected response from store (HTTP {response.status_code})'}
        except requests.exceptions.SSLError as e:
            logger.error(f"Connection test SSL error: {e}")
            return {'success': False, 'error': f'SSL certificate error connecting to store. Ensure the URL uses a valid HTTPS certificate.'}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection test connection error: {e}")
            return {'success': False, 'error': 'Cannot connect to store. Please check the URL is correct and the store is online.'}
        except requests.exceptions.Timeout:
            logger.error(f"Connection test timed out for {url}")
            return {'success': False, 'error': 'Connection timed out (10s). Is the store URL correct and the site responsive?'}
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {'success': False, 'error': str(e)}

    def get_api_version(self) -> Optional[str]:
        """
        Get WooCommerce API version

        Returns:
            str: API version (e.g., 'wc/v3')
        """
        try:
            response = self._request('GET', '/')
            data = response.json()
            return data.get('namespace', 'unknown')
        except:
            return None

    # Paginated fetch methods

    def fetch_all_categories(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Fetch all product categories with pagination

        Args:
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of category dictionaries
        """
        return self._fetch_all_paginated('/products/categories', progress_callback)

    def fetch_all_products(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Fetch all products with pagination

        Args:
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of product dictionaries
        """
        return self._fetch_all_paginated('/products', progress_callback)

    def fetch_all_customers(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Fetch all customers with pagination

        Args:
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of customer dictionaries
        """
        return self._fetch_all_paginated('/customers', progress_callback)

    def fetch_all_orders(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Fetch all orders with pagination

        Args:
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of order dictionaries
        """
        return self._fetch_all_paginated('/orders', progress_callback)

    def fetch_all_coupons(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Fetch all coupons with pagination

        Args:
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of coupon dictionaries
        """
        return self._fetch_all_paginated('/coupons', progress_callback)

    def fetch_all_reviews(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Fetch all product reviews with pagination

        Args:
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of review dictionaries
        """
        return self._fetch_all_paginated('/products/reviews', progress_callback)

    # Single page fetch methods

    def fetch_categories(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        """Fetch categories (single page)"""
        return self._fetch_page('/products/categories', page, per_page)

    def fetch_products(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        """Fetch products (single page)"""
        return self._fetch_page('/products', page, per_page)

    def fetch_customers(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        """Fetch customers (single page)"""
        return self._fetch_page('/customers', page, per_page)

    def fetch_orders(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        """Fetch orders (single page)"""
        return self._fetch_page('/orders', page, per_page)

    def fetch_coupons(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        """Fetch coupons (single page)"""
        return self._fetch_page('/coupons', page, per_page)

    def fetch_reviews(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        """Fetch product reviews (single page)"""
        return self._fetch_page('/products/reviews', page, per_page)

    # Product variation methods

    def fetch_all_product_variations(
        self,
        product_id: int,
        progress_callback: Optional[Callable] = None
    ) -> List[Dict]:
        """
        Fetch all variations for a specific product with pagination.

        WooCommerce endpoint: GET /products/{product_id}/variations

        Args:
            product_id: WooCommerce product ID
            progress_callback: Optional callback(current, total) for progress tracking

        Returns:
            List of variation dictionaries
        """
        endpoint = f'/products/{product_id}/variations'
        return self._fetch_all_paginated(endpoint, progress_callback)

    def fetch_product_variations(
        self,
        product_id: int,
        page: int = 1,
        per_page: int = 100
    ) -> List[Dict]:
        """
        Fetch variations for a product (single page).

        Args:
            product_id: WooCommerce product ID
            page: Page number (1-indexed)
            per_page: Items per page (max 100)

        Returns:
            List of variation dictionaries
        """
        endpoint = f'/products/{product_id}/variations'
        return self._fetch_page(endpoint, page, per_page)

    # Core methods

    def _fetch_page(self, endpoint: str, page: int, per_page: int) -> List[Dict]:
        """
        Fetch a single page of results

        Args:
            endpoint: API endpoint (e.g., '/products')
            page: Page number (1-indexed)
            per_page: Items per page (max 100)

        Returns:
            List of items
        """
        params = {
            'page': page,
            'per_page': min(per_page, 100)  # WooCommerce max is 100
        }

        response = self._request('GET', endpoint, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch {endpoint} page {page}: {response.status_code}")
            return []

    def _fetch_all_paginated(self, endpoint: str, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Fetch all items with automatic pagination

        Uses WooCommerce pagination headers:
        - X-WP-Total: Total number of items
        - X-WP-TotalPages: Total number of pages

        Args:
            endpoint: API endpoint
            progress_callback: Optional callback(current, total)

        Returns:
            List of all items
        """
        all_items = []
        page = 1
        per_page = 100  # Max allowed by WooCommerce
        total_items = None
        total_pages = None

        while True:
            params = {
                'page': page,
                'per_page': per_page
            }

            response = self._request('GET', endpoint, params=params)

            if response.status_code != 200:
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

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None,
                 max_retries: int = 3) -> requests.Response:
        """
        Make HTTP request with retry logic and rate limiting

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

                # Update rate limit info
                self._update_rate_limit_info(response)

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
                    logger.warning(f"Request timeout. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
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
        """Wait if needed to respect rate limits"""
        # Minimum interval between requests
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        # WooCommerce rate limit (if we have info)
        if self.rate_limit_remaining is not None and self.rate_limit_remaining <= 5:
            # Low on requests, slow down
            logger.debug(f"Rate limit low ({self.rate_limit_remaining} remaining), slowing down")
            time.sleep(1)

    def _update_rate_limit_info(self, response: requests.Response):
        """
        Update rate limit info from response headers

        WooCommerce provides these headers:
        - X-WC-Store-API-Rate-Limit-Remaining: Requests remaining
        - X-WC-Store-API-Rate-Limit-Reset: Reset timestamp
        """
        remaining = response.headers.get('X-WC-Store-API-Rate-Limit-Remaining')
        reset = response.headers.get('X-WC-Store-API-Rate-Limit-Reset')

        if remaining:
            self.rate_limit_remaining = int(remaining)

        if reset:
            self.rate_limit_reset = int(reset)

        if remaining and self.rate_limit_remaining < 10:
            logger.warning(f"Rate limit warning: {self.rate_limit_remaining} requests remaining")

    def get_total_counts(self) -> Dict[str, int]:
        """
        Get total counts for all data types

        Makes HEAD requests to get totals without fetching data

        Returns:
            Dict with counts: {
                'products': 153,
                'categories': 49,
                'customers': 70,
                'orders': 216,
                'coupons': 5
            }
        """
        counts = {}

        endpoints = [
            'products',
            'products/categories',
            'customers',
            'orders',
            'coupons',
            'products/reviews'
        ]

        for endpoint in endpoints:
            try:
                response = self.session.head(
                    f"{self.base_url}/{endpoint}",
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    total = int(response.headers.get('X-WP-Total', 0))
                    # Normalize key (remove 'products/' prefix)
                    key = endpoint.split('/')[-1]
                    counts[key] = total
                else:
                    counts[endpoint.split('/')[-1]] = 0

            except Exception as e:
                logger.error(f"Failed to get count for {endpoint}: {e}")
                counts[endpoint.split('/')[-1]] = 0

        return counts
