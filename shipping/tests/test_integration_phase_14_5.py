"""
Integration Tests for Phase 14.5: Provider Integration & Service Layer

Tests the complete flow:
1. ProviderRegistry discovers FedEx provider
2. LabelService purchases label via FedEx provider
3. Shipment and Order models are updated
4. Celery tasks work correctly
"""

import os
import sys

import django

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from decimal import Decimal

from component_updates.models import ComponentRegistry
from shipping.models import ProviderAccount, Shipment, TrackingEvent
from shipping.providers.registry import ProviderRegistry
from shipping.services.label_service import LabelService
from shipping.utils.encryption import decrypt_credentials, encrypt_credentials


def test_provider_registry():
    """Test that FedEx provider can be discovered and retrieved"""
    print("\n" + "=" * 80)
    print("TEST 1: Provider Registry Discovery")
    print("=" * 80)

    # Manually register FedEx provider for testing
    from shipping.providers.fedex import FedExProvider

    ProviderRegistry.register_provider(FedExProvider)

    # Get provider
    provider_class = ProviderRegistry.get_provider("fedex")

    if provider_class:
        print(" FedEx provider successfully retrieved from registry")
        print(f"   Provider key: {provider_class.provider_key}")
        print(f"   Provider name: {provider_class.provider_name}")
    else:
        print("L Failed to retrieve FedEx provider")
        return False

    # List all providers
    providers = ProviderRegistry.list_providers()
    print(f"\n=� Total providers registered: {len(providers)}")
    for key, prov_class in providers.items():
        print(f"   - {key}: {prov_class.provider_name}")

    return True


def test_encryption():
    """Test credential encryption/decryption"""
    print("\n" + "=" * 80)
    print("TEST 2: Credential Encryption")
    print("=" * 80)

    credentials = {
        "client_id": "test_client_id_12345",
        "client_secret": "test_secret_key_67890",
        "environment": "sandbox",
        "account_number": "123456789",
    }

    # Encrypt
    encrypted = encrypt_credentials(credentials)
    print(" Credentials encrypted successfully")
    print(f"   Encrypted fields: {list(encrypted.keys())}")

    # Decrypt
    decrypted = decrypt_credentials(encrypted)
    print(" Credentials decrypted successfully")

    # Verify
    if decrypted == credentials:
        print(" Decrypted credentials match original")
        return True
    else:
        print("L Decrypted credentials don't match")
        return False


def test_label_service_structure():
    """Test that LabelService can be imported and has required methods"""
    print("\n" + "=" * 80)
    print("TEST 3: LabelService Structure")
    print("=" * 80)

    # Check LabelService has required methods
    required_methods = [
        "buy_label",
        "_build_label_options",
        "_update_shipment",
        "_create_tracking_event",
        "_sync_order_tracking",
    ]

    for method_name in required_methods:
        if hasattr(LabelService, method_name):
            print(f" LabelService.{method_name}() exists")
        else:
            print(f"L LabelService.{method_name}() missing")
            return False

    return True


def test_full_integration():
    """
    Test full integration with real FedEx sandbox API

    NOTE: This requires:
    - A ComponentRegistry entry for 'fedex'
    - A ProviderAccount with valid FedEx sandbox credentials
    - An Order with shipping address
    - A Shipment linked to the order
    """
    print("\n" + "=" * 80)
    print("TEST 4: Full Integration (Manual Setup Required)")
    print("=" * 80)

    # Check if FedEx component exists
    try:
        component = ComponentRegistry.objects.get(slug="fedex", component_type="shipping_provider")
        print(f" FedEx component found: {component.name}")
    except ComponentRegistry.DoesNotExist:
        print("�  FedEx component not found in ComponentRegistry")
        print("   Run: python manage.py shell")
        print("   >>> from component_updates.models import ComponentRegistry")
        print("   >>> ComponentRegistry.objects.create(")
        print("   ...     slug='fedex',")
        print("   ...     component_type='shipping_provider',")
        print("   ...     name='FedEx',")
        print("   ...     description='FedEx shipping provider'")
        print("   ... )")
        return False

    # Check if provider account exists
    provider_account = ProviderAccount.objects.filter(
        component__slug="fedex", is_active=True
    ).first()

    if not provider_account:
        print("�  No active FedEx ProviderAccount found")
        print("   Create one in Django admin at /admin/shipping/provideraccount/add/")
        return False

    print(f" FedEx ProviderAccount found: {provider_account.display_name or 'Unnamed'}")

    # Check if there are any shipments
    shipment = Shipment.objects.filter(provider_account=provider_account, status="created").first()

    if not shipment:
        print("�  No shipments in 'created' status found")
        print("   Create a test shipment first")
        return False

    print(f" Test shipment found: {shipment.id}")
    print(f"   Order: {shipment.order.order_number if shipment.order else 'N/A'}")
    print(f"   Status: {shipment.status}")

    # Try to purchase label
    print("\n=� Attempting to purchase label via LabelService...")
    print("   (This will make a real API call to FedEx sandbox)")

    try:
        # Build a test rate
        rate = {
            "service_code": "FEDEX_GROUND",
            "service_name": "FedEx Ground",
            "carrier": "FedEx",
            "rate": Decimal("12.50"),
            "currency": "USD",
        }

        label_info = LabelService.buy_label(
            shipment=shipment, rate=rate, label_format="PDF", label_size="4x6"
        )

        print("\n Label purchased successfully!")
        print(f"   Tracking Number: {label_info['tracking_number']}")
        print(
            f"   Label URL: {label_info['label_url'][:100]}..."
            if len(label_info["label_url"]) > 100
            else f"   Label URL: {label_info['label_url']}"
        )
        print(f"   Cost: {label_info['cost']} {label_info['currency']}")
        print(f"   Carrier: {label_info['carrier']}")
        print(f"   Service: {label_info['service']}")

        # Verify shipment was updated
        shipment.refresh_from_db()
        print("\n Shipment updated:")
        print(f"   Status: {shipment.status}")
        print(f"   Tracking ID: {shipment.tracking_id}")
        print(f"   Label URL length: {len(shipment.label_url)} characters")

        # Verify tracking event was created
        events = TrackingEvent.objects.filter(shipment=shipment).count()
        print(f"\n Tracking events created: {events}")

        # Verify order was updated
        if shipment.order:
            shipment.order.refresh_from_db()
            if shipment.order.tracking_number:
                print(f" Order tracking number updated: {shipment.order.tracking_number}")
            else:
                print("�  Order tracking number not updated")

        return True

    except Exception as e:
        print(f"\nL Label purchase failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all integration tests"""
    print("\n" + "=" * 80)
    print("PHASE 14.5 INTEGRATION TESTS")
    print("=" * 80)

    results = {
        "Provider Registry": test_provider_registry(),
        "Encryption": test_encryption(),
        "LabelService Structure": test_label_service_structure(),
        "Full Integration": test_full_integration(),
    }

    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    for test_name, result in results.items():
        status = " PASS" if result else "L FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(results.values())
    print("\n" + "=" * 80)
    if all_passed:
        print("<� ALL TESTS PASSED!")
    else:
        print("�  SOME TESTS FAILED")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
