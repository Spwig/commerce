# -*- coding: utf-8 -*-
"""
Custom exceptions for FedEx provider.

This module defines FedEx-specific exceptions to provide better error handling
and more informative error messages throughout the provider implementation.
"""
from django.utils.translation import gettext_lazy as _


class FedExError(Exception):
    """Base exception for all FedEx-related errors."""
    pass


class FedExAuthenticationError(FedExError):
    """
    Raised when FedEx API authentication fails.

    Common causes:
    - Invalid API key or secret
    - Expired OAuth token
    - Credentials for wrong environment (sandbox vs production)
    """
    pass


class FedExAuthorizationError(FedExError):
    """
    Raised when FedEx API authorization fails.

    Common causes:
    - Account doesn't have permission for requested service
    - Account not enabled for international shipping
    - Account not enabled for specific service type
    """
    pass


class FedExValidationError(FedExError):
    """
    Raised when FedEx API request validation fails.

    Common causes:
    - Invalid address format
    - Missing required fields
    - Invalid service type for route
    - Invalid package dimensions/weight
    """
    pass


class FedExRateLimitError(FedExError):
    """
    Raised when FedEx API rate limit is exceeded.

    The error includes retry_after attribute indicating when to retry.
    """
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


class FedExServiceUnavailableError(FedExError):
    """
    Raised when FedEx API is temporarily unavailable.

    This is typically a temporary issue. Retry with exponential backoff.
    """
    pass


class FedExAccountError(FedExError):
    """
    Raised when there's an issue with the FedEx account.

    Common causes:
    - Account number mismatch
    - Account suspended or disabled
    - Account not registered for API access
    """
    pass


class FedExShipmentError(FedExError):
    """
    Raised when there's an error with shipment creation or processing.

    Common causes:
    - Invalid shipment data
    - Service not available for route
    - Package restrictions violated
    """
    pass


class FedExTrackingError(FedExError):
    """
    Raised when tracking information cannot be retrieved.

    Common causes:
    - Invalid tracking number
    - Tracking number not yet in system
    - Shipment too old (archived)
    """
    pass


class FedExDocumentError(FedExError):
    """
    Raised when there's an error with document upload or processing.

    Common causes:
    - Document file too large (>5MB)
    - Unsupported file format
    - Document upload failed
    - Invalid document type
    """
    pass


class FedExAPIError(FedExError):
    """
    Raised for general FedEx API errors that don't fit other categories.

    Includes the error code and full error details from FedEx.
    """
    def __init__(self, message, error_code=None, error_details=None):
        super().__init__(message)
        self.error_code = error_code
        self.error_details = error_details or {}


# Error code mappings from FedEx API to custom exceptions
FEDEX_ERROR_CODE_MAP = {
    # Authentication errors
    'NOT.AUTHORIZED.ERROR': FedExAuthenticationError,
    'UNAUTHORIZED': FedExAuthenticationError,
    'AUTHENTICATION.ERROR': FedExAuthenticationError,
    'INVALID.ACCESS.TOKEN': FedExAuthenticationError,

    # Authorization errors
    'FORBIDDEN.ERROR': FedExAuthorizationError,
    'FORBIDDEN': FedExAuthorizationError,
    'INSUFFICIENT.PERMISSIONS': FedExAuthorizationError,

    # Account errors
    'ACCOUNT.NUMBER.MISMATCH': FedExAccountError,
    'ACCOUNTNUMBER.REGISTRATION.REQUIRED': FedExAccountError,
    'INVALID.ACCOUNT.NUMBER': FedExAccountError,
    'ACCOUNT.SUSPENDED': FedExAccountError,

    # Validation errors
    'VALIDATION.ERROR': FedExValidationError,
    'INVALID.INPUT.DATA': FedExValidationError,
    'MISSING.REQUIRED.FIELD': FedExValidationError,
    'INVALID.ADDRESS': FedExValidationError,

    # Rate limit errors
    'RATE.LIMIT.EXCEEDED': FedExRateLimitError,
    'TOO.MANY.REQUESTS': FedExRateLimitError,

    # Service availability errors
    'SERVICE.UNAVAILABLE.ERROR': FedExServiceUnavailableError,
    'INTERNAL.SERVER.ERROR': FedExServiceUnavailableError,
    'GATEWAY.TIMEOUT': FedExServiceUnavailableError,
    'SERVICE.TEMPORARILY.UNAVAILABLE': FedExServiceUnavailableError,

    # Shipment errors
    'SHIPMENT.NOT.FOUND': FedExShipmentError,
    'INVALID.SHIPMENT.DATA': FedExShipmentError,
    'SERVICE.NOT.AVAILABLE': FedExShipmentError,

    # Tracking errors
    'TRACKING.NUMBER.NOT.FOUND': FedExTrackingError,
    'INVALID.TRACKING.NUMBER': FedExTrackingError,
    'TRACKING.DATA.UNAVAILABLE': FedExTrackingError,

    # Document errors
    'DOCUMENT.UPLOAD.FAILED': FedExDocumentError,
    'INVALID.DOCUMENT.TYPE': FedExDocumentError,
    'DOCUMENT.SIZE.EXCEEDED': FedExDocumentError,
    'UNSUPPORTED.DOCUMENT.FORMAT': FedExDocumentError,
}


def get_exception_for_error_code(error_code):
    """
    Get the appropriate exception class for a FedEx error code.

    Args:
        error_code: FedEx API error code string

    Returns:
        Exception class to raise, defaults to FedExAPIError
    """
    return FEDEX_ERROR_CODE_MAP.get(error_code, FedExAPIError)
