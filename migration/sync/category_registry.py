"""
Sync Category Registry

Central registry defining all data categories available for sync and migration.
Each category specifies its models, serializer, dependencies, and feature availability.
"""

from collections import OrderedDict

from django.utils.translation import gettext_lazy as _

# Feature availability constants
FEATURE_BOTH = "both"  # Available in settings sync AND full migration
FEATURE_FULL_MIGRATION = "full_migration"  # Only available in full migration


SYNC_CATEGORIES = OrderedDict(
    [
        # ===================================================================
        # SETTINGS CATEGORIES (available in both settings sync and full migration)
        # ===================================================================
        (
            "site_settings",
            {
                "label": _("Site Settings"),
                "description": _(
                    "Core site configuration: name, branding, currency, checkout, SEO, maintenance"
                ),
                "models": ["core.SiteSettings"],
                "serializer": "migration.sync.serializers.site_settings.SiteSettingsSerializer",
                "sync_type": "singleton",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
                "has_files": True,  # logos, favicons
            },
        ),
        (
            "design_theme",
            {
                "label": _("Design & Theme"),
                "description": _("Active theme, design tokens, custom CSS, theme branding"),
                "models": [
                    "design.Theme",
                    "design.GlobalDesignSettings",
                    "design.DesignToken",
                    "design.CustomCSS",
                    "design.ThemeBranding",
                ],
                "serializer": "migration.sync.serializers.design_theme.DesignThemeSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "design",
                "has_files": True,  # theme package files, logos, favicons, OG images
            },
        ),
        (
            "design_layout",
            {
                "label": _("Headers, Footers & Menus"),
                "description": _("Header/footer templates, widgets, navigation menus"),
                "models": [
                    "design.HeaderTemplate",
                    "design.FooterTemplate",
                    "design.Widget",
                    "design.WidgetPlacement",
                    "design.Menu",
                    "design.MenuItem",
                ],
                "serializer": "migration.sync.serializers.design_layout.DesignLayoutSerializer",
                "sync_type": "collection",
                "dependencies": ["design_theme"],
                "feature": FEATURE_BOTH,
                "group": "design",
            },
        ),
        (
            "email_config",
            {
                "label": _("Email Configuration"),
                "description": _("Email provider accounts, templates, and template translations"),
                "models": [
                    "email_system.EmailAccount",
                    "email_system.EmailTemplate",
                    "email_system.EmailTemplateTranslation",
                ],
                "serializer": "migration.sync.serializers.email_config.EmailConfigSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "providers",
                "has_credentials": True,
            },
        ),
        (
            "sms_config",
            {
                "label": _("SMS & WhatsApp Configuration"),
                "description": _("SMS/WhatsApp provider accounts and message templates"),
                "models": ["sms_system.SMSProviderAccount", "sms_system.SMSTemplate"],
                "serializer": "migration.sync.serializers.sms_config.SMSConfigSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "providers",
                "has_credentials": True,
            },
        ),
        (
            "payment_providers",
            {
                "label": _("Payment Providers"),
                "description": _("Payment provider accounts (Stripe, PayPal, etc.)"),
                "models": ["payment_providers.PaymentProviderAccount"],
                "serializer": "migration.sync.serializers.payment_providers.PaymentProviderSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "providers",
                "has_credentials": True,
                "production_warning": _(
                    "Sandbox/test credentials will NOT be synced to production."
                ),
            },
        ),
        (
            "shipping_config",
            {
                "label": _("Shipping Configuration"),
                "description": _(
                    "Shipping providers, zones, methods, promotions, rate tables, packages, carrier presets, locations"
                ),
                "models": [
                    "shipping.ProviderAccount",
                    "shipping.ShippingZone",
                    "cart.ShippingMethod",
                    "shipping.ShippingPromotion",
                    "shipping.ShippingRateTable",
                    "shipping.ShippingPackage",
                    "shipping.CarrierPreset",
                    "shipping.Location",
                ],
                "serializer": "migration.sync.serializers.shipping_config.ShippingConfigSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "providers",
                "has_credentials": True,
                "has_files": True,  # carrier logos
            },
        ),
        (
            "tax_currency",
            {
                "label": _("Tax & Currency"),
                "description": _(
                    "Supported currencies, exchange rate providers, manual exchange rates"
                ),
                "models": [
                    "core.SupportedCurrency",
                    "exchange_rates.ExchangeRateProviderAccount",
                    "exchange_rates.ManualExchangeRate",
                ],
                "serializer": "migration.sync.serializers.tax_currency.TaxCurrencySerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
                "has_credentials": True,
            },
        ),
        (
            "tax_config",
            {
                "label": _("Tax Rates & Presets"),
                "description": _("Tax rates, tax preset groups and preset rates"),
                "models": [
                    "cart.TaxRate",
                    "cart.TaxPresetGroup",
                    "cart.TaxPresetRate",
                ],
                "serializer": "migration.sync.serializers.tax_config.TaxConfigSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "languages",
            {
                "label": _("Languages & Translations"),
                "description": _("Site languages, translation providers, UI translation overrides"),
                "models": [
                    "translations.SiteLanguage",
                    "translations.UITranslationOverride",
                    "translations.TranslationProvider",
                ],
                "serializer": "migration.sync.serializers.languages.LanguagesSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "blog_settings",
            {
                "label": _("Blog Settings"),
                "description": _("Blog configuration (posts per page, RSS, subscriptions)"),
                "models": ["blog.BlogSettings"],
                "serializer": "migration.sync.serializers.blog_settings.BlogSettingsSerializer",
                "sync_type": "singleton",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "social_sharing",
            {
                "label": _("Social Sharing"),
                "description": _("Social sharing button configuration and platform settings"),
                "models": ["social_sharing.SocialSharingSettings"],
                "serializer": "migration.sync.serializers.social_sharing.SocialSharingSerializer",
                "sync_type": "singleton",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "warehouse_config",
            {
                "label": _("Sales Regions & Warehouses"),
                "description": _(
                    "Sales regions, warehouse locations, and fulfillment configuration"
                ),
                "models": ["catalog.SalesRegion", "catalog.Warehouse"],
                "serializer": "migration.sync.serializers.warehouse_config.WarehouseConfigSerializer",
                "sync_type": "collection",
                "dependencies": ["shipping_config"],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "collections",
            {
                "label": _("Product Collections"),
                "description": _("Curated and automatic product collections"),
                "models": ["catalog.Collection"],
                "serializer": "migration.sync.serializers.collections.CollectionsSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "content",
                "has_files": True,  # collection images
            },
        ),
        (
            "commerce_rules",
            {
                "label": _("Commerce Rules"),
                "description": _(
                    "Vouchers, promotions, loyalty program, subscriptions, referral program"
                ),
                "models": [
                    "vouchers.VoucherCode",
                    "vouchers.VoucherRestriction",
                    "catalog.Promotion",
                    "loyalty.LoyaltyTier",
                    "loyalty.LoyaltyRule",
                    "loyalty.LoyaltyReward",
                    "loyalty.LoyaltyBadge",
                    "loyalty.LoyaltyCampaign",
                    "loyalty.LoyaltySegment",
                    "subscriptions.SubscriptionPlan",
                    "subscriptions.PlanAddon",
                ],
                "serializer": "migration.sync.serializers.commerce_rules.CommerceRulesSerializer",
                "sync_type": "collection",
                "dependencies": ["collections"],
                "feature": FEATURE_BOTH,
                "group": "commerce",
                "has_files": True,  # loyalty badge/reward images
            },
        ),
        (
            "webhooks_integrations",
            {
                "label": _("Webhooks & Integrations"),
                "description": _("Webhook endpoints and OAuth provider settings"),
                "models": ["webhooks.WebhookEndpoint", "accounts.OAuthProviderSettings"],
                "serializer": "migration.sync.serializers.webhooks.WebhooksSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
                "has_credentials": True,
            },
        ),
        (
            "custom_fields",
            {
                "label": _("Custom Fields"),
                "description": _("Custom field groups and field definitions"),
                "models": ["custom_fields.CustomFieldGroup", "custom_fields.CustomFieldDefinition"],
                "serializer": "migration.sync.serializers.custom_fields.CustomFieldsSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "staff_roles",
            {
                "label": _("Staff Roles"),
                "description": _("Staff role definitions and permissions"),
                "models": ["staff_roles.StaffRole"],
                "serializer": "migration.sync.serializers.staff_roles.StaffRolesSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "forms",
            {
                "label": _("Forms"),
                "description": _("Form builder forms and configurations"),
                "models": ["form_builder.Form"],
                "serializer": "migration.sync.serializers.forms.FormsSerializer",
                "sync_type": "collection",
                "dependencies": ["custom_fields"],
                "feature": FEATURE_BOTH,
                "group": "content",
            },
        ),
        (
            "page_content",
            {
                "label": _("Pages & Templates"),
                "description": _("Page builder pages, page templates, element templates"),
                "models": [
                    "page_builder.Page",
                    "page_builder.PageTemplate",
                    "page_builder.ElementTemplate",
                ],
                "serializer": "migration.sync.serializers.page_content.PageContentSerializer",
                "sync_type": "collection",
                "dependencies": ["design_theme"],
                "feature": FEATURE_BOTH,
                "group": "content",
                "has_files": True,  # page/template preview images
            },
        ),
        (
            "blog_content",
            {
                "label": _("Blog Posts & Categories"),
                "description": _("Blog posts, categories, and tags"),
                "models": ["blog.BlogPost", "blog.BlogCategory"],
                "serializer": "migration.sync.serializers.blog_content.BlogContentSerializer",
                "sync_type": "collection",
                "dependencies": ["blog_settings"],
                "feature": FEATURE_BOTH,
                "group": "content",
            },
        ),
        (
            "announcements",
            {
                "label": _("Announcements"),
                "description": _("Site announcements and notification banners"),
                "models": ["announcements.Announcement"],
                "serializer": "migration.sync.serializers.announcements.AnnouncementsSerializer",
                "sync_type": "collection",
                "dependencies": ["design_theme"],
                "feature": FEATURE_BOTH,
                "group": "content",
                "has_files": True,  # announcement images
            },
        ),
        (
            "search_config",
            {
                "label": _("Search Configuration"),
                "description": _("Search redirects and search settings"),
                "models": ["search.SearchRedirect"],
                "serializer": "migration.sync.serializers.search_config.SearchConfigSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "seo_providers",
            {
                "label": _("SEO Providers"),
                "description": _("SEO generator provider accounts and configuration"),
                "models": ["seo_generator.SEOProviderAccount"],
                "serializer": "migration.sync.serializers.seo_providers.SEOProvidersSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "providers",
                "has_credentials": True,
            },
        ),
        (
            "product_feed_providers",
            {
                "label": _("Product Feed Providers"),
                "description": _("Product feed provider accounts for Google Shopping, Meta, etc."),
                "models": ["product_feeds.FeedProviderAccount"],
                "serializer": "migration.sync.serializers.product_feed_providers.ProductFeedProvidersSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "providers",
                "has_credentials": True,
            },
        ),
        (
            "social_connectors",
            {
                "label": _("Blog Social Connectors"),
                "description": _("Social media connector accounts for blog auto-sharing"),
                "models": ["blog.SocialConnectorAccount"],
                "serializer": "migration.sync.serializers.social_connectors.SocialConnectorsSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "providers",
                "has_credentials": True,
                "production_warning": _(
                    "OAuth tokens will need to be re-authorized on the destination."
                ),
            },
        ),
        (
            "customer_analytics_config",
            {
                "label": _("Customer Analytics Configuration"),
                "description": _("Customer segments, LTV settings, and category multipliers"),
                "models": [
                    "customers.CustomerSegment",
                    "customers.LTVSettings",
                    "customers.ProductCategoryLTVMultiplier",
                ],
                "serializer": "migration.sync.serializers.customer_analytics_config.CustomerAnalyticsConfigSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "settings",
            },
        ),
        (
            "affiliate_config",
            {
                "label": _("Affiliate Program Configuration"),
                "description": _("Affiliate program settings, report settings, and programs"),
                "models": [
                    "affiliate.AffiliateSettings",
                    "affiliate.AffiliateReportSettings",
                    "affiliate.Program",
                ],
                "serializer": "migration.sync.serializers.affiliate_config.AffiliateConfigSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_BOTH,
                "group": "commerce",
            },
        ),
        (
            "pos_config",
            {
                "label": _("POS Configuration"),
                "description": _(
                    "Store groups, terminals, receipt templates, promo slides, staff discounts"
                ),
                "models": [
                    "pos_app.StoreGroup",
                    "pos_app.POSTerminalProvider",
                    "pos_app.POSTerminal",
                    "pos_app.ReceiptTemplate",
                    "pos_app.PromoSlide",
                    "pos_app.POSStaffDiscount",
                ],
                "serializer": "migration.sync.serializers.pos_config.POSConfigSerializer",
                "sync_type": "collection",
                "dependencies": ["warehouse_config"],
                "feature": FEATURE_BOTH,
                "group": "providers",
                "has_credentials": True,
                "has_files": True,  # promo slide images, receipt logos
            },
        ),
        # ===================================================================
        # FULL MIGRATION ONLY CATEGORIES
        # ===================================================================
        (
            "installed_components",
            {
                "label": _("Installed Components"),
                "description": _(
                    "Installed themes, provider integrations, and utility components with filesystem packages"
                ),
                "models": [
                    "component_updates.ComponentRegistry",
                    "component_updates.ComponentVersion",
                    "component_updates.ComponentDependency",
                ],
                "serializer": "migration.sync.serializers.installed_components.InstalledComponentsSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
                "has_files": True,
                "large_data": True,  # theme packages can be large
            },
        ),
        (
            "catalog",
            {
                "label": _("Products, Categories & Brands"),
                "description": _("Products, variants, images, categories, brands, attributes"),
                "models": [
                    "catalog.Category",
                    "catalog.Brand",
                    "catalog.Product",
                    "catalog.ProductVariant",
                    "catalog.ProductImage",
                    "catalog.ProductAttribute",
                    "catalog.AttributeValue",
                    "catalog.ProductAttributeAssignment",
                    "catalog.BundleItem",
                ],
                "serializer": "migration.sync.serializers.catalog.CatalogSerializer",
                "sync_type": "collection",
                "dependencies": ["custom_fields", "warehouse_config"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
                "has_files": True,  # product images, brand logos
            },
        ),
        (
            "media",
            {
                "label": _("Media Library"),
                "description": _("Media assets, thumbnails, and uploaded files"),
                "models": ["media_library.MediaAsset"],
                "serializer": "migration.sync.serializers.media.MediaSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
                "has_files": True,
                "large_data": True,  # chunked transfer required
            },
        ),
        (
            "customers",
            {
                "label": _("Customers & Addresses"),
                "description": _("Customer accounts, profiles, and addresses"),
                "models": [
                    "auth.User",
                    "accounts.CustomerProfile",
                    "accounts.CommunicationPreference",
                    "orders.Address",
                ],
                "serializer": "migration.sync.serializers.customers.CustomersSerializer",
                "sync_type": "collection",
                "dependencies": [],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "orders",
            {
                "label": _("Order History"),
                "description": _("Orders, order items, and transaction records"),
                "models": ["orders.Order", "orders.OrderItem"],
                "serializer": "migration.sync.serializers.orders.OrdersSerializer",
                "sync_type": "collection",
                "dependencies": ["customers", "catalog"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "reviews",
            {
                "label": _("Product Reviews"),
                "description": _("Product reviews and ratings"),
                "models": ["catalog.ProductReview"],
                "serializer": "migration.sync.serializers.reviews.ReviewsSerializer",
                "sync_type": "collection",
                "dependencies": ["catalog", "customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "inventory",
            {
                "label": _("Stock Levels"),
                "description": _(
                    "Per-warehouse stock quantities, reserved stock, and reorder points"
                ),
                "models": ["catalog.StockItem"],
                "serializer": "migration.sync.serializers.inventory.InventorySerializer",
                "sync_type": "collection",
                "dependencies": ["warehouse_config", "catalog"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "digital_products",
            {
                "label": _("Digital Products & Licenses"),
                "description": _(
                    "Digital assets, license key templates, license pools, license providers"
                ),
                "models": [
                    "catalog.DigitalAsset",
                    "catalog.LicenseKeyTemplate",
                    "catalog.LicensePool",
                    "catalog.LicenseProvider",
                ],
                "serializer": "migration.sync.serializers.digital_products.DigitalProductsSerializer",
                "sync_type": "collection",
                "dependencies": ["catalog"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
                "has_files": True,  # digital asset files
                "has_credentials": True,  # license provider API keys
            },
        ),
        (
            "gift_cards",
            {
                "label": _("Gift Cards & Voucher Usage"),
                "description": _("Gift card balances, transactions, voucher usage records"),
                "models": [
                    "catalog.GiftCard",
                    "catalog.GiftCardTransaction",
                    "vouchers.VoucherUsage",
                    "vouchers.AppliedVoucher",
                ],
                "serializer": "migration.sync.serializers.gift_cards.GiftCardsSerializer",
                "sync_type": "collection",
                "dependencies": ["commerce_rules", "catalog", "customers", "orders"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "wallet",
            {
                "label": _("Store Credit & Wallets"),
                "description": _("Customer wallet balances and transaction history"),
                "models": ["wallet.CustomerWallet", "wallet.WalletTransaction"],
                "serializer": "migration.sync.serializers.wallet.WalletSerializer",
                "sync_type": "collection",
                "dependencies": ["customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "loyalty_members",
            {
                "label": _("Loyalty Program Members"),
                "description": _(
                    "Loyalty members, points balances, transactions, redemptions, badges"
                ),
                "models": [
                    "loyalty.LoyaltyMember",
                    "loyalty.LoyaltyBalance",
                    "loyalty.LoyaltyTransaction",
                    "loyalty.LoyaltyRedemption",
                    "loyalty.LoyaltyMemberBadge",
                    "loyalty.LoyaltyCampaignExecution",
                    "loyalty.LoyaltySegmentMembership",
                ],
                "serializer": "migration.sync.serializers.loyalty_members.LoyaltyMembersSerializer",
                "sync_type": "collection",
                "dependencies": ["commerce_rules", "customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "subscriptions_active",
            {
                "label": _("Active Subscriptions"),
                "description": _(
                    "Subscription plans pricing, active subscriptions, billing cycles, payment tokens"
                ),
                "models": [
                    "subscriptions.PlanPricingTier",
                    "subscriptions.CustomerSubscription",
                    "subscriptions.CustomerSubscriptionAddon",
                    "subscriptions.SubscriptionDiscount",
                    "subscriptions.BillingCycleLog",
                    "subscriptions.PaymentToken",
                ],
                "serializer": "migration.sync.serializers.subscriptions_active.SubscriptionsActiveSerializer",
                "sync_type": "collection",
                "dependencies": ["commerce_rules", "customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
                "has_credentials": True,  # payment tokens
                "production_warning": _(
                    "Payment tokens may not be valid across different payment provider installations."
                ),
            },
        ),
        (
            "shipments",
            {
                "label": _("Shipments & Tracking"),
                "description": _("Shipment records and tracking event history"),
                "models": ["shipping.Shipment", "shipping.TrackingEvent"],
                "serializer": "migration.sync.serializers.shipments.ShipmentsSerializer",
                "sync_type": "collection",
                "dependencies": ["orders", "shipping_config"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "refunds_returns",
            {
                "label": _("Refunds, Returns & Order Notes"),
                "description": _("Refund records, return requests, and order notes"),
                "models": ["orders.Refund", "orders.ReturnRequest", "orders.OrderNote"],
                "serializer": "migration.sync.serializers.refunds_returns.RefundsReturnsSerializer",
                "sync_type": "collection",
                "dependencies": ["orders", "customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "wishlists",
            {
                "label": _("Customer Wishlists"),
                "description": _("Customer wishlists and wishlist items"),
                "models": ["cart.Wishlist", "cart.WishlistItem"],
                "serializer": "migration.sync.serializers.wishlists.WishlistsSerializer",
                "sync_type": "collection",
                "dependencies": ["customers", "catalog"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "blog_subscribers",
            {
                "label": _("Blog Subscribers"),
                "description": _("Blog email subscribers and category subscriptions"),
                "models": ["blog.BlogSubscriber"],
                "serializer": "migration.sync.serializers.blog_subscribers.BlogSubscribersSerializer",
                "sync_type": "collection",
                "dependencies": ["blog_content", "customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "form_submissions",
            {
                "label": _("Form Submissions"),
                "description": _("Form response data and submission history"),
                "models": ["form_builder.FormResponse"],
                "serializer": "migration.sync.serializers.form_submissions.FormSubmissionsSerializer",
                "sync_type": "collection",
                "dependencies": ["forms", "customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "customer_analytics",
            {
                "label": _("Customer Analytics & History"),
                "description": _("Customer notes, abandoned carts, cohort data, preference logs"),
                "models": [
                    "customers.CustomerNote",
                    "customers.AbandonedCart",
                    "customers.CustomerCohort",
                    "customers.CohortMetrics",
                    "accounts.PreferenceChangeLog",
                ],
                "serializer": "migration.sync.serializers.customer_analytics.CustomerAnalyticsSerializer",
                "sync_type": "collection",
                "dependencies": ["customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "affiliate_data",
            {
                "label": _("Affiliate Member Data"),
                "description": _(
                    "Affiliate accounts, program memberships, links, commissions, payouts"
                ),
                "models": [
                    "affiliate.Affiliate",
                    "affiliate.AffiliateProgramMembership",
                    "affiliate.Link",
                    "affiliate.Commission",
                    "affiliate.Payout",
                ],
                "serializer": "migration.sync.serializers.affiliate_data.AffiliateDataSerializer",
                "sync_type": "collection",
                "dependencies": ["affiliate_config", "customers", "orders"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "pos_transactions",
            {
                "label": _("POS Transaction History"),
                "description": _("POS shifts, cash movements, payments, and parked carts"),
                "models": [
                    "pos_app.POSShift",
                    "pos_app.CashMovement",
                    "pos_app.POSPayment",
                    "pos_app.ParkedCart",
                ],
                "serializer": "migration.sync.serializers.pos_transactions.POSTransactionsSerializer",
                "sync_type": "collection",
                "dependencies": ["pos_config", "customers", "orders"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        (
            "license_keys",
            {
                "label": _("Software License Keys"),
                "description": _("License keys, activations, and device registrations"),
                "models": ["catalog.LicenseKey", "catalog.LicenseActivation"],
                "serializer": "migration.sync.serializers.license_keys.LicenseKeysSerializer",
                "sync_type": "collection",
                "dependencies": ["digital_products", "orders", "customers"],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
            },
        ),
        # ===================================================================
        # SPECIAL CATEGORIES
        # ===================================================================
        (
            "platform_license",
            {
                "label": _("Platform License"),
                "description": _("Platform license transfer and EULA acceptance history"),
                "models": ["core.LicenseAcceptanceRecord"],
                "serializer": "migration.sync.serializers.platform_license.PlatformLicenseSerializer",
                "sync_type": "special",
                "dependencies": [],
                "feature": FEATURE_FULL_MIGRATION,
                "group": "data",
                "requires_update_server": True,
                "production_warning": _(
                    "This will deactivate the license on the source installation. "
                    "The source installation will stop working after transfer."
                ),
            },
        ),
    ]
)


# Groups for UI display
CATEGORY_GROUPS = OrderedDict(
    [
        (
            "settings",
            {
                "label": _("Settings"),
                "icon": "fas fa-cog",
                "description": _("Core site settings, currencies, languages"),
            },
        ),
        (
            "design",
            {
                "label": _("Design"),
                "icon": "fas fa-palette",
                "description": _("Theme, layout, menus, widgets"),
            },
        ),
        (
            "providers",
            {
                "label": _("Providers"),
                "icon": "fas fa-plug",
                "description": _("Email, SMS, payment, shipping providers"),
            },
        ),
        (
            "commerce",
            {
                "label": _("Commerce"),
                "icon": "fas fa-shopping-cart",
                "description": _("Vouchers, promotions, loyalty, subscriptions"),
            },
        ),
        (
            "content",
            {
                "label": _("Content"),
                "icon": "fas fa-file-alt",
                "description": _("Pages, blog posts, forms"),
            },
        ),
        (
            "data",
            {
                "label": _("Data"),
                "icon": "fas fa-database",
                "description": _("Products, customers, orders, media"),
            },
        ),
    ]
)


def get_categories_for_feature(feature_type):
    """
    Get categories available for a specific feature type.

    Args:
        feature_type: 'settings_sync' or 'full_migration'

    Returns:
        OrderedDict of category_key -> category_config
    """
    result = OrderedDict()
    for key, config in SYNC_CATEGORIES.items():
        if feature_type == "settings_sync" and config["feature"] == FEATURE_FULL_MIGRATION:
            continue
        result[key] = config
    return result


def get_categories_grouped(feature_type):
    """
    Get categories grouped by their UI group for a feature.

    Returns:
        OrderedDict of group_key -> {label, icon, categories: [...]}
    """
    categories = get_categories_for_feature(feature_type)
    grouped = OrderedDict()

    for group_key, group_config in CATEGORY_GROUPS.items():
        group_categories = OrderedDict()
        for cat_key, cat_config in categories.items():
            if cat_config.get("group") == group_key:
                group_categories[cat_key] = cat_config
        if group_categories:
            grouped[group_key] = {
                **group_config,
                "categories": group_categories,
            }

    return grouped


def resolve_dependencies(selected_categories):
    """
    Topologically sort selected categories by their dependencies.
    Also adds any missing dependency categories.

    Args:
        selected_categories: list of category keys

    Returns:
        list: Ordered category keys (dependencies first)
    """
    # Build full set including dependencies
    required = set(selected_categories)
    added = True
    while added:
        added = False
        for cat_key in list(required):
            config = SYNC_CATEGORIES.get(cat_key, {})
            for dep in config.get("dependencies", []):
                if dep not in required:
                    required.add(dep)
                    added = True

    # Topological sort (Kahn's algorithm)
    in_degree = dict.fromkeys(required, 0)
    for cat_key in required:
        config = SYNC_CATEGORIES.get(cat_key, {})
        for dep in config.get("dependencies", []):
            if dep in required:
                in_degree[cat_key] = in_degree.get(cat_key, 0) + 1

    queue = [k for k in required if in_degree[k] == 0]
    result = []

    while queue:
        # Sort for deterministic order
        queue.sort()
        node = queue.pop(0)
        result.append(node)

        # Find categories that depend on this node
        for cat_key in required:
            config = SYNC_CATEGORIES.get(cat_key, {})
            if node in config.get("dependencies", []):
                in_degree[cat_key] -= 1
                if in_degree[cat_key] == 0:
                    queue.append(cat_key)

    return result
