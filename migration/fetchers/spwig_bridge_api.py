"""
Spwig Migration Bridge API client for affiliate data migration.

This client fetches affiliate data (affiliates, commissions, plans, payouts)
from WordPress sites with the Spwig Migration Bridge plugin installed.
It uses query string auth with WooCommerce consumer keys.
"""

import logging
import time
from collections.abc import Callable

import requests

logger = logging.getLogger(__name__)


class SpwigBridgeAPIClient:
    """
    Spwig Migration Bridge REST API client for fetching affiliate data.

    Features:
    - Query string authentication (WooCommerce consumer key/secret)
    - Automatic pagination handling (X-WP-Total, X-WP-TotalPages headers)
    - Rate limiting with respectful delays
    - Progress callbacks for TQDM integration
    """

    def __init__(self, store_url: str, consumer_key: str, consumer_secret: str, timeout: int = 30):
        self.store_url = store_url.rstrip("/")
        self.base_url = f"{self.store_url}/wp-json/spwig/v1"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests

    def test_connection(self) -> dict:
        """
        Test connection by probing /spwig/v1/info.

        Returns:
            dict with plugin info if successful, or raises exception
        """
        response = self._request("GET", "/info")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ConnectionError(
                "Spwig Migration Bridge plugin not found. "
                "Please install and activate the plugin on your WordPress site."
            )
        elif response.status_code in (401, 403):
            raise ConnectionError(
                "Authentication failed. Please check your WooCommerce API keys "
                "have at least 'Read' permissions."
            )
        else:
            raise ConnectionError(
                f"Bridge plugin returned status {response.status_code}: {response.text[:200]}"
            )

    def get_info(self) -> dict:
        """
        Get full bridge info including detected plugin and record counts.

        Returns:
            dict: {detected_plugin, plugin_name, plugin_version, counts, store_currency}
        """
        response = self._request("GET", "/info")
        if response.status_code == 200:
            return response.json()
        return {}

    def fetch_all_affiliates(self, progress_callback: Callable | None = None) -> list[dict]:
        return self._fetch_all_paginated("/affiliates", progress_callback)

    def fetch_all_referrals(self, progress_callback: Callable | None = None) -> list[dict]:
        return self._fetch_all_paginated("/referrals", progress_callback)

    def fetch_all_plans(self, progress_callback: Callable | None = None) -> list[dict]:
        return self._fetch_all_paginated("/plans", progress_callback)

    def fetch_all_payouts(self, progress_callback: Callable | None = None) -> list[dict]:
        return self._fetch_all_paginated("/payouts", progress_callback)

    # Core methods

    def _fetch_all_paginated(
        self, endpoint: str, progress_callback: Callable | None = None
    ) -> list[dict]:
        """
        Fetch all items with automatic pagination.

        Uses WordPress pagination headers:
        - X-WP-Total: Total number of items
        - X-WP-TotalPages: Total number of pages

        Args:
            endpoint: API endpoint (e.g., '/affiliates')
            progress_callback: Optional callback(current, total)

        Returns:
            List of all items
        """
        all_items = []
        page = 1
        per_page = 100  # Bridge plugin max
        total_items = None
        total_pages = None

        while True:
            params = {
                "page": page,
                "per_page": per_page,
            }

            response = self._request("GET", endpoint, params=params)

            if response.status_code != 200:
                if response.status_code == 400 and page > 1:
                    break
                logger.error(f"Failed to fetch {endpoint} page {page}: {response.status_code}")
                break

            if total_items is None:
                total_items = int(response.headers.get("X-WP-Total", 0))
                total_pages = int(response.headers.get("X-WP-TotalPages", 1))
                logger.info(f"Fetching {total_items} items from {endpoint} ({total_pages} pages)")

            items = response.json()
            if not items:
                break

            all_items.extend(items)

            if progress_callback:
                progress_callback(len(all_items), total_items)

            if page >= total_pages:
                break

            page += 1

        logger.info(f"Fetched {len(all_items)} items from {endpoint}")
        return all_items

    def _request(
        self, method: str, endpoint: str, params: dict | None = None, max_retries: int = 3
    ) -> requests.Response:
        """
        Make HTTP request with query string auth, retry logic, and rate limiting.
        """
        url = f"{self.base_url}{endpoint}"

        # Add WC consumer key auth to query params
        auth_params = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
        }
        if params:
            auth_params.update(params)

        for attempt in range(max_retries):
            try:
                self._rate_limit_wait()

                response = self.session.request(
                    method, url, params=auth_params, timeout=self.timeout
                )

                self.last_request_time = time.time()

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue

                return response

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    logger.warning(
                        f"Request timeout. Retrying in {wait_time}s... "
                        f"(attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(wait_time)
                else:
                    raise

            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    logger.warning(f"Connection error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise

            except Exception:
                raise

        raise Exception(f"Failed to complete request after {max_retries} attempts")

    def _rate_limit_wait(self):
        """Wait if needed to respect rate limits."""
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
