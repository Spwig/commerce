"""
Test script to fetch real WooCommerce data and analyze fields
This helps ensure our models have all necessary fields
"""
import json
import sys
import os
from pathlib import Path

# Add project root to path — this file lives at migration/, so up one
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

import django
django.setup()

from migration.fetchers.woocommerce_api import WooCommerceAPIClient
from migration.models import MigrationJob

# Get the migration job
job = MigrationJob.objects.first()

if not job or not job.connection_config:
    print("❌ No migration job with WooCommerce credentials found")
    sys.exit(1)

# Initialize client
client = WooCommerceAPIClient(
    store_url=job.connection_config['store_url'],
    consumer_key=job.connection_config['consumer_key'],
    consumer_secret=job.connection_config['consumer_secret']
)

print("=" * 80)
print("WOOCOMMERCE DATA STRUCTURE ANALYSIS")
print("=" * 80)

# Fetch and analyze customers
print("\n📋 CUSTOMERS (1 sample)")
print("-" * 80)
try:
    customers = client.fetch_customers(page=1, per_page=1)
    if customers:
        customer = customers[0]
        print(json.dumps(customer, indent=2))
        print(f"\n✅ Customer fields: {len(customer.keys())}")
        print(f"Keys: {list(customer.keys())}")
    else:
        print("⚠️  No customers found")
except Exception as e:
    print(f"❌ Error fetching customers: {e}")

# Fetch and analyze orders
print("\n\n📋 ORDERS (1 sample)")
print("-" * 80)
try:
    orders = client.fetch_orders(page=1, per_page=1)
    if orders:
        order = orders[0]
        print(json.dumps(order, indent=2))
        print(f"\n✅ Order fields: {len(order.keys())}")
        print(f"Keys: {list(order.keys())}")

        if order.get('line_items'):
            print(f"\n📦 Line item fields: {list(order['line_items'][0].keys())}")
    else:
        print("⚠️  No orders found")
except Exception as e:
    print(f"❌ Error fetching orders: {e}")

# Fetch and analyze reviews
print("\n\n📋 REVIEWS (1 sample)")
print("-" * 80)
try:
    reviews = client.fetch_reviews(page=1, per_page=1)
    if reviews:
        review = reviews[0]
        print(json.dumps(review, indent=2))
        print(f"\n✅ Review fields: {len(review.keys())}")
        print(f"Keys: {list(review.keys())}")
    else:
        print("⚠️  No reviews found")
except Exception as e:
    print(f"❌ Error fetching reviews: {e}")

# Fetch and analyze coupons
print("\n\n📋 COUPONS (1 sample)")
print("-" * 80)
try:
    coupons = client.fetch_coupons(page=1, per_page=1)
    if coupons:
        coupon = coupons[0]
        print(json.dumps(coupon, indent=2))
        print(f"\n✅ Coupon fields: {len(coupon.keys())}")
        print(f"Keys: {list(coupon.keys())}")
    else:
        print("⚠️  No coupons found")
except Exception as e:
    print(f"❌ Error fetching coupons: {e}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
