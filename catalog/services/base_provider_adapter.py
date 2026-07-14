"""
Base adapter class for external license providers.

This module defines the interface that all provider adapters must implement.
"""

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseLicenseProviderAdapter(ABC):
    """
    Abstract base class for external license provider adapters.

    All provider-specific adapters (Keygen, License Spring, etc.) must inherit
    from this class and implement all abstract methods.
    """

    def __init__(self, provider):
        """
        Initialize adapter with provider configuration.

        Args:
            provider: LicenseProvider model instance
        """
        self.provider = provider
        self.api_endpoint = provider.api_endpoint
        self.api_key = provider.api_key
        self.api_secret = provider.api_secret
        self.config = provider.provider_config

    @abstractmethod
    def create_license(self, license_key, product, order) -> tuple[bool, str, dict]:
        """
        Create a license in the external provider system.

        Args:
            license_key: LicenseKey model instance
            product: Product model instance
            order: Order model instance

        Returns:
            Tuple of (success: bool, external_id: str, response_data: dict)
        """
        pass

    @abstractmethod
    def validate_license(self, key: str) -> tuple[bool, dict]:
        """
        Validate a license key with the external provider.

        Args:
            key: License key string to validate

        Returns:
            Tuple of (is_valid: bool, validation_data: dict)
        """
        pass

    @abstractmethod
    def activate_device(
        self, license_key, device_fingerprint: str, device_info: dict
    ) -> tuple[bool, str, dict]:
        """
        Register a device activation with the external provider.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier
            device_info: Dictionary of device information

        Returns:
            Tuple of (success: bool, activation_id: str, response_data: dict)
        """
        pass

    @abstractmethod
    def deactivate_device(self, license_key, device_fingerprint: str) -> tuple[bool, dict]:
        """
        Deactivate a device with the external provider.

        Args:
            license_key: LicenseKey model instance
            device_fingerprint: Unique device identifier

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        pass

    @abstractmethod
    def suspend_license(self, license_key) -> tuple[bool, dict]:
        """
        Suspend a license in the external provider.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        pass

    @abstractmethod
    def revoke_license(self, license_key) -> tuple[bool, dict]:
        """
        Revoke a license in the external provider.

        Args:
            license_key: LicenseKey model instance

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        pass

    @abstractmethod
    def get_license_info(self, external_id: str) -> tuple[bool, dict]:
        """
        Retrieve license information from external provider.

        Args:
            external_id: External license ID

        Returns:
            Tuple of (success: bool, license_data: dict)
        """
        pass

    def handle_webhook(self, event_type: str, payload: dict) -> tuple[bool, str | None]:
        """
        Process webhook event from external provider.

        This method can be overridden by subclasses for provider-specific webhook handling.

        Args:
            event_type: Type of webhook event
            payload: Webhook payload data

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        logger.info(f"Received webhook event: {event_type} from {self.provider.name}")
        # Default implementation - subclasses should override
        return True, None

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> tuple[bool, dict]:
        """
        Helper method for making HTTP requests to provider API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request payload (for POST/PUT)
            headers: Additional HTTP headers

        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        import requests

        url = f"{self.api_endpoint.rstrip('/')}/{endpoint.lstrip('/')}"

        # Build headers with authentication
        request_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if headers:
            request_headers.update(headers)

        try:
            response = requests.request(
                method=method, url=url, json=data, headers=request_headers, timeout=30
            )

            response.raise_for_status()

            return True, response.json() if response.content else {}

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return False, {"error": str(e)}
