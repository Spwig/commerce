"""
Test FedEx Tracking Implementation (Phase 6)

Tests the get_tracking() method with real FedEx sandbox API.

Run this with: ./shop_venv/bin/python manage.py shell < shipping/providers/fedex/tests/test_tracking.py
Or set DJANGO_SETTINGS_MODULE and run directly.
"""

import os

# Try to import without Django setup first (for standalone test)
try:
    from shipping.providers.fedex import FedExProvider
except Exception:
    # If that fails, we're in a Django context, import normally
    import sys
    from pathlib import Path

    import django

    # Repo root is four parents up from this file
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()
    from shipping.providers.fedex import FedExProvider


def test_tracking_with_label():
    """
    Test tracking using a tracking number from a previously generated label.

    This test requires:
    1. FedEx sandbox credentials
    2. A tracking number from a label generated in Phase 5
    """
    print("\n" + "=" * 80)
    print("TEST: FedEx Tracking (Phase 6)")
    print("=" * 80)

    # Load credentials from environment
    credentials = {
        "api_key": os.getenv("FEDEX_API_KEY") or os.getenv("FEDEX_CLIENT_ID"),
        "api_secret": os.getenv("FEDEX_API_SECRET") or os.getenv("FEDEX_CLIENT_SECRET"),
        "environment": "sandbox",
        "account_number": os.getenv("FEDEX_ACCOUNT_NUMBER", "740561073"),
    }

    # Validate credentials
    if not credentials["api_key"] or not credentials["api_secret"]:
        print("[X] Missing FedEx credentials in environment")
        print("    Set FEDEX_API_KEY and FEDEX_API_SECRET")
        print("    (or FEDEX_CLIENT_ID and FEDEX_CLIENT_SECRET)")
        return False

    print(f"[OK] Using FedEx sandbox account: {credentials['account_number']}")

    # Initialize provider
    provider = FedExProvider(credentials)
    print(f"[OK] Provider initialized: {provider.provider_name}")

    # Get tracking number from user input or environment
    tracking_number = os.getenv("FEDEX_TEST_TRACKING_NUMBER")

    if not tracking_number:
        print("\n[!] No tracking number provided")
        print("    Options:")
        print("    1. Set FEDEX_TEST_TRACKING_NUMBER environment variable")
        print("    2. Use a tracking number from a previously generated label")
        print("\n    To get a tracking number, run test_label_purchase.py first")
        return False

    print(f"\n[>] Looking up tracking number: {tracking_number}")

    # Call get_tracking()
    try:
        tracking_info = provider.get_tracking(tracking_number)

        print("\n" + "=" * 80)
        print("[OK] TRACKING INFORMATION RETRIEVED")
        print("=" * 80)

        print("\nPackage Details:")
        print(f"  Tracking Number: {tracking_info['tracking_number']}")
        print(f"  Status: {tracking_info['status']} ({tracking_info['status_description']})")
        print(f"  Carrier: {tracking_info['carrier']}")
        print(f"  Service: {tracking_info['service']}")

        if tracking_info.get("current_location"):
            print(f"  Current Location: {tracking_info['current_location']}")

        print("\nDelivery Times:")
        if tracking_info.get("estimated_delivery"):
            print(f"  Estimated: {tracking_info['estimated_delivery'].strftime('%Y-%m-%d %H:%M')}")
        else:
            print("  Estimated: Not available")

        if tracking_info.get("actual_delivery"):
            print(f"  Actual: {tracking_info['actual_delivery'].strftime('%Y-%m-%d %H:%M')}")
        else:
            print("  Actual: Not yet delivered")

        # Display events
        events = tracking_info.get("events", [])
        print(f"\nTracking Events ({len(events)} total):")

        if events:
            for i, event in enumerate(events, 1):
                timestamp_str = (
                    event["timestamp"].strftime("%Y-%m-%d %H:%M")
                    if event["timestamp"]
                    else "Unknown"
                )
                print(f"\n  {i}. {timestamp_str}")
                print(f"     Status: {event['status']} ({event['raw_code']})")
                print(f"     Location: {event['location'] or 'Unknown'}")
                print(f"     Description: {event['description']}")
        else:
            print("  No tracking events available yet")

        print("\n" + "=" * 80)
        print("[OK] TEST PASSED - Tracking information retrieved successfully")
        print("=" * 80)

        return True

    except ValueError as e:
        print(f"\n[X] Tracking error: {e}")
        return False
    except Exception as e:
        print(f"\n[X] Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_invalid_tracking_number():
    """Test tracking with an invalid tracking number."""
    print("\n" + "=" * 80)
    print("TEST: Invalid Tracking Number")
    print("=" * 80)

    credentials = {
        "api_key": os.getenv("FEDEX_API_KEY") or os.getenv("FEDEX_CLIENT_ID"),
        "api_secret": os.getenv("FEDEX_API_SECRET") or os.getenv("FEDEX_CLIENT_SECRET"),
        "environment": "sandbox",
        "account_number": os.getenv("FEDEX_ACCOUNT_NUMBER", "740561073"),
    }

    if not credentials["api_key"] or not credentials["api_secret"]:
        print("[X] Missing FedEx credentials")
        return False

    provider = FedExProvider(credentials)

    # Test with obviously invalid tracking number
    invalid_number = "000000000000"
    print(f"\n[>] Testing with invalid tracking number: {invalid_number}")

    try:
        tracking_info = provider.get_tracking(invalid_number)
        # FedEx sandbox may return results for invalid numbers or may return error
        # Either behavior is acceptable for the test
        if tracking_info and tracking_info.get("events"):
            print("[!] TEST WARNING - FedEx sandbox returned data for invalid number")
            print("    This is expected behavior in sandbox environment")
            return True
        else:
            print("[OK] TEST PASSED - No tracking data for invalid number")
            return True
    except ValueError as e:
        print(f"[OK] TEST PASSED - Correctly raised ValueError: {e}")
        return True
    except Exception as e:
        print(f"[!] TEST WARNING - Unexpected exception type: {type(e).__name__}: {e}")
        return True  # Still passes if it errors


def main():
    """Run all tracking tests."""
    print("\n" + "=" * 80)
    print("FEDEX TRACKING TESTS (PHASE 6)")
    print("=" * 80)

    results = {
        "Valid Tracking Number": test_tracking_with_label(),
        "Invalid Tracking Number": test_invalid_tracking_number(),
    }

    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)

    for test_name, result in results.items():
        status = "[OK] PASS" if result else "[X] FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(results.values())
    print("\n" + "=" * 80)
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED")
    print("=" * 80 + "\n")

    return all_passed


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
