"""
Sample Data Provider for Email Template Preview
Provides realistic sample data for testing and previewing email templates
"""


class SampleDataProvider:
    """
    Provides sample data for email template previews
    """

    @staticmethod
    def get_sample_data(template_type: str, language: str = "en", request=None) -> dict:
        """
        Get sample data for template preview

        Args:
            template_type: Template type (e.g., 'order_confirmation')
            language: Language code for localized data
            request: Optional request object to build absolute URLs

        Returns:
            Dict with template variables and sample values
        """
        # Build shop URL from request or use default
        if request:
            shop_url = request.build_absolute_uri("/").rstrip("/")
        else:
            shop_url = "https://demo.example.com"

        # Common variables across all templates - use actual SiteSettings when available
        common_data = {
            **SampleDataProvider._get_site_settings_sample_data(shop_url, request),
            **SampleDataProvider._get_site_logo_sample_data(shop_url, request),
        }

        # Template-specific data
        template_data = {
            "order_confirmation": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "order_number": "ORD-2025-001234",
                "invoice_number": "ORD-2025-001234",  # Same as order_number
                "order_date": "2025-10-29",
                "order_total": "$156.50",
                "order_url": f"{shop_url}/orders/001234",
                "estimated_delivery_date": "November 3, 2025",
                "estimated_delivery_start": "November 3",
                "estimated_delivery_end": "November 5",
                "items": [
                    {
                        "name": "Premium Cotton T-Shirt",
                        "sku": "SHIRT-COTTON-BLK-M",
                        "quantity": 2,
                        "price": "$29.99",
                        "subtotal": "$59.98",
                        "product_url": f"{shop_url}/products/premium-cotton-tshirt",
                        "product_thumbnail_url": f"{shop_url}/media/products/shirts/cotton-tshirt-thumb.webp",
                    },
                    {
                        "name": "Denim Jeans",
                        "sku": "JEANS-DENIM-32",
                        "quantity": 1,
                        "price": "$79.99",
                        "subtotal": "$79.99",
                        "product_url": f"{shop_url}/products/denim-jeans",
                        "product_thumbnail_url": f"{shop_url}/media/products/jeans/denim-jeans-thumb.webp",
                    },
                ],
                "subtotal": "$139.97",
                "shipping": "$10.00",
                "tax": "$6.53",
                "total": "$156.50",
                "shipping_address": {
                    "full_address": "123 Main Street, New York, NY 10001",
                    "name": SampleDataProvider._get_name(language),
                    "street": "123 Main Street",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "United States",
                },
                "billing_address": {
                    "full_address": "123 Main Street, New York, NY 10001",
                    "name": SampleDataProvider._get_name(language),
                    "street": "123 Main Street",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "United States",
                },
                "payment_method": "Visa ending in 4242",
                "timeline_stages": [
                    {
                        "stage": "ordered",
                        "label": "Order Placed",
                        "active": True,
                        "completed": True,
                    },
                    {
                        "stage": "processing",
                        "label": "Processing",
                        "active": False,
                        "completed": False,
                    },
                    {"stage": "shipped", "label": "Shipped", "active": False, "completed": False},
                    {
                        "stage": "delivered",
                        "label": "Delivered",
                        "active": False,
                        "completed": False,
                    },
                ],
            },
            "shipping_confirmation": {
                "customer_name": SampleDataProvider._get_name(language),
                "order_number": "ORD-2025-001234",
                "invoice_number": "ORD-2025-001234",
                "order_url": f"{shop_url}/orders/001234",
                "tracking_number": "1Z999AA10123456784",
                "tracking_url": "https://www.fedex.com/track?tracknumber=1Z999AA10123456784",
                "carrier": "FedEx",
                "carrier_logo_url": f"{shop_url}/static/carriers/fedex.png",
                "estimated_delivery_date": "November 2, 2025",
                "shipped_date": "October 29, 2025",
                "shipping_address": {
                    "full_address": "123 Main Street, New York, NY 10001",
                    "name": SampleDataProvider._get_name(language),
                    "street": "123 Main Street",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "United States",
                },
                "items": [
                    {
                        "name": "Premium Cotton T-Shirt",
                        "sku": "SHIRT-COTTON-BLK-M",
                        "quantity": 2,
                        "product_thumbnail_url": f"{shop_url}/media/products/shirts/cotton-tshirt-thumb.webp",
                    },
                    {
                        "name": "Denim Jeans",
                        "sku": "JEANS-DENIM-32",
                        "quantity": 1,
                        "product_thumbnail_url": f"{shop_url}/media/products/jeans/denim-jeans-thumb.webp",
                    },
                ],
                "timeline_stages": [
                    {
                        "stage": "ordered",
                        "label": "Order Placed",
                        "active": False,
                        "completed": True,
                    },
                    {
                        "stage": "processing",
                        "label": "Processing",
                        "active": False,
                        "completed": True,
                    },
                    {"stage": "shipped", "label": "Shipped", "active": True, "completed": True},
                    {
                        "stage": "delivered",
                        "label": "Delivered",
                        "active": False,
                        "completed": False,
                    },
                ],
            },
            "password_reset": {
                "user_name": SampleDataProvider._get_name(language),
                "reset_url": f"{shop_url}/reset-password?token=abc123xyz",
                "expiry_hours": 24,
            },
            "email_verification": {
                "user_name": SampleDataProvider._get_name(language),
                "verification_url": f"{shop_url}/verify-email?token=xyz789abc",
                "expiry_hours": 48,
            },
            "payment_confirmation": {
                "customer_name": SampleDataProvider._get_name(language),
                "order_number": "ORD-2025-001234",
                "invoice_number": "ORD-2025-001234",
                "order_url": f"{shop_url}/orders/001234",
                "payment_amount": "$156.50",
                "payment_method": "Visa ending in 4242",
                "payment_date": "October 29, 2025",
                "transaction_id": "TXN-2025-789456",
                "items": [
                    {
                        "name": "Premium Cotton T-Shirt",
                        "quantity": 2,
                        "price": "$29.99",
                        "subtotal": "$59.98",
                        "product_thumbnail_url": f"{shop_url}/media/products/shirts/cotton-tshirt-thumb.webp",
                    },
                    {
                        "name": "Denim Jeans",
                        "quantity": 1,
                        "price": "$79.99",
                        "subtotal": "$79.99",
                        "product_thumbnail_url": f"{shop_url}/media/products/jeans/denim-jeans-thumb.webp",
                    },
                ],
                "subtotal": "$139.97",
                "tax": "$6.53",
                "total": "$156.50",
                "timeline_stages": [
                    {
                        "stage": "ordered",
                        "label": "Order Placed",
                        "active": False,
                        "completed": True,
                    },
                    {
                        "stage": "processing",
                        "label": "Processing",
                        "active": True,
                        "completed": True,
                    },
                    {"stage": "shipped", "label": "Shipped", "active": False, "completed": False},
                    {
                        "stage": "delivered",
                        "label": "Delivered",
                        "active": False,
                        "completed": False,
                    },
                ],
            },
            "delivery_confirmation": {
                "customer_name": SampleDataProvider._get_name(language),
                "order_number": "ORD-2025-001234",
                "invoice_number": "ORD-2025-001234",
                "order_url": f"{shop_url}/orders/001234",
                "delivery_date": "November 2, 2025",
                "delivered_at": "2:45 PM",
                "delivered_to": "123 Main Street, New York, NY 10001",
                "signature_required": False,
                "carrier": "FedEx",
                "items": [
                    {
                        "name": "Premium Cotton T-Shirt",
                        "quantity": 2,
                        "product_thumbnail_url": f"{shop_url}/media/products/shirts/cotton-tshirt-thumb.webp",
                    },
                    {
                        "name": "Denim Jeans",
                        "quantity": 1,
                        "product_thumbnail_url": f"{shop_url}/media/products/jeans/denim-jeans-thumb.webp",
                    },
                ],
                "timeline_stages": [
                    {
                        "stage": "ordered",
                        "label": "Order Placed",
                        "active": False,
                        "completed": True,
                    },
                    {
                        "stage": "processing",
                        "label": "Processing",
                        "active": False,
                        "completed": True,
                    },
                    {"stage": "shipped", "label": "Shipped", "active": False, "completed": True},
                    {"stage": "delivered", "label": "Delivered", "active": True, "completed": True},
                ],
            },
            "refund_notification": {
                "customer_name": SampleDataProvider._get_name(language),
                "order_number": "ORD-2025-001234",
                "invoice_number": "ORD-2025-001234",
                "order_url": f"{shop_url}/orders/001234",
                "refund_amount": "$156.50",
                "refund_method": "Original payment method (Visa ending in 4242)",
                "refund_date": "November 5, 2025",
                "refund_reason": "Product returned in original condition",
                "refund_timeline": "5-10 business days",
                "processing_days": "5-7 business days",
                "items": [
                    {
                        "name": "Premium Cotton T-Shirt",
                        "quantity": 2,
                        "price": "$29.99",
                        "subtotal": "$59.98",
                        "product_thumbnail_url": f"{shop_url}/media/products/shirts/cotton-tshirt-thumb.webp",
                        "refund_reason": "Size too small",
                    },
                    {
                        "name": "Denim Jeans",
                        "quantity": 1,
                        "price": "$79.99",
                        "subtotal": "$79.99",
                        "product_thumbnail_url": f"{shop_url}/media/products/jeans/denim-jeans-thumb.webp",
                        "refund_reason": "Color not as expected",
                    },
                ],
                "subtotal": "$139.97",
                "tax_refund": "$6.53",
                "shipping_refund": "$10.00",
                "total": "$156.50",
            },
            "admin_new_order": {
                "order_number": "ORD-2025-001234",
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "order_total": "$156.50",
                "order_date": "October 29, 2025",
                "items_count": 3,
                "admin_url": f"{shop_url}/admin/orders/1234",
            },
            "admin_payment_failed": {
                "order_number": "ORD-2025-001234",
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "payment_amount": "$156.50",
                "error_message": "Insufficient funds",
                "error_code": "CARD_DECLINED",
                "retry_url": f"{shop_url}/admin/orders/1234",
                "attempt_number": 2,
            },
            "admin_payment_sdk_failure": {
                "provider_name": "Airwallex",
                "error_type": "sdk_load_failure",
                "timestamp": "February 18, 2026 at 14:30 UTC",
                "failure_count": 5,
                "admin_url": f"{shop_url}/en/admin/payment_providers/paymentprovideraccount/",
                "page_url": f"{shop_url}/en/checkout/",
            },
            # New Template Types
            "account_welcome": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "account_url": f"{shop_url}/account",
                "shop_benefits": [
                    "Faster checkout with saved addresses",
                    "Track your orders in real-time",
                    "Save items to your wishlist",
                    "Exclusive member-only discounts",
                    "Early access to new products",
                ],
                "getting_started_url": f"{shop_url}/getting-started",
                "browse_products_url": f"{shop_url}/products",
            },
            "order_delay": {
                "customer_name": SampleDataProvider._get_name(language),
                "order_number": "ORD-2025-001234",
                "invoice_number": "ORD-2025-001234",
                "order_url": f"{shop_url}/orders/001234",
                "order_date": "October 29, 2025",
                "original_delivery_date": "November 2, 2025",
                "new_delivery_date": "November 8, 2025",
                "delay_reason": "Due to unexpected high demand, your order is taking a bit longer to process. We sincerely apologize for the inconvenience and appreciate your patience.",
                "items": [
                    {
                        "name": "Premium Cotton T-Shirt",
                        "quantity": 2,
                        "product_thumbnail_url": f"{shop_url}/media/products/shirts/cotton-tshirt-thumb.webp",
                    },
                    {
                        "name": "Denim Jeans",
                        "quantity": 1,
                        "product_thumbnail_url": f"{shop_url}/media/products/jeans/denim-jeans-thumb.webp",
                    },
                ],
                "compensation_offered": True,
                "compensation_details": "10% discount on your next order",
                "discount_code": "SORRY10",
            },
            "review_request": {
                "customer_name": SampleDataProvider._get_name(language),
                "order_number": "ORD-2025-001234",
                "order_url": f"{shop_url}/orders/001234",
                "delivery_date": "November 2, 2025",
                "days_since_delivery": 7,
                "items": [
                    {
                        "name": "Premium Cotton T-Shirt",
                        "quantity": 2,
                        "product_url": f"{shop_url}/products/premium-cotton-tshirt",
                        "review_url": f"{shop_url}/products/premium-cotton-tshirt/review",
                        "product_thumbnail_url": f"{shop_url}/media/products/shirts/cotton-tshirt-thumb.webp",
                    },
                    {
                        "name": "Denim Jeans",
                        "quantity": 1,
                        "product_url": f"{shop_url}/products/denim-jeans",
                        "review_url": f"{shop_url}/products/denim-jeans/review",
                        "product_thumbnail_url": f"{shop_url}/media/products/jeans/denim-jeans-thumb.webp",
                    },
                ],
                "incentive_offered": True,
                "incentive_details": "Leave a review and get 10% off your next purchase!",
                "incentive_code": "REVIEW10",
            },
            "back_in_stock": {
                "product_name": "Premium Wireless Headphones",
                "variant_name": "Midnight Black",
                "product_url": f"{shop_url}/products/premium-wireless-headphones",
                "product_image_url": f"{shop_url}/media/products/electronics/headphones-black-thumb.webp",
                "subscriber_email": "customer@example.com",
            },
            # Account Templates
            "account_invitation": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "total_orders": 5,
                "total_spent": "$847.50",
                "activation_url": f"{shop_url}/account/activate?token=abc123def456",
                "site_name": "Demo Store",
                "expiry_hours": 72,
            },
            # Gift Card Templates
            "gift_card_delivery": {
                "gift_card": {
                    "code": "GC-ABCD-EFGH-IJKL",
                    "current_balance": "$50.00",
                    "initial_value": "$50.00",
                    "expires_at": "December 31, 2026",
                    "message": "Happy Birthday! Hope you find something special!",
                    "sender_name": "John Smith",
                    "recipient_name": "Sarah Johnson",
                    "recipient_email": "sarah@example.com",
                },
                "recipient_name": "Sarah Johnson",
                "recipient_email": "sarah@example.com",
                "sender_name": "John Smith",
                "gift_card_code": "GC-ABCD-EFGH-IJKL",
                "gift_card_amount": "$50.00",
                "gift_card_message": "Happy Birthday! Hope you find something special!",
                "gift_card_expiry": "December 31, 2026",
                "check_balance_url": f"{shop_url}/gift-cards/check-balance/",
                "redeem_url": f"{shop_url}/gift-cards/redeem/",
            },
            # Referral Program Templates
            "referral_reward_issued_referrer": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "referrer@example.com",
                "reward_amount": "$15.00",
                "reward_type": "credit",
                "reward_type_display": "Store Credit",
                "reward_currency": "$",
                "expires_at": "December 31, 2025",
                "referee_name": "Sarah Johnson",
                "referee_email": "sarah@example.com",
                "total_referrals": 7,
                "total_rewards_earned": "$105.00",
                "referral_link": f"{shop_url}/ref/JOHN2025",
                "referral_dashboard_url": f"{shop_url}/account/referrals/",
                "referral_message": "Check out this amazing store! Use my link for a discount.",
            },
            "referral_reward_issued_referee": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "newcustomer@example.com",
                "reward_amount": "10%",
                "reward_type": "percent",
                "reward_type_display": "Discount",
                "reward_currency": "%",
                "expires_at": "December 31, 2025",
                "referrer_name": "John Smith",
                "my_referral_link_url": f"{shop_url}/account/referrals/",
                "browse_products_url": f"{shop_url}/products",
            },
            "referral_successful": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "referrer@example.com",
                "referee_name": "Sarah Johnson",
                "referee_email": "sarah@example.com",
                "referral_link": f"{shop_url}/ref/JOHN2025",
                "referral_dashboard_url": f"{shop_url}/account/referrals/",
                "total_referrals": 8,
                "total_rewards": "$120.00",
                "conversion_rate": "75%",
                "pending_rewards": "$15.00",
            },
            "referral_reward_expiring": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "reward_amount": "$15.00",
                "reward_type": "credit",
                "reward_type_display": "Store Credit",
                "days_until_expiration": 7,
                "expiration_date": "November 15, 2025",
                "browse_products_url": f"{shop_url}/products",
                "account_url": f"{shop_url}/account",
            },
            "referral_invitation": {
                "referrer_name": SampleDataProvider._get_name(language),
                "referrer_email": "referrer@example.com",
                "referral_link": f"{shop_url}/ref/JOHN2025",
                "reward_amount": "10%",
                "reward_description": "Get 10% off your first order",
                "personal_message": "Hey! I thought you would love this store. Use my link to get 10% off your first order!",
                "referrer_reward": "$15.00",
                "referrer_reward_description": "Your friend earns $15 store credit when you make a purchase",
            },
            # Digital Product Templates
            "digital_product_delivery": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "order_number": "ORD-2025-001234",
                "order_date": "October 29, 2025",
                "product_name": "Ultimate Photo Editing Suite",
                "product_version": "v2.5.1",
                "file_name": "photo-editing-suite-v2.5.1.zip",
                "file_size": "1.2 GB",
                "download_url": f"{shop_url}/downloads/abc123xyz789",
                "download_limit": 5,
                "downloads_remaining": 5,
                "expiration_days": 30,
                "expiration_date": "November 29, 2025",
                "account_url": f"{shop_url}/account/downloads",
                "digital_items": [
                    {
                        "product_name": "Ultimate Photo Editing Suite",
                        "quantity": 1,
                        "assets": [
                            {
                                "filename": "photo-editing-suite-v2.5.1.zip",
                                "version": "v2.5.1",
                                "size": "1.2 GB",
                                "download_limit": 5,
                                "expiration_days": 30,
                                "download_url": f"{shop_url}/downloads/abc123xyz789",
                            },
                        ],
                    },
                ],
            },
            "digital_product_license_key": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "order_number": "ORD-2025-001234",
                "order_date": "October 29, 2025",
                "product_name": "Ultimate Photo Editing Suite",
                "product_version": "v2.5.1",
                "license_key": "XXXX-XXXX-XXXX-XXXX-XXXX",
                "license_type": "Professional License",
                "license_type_display": "Professional License",
                "max_activations": 3,
                "current_activations": 0,
                "is_lifetime": False,
                "expiration_date": "November 1, 2026",
                "download_url": f"{shop_url}/downloads/abc123xyz789",
                "activation_url": f"{shop_url}/activate",
                "account_url": f"{shop_url}/account/licenses",
                "license_keys": [
                    {
                        "key": "XXXX-XXXX-XXXX-XXXX-XXXX",
                        "type": "Professional License",
                        "max_activations": 3,
                        "product_name": "Ultimate Photo Editing Suite",
                    },
                ],
            },
            "digital_product_download_expired": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "order_number": "ORD-2025-001234",
                "product_name": "Ultimate Photo Editing Suite",
                "expiration_days": 30,
                "expired_date": "November 29, 2025",
                "account_url": f"{shop_url}/account/downloads",
                "contact_support_url": f"{shop_url}/contact",
                "redownload_request_url": f"{shop_url}/account/downloads/request-access",
            },
            "digital_product_license_expired": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "product_name": "Ultimate Photo Editing Suite",
                "license_key": "XXXX-XXXX-XXXX-XXXX-XXXX",
                "expiration_date": "November 1, 2025",
                "days_since_expiry": 7,
                "renewal_url": f"{shop_url}/renew/abc123",
                "account_url": f"{shop_url}/account/licenses",
                "renewal_discount": "20%",
                "renewal_price": "$79.99",
                "original_price": "$99.99",
            },
            # Subscription Templates
            "subscription_created": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "subscription_amount": "$29.99",
                "billing_cycle": "month",
                "billing_cycle_display": "Monthly",
                "trial_period": 14,
                "trial_end_date": "November 15, 2025",
                "next_billing_date": "December 15, 2025",
                "payment_method": "Visa ending in 4242",
                "subscription_start_date": "November 1, 2025",
                "manage_subscription_url": f"{shop_url}/account/subscriptions",
                "plan_benefits": [
                    "Unlimited access to premium content",
                    "Priority customer support",
                    "Early access to new features",
                    "Exclusive member discounts",
                ],
            },
            "subscription_trial_ending": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "days_remaining": 3,
                "trial_end_date": "November 15, 2025",
                "subscription_amount": "$29.99",
                "billing_cycle": "month",
                "payment_method": "Visa ending in 4242",
                "manage_subscription_url": f"{shop_url}/account/subscriptions",
                "cancel_subscription_url": f"{shop_url}/account/subscriptions/cancel",
                "update_payment_url": f"{shop_url}/account/payment-methods",
            },
            "subscription_renewal_reminder": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "subscription_amount": "$29.99",
                "renewal_date": "November 15, 2025",
                "days_until_renewal": 7,
                "billing_cycle": "month",
                "payment_method": "Visa ending in 4242",
                "manage_subscription_url": f"{shop_url}/account/subscriptions",
                "update_payment_url": f"{shop_url}/account/payment-methods",
                "cancel_subscription_url": f"{shop_url}/account/subscriptions/cancel",
            },
            "subscription_payment_success": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "subscription_amount": "$29.99",
                "payment_date": "November 1, 2025",
                "next_billing_date": "December 1, 2025",
                "billing_cycle": "month",
                "payment_method": "Visa ending in 4242",
                "transaction_id": "TXN-2025-789456",
                "invoice_url": f"{shop_url}/invoices/INV-2025-001234",
                "invoice_number": "INV-2025-001234",
                "manage_subscription_url": f"{shop_url}/account/subscriptions",
            },
            "subscription_payment_failed": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "subscription_amount": "$29.99",
                "payment_method": "Visa ending in 4242",
                "failure_reason": "Your card was declined",
                "failure_code": "card_declined",
                "retry_date": "November 4, 2025",
                "grace_period_days": 7,
                "grace_period_end_date": "November 8, 2025",
                "update_payment_url": f"{shop_url}/account/payment-methods",
                "manage_subscription_url": f"{shop_url}/account/subscriptions",
                "attempt_number": 1,
                "max_attempts": 3,
            },
            "subscription_paused": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "paused_date": "November 1, 2025",
                "resume_date": "January 1, 2026",
                "pause_duration": "2 months",
                "pause_reason": "Requested by customer",
                "manage_subscription_url": f"{shop_url}/account/subscriptions",
                "resume_subscription_url": f"{shop_url}/account/subscriptions/resume",
            },
            "subscription_resumed": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "subscription_amount": "$29.99",
                "resumed_date": "January 1, 2026",
                "next_billing_date": "January 1, 2026",
                "billing_cycle": "month",
                "payment_method": "Visa ending in 4242",
                "manage_subscription_url": f"{shop_url}/account/subscriptions",
            },
            "subscription_canceled": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "canceled_date": "November 1, 2025",
                "access_until_date": "November 30, 2025",
                "cancellation_reason": "Customer requested cancellation",
                "days_remaining": 29,
                "reactivate_url": f"{shop_url}/account/subscriptions/reactivate",
                "feedback_url": f"{shop_url}/feedback",
                "browse_plans_url": f"{shop_url}/plans",
            },
            "subscription_expired": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "expired_date": "November 30, 2025",
                "subscription_amount": "$29.99",
                "resubscribe_url": f"{shop_url}/subscribe/premium",
                "browse_plans_url": f"{shop_url}/plans",
                "special_offer": "20% off if you resubscribe within 7 days",
                "offer_code": "COMEBACK20",
                "offer_expires": "December 7, 2025",
            },
            "subscription_payment_method_expiring": {
                "customer_name": SampleDataProvider._get_name(language),
                "customer_email": "customer@example.com",
                "plan_name": "Premium Monthly",
                "product_name": "Premium Membership",
                "card_brand": "Visa",
                "card_last4": "4242",
                "card_expiry": "November 2025",
                "card_expiry_month": "11",
                "card_expiry_year": "2025",
                "days_until_expiry": 14,
                "next_billing_date": "December 1, 2025",
                "subscription_amount": "$29.99",
                "update_payment_url": f"{shop_url}/account/payment-methods",
                "manage_subscription_url": f"{shop_url}/account/subscriptions",
            },
            # Marketing Templates
            "newsletter": {
                "subscriber_email": "subscriber@example.com",
                "subscriber_name": SampleDataProvider._get_name(language),
                "newsletter_title": "November Special Edition",
                "newsletter_subtitle": "Exclusive deals just for you!",
                "preheader_text": "Exclusive deals just for you!",
                "featured_products": [
                    {
                        "name": "Premium Wireless Headphones",
                        "description": "High-quality audio with noise cancellation",
                        "price": "$129.99",
                        "sale_price": "$99.99",
                        "discount_percent": "23%",
                        "product_url": f"{shop_url}/products/premium-wireless-headphones",
                        "product_image_url": f"{shop_url}/media/products/electronics/headphones-thumb.webp",
                    },
                    {
                        "name": "Organic Cotton T-Shirt",
                        "description": "Sustainable comfort in classic style",
                        "price": "$34.99",
                        "sale_price": None,
                        "discount_percent": None,
                        "product_url": f"{shop_url}/products/organic-cotton-tshirt",
                        "product_image_url": f"{shop_url}/media/products/shirts/organic-tshirt-thumb.webp",
                    },
                    {
                        "name": "Leather Messenger Bag",
                        "description": "Handcrafted genuine leather bag",
                        "price": "$189.99",
                        "sale_price": "$149.99",
                        "discount_percent": "21%",
                        "product_url": f"{shop_url}/products/leather-messenger-bag",
                        "product_image_url": f"{shop_url}/media/products/bags/messenger-thumb.webp",
                    },
                ],
                "promo_code": "NOVEMBER20",
                "promo_discount": "20% off",
                "promo_description": "Use code NOVEMBER20 for 20% off your entire order",
                "promo_expires": "November 30, 2025",
                "promo_min_purchase": "$50.00",
                "blog_posts": [
                    {
                        "title": "Winter Fashion Trends 2025",
                        "excerpt": "Discover the hottest styles for the upcoming season...",
                        "post_url": f"{shop_url}/blog/winter-fashion-trends-2025",
                        "image_url": f"{shop_url}/media/blog/winter-trends-thumb.webp",
                    },
                ],
                "social_links": {
                    "facebook": "https://facebook.com/demostore",
                    "instagram": "https://instagram.com/demostore",
                    "twitter": "https://twitter.com/demostore",
                },
                "unsubscribe_url": f"{shop_url}/newsletter/unsubscribe?token=abc123",
                "preferences_url": f"{shop_url}/account/email-preferences",
                "view_in_browser_url": f"{shop_url}/newsletter/view/abc123",
            },
        }

        # Merge common and template-specific data
        data = {**common_data, **template_data.get(template_type, {})}
        return data

    @staticmethod
    def _get_name(language: str) -> str:
        """
        Get localized sample name

        Args:
            language: Language code

        Returns:
            Sample name appropriate for the language
        """
        names = {
            "en": "John Smith",
            "es": "Juan García",
            "fr": "Marie Dupont",
            "de": "Max Müller",
            "ja": "田中太郎",
            "pt": "João Silva",
            "zh-hans": "李明",
        }
        return names.get(language, "John Smith")

    @staticmethod
    def _get_site_settings_sample_data(shop_url: str, request=None) -> dict[str, str]:
        """
        Get site settings for sample data.

        Attempts to use actual SiteSettings values when available.
        Falls back to demo values if settings unavailable.

        Args:
            shop_url: Base shop URL for fallback
            request: Optional request for building absolute URLs

        Returns:
            Dict with shop_name, shop_url, support_email, support_phone, current_year
        """
        from django.utils import timezone

        try:
            from core.models import SiteSettings

            settings = SiteSettings.get_settings()

            # Build shop_url from request or settings
            if request:
                actual_shop_url = request.build_absolute_uri("/").rstrip("/")
            else:
                actual_shop_url = settings.site_url or shop_url

            return {
                "shop_name": settings.site_name or "Demo Store",
                "shop_url": actual_shop_url,
                "support_email": settings.get_support_email() or "support@example.com",
                "support_phone": settings.phone_number or "",
                "current_year": timezone.now().year,
            }
        except Exception:
            pass

        # Fallback to demo values
        from django.utils import timezone

        return {
            "shop_name": "Demo Store",
            "shop_url": shop_url,
            "support_email": "support@example.com",
            "support_phone": "+1 (555) 123-4567",
            "current_year": timezone.now().year,
        }

    @staticmethod
    def _get_site_logo_sample_data(shop_url: str, request=None) -> dict[str, str]:
        """
        Get site logo URLs for sample data.

        Attempts to use actual site settings logo if available.
        Falls back to empty strings if no logo configured.

        Args:
            shop_url: Base shop URL for constructing absolute URLs
            request: Optional request for building absolute URLs

        Returns:
            Dict with site_logo_url and size variants
        """
        # Try to get actual site logo
        try:
            from core.models import SiteSettings

            settings = SiteSettings.get_settings()

            if settings.site_logo:

                def make_absolute(url):
                    if not url:
                        return ""
                    if url.startswith("http"):
                        return url
                    if request:
                        return request.build_absolute_uri(url)
                    return f"{shop_url}{url}"

                return {
                    "site_logo_url": make_absolute(settings.get_site_logo_url("email")),
                    "site_logo_url_header": make_absolute(settings.get_site_logo_url("header")),
                    "site_logo_url_footer": make_absolute(settings.get_site_logo_url("footer")),
                    "site_logo_url_square": make_absolute(settings.get_site_logo_url("square")),
                }
        except Exception:
            pass

        # No logo configured - return empty strings
        return {
            "site_logo_url": "",
            "site_logo_url_header": "",
            "site_logo_url_footer": "",
            "site_logo_url_square": "",
        }

    @staticmethod
    def get_available_variables(template_type: str) -> list:
        """
        Get list of available variables for a template type

        Args:
            template_type: Template type

        Returns:
            List of variable names available for this template
        """
        sample_data = SampleDataProvider.get_sample_data(template_type)
        return list(sample_data.keys())
