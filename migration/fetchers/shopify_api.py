"""
Shopify Admin API client with token exchange, rate limiting, and cursor pagination.

Auth: Client credentials grant (Dev Dashboard app).
Rate limiting: Leaky bucket via X-Shopify-Shop-Api-Call-Limit header.
Pagination: Cursor-based via Link header with rel="next".
"""
import requests
import time
import logging
import re
from typing import List, Dict, Callable, Optional

logger = logging.getLogger(__name__)


class ShopifyAPIClient:
    """
    Shopify Admin API client for migration.

    Features:
    - Client credentials token exchange with 24h auto-refresh
    - Cursor-based pagination via Link header
    - Leaky bucket rate limiting (40 req/app/store)
    - Retry logic with exponential backoff
    - Progress callbacks for tqdm integration
    """

    def __init__(self, store_domain: str, client_id: str, client_secret: str,
                 api_version: str = '2025-01', timeout: int = 30):
        """
        Args:
            store_domain: Shopify store domain (e.g., yourstore.myshopify.com)
            client_id: Dev Dashboard app Client ID
            client_secret: Dev Dashboard app Client Secret
            api_version: Shopify API version (e.g., '2025-01')
            timeout: Request timeout in seconds
        """
        self.store_domain = store_domain.strip().rstrip('/')
        # Strip protocol if provided
        if self.store_domain.startswith('https://'):
            self.store_domain = self.store_domain[8:]
        elif self.store_domain.startswith('http://'):
            self.store_domain = self.store_domain[7:]

        self.client_id = client_id.strip()
        self.client_secret = client_secret.strip()
        self.api_version = api_version
        self.timeout = timeout
        self.base_url = f"https://{self.store_domain}/admin/api/{self.api_version}"

        self.session = requests.Session()

        # Token management
        self._access_token = None
        self._token_expires_at = 0

        # Rate limiting (Shopify leaky bucket: 40 requests max)
        self._bucket_used = 0
        self._bucket_max = 40
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests

    # ──────────────────────────────────────────────
    # Token management
    # ──────────────────────────────────────────────

    def _ensure_token(self):
        """Exchange or refresh the access token if needed."""
        if self._access_token and time.time() < (self._token_expires_at - 60):
            return  # Token is still valid (with 60s buffer)

        logger.info("Exchanging client credentials for access token...")
        url = f"https://{self.store_domain}/admin/oauth/access_token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        try:
            response = requests.post(url, data=data, timeout=15)
            if response.status_code == 200:
                result = response.json()
                self._access_token = result['access_token']
                expires_in = result.get('expires_in', 86399)
                self._token_expires_at = time.time() + expires_in
                self.session.headers['X-Shopify-Access-Token'] = self._access_token
                logger.info(f"Access token obtained (expires in {expires_in}s)")
            else:
                error_body = response.text[:500]
                logger.error(f"Token exchange failed ({response.status_code}): {error_body}")
                raise ConnectionError(
                    f"Failed to exchange credentials for access token (HTTP {response.status_code}). "
                    f"Verify your Client ID and Secret are correct."
                )
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to {self.store_domain}. "
                f"Check the store domain is correct and the store is online."
            )

    # ──────────────────────────────────────────────
    # Connection testing
    # ──────────────────────────────────────────────

    def test_connection(self) -> dict:
        """
        Test API connection: exchange token + fetch shop info.

        Returns:
            dict with 'success' (bool), optionally 'error' (str) and 'shop_info' (dict)
        """
        try:
            self._ensure_token()
        except ConnectionError as e:
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Token exchange failed: {e}")
            return {'success': False, 'error': f'Failed to authenticate: {e}'}

        try:
            response = self.session.get(
                f"{self.base_url}/shop.json",
                timeout=10
            )
            if response.status_code == 200:
                shop_data = response.json().get('shop', {})
                return {
                    'success': True,
                    'shop_info': {
                        'name': shop_data.get('name', ''),
                        'email': shop_data.get('email', ''),
                        'domain': shop_data.get('domain', ''),
                        'plan_name': shop_data.get('plan_name', ''),
                        'currency': shop_data.get('currency', 'USD'),
                    }
                }
            elif response.status_code == 401:
                return {'success': False, 'error': 'Invalid access token (401 Unauthorized). Check your Client ID and Secret.'}
            elif response.status_code == 403:
                return {'success': False, 'error': 'Access denied (403 Forbidden). The app may not be installed on this store.'}
            elif response.status_code == 404:
                return {'success': False, 'error': f'Shopify Admin API not found (404). Check your store domain.'}
            else:
                return {'success': False, 'error': f'Unexpected response (HTTP {response.status_code})'}
        except requests.exceptions.SSLError:
            return {'success': False, 'error': 'SSL certificate error connecting to store.'}
        except requests.exceptions.ConnectionError:
            return {'success': False, 'error': 'Cannot connect to store. Check the domain is correct and the store is online.'}
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'Connection timed out. Is the store responsive?'}
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {'success': False, 'error': str(e)}

    def get_available_scopes(self) -> List[str]:
        """
        Get the access scopes granted to this token.

        Returns:
            List of scope strings (e.g., ['read_products', 'read_customers'])
        """
        self._ensure_token()
        try:
            response = self._request('GET', '/admin/oauth/access_scopes.json', use_base_url=False)
            if response.status_code == 200:
                scopes_data = response.json().get('access_scopes', [])
                return [s.get('handle', '') for s in scopes_data]
            return []
        except Exception as e:
            logger.error(f"Failed to fetch scopes: {e}")
            return []

    # ──────────────────────────────────────────────
    # Count methods
    # ──────────────────────────────────────────────

    def get_total_counts(self) -> Dict[str, int]:
        """
        Get total counts for all data types using count endpoints.

        Returns:
            Dict like {'products': 50, 'collections': 10, 'customers': 25, ...}
        """
        self._ensure_token()
        counts = {}

        count_endpoints = {
            'products': '/products/count.json',
            'custom_collections': '/custom_collections/count.json',
            'smart_collections': '/smart_collections/count.json',
            'customers': '/customers/count.json',
            'orders': '/orders/count.json',
            'articles': None,  # Requires iterating blogs
            'discounts': '/price_rules/count.json',
        }

        for key, endpoint in count_endpoints.items():
            if endpoint is None:
                continue
            try:
                # Orders default to status=open; pass status=any to count all
                params = {'status': 'any'} if key == 'orders' else None
                response = self._request('GET', endpoint, params=params)
                if response.status_code == 200:
                    counts[key] = response.json().get('count', 0)
                else:
                    counts[key] = 0
            except Exception as e:
                logger.warning(f"Failed to get count for {key}: {e}")
                counts[key] = 0

        # Combine collection counts
        counts['collections'] = counts.pop('custom_collections', 0) + counts.pop('smart_collections', 0)

        # Article count requires iterating blogs
        try:
            blogs = self.fetch_blogs()
            total_articles = 0
            for blog in blogs:
                response = self._request('GET', f"/blogs/{blog['id']}/articles/count.json")
                if response.status_code == 200:
                    total_articles += response.json().get('count', 0)
            counts['articles'] = total_articles
        except Exception as e:
            logger.warning(f"Failed to get article count: {e}")
            counts['articles'] = 0

        return counts

    # ──────────────────────────────────────────────
    # Paginated fetch methods (cursor-based)
    # ──────────────────────────────────────────────

    def fetch_all_products(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all products with cursor pagination."""
        return self._fetch_all_paginated('/products.json', 'products', progress_callback)

    def fetch_all_custom_collections(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all custom (manually curated) collections."""
        return self._fetch_all_paginated('/custom_collections.json', 'custom_collections', progress_callback)

    def fetch_all_smart_collections(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all smart (rule-based) collections."""
        return self._fetch_all_paginated('/smart_collections.json', 'smart_collections', progress_callback)

    def fetch_all_customers(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all customers with cursor pagination."""
        return self._fetch_all_paginated('/customers.json', 'customers', progress_callback)

    def fetch_all_orders(self, progress_callback: Optional[Callable] = None,
                         status: str = 'any') -> List[Dict]:
        """Fetch all orders with cursor pagination."""
        return self._fetch_all_paginated(
            '/orders.json', 'orders', progress_callback,
            extra_params={'status': status}
        )

    def fetch_all_price_rules(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all price rules (discount definitions)."""
        return self._fetch_all_paginated('/price_rules.json', 'price_rules', progress_callback)

    def fetch_discount_codes(self, price_rule_id: int) -> List[Dict]:
        """Fetch all discount codes for a price rule."""
        return self._fetch_all_paginated(
            f'/price_rules/{price_rule_id}/discount_codes.json',
            'discount_codes'
        )

    def fetch_blogs(self) -> List[Dict]:
        """Fetch all blogs (blog containers, not articles)."""
        return self._fetch_all_paginated('/blogs.json', 'blogs')

    def fetch_all_articles(self, blog_id: int,
                           progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all articles for a specific blog."""
        return self._fetch_all_paginated(
            f'/blogs/{blog_id}/articles.json', 'articles', progress_callback
        )

    # ──────────────────────────────────────────────
    # Single-page fetch methods (for previews)
    # ──────────────────────────────────────────────

    def fetch_products(self, limit: int = 5) -> List[Dict]:
        """Fetch a small sample of products for preview."""
        return self._fetch_page('/products.json', 'products', limit)

    def fetch_customers(self, limit: int = 5) -> List[Dict]:
        """Fetch a small sample of customers for preview."""
        return self._fetch_page('/customers.json', 'customers', limit)

    def fetch_orders(self, limit: int = 5) -> List[Dict]:
        """Fetch a small sample of orders for preview."""
        return self._fetch_page('/orders.json', 'orders', limit, extra_params={'status': 'any'})

    # ──────────────────────────────────────────────
    # Collection product assignments
    # ──────────────────────────────────────────────

    def fetch_collects(self, product_id: int = None,
                       collection_id: int = None) -> List[Dict]:
        """Fetch product-collection assignments.

        Args:
            product_id: Filter by product (which collections does this product belong to?)
            collection_id: Filter by collection (which products are in this collection?)
        """
        params = {}
        if product_id:
            params['product_id'] = product_id
        if collection_id:
            params['collection_id'] = collection_id
        return self._fetch_all_paginated(
            '/collects.json', 'collects',
            extra_params=params
        )

    # ──────────────────────────────────────────────
    # Core request methods
    # ──────────────────────────────────────────────

    def _fetch_page(self, endpoint: str, resource_key: str,
                    limit: int = 50, extra_params: Optional[Dict] = None) -> List[Dict]:
        """Fetch a single page of results."""
        self._ensure_token()
        params = {'limit': min(limit, 250)}
        if extra_params:
            params.update(extra_params)

        response = self._request('GET', endpoint, params=params)
        if response.status_code == 200:
            return response.json().get(resource_key, [])
        else:
            logger.error(f"Failed to fetch {endpoint}: {response.status_code}")
            return []

    def _fetch_all_paginated(self, endpoint: str, resource_key: str,
                             progress_callback: Optional[Callable] = None,
                             extra_params: Optional[Dict] = None) -> List[Dict]:
        """
        Fetch all items using Shopify cursor-based pagination.

        Shopify uses the Link header with rel="next" for pagination:
            Link: <https://store.myshopify.com/admin/api/.../products.json?page_info=xxx&limit=250>; rel="next"
        """
        self._ensure_token()
        all_items = []
        params = {'limit': 250}  # Shopify max per page
        if extra_params:
            params.update(extra_params)

        # First request: pass endpoint, let _request build full URL
        # Subsequent requests: use full URL from Link header
        next_url = None
        is_first = True

        while True:
            if is_first:
                response = self._request('GET', endpoint, params=params)
                is_first = False
            else:
                response = self._request('GET', next_url, is_full_url=True)

            if response.status_code != 200:
                logger.error(f"Failed to fetch {endpoint}: {response.status_code}")
                break

            data = response.json()
            items = data.get(resource_key, [])

            if not items:
                break

            all_items.extend(items)

            if progress_callback:
                progress_callback(len(all_items))

            # Get next page URL from Link header
            next_url = self._parse_next_link(response.headers.get('Link', ''))
            if not next_url:
                break
            # page_info is embedded in the next URL, so clear params
            params = None

        logger.info(f"Fetched {len(all_items)} items from {endpoint}")
        return all_items

    def _parse_next_link(self, link_header: str) -> Optional[str]:
        """
        Parse the next page URL from Shopify's Link header.

        Format: <URL>; rel="next", <URL>; rel="previous"
        """
        if not link_header:
            return None

        # Match rel="next" link
        match = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
        if match:
            return match.group(1)
        return None

    def _request(self, method: str, url_or_endpoint: str,
                 params: Optional[Dict] = None,
                 max_retries: int = 3,
                 is_full_url: bool = False,
                 use_base_url: bool = True) -> requests.Response:
        """
        Make HTTP request with retry logic and rate limiting.

        Args:
            method: HTTP method
            url_or_endpoint: Full URL or API endpoint
            params: Query parameters
            max_retries: Retry attempts
            is_full_url: If True, url_or_endpoint is a complete URL
            use_base_url: If False, use store root instead of versioned API base
        """
        if is_full_url:
            url = url_or_endpoint
        elif use_base_url:
            url = f"{self.base_url}{url_or_endpoint}"
        else:
            url = f"https://{self.store_domain}{url_or_endpoint}"

        for attempt in range(max_retries):
            try:
                self._rate_limit_wait()

                response = self.session.request(
                    method, url, params=params, timeout=self.timeout
                )

                self._update_rate_limit_info(response)
                self.last_request_time = time.time()

                if response.status_code == 429:
                    retry_after = float(response.headers.get('Retry-After', 2.0))
                    logger.warning(f"Rate limited. Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue

                return response

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Timeout. Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise

            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Connection error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise

            except Exception:
                raise

        raise Exception(f"Failed to complete request after {max_retries} attempts")

    def _rate_limit_wait(self):
        """Wait if needed to respect Shopify's leaky bucket rate limits."""
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        # Back off when bucket is nearly full
        if self._bucket_max > 0 and self._bucket_used >= (self._bucket_max - 2):
            logger.debug(f"Rate limit near capacity ({self._bucket_used}/{self._bucket_max}), backing off")
            time.sleep(1.0)

    def _update_rate_limit_info(self, response: requests.Response):
        """
        Update rate limit state from Shopify's response header.

        Header format: X-Shopify-Shop-Api-Call-Limit: 32/40
        """
        limit_header = response.headers.get('X-Shopify-Shop-Api-Call-Limit', '')
        if '/' in limit_header:
            try:
                parts = limit_header.split('/')
                self._bucket_used = int(parts[0])
                self._bucket_max = int(parts[1])
            except (ValueError, IndexError):
                pass

        if self._bucket_used > 0 and self._bucket_used >= (self._bucket_max - 5):
            logger.warning(f"Rate limit warning: {self._bucket_used}/{self._bucket_max} requests used")
