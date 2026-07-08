"""
Standard field mappings for WooCommerce → Platform
Based on real WooCommerce v3 API response structure from cocosbotanica.com

Each mapping is a tuple: (dest_model, dest_field, transform_type)
- dest_model: Django model name (Product, Category, etc.)
- dest_field: Field name on the model
- transform_type: Transformation to apply (from MigrationMapping.TRANSFORM_TYPES)

Special destination models:
- 'meta': Store in imported_meta JSONField
- 'special': Requires custom handling (relationships, arrays)
"""

WOOCOMMERCE_MAPPINGS = {
    'products': {
        # Identity fields
        'id': ('Product', 'external_id', 'string'),
        'name': ('Product', 'name', 'string'),
        'slug': ('Product', 'slug', 'string'),
        'sku': ('Product', 'sku', 'string'),
        'permalink': ('meta', 'woocommerce_permalink', 'url'),

        # Product type and status
        'type': ('Product', 'product_type', 'woocommerce_type'),
        'status': ('Product', 'status', 'woocommerce_status'),
        'featured': ('Product', 'is_featured', 'boolean'),
        'catalog_visibility': ('meta', 'catalog_visibility', 'string'),

        # Content
        'description': ('Product', 'full_description', 'string'),
        'short_description': ('Product', 'short_description', 'string'),

        # Pricing (will need currency handling)
        'price': ('meta', 'current_price', 'money'),  # Effective price (regular or sale)
        'regular_price': ('Product', 'price', 'money'),
        'sale_price': ('meta', 'woocommerce_sale_price', 'money'),
        'price_html': ('meta', 'price_html', 'string'),
        'on_sale': ('meta', 'on_sale', 'boolean'),
        'date_on_sale_from': ('meta', 'sale_start_date', 'date'),
        'date_on_sale_to': ('meta', 'sale_end_date', 'date'),

        # Inventory
        'stock_quantity': ('meta', 'woocommerce_stock_quantity', 'integer_nullable'),
        'manage_stock': ('Product', 'track_inventory', 'boolean'),
        'stock_status': ('meta', 'stock_status', 'string'),
        'backorders': ('Product', 'allow_backorders', 'woocommerce_backorders'),
        'backorders_allowed': ('meta', 'backorders_allowed', 'boolean'),
        'backordered': ('meta', 'is_backordered', 'boolean'),
        'low_stock_amount': ('meta', 'low_stock_threshold', 'integer_nullable'),
        'sold_individually': ('meta', 'sold_individually', 'boolean'),

        # Physical attributes
        'weight': ('Product', 'weight', 'decimal_nullable'),
        'dimensions.length': ('Product', 'length', 'decimal_nullable'),
        'dimensions.width': ('Product', 'width', 'decimal_nullable'),
        'dimensions.height': ('Product', 'height', 'decimal_nullable'),

        # Shipping
        'shipping_required': ('Product', 'requires_shipping', 'boolean'),
        'shipping_taxable': ('meta', 'shipping_taxable', 'boolean'),
        'shipping_class': ('meta', 'shipping_class', 'string'),
        'shipping_class_id': ('meta', 'shipping_class_id', 'integer'),

        # Tax
        'tax_status': ('Product', 'is_taxable', 'tax_status_boolean'),
        'tax_class': ('meta', 'tax_class', 'string'),

        # Virtual/Downloadable
        'virtual': ('Product', 'is_virtual', 'boolean'),
        'downloadable': ('Product', 'is_digital', 'boolean'),
        'downloads': ('meta', 'download_files', 'json'),
        'download_limit': ('meta', 'download_limit', 'integer'),
        'download_expiry': ('meta', 'download_expiry_days', 'integer'),

        # Reviews
        'reviews_allowed': ('Product', 'allow_reviews', 'boolean'),
        'average_rating': ('meta', 'average_rating', 'decimal'),
        'rating_count': ('meta', 'rating_count', 'integer'),

        # Sales/stats
        'total_sales': ('meta', 'total_sales', 'integer'),
        'purchasable': ('meta', 'is_purchasable', 'boolean'),

        # Timestamps
        'date_created': ('Product', 'created_at', 'date'),
        'date_created_gmt': ('meta', 'date_created_gmt', 'date'),
        'date_modified': ('Product', 'updated_at', 'date'),
        'date_modified_gmt': ('meta', 'date_modified_gmt', 'date'),

        # Relationships (handled separately with special logic)
        'parent_id': ('special', 'parent_product', 'product_lookup'),
        'categories': ('special', 'categories', 'category_array'),
        'tags': ('special', 'tags', 'tag_array'),
        'images': ('special', 'images', 'image_array'),
        'variations': ('special', 'variations', 'variant_array'),
        'grouped_products': ('meta', 'grouped_product_ids', 'json'),

        # Brands (if using brand plugin)
        'brands': ('special', 'brands', 'brand_array'),

        # Store complex objects in meta
        'attributes': ('meta', 'attributes', 'json'),
        'default_attributes': ('meta', 'default_attributes', 'json'),
        'meta_data': ('meta', 'woocommerce_meta', 'meta_array'),

        # SEO (Yoast)
        'yoast_head': ('meta', 'yoast_head', 'string'),
        'yoast_head_json': ('meta', 'yoast_seo', 'json'),

        # Related products
        'upsell_ids': ('meta', 'upsell_ids', 'json'),
        'cross_sell_ids': ('meta', 'cross_sell_ids', 'json'),
        'related_ids': ('meta', 'related_ids', 'json'),

        # Purchase note
        'purchase_note': ('meta', 'purchase_note', 'string'),

        # Menu order (for manual sorting)
        'menu_order': ('meta', 'menu_order', 'integer'),

        # External product (affiliate)
        'external_url': ('meta', 'external_url', 'url'),
        'button_text': ('meta', 'external_button_text', 'string'),
    },

    'categories': {
        # Identity fields
        'id': ('Category', 'external_id', 'string'),
        'name': ('Category', 'name', 'string'),
        'slug': ('Category', 'slug', 'string'),
        'permalink': ('meta', 'woocommerce_permalink', 'url'),

        # Content
        'description': ('Category', 'description', 'string'),

        # Hierarchy
        'parent': ('special', 'parent_ref', 'category_parent'),

        # Display
        'display': ('meta', 'page_template', 'string'),  # default, products, subcategories, both
        'menu_order': ('Category', 'sort_order', 'integer'),

        # Stats
        'count': ('meta', 'product_count', 'integer'),

        # Media
        'image': ('special', 'image_url', 'image_download'),

        # SEO
        'yoast_head': ('meta', 'yoast_head', 'string'),
        'yoast_head_json': ('meta', 'yoast_seo', 'json'),
    },

    'customers': {
        # Identity fields
        'id': ('User', 'external_id', 'string'),
        'email': ('User', 'email', 'email'),
        'first_name': ('User', 'first_name', 'string'),
        'last_name': ('User', 'last_name', 'string'),
        'username': ('User', 'username', 'string'),

        # Role
        'role': ('meta', 'woocommerce_role', 'string'),

        # Timestamps
        'date_created': ('User', 'date_joined', 'date'),
        'date_created_gmt': ('meta', 'date_created_gmt', 'date'),
        'date_modified': ('meta', 'date_modified', 'date'),
        'date_modified_gmt': ('meta', 'date_modified_gmt', 'date'),

        # Addresses (handled specially)
        'billing': ('special', 'billing_address', 'address_object'),
        'shipping': ('special', 'shipping_address', 'address_object'),

        # Stats
        'is_paying_customer': ('meta', 'is_paying_customer', 'boolean'),
        'orders_count': ('meta', 'total_orders', 'integer'),
        'total_spent': ('meta', 'total_spent', 'money'),

        # Profile
        'avatar_url': ('meta', 'avatar_url', 'url'),

        # Meta data
        'meta_data': ('meta', 'woocommerce_meta', 'meta_array'),
    },

    'orders': {
        # Identity fields
        'id': ('Order', 'order_number', 'string'),
        'parent_id': ('meta', 'parent_order_id', 'integer'),
        'order_key': ('meta', 'order_key', 'string'),
        'number': ('meta', 'formatted_order_number', 'string'),

        # Status
        'status': ('Order', 'status', 'woocommerce_order_status'),

        # Currency
        'currency': ('meta', 'currency', 'string'),
        'currency_symbol': ('meta', 'currency_symbol', 'string'),

        # Timestamps
        'date_created': ('Order', 'created_at', 'date'),
        'date_created_gmt': ('meta', 'date_created_gmt', 'date'),
        'date_modified': ('meta', 'date_modified', 'date'),
        'date_modified_gmt': ('meta', 'date_modified_gmt', 'date'),
        'date_paid': ('meta', 'date_paid', 'date'),
        'date_paid_gmt': ('meta', 'date_paid_gmt', 'date'),
        'date_completed': ('meta', 'date_completed', 'date'),
        'date_completed_gmt': ('meta', 'date_completed_gmt', 'date'),

        # Totals
        'total': ('Order', 'total_amount', 'money'),
        'subtotal': ('Order', 'subtotal', 'money'),
        'total_tax': ('Order', 'tax_amount', 'money'),
        'shipping_total': ('Order', 'shipping_cost', 'money'),
        'shipping_tax': ('meta', 'shipping_tax', 'money'),
        'discount_total': ('Order', 'discount_amount', 'money'),
        'discount_tax': ('meta', 'discount_tax', 'money'),
        'cart_tax': ('meta', 'cart_tax', 'money'),
        'fees_total': ('meta', 'fees_total', 'money'),
        'refunded_total': ('meta', 'refunded_amount', 'money'),

        # Customer
        'customer_id': ('special', 'customer_ref', 'customer_lookup'),
        'customer_ip_address': ('meta', 'customer_ip', 'string'),
        'customer_user_agent': ('meta', 'customer_user_agent', 'string'),
        'customer_note': ('Order', 'notes', 'string'),

        # Addresses (handled specially)
        'billing': ('special', 'billing_address', 'address_object'),
        'shipping': ('special', 'shipping_address', 'address_object'),

        # Payment
        'payment_method': ('meta', 'payment_method', 'string'),
        'payment_method_title': ('meta', 'payment_method_title', 'string'),
        'transaction_id': ('meta', 'transaction_id', 'string'),

        # Shipping
        'shipping_lines': ('meta', 'shipping_lines', 'json'),

        # Coupons
        'coupon_lines': ('special', 'coupons_applied', 'coupon_lines_array'),

        # Items (handled specially)
        'line_items': ('special', 'order_items', 'order_items_array'),

        # Tax lines
        'tax_lines': ('meta', 'tax_lines', 'json'),
        'fee_lines': ('meta', 'fee_lines', 'json'),

        # Misc
        'prices_include_tax': ('meta', 'prices_include_tax', 'boolean'),
        'cart_hash': ('meta', 'cart_hash', 'string'),
        'created_via': ('meta', 'created_via', 'string'),
        'version': ('meta', 'woocommerce_version', 'string'),

        # Meta data
        'meta_data': ('meta', 'woocommerce_meta', 'meta_array'),
    },

    'reviews': {
        # Identity
        'id': ('meta', 'woocommerce_review_id', 'string'),

        # Product relationship
        'product_id': ('special', 'product_ref', 'product_lookup'),
        'product_name': ('meta', 'product_name', 'string'),
        'product_permalink': ('meta', 'product_permalink', 'url'),

        # Reviewer
        'reviewer': ('special', 'reviewer_name', 'string'),
        'reviewer_email': ('special', 'reviewer_email', 'email'),
        'reviewer_avatar_urls': ('meta', 'reviewer_avatar_urls', 'json'),

        # Review content
        'review': ('ProductReview', 'comment', 'string'),
        'rating': ('ProductReview', 'rating', 'integer'),

        # Status
        'status': ('ProductReview', 'is_approved', 'review_status'),
        'verified': ('ProductReview', 'is_verified_purchase', 'boolean'),

        # Timestamps
        'date_created': ('ProductReview', 'created_at', 'date'),
        'date_created_gmt': ('meta', 'date_created_gmt', 'date'),
    },

    'coupons': {
        # Identity
        'id': ('meta', 'woocommerce_coupon_id', 'string'),
        'code': ('VoucherCode', 'code', 'string'),

        # Discount
        'amount': ('VoucherCode', 'discount_value', 'decimal'),
        'discount_type': ('VoucherCode', 'discount_type', 'coupon_discount_type'),

        # Content
        'description': ('VoucherCode', 'description', 'string'),

        # Dates
        'date_created': ('meta', 'date_created', 'date'),
        'date_created_gmt': ('meta', 'date_created_gmt', 'date'),
        'date_modified': ('meta', 'date_modified', 'date'),
        'date_modified_gmt': ('meta', 'date_modified_gmt', 'date'),
        'date_expires': ('VoucherCode', 'end_date', 'date'),
        'date_expires_gmt': ('meta', 'date_expires_gmt', 'date'),

        # Usage
        'usage_count': ('VoucherCode', 'current_uses', 'integer'),
        'usage_limit': ('VoucherCode', 'max_uses_total', 'integer_nullable'),
        'usage_limit_per_user': ('VoucherCode', 'max_uses_per_customer', 'integer_nullable'),
        'limit_usage_to_x_items': ('meta', 'limit_usage_to_x_items', 'integer_nullable'),

        # Restrictions
        'individual_use': ('meta', 'individual_use', 'boolean'),
        'exclude_sale_items': ('VoucherCode', 'exclude_sale_items', 'boolean'),
        'minimum_amount': ('VoucherCode', 'min_order_value', 'money'),
        'maximum_amount': ('VoucherCode', 'max_discount_amount', 'money'),

        # Product restrictions (handled specially)
        'product_ids': ('special', 'eligible_products', 'product_ids_array'),
        'excluded_product_ids': ('meta', 'excluded_product_ids', 'json'),
        'product_categories': ('special', 'eligible_categories', 'category_ids_array'),
        'excluded_product_categories': ('meta', 'excluded_product_categories', 'json'),

        # Email restrictions
        'email_restrictions': ('meta', 'email_restrictions', 'json'),

        # Shipping
        'free_shipping': ('meta', 'free_shipping', 'boolean'),

        # Meta data
        'meta_data': ('meta', 'woocommerce_meta', 'meta_array'),
    },

    # WordPress Blog Posts (wp-json/wp/v2/posts)
    'blog_posts': {
        'id': ('meta', 'wordpress_post_id', 'string'),
        'title.rendered': ('BlogPost', 'title', 'string'),
        'slug': ('BlogPost', 'slug', 'string'),
        'status': ('BlogPost', 'status', 'string'),
        'content.rendered': ('BlogPost', 'simple_content', 'string'),
        'excerpt.rendered': ('BlogPost', 'excerpt', 'string'),
        'date': ('BlogPost', 'created_at', 'date'),
        'date_gmt': ('BlogPost', 'published_at', 'date'),
        'modified': ('meta', 'date_modified', 'date'),
        'featured_media': ('special', 'featured_image', 'integer'),
        'categories': ('special', 'blog_categories', 'category_array'),
        'tags': ('special', 'blog_tags', 'category_array'),
        'author': ('meta', 'wordpress_author_id', 'integer'),
    },

    # WordPress Blog Categories (wp-json/wp/v2/categories)
    'blog_categories': {
        'id': ('meta', 'wordpress_category_id', 'string'),
        'name': ('BlogCategory', 'name', 'string'),
        'slug': ('BlogCategory', 'slug', 'string'),
        'description': ('BlogCategory', 'description', 'string'),
        'parent': ('special', 'parent_category', 'integer'),
        'count': ('meta', 'wordpress_post_count', 'integer'),
    },

    # WordPress Blog Tags (wp-json/wp/v2/tags)
    'blog_tags': {
        'id': ('meta', 'wordpress_tag_id', 'string'),
        'name': ('BlogTag', 'name', 'string'),
        'slug': ('BlogTag', 'slug', 'string'),
        'count': ('meta', 'wordpress_post_count', 'integer'),
    },
}


