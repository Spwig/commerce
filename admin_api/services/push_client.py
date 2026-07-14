"""
Push Notification Client for push.spwig.com

HTTP client that sends push notifications via the Spwig push notification service.
This replaces direct APNs communication with a centralized service.
"""

import logging
import time
from dataclasses import dataclass
from typing import Any

import httpx
import jwt
from django.conf import settings

from core.platform_secrets import get_installation_uuid, get_push_secret

logger = logging.getLogger(__name__)

# Default service URL
PUSH_SERVICE_URL = getattr(settings, "PUSH_SERVICE_URL", "https://push.spwig.com")


@dataclass
class PushResult:
    """Result from a push notification send operation."""

    success: bool
    sent: int
    failed: int
    results: list[dict[str, Any]]
    error: str | None = None


class PushClientError(Exception):
    """Base exception for push client errors."""

    pass


class PushAuthError(PushClientError):
    """Authentication failed with push service."""

    pass


class PushRateLimitError(PushClientError):
    """Rate limit exceeded."""

    pass


class PushClient:
    """
    HTTP client for the Spwig push notification service (push.spwig.com).

    Handles JWT authentication and provides methods for sending push
    notifications to iOS devices via the centralized push service.

    Usage:
        client = PushClient()
        result = client.send_notification(
            tokens=['device_token_1', 'device_token_2'],
            title='New Order',
            body='Order #12345 received'
        )
    """

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        """
        Initialize the push client.

        Args:
            base_url: Override the push service URL (defaults to PUSH_SERVICE_URL setting)
            timeout: Request timeout in seconds
        """
        self.base_url = (base_url or PUSH_SERVICE_URL).rstrip("/")
        self.timeout = timeout
        self._jwt_token: str | None = None
        self._jwt_expires_at: float = 0

    def _get_jwt_secret(self) -> str:
        """Get the JWT secret for authentication."""
        secret = get_push_secret()
        if not secret:
            raise PushAuthError(
                "Push JWT secret not configured. "
                "Ensure the installation is registered with the license server."
            )
        return secret

    def _get_installation_uuid(self) -> str:
        """Get the installation UUID."""
        uuid = get_installation_uuid()
        if not uuid:
            raise PushAuthError(
                "Installation UUID not found. "
                "Ensure the installation is registered with the license server."
            )
        return uuid

    def _generate_jwt(self) -> str:
        """
        Generate a JWT for authentication with the push service.

        The JWT contains claims identifying this installation and is
        signed with the shared secret issued by the license server.
        """
        now = int(time.time())

        # Check if we have a valid cached token
        if self._jwt_token and self._jwt_expires_at > now + 60:
            return self._jwt_token

        secret = self._get_jwt_secret()
        installation_uuid = self._get_installation_uuid()

        # JWT payload matching what push.spwig.com expects
        payload = {
            "installation_uuid": installation_uuid,
            "sub": installation_uuid,  # Subject (merchant identifier)
            "aud": "push.spwig.com",  # Audience
            "iat": now,
            "exp": now + 3600,  # 1 hour expiry
            "iss": "spwig-platform",  # Must match push server's jwt_issuer
            "tier": "standard",
            "rate_limit": 1000,
        }

        self._jwt_token = jwt.encode(payload, secret, algorithm="HS256")
        self._jwt_expires_at = now + 3600

        return self._jwt_token

    def _get_headers(self) -> dict[str, str]:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self._generate_jwt()}",
            "Content-Type": "application/json",
            "User-Agent": "SpwigShop/1.0",
        }

    def _over_limit_cache_key(self) -> str:
        return f"push:over_limit:{self._get_installation_uuid()}"

    def is_over_limit(self) -> bool:
        """
        True while a recent 429 response is still in the Retry-After window.
        Callers can check this before attempting a send to short-circuit
        without an HTTP round trip.
        """
        from django.core.cache import cache as django_cache

        return bool(django_cache.get(self._over_limit_cache_key()))

    def _mark_over_limit(self, response) -> None:
        from django.core.cache import cache as django_cache

        retry_after = int(response.headers.get("Retry-After", 60))
        django_cache.set(self._over_limit_cache_key(), True, timeout=retry_after)
        logger.debug("Push service over tier limit; cached for %ds", retry_after)

    def _handle_response(self, response: httpx.Response, operation: str) -> dict[str, Any]:
        """
        Handle API response, raising appropriate exceptions on error.

        Args:
            response: The HTTP response
            operation: Description of the operation (for error messages)

        Returns:
            Parsed JSON response data

        Raises:
            PushAuthError: If authentication fails (401)
            PushRateLimitError: If rate limited (429)
            PushClientError: For other errors
        """
        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:
            # Clear cached token so next request generates a new one
            self._jwt_token = None
            self._jwt_expires_at = 0
            raise PushAuthError(f"Authentication failed during {operation}: {response.text}")

        if response.status_code == 429:
            # Cache the "over limit" state locally so subsequent calls
            # short-circuit until the Retry-After window elapses. Prevents
            # merchants near the Community daily cap from hammering the
            # server for every notification attempt.
            self._mark_over_limit(response)
            raise PushRateLimitError(f"Rate limit exceeded during {operation}")

        # Generic error
        raise PushClientError(
            f"Push service error during {operation}: HTTP {response.status_code} - {response.text}"
        )

    def send_notification(
        self,
        tokens: list[str],
        title: str,
        body: str,
        data: dict[str, Any] | None = None,
        sound: str = "default",
        badge: int | None = None,
        sandbox: bool = False,
    ) -> PushResult:
        """
        Send a push notification to one or more devices.

        Args:
            tokens: List of device push tokens (max 100)
            title: Notification title
            body: Notification body text
            data: Optional custom data payload
            sound: Sound name (default: 'default')
            badge: Badge number to display (optional)
            sandbox: Use APNs sandbox for development builds

        Returns:
            PushResult with sent/failed counts and per-token results
        """
        if not tokens:
            return PushResult(success=True, sent=0, failed=0, results=[])

        if len(tokens) > 100:
            logger.warning(f"Token list exceeds 100, truncating from {len(tokens)}")
            tokens = tokens[:100]

        payload = {
            "tokens": tokens,
            "platform": "ios",
            "notification": {
                "title": title,
                "body": body,
                "sound": sound,
            },
            "sandbox": sandbox,
        }

        if badge is not None:
            payload["notification"]["badge"] = badge

        if data:
            payload["data"] = data

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/api/v1/send/",
                    headers=self._get_headers(),
                    json=payload,
                )

            result_data = self._handle_response(response, "send_notification")

            return PushResult(
                success=result_data.get("success", False),
                sent=result_data.get("sent", 0),
                failed=result_data.get("failed", 0),
                results=result_data.get("results", []),
            )

        except httpx.TimeoutException:
            logger.error("Push service request timed out")
            return PushResult(
                success=False,
                sent=0,
                failed=len(tokens),
                results=[],
                error="Request timed out",
            )
        except httpx.RequestError as e:
            logger.error(f"Push service request failed: {e}")
            return PushResult(
                success=False,
                sent=0,
                failed=len(tokens),
                results=[],
                error=str(e),
            )
        except (PushAuthError, PushRateLimitError):
            raise
        except Exception as e:
            logger.exception(f"Unexpected error sending push notification: {e}")
            return PushResult(
                success=False,
                sent=0,
                failed=len(tokens),
                results=[],
                error=str(e),
            )

    def send_bulk(
        self,
        notifications: list[dict[str, Any]],
        sandbox: bool = False,
    ) -> PushResult:
        """
        Send multiple different notifications in one request.

        Args:
            notifications: List of notification dicts, each with:
                - token: Device push token
                - title: Notification title
                - body: Notification body
                - data: Optional custom data
            sandbox: Use APNs sandbox for development builds

        Returns:
            PushResult with aggregated results
        """
        if not notifications:
            return PushResult(success=True, sent=0, failed=0, results=[])

        if len(notifications) > 100:
            logger.warning(f"Notification list exceeds 100, truncating from {len(notifications)}")
            notifications = notifications[:100]

        # Format for push service API
        bulk_payload = {
            "notifications": [
                {
                    "token": n["token"],
                    "platform": "ios",
                    "notification": {
                        "title": n.get("title", ""),
                        "body": n.get("body", ""),
                        "sound": n.get("sound", "default"),
                        "badge": n.get("badge"),
                    },
                    "data": n.get("data"),
                }
                for n in notifications
            ],
            "sandbox": sandbox,
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/api/v1/send/bulk/",
                    headers=self._get_headers(),
                    json=bulk_payload,
                )

            result_data = self._handle_response(response, "send_bulk")

            return PushResult(
                success=result_data.get("success", False),
                sent=result_data.get("sent", 0),
                failed=result_data.get("failed", 0),
                results=result_data.get("results", []),
            )

        except httpx.TimeoutException:
            logger.error("Push service bulk request timed out")
            return PushResult(
                success=False,
                sent=0,
                failed=len(notifications),
                results=[],
                error="Request timed out",
            )
        except httpx.RequestError as e:
            logger.error(f"Push service bulk request failed: {e}")
            return PushResult(
                success=False,
                sent=0,
                failed=len(notifications),
                results=[],
                error=str(e),
            )
        except (PushAuthError, PushRateLimitError):
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in bulk send: {e}")
            return PushResult(
                success=False,
                sent=0,
                failed=len(notifications),
                results=[],
                error=str(e),
            )

    def is_configured(self) -> bool:
        """
        Check if the push client is properly configured and available.

        Returns:
            True if push secret and installation UUID are available
            and maintenance is active (or in grace period)
        """
        try:
            from core.license import get_license_manager

            if not get_license_manager().are_spwig_services_available():
                return False
        except Exception:
            pass  # Fail open - don't break push on import errors

        try:
            secret = get_push_secret()
            uuid = get_installation_uuid()
            return bool(secret and uuid)
        except Exception:
            return False

    def health_check(self) -> dict[str, Any]:
        """
        Check connectivity to the push service.

        Returns:
            Health check response from push service
        """
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.base_url}/health")

            if response.status_code == 200:
                return {"healthy": True, "service_url": self.base_url, **response.json()}
            else:
                return {
                    "healthy": False,
                    "service_url": self.base_url,
                    "error": f"HTTP {response.status_code}",
                }
        except Exception as e:
            return {"healthy": False, "service_url": self.base_url, "error": str(e)}
