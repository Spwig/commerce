"""
Manual test script for WooCommerce API connection

Usage:
    python manage.py shell < migration/tests/manual_test_woocommerce.py

Or in Django shell:
    from migration.tests.manual_test_woocommerce import test_woocommerce_connection
    test_woocommerce_connection('https://yourstore.com', 'ck_xxx', 'cs_xxx')
"""
import requests
from pprint import pprint


def test_woocommerce_connection(store_url, consumer_key, consumer_secret):
    """
    Test WooCommerce API connection with real credentials

    Args:
        store_url: Your WooCommerce store URL (e.g., https://yourstore.com)
        consumer_key: WooCommerce REST API consumer key (ck_xxx)
        consumer_secret: WooCommerce REST API consumer secret (cs_xxx)

    Example:
        test_woocommerce_connection(
            'https://demo.woothemes.com',
            'ck_your_key_here',
            'cs_your_secret_here'
        )
    """
    print("=" * 80)
    print("WooCommerce API Connection Test")
    print("=" * 80)

    base_url = store_url.rstrip('/')
    auth = (consumer_key, consumer_secret)

    # Test 1: System Status
    print("\n[1] Testing System Status Endpoint...")
    try:
        response = requests.get(
            f"{base_url}/wp-json/wc/v3/system_status",
            auth=auth,
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✓ Connection successful!")
            print(f"  WordPress Version: {data.get('environment', {}).get('wp_version', 'N/A')}")
            print(f"  WooCommerce Version: {data.get('environment', {}).get('version', 'N/A')}")
            print(f"  Database: {data.get('database', {}).get('version', 'N/A')}")
        elif response.status_code == 401:
            print("✗ Authentication failed! Check your API credentials.")
            return False
        elif response.status_code == 404:
            print("✗ WooCommerce API not found. Is WooCommerce installed?")
            return False
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("✗ Connection timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to store. Check the URL.")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    # Test 2: Products Endpoint
    print("\n[2] Testing Products Endpoint...")
    try:
        response = requests.get(
            f"{base_url}/wp-json/wc/v3/products",
            auth=auth,
            params={'per_page': 5},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            total_products = response.headers.get('X-WP-Total', 'N/A')
            print(f"✓ Products accessible! Total: {total_products}")
            if products:
                print(f"  Sample product: {products[0]['name']}")
        else:
            print(f"✗ Cannot access products (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 3: Categories Endpoint
    print("\n[3] Testing Categories Endpoint...")
    try:
        response = requests.get(
            f"{base_url}/wp-json/wc/v3/products/categories",
            auth=auth,
            params={'per_page': 5},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()
            total_categories = response.headers.get('X-WP-Total', 'N/A')
            print(f"✓ Categories accessible! Total: {total_categories}")
            if categories:
                print(f"  Sample category: {categories[0]['name']}")
        else:
            print(f"✗ Cannot access categories (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 4: Customers Endpoint
    print("\n[4] Testing Customers Endpoint...")
    try:
        response = requests.get(
            f"{base_url}/wp-json/wc/v3/customers",
            auth=auth,
            params={'per_page': 5},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            customers = response.json()
            total_customers = response.headers.get('X-WP-Total', 'N/A')
            print(f"✓ Customers accessible! Total: {total_customers}")
            if customers:
                print(f"  Sample customer: {customers[0].get('email', 'N/A')}")
        else:
            print(f"✗ Cannot access customers (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 5: Orders Endpoint
    print("\n[5] Testing Orders Endpoint...")
    try:
        response = requests.get(
            f"{base_url}/wp-json/wc/v3/orders",
            auth=auth,
            params={'per_page': 5},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            orders = response.json()
            total_orders = response.headers.get('X-WP-Total', 'N/A')
            print(f"✓ Orders accessible! Total: {total_orders}")
            if orders:
                print(f"  Sample order: #{orders[0].get('number', 'N/A')}")
        else:
            print(f"✗ Cannot access orders (status: {response.status_code})")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 6: Sample Product Details
    print("\n[6] Fetching Sample Product Details...")
    try:
        response = requests.get(
            f"{base_url}/wp-json/wc/v3/products",
            auth=auth,
            params={'per_page': 1},
            timeout=10
        )
        if response.status_code == 200 and response.json():
            product = response.json()[0]
            print("✓ Sample product structure:")
            print(f"  ID: {product.get('id')}")
            print(f"  Name: {product.get('name')}")
            print(f"  SKU: {product.get('sku', 'N/A')}")
            print(f"  Price: {product.get('price')}")
            print(f"  Regular Price: {product.get('regular_price')}")
            print(f"  Sale Price: {product.get('sale_price', 'N/A')}")
            print(f"  Stock: {product.get('stock_quantity', 'N/A')}")
            print(f"  Categories: {len(product.get('categories', []))}")
            print(f"  Images: {len(product.get('images', []))}")
            print(f"  Meta Data: {len(product.get('meta_data', []))}")

            if product.get('images'):
                print(f"  Sample Image URL: {product['images'][0].get('src', 'N/A')}")

            if product.get('meta_data'):
                print(f"  Sample Meta Keys: {[m['key'] for m in product['meta_data'][:3]]}")
    except Exception as e:
        print(f"✗ Error: {e}")

    print("\n" + "=" * 80)
    print("Test Complete!")
    print("=" * 80)
    return True


# Example usage for testing
if __name__ == "__main__":
    print("\n" + "="*80)
    print("WooCommerce API Test Script")
    print("="*80)
    print("\nTo test your WooCommerce connection, run:")
    print("\n  from migration.tests.manual_test_woocommerce import test_woocommerce_connection")
    print("  test_woocommerce_connection('https://yourstore.com', 'ck_xxx', 'cs_xxx')")
    print("\n" + "="*80 + "\n")

    # Uncomment and fill in your credentials to test:
    # test_woocommerce_connection(
    #     store_url='https://yourstore.com',
    #     consumer_key='ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    #     consumer_secret='cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    # )