# SEO-related meta fields to extract (Yoast SEO plugin)
SEO_META_FIELDS = [
    '_yoast_wpseo_primary_product_cat',  # Primary category ID
    '_yoast_wpseo_primary_product_brand',  # Primary brand ID
    '_yoast_wpseo_content_score',  # SEO score
    '_yoast_wpseo_estimated-reading-time-minutes',
    'wpseo_global_identifier_values',  # Product identifiers (GTIN, ISBN, MPN, etc.)
    '_cr_gtin',  # GTIN from SEO plugin
]


# Meta field prefixes to ignore (plugin noise)
# NOTE: afgc_ (gift card) prefix removed - now extracted by detect_gift_card_product()
IGNORE_META_PREFIXES = [
    # POS systems
    'foosales_',

    # Events/tickets plugins
    'WooCommerceEvents',

    # Theme-specific settings
    'site-',
    'ast-',
    'theme-',
    'stick-header-',
    'astra-',

    # Internal WordPress fields (except SEO)
    '_wp_',
    '_edit_',
    '_thumbnail_',
]


def should_skip_meta_field(key):
    """
    Determine if a meta_data field should be skipped.

    Args:
        key: Meta field key

    Returns:
        bool: True if should skip, False if should import
    """
    # Skip if matches ignore prefixes
    if any(key.startswith(prefix) for prefix in IGNORE_META_PREFIXES):
        return True

    # Never skip extension meta keys (subscriptions, add-ons, bundles, etc.)
    if key in EXTENSION_META_KEYS:
        return False

    # Skip internal WordPress fields (start with _) unless they're SEO fields
    if key.startswith('_') and key not in SEO_META_FIELDS:
        return True

    return False


