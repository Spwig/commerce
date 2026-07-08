"""
Standard field mappings for Shopify Admin API → Platform
Based on Shopify REST Admin API 2025-01 response structure

Each mapping is a tuple: (dest_model, dest_field, transform_type)
- dest_model: Django model name (Product, Category, etc.)
- dest_field: Field name on the model
- transform_type: Transformation to apply (from MigrationMapping.TRANSFORM_TYPES)

Special destination models:
- 'meta': Store in imported_meta JSONField
- 'special': Requires custom handling (relationships, arrays)
"""

SHOPIFY_MAPPINGS = {
    'products': {
        # Identity fields
        'id': ('Product', 'external_id', 'string'),
        'title': ('Product', 'name', 'string'),
        'handle': ('Product', 'slug', 'string'),

        # Product type and status
        'status': ('Product', 'status', 'shopify_status'),
        'product_type': ('meta', 'shopify_product_type', 'string'),
        'vendor': ('meta', 'shopify_vendor', 'string'),

        # Content
        'body_html': ('Product', 'full_description', 'string'),

        # Pricing (from first variant — actual mapping done in executor)
        'variants.0.price': ('meta', 'current_price', 'money'),
        'variants.0.compare_at_price': ('Product', 'price', 'money'),
        'variants.0.sku': ('Product', 'sku', 'string'),

        # Inventory (from first variant)
        'variants.0.inventory_management': ('Product', 'track_inventory', 'shopify_inventory_tracked'),
        'variants.0.inventory_quantity': ('meta', 'shopify_stock_quantity', 'integer_nullable'),
        'variants.0.inventory_policy': ('Product', 'allow_backorders', 'shopify_inventory_policy'),

        # Physical attributes (from first variant)
        'variants.0.weight': ('Product', 'weight', 'decimal_nullable'),
        'variants.0.weight_unit': ('meta', 'weight_unit', 'string'),

        # Shipping
        'variants.0.requires_shipping': ('Product', 'requires_shipping', 'boolean'),

        # Tax
        'variants.0.taxable': ('Product', 'is_taxable', 'boolean'),

        # Timestamps
        'created_at': ('Product', 'created_at', 'date'),
        'updated_at': ('Product', 'updated_at', 'date'),
        'published_at': ('meta', 'published_at', 'date'),

        # Relationships (handled separately with special logic)
        'images': ('special', 'images', 'image_array'),
        'variants': ('special', 'variations', 'variant_array'),
        'options': ('meta', 'shopify_options', 'json'),

        # Tags (comma-separated string)
        'tags': ('special', 'tags', 'comma_separated'),

        # Template
        'template_suffix': ('meta', 'template_suffix', 'string'),
    },

    'collections': {
        # Identity fields
        'id': ('Category', 'external_id', 'string'),
        'title': ('Category', 'name', 'string'),
        'handle': ('Category', 'slug', 'string'),

        # Content
        'body_html': ('Category', 'description', 'string'),

        # Display
        'sort_order': ('meta', 'shopify_sort_order', 'string'),

        # Media
        'image': ('special', 'image_url', 'image_download'),

        # Timestamps
        'published_at': ('meta', 'published_at', 'date'),
        'updated_at': ('meta', 'date_modified', 'date'),
    },

    'customers': {
        # Identity fields
        'id': ('User', 'external_id', 'string'),
        'email': ('User', 'email', 'email'),
        'first_name': ('User', 'first_name', 'string'),
        'last_name': ('User', 'last_name', 'string'),

        # Timestamps
        'created_at': ('User', 'date_joined', 'date'),
        'updated_at': ('meta', 'date_modified', 'date'),

        # Addresses (handled specially)
        'addresses': ('special', 'addresses', 'address_array'),

        # Stats
        'orders_count': ('meta', 'total_orders', 'integer'),
        'total_spent': ('meta', 'total_spent', 'money'),

        # Profile
        'state': ('meta', 'shopify_customer_state', 'string'),
        'verified_email': ('meta', 'email_verified', 'boolean'),
        'tags': ('meta', 'shopify_customer_tags', 'string'),
        'note': ('meta', 'shopify_customer_note', 'string'),
        'tax_exempt': ('meta', 'tax_exempt', 'boolean'),
    },

    'orders': {
        # Identity fields
        'id': ('meta', 'shopify_order_id', 'string'),
        'order_number': ('Order', 'order_number', 'string'),
        'name': ('meta', 'shopify_order_name', 'string'),

        # Status (compound — financial + fulfillment)
        'financial_status': ('Order', 'status', 'shopify_order_status'),

        # Currency
        'currency': ('meta', 'currency', 'string'),
        'presentment_currency': ('meta', 'presentment_currency', 'string'),

        # Timestamps
        'created_at': ('Order', 'created_at', 'date'),
        'updated_at': ('meta', 'date_modified', 'date'),
        'processed_at': ('meta', 'date_paid', 'date'),
        'closed_at': ('meta', 'date_completed', 'date'),
        'cancelled_at': ('meta', 'date_cancelled', 'date'),

        # Totals
        'total_price': ('Order', 'total_amount', 'money'),
        'subtotal_price': ('Order', 'subtotal', 'money'),
        'total_tax': ('Order', 'tax_amount', 'money'),
        'total_discounts': ('Order', 'discount_amount', 'money'),

        # Customer
        'customer.id': ('special', 'customer_ref', 'customer_lookup'),
        'email': ('meta', 'customer_email', 'email'),
        'contact_email': ('meta', 'contact_email', 'email'),
        'customer_note': ('Order', 'notes', 'string'),

        # Addresses (handled specially)
        'billing_address': ('special', 'billing_address', 'address_object'),
        'shipping_address': ('special', 'shipping_address', 'address_object'),

        # Payment
        'payment_gateway_names': ('meta', 'payment_gateways', 'json'),
        'gateway': ('meta', 'payment_gateway', 'string'),

        # Items (handled specially)
        'line_items': ('special', 'order_items', 'order_items_array'),

        # Shipping
        'shipping_lines': ('meta', 'shipping_lines', 'json'),

        # Discount codes
        'discount_codes': ('meta', 'discount_codes', 'json'),

        # Tax lines
        'tax_lines': ('meta', 'tax_lines', 'json'),

        # Misc
        'taxes_included': ('meta', 'taxes_included', 'boolean'),
        'source_name': ('meta', 'source_name', 'string'),
        'tags': ('meta', 'shopify_order_tags', 'string'),
        'note': ('Order', 'notes', 'string'),
    },

    'discounts': {
        # Identity
        'price_rule.id': ('meta', 'shopify_price_rule_id', 'string'),
        'discount_code.code': ('VoucherCode', 'code', 'string'),

        # Discount
        'price_rule.value': ('VoucherCode', 'discount_value', 'shopify_discount_value'),
        'price_rule.value_type': ('VoucherCode', 'discount_type', 'shopify_discount_type'),

        # Content
        'price_rule.title': ('VoucherCode', 'description', 'string'),

        # Dates
        'price_rule.starts_at': ('meta', 'starts_at', 'date'),
        'price_rule.ends_at': ('VoucherCode', 'end_date', 'date'),

        # Usage
        'discount_code.usage_count': ('VoucherCode', 'current_uses', 'integer'),
        'price_rule.usage_limit': ('VoucherCode', 'max_uses_total', 'integer_nullable'),

        # Restrictions
        'price_rule.once_per_customer': ('meta', 'once_per_customer', 'boolean'),
        'price_rule.prerequisite_subtotal_range': ('meta', 'prerequisite_subtotal_range', 'json'),

        # Target
        'price_rule.target_type': ('meta', 'target_type', 'string'),
        'price_rule.allocation_method': ('meta', 'allocation_method', 'string'),
    },

    # Shopify Blog Articles
    'articles': {
        'id': ('meta', 'shopify_article_id', 'string'),
        'title': ('BlogPost', 'title', 'string'),
        'handle': ('BlogPost', 'slug', 'string'),
        'body_html': ('BlogPost', 'simple_content', 'string'),
        'summary_html': ('BlogPost', 'excerpt', 'string'),
        'published_at': ('BlogPost', 'published_at', 'date'),
        'created_at': ('BlogPost', 'created_at', 'date'),
        'author': ('meta', 'shopify_author', 'string'),
        'blog_id': ('special', 'blog_category', 'integer'),
        'tags': ('special', 'blog_tags', 'comma_separated'),
        'image': ('special', 'featured_image', 'image_download'),
    },
}
