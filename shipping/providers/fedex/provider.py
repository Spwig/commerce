"""
FedEx Shipping Provider

OAuth 2.0 authenticated shipping provider for FedEx Web Services API.
Implements rate calculation, label generation, and tracking.

Version: 1.0.0
"""

import logging
from datetime import datetime
from decimal import Decimal
from typing import Any

import requests
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.utils import get_default_currency, get_shipping_origin_country
from shipping.providers.base import ProviderBase
from shipping.providers.fedex import utils
from shipping.providers.fedex.auth import FedExOAuthClient, create_oauth_client
from shipping.providers.fedex.exceptions import (
    FedExAccountError,
    FedExAPIError,
    FedExAuthenticationError,
    FedExAuthorizationError,
    FedExError,
    FedExRateLimitError,
    FedExServiceUnavailableError,
    FedExTrackingError,
    FedExValidationError,
    get_exception_for_error_code,
)
from shipping.providers.fedex.retry import retry_with_backoff

logger = logging.getLogger(__name__)


class FedExProvider(ProviderBase):
    """
    FedEx shipping provider implementation.

    Provides rate calculation, label generation, and tracking
    via FedEx Web Services REST API with OAuth 2.0 authentication.

    Capabilities:
        - Rate quotes (Ground, Express, International)
        - Shipping label generation (PDF, PNG, ZPL)
        - Real-time tracking
        - International shipping
        - Insurance support
        - Signature confirmation

    API Documentation: https://developer.fedex.com
    """

    # Provider identification
    provider_key = "fedex"
    provider_name = _("FedEx")

    # API URLs
    SANDBOX_BASE_URL = "https://apis-sandbox.fedex.com"
    PRODUCTION_BASE_URL = "https://apis.fedex.com"

    def __init__(self, credentials: dict[str, Any], config: dict[str, Any] | None = None):
        """
        Initialize FedEx provider.

        Args:
            credentials: Dictionary containing:
                - api_key: FedEx API Key
                - api_secret: FedEx API Secret
                - account_number: 9-digit FedEx account number
                - environment: 'sandbox' or 'production'
            config: Optional configuration dictionary

        Raises:
            ValueError: If credentials are invalid
        """
        # Initialize parent class (validates credentials)
        super().__init__(credentials, config)

        # Set API base URL based on environment
        environment = credentials.get("environment", "sandbox")
        self.base_url = (
            self.PRODUCTION_BASE_URL if environment == "production" else self.SANDBOX_BASE_URL
        )

        # Store account number
        self.account_number = credentials.get("account_number")
        self.environment = environment

        # Create OAuth client
        self.oauth_client: FedExOAuthClient = create_oauth_client(credentials)

        logger.info(f"FedEx provider initialized (environment={environment})")

    @property
    def capabilities(self) -> dict[str, bool]:
        """
        Return FedEx provider capabilities.

        Returns:
            Dictionary of supported features
        """
        return {
            "rates": True,  # Rate calculation
            "labels": True,  # Label generation
            "tracking": True,  # Shipment tracking
            "international": True,  # International shipping
            "returns": False,  # Return labels (not in v1.0)
            "pickup": False,  # Pickup scheduling (not in v1.0)
            "insurance": True,  # Shipment insurance
            "signature": True,  # Signature confirmation
        }

    @property
    def credential_schema(self) -> dict[str, Any]:
        """
        Return JSON schema for FedEx credentials.

        Returns:
            JSON schema dictionary
        """
        return {
            "type": "object",
            "properties": {
                "api_key": {
                    "type": "string",
                    "title": _("API Key"),
                    "description": _(
                        "Your FedEx API Key (Client ID) from the FedEx Developer Portal"
                    ),
                    "required": True,
                    "secret": True,
                    "min_length": 20,
                },
                "api_secret": {
                    "type": "string",
                    "title": _("API Secret"),
                    "description": _(
                        "Your FedEx API Secret (Client Secret) from the FedEx Developer Portal"
                    ),
                    "required": True,
                    "secret": True,
                    "min_length": 20,
                },
                "account_number": {
                    "type": "string",
                    "title": _("Account Number"),
                    "description": _("Your 9-digit FedEx account number"),
                    "required": True,
                    "pattern": r"^\d{9}$",
                },
                "environment": {
                    "type": "string",
                    "title": _("Environment"),
                    "enum": ["sandbox", "production"],
                    "default": "sandbox",
                    "description": _(
                        "API environment to use. Use sandbox for testing, production for live shipping."
                    ),
                },
            },
        }

    def validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate FedEx credentials.

        Args:
            credentials: Dictionary of credential values

        Raises:
            ValueError: If credentials are invalid or missing
        """
        required_fields = ["api_key", "api_secret", "account_number"]
        missing_fields = [f for f in required_fields if not credentials.get(f)]

        if missing_fields:
            raise ValueError(
                _("Missing required FedEx credentials: %(fields)s")
                % {"fields": ", ".join(missing_fields)}
            )

        # Validate API key length
        api_key = credentials.get("api_key", "")
        if len(api_key) < 20:
            raise ValueError(_("FedEx API Key must be at least 20 characters"))

        # Validate API secret length
        api_secret = credentials.get("api_secret", "")
        if len(api_secret) < 20:
            raise ValueError(_("FedEx API Secret must be at least 20 characters"))

        # Validate account number format (9 digits)
        account_number = credentials.get("account_number", "")
        if not account_number.isdigit() or len(account_number) != 9:
            raise ValueError(_("FedEx Account Number must be exactly 9 digits"))

        # Validate environment
        environment = credentials.get("environment", "sandbox")
        if environment not in ["sandbox", "production"]:
            raise ValueError(_("Environment must be 'sandbox' or 'production'"))

        logger.debug(f"FedEx credentials validated successfully (account={account_number})")

    def redact_credentials(self, credentials: dict[str, Any]) -> dict[str, Any]:
        """
        Redact sensitive credential values for logging.

        Args:
            credentials: Original credentials dictionary

        Returns:
            Dictionary with masked sensitive values
        """
        redacted = credentials.copy()

        if "api_key" in redacted:
            key = redacted["api_key"]
            redacted["api_key"] = f"***{key[-4:]}" if len(key) > 4 else "***"

        if "api_secret" in redacted:
            redacted["api_secret"] = "***HIDDEN***"

        # Account number is semi-sensitive - show last 4 digits
        if "account_number" in redacted:
            acct = redacted["account_number"]
            redacted["account_number"] = f"*****{acct[-4:]}" if len(acct) > 4 else "***"

        return redacted

    def _handle_api_error(self, response: requests.Response, context: str = "API call") -> None:
        """
        Handle FedEx API error responses.

        Parses FedEx error response and raises appropriate exception.

        Args:
            response: HTTP response from FedEx API
            context: Description of what operation failed (for logging)

        Raises:
            FedExAuthenticationError: For authentication failures
            FedExAuthorizationError: For authorization/permission failures
            FedExValidationError: For validation errors
            FedExAccountError: For account-related errors
            FedExRateLimitError: For rate limiting
            FedExServiceUnavailableError: For service unavailability
            FedExAPIError: For other API errors
        """
        status_code = response.status_code

        # Try to parse error response
        try:
            error_data = response.json()
        except Exception:
            # Can't parse JSON, use status code
            if status_code == 401:
                raise FedExAuthenticationError(f"{context} failed: Unauthorized (401)")
            elif status_code == 403:
                raise FedExAuthorizationError(f"{context} failed: Forbidden (403)")
            elif status_code == 429:
                # Extract retry_after from headers if available
                retry_after = response.headers.get("Retry-After")
                retry_after = int(retry_after) if retry_after else None
                raise FedExRateLimitError(
                    f"{context} failed: Rate limit exceeded (429)", retry_after=retry_after
                )
            elif status_code >= 500:
                raise FedExServiceUnavailableError(
                    f"{context} failed: Service unavailable ({status_code})"
                )
            else:
                raise FedExAPIError(
                    f"{context} failed: HTTP {status_code}", error_code=str(status_code)
                )

        # Parse FedEx error format
        errors = error_data.get("errors", [])
        if not errors:
            # No structured errors, use status code
            raise FedExAPIError(f"{context} failed: {error_data}", error_details=error_data)

        # Get first error (usually most relevant)
        error = errors[0]
        error_code = error.get("code", "UNKNOWN")
        error_message = error.get("message", "Unknown error")

        # Log full error details
        logger.error(
            f"FedEx API error in {context}: "
            f"code={error_code}, message={error_message}, "
            f"status={status_code}, errors={errors}"
        )

        # Get appropriate exception class for error code
        exception_class = get_exception_for_error_code(error_code)

        # Raise appropriate exception
        if exception_class == FedExRateLimitError:
            retry_after = response.headers.get("Retry-After")
            retry_after = int(retry_after) if retry_after else None
            raise FedExRateLimitError(error_message, retry_after=retry_after)
        else:
            raise exception_class(
                f"{context} failed: {error_message}",
                error_code=error_code if hasattr(exception_class, "error_code") else None,
                error_details=error if hasattr(exception_class, "error_details") else None,
            )

    def _make_api_request(
        self,
        method: str,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        context: str = "API request",
        timeout: int = 30,
        retry: bool = True,
    ) -> dict[str, Any]:
        """
        Make an authenticated API request to FedEx with error handling and retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path (e.g., '/rate/v1/rates/quotes')
            payload: Request payload (for POST/PUT)
            context: Description for logging
            timeout: Request timeout in seconds
            retry: Whether to retry on transient failures

        Returns:
            Parsed JSON response

        Raises:
            Various FedExError subclasses based on error type
        """
        url = f"{self.base_url}{endpoint}"

        # Get OAuth token
        token = self.oauth_client.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-locale": "en_US",
        }

        # Log request (redact sensitive data)
        logger.info(f"FedEx {method} {endpoint} - {context}")
        if payload and logger.isEnabledFor(logging.DEBUG):
            # Only log payload in debug mode (might contain sensitive data)
            logger.debug(f"Request payload: {payload}")

        # Define request function for retry decorator
        def make_request():
            try:
                response = requests.request(
                    method=method, url=url, json=payload, headers=headers, timeout=timeout
                )

                # Check for errors
                if response.status_code >= 400:
                    self._handle_api_error(response, context)

                # Parse and return successful response
                result = response.json()
                logger.info(f"FedEx {method} {endpoint} - {context} succeeded")
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"Response: {result}")

                return result

            except requests.exceptions.Timeout:
                logger.error(f"{context} timed out after {timeout}s")
                raise FedExServiceUnavailableError(f"{context} timed out")

            except requests.exceptions.ConnectionError as e:
                logger.error(f"{context} connection error: {e}")
                raise FedExServiceUnavailableError(f"{context} connection failed: {e}")

            except requests.exceptions.RequestException as e:
                logger.error(f"{context} request error: {e}")
                raise FedExAPIError(f"{context} failed: {e}")

        # Execute with or without retry
        if retry:
            # Apply retry decorator
            @retry_with_backoff()
            def retry_wrapper():
                return make_request()

            return retry_wrapper()
        else:
            return make_request()

    def test_connection(self) -> dict[str, Any]:
        """
        Test FedEx API connection and credentials.

        Attempts to acquire OAuth token to verify credentials work.

        Returns:
            Dictionary with test results
        """
        logger.info("Testing FedEx API connection")

        try:
            # Attempt to get OAuth token (this validates credentials)
            self.oauth_client.get_token()

            logger.info("FedEx connection test successful")

            return {
                "success": True,
                "message": _("Connection successful"),
                "details": {
                    "provider": "FedEx",
                    "environment": self.environment,
                    "account_number": f"*****{self.account_number[-4:]}",
                    "token_acquired": True,
                },
            }

        except (FedExAuthenticationError, FedExAuthorizationError) as e:
            # Invalid credentials
            logger.error(f"FedEx connection test failed - authentication: {e}")
            return {
                "success": False,
                "message": str(e),
                "details": {"error_type": "authentication"},
            }

        except FedExAccountError as e:
            # Account issue
            logger.error(f"FedEx connection test failed - account: {e}")
            return {"success": False, "message": str(e), "details": {"error_type": "account"}}

        except FedExServiceUnavailableError as e:
            # Service unavailable
            logger.error(f"FedEx connection test failed - service unavailable: {e}")
            return {
                "success": False,
                "message": str(e),
                "details": {"error_type": "service_unavailable"},
            }

        except FedExError as e:
            # Other FedEx errors
            logger.error(f"FedEx connection test failed: {e}")
            return {"success": False, "message": str(e), "details": {"error_type": "fedex_error"}}

        except Exception as e:
            # Unexpected error
            logger.error(f"FedEx connection test failed with unexpected error: {e}", exc_info=True)
            return {
                "success": False,
                "message": _("Unexpected error: %(error)s") % {"error": str(e)},
                "details": {"error_type": "unexpected"},
            }

    def get_rates(
        self,
        origin: dict[str, str],
        destination: dict[str, str],
        parcels: list[dict[str, Any]],
        options: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get FedEx shipping rates.

        Args:
            origin: Origin address
            destination: Destination address
            parcels: List of parcels
            options: Optional shipping options

        Returns:
            List of rate dictionaries sorted by price

        Raises:
            FedExValidationError: If parameters are invalid
            FedExAuthenticationError: If authentication fails
            FedExServiceUnavailableError: If service is unavailable
            FedExAPIError: For other API errors
        """
        logger.info(f"Getting FedEx rates: {origin['country']} -> {destination['country']}")

        # Build request payload
        payload = self._build_rate_request(origin, destination, parcels, options or {})

        # Make API request with centralized error handling and retry
        data = self._make_api_request(
            method="POST",
            endpoint="/rate/v1/rates/quotes",
            payload=payload,
            context="Getting rates",
            retry=True,
        )

        # Parse response
        rates = self._parse_rate_response(data)

        logger.info(f"Retrieved {len(rates)} FedEx rates")
        return rates

    def _build_rate_request(
        self,
        origin: dict[str, str],
        destination: dict[str, str],
        parcels: list[dict[str, Any]],
        options: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build FedEx rate request payload.

        Args:
            origin: Origin address
            destination: Destination address
            parcels: List of parcels
            options: Shipping options

        Returns:
            Rate request payload dictionary
        """
        # Build package line items
        package_line_items = []
        for parcel in parcels:
            package = {
                "weight": {"units": "LB", "value": utils.grams_to_pounds(parcel.get("weight", 0))}
            }

            # Add dimensions if provided
            if all(k in parcel for k in ["length", "width", "height"]):
                package["dimensions"] = {
                    "length": utils.cm_to_inches(parcel["length"]),
                    "width": utils.cm_to_inches(parcel["width"]),
                    "height": utils.cm_to_inches(parcel["height"]),
                    "units": "IN",
                }

            # Add insured value if provided
            if "value" in parcel and parcel["value"] > 0:
                package["declaredValue"] = {
                    "amount": float(parcel["value"]),
                    "currency": parcel.get("currency", get_default_currency()),
                }

            package_line_items.append(package)

        # Build request
        payload = {
            "accountNumber": {"value": self.account_number},
            "requestedShipment": {
                "shipper": {
                    "address": {
                        "postalCode": origin.get("postal_code"),
                        "countryCode": origin.get("country"),
                    }
                },
                "recipient": {
                    "address": {
                        "postalCode": destination.get("postal_code"),
                        "countryCode": destination.get("country"),
                    }
                },
                "pickupType": "USE_SCHEDULED_PICKUP",
                "rateRequestType": ["LIST", "ACCOUNT"],
                "requestedPackageLineItems": package_line_items,
            },
            "rateRequestControlParameters": {"returnTransitTimes": True},
        }

        # Add city/state if provided (optional but helps with accuracy)
        if "city" in origin:
            payload["requestedShipment"]["shipper"]["address"]["city"] = origin["city"]
        if "state" in origin:
            payload["requestedShipment"]["shipper"]["address"]["stateOrProvinceCode"] = origin[
                "state"
            ]

        if "city" in destination:
            payload["requestedShipment"]["recipient"]["address"]["city"] = destination["city"]
        if "state" in destination:
            payload["requestedShipment"]["recipient"]["address"]["stateOrProvinceCode"] = (
                destination["state"]
            )

        # Add ship date (today or specified)
        ship_date = options.get("ship_date", timezone.now())
        payload["requestedShipment"]["shipDateStamp"] = utils.format_fedex_date(ship_date)

        # Add service type filter if specified
        if "service_type" in options:
            payload["requestedShipment"]["serviceType"] = options["service_type"]

        # Add carrier code filter if specified
        if "carrier_codes" in options:
            payload["carrierCodes"] = options["carrier_codes"]

        # Add customs clearance detail for international shipments
        is_international = origin.get("country") != destination.get("country")
        if is_international and "order_items" in options:
            logger.info("International shipment detected - adding customs clearance detail")

            try:
                # Build customs clearance detail
                customs_clearance = self.build_customs_clearance_detail(
                    order_items=options["order_items"],
                    duties_payment=options.get("duties_payment", "RECIPIENT"),
                    commercial_invoice_terms=options.get("commercial_invoice_terms", "DDU"),
                    currency=options.get("currency", get_default_currency()),
                )

                payload["requestedShipment"]["customsClearanceDetail"] = customs_clearance

                logger.info("Customs clearance detail added to rate request")

            except FedExValidationError as e:
                # Re-raise validation errors with helpful context
                raise FedExValidationError(
                    f"Cannot get rates for international shipment: {e}. "
                    f"Please ensure all products have required customs data (HS code, country of origin, customs price)."
                )

        logger.debug(f"Built rate request for {len(package_line_items)} packages")
        return payload

    def _parse_rate_response(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Parse FedEx rate response into standard format.

        Args:
            data: FedEx API response data

        Returns:
            List of rate dictionaries
        """
        rates = []

        # Get rate details from response
        output = data.get("output", {})
        rate_reply_details = output.get("rateReplyDetails", [])

        for detail in rate_reply_details:
            try:
                # Get service info
                service_type = detail.get("serviceType")
                service_name = detail.get("serviceName") or utils.get_service_name(service_type)

                # Get rated shipment details (use first one, usually ACCOUNT or LIST)
                rated_shipment_list = detail.get("ratedShipmentDetails", [])
                if not rated_shipment_list:
                    continue

                rated_shipment = rated_shipment_list[0]

                # Get total charge (can be plain number or Money object)
                total_charge = rated_shipment.get("totalNetCharge") or rated_shipment.get(
                    "totalBaseCharge"
                )
                if total_charge is None:
                    continue

                rate_amount = utils.parse_money(total_charge)

                # Get currency from rated shipment (fallback to USD)
                currency = rated_shipment.get("currency", "USD")

                # Get delivery information
                commit = detail.get("commit", {})
                delivery_days = utils.calculate_delivery_days(commit)

                # Get delivery date
                delivery_date = None
                date_detail = commit.get("dateDetail", {})
                if date_detail:
                    delivery_date_str = date_detail.get("dayFormat")
                    delivery_date = utils.parse_fedex_date(delivery_date_str)

                # Get billable weight
                billable_weight = None
                shipment_weight = rated_shipment.get("totalBillingWeight", {})
                if shipment_weight:
                    weight_value = shipment_weight.get("value")
                    weight_units = shipment_weight.get("units", "LB")
                    if weight_value and weight_units == "LB":
                        billable_weight = utils.pounds_to_grams(float(weight_value))

                # Build rate dictionary
                rate = {
                    "service_code": service_type,
                    "service_name": service_name,
                    "carrier": "FedEx",
                    "rate": rate_amount,
                    "currency": currency,
                    "delivery_days": delivery_days,
                    "delivery_date": delivery_date,
                    "billable_weight": billable_weight,
                    "included_insurance": Decimal("0.00"),  # FedEx includes basic coverage
                }

                rates.append(rate)

            except Exception as e:
                logger.warning(f"Failed to parse rate detail: {e}")
                continue

        # Sort by rate (cheapest first)
        rates.sort(key=lambda r: r["rate"] if r["rate"] else Decimal("9999999"))

        return rates

    def _parse_api_error(self, response: requests.Response) -> str:
        """
        Parse FedEx API error response.

        Args:
            response: Failed HTTP response

        Returns:
            Human-readable error message
        """
        try:
            error_data = response.json()
            errors = error_data.get("errors", [])

            if errors:
                error = errors[0]
                code = error.get("code", "UNKNOWN")
                message = error.get("message", "Unknown error")
                return f"{code}: {message}"

            return f"HTTP {response.status_code}"

        except Exception:
            return f"HTTP {response.status_code}: {response.text[:200]}"

    def buy_label(
        self, shipment_id: str, rate: dict[str, Any], options: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Purchase FedEx shipping label.

        Args:
            shipment_id: Internal shipment ID
            rate: Selected rate from get_rates()
            options: Required shipping options:
                {
                    'origin': {...},  # Origin address (same format as get_rates)
                    'destination': {...},  # Destination address
                    'parcels': [...],  # Parcel list
                    'label_format': 'PDF',  # PDF, PNG, ZPLII (default: PDF)
                    'label_size': '4x6',  # 4x6, PAPER_LETTER (default: 4x6)
                    'shipper_name': 'Company Name',  # Required
                    'shipper_phone': '+1234567890',  # Required
                    'recipient_name': 'John Doe',  # Required
                    'recipient_phone': '+1987654321',  # Optional
                }

        Returns:
            Label information dictionary:
            {
                'tracking_number': '794953535000',
                'label_url': 'data:application/pdf;base64,...',
                'label_format': 'PDF',
                'cost': Decimal('17.30'),
                'currency': 'USD',
                'carrier': 'FedEx',
                'service': 'FedEx Ground',
                'external_shipment_id': 'fedex_794953535000',
                'created_at': datetime(...)
            }

        Raises:
            FedExValidationError: If required options are missing or invalid
            FedExShipmentError: If shipment creation fails
            FedExAuthenticationError: If authentication fails
            FedExServiceUnavailableError: If service is unavailable
            FedExAPIError: For other API errors
        """
        logger.info(f"Purchasing FedEx label for shipment {shipment_id}")

        # Validate required options
        if not options:
            raise FedExValidationError(_("Options are required for label purchase"))

        required_fields = [
            "origin",
            "destination",
            "parcels",
            "shipper_name",
            "shipper_phone",
            "recipient_name",
        ]
        missing = [f for f in required_fields if f not in options]
        if missing:
            raise FedExValidationError(
                _("Missing required options: %(fields)s") % {"fields": ", ".join(missing)}
            )

        # Build ship request payload
        payload = self._build_ship_request(shipment_id, rate, options)

        # Make API request with centralized error handling and retry
        data = self._make_api_request(
            method="POST",
            endpoint="/ship/v1/shipments",
            payload=payload,
            context="Purchasing label",
            timeout=60,
            retry=True,
        )

        # Parse response
        label_info = self._parse_ship_response(data, rate, options)

        logger.info(f"Successfully created FedEx label: {label_info['tracking_number']}")
        return label_info

    def _build_ship_request(
        self, shipment_id: str, rate: dict[str, Any], options: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Build FedEx ship request payload.

        Args:
            shipment_id: Internal shipment ID
            rate: Selected rate
            options: Shipping options with origin, destination, parcels, etc.

        Returns:
            Ship request payload dictionary
        """
        origin = options["origin"]
        destination = options["destination"]
        parcels = options["parcels"]

        # Get label preferences
        label_format = options.get("label_format", "PDF").upper()
        label_size = options.get("label_size", "4x6")

        # Map label size to FedEx stock type
        # STOCK_* types are for thermal printers (ZPL, EPL)
        # PAPER_* types are for PDF/PNG
        if label_format in ["PDF", "PNG"]:
            stock_type_map = {
                "4x6": "PAPER_4X6",
                "4x8": "PAPER_4X8",
                "letter": "PAPER_LETTER",
                "PAPER_LETTER": "PAPER_LETTER",
            }
        else:  # ZPLII, EPL2
            stock_type_map = {
                "4x6": "STOCK_4X6",
                "4x8": "STOCK_4X8",
                "letter": "PAPER_LETTER",
            }
        stock_type = stock_type_map.get(
            label_size.lower(), "PAPER_4X6" if label_format in ["PDF", "PNG"] else "STOCK_4X6"
        )

        # Build package line items
        package_line_items = []
        for parcel in parcels:
            package = {
                "weight": {"units": "LB", "value": utils.grams_to_pounds(parcel.get("weight", 0))}
            }

            # Add dimensions if provided
            if all(k in parcel for k in ["length", "width", "height"]):
                package["dimensions"] = {
                    "length": utils.cm_to_inches(parcel["length"]),
                    "width": utils.cm_to_inches(parcel["width"]),
                    "height": utils.cm_to_inches(parcel["height"]),
                    "units": "IN",
                }

            # Add insured value if provided
            if "value" in parcel and parcel["value"] > 0:
                package["insuredValue"] = {
                    "amount": float(parcel["value"]),
                    "currency": parcel.get("currency", get_default_currency()),
                }

            package_line_items.append(package)

        # Build request payload
        payload = {
            "labelResponseOptions": "LABEL",
            "requestedShipment": {
                "shipper": {
                    "contact": {
                        "personName": options["shipper_name"],
                        "phoneNumber": options["shipper_phone"],
                        "companyName": options.get("shipper_company", options["shipper_name"]),
                    },
                    "address": {
                        "streetLines": [origin.get("address1", "")],
                        "city": origin.get("city", ""),
                        "stateOrProvinceCode": origin.get("state", ""),
                        "postalCode": origin.get("postal_code", ""),
                        "countryCode": origin.get("country", get_shipping_origin_country()),
                    },
                },
                "recipients": [
                    {
                        "contact": {
                            "personName": options["recipient_name"],
                            "phoneNumber": options.get("recipient_phone", ""),
                            "companyName": options.get("recipient_company", ""),
                        },
                        "address": {
                            "streetLines": [destination.get("address1", "")],
                            "city": destination.get("city", ""),
                            "stateOrProvinceCode": destination.get("state", ""),
                            "postalCode": destination.get("postal_code", ""),
                            "countryCode": destination.get("country", "US"),
                            "residential": options.get("residential", False),
                        },
                    }
                ],
                "shipDatestamp": utils.format_fedex_date(timezone.now()),
                "serviceType": rate.get("service_code", "FEDEX_GROUND"),
                "packagingType": "YOUR_PACKAGING",
                "pickupType": "USE_SCHEDULED_PICKUP",
                "blockInsightVisibility": False,
                "shippingChargesPayment": {
                    "paymentType": "SENDER",
                    "payor": {
                        "responsibleParty": {"accountNumber": {"value": self.account_number}}
                    },
                },
                "labelSpecification": {
                    "imageType": label_format,
                    "labelStockType": stock_type,
                    "labelFormatType": "COMMON2D",
                },
                "requestedPackageLineItems": package_line_items,
            },
            "accountNumber": {"value": self.account_number},
        }

        # Add address line 2 if provided
        if origin.get("address2"):
            payload["requestedShipment"]["shipper"]["address"]["streetLines"].append(
                origin["address2"]
            )

        if destination.get("address2"):
            payload["requestedShipment"]["recipients"][0]["address"]["streetLines"].append(
                destination["address2"]
            )

        # Add customs clearance detail and ETD for international shipments
        is_international = origin.get("country") != destination.get("country")
        if is_international:
            logger.info("International shipment detected - adding customs clearance and ETD")

            # Validate destination address for international shipping
            self.validate_international_shipping_address(destination)

            # Check export compliance if order_items provided
            if "order_items" in options:
                compliance = self.check_export_compliance(
                    destination_country=destination.get("country"),
                    order_items=options["order_items"],
                )

                # Block shipment if not compliant
                if not compliance["compliant"]:
                    raise FedExValidationError(
                        f"International shipment blocked due to export compliance violations: "
                        f"{'; '.join(compliance['errors'])}"
                    )

                # Build and add customs clearance detail
                try:
                    customs_clearance = self.build_customs_clearance_detail(
                        order_items=options["order_items"],
                        duties_payment=options.get("duties_payment", "RECIPIENT"),
                        commercial_invoice_terms=options.get("commercial_invoice_terms", "DDU"),
                        currency=options.get("currency", get_default_currency()),
                    )

                    payload["requestedShipment"]["customsClearanceDetail"] = customs_clearance

                    logger.info("Customs clearance detail added to shipment")

                except FedExValidationError as e:
                    raise FedExValidationError(
                        f"Cannot create international shipping label: {e}. "
                        f"Please ensure all products have required customs data."
                    )

                # Add Electronic Trade Documents (ETD) special service
                # This tells FedEx to generate commercial invoice and other docs electronically
                special_services = payload["requestedShipment"].get("shipmentSpecialServices", {})
                special_services_requested = special_services.get("specialServiceTypes", [])

                # Add ETD service
                if "ELECTRONIC_TRADE_DOCUMENTS" not in special_services_requested:
                    special_services_requested.append("ELECTRONIC_TRADE_DOCUMENTS")

                special_services["specialServiceTypes"] = special_services_requested
                payload["requestedShipment"]["shipmentSpecialServices"] = special_services

                logger.info("Electronic Trade Documents (ETD) service added")

                # Log compliance warnings if any
                if compliance["warnings"]:
                    for warning in compliance["warnings"]:
                        logger.warning(f"Export compliance warning: {warning}")

            else:
                # No order_items - can't build customs clearance
                logger.warning(
                    "International shipment without order_items - customs clearance not added. "
                    "This may cause shipment creation to fail. Include 'order_items' in options."
                )

        logger.debug(f"Built ship request for {len(package_line_items)} packages")
        return payload

    def _parse_ship_response(
        self, data: dict[str, Any], rate: dict[str, Any], options: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Parse FedEx ship response into standard format.

        Args:
            data: FedEx API response data
            rate: Selected rate
            options: Shipping options

        Returns:
            Label information dictionary
        """
        output = data.get("output", {})
        transaction_shipments = output.get("transactionShipments", [])

        if not transaction_shipments:
            raise ValueError(_("No shipment data in FedEx response"))

        shipment = transaction_shipments[0]

        # Get tracking number
        tracking_number = shipment.get("masterTrackingNumber")
        if not tracking_number:
            raise ValueError(_("No tracking number in FedEx response"))

        # Get label data from pieceResponses (not completedPackageDetails)
        piece_responses = shipment.get("pieceResponses", [])

        if not piece_responses:
            raise ValueError(_("No piece responses in FedEx shipment"))

        piece = piece_responses[0]
        label_data = piece.get("packageDocuments", [])

        # Find the shipping label (not commercial invoice)
        label_doc = None
        for doc in label_data:
            if doc.get("contentType") == "LABEL" or doc.get("docType") == "LABEL":
                label_doc = doc
                break

        if not label_doc:
            # Fallback: use first document
            label_doc = label_data[0] if label_data else {}

        # Get base64 encoded label
        encoded_label = label_doc.get("encodedLabel", "")
        label_format = options.get("label_format", "PDF").upper()

        # Determine MIME type
        mime_types = {
            "PDF": "application/pdf",
            "PNG": "image/png",
            "ZPLII": "application/zpl",
            "EPL2": "application/epl",
        }
        mime_type = mime_types.get(label_format, "application/pdf")

        # Build label URL (data URI)
        label_url = f"data:{mime_type};base64,{encoded_label}" if encoded_label else ""

        # Get shipment cost (use rate cost if not in response)
        cost = rate.get("rate", Decimal("0.00"))
        currency = rate.get("currency", "USD")

        # Build return dictionary
        return {
            "tracking_number": tracking_number,
            "label_url": label_url,
            "label_format": label_format,
            "cost": cost,
            "currency": currency,
            "carrier": "FedEx",
            "service": rate.get("service_name", rate.get("service_code", "FedEx")),
            "external_shipment_id": f"fedex_{tracking_number}",
            "created_at": timezone.now(),
        }

    def cancel_label(self, tracking_number: str, reason: str | None = None) -> dict[str, Any]:
        """
        Cancel FedEx shipping label.

        TO BE IMPLEMENTED in future version.

        Args:
            tracking_number: Tracking number to cancel
            reason: Optional cancellation reason

        Returns:
            Cancellation result dictionary

        Raises:
            NotImplementedError: Not yet implemented
        """
        raise NotImplementedError(_("Label cancellation not yet implemented"))

    def get_tracking(self, tracking_number: str, force_refresh: bool = False) -> dict[str, Any]:
        """
        Get FedEx tracking information via Track API with intelligent caching.

        Fetches detailed tracking information including scan events, delivery status,
        estimated delivery time, and location history. Results are cached to minimize
        API calls (FedEx charges per tracking request).

        Caching Strategy:
        - Delivered packages: 7 days (status rarely changes)
        - In-transit packages: 1 hour (status changes frequently)
        - Exception/returned: 2 hours (might get updates)
        - Other statuses: 30 minutes

        Args:
            tracking_number: FedEx tracking number to look up
            force_refresh: If True, bypass cache and fetch fresh data

        Returns:
            Dictionary with tracking information:
            {
                'tracking_number': '794932643366',
                'status': 'in_transit',  # Platform status
                'carrier': 'FedEx',
                'service': 'FedEx Ground',
                'estimated_delivery': datetime(2025, 10, 23, 20, 0),
                'actual_delivery': datetime(2025, 10, 22, 14, 30) or None,
                'current_location': 'Memphis, TN',
                'events': [
                    {
                        'timestamp': datetime(2025, 10, 20, 10, 30),
                        'status': 'in_transit',
                        'location': 'Los Angeles, CA',
                        'description': 'Picked up',
                        'raw_code': 'PU'
                    },
                    ...
                ],
                '_cached': True,  # Added if data is from cache
                '_cached_at': datetime(...)  # Cache timestamp
            }

        Raises:
            ValueError: If tracking number is invalid or not found (backward compatibility)
            FedExAuthenticationError: If authentication fails
            FedExServiceUnavailableError: If service is unavailable
            FedExAPIError: For other API errors
        """
        from django.core.cache import cache

        # Check cache first (unless force_refresh)
        cache_key = f"fedex_tracking_{tracking_number}"
        if not force_refresh:
            cached_data = cache.get(cache_key)
            if cached_data:
                cached_data["_cached"] = True
                cached_data["_cached_at"] = cached_data.get("_cache_timestamp", timezone.now())
                logger.debug(
                    f"Returning cached tracking data for {tracking_number} "
                    f"(cached at {cached_data.get('_cache_timestamp')})"
                )
                return cached_data

        # Build Track API request
        payload = {
            "includeDetailedScans": True,
            "trackingInfo": [{"trackingNumberInfo": {"trackingNumber": tracking_number}}],
        }

        # Make API request with centralized error handling
        try:
            data = self._make_api_request(
                method="POST",
                endpoint="/track/v1/trackingnumbers",
                payload=payload,
                context=f"Getting tracking for {tracking_number}",
                retry=True,
            )
        except FedExValidationError as e:
            # Convert validation errors to ValueError for backward compatibility
            raise ValueError(str(e))
        except FedExTrackingError as e:
            # Convert tracking errors to ValueError for backward compatibility
            raise ValueError(str(e))

        # Parse tracking results
        try:
            complete_results = data["output"]["completeTrackResults"][0]
            track_results = complete_results["trackResults"][0]
        except (KeyError, IndexError) as e:
            raise ValueError(
                _("Unexpected FedEx Track API response format: %(error)s") % {"error": str(e)}
            )

        # Extract latest status
        latest_status = track_results.get("latestStatusDetail", {})
        status_code = latest_status.get("code", "")
        status_description = latest_status.get("description", "")

        # Map FedEx status codes to platform statuses
        status_map = {
            "OC": "created",  # Order Created
            "PU": "in_transit",  # Picked Up
            "IT": "in_transit",  # In Transit
            "AR": "in_transit",  # Arrived at FedEx location
            "DP": "in_transit",  # Departed FedEx location
            "OD": "out_for_delivery",  # Out for Delivery
            "DL": "delivered",  # Delivered
            "DE": "exception",  # Delivery Exception
            "RS": "returned",  # Return to Sender
            "CA": "canceled",  # Canceled
        }

        platform_status = status_map.get(status_code, "in_transit")

        # Extract service information
        service_detail = track_results.get("serviceDetail", {})
        service_name = service_detail.get("description", "FedEx")

        # Extract delivery information
        estimated_delivery = None
        actual_delivery = None

        # Estimated delivery from window
        delivery_window = track_results.get("estimatedDeliveryTimeWindow", {}).get("window", {})
        if delivery_window.get("ends"):
            estimated_delivery = self._parse_fedex_datetime(delivery_window["ends"])

        # Actual delivery timestamp
        delivery_details = track_results.get("deliveryDetails", {})
        if delivery_details.get("actualDeliveryTimestamp"):
            actual_delivery = self._parse_fedex_datetime(
                delivery_details["actualDeliveryTimestamp"]
            )

        # Extract current location
        current_location = None
        if latest_status.get("scanLocation"):
            loc = latest_status["scanLocation"]
            city = loc.get("city", "")
            state = loc.get("stateOrProvinceCode", "")
            current_location = f"{city}, {state}" if city and state else city or state

        # Parse scan events
        events = []
        for scan in track_results.get("scanEvents", []):
            event_code = scan.get("eventType", "")
            event_status = status_map.get(event_code, "in_transit")

            # Extract location
            scan_location = scan.get("scanLocation", {})
            city = scan_location.get("city", "")
            state = scan_location.get("stateOrProvinceCode", "")
            location_str = f"{city}, {state}" if city and state else city or state or ""

            # Parse timestamp
            timestamp = self._parse_fedex_datetime(scan.get("date", ""))

            events.append(
                {
                    "timestamp": timestamp,
                    "status": event_status,
                    "location": location_str,
                    "description": scan.get("eventDescription", ""),
                    "raw_code": event_code,
                }
            )

        # Sort events chronologically (oldest first)
        events.sort(key=lambda x: x["timestamp"] if x["timestamp"] else timezone.now())

        # Build result dictionary
        result = {
            "tracking_number": tracking_number,
            "status": platform_status,
            "status_description": status_description,
            "carrier": "FedEx",
            "service": service_name,
            "estimated_delivery": estimated_delivery,
            "actual_delivery": actual_delivery,
            "current_location": current_location,
            "events": events,
            "_cache_timestamp": timezone.now(),  # For cache metadata
        }

        # Cache the result with TTL based on status
        # This minimizes FedEx API charges by avoiding redundant tracking requests
        cache_ttl = self._get_tracking_cache_ttl(platform_status)
        cache.set(cache_key, result, cache_ttl)

        logger.info(
            f"Fetched tracking data for {tracking_number} from FedEx API "
            f"(status={platform_status}, cached for {cache_ttl}s)"
        )

        return result

    def _get_tracking_cache_ttl(self, status: str) -> int:
        """
        Get cache TTL (time-to-live) in seconds based on shipment status.

        Different statuses have different update frequencies:
        - Delivered packages rarely change (cache longer)
        - In-transit packages change frequently (cache shorter)
        - Exceptions might get updates (moderate cache)

        Args:
            status: Platform status (created, in_transit, delivered, etc.)

        Returns:
            Cache TTL in seconds
        """
        ttl_map = {
            "delivered": 7 * 24 * 60 * 60,  # 7 days (604800s)
            "returned": 3 * 24 * 60 * 60,  # 3 days (259200s)
            "canceled": 3 * 24 * 60 * 60,  # 3 days
            "exception": 2 * 60 * 60,  # 2 hours (7200s)
            "in_transit": 1 * 60 * 60,  # 1 hour (3600s)
            "out_for_delivery": 30 * 60,  # 30 minutes (1800s)
            "created": 30 * 60,  # 30 minutes
        }

        return ttl_map.get(status, 30 * 60)  # Default: 30 minutes

    def _parse_fedex_datetime(self, datetime_str: str) -> datetime | None:
        """
        Parse FedEx datetime string to Python datetime.

        FedEx uses ISO 8601 format: 2025-10-20T10:30:00-05:00

        Args:
            datetime_str: ISO 8601 datetime string

        Returns:
            Parsed datetime object or None if parsing fails
        """
        if not datetime_str:
            return None

        try:
            # Parse ISO 8601 format with timezone
            from dateutil import parser

            return parser.isoparse(datetime_str)
        except (ValueError, ImportError):
            # Fallback: try basic ISO format without dateutil
            try:
                # Remove timezone suffix for basic parsing
                if "+" in datetime_str:
                    datetime_str = datetime_str.split("+")[0]
                elif datetime_str.count("-") > 2:  # Has timezone like -05:00
                    # Remove timezone
                    datetime_str = (
                        datetime_str.rsplit("-", 1)[0] if "T" in datetime_str else datetime_str
                    )

                # Parse as naive datetime then make timezone-aware
                dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
                return timezone.make_aware(dt)
            except ValueError:
                return None

    # ===================================================================
    # INTERNATIONAL SHIPPING / CUSTOMS CLEARANCE METHODS
    # ===================================================================

    def build_customs_clearance_detail(
        self,
        order_items: list[dict[str, Any]],
        duties_payment: str = "SENDER",
        commercial_invoice_terms: str = "DDU",
        currency: str = None,
    ) -> dict[str, Any]:
        """
        Build customs clearance detail for international shipments.

        Required for all international shipments outside the origin country.

        Args:
            order_items: List of order items with products and quantities
            duties_payment: Who pays duties ('SENDER' or 'RECIPIENT')
            commercial_invoice_terms: Terms of sale ('DDU' or 'DDP')
                - DDU: Delivered Duty Unpaid (recipient pays customs duties)
                - DDP: Delivered Duty Paid (sender pays customs duties)
            currency: ISO currency code (default: USD)

        Returns:
            Dict containing customsClearanceDetail structure for FedEx API

        Raises:
            FedExValidationError: If products missing required customs data
        """
        currency = currency or get_default_currency()
        logger.info(f"Building customs clearance detail for {len(order_items)} items")

        # Build commodity list
        commodities = self._build_commodity_items(order_items, currency)

        # Calculate total customs value
        customs_value = sum(
            Decimal(str(commodity["customsValue"]["amount"])) for commodity in commodities
        )

        # Build duties payment structure
        duties_payment_struct = {
            "paymentType": duties_payment,
            "payor": {"responsibleParty": {"accountNumber": {"value": self.account_number}}},
        }

        # Build customs clearance detail
        customs_clearance = {
            "dutiesPayment": duties_payment_struct,
            "commodities": commodities,
            "commercialInvoice": {
                "purpose": "SOLD",  # Other options: GIFT, SAMPLE, REPAIR, etc.
                "termsOfSale": commercial_invoice_terms,
            },
        }

        logger.info(
            f"Customs clearance detail built: "
            f"{len(commodities)} items, "
            f"total value: {currency} {customs_value:.2f}"
        )

        return customs_clearance

    def _build_commodity_items(
        self,
        order_items: list[dict[str, Any]],
        currency: str = None,
    ) -> list[dict[str, Any]]:
        """
        Build commodity items list for customs declaration.

        Each commodity must include:
        - Description (max 35 chars)
        - Quantity
        - Unit price
        - Customs value (unit price × quantity)
        - Weight
        - Country of manufacture (ISO 2-letter code)
        - HS code (Harmonized System tariff code)

        Args:
            order_items: List of order items with 'product' and 'quantity'
            currency: ISO currency code

        Returns:
            List of commodity item dictionaries

        Raises:
            FedExValidationError: If any product missing required customs data
        """
        currency = currency or get_default_currency()
        commodities = []

        for item in order_items:
            product = item.get("product")
            quantity = item.get("quantity", 1)

            if not product:
                raise FedExValidationError("Order item missing product")

            # Validate product has required international shipping data
            if not product.is_international_shipping_ready():
                missing_fields = product.get_missing_customs_fields()
                raise FedExValidationError(
                    f"Product '{product.name}' (SKU: {product.sku}) is not ready for international shipping. "
                    f"Missing required customs fields: {', '.join(missing_fields)}. "
                    f"Please update the product in the catalog admin."
                )

            # Calculate values
            unit_price = product.unit_price_for_customs
            total_value = unit_price * Decimal(str(quantity))

            # Build commodity item
            commodity = {
                "description": product.name[:35],  # FedEx limit: 35 characters
                "quantity": quantity,
                "quantityUnits": "PCS",  # Pieces
                "unitPrice": {
                    "currency": currency,
                    "amount": float(unit_price),
                },
                "customsValue": {
                    "currency": currency,
                    "amount": float(total_value),
                },
                "weight": {
                    "units": "LB",
                    "value": float(product.weight or 0),
                },
                "countryOfManufacture": product.country_of_origin,
                "harmonizedCode": product.hs_code,
            }

            # Add export license if present
            if product.export_license_number:
                commodity["exportLicenseNumber"] = product.export_license_number
                if product.export_license_expiry:
                    commodity["exportLicenseExpirationDate"] = (
                        product.export_license_expiry.isoformat()
                    )

            commodities.append(commodity)

        return commodities

    def validate_international_shipping_address(
        self,
        address: dict[str, Any],
    ) -> None:
        """
        Validate address for international shipping.

        International shipments have stricter requirements than domestic.

        Args:
            address: Address dictionary

        Raises:
            FedExValidationError: If address validation fails
        """
        required_fields = ["country", "postal_code", "city"]

        # For non-US destinations, state/province may be required
        if address.get("country") not in ["US", "CA"]:
            # Most countries don't require state, but validate what we have
            pass
        else:
            required_fields.append("state_province")

        missing = [field for field in required_fields if not address.get(field)]

        if missing:
            raise FedExValidationError(
                f"International shipping address missing required fields: {', '.join(missing)}"
            )

        # Validate country code format (must be 2-letter ISO)
        country = address.get("country", "")
        if len(country) != 2:
            raise FedExValidationError(
                f"Invalid country code: {country}. Must be 2-letter ISO code (e.g., 'CA', 'GB', 'DE')"
            )

    def check_export_compliance(
        self,
        destination_country: str,
        order_items: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Check export compliance for international shipment.

        Validates:
        - Export licenses for controlled items
        - Country embargoes and restrictions
        - EEI (Electronic Export Information) requirements

        Args:
            destination_country: ISO 2-letter country code
            order_items: List of order items with products

        Returns:
            {
                'compliant': bool,
                'requires_eei': bool,  # Electronic Export Information
                'warnings': List[str],
                'errors': List[str],
            }
        """
        logger.info(f"Checking export compliance for shipment to {destination_country}")

        warnings = []
        errors = []
        requires_eei = False

        # Check for embargoed countries (basic list - expand as needed)
        # Source: https://www.trade.gov/country-commercial-guides
        embargoed_countries = ["CU", "IR", "KP", "SY"]  # Cuba, Iran, North Korea, Syria

        if destination_country in embargoed_countries:
            errors.append(
                f"Cannot ship to {destination_country}: Country is subject to US trade embargo. "
                f"Shipment blocked for compliance."
            )

        # Calculate total customs value and check for EEI requirement
        total_value = Decimal("0")
        for item in order_items:
            product = item.get("product")
            quantity = item.get("quantity", 1)

            if product and product.unit_price_for_customs:
                total_value += product.unit_price_for_customs * Decimal(str(quantity))

            # Check for export licenses
            if product and product.export_license_number:
                # Verify license hasn't expired
                if product.export_license_expiry:
                    from django.utils import timezone

                    if product.export_license_expiry < timezone.now().date():
                        errors.append(
                            f"Product '{product.name}' has expired export license "
                            f"(expired: {product.export_license_expiry}). "
                            f"Update license before shipping."
                        )

        # EEI required for shipments > $2,500 USD or to certain countries
        # https://www.census.gov/foreign-trade/regulations/
        if total_value > Decimal("2500.00"):
            requires_eei = True
            warnings.append(
                f"Shipment value (${total_value:.2f}) exceeds $2,500. "
                f"Electronic Export Information (EEI) filing required via AES. "
                f"Consult with customs broker."
            )

        # Additional high-risk countries that may require EEI regardless of value
        eei_countries = ["RU", "CN"]  # Russia, China (example - verify with legal)
        if destination_country in eei_countries:
            requires_eei = True
            warnings.append(
                f"Destination country ({destination_country}) may require EEI filing. "
                f"Verify with customs broker."
            )

        compliant = len(errors) == 0

        result = {
            "compliant": compliant,
            "requires_eei": requires_eei,
            "warnings": warnings,
            "errors": errors,
        }

        if not compliant:
            logger.warning(f"Export compliance check FAILED for {destination_country}: {errors}")
        else:
            logger.info(f"Export compliance check passed for {destination_country}")

        return result

    def verify_webhook_signature(self, payload: bytes, signature: str, **kwargs) -> bool:
        """
        Verify FedEx webhook signature.

        NOTE: FedEx REST API does not support webhooks as of v1.0.
        Use polling with get_tracking() instead.

        Args:
            payload: Raw request body
            signature: Signature header
            **kwargs: Additional headers

        Returns:
            False (webhooks not supported)

        Raises:
            NotImplementedError: FedEx does not support webhooks
        """
        raise NotImplementedError(
            _("FedEx REST API does not support webhooks. Use polling instead.")
        )

    def handle_webhook(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Handle FedEx webhook event.

        NOTE: FedEx REST API does not support webhooks as of v1.0.
        Use polling with get_tracking() instead.

        Args:
            event_type: Event type
            payload: Webhook payload

        Returns:
            Processed webhook data

        Raises:
            NotImplementedError: FedEx does not support webhooks
        """
        raise NotImplementedError(
            _("FedEx REST API does not support webhooks. Use polling instead.")
        )
