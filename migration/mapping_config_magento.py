"""
Standard field mappings for Magento 2 REST API -> Platform

Based on Magento 2 REST API /rest/V1/ response structure.

Each mapping is a tuple: (dest_model, dest_field, transform_type)
- dest_model: Django model name (Product, Category, etc.)
- dest_field: Field name on the model
- transform_type: Transformation to apply (from MigrationMapping.TRANSFORM_TYPES)

Special destination models:
- 'meta': Store in imported_meta JSONField
- 'special': Requires custom handling (relationships, arrays)

Note: Magento uses a custom_attributes array for many fields (EAV system).
These are accessed via resolve_custom_attribute() in the mappers, not via
direct field paths. The mappings below use 'custom_attributes.{code}' notation
to indicate EAV attributes.
"""

MAGENTO_MAPPINGS = {
    'products': {
        # Identity
        'id': ('Product', 'external_id', 'string'),
        'sku': ('Product', 'sku', 'string'),
        'name': ('Product', 'name', 'string'),
        'custom_attributes.url_key': ('Product', 'slug', 'string'),

        # Type and status
        'type_id': ('meta', 'magento_product_type', 'string'),
        'status': ('Product', 'status', 'magento_status'),
        'visibility': ('meta', 'magento_visibility', 'magento_visibility'),

        # Content
        'custom_attributes.description': ('Product', 'full_description', 'string'),
        'custom_attributes.short_description': ('Product', 'description', 'string'),

        # Pricing
        'price': ('Product', 'price', 'money'),
        'custom_attributes.special_price': ('Product', 'sale_price', 'money'),
        'custom_attributes.special_from_date': ('meta', 'sale_start_date', 'date'),
        'custom_attributes.special_to_date': ('meta', 'sale_end_date', 'date'),

        # Physical
        'weight': ('Product', 'weight', 'decimal_nullable'),

        # Inventory (from extension_attributes.stock_item)
        'extension_attributes.stock_item.qty': ('meta', 'stock_quantity', 'integer_nullable'),
        'extension_attributes.stock_item.is_in_stock': ('meta', 'is_in_stock', 'boolean'),
        'extension_attributes.stock_item.manage_stock': ('Product', 'track_inventory', 'boolean'),
        'extension_attributes.stock_item.backorders': ('meta', 'magento_backorders', 'integer_nullable'),

        # SEO
        'custom_attributes.meta_title': ('Product', 'meta_title', 'string'),
        'custom_attributes.meta_description': ('Product', 'meta_description', 'string'),
        'custom_attributes.meta_keyword': ('meta', 'magento_meta_keywords', 'string'),

        # Tax
        'custom_attributes.tax_class_id': ('meta', 'magento_tax_class_id', 'string'),

        # Relationships (handled separately with special logic)
        'extension_attributes.category_links': ('special', 'categories', 'category_array'),
        'media_gallery_entries': ('special', 'images', 'image_array'),

        # Timestamps
        'created_at': ('Product', 'created_at', 'date'),
        'updated_at': ('Product', 'updated_at', 'date'),

        # Attribute set (for reference)
        'attribute_set_id': ('meta', 'magento_attribute_set_id', 'integer_nullable'),
    },

    'categories': {
        'id': ('Category', 'external_id', 'string'),
        'name': ('Category', 'name', 'string'),
        'custom_attributes.url_key': ('Category', 'slug', 'string'),
        'custom_attributes.description': ('Category', 'description', 'string'),
        'parent_id': ('special', 'parent', 'category_parent'),
        'is_active': ('Category', 'is_active', 'boolean'),
        'position': ('Category', 'sort_order', 'integer_nullable'),
        'level': ('meta', 'magento_level', 'integer_nullable'),
        'product_count': ('meta', 'magento_product_count', 'integer_nullable'),
        'custom_attributes.image': ('special', 'image_url', 'image_download'),
        'custom_attributes.meta_title': ('Category', 'meta_title', 'string'),
        'custom_attributes.meta_description': ('Category', 'meta_description', 'string'),
    },

    'customers': {
        'id': ('User', 'external_id', 'string'),
        'email': ('User', 'email', 'email'),
        'firstname': ('User', 'first_name', 'string'),
        'lastname': ('User', 'last_name', 'string'),
        'group_id': ('meta', 'magento_group_id', 'integer_nullable'),
        'store_id': ('meta', 'magento_store_id', 'integer_nullable'),
        'website_id': ('meta', 'magento_website_id', 'integer_nullable'),
        'created_at': ('User', 'date_joined', 'date'),
        'updated_at': ('meta', 'updated_at', 'date'),
        'addresses': ('special', 'addresses', 'json'),
        'default_billing': ('meta', 'default_billing_id', 'string'),
        'default_shipping': ('meta', 'default_shipping_id', 'string'),
    },

    'orders': {
        'entity_id': ('Order', 'external_id', 'string'),
        'increment_id': ('Order', 'order_number', 'string'),
        'status': ('Order', 'status', 'magento_order_status'),
        'state': ('meta', 'magento_state', 'string'),
        'customer_email': ('meta', 'customer_email', 'email'),
        'customer_id': ('meta', 'magento_customer_id', 'string'),
        'customer_firstname': ('meta', 'customer_first_name', 'string'),
        'customer_lastname': ('meta', 'customer_last_name', 'string'),

        # Totals
        'subtotal': ('Order', 'subtotal', 'money'),
        'discount_amount': ('Order', 'discount_total', 'money'),
        'shipping_amount': ('Order', 'shipping_total', 'money'),
        'tax_amount': ('Order', 'tax_total', 'money'),
        'grand_total': ('Order', 'total', 'money'),
        'total_qty_ordered': ('meta', 'total_qty_ordered', 'decimal_nullable'),

        # Currency
        'order_currency_code': ('Order', 'currency', 'string'),

        # Payment
        'payment.method': ('Order', 'payment_method', 'string'),

        # Dates
        'created_at': ('Order', 'created_at', 'date'),
        'updated_at': ('Order', 'updated_at', 'date'),

        # Addresses and items (handled separately with special logic)
        'billing_address': ('special', 'billing_address', 'json'),
        'extension_attributes.shipping_assignments': ('special', 'shipping_address', 'json'),
        'items': ('special', 'line_items', 'json'),

        # Customer note
        'customer_note': ('Order', 'customer_notes', 'string'),
    },

    'reviews': {
        'id': ('meta', 'magento_review_id', 'string'),
        'title': ('meta', 'review_title', 'string'),
        'detail': ('meta', 'review_content', 'string'),
        'nickname': ('meta', 'reviewer_name', 'string'),
        'customer_id': ('meta', 'magento_customer_id', 'string'),
        'entity_pk_value': ('special', 'product_id', 'string'),
        'ratings': ('special', 'rating', 'json'),
        'review_status': ('meta', 'status', 'integer_nullable'),
        'created_at': ('meta', 'created_at', 'date'),
    },

    'coupons': {
        # Sales rule fields
        'rule_id': ('meta', 'magento_rule_id', 'string'),
        'name': ('VoucherCode', 'name', 'string'),
        'description': ('meta', 'description', 'string'),
        'from_date': ('VoucherCode', 'valid_from', 'date'),
        'to_date': ('VoucherCode', 'valid_to', 'date'),
        'is_active': ('VoucherCode', 'is_active', 'boolean'),
        'simple_action': ('VoucherCode', 'discount_type', 'magento_discount_type'),
        'discount_amount': ('VoucherCode', 'discount_value', 'money'),
        'uses_per_customer': ('VoucherCode', 'usage_limit_per_customer', 'integer_nullable'),
        'times_used': ('meta', 'times_used', 'integer_nullable'),
        'coupon_code': ('VoucherCode', 'code', 'string'),
    },

    'cms_pages': {
        'id': ('meta', 'magento_page_id', 'string'),
        'identifier': ('BlogPost', 'slug', 'string'),
        'title': ('BlogPost', 'title', 'string'),
        'content': ('BlogPost', 'content', 'string'),
        'content_heading': ('meta', 'content_heading', 'string'),
        'meta_title': ('BlogPost', 'meta_title', 'string'),
        'meta_description': ('BlogPost', 'meta_description', 'string'),
        'meta_keywords': ('meta', 'meta_keywords', 'string'),
        'active': ('BlogPost', 'is_published', 'boolean'),
        'creation_time': ('BlogPost', 'created_at', 'date'),
        'update_time': ('BlogPost', 'updated_at', 'date'),
    },
}
