"""
Marketplace Service
Wraps upgrade server API calls for the marketplace browse/install experience.
Reuses UpdateManager for authentication and component installation.
"""

import logging

import requests
from django.core.cache import cache

from component_updates.models import ComponentRegistry, UpdateServerConfig
from component_updates.services import UpdateAuthenticationError, UpdateManager

logger = logging.getLogger(__name__)

CACHE_PREFIX = "marketplace"
BROWSE_CACHE_TTL = 120  # 2 minutes
DETAIL_CACHE_TTL = 300  # 5 minutes
TYPES_CACHE_TTL = 600  # 10 minutes


class MarketplaceService:
    """
    Service layer for marketplace operations.
    Delegates to the upgrade server internal API for data
    and to UpdateManager for component installation.
    """

    def __init__(self):
        self.config = UpdateServerConfig.get_instance()
        self._update_manager = None

    @property
    def update_manager(self):
        if self._update_manager is None:
            self._update_manager = UpdateManager()
        return self._update_manager

    def _get_internal_api_url(self, path):
        """Build internal API URL."""
        base = self.config.server_url.rstrip("/")
        return f"{base}/api/v1/internal/{path.lstrip('/')}"

    def _get_jwt_token(self):
        """
        Obtain a valid JWT token via UpdateManager.
        Returns the token string, or None if authentication is not possible
        (e.g. license not activated yet).
        """
        try:
            self.update_manager._ensure_authenticated()
            return self.config.jwt_token
        except UpdateAuthenticationError as e:
            logger.warning(f"Marketplace JWT auth failed: {e}")
            return None
        except Exception as e:
            logger.warning(f"Marketplace JWT auth unexpected error: {e}")
            return None

    def _get_headers(self):
        """
        Build request headers using JWT Bearer token for authentication.
        Each installation has its own JWT tied to its license key.
        """
        headers = {"Accept": "application/json"}
        token = self._get_jwt_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _api_get(self, path, params=None, timeout=15):
        """Make an authenticated GET request to the internal API."""
        try:
            response = requests.get(
                self._get_internal_api_url(path),
                headers=self._get_headers(),
                params=params or {},
                timeout=timeout,
            )
            if response.status_code == 401:
                logger.warning(
                    f"Marketplace API auth rejected (GET {path}). Ensure the license is activated."
                )
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Marketplace API error (GET {path}): {e}")
            return None

    def _api_post(self, path, data=None, timeout=15):
        """Make an authenticated POST request to the internal API."""
        try:
            response = requests.post(
                self._get_internal_api_url(path),
                headers=self._get_headers(),
                json=data or {},
                timeout=timeout,
            )
            if response.status_code == 401:
                logger.warning(
                    f"Marketplace API auth rejected (POST {path}). Ensure the license is activated."
                )
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Marketplace API error (POST {path}): {e}")
            return None

    # ------------------------------------------------------------------
    # Browse
    # ------------------------------------------------------------------

    def browse(self, filters=None):
        """
        Fetch marketplace listings from upgrade server.
        Returns dict with 'results', 'count', 'page', 'pages'.
        """
        filters = filters or {}

        # Check if we can authenticate before hitting the API.
        # _get_jwt_token() caches the token in UpdateServerConfig, so the
        # subsequent _api_get() → _get_headers() call won't re-authenticate.
        if not self._get_jwt_token():
            return {
                "results": [],
                "count": 0,
                "page": 1,
                "pages": 0,
                "auth_required": True,
            }

        cache_key = f"{CACHE_PREFIX}:browse:{hash(frozenset(filters.items()))}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = self._api_get("marketplace/browse/", params=filters)
        if data:
            # Mark installed components
            # Normalize slugs: upgrade server may use hyphens, local registry may use underscores
            installed_slugs = set(ComponentRegistry.objects.values_list("slug", flat=True))
            installed_normalized = {s.replace("_", "-") for s in installed_slugs} | installed_slugs
            for item in data.get("results", []):
                item["is_installed"] = item["slug"] in installed_normalized

            cache.set(cache_key, data, BROWSE_CACHE_TTL)
        return data or {"results": [], "count": 0, "page": 1, "pages": 0}

    # ------------------------------------------------------------------
    # Detail
    # ------------------------------------------------------------------

    def get_detail(self, slug):
        """
        Fetch full component details from upgrade server.
        """
        cache_key = f"{CACHE_PREFIX}:detail:{slug}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {}
        if self.config.license_key:
            params["license_key"] = self.config.license_key

        data = self._api_get(f"marketplace/component/{slug}/", params=params)
        if data:
            # Check local install status
            # Normalize: upgrade server uses hyphens, local registry may use underscores
            slug_underscore = slug.replace("-", "_")
            data["is_installed"] = ComponentRegistry.objects.filter(
                slug__in=[slug, slug_underscore]
            ).exists()

            # Get installed version if applicable
            if data["is_installed"]:
                reg = ComponentRegistry.objects.filter(slug__in=[slug, slug_underscore]).first()
                if reg:
                    data["installed_version"] = reg.current_version

            cache.set(cache_key, data, DETAIL_CACHE_TTL)
        return data

    # ------------------------------------------------------------------
    # Reviews
    # ------------------------------------------------------------------

    def get_reviews(self, slug, page=1):
        """Fetch paginated reviews for a component."""
        return self._api_get(f"marketplace/component/{slug}/reviews/", params={"page": page}) or {
            "results": [],
            "count": 0,
            "page": 1,
            "pages": 0,
        }

    def submit_review(self, slug, rating, title="", comment=""):
        """Submit a review from this installation."""
        return self._api_post(
            f"marketplace/component/{slug}/reviews/",
            data={
                "installation_uuid": str(self.config.installation_uuid),
                "rating": rating,
                "title": title,
                "comment": comment,
                "author_name": self._get_store_name(),
            },
        )

    # ------------------------------------------------------------------
    # Install
    # ------------------------------------------------------------------

    def install_free_component(self, slug, version=None):
        """
        Install a free component using UpdateManager.
        Returns dict with success status.
        """
        try:
            # Determine component type from browse data
            detail = self.get_detail(slug)
            if not detail:
                return {"success": False, "error": "Component not found"}

            if detail.get("pricing_model") == "paid":
                is_entitled = detail.get("is_entitled", False)
                if not is_entitled:
                    return {"success": False, "error": "Purchase required"}

            component_type = detail.get("component_type", "theme")
            target_version = version or detail.get("current_version")

            result = self.update_manager.install_component(
                component_type=component_type,
                slug=slug,
                version=target_version,
            )

            # Invalidate caches
            cache.delete(f"{CACHE_PREFIX}:detail:{slug}")
            # Clear browse cache (installed status changed)
            cache.delete_pattern(f"{CACHE_PREFIX}:browse:*") if hasattr(
                cache, "delete_pattern"
            ) else None

            return result

        except Exception as e:
            logger.exception(f"Failed to install component {slug}: {e}")
            return {"success": False, "error": str(e)}

    # ------------------------------------------------------------------
    # Purchase
    # ------------------------------------------------------------------

    def get_purchase_url(self, slug, return_url=""):
        """Get spwig.com purchase URL for a paid component."""
        params = {}
        if return_url:
            params["return_url"] = return_url

        data = self._api_get(
            f"marketplace/component/{slug}/purchase-url/",
            params=params,
        )
        return data

    # ------------------------------------------------------------------
    # Entitlements
    # ------------------------------------------------------------------

    def check_entitlements(self):
        """Get list of paid components this license is entitled to."""
        return self._api_get("marketplace/entitlements/")

    # ------------------------------------------------------------------
    # Component types (for filter tabs)
    # ------------------------------------------------------------------

    def get_component_types(self):
        """Fetch all active component types for the filter tabs."""
        cache_key = f"{CACHE_PREFIX}:types"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = self._api_get("component-types/")
        types = data.get("types", []) if data else []
        cache.set(cache_key, types, TYPES_CACHE_TTL)
        return types

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_store_name(self):
        """Get the merchant's store name for review attribution."""
        try:
            from core.models import SiteSettings

            site_settings = SiteSettings.objects.first()
            if site_settings and site_settings.store_name:
                return site_settings.store_name
        except Exception:
            pass
        return "Anonymous Store"
