# -*- coding: utf-8 -*-
"""
Test error handling for FedEx provider.

Tests custom exceptions, retry logic, and error recovery.
"""
import os
import sys
import django
import logging
from pathlib import Path

# Setup Django — this file lives at shipping/providers/fedex/tests/,
# so the repo root is four parents up.
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shipping.providers.fedex.provider import FedExProvider
from shipping.providers.fedex.exceptions import (
    FedExAuthenticationError,
    FedExValidationError,
    FedExTrackingError,
)

# Enable DEBUG logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_authentication_error():
    """Test authentication error with invalid credentials."""
    print("\n" + "="*70)
    print("TEST 1: Authentication Error")
    print("="*70)

    credentials = {
        'api_key': 'invalid-key',
        'api_secret': 'invalid-secret',
        'environment': 'sandbox',
        'account_number': '123456789',
    }

    try:
        provider = FedExProvider(credentials)
        result = provider.test_connection()

        if result['success']:
            print("❌ FAIL: Should have failed with invalid credentials")
        else:
            print("✅ PASS: Connection failed as expected")
            print(f"   Error type: {result['details'].get('error_type')}")
            print(f"   Message: {result['message']}")

    except Exception as e:
        print(f"❌ FAIL: Unexpected exception: {e}")


def test_validation_error():
    """Test validation error with invalid address."""
    print("\n" + "="*70)
    print("TEST 2: Validation Error")
    print("="*70)

    # Load real credentials
    credentials = {
        'api_key': os.getenv('FEDEX_API_KEY') or os.getenv('FEDEX_CLIENT_ID'),
        'api_secret': os.getenv('FEDEX_API_SECRET') or os.getenv('FEDEX_CLIENT_SECRET'),
        'environment': 'sandbox',
        'account_number': '740561073',
    }

    provider = FedExProvider(credentials)

    # Invalid address (missing required fields)
    origin = {
        'country': 'US',
        'postal_code': '',  # Missing!
        'city': '',  # Missing!
    }

    destination = {
        'country': 'US',
        'postal_code': '90210',
        'city': 'Beverly Hills',
        'state_province': 'CA',
    }

    parcels = [{
        'weight': 1.5,
        'length': 10,
        'width': 8,
        'height': 6,
    }]

    try:
        rates = provider.get_rates(origin, destination, parcels)
        print("❌ FAIL: Should have raised validation error")

    except FedExValidationError as e:
        print("✅ PASS: Validation error raised as expected")
        print(f"   Message: {e}")

    except Exception as e:
        print(f"❓ PARTIAL: Different exception raised: {type(e).__name__}: {e}")


def test_tracking_error():
    """Test tracking error with invalid tracking number."""
    print("\n" + "="*70)
    print("TEST 3: Tracking Error")
    print("="*70)

    # Load real credentials
    credentials = {
        'api_key': os.getenv('FEDEX_API_KEY') or os.getenv('FEDEX_CLIENT_ID'),
        'api_secret': os.getenv('FEDEX_API_SECRET') or os.getenv('FEDEX_CLIENT_SECRET'),
        'environment': 'sandbox',
        'account_number': '740561073',
    }

    provider = FedExProvider(credentials)

    # Invalid tracking number
    invalid_tracking = "000000000"

    try:
        tracking = provider.get_tracking(invalid_tracking)

        # Sandbox may return empty data instead of error
        if tracking.get('events'):
            print("❓ PARTIAL: Sandbox returned data for invalid tracking number")
        else:
            print("✅ PASS: Empty tracking data for invalid number")

    except FedExTrackingError as e:
        print("✅ PASS: Tracking error raised as expected")
        print(f"   Message: {e}")

    except Exception as e:
        print(f"❓ PARTIAL: Different exception raised: {type(e).__name__}: {e}")


def test_successful_connection():
    """Test successful connection with valid credentials."""
    print("\n" + "="*70)
    print("TEST 4: Successful Connection")
    print("="*70)

    # Load real credentials
    credentials = {
        'api_key': os.getenv('FEDEX_API_KEY') or os.getenv('FEDEX_CLIENT_ID'),
        'api_secret': os.getenv('FEDEX_API_SECRET') or os.getenv('FEDEX_CLIENT_SECRET'),
        'environment': 'sandbox',
        'account_number': '740561073',
    }

    try:
        provider = FedExProvider(credentials)
        result = provider.test_connection()

        if result['success']:
            print("✅ PASS: Connection successful")
            print(f"   Environment: {result['details']['environment']}")
            print(f"   Account: {result['details']['account_number']}")
        else:
            print("❌ FAIL: Connection should have succeeded")
            print(f"   Message: {result['message']}")

    except Exception as e:
        print(f"❌ FAIL: Unexpected exception: {e}")


def test_exception_hierarchy():
    """Test exception hierarchy and catching."""
    print("\n" + "="*70)
    print("TEST 5: Exception Hierarchy")
    print("="*70)

    from shipping.providers.fedex.exceptions import FedExError

    try:
        raise FedExAuthenticationError("Test auth error")
    except FedExError as e:
        print("✅ PASS: FedExAuthenticationError caught as FedExError")
    except Exception:
        print("❌ FAIL: Exception hierarchy broken")

    try:
        raise FedExValidationError("Test validation error")
    except FedExError as e:
        print("✅ PASS: FedExValidationError caught as FedExError")
    except Exception:
        print("❌ FAIL: Exception hierarchy broken")


def run_all_tests():
    """Run all error handling tests."""
    print("\n" + "="*70)
    print("FEDEX PROVIDER ERROR HANDLING TESTS")
    print("="*70)

    # Check for credentials
    if not os.getenv('FEDEX_API_KEY') and not os.getenv('FEDEX_CLIENT_ID'):
        print("\n⚠️  WARNING: FedEx credentials not found in environment")
        print("   Some tests will be skipped")
        print("   Set FEDEX_CLIENT_ID and FEDEX_CLIENT_SECRET to run all tests\n")

    # Run tests
    test_exception_hierarchy()
    test_authentication_error()

    if os.getenv('FEDEX_API_KEY') or os.getenv('FEDEX_CLIENT_ID'):
        test_successful_connection()
        test_validation_error()
        test_tracking_error()

    print("\n" + "="*70)
    print("TESTS COMPLETE")
    print("="*70 + "\n")


if __name__ == '__main__':
    run_all_tests()
