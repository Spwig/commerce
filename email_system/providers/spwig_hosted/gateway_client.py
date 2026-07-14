"""
Spwig Mail Gateway Management API client.

Provides a Python interface to the Gateway Management API running on the
dedicated mail server. Used by:

- The provisioning orchestrator (spwig.com) to create/delete merchant
  SMTP credentials during instance lifecycle
- The shop admin UI for custom domain management (future)

The gateway API runs on a dedicated Linode behind nginx with TLS.
All endpoints (except /health) require a Bearer API key.
"""

import logging

import httpx

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 15


class GatewayAPIError(Exception):
    """Raised when a Gateway API call fails."""

    def __init__(self, message: str, status_code: int | None = None, detail: str = ""):
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class SpwigMailGatewayClient:
    """Client for the Spwig Mail Gateway Management API.

    Usage::

        client = SpwigMailGatewayClient(
            base_url="https://mail.myspwig.com",
            api_key="your-api-key",
        )

        # Create merchant SMTP credentials
        result = client.create_merchant("acme-store", plan="starter")
        # result contains auth_user, auth_token, gateway_host, gateway_port

        # Register a custom domain
        domain_info = client.register_domain("acme-store.com", "acme-store")
        # domain_info contains dns_records the merchant needs to add
    """

    def __init__(self, base_url: str, api_key: str, timeout: int = DEFAULT_TIMEOUT):
        self._base_url = base_url.rstrip("/")
        self._headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        }
        self._timeout = timeout

    # ── Merchants ─────────────────────────────────────────────────────

    def create_merchant(
        self,
        slug: str,
        plan: str = "starter",
        rate_limits: dict | None = None,
    ) -> dict:
        """Create SASL credentials for a new merchant.

        Args:
            slug: Unique merchant identifier (e.g. "acme-store")
            plan: Subscription plan ("starter", "business", "enterprise")
            rate_limits: Optional custom rate limits {hourly, daily, monthly}

        Returns:
            Dict with auth_user, auth_token (plaintext, one-time),
            gateway_host, gateway_port, plan, rate_limits

        Raises:
            GatewayAPIError: On API failure or duplicate merchant (409)
        """
        payload = {"merchant_slug": slug, "plan": plan}
        if rate_limits:
            payload["rate_limits"] = rate_limits
        return self._post("/api/merchants/", payload)

    def delete_merchant(self, slug: str) -> bool:
        """Remove a merchant's SMTP credentials.

        Returns:
            True if merchant was found and deleted

        Raises:
            GatewayAPIError: On API failure (404 returns False)
        """
        try:
            self._delete(f"/api/merchants/{slug}")
            return True
        except GatewayAPIError as e:
            if e.status_code == 404:
                return False
            raise

    def get_merchant(self, slug: str) -> dict | None:
        """Get merchant info including plan and rate limits.

        Returns:
            Merchant info dict, or None if not found
        """
        try:
            return self._get(f"/api/merchants/{slug}")
        except GatewayAPIError as e:
            if e.status_code == 404:
                return None
            raise

    def list_merchants(self) -> list[dict]:
        """List all registered merchants."""
        result = self._get("/api/merchants/")
        return result.get("merchants", [])

    def update_rate_limits(
        self,
        slug: str,
        hourly: int | None = None,
        daily: int | None = None,
        monthly: int | None = None,
    ) -> dict | None:
        """Update rate limits for a merchant.

        Only provided values are updated. Returns updated rate limits
        dict, or None if merchant not found.
        """
        payload = {}
        if hourly is not None:
            payload["hourly"] = hourly
        if daily is not None:
            payload["daily"] = daily
        if monthly is not None:
            payload["monthly"] = monthly

        try:
            return self._request("PATCH", f"/api/merchants/{slug}/rate-limits", json=payload)
        except GatewayAPIError as e:
            if e.status_code == 404:
                return None
            raise

    # ── Domains ───────────────────────────────────────────────────────

    def register_domain(self, domain: str, merchant_slug: str) -> dict:
        """Register a custom domain and generate DKIM keys.

        Args:
            domain: The custom domain (e.g. "acme-store.com")
            merchant_slug: Owning merchant

        Returns:
            Dict with domain, status, dns_records (SPF, DKIM, DMARC)

        Raises:
            GatewayAPIError: On API failure or duplicate domain (409)
        """
        return self._post(
            "/api/domains/",
            {
                "domain": domain,
                "merchant_slug": merchant_slug,
            },
        )

    def verify_domain(self, domain: str) -> dict:
        """Verify DNS records for a custom domain.

        If all records pass, activates DKIM signing.

        Returns:
            Dict with domain, status, spf_valid, dkim_valid, dmarc_valid
        """
        return self._post(f"/api/domains/{domain}/verify", {})

    def get_domain_status(self, domain: str) -> dict | None:
        """Get current status of a registered domain.

        Returns:
            Domain info dict, or None if not found
        """
        try:
            return self._get(f"/api/domains/{domain}")
        except GatewayAPIError as e:
            if e.status_code == 404:
                return None
            raise

    def remove_domain(self, domain: str) -> bool:
        """Remove a custom domain (DKIM keys, signing tables).

        Returns:
            True if domain was found and deleted
        """
        try:
            self._delete(f"/api/domains/{domain}")
            return True
        except GatewayAPIError as e:
            if e.status_code == 404:
                return False
            raise

    def list_domains(self) -> list[dict]:
        """List all registered custom domains."""
        result = self._get("/api/domains/")
        return result.get("domains", [])

    # ── Stats ─────────────────────────────────────────────────────────

    def get_merchant_stats(
        self,
        slug: str,
        period: str = "last_24h",
    ) -> dict:
        """Get sending statistics for a merchant."""
        return self._get(f"/api/stats/{slug}", params={"period": period})

    def get_merchant_bounces(self, slug: str) -> dict:
        """Get detailed bounce data for a merchant."""
        return self._get(f"/api/stats/{slug}/bounces")

    def get_system_stats(self, period: str = "last_24h") -> dict:
        """Get system-wide aggregate statistics."""
        return self._get("/api/stats/", params={"period": period})

    # ── Health & Blacklist ────────────────────────────────────────────

    def health_check(self) -> dict:
        """Check gateway health (no auth required)."""
        return self._request("GET", "/health", auth=False)

    def get_blacklist_status(self) -> dict:
        """Check gateway IP against DNS blacklists."""
        return self._get("/api/blacklist-status")

    # ── Internal HTTP helpers ─────────────────────────────────────────

    def _get(self, path: str, params: dict | None = None) -> dict:
        return self._request("GET", path, params=params)

    def _post(self, path: str, payload: dict) -> dict:
        return self._request("POST", path, json=payload)

    def _delete(self, path: str) -> dict:
        return self._request("DELETE", path)

    def _request(
        self,
        method: str,
        path: str,
        json: dict | None = None,
        params: dict | None = None,
        auth: bool = True,
    ) -> dict:
        """Make an HTTP request to the gateway API."""
        url = f"{self._base_url}{path}"
        headers = self._headers if auth else {"Content-Type": "application/json"}

        try:
            resp = httpx.request(
                method,
                url,
                headers=headers,
                json=json,
                params=params,
                timeout=self._timeout,
            )
        except httpx.TimeoutException:
            raise GatewayAPIError(
                f"Gateway API timeout ({method} {path})",
                detail="Request timed out",
            )
        except httpx.HTTPError as e:
            raise GatewayAPIError(
                f"Gateway API connection error: {e}",
                detail=str(e),
            )

        if resp.status_code >= 400:
            try:
                data = resp.json()
                detail = data.get("detail", str(data))
            except Exception:
                detail = resp.text
            raise GatewayAPIError(
                f"Gateway API error ({resp.status_code}): {detail}",
                status_code=resp.status_code,
                detail=detail,
            )

        return resp.json()
