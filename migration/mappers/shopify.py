"""
Shopify Data Mappers
Transform Shopify Admin API data to internal platform format
"""

import logging
from decimal import Decimal

from .base import BaseMapper

logger = logging.getLogger(__name__)


class ShopifyCollectionMapper(BaseMapper):
    """Map Shopify collections (custom + smart) to internal Category model"""

    def map(self, source_data: dict) -> dict:
        """
        Map Shopify collection to internal format

        Shopify custom collection:
        {
            "id": 841564295,
            "handle": "ipods",
            "title": "IPods",
            "body_html": "<p>The best selling ipod ever</p>",
            "sort_order": "best-selling",
            "published_at": "2008-02-01T19:00:00-05:00",
            "image": {"src": "https://...jpg", "alt": "Alt text"}
        }

        Shopify smart collection:
        {
            "id": 482865238,
            "handle": "smart-ipods",
            "title": "Smart IPods",
            "body_html": null,
            "rules": [{"column": "type", "relation": "equals", "condition": "Cult Products"}],
            "disjunctive": false
        }
        """
        try:
            image = source_data.get("image") or {}

            mapped = {
                # Basic fields
                "name": source_data.get("title", ""),
                "slug": self.generate_slug(
                    source_data.get("handle", "") or source_data.get("title", "")
                ),
                "description": self.parse_html(source_data.get("body_html", "") or ""),
                # Shopify collections are flat (no parent hierarchy)
                "parent_id": 0,
                # Display
                "sort_order": 0,
                "is_active": source_data.get("published_at") is not None,
                "is_featured": False,
                # SEO
                "meta_title": "",
                "meta_description": (
                    (source_data.get("body_html", "") or "")[:255]
                    if source_data.get("body_html")
                    else ""
                ),
                # Image
                "image_url": image.get("src") if image else None,
                "image_alt": image.get("alt", "") if image else "",
                # Display settings
                "page_template": self._map_sort_order(source_data.get("sort_order", "")),
                "products_per_page": 24,
                "show_subcategories": False,  # Shopify collections are flat
                # Source tracking
                "source_id": str(source_data.get("id")),
                "source_platform": "shopify",
                # Smart collection rules (stored in meta for reference)
                "collection_type": "smart" if "rules" in source_data else "custom",
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map collection: {e}", source_data)
            raise

    def _map_sort_order(self, shopify_sort: str) -> str:
        """Map Shopify sort order to page template"""
        # All collections display as grid
        return "grid"


class ShopifyProductMapper(BaseMapper):
    """Map Shopify products to internal Product model"""

    def map(self, source_data: dict) -> dict:
        """
        Map Shopify product to internal format

        Shopify product structure:
        {
            "id": 632910392,
            "title": "IPod Nano - 8GB",
            "handle": "ipod-nano",
            "body_html": "<p>It's the small iPod...</p>",
            "product_type": "Cult Products",
            "status": "active",
            "tags": "Emotive, Flash Memory, MP3, Music",
            "variants": [{
                "id": 808950810,
                "product_id": 632910392,
                "title": "Pink",
                "price": "199.00",
                "sku": "IPOD2008PINK",
                "option1": "Pink",
                "option2": null,
                "option3": null,
                "inventory_quantity": 10,
                "inventory_management": "shopify",
                "weight": 0.2,
                "weight_unit": "kg"
            }],
            "options": [{"name": "Color", "values": ["Pink", "Red", "Green"]}],
            "images": [{"src": "https://...jpg", "alt": "Alt", "position": 1}]
        }
        """
        try:
            variants = source_data.get("variants", [])
            first_variant = variants[0] if variants else {}

            mapped = {
                # Basic information
                "name": source_data.get("title", ""),
                "slug": self.generate_slug(
                    source_data.get("handle", "") or source_data.get("title", "")
                ),
                "sku": first_variant.get("sku", ""),
                # Product type
                "product_type": self._map_product_type(source_data, variants),
                # Descriptions
                "full_description": self.parse_html(source_data.get("body_html", "") or ""),
                "short_description": "",  # Shopify doesn't have separate short description
                # Pricing (from first variant)
                "price": self._parse_price(first_variant.get("price")),
                "regular_price": self._parse_price(
                    first_variant.get("compare_at_price") or first_variant.get("price")
                ),
                "sale_price": self._parse_price(first_variant.get("price"))
                if first_variant.get("compare_at_price")
                else None,
                # Categories (collections are linked separately via collects)
                "category_ids": [],
                "primary_category_id": None,
                # Inventory (from first variant)
                "track_inventory": first_variant.get("inventory_management") == "shopify",
                "stock_quantity": int(first_variant.get("inventory_quantity", 0) or 0),
                "allow_backorders": (first_variant.get("inventory_policy", "deny") == "continue"),
                "low_stock_threshold": 5,
                # Physical attributes (from first variant)
                "weight": self._parse_decimal(first_variant.get("weight")),
                "length": None,  # Shopify doesn't track dimensions in REST API
                "width": None,
                "height": None,
                # Status
                "status": self._map_status(source_data.get("status", "active")),
                "is_featured": False,  # Shopify doesn't have featured flag
                "is_digital": not first_variant.get("requires_shipping", True),
                # SEO
                "meta_title": source_data.get("title", ""),
                "meta_description": (
                    (source_data.get("body_html", "") or "")[:255]
                    if source_data.get("body_html")
                    else ""
                ),
                # Images
                "images": self._map_images(source_data.get("images", [])),
                # Attributes from options
                "attributes": self._map_attributes(source_data.get("options", [])),
                "specifications": {},
                # Variations
                "has_variations": len(variants) > 1,
                "variants": variants,  # Keep raw for executor to process
                # Tags (Shopify uses comma-separated string)
                "tags": self._parse_tags(source_data.get("tags", "")),
                # Reviews (not available via Shopify API)
                "reviews_allowed": True,
                "average_rating": 0,
                "rating_count": 0,
                # Source tracking
                "source_id": str(source_data.get("id")),
                "source_platform": "shopify",
                "source_data": {
                    "product_type": source_data.get("product_type", ""),
                    "vendor": source_data.get("vendor", ""),
                    "published_at": source_data.get("published_at"),
                    "created_at": source_data.get("created_at"),
                    "updated_at": source_data.get("updated_at"),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(
                f"Failed to map product: {e}",
                {"id": source_data.get("id"), "title": source_data.get("title")},
            )
            raise

    def _map_product_type(self, source_data: dict, variants: list[dict]) -> str:
        """Determine internal product type from Shopify data"""
        if len(variants) > 1:
            return "variable"

        first_variant = variants[0] if variants else {}
        if not first_variant.get("requires_shipping", True):
            return "digital"

        return "simple"

    def _map_status(self, shopify_status: str) -> str:
        """Map Shopify product status to internal status"""
        mapping = {
            "active": "published",
            "draft": "draft",
            "archived": "discontinued",
        }
        return mapping.get(shopify_status, "draft")

    def _parse_price(self, price) -> Decimal | None:
        """Parse price to Decimal"""
        if not price:
            return None
        try:
            return Decimal(str(price))
        except (ValueError, TypeError):
            self.log_warning(f"Failed to parse price: {price}")
            return None

    def _parse_decimal(self, value) -> Decimal | None:
        """Parse decimal value"""
        if not value:
            return None
        try:
            return Decimal(str(value))
        except (ValueError, TypeError):
            return None

    def _map_images(self, shopify_images: list[dict]) -> list[dict]:
        """Map Shopify images"""
        mapped_images = []
        for idx, img in enumerate(shopify_images):
            mapped_images.append(
                {
                    "src": img.get("src"),
                    "name": "",
                    "alt_text": img.get("alt") or "",
                    "position": img.get("position", idx + 1) - 1,  # Shopify is 1-based
                    "is_primary": idx == 0,
                }
            )
        return mapped_images

    def _map_attributes(self, shopify_options: list[dict]) -> dict:
        """Map Shopify product options to attributes"""
        attributes = {}
        for opt in shopify_options:
            name = opt.get("name", "")
            values = opt.get("values", [])
            if name and values and name != "Title":
                # Skip default "Title" option for single-variant products
                attributes[name] = ", ".join([str(v) for v in values])
        return attributes

    def _parse_tags(self, tags_string: str) -> list[str]:
        """Parse Shopify comma-separated tags string"""
        if not tags_string:
            return []
        return [tag.strip() for tag in tags_string.split(",") if tag.strip()]


class ShopifyCustomerMapper(BaseMapper):
    """Map Shopify customers to internal User/Customer model"""

    def map(self, source_data: dict) -> dict:
        """
        Map Shopify customer to internal format

        Shopify customer structure:
        {
            "id": 207119551,
            "email": "bob.norman@mail.example.com",
            "first_name": "Bob",
            "last_name": "Norman",
            "state": "disabled",
            "addresses": [{
                "id": 207119551,
                "first_name": "Bob",
                "last_name": "Norman",
                "address1": "Chestnut Street 92",
                "city": "Louisville",
                "province": "Kentucky",
                "country": "United States",
                "zip": "40202",
                "phone": "555-625-1199",
                "default": true
            }],
            "orders_count": 1,
            "total_spent": "199.65",
            "verified_email": true
        }
        """
        try:
            # Find default address
            addresses = source_data.get("addresses", [])
            default_address = {}
            for addr in addresses:
                if addr.get("default", False):
                    default_address = addr
                    break
            if not default_address and addresses:
                default_address = addresses[0]

            mapped = {
                # User fields
                "email": source_data.get("email", ""),
                "username": (
                    source_data.get("email", "").split("@")[0] if source_data.get("email") else ""
                ),
                "first_name": source_data.get("first_name") or "",
                "last_name": source_data.get("last_name") or "",
                # Customer profile
                "is_active": source_data.get("state", "disabled") != "disabled",
                # Addresses (Shopify doesn't split billing/shipping)
                "billing_address": self._map_address(default_address),
                "shipping_address": self._map_address(default_address),
                # Metadata
                "total_orders": source_data.get("orders_count", 0),
                "total_spent": self._parse_price(source_data.get("total_spent", 0)),
                # Source tracking
                "source_id": str(source_data.get("id")),
                "source_platform": "shopify",
                "source_data": {
                    "created_at": source_data.get("created_at"),
                    "updated_at": source_data.get("updated_at"),
                    "verified_email": source_data.get("verified_email", False),
                    "tags": source_data.get("tags", ""),
                    "note": source_data.get("note", ""),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(
                f"Failed to map customer: {e}",
                {"id": source_data.get("id"), "email": source_data.get("email")},
            )
            raise

    def _map_address(self, address_data: dict) -> dict:
        """Map Shopify address format to internal format"""
        if not address_data:
            return {}

        return {
            "first_name": address_data.get("first_name") or "",
            "last_name": address_data.get("last_name") or "",
            "company": address_data.get("company") or "",
            "address_1": address_data.get("address1") or "",
            "address_2": address_data.get("address2") or "",
            "city": address_data.get("city") or "",
            "state": address_data.get("province") or address_data.get("province_code") or "",
            "postcode": address_data.get("zip") or "",
            "country": address_data.get("country_code") or address_data.get("country") or "",
            "phone": address_data.get("phone") or "",
            "email": "",  # Shopify addresses don't include email
        }

    def _parse_price(self, price) -> Decimal | None:
        """Parse price to Decimal"""
        if not price:
            return None
        try:
            return Decimal(str(price))
        except (ValueError, TypeError):
            return None


class ShopifyOrderMapper(BaseMapper):
    """Map Shopify orders to internal Order model"""

    def map(self, source_data: dict) -> dict:
        """
        Map Shopify order to internal format

        Shopify order structure:
        {
            "id": 450789469,
            "name": "#1001",
            "order_number": 1001,
            "financial_status": "paid",
            "fulfillment_status": null,
            "total_price": "598.94",
            "subtotal_price": "597.00",
            "total_tax": "11.94",
            "total_discounts": "10.00",
            "currency": "USD",
            "line_items": [...],
            "billing_address": {...},
            "shipping_address": {...},
            "customer": {"id": 207119551},
            "shipping_lines": [...]
        }
        """
        try:
            customer = source_data.get("customer") or {}

            mapped = {
                # Order identification
                "order_number": str(source_data.get("order_number", source_data.get("id"))),
                # Customer
                "customer_id": customer.get("id", 0),
                "customer_email": source_data.get("email") or source_data.get("contact_email", ""),
                # Status (compound from financial + fulfillment)
                "status": self._map_order_status(
                    source_data.get("financial_status", ""),
                    source_data.get("fulfillment_status"),
                    source_data.get("cancelled_at"),
                ),
                "payment_status": self._map_payment_status(
                    source_data.get("financial_status", "pending")
                ),
                # Amounts
                "subtotal": self._parse_price(source_data.get("subtotal_price", 0)),
                "discount_total": self._parse_price(source_data.get("total_discounts", 0)),
                "shipping_total": self._parse_price(
                    sum(
                        Decimal(str(line.get("price", 0)))
                        for line in source_data.get("shipping_lines", [])
                    )
                ),
                "tax_total": self._parse_price(source_data.get("total_tax", 0)),
                "total": self._parse_price(source_data.get("total_price", 0)),
                # Currency
                "currency": source_data.get("currency", "USD"),
                # Payment
                "payment_method": (
                    source_data.get("payment_gateway_names", [""])[0]
                    if source_data.get("payment_gateway_names")
                    else ""
                ),
                "payment_method_id": "",
                # Addresses
                "billing_address": self._map_address(source_data.get("billing_address", {})),
                "shipping_address": self._map_address(source_data.get("shipping_address", {})),
                # Line items
                "line_items": self._map_line_items(source_data.get("line_items", [])),
                # Shipping
                "shipping_lines": self._map_shipping_lines(source_data.get("shipping_lines", [])),
                # Notes
                "customer_note": source_data.get("note", "") or "",
                # Dates
                "created_at": source_data.get("created_at"),
                "updated_at": source_data.get("updated_at"),
                "paid_at": source_data.get("processed_at"),
                "completed_at": source_data.get("closed_at"),
                # Source tracking
                "source_id": str(source_data.get("id")),
                "source_platform": "shopify",
                "source_data": {
                    "name": source_data.get("name", ""),
                    "financial_status": source_data.get("financial_status"),
                    "fulfillment_status": source_data.get("fulfillment_status"),
                    "gateway": source_data.get("gateway", ""),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(
                f"Failed to map order: {e}",
                {
                    "id": source_data.get("id"),
                    "name": source_data.get("name"),
                },
            )
            raise

    def _map_order_status(
        self, financial_status: str, fulfillment_status: str | None, cancelled_at: str | None
    ) -> str:
        """
        Map Shopify compound status to single internal status.

        Shopify has two separate status fields:
        - financial_status: pending, authorized, partially_paid, paid, partially_refunded, refunded, voided
        - fulfillment_status: null (unfulfilled), partial, fulfilled
        """
        if cancelled_at:
            return "cancelled"

        if financial_status == "refunded":
            return "refunded"

        if financial_status == "voided":
            return "cancelled"

        if fulfillment_status == "fulfilled":
            return "completed"

        if fulfillment_status == "partial":
            return "processing"

        if financial_status in ("paid", "partially_paid"):
            return "processing"

        if financial_status == "authorized":
            return "on_hold"

        return "pending"

    def _map_payment_status(self, financial_status: str) -> str:
        """Map Shopify financial status to payment status"""
        mapping = {
            "pending": "pending",
            "authorized": "pending",
            "partially_paid": "paid",
            "paid": "paid",
            "partially_refunded": "paid",
            "refunded": "refunded",
            "voided": "cancelled",
        }
        return mapping.get(financial_status, "pending")

    def _map_address(self, address_data: dict) -> dict:
        """Map Shopify address format"""
        if not address_data:
            return {}

        return {
            "first_name": address_data.get("first_name") or "",
            "last_name": address_data.get("last_name") or "",
            "company": address_data.get("company") or "",
            "address_1": address_data.get("address1") or "",
            "address_2": address_data.get("address2") or "",
            "city": address_data.get("city") or "",
            "state": address_data.get("province") or address_data.get("province_code") or "",
            "postcode": address_data.get("zip") or "",
            "country": address_data.get("country_code") or address_data.get("country") or "",
            "phone": address_data.get("phone") or "",
            "email": "",
        }

    def _map_line_items(self, line_items: list[dict]) -> list[dict]:
        """Map Shopify order line items"""
        mapped_items = []
        for item in line_items:
            mapped_items.append(
                {
                    "product_id": item.get("product_id"),
                    "variation_id": item.get("variant_id", 0),
                    "name": item.get("title") or item.get("name", ""),
                    "sku": item.get("sku") or "",
                    "quantity": item.get("quantity", 1),
                    "subtotal": self._parse_price(item.get("price", 0)),
                    "total": self._parse_price(
                        Decimal(str(item.get("price", 0))) * item.get("quantity", 1)
                    ),
                    "tax_total": self._parse_price(
                        sum(Decimal(str(tl.get("price", 0))) for tl in item.get("tax_lines", []))
                    ),
                    "price": self._parse_price(item.get("price", 0)),
                }
            )
        return mapped_items

    def _map_shipping_lines(self, shipping_lines: list[dict]) -> list[dict]:
        """Map Shopify shipping lines"""
        mapped_shipping = []
        for line in shipping_lines:
            mapped_shipping.append(
                {
                    "method_id": line.get("code") or "",
                    "method_title": line.get("title") or "",
                    "total": self._parse_price(line.get("price", 0)),
                    "tax_total": self._parse_price(
                        sum(Decimal(str(tl.get("price", 0))) for tl in line.get("tax_lines", []))
                    ),
                }
            )
        return mapped_shipping

    def _parse_price(self, price) -> Decimal | None:
        """Parse price to Decimal"""
        if price is None:
            return None
        try:
            return Decimal(str(price))
        except (ValueError, TypeError):
            self.log_warning(f"Failed to parse price: {price}")
            return None


class ShopifyDiscountMapper(BaseMapper):
    """Map Shopify price rules + discount codes to internal VoucherCode model"""

    def map(self, source_data: dict) -> dict:
        """
        Map Shopify price rule + discount code to internal format.

        Expects a combined dict with both price_rule and discount_code data:
        {
            "price_rule": {
                "id": 507328175,
                "title": "SUMMERSALE",
                "value_type": "percentage",
                "value": "-10.0",
                "target_type": "line_item",
                "allocation_method": "across",
                "starts_at": "2017-01-19T17:59:10-05:00",
                "ends_at": "2018-01-19T17:59:10-05:00",
                "usage_limit": 100
            },
            "discount_code": {
                "id": 507328175,
                "code": "SUMMERSALE",
                "usage_count": 5
            }
        }
        """
        try:
            price_rule = source_data.get("price_rule", source_data)
            discount_code = source_data.get("discount_code", {})

            # Shopify value is negative (e.g., "-10.0")
            raw_value = str(price_rule.get("value", "0"))
            value = abs(Decimal(raw_value)) if raw_value else Decimal("0")

            mapped = {
                "code": discount_code.get("code", "") or price_rule.get("title", ""),
                # Discount type and value
                "discount_type": self._map_discount_type(
                    price_rule.get("value_type", "fixed_amount")
                ),
                "discount_value": value,
                # Description
                "description": price_rule.get("title", ""),
                # Dates
                "start_date": price_rule.get("starts_at"),
                "end_date": price_rule.get("ends_at"),
                # Usage
                "current_uses": discount_code.get("usage_count", 0),
                "max_uses_total": price_rule.get("usage_limit"),
                "max_uses_per_customer": (price_rule.get("once_per_customer") and 1) or None,
                # Restrictions
                "min_order_value": self._parse_price(
                    price_rule.get("prerequisite_subtotal_range", {}).get(
                        "greater_than_or_equal_to"
                    )
                ),
                "exclude_sale_items": False,  # Not a Shopify concept
                # Source tracking
                "source_id": str(price_rule.get("id")),
                "source_platform": "shopify",
                "source_data": {
                    "value_type": price_rule.get("value_type"),
                    "target_type": price_rule.get("target_type"),
                    "allocation_method": price_rule.get("allocation_method"),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map discount: {e}", source_data)
            raise

    def _map_discount_type(self, value_type: str) -> str:
        """Map Shopify discount type to internal type"""
        mapping = {
            "percentage": "percentage",
            "fixed_amount": "fixed",
        }
        return mapping.get(value_type, "fixed")

    def _parse_price(self, price) -> Decimal | None:
        """Parse price to Decimal"""
        if not price:
            return None
        try:
            return Decimal(str(price))
        except (ValueError, TypeError):
            return None


class ShopifyArticleMapper(BaseMapper):
    """Map Shopify blog articles to internal BlogPost model"""

    def map(self, source_data: dict) -> dict:
        """
        Map Shopify article to internal format

        Shopify article structure:
        {
            "id": 989034056,
            "title": "Some article title",
            "handle": "some-article-title",
            "body_html": "<p>Article content</p>",
            "author": "John Doe",
            "summary_html": "<p>Article summary</p>",
            "tags": "tag1, tag2",
            "blog_id": 241253187,
            "published_at": "2014-04-07T14:53:27-04:00",
            "created_at": "2014-04-07T14:53:27-04:00",
            "image": {"src": "https://...jpg", "alt": "Alt text"}
        }
        """
        try:
            image = source_data.get("image") or {}

            mapped = {
                "title": source_data.get("title", ""),
                "slug": self.generate_slug(
                    source_data.get("handle", "") or source_data.get("title", "")
                ),
                "content": self.parse_html(source_data.get("body_html", "") or ""),
                "excerpt": self.parse_html(source_data.get("summary_html", "") or ""),
                "status": "published" if source_data.get("published_at") else "draft",
                "author_name": source_data.get("author", ""),
                # Dates
                "created_at": source_data.get("created_at"),
                "published_at": source_data.get("published_at"),
                # Tags (comma-separated string)
                "tags": self._parse_tags(source_data.get("tags", "")),
                # Featured image
                "featured_image_url": image.get("src") if image else None,
                "featured_image_alt": image.get("alt", "") if image else "",
                # Blog association
                "blog_id": source_data.get("blog_id"),
                # Source tracking
                "source_id": str(source_data.get("id")),
                "source_platform": "shopify",
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map article: {e}", source_data)
            raise

    def _parse_tags(self, tags_string: str) -> list[str]:
        """Parse Shopify comma-separated tags string"""
        if not tags_string:
            return []
        return [tag.strip() for tag in tags_string.split(",") if tag.strip()]