def get_mapping_for_field(source_type, field_name):
    """
    Get mapping configuration for a specific field.

    Args:
        source_type: Type of source data ('products', 'categories', etc.)
        field_name: Name of the field

    Returns:
        tuple: (dest_model, dest_field, transform_type) or None if no mapping
    """
    mappings = WOOCOMMERCE_MAPPINGS.get(source_type, {})
    return mappings.get(field_name)


def get_all_mappings_for_type(source_type):
    """
    Get all field mappings for a source type.

    Args:
        source_type: Type of source data ('products', 'categories', etc.)

    Returns:
        dict: Field mappings
    """
    return WOOCOMMERCE_MAPPINGS.get(source_type, {})


# Extension meta field keys that should NOT be stripped by filter_meta_data.
# These are extracted by detection functions in transformers.py.
EXTENSION_META_KEYS = [
    # WooCommerce Subscriptions
    '_subscription_period',
    '_subscription_period_interval',
    '_subscription_price',
    '_subscription_sign_up_fee',
    '_subscription_trial_period',
    '_subscription_trial_length',
    '_subscription_length',
    '_subscription_limit',
    '_subscription_one_time_shipping',
    # WooCommerce Product Add-Ons
    '_product_addons',
    '_product_addons_exclude_global',
    # WooCommerce Product Bundles
    '_bundled_items',
    '_bundle_sell_ids',
    '_bundle_layout',
    # WooCommerce Gift Cards (multiple plugins)
    '_gift_card_amounts',
    '_gift_card_type',
    '_ywgc_amounts',
    '_ywgc_amounts_type',
    '_pw_gift_card_default_amount',
    '_pw_is_gift_card',
    # WooCommerce Composite Products
    '_composite_data',
    '_bto_data',
    '_composite_layout',
    '_composite_add_to_cart_form_location',
    # WooCommerce Bookings
    '_wc_booking_duration',
    '_wc_booking_duration_type',
    '_wc_booking_duration_unit',
    '_wc_booking_has_resources',
    '_wc_booking_resources_assignment',
    '_wc_booking_has_persons',
    '_wc_booking_min_persons',
    '_wc_booking_max_persons',
    '_wc_booking_base_cost',
    '_wc_booking_cost',
    '_wc_booking_block_cost',
    '_wc_booking_display_cost',
    '_wc_booking_has_restricted_days',
    '_wc_booking_restricted_days',
    '_wc_booking_availability',
    '_wc_booking_min_date',
    '_wc_booking_max_date',
    '_wc_booking_min_date_unit',
    '_wc_booking_max_date_unit',
    '_wc_booking_buffer_period',
    '_wc_booking_calendar_display_mode',
    '_wc_booking_requires_confirmation',
    '_wc_booking_user_can_cancel',
    '_wc_booking_cancel_limit',
    '_wc_booking_cancel_limit_unit',
    # WooCommerce Accommodation Bookings
    '_wc_accommodation_booking_check_in_time',
    '_wc_accommodation_booking_check_out_time',
    '_wc_accommodation_booking_min_duration',
    '_wc_accommodation_booking_max_duration',
]
