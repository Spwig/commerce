"""
Magento 2 REST API client with Bearer token auth, searchCriteria pagination,
and EAV attribute resolution.

Auth: Integration access token (Bearer).
Rate limiting: Configurable interval + 429 backoff (no built-in limits on most installs).
Pagination: searchCriteria[pageSize] + searchCriteria[currentPage] with total_count in body.
"""
import requests
import time
import logging
from typing import List, Dict, Callable, Optional
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class MagentoAPIClient:
    """
    Magento 2 REST API client for migration.

    Features:
    - Bearer token authentication (Integration access token)
    - searchCriteria-based pagination with total_count progress tracking
    - Configurable rate limiting (100ms default interval)
    - Retry logic with exponential backoff
    - EAV attribute option pre-fetching and caching
    - Progress callbacks for tqdm integration
    """

    PAGE_SIZE = 100  # Items per page (Magento default max is 300 when input limits enabled)

    def __init__(self, store_url: str, access_token: str, timeout: int = 30,
                 verify_ssl: bool = True):
        """
        Args:
            store_url: Magento store URL (e.g., https://yourstore.com)
            access_token: Integration access token from Magento admin
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates (disable for self-signed certs)
        """
        self.store_url = store_url.strip().rstrip('/')
        if not self.store_url.startswith('http'):
            self.store_url = f'https://{self.store_url}'

        self.access_token = access_token.strip()
        self.timeout = timeout
        self.base_url = f"{self.store_url}/rest/V1"

        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })

        # Connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=5, pool_maxsize=10
        )
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests

        # EAV attribute cache: {attribute_code: {option_id_str: label}}
        self._attribute_options_cache = {}
        self._attributes_loaded = False

    # ──────────────────────────────────────────────
    # Connection testing
    # ──────────────────────────────────────────────

    def test_connection(self) -> dict:
        """
        Test API connection by fetching store configuration.

        Returns:
            dict with 'success' (bool), optionally 'error' (str) and 'store_info' (dict)
        """
        try:
            response = self._request('GET', '/store/storeConfigs')

            if response.status_code == 200:
                configs = response.json()
                if isinstance(configs, list) and configs:
                    config = configs[0]
                    return {
                        'success': True,
                        'store_info': {
                            'name': config.get('base_url', ''),
                            'locale': config.get('locale', ''),
                            'currency': config.get('base_currency_code', 'USD'),
                            'timezone': config.get('timezone', ''),
                            'weight_unit': config.get('weight_unit', ''),
                        },
                        'shop_name': config.get('base_url', 'Magento Store'),
                    }
                return {
                    'success': True,
                    'store_info': {},
                    'shop_name': 'Magento Store',
                }
            elif response.status_code == 401:
                return {
                    'success': False,
                    'error': 'Invalid access token (401 Unauthorized). '
                             'Check your Integration access token is correct and active.'
                }
            elif response.status_code == 403:
                return {
                    'success': False,
                    'error': 'Access denied (403 Forbidden). '
                             'The Integration may not have sufficient API permissions.'
                }
            elif response.status_code == 404:
                return {
                    'success': False,
                    'error': 'Magento REST API not found (404). '
                             'Check your store URL and ensure Magento 2 is installed.'
                }
            else:
                return {
                    'success': False,
                    'error': f'Unexpected response (HTTP {response.status_code})'
                }
        except requests.exceptions.SSLError:
            return {'success': False, 'error': 'SSL certificate error connecting to store.'}
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Cannot connect to store. Check the URL is correct and the store is online.'
            }
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'Connection timed out. Is the store responsive?'}
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {'success': False, 'error': str(e)}

    def check_endpoint_access(self, endpoint: str) -> bool:
        """Check if the token has access to a specific endpoint."""
        try:
            params = self._build_search_criteria(page_size=1, current_page=1)
            response = self._request('GET', endpoint, params=params)
            return response.status_code == 200
        except Exception:
            return False

    # ──────────────────────────────────────────────
    # Count methods
    # ──────────────────────────────────────────────

    def get_total_counts(self) -> Dict[str, int]:
        """
        Get total counts for all data types.

        Returns:
            Dict like {'products': 150, 'categories': 25, 'customers': 80, ...}
        """
        counts = {}

        # Products (exclude visibility=1 children)
        try:
            params = self._build_search_criteria(page_size=1, current_page=1, filters=[
                ('visibility', '1', 'neq'),
            ])
            response = self._request('GET', '/products', params=params)
            if response.status_code == 200:
                counts['products'] = response.json().get('total_count', 0)
            else:
                counts['products'] = 0
        except Exception as e:
            logger.warning(f"Failed to get product count: {e}")
            counts['products'] = 0

        # Categories (tree endpoint, count manually)
        try:
            response = self._request('GET', '/categories')
            if response.status_code == 200:
                tree = response.json()
                counts['categories'] = self._count_categories(tree)
            else:
                counts['categories'] = 0
        except Exception as e:
            logger.warning(f"Failed to get category count: {e}")
            counts['categories'] = 0

        # Other entity types via searchCriteria with pageSize=1
        entity_endpoints = {
            'customers': '/customers/search',
            'orders': '/orders',
            'reviews': '/reviews',
            'coupons': '/salesRules/search',
            'cms_pages': '/cmsPage/search',
        }

        for key, endpoint in entity_endpoints.items():
            try:
                params = self._build_search_criteria(page_size=1, current_page=1)
                response = self._request('GET', endpoint, params=params)
                if response.status_code == 200:
                    counts[key] = response.json().get('total_count', 0)
                else:
                    counts[key] = 0
            except Exception as e:
                logger.warning(f"Failed to get count for {key}: {e}")
                counts[key] = 0

        return counts

    def _count_categories(self, node: dict) -> int:
        """Recursively count categories in the tree (excluding root id=1)."""
        count = 0
        if node.get('id', 0) > 1:
            count = 1
        for child in node.get('children_data', []):
            count += self._count_categories(child)
        return count

    # ──────────────────────────────────────────────
    # Paginated fetch methods (searchCriteria)
    # ──────────────────────────────────────────────

    def fetch_all_products(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all products, excluding visibility=1 (configurable children).

        Children of configurable products are fetched separately via
        fetch_configurable_children().
        """
        filters = [('visibility', '1', 'neq')]
        return self._fetch_all_paginated('/products', progress_callback, filters=filters)

    def fetch_configurable_children(self, parent_sku: str) -> List[Dict]:
        """Fetch child simple products of a configurable product."""
        try:
            response = self._request('GET', f'/configurable-products/{parent_sku}/children')
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Failed to fetch children for {parent_sku}: {response.status_code}"
                )
                return []
        except Exception as e:
            logger.warning(f"Failed to fetch children for {parent_sku}: {e}")
            return []

    def fetch_configurable_options(self, parent_sku: str) -> List[Dict]:
        """Fetch configurable product option definitions (which attributes are used)."""
        try:
            response = self._request(
                'GET', f'/configurable-products/{parent_sku}/options/all'
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logger.warning(f"Failed to fetch options for {parent_sku}: {e}")
            return []

    def fetch_all_categories(self) -> Dict:
        """Fetch the full category tree (single request, no pagination).

        Returns the root category node with nested children_data.
        """
        try:
            response = self._request('GET', '/categories')
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch categories: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"Failed to fetch categories: {e}")
            return {}

    def fetch_all_customers(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all customers with searchCriteria pagination."""
        return self._fetch_all_paginated('/customers/search', progress_callback)

    def fetch_all_orders(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all orders with searchCriteria pagination."""
        return self._fetch_all_paginated('/orders', progress_callback)

    def fetch_all_reviews(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all product reviews.

        Note: Magento Community Edition does not expose a REST API for reviews.
        This endpoint only works if a custom module or Magento Commerce (Adobe)
        provides the /V1/reviews route. Returns empty list if unavailable.
        """
        try:
            test_params = self._build_search_criteria(page_size=1, current_page=1)
            response = self._request('GET', '/reviews', params=test_params)
            if response.status_code == 404:
                logger.info(
                    "Reviews REST API not available (standard Magento Community "
                    "limitation). Skipping review migration."
                )
                return []
        except Exception:
            pass
        return self._fetch_all_paginated('/reviews', progress_callback)

    def fetch_all_sales_rules(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all cart price rules (sales rules)."""
        return self._fetch_all_paginated('/salesRules/search', progress_callback)

    def fetch_coupons_for_rule(self, rule_id: int) -> List[Dict]:
        """Fetch coupon codes associated with a sales rule."""
        filters = [('rule_id', str(rule_id), 'eq')]
        return self._fetch_all_paginated('/coupons/search', filters=filters)

    def fetch_all_cms_pages(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all CMS pages."""
        return self._fetch_all_paginated('/cmsPage/search', progress_callback)

    # ──────────────────────────────────────────────
    # EAV attribute resolution
    # ──────────────────────────────────────────────

    def load_attribute_options(self):
        """Pre-fetch all select/multiselect product attributes and their options.

        Builds self._attribute_options_cache = {attr_code: {option_id: label}}
        Call this once before processing products to avoid N+1 API calls.
        """
        if self._attributes_loaded:
            return

        logger.info("Pre-fetching Magento product attribute options...")

        # Fetch all product attributes
        all_attributes = self._fetch_all_paginated('/products/attributes')

        count = 0
        for attr in all_attributes:
            frontend_input = attr.get('frontend_input', '')
            if frontend_input in ('select', 'multiselect', 'swatch_visual', 'swatch_text'):
                code = attr.get('attribute_code', '')
                options = attr.get('options', [])
                if code and options:
                    option_map = {}
                    for opt in options:
                        opt_value = str(opt.get('value', ''))
                        opt_label = opt.get('label', '')
                        if opt_value and opt_label and opt_label.strip():
                            option_map[opt_value] = opt_label
                    if option_map:
                        self._attribute_options_cache[code] = option_map
                        count += 1

        self._attributes_loaded = True
        logger.info(f"Cached options for {count} product attributes")

    def get_attribute_options_cache(self) -> Dict[str, Dict[str, str]]:
        """Return the attribute options cache, loading it if needed."""
        if not self._attributes_loaded:
            self.load_attribute_options()
        return self._attribute_options_cache

    # ──────────────────────────────────────────────
    # Media URL construction
    # ──────────────────────────────────────────────

    def get_media_url(self, relative_path: str) -> str:
        """Construct full URL for a product image.

        Magento stores relative paths like "/w/s/wsh12-green_main.jpg".
        Full URL: {store_url}/media/catalog/product{relative_path}
        """
        if not relative_path:
            return ''
        if relative_path.startswith(('http://', 'https://')):
            return relative_path
        return f"{self.store_url}/media/catalog/product{relative_path}"

    # ──────────────────────────────────────────────
    # Preview methods (single page)
    # ──────────────────────────────────────────────

    def fetch_products(self, limit: int = 5) -> List[Dict]:
        """Fetch a small sample of products for preview."""
        params = self._build_search_criteria(page_size=limit, current_page=1, filters=[
            ('visibility', '1', 'neq'),
        ])
        try:
            response = self._request('GET', '/products', params=params)
            if response.status_code == 200:
                return response.json().get('items', [])
            return []
        except Exception:
            return []

    def fetch_customers(self, limit: int = 5) -> List[Dict]:
        """Fetch a small sample of customers for preview."""
        params = self._build_search_criteria(page_size=limit, current_page=1)
        try:
            response = self._request('GET', '/customers/search', params=params)
            if response.status_code == 200:
                return response.json().get('items', [])
            return []
        except Exception:
            return []

    def fetch_orders(self, limit: int = 5) -> List[Dict]:
        """Fetch a small sample of orders for preview."""
        params = self._build_search_criteria(page_size=limit, current_page=1)
        try:
            response = self._request('GET', '/orders', params=params)
            if response.status_code == 200:
                return response.json().get('items', [])
            return []
        except Exception:
            return []

    # ──────────────────────────────────────────────
    # Core request methods
    # ──────────────────────────────────────────────

    def _fetch_all_paginated(self, endpoint: str,
                             progress_callback: Optional[Callable] = None,
                             filters: Optional[List[tuple]] = None) -> List[Dict]:
        """
        Fetch all items using Magento searchCriteria pagination.

        Magento returns:
            {"items": [...], "total_count": N, "search_criteria": {...}}
        """
        all_items = []
        current_page = 1

        while True:
            params = self._build_search_criteria(
                page_size=self.PAGE_SIZE,
                current_page=current_page,
                filters=filters,
            )

            response = self._request('GET', endpoint, params=params)

            if response.status_code != 200:
                logger.error(f"Failed to fetch {endpoint}: {response.status_code}")
                break

            data = response.json()
            items = data.get('items', [])
            total_count = data.get('total_count', 0)

            if not items:
                break

            all_items.extend(items)

            if progress_callback:
                progress_callback(len(all_items))

            # Check if we've fetched all items
            if len(all_items) >= total_count:
                break

            current_page += 1

        logger.info(f"Fetched {len(all_items)} items from {endpoint}")
        return all_items

    def _build_search_criteria(self, page_size: int = 100,
                                current_page: int = 1,
                                filters: Optional[List[tuple]] = None,
                                sort_field: str = None,
                                sort_direction: str = 'ASC') -> Dict:
        """
        Build Magento searchCriteria query parameters.

        Args:
            page_size: Items per page
            current_page: Page number (1-based)
            filters: List of (field, value, condition_type) tuples
            sort_field: Field to sort by
            sort_direction: ASC or DESC

        Returns:
            Dict of query parameters
        """
        params = {
            'searchCriteria[pageSize]': page_size,
            'searchCriteria[currentPage]': current_page,
        }

        if filters:
            for i, (field, value, condition) in enumerate(filters):
                params[f'searchCriteria[filter_groups][{i}][filters][0][field]'] = field
                params[f'searchCriteria[filter_groups][{i}][filters][0][value]'] = value
                params[f'searchCriteria[filter_groups][{i}][filters][0][condition_type]'] = condition

        if sort_field:
            params['searchCriteria[sortOrders][0][field]'] = sort_field
            params['searchCriteria[sortOrders][0][direction]'] = sort_direction

        return params

    def _request(self, method: str, endpoint: str,
                 params: Optional[Dict] = None,
                 json_data: Optional[Dict] = None,
                 max_retries: int = 3) -> requests.Response:
        """
        Make HTTP request with retry logic and rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint (relative to /rest/V1)
            params: Query parameters
            json_data: JSON body for POST/PUT
            max_retries: Retry attempts
        """
        url = f"{self.base_url}{endpoint}"

        for attempt in range(max_retries):
            try:
                self._rate_limit_wait()

                response = self.session.request(
                    method, url, params=params, json=json_data,
                    timeout=self.timeout
                )

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
                    logger.warning(
                        f"Timeout. Retrying in {wait_time}s "
                        f"(attempt {attempt + 1}/{max_retries})"
                    )
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
        """Wait if needed to respect minimum request interval."""
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
