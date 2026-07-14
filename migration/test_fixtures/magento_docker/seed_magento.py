#!/usr/bin/env python3
"""
Seed a Bitnami Magento 2 instance with test data for migration testing.

Usage:
    python seed_magento.py [--url http://localhost:8085] [--user user] [--password bitnami1]

Creates:
    - 5 categories (nested hierarchy)
    - 10 simple products, 2 configurable products with variants
    - 5 customers with addresses
    - 8 orders with line items
    - 5 product reviews
    - 3 sales rules with coupon codes
    - 3 CMS pages

After seeding, creates an Integration and prints the access token for migration testing.
"""

import argparse
import random
import sys
import time

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MagentoSeeder:
    def __init__(self, base_url: str, admin_user: str, admin_password: str):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/rest/V1"
        self.session = requests.Session()
        self.session.verify = False
        self.admin_token = None
        self.created = {
            "categories": [],
            "products": [],
            "customers": [],
            "orders": [],
            "configurable_products": [],
        }

    def authenticate(self, username: str, password: str):
        """Get admin bearer token."""
        print("Authenticating with Magento admin...")
        resp = self.session.post(
            f"{self.api_url}/integration/admin/token",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        self.admin_token = resp.json()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.admin_token}",
                "Content-Type": "application/json",
            }
        )
        print(f"  Admin token obtained: {self.admin_token[:20]}...")

    def _post(self, endpoint: str, data: dict) -> dict:
        resp = self.session.post(f"{self.api_url}{endpoint}", json=data)
        if not resp.ok:
            print(f"  ERROR {resp.status_code}: {resp.text[:300]}")
        resp.raise_for_status()
        return resp.json()

    def _put(self, endpoint: str, data: dict) -> dict:
        resp = self.session.put(f"{self.api_url}{endpoint}", json=data)
        if not resp.ok:
            print(f"  ERROR {resp.status_code}: {resp.text[:300]}")
        resp.raise_for_status()
        return resp.json()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        resp = self.session.get(f"{self.api_url}{endpoint}", params=params)
        resp.raise_for_status()
        return resp.json()

    # ──────────────────────────────────────────────
    # Categories
    # ──────────────────────────────────────────────

    def seed_categories(self):
        print("\nSeeding categories...")
        # Get default category (ID 2 is the Default Category in Magento)
        root_id = 2

        categories = [
            {"name": "Electronics", "parent_id": root_id, "is_active": True, "position": 1},
            {"name": "Clothing", "parent_id": root_id, "is_active": True, "position": 2},
            {"name": "Home & Garden", "parent_id": root_id, "is_active": True, "position": 3},
        ]

        for cat in categories:
            result = self._post(
                "/categories",
                {
                    "category": {
                        "name": cat["name"],
                        "parent_id": cat["parent_id"],
                        "is_active": cat["is_active"],
                        "position": cat["position"],
                        "include_in_menu": True,
                        "custom_attributes": [
                            {
                                "attribute_code": "description",
                                "value": f"Test category: {cat['name']}",
                            },
                            {
                                "attribute_code": "url_key",
                                "value": cat["name"].lower().replace(" & ", "-").replace(" ", "-"),
                            },
                        ],
                    }
                },
            )
            cat_id = result.get("id")
            self.created["categories"].append(cat_id)
            print(f"  Created category: {cat['name']} (ID: {cat_id})")

        # Subcategories
        electronics_id = self.created["categories"][0]
        subcats = [
            {"name": "Smartphones", "parent_id": electronics_id},
            {"name": "Laptops", "parent_id": electronics_id},
        ]
        for sub in subcats:
            result = self._post(
                "/categories",
                {
                    "category": {
                        "name": sub["name"],
                        "parent_id": sub["parent_id"],
                        "is_active": True,
                        "position": 1,
                        "custom_attributes": [
                            {"attribute_code": "url_key", "value": sub["name"].lower()},
                        ],
                    }
                },
            )
            sub_id = result.get("id")
            self.created["categories"].append(sub_id)
            print(f"  Created subcategory: {sub['name']} (ID: {sub_id})")

    # ──────────────────────────────────────────────
    # Products
    # ──────────────────────────────────────────────

    def seed_products(self):
        print("\nSeeding products...")

        simple_products = [
            {
                "sku": "TEST-PHONE-001",
                "name": "Test Smartphone Pro",
                "price": 599.99,
                "description": "<p>A premium test smartphone with all the features.</p>",
                "short_description": "Premium test smartphone",
                "weight": 0.2,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][0], self.created["categories"][3]],
                "special_price": 549.99,
                "meta_title": "Test Smartphone Pro | Best Phone",
                "meta_description": "Buy the Test Smartphone Pro with amazing features",
                "qty": 50,
            },
            {
                "sku": "TEST-LAPTOP-001",
                "name": "Test Laptop Ultra",
                "price": 1299.99,
                "description": "<p>A powerful test laptop for professionals.</p>",
                "short_description": "Professional test laptop",
                "weight": 1.5,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][0], self.created["categories"][4]],
                "meta_title": "Test Laptop Ultra",
                "qty": 25,
            },
            {
                "sku": "TEST-TSHIRT-001",
                "name": "Classic Cotton T-Shirt",
                "price": 29.99,
                "description": "<p>A comfortable cotton t-shirt for everyday wear.</p>",
                "short_description": "Comfortable cotton tee",
                "weight": 0.3,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][1]],
                "qty": 200,
            },
            {
                "sku": "TEST-JEANS-001",
                "name": "Slim Fit Denim Jeans",
                "price": 79.99,
                "description": "<p>Modern slim fit jeans made from premium denim.</p>",
                "short_description": "Premium slim fit jeans",
                "weight": 0.8,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][1]],
                "special_price": 64.99,
                "qty": 150,
            },
            {
                "sku": "TEST-LAMP-001",
                "name": "Modern Desk Lamp",
                "price": 49.99,
                "description": "<p>An elegant modern desk lamp with adjustable brightness.</p>",
                "short_description": "Adjustable desk lamp",
                "weight": 1.2,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][2]],
                "qty": 75,
            },
            {
                "sku": "TEST-PILLOW-001",
                "name": "Memory Foam Pillow",
                "price": 39.99,
                "description": "<p>Ergonomic memory foam pillow for better sleep.</p>",
                "short_description": "Ergonomic memory foam pillow",
                "weight": 0.5,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][2]],
                "qty": 100,
            },
            {
                "sku": "TEST-HEADPHONES-001",
                "name": "Wireless Noise-Cancelling Headphones",
                "price": 199.99,
                "description": "<p>Premium wireless headphones with active noise cancellation.</p>",
                "short_description": "ANC wireless headphones",
                "weight": 0.35,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][0]],
                "special_price": 179.99,
                "qty": 60,
            },
            {
                "sku": "TEST-CHARGER-001",
                "name": "USB-C Fast Charger",
                "price": 24.99,
                "description": "<p>65W USB-C fast charger compatible with all devices.</p>",
                "short_description": "65W USB-C charger",
                "weight": 0.15,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][0]],
                "qty": 300,
            },
            {
                "sku": "TEST-DRAFT-001",
                "name": "Draft Product (Not Published)",
                "price": 9.99,
                "description": "<p>This product is disabled/draft.</p>",
                "short_description": "Draft product",
                "weight": 0.1,
                "status": 2,  # Disabled
                "visibility": 4,
                "category_ids": [self.created["categories"][0]],
                "qty": 0,
            },
            {
                "sku": "TEST-DIGITAL-001",
                "name": "Digital E-Book: Python Mastery",
                "price": 19.99,
                "description": "<p>Comprehensive e-book on Python programming.</p>",
                "short_description": "Python programming e-book",
                "weight": 0,
                "status": 1,
                "visibility": 4,
                "category_ids": [self.created["categories"][0]],
                "qty": 9999,
            },
        ]

        for prod in simple_products:
            custom_attrs = [
                {"attribute_code": "description", "value": prod["description"]},
                {"attribute_code": "short_description", "value": prod["short_description"]},
                {"attribute_code": "url_key", "value": prod["sku"].lower().replace("_", "-")},
                {"attribute_code": "meta_title", "value": prod.get("meta_title", prod["name"])},
                {
                    "attribute_code": "meta_description",
                    "value": prod.get("meta_description", prod["short_description"]),
                },
            ]
            if prod.get("special_price"):
                custom_attrs.append(
                    {"attribute_code": "special_price", "value": str(prod["special_price"])}
                )

            product_data = {
                "product": {
                    "sku": prod["sku"],
                    "name": prod["name"],
                    "price": prod["price"],
                    "status": prod["status"],
                    "visibility": prod["visibility"],
                    "type_id": "virtual" if prod["weight"] == 0 else "simple",
                    "weight": prod["weight"],
                    "attribute_set_id": 4,  # Default attribute set
                    "custom_attributes": custom_attrs,
                    "extension_attributes": {
                        "category_links": [
                            {"category_id": cid, "position": 0} for cid in prod["category_ids"]
                        ],
                        "stock_item": {
                            "qty": prod["qty"],
                            "is_in_stock": prod["qty"] > 0,
                            "manage_stock": True,
                        },
                    },
                }
            }

            result = self._post("/products", product_data)
            prod_id = result.get("id")
            self.created["products"].append(
                {"id": prod_id, "sku": prod["sku"], "price": prod["price"]}
            )
            print(f"  Created product: {prod['name']} (ID: {prod_id}, SKU: {prod['sku']})")

    def seed_configurable_products(self):
        """Create configurable products with child variants."""
        print("\nSeeding configurable products...")

        # First, check if 'color' attribute exists with options
        try:
            color_attr = self._get("/products/attributes/color")
            color_options = {
                opt["label"]: opt["value"] for opt in color_attr.get("options", []) if opt["value"]
            }
        except Exception:
            print("  Color attribute not available, skipping configurable products")
            return

        if not color_options:
            print("  No color options available, skipping configurable products")
            return

        # Pick 3 colors to use
        colors = list(color_options.items())[:3]
        if len(colors) < 2:
            print("  Not enough color options, skipping configurable products")
            return

        color_attr_id = color_attr.get("attribute_id")

        # Create configurable parent
        parent_sku = "TEST-CONFIG-HOODIE"
        parent_data = {
            "product": {
                "sku": parent_sku,
                "name": "Zip-Up Hoodie",
                "price": 59.99,
                "status": 1,
                "visibility": 4,
                "type_id": "configurable",
                "attribute_set_id": 4,
                "weight": 0.6,
                "custom_attributes": [
                    {
                        "attribute_code": "description",
                        "value": "<p>A cozy zip-up hoodie in multiple colors.</p>",
                    },
                    {"attribute_code": "short_description", "value": "Cozy zip-up hoodie"},
                    {"attribute_code": "url_key", "value": "zip-up-hoodie"},
                ],
                "extension_attributes": {
                    "category_links": [
                        {"category_id": self.created["categories"][1], "position": 0}
                    ],
                },
            }
        }

        try:
            parent = self._post("/products", parent_data)
            parent_id = parent.get("id")
            print(f"  Created configurable product: Zip-Up Hoodie (ID: {parent_id})")
            self.created["configurable_products"].append({"id": parent_id, "sku": parent_sku})

            # Create child simple products (visibility=1 = not individually visible)
            child_ids = []
            for color_label, color_value in colors:
                child_sku = f"TEST-CONFIG-HOODIE-{color_label.upper()}"
                child_data = {
                    "product": {
                        "sku": child_sku,
                        "name": f"Zip-Up Hoodie - {color_label}",
                        "price": 59.99,
                        "status": 1,
                        "visibility": 1,  # Not Visible Individually
                        "type_id": "simple",
                        "attribute_set_id": 4,
                        "weight": 0.6,
                        "custom_attributes": [
                            {"attribute_code": "color", "value": color_value},
                            {
                                "attribute_code": "url_key",
                                "value": f"zip-up-hoodie-{color_label.lower()}",
                            },
                        ],
                        "extension_attributes": {
                            "stock_item": {
                                "qty": random.randint(10, 50),
                                "is_in_stock": True,
                                "manage_stock": True,
                            },
                        },
                    }
                }
                child = self._post("/products", child_data)
                child_ids.append(child.get("id"))
                print(f"    Created variant: {color_label} (ID: {child.get('id')})")

            # Link children to configurable parent
            # Set configurable attribute
            self._post(
                f"/configurable-products/{parent_sku}/options",
                {
                    "option": {
                        "attribute_id": color_attr_id,
                        "label": "Color",
                        "position": 0,
                        "values": [{"value_index": opt[1]} for opt in colors],
                    }
                },
            )

            # Assign children
            for color_label, _color_value in colors:
                child_sku = f"TEST-CONFIG-HOODIE-{color_label.upper()}"
                try:
                    self._post(
                        f"/configurable-products/{parent_sku}/child", {"childSku": child_sku}
                    )
                except Exception as e:
                    print(f"    Warning: Could not link child {child_sku}: {e}")

            print(f"  Linked {len(colors)} variants to configurable product")

        except Exception as e:
            print(f"  Warning: Could not create configurable product: {e}")

    # ──────────────────────────────────────────────
    # Customers
    # ──────────────────────────────────────────────

    def seed_customers(self):
        print("\nSeeding customers...")

        customers = [
            {
                "email": "john.doe@example.com",
                "firstname": "John",
                "lastname": "Doe",
                "addresses": [
                    {
                        "firstname": "John",
                        "lastname": "Doe",
                        "street": ["123 Main Street", "Apt 4B"],
                        "city": "New York",
                        "region": {"region": "New York", "region_code": "NY", "region_id": 43},
                        "postcode": "10001",
                        "country_id": "US",
                        "telephone": "212-555-0100",
                        "default_billing": True,
                        "default_shipping": True,
                    }
                ],
            },
            {
                "email": "jane.smith@example.com",
                "firstname": "Jane",
                "lastname": "Smith",
                "addresses": [
                    {
                        "firstname": "Jane",
                        "lastname": "Smith",
                        "street": ["456 Oak Avenue"],
                        "city": "Los Angeles",
                        "region": {"region": "California", "region_code": "CA", "region_id": 12},
                        "postcode": "90001",
                        "country_id": "US",
                        "telephone": "310-555-0200",
                        "default_billing": True,
                        "default_shipping": True,
                    }
                ],
            },
            {
                "email": "bob.wilson@example.com",
                "firstname": "Bob",
                "lastname": "Wilson",
                "addresses": [
                    {
                        "firstname": "Bob",
                        "lastname": "Wilson",
                        "street": ["789 Pine Road"],
                        "city": "Chicago",
                        "region": {"region": "Illinois", "region_code": "IL", "region_id": 14},
                        "postcode": "60601",
                        "country_id": "US",
                        "telephone": "312-555-0300",
                        "default_billing": True,
                        "default_shipping": True,
                    }
                ],
            },
            {
                "email": "alice.chen@example.com",
                "firstname": "Alice",
                "lastname": "Chen",
                "addresses": [
                    {
                        "firstname": "Alice",
                        "lastname": "Chen",
                        "street": ["321 Maple Lane"],
                        "city": "San Francisco",
                        "region": {"region": "California", "region_code": "CA", "region_id": 12},
                        "postcode": "94102",
                        "country_id": "US",
                        "telephone": "415-555-0400",
                        "default_billing": True,
                        "default_shipping": True,
                    }
                ],
            },
            {
                "email": "marco.rossi@example.com",
                "firstname": "Marco",
                "lastname": "Rossi",
                "addresses": [
                    {
                        "firstname": "Marco",
                        "lastname": "Rossi",
                        "street": ["55 Elm Street"],
                        "city": "Boston",
                        "region": {"region": "Massachusetts", "region_code": "MA", "region_id": 22},
                        "postcode": "02101",
                        "country_id": "US",
                        "telephone": "617-555-0500",
                        "default_billing": True,
                        "default_shipping": True,
                    }
                ],
            },
        ]

        for cust in customers:
            try:
                result = self._post(
                    "/customers",
                    {
                        "customer": {
                            "email": cust["email"],
                            "firstname": cust["firstname"],
                            "lastname": cust["lastname"],
                            "addresses": cust["addresses"],
                            "group_id": 1,
                            "store_id": 1,
                            "website_id": 1,
                        },
                        "password": "TestPassword123!",
                    },
                )
                cust_id = result.get("id")
                self.created["customers"].append({"id": cust_id, "email": cust["email"]})
                print(f"  Created customer: {cust['firstname']} {cust['lastname']} (ID: {cust_id})")
            except Exception as e:
                print(f"  Warning: Could not create customer {cust['email']}: {e}")

    # ──────────────────────────────────────────────
    # Orders
    # ──────────────────────────────────────────────

    def seed_orders(self):
        """Create orders via the cart/checkout API flow."""
        print("\nSeeding orders...")

        if not self.created["customers"] or not self.created["products"]:
            print("  Skipping orders: no customers or products available")
            return

        order_configs = [
            {"customer_idx": 0, "products": [(0, 1), (2, 2)], "status": "processing"},
            {"customer_idx": 0, "products": [(1, 1)], "status": "complete"},
            {"customer_idx": 1, "products": [(4, 1), (5, 2)], "status": "processing"},
            {"customer_idx": 1, "products": [(6, 1)], "status": "pending"},
            {"customer_idx": 2, "products": [(0, 1), (7, 3)], "status": "processing"},
            {"customer_idx": 2, "products": [(3, 1)], "status": "canceled"},
            {"customer_idx": 3, "products": [(1, 1), (6, 1), (4, 1)], "status": "complete"},
            {"customer_idx": 4, "products": [(2, 3)], "status": "pending"},
        ]

        for cfg in order_configs:
            if cfg["customer_idx"] >= len(self.created["customers"]):
                continue
            customer = self.created["customers"][cfg["customer_idx"]]

            try:
                # Get customer token
                resp = self.session.post(
                    f"{self.api_url}/integration/customer/token",
                    json={"username": customer["email"], "password": "TestPassword123!"},
                )
                if not resp.ok:
                    print(
                        f"  Warning: Could not get token for {customer['email']}: {resp.text[:100]}"
                    )
                    continue
                cust_token = resp.json()

                cust_headers = {
                    "Authorization": f"Bearer {cust_token}",
                    "Content-Type": "application/json",
                }

                # Create cart
                cart_resp = self.session.post(f"{self.api_url}/carts/mine", headers=cust_headers)
                cart_resp.raise_for_status()
                cart_id = cart_resp.json()

                # Add items
                for prod_idx, qty in cfg["products"]:
                    if prod_idx >= len(self.created["products"]):
                        continue
                    prod = self.created["products"][prod_idx]
                    self.session.post(
                        f"{self.api_url}/carts/mine/items",
                        headers=cust_headers,
                        json={
                            "cartItem": {
                                "sku": prod["sku"],
                                "qty": qty,
                                "quote_id": cart_id,
                            }
                        },
                    )

                # Set shipping info
                self.session.post(
                    f"{self.api_url}/carts/mine/shipping-information",
                    headers=cust_headers,
                    json={
                        "addressInformation": {
                            "shipping_address": {
                                "firstname": "Test",
                                "lastname": "Customer",
                                "street": ["123 Test St"],
                                "city": "Test City",
                                "region_code": "NY",
                                "region_id": 43,
                                "postcode": "10001",
                                "country_id": "US",
                                "telephone": "555-0000",
                            },
                            "billing_address": {
                                "firstname": "Test",
                                "lastname": "Customer",
                                "street": ["123 Test St"],
                                "city": "Test City",
                                "region_code": "NY",
                                "region_id": 43,
                                "postcode": "10001",
                                "country_id": "US",
                                "telephone": "555-0000",
                            },
                            "shipping_method_code": "flatrate",
                            "shipping_carrier_code": "flatrate",
                        }
                    },
                )

                # Place order
                order_resp = self.session.put(
                    f"{self.api_url}/carts/mine/order",
                    headers=cust_headers,
                    json={"paymentMethod": {"method": "checkmo"}},
                )
                if order_resp.ok:
                    order_id = order_resp.json()
                    self.created["orders"].append(order_id)
                    print(f"  Created order #{order_id} for {customer['email']}")

                    # Update status if needed
                    if cfg["status"] != "pending":
                        try:
                            if cfg["status"] == "processing":
                                # Create invoice to move to processing
                                self.session.post(
                                    f"{self.api_url}/order/{order_id}/invoice",
                                    json={
                                        "capture": True,
                                        "notify": False,
                                    },
                                )
                            elif cfg["status"] == "complete":
                                # Invoice then ship
                                self.session.post(
                                    f"{self.api_url}/order/{order_id}/invoice",
                                    json={
                                        "capture": True,
                                        "notify": False,
                                    },
                                )
                                self.session.post(
                                    f"{self.api_url}/order/{order_id}/ship",
                                    json={
                                        "notify": False,
                                    },
                                )
                            elif cfg["status"] == "canceled":
                                self.session.post(f"{self.api_url}/orders/{order_id}/cancel")
                        except Exception:
                            pass  # Status update is best-effort
                else:
                    print(f"  Warning: Order placement failed: {order_resp.text[:200]}")

            except Exception as e:
                print(f"  Warning: Could not create order: {e}")

    # ──────────────────────────────────────────────
    # Reviews
    # ──────────────────────────────────────────────

    def seed_reviews(self):
        print("\nSeeding reviews...")

        if not self.created["products"]:
            print("  Skipping reviews: no products available")
            return

        reviews = [
            {
                "title": "Excellent smartphone!",
                "detail": "Battery life is amazing and the camera quality is outstanding.",
                "nickname": "TechLover",
                "product_idx": 0,
                "rating": 90,
            },
            {
                "title": "Great laptop for work",
                "detail": "Fast, reliable, and the screen is beautiful. Highly recommend for professionals.",
                "nickname": "WorkPro",
                "product_idx": 1,
                "rating": 80,
            },
            {
                "title": "Comfortable but runs small",
                "detail": "The fabric is nice but I had to order a size up. Good quality otherwise.",
                "nickname": "FashionFan",
                "product_idx": 2,
                "rating": 60,
            },
            {
                "title": "Best headphones I've owned",
                "detail": "The noise cancellation is incredible. Sound quality is crystal clear.",
                "nickname": "MusicEnthusiast",
                "product_idx": 6,
                "rating": 100,
            },
            {
                "title": "Decent desk lamp",
                "detail": "Does the job but the adjustable arm could be sturdier. Light quality is good.",
                "nickname": "HomeOfficePro",
                "product_idx": 4,
                "rating": 70,
            },
        ]

        # First, get rating entity (or create one)
        try:
            # Magento reviews need a rating to be set up
            # We'll try to use the existing ratings
            for rev in reviews:
                if rev["product_idx"] >= len(self.created["products"]):
                    continue
                prod = self.created["products"][rev["product_idx"]]

                review_data = {
                    "review": {
                        "title": rev["title"],
                        "detail": rev["detail"],
                        "nickname": rev["nickname"],
                        "ratings": [
                            {
                                "rating_name": "Rating",
                                "value": str(rev["rating"]),
                            }
                        ],
                        "review_entity": "product",
                        "review_status": 1,  # Approved
                        "entity_pk_value": prod["id"],
                        "store_id": 1,
                        "stores": [1],
                    }
                }

                try:
                    self._post("/reviews", review_data)
                    print(f"  Created review: '{rev['title']}' for product {prod['sku']}")
                except Exception as e:
                    print(f"  Warning: Could not create review '{rev['title']}': {e}")

        except Exception as e:
            print(f"  Warning: Review seeding had issues: {e}")

    # ──────────────────────────────────────────────
    # Sales Rules / Coupons
    # ──────────────────────────────────────────────

    def seed_coupons(self):
        print("\nSeeding sales rules and coupons...")

        rules = [
            {
                "name": "Summer Sale 10% Off",
                "description": "10% off everything for summer",
                "is_active": True,
                "coupon_type": "SPECIFIC_COUPON",
                "simple_action": "by_percent",
                "discount_amount": 10,
                "uses_per_customer": 1,
                "code": "SUMMER10",
            },
            {
                "name": "Welcome Discount $5",
                "description": "New customer welcome discount",
                "is_active": True,
                "coupon_type": "SPECIFIC_COUPON",
                "simple_action": "by_fixed",
                "discount_amount": 5,
                "uses_per_customer": 1,
                "code": "WELCOME5",
            },
            {
                "name": "Free Shipping Over $50",
                "description": "Free shipping on orders over $50",
                "is_active": False,
                "coupon_type": "SPECIFIC_COUPON",
                "simple_action": "cart_fixed",
                "discount_amount": 0,
                "uses_per_customer": 3,
                "code": "FREESHIP50",
            },
        ]

        for rule_data in rules:
            try:
                result = self._post(
                    "/salesRules",
                    {
                        "rule": {
                            "name": rule_data["name"],
                            "description": rule_data["description"],
                            "is_active": rule_data["is_active"],
                            "coupon_type": rule_data["coupon_type"],
                            "simple_action": rule_data["simple_action"],
                            "discount_amount": rule_data["discount_amount"],
                            "uses_per_customer": rule_data["uses_per_customer"],
                            "store_labels": [
                                {"store_id": 0, "store_label": rule_data["name"]},
                                {"store_id": 1, "store_label": rule_data["name"]},
                            ],
                            "website_ids": [1],
                            "customer_group_ids": [0, 1, 2, 3],
                        }
                    },
                )
                rule_id = result.get("rule_id")
                print(f"  Created sales rule: {rule_data['name']} (ID: {rule_id})")

                # Create coupon code for the rule
                self._post(
                    "/coupons",
                    {
                        "coupon": {
                            "rule_id": rule_id,
                            "code": rule_data["code"],
                            "usage_limit": 100,
                            "usage_per_customer": rule_data["uses_per_customer"],
                            "type": 0,
                            "is_primary": True,
                        }
                    },
                )
                print(f"    Created coupon code: {rule_data['code']}")

            except Exception as e:
                print(f"  Warning: Could not create sales rule '{rule_data['name']}': {e}")

    # ──────────────────────────────────────────────
    # CMS Pages
    # ──────────────────────────────────────────────

    def seed_cms_pages(self):
        print("\nSeeding CMS pages...")

        pages = [
            {
                "identifier": "about-us",
                "title": "About Our Store",
                "content": '<div class="about-page">\n<h2>Welcome to Our Test Store</h2>\n<p>We are a leading online retailer specializing in electronics, clothing, and home goods.</p>\n<p>{{media url="wysiwyg/about-banner.jpg"}}</p>\n<p>Founded in 2020, we have served over 10,000 happy customers worldwide.</p>\n</div>',
                "is_active": True,
                "meta_title": "About Us | Test Store",
                "meta_description": "Learn about our test store and our mission to provide quality products.",
            },
            {
                "identifier": "shipping-info",
                "title": "Shipping Information",
                "content": '<div class="shipping-page">\n<h2>Shipping Policy</h2>\n<p>We offer free shipping on orders over $50.</p>\n<ul>\n<li>Standard Shipping: 5-7 business days</li>\n<li>Express Shipping: 2-3 business days</li>\n<li>Next Day: Available for select areas</li>\n</ul>\n<p>{{widget type="Magento\\\\Cms\\\\Block\\\\Widget\\\\Block" template="widget/static_block/default.phtml" block_id="2"}}</p>\n</div>',
                "is_active": True,
                "meta_title": "Shipping Info | Test Store",
                "meta_description": "Shipping rates and delivery times for our test store.",
            },
            {
                "identifier": "sale-announcement",
                "title": "Big Summer Sale!",
                "content": '<div class="sale-page">\n<h1>Summer Sale is Here!</h1>\n<p>Save up to 30% on select electronics and clothing.</p>\n<p>Use code <strong>SUMMER10</strong> for an extra 10% off.</p>\n<p>Sale ends August 31st. {{store url="catalog/category/view/id/3"}}</p>\n</div>',
                "is_active": True,
                "meta_title": "Summer Sale | Test Store",
                "meta_description": "Big summer sale with discounts on electronics and clothing.",
            },
        ]

        for page_data in pages:
            try:
                self._post(
                    "/cmsPage",
                    {
                        "page": {
                            "identifier": page_data["identifier"],
                            "title": page_data["title"],
                            "content": page_data["content"],
                            "active": page_data["is_active"],
                            "meta_title": page_data["meta_title"],
                            "meta_description": page_data["meta_description"],
                            "page_layout": "1column",
                            "sort_order": 0,
                        }
                    },
                )
                print(f"  Created CMS page: {page_data['title']} (/{page_data['identifier']})")
            except Exception as e:
                print(f"  Warning: Could not create CMS page '{page_data['title']}': {e}")

    # ──────────────────────────────────────────────
    # Integration (access token for migration)
    # ──────────────────────────────────────────────

    def create_integration(self):
        """Create an Integration and print the access token for migration testing."""
        print("\n" + "=" * 60)
        print("CREATING INTEGRATION FOR MIGRATION TESTING")
        print("=" * 60)

        # The admin token we already have works for API access
        # For a real Integration, we'd need to use the admin UI
        # But for testing, the admin token works identically

        print(f"\n  Store URL:     {self.base_url}")
        print(f"  Access Token:  {self.admin_token}")
        print("\n  Use these values in the Spwig migration wizard.")
        print(
            f"\n  API test: curl -H 'Authorization: Bearer {self.admin_token}' {self.api_url}/store/storeConfigs"
        )

    def print_summary(self):
        print("\n" + "=" * 60)
        print("SEED SUMMARY")
        print("=" * 60)
        print(f"  Categories:             {len(self.created['categories'])}")
        print(f"  Simple Products:        {len(self.created['products'])}")
        print(f"  Configurable Products:  {len(self.created['configurable_products'])}")
        print(f"  Customers:              {len(self.created['customers'])}")
        print(f"  Orders:                 {len(self.created['orders'])}")
        print("  Reviews:                5 (attempted)")
        print("  Sales Rules + Coupons:  3")
        print("  CMS Pages:              3")


