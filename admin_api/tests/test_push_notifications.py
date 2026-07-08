"""
Test script for APNs push notifications via push.spwig.com

Usage:
    # From project root with venv activated:
    ./shop_venv/bin/python -c "from admin_api.tests.test_push_notifications import *; run_all_tests()"

    # Or run individual tests:
    ./shop_venv/bin/python -c "from admin_api.tests.test_push_notifications import *; test_push_config()"
    ./shop_venv/bin/python -c "from admin_api.tests.test_push_notifications import *; test_new_order_notification()"
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from decimal import Decimal


def set_test_installation_uuid():
    """Set a test installation UUID for development testing."""
    import uuid
    from core.models import PlatformSecrets

    secrets = PlatformSecrets.get_secrets()

    if secrets.installation_uuid:
        print(f"  Installation UUID already set: {secrets.installation_uuid}")
        return str(secrets.installation_uuid)

    test_uuid = str(uuid.uuid4())
    secrets.installation_uuid = test_uuid
    secrets.save()
    print(f"  Set test installation UUID: {test_uuid}")
    print("  [WARNING] This is for TESTING ONLY!")
    return test_uuid


def test_push_config(setup_test_env=False):
    """Test 1: Check push service configuration."""
    print("\n" + "="*60)
    print("TEST 1: Push Service Configuration")
    print("="*60)

    from admin_api.services.push_client import PushClient
    from core.platform_secrets import get_push_secret, get_installation_uuid

    client = PushClient()

    # Check configuration
    print("\n1.1 Checking configuration...")
    push_secret = get_push_secret()
    installation_uuid = get_installation_uuid()

    print(f"  - Installation UUID: {installation_uuid if installation_uuid else '[NOT SET]'}")
    print(f"  - Push Secret: {'[SET]' if push_secret else '[NOT SET]'}")
    print(f"  - Push Service URL: {client.base_url}")
    print(f"  - Is Configured: {client.is_configured()}")

    # Setup test environment if requested
    if setup_test_env and not installation_uuid:
        print("\n1.2 Setting up test environment...")
        set_test_installation_uuid()
        # Re-check configuration
        installation_uuid = get_installation_uuid()
        print(f"  - Installation UUID now: {installation_uuid}")

    if not client.is_configured():
        print("\n  [WARNING] Push notifications are NOT configured!")
        print("  Run with setup_test_env=True to set a test UUID for development.")
        print("  Production requires proper license server registration.")
        return False

    # Health check
    print("\n1.3 Health check...")
    health = client.health_check()
    print(f"  - Service Healthy: {health.get('healthy')}")
    if health.get('error'):
        print(f"  - Error: {health.get('error')}")

    return health.get('healthy', False)


def register_test_device(push_token, user_email=None):
    """
    Register a test device for push notifications.

    Args:
        push_token: The APNs push token from your iOS device
        user_email: Email of staff user to associate (defaults to first superuser)
    """
    from admin_api.models import DeviceRegistration
    from django.contrib.auth import get_user_model
    import uuid

    User = get_user_model()

    # Find user
    if user_email:
        user = User.objects.filter(email=user_email).first()
    else:
        user = User.objects.filter(is_superuser=True).first()

    if not user:
        print(f"  [ERROR] No user found!")
        return None

    # Create or update device registration
    device_id = f"test-device-{uuid.uuid4().hex[:8]}"

    device, created = DeviceRegistration.objects.update_or_create(
        push_token=push_token,
        defaults={
            'user': user,
            'device_id': device_id,
            'platform': 'ios',
            'notify_new_orders': True,
            'notify_low_stock': True,
            'notify_customer_messages': True,
            'is_active': True,
        }
    )

    action = "Created" if created else "Updated"
    print(f"  {action} device registration:")
    print(f"    - Device ID: {device.device_id}")
    print(f"    - User: {user.email}")
    print(f"    - Token: {push_token[:30]}...")

    return device


def test_list_devices():
    """Test 2: List registered devices."""
    print("\n" + "="*60)
    print("TEST 2: Registered Devices")
    print("="*60)

    from admin_api.models import DeviceRegistration

    devices = DeviceRegistration.objects.filter(is_active=True)
    print(f"\nActive devices: {devices.count()}")

    if devices.count() == 0:
        print("\n  [WARNING] No devices registered for push notifications!")
        print("  Register a device via: POST /api/admin/settings/devices/register/")
        print("  Or use: register_test_device('your-apns-token-here')")
        return []

    for device in devices:
        print(f"\n  Device: {device.device_id[:20]}...")
        print(f"    - User: {device.user.email}")
        print(f"    - Platform: {device.platform}")
        print(f"    - Token: {device.push_token[:30]}...")
        print(f"    - Notify Orders: {device.notify_new_orders}")
        print(f"    - Notify Low Stock: {device.notify_low_stock}")
        print(f"    - Notify Messages: {device.notify_customer_messages}")

    return list(devices)


def test_new_order_notification(dry_run=True):
    """Test 3: Simulate new order notification."""
    print("\n" + "="*60)
    print("TEST 3: New Order Notification")
    print("="*60)

    from admin_api.services.push_service import PushNotificationService
    from orders.models import Order

    # Get a recent order or create mock data
    order = Order.objects.order_by('-created_at').first()

    if not order:
        print("\n  [WARNING] No orders found in database!")
        return False

    print(f"\n  Using order: {order.order_number}")
    print(f"  - Status: {order.status}")
    print(f"  - Payment Status: {order.payment_status}")
    print(f"  - Total: {order.total_amount}")

    if dry_run:
        print("\n  [DRY RUN] Would send notification:")
        print(f"    Title: New Order Received")
        print(f"    Body: Order #{order.order_number} - {order.total_amount.amount} {order.total_amount.currency}")
        print(f"    Data: {{'type': 'new_order', 'order_number': '{order.order_number}', 'order_id': {order.id}}}")
        return True

    # Actually send the notification
    print("\n  Sending notification...")
    sent_count = PushNotificationService.send_new_order_notification(order)
    print(f"  Notifications sent: {sent_count}")

    return sent_count > 0


def test_customer_message_contact_form(dry_run=True):
    """Test 4: Simulate customer message notification (contact form)."""
    print("\n" + "="*60)
    print("TEST 4: Customer Message Notification (Contact Form)")
    print("="*60)

    from admin_api.services.push_service import PushNotificationService
    from admin_api.models import CustomerMessage

    # Get a recent message or show what would be sent
    message = CustomerMessage.objects.order_by('-created_at').first()

    if not message:
        print("\n  [INFO] No CustomerMessage found, showing sample notification...")
        print("\n  [DRY RUN] Would send notification:")
        print(f"    Title: New Customer Message")
        print(f"    Body: From Test User: Test Subject")
        print(f"    Data: {{'type': 'customer_message', 'source': 'contact_form', 'message_id': 1}}")
        return True

    print(f"\n  Using message ID: {message.id}")
    print(f"  - From: {message.name} <{message.email}>")
    print(f"  - Subject: {message.subject}")
    print(f"  - Status: {message.status}")

    if dry_run:
        print("\n  [DRY RUN] Would send notification:")
        print(f"    Title: New Customer Message")
        print(f"    Body: From {message.name}: {message.subject}")
        data = {
            'type': 'customer_message',
            'source': 'contact_form',
            'message_id': message.id,
            'sender_name': message.name,
        }
        print(f"    Data: {data}")
        return True

    # Actually send
    print("\n  Sending notification...")
    sent_count = PushNotificationService.send_customer_message_notification(message, source='contact_form')
    print(f"  Notifications sent: {sent_count}")

    return sent_count > 0


def test_customer_message_order_note(dry_run=True):
    """Test 5: Simulate customer message notification (order note)."""
    print("\n" + "="*60)
    print("TEST 5: Customer Message Notification (Order Note)")
    print("="*60)

    from admin_api.services.push_service import PushNotificationService
    from orders.models import OrderNote

    # Get a recent customer note
    note = OrderNote.objects.filter(is_customer_note=True).order_by('-created_at').first()

    if not note:
        print("\n  [INFO] No customer OrderNote found, showing sample notification...")
        print("\n  [DRY RUN] Would send notification:")
        print(f"    Title: New Customer Message")
        print(f"    Body: From Customer: Re: Order #ORD-12345")
        print(f"    Data: {{'type': 'customer_message', 'source': 'order_note', 'order_number': 'ORD-12345'}}")
        return True

    order = note.order
    customer_name = order.billing_name or order.shipping_name or 'Customer'

    print(f"\n  Using note ID: {note.id}")
    print(f"  - Order: {order.order_number}")
    print(f"  - From: {customer_name}")
    print(f"  - Note: {note.note[:50]}...")

    if dry_run:
        print("\n  [DRY RUN] Would send notification:")
        print(f"    Title: New Customer Message")
        print(f"    Body: From {customer_name}: Re: Order #{order.order_number}")
        data = {
            'type': 'customer_message',
            'source': 'order_note',
            'message_id': note.id,
            'order_number': order.order_number,
        }
        print(f"    Data: {data}")
        return True

    # Actually send
    print("\n  Sending notification...")
    sent_count = PushNotificationService.send_customer_message_notification(note, source='order_note')
    print(f"  Notifications sent: {sent_count}")

    return sent_count > 0


def test_low_stock_notification(dry_run=True):
    """Test 6: Simulate low stock notification."""
    print("\n" + "="*60)
    print("TEST 6: Low Stock Notification")
    print("="*60)

    from admin_api.services.push_service import PushNotificationService
    from catalog.models import Product

    # Get a product that tracks inventory
    product = Product.objects.filter(track_inventory=True).first()

    if not product:
        print("\n  [INFO] No inventory-tracked products, showing sample notification...")
        print("\n  [DRY RUN] Would send notification:")
        print(f"    Title: Low Stock Alert")
        print(f"    Body: Sample Product has only 5 units left")
        print(f"    Data: {{'type': 'low_stock', 'product_id': 1, 'sku': 'SKU-001', 'current_stock': 5}}")
        return True

    print(f"\n  Using product: {product.name}")
    print(f"  - SKU: {product.sku}")
    print(f"  - Low Stock Threshold: {product.low_stock_threshold}")

    # Simulate low stock
    current_stock = 5

    if dry_run:
        print("\n  [DRY RUN] Would send notification:")
        print(f"    Title: Low Stock Alert")
        print(f"    Body: {product.name} has only {current_stock} units left")
        data = {
            'type': 'low_stock',
            'product_id': product.id,
            'product_name': product.name,
            'sku': product.sku,
            'current_stock': current_stock,
        }
        print(f"    Data: {data}")
        return True

    # Actually send
    print("\n  Sending notification...")
    sent_count = PushNotificationService.send_low_stock_notification(product, current_stock)
    print(f"  Notifications sent: {sent_count}")

    return sent_count > 0


def test_direct_push(token=None):
    """Test 7: Send a direct test push notification."""
    print("\n" + "="*60)
    print("TEST 7: Direct Push Test")
    print("="*60)

    from admin_api.services.push_client import PushClient
    from admin_api.models import DeviceRegistration

    # Get token from argument or first registered device
    if not token:
        device = DeviceRegistration.objects.filter(is_active=True, platform='ios').first()
        if not device:
            print("\n  [ERROR] No active iOS device found!")
            return False
        token = device.push_token
        print(f"\n  Using device: {device.device_id[:20]}...")

    client = PushClient()

    # Check sandbox mode
    use_sandbox = getattr(settings, 'DEBUG', False)
    print(f"  - Using Sandbox: {use_sandbox}")
    print(f"  - Token: {token[:30]}...")

    print("\n  Sending test notification...")

    result = client.send_notification(
        tokens=[token],
        title="Test Notification",
        body="This is a test push notification from Spwig Admin API",
        data={
            'type': 'test',
            'timestamp': str(django.utils.timezone.now()),
        },
        sandbox=use_sandbox,
    )

    print(f"\n  Result:")
    print(f"    - Success: {result.success}")
    print(f"    - Sent: {result.sent}")
    print(f"    - Failed: {result.failed}")
    if result.error:
        print(f"    - Error: {result.error}")
    if result.results:
        for r in result.results:
            print(f"    - Token Result: {r}")

    return result.success and result.sent > 0


def run_all_tests(dry_run=True, setup_test_env=False):
    """
    Run all push notification tests.

    Args:
        dry_run: If True, show what would be sent without actually sending
        setup_test_env: If True, set test installation UUID if not configured
    """
    print("\n" + "="*60)
    print("PUSH NOTIFICATION TEST SUITE")
    print("="*60)
    print(f"\nDry Run Mode: {dry_run}")
    print(f"Setup Test Env: {setup_test_env}")
    if dry_run:
        print("(Set dry_run=False to actually send notifications)")

    results = {}

    # Test 1: Configuration
    results['config'] = test_push_config(setup_test_env=setup_test_env)

    # Test 2: List devices
    devices = test_list_devices()
    results['devices'] = len(devices) > 0

    if not results['config']:
        print("\n" + "="*60)
        print("STOPPING: Push service not configured")
        print("To set up test environment, run:")
        print("  run_all_tests(setup_test_env=True)")
        print("="*60)
        return results

    if not devices:
        print("\n" + "="*60)
        print("STOPPING: No devices registered")
        print("To register a test device, run:")
        print("  register_test_device('your-apns-push-token')")
        print("="*60)
        return results

    # Test 3-6: Notification types (dry run by default)
    results['new_order'] = test_new_order_notification(dry_run=dry_run)
    results['contact_form'] = test_customer_message_contact_form(dry_run=dry_run)
    results['order_note'] = test_customer_message_order_note(dry_run=dry_run)
    results['low_stock'] = test_low_stock_notification(dry_run=dry_run)

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {test}: {status}")

    all_passed = all(results.values())
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

    return results


def send_live_test():
    """Send actual push notifications (not dry run)."""
    print("\n" + "!"*60)
    print("WARNING: This will send REAL push notifications!")
    print("!"*60)

    confirm = input("\nType 'yes' to continue: ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return

    run_all_tests(dry_run=False)


if __name__ == '__main__':
    run_all_tests(dry_run=True)