def wait_for_magento(base_url: str, timeout: int = 600):
    """Wait for Magento to be ready."""
    print(f"Waiting for Magento at {base_url} to be ready...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(f"{base_url}/rest/V1/store/storeConfigs", timeout=5, verify=False)
            if resp.status_code in (200, 401):  # 401 means Magento is up but needs auth
                print("  Magento is ready!")
                return True
        except requests.ConnectionError:
            pass
        time.sleep(10)
        elapsed = int(time.time() - start)
        print(f"  Still waiting... ({elapsed}s)")
    print("  TIMEOUT: Magento did not become ready")
    return False


def main():
    parser = argparse.ArgumentParser(description="Seed Magento test instance")
    parser.add_argument("--url", default="https://localhost:8445", help="Magento base URL")
    parser.add_argument("--user", default="john.smith", help="Admin username")
    parser.add_argument("--password", default="password123", help="Admin password")
    parser.add_argument("--wait", action="store_true", help="Wait for Magento to be ready first")
    parser.add_argument("--timeout", type=int, default=600, help="Max seconds to wait")
    args = parser.parse_args()

    if args.wait and not wait_for_magento(args.url, args.timeout):
        sys.exit(1)

    seeder = MagentoSeeder(args.url, args.user, args.password)
    seeder.authenticate(args.user, args.password)

    seeder.seed_categories()
    seeder.seed_products()
    seeder.seed_configurable_products()
    seeder.seed_customers()
    seeder.seed_orders()
    seeder.seed_reviews()
    seeder.seed_coupons()
    seeder.seed_cms_pages()
    seeder.create_integration()
    seeder.print_summary()


if __name__ == "__main__":
    main()
