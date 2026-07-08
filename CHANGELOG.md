# Changelog

All notable changes to the Spwig eCommerce Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.7] - 2026-07-05

### Fixed

- **Installed provider component versions didn't take effect until a container
  restart** — Installing a new version of a payment / shipping / email / any
  integration component wrote the new files to disk and the registry logged
  "Loaded provider" as if the reload succeeded, but the running workers kept
  executing the previous version's code. Merchants had to `docker restart`
  the shop to actually apply the fix they'd just installed. Root cause was in
  the module loader: after re-importing the component's package, Python's
  import machinery kept the previous version's submodules cached in
  `sys.modules`. When the package's `__init__.py` did `from .provider import X`,
  Python returned the stale submodule and the registry bound the old class.
  The loader now purges the whole package subtree from `sys.modules` before
  re-import, so the new code takes effect on the next request. Fix lives in
  the shared `component_updates.integration_paths.import_component_module`
  helper; the payment, shipping, and POS terminal registries now delegate to
  it so all provider types share the fix.

---

## [1.5.6] - 2026-06-30

### Fixed

- **Embedded card payments (Stripe PaymentElement, Adyen Components, etc.)
  crashed with a database error at checkout** — Headless storefronts that
  use a provider's embedded card UI (rather than a redirect to a hosted
  payment page) call `POST /api/payments/intents/` to set up the payment.
  Providers correctly return no `checkout_url` for the embedded path —
  there is no hosted page to redirect to. The orchestrator was persisting
  that explicit absence as `null` into a non-nullable column, producing a
  500 the moment the customer hit "Pay". Storefronts using
  redirect-based flows (Stripe Checkout hosted, PayPal, etc.) were
  unaffected. Now coalesced to an empty string for `checkout_url`,
  `client_secret`, `provider_intent_id`, `action_type`, and `action_url`
  — defensive against any provider that returns explicit `None`.

---

## [1.5.5] - 2026-06-28

### Added

- `applied_gift_cards` and `gift_card_discount_amount` on the cart API response,
  so headless storefronts can render gift-card chips and persist them across
  page reloads without re-calling the apply endpoint.
- `publishable_key` on the payment provider API response. Headless storefronts
  can now initialise Stripe (and Revolut) from the merchant's stored
  credentials at runtime instead of baking the key into the build. Server-side-only
  providers (Airwallex, PayPal, Square) return `null`.

## [1.5.4] - 2026-06-27

### Added

- **Voucher CSV/XLSX import wizard** — Merchants can now bulk-load voucher codes from a CSV or Excel file via a new two-step wizard on the Voucher Codes admin. Pick the discount settings once for the whole batch, map the file's columns to voucher fields (auto-detected for common header names like "Code", "Voucher Code", "Member ID"), and choose what to do about duplicates: skip them, overwrite their settings, or fail the import. Hard caps of 5 MB and 5 000 rows per batch keep the experience snappy. Motivated by loyalty programme partners who send monthly Excel files of pre-generated birthday codes
- **Voucher export to XLSX** — A new "Export to XLSX" action alongside the existing CSV export. Both formats now produce the same round-trip-compatible column shape, so you can export, edit in a spreadsheet, and re-import without losing fields

### Fixed

- **Payment provider configuration could leave merchants stranded** — Two related traps tripped on a fresh Stripe install today. First, the connection wizard saved the provider account but never synced its payment methods, so checkout silently returned no providers ("Loading payment options…" forever on the storefront). The wizard now syncs methods automatically the moment the account is saved; failures surface as a clear warning with a link to the manual sync action. Second, if a provider's installed files vanished (e.g. after a Docker volume reset) the registry row hung around as an "installed but invisible" ghost — selecting "Install" would short-circuit on the orphan row. The install endpoint now detects missing files and re-downloads, and the provider wizard shows a "Reinstall" button next to any provider whose package is missing
- **Selecting Stripe (or any provider by slug) returned a 500 at checkout** — The checkout payment-method endpoint crashed with a database error whenever a customer picked a provider by slug. Customers couldn't progress past the payment step. Now resolves correctly
- **No payment providers appeared at checkout if shipping countries hadn't been configured** — The shipping zone admin lets merchants declare delivery regions, but the platform was also reading a separate (unsurfaced) "shipping countries" table to decide which payment providers a customer could see. Saving a shipping zone now keeps both in sync automatically, so merchants only need to think about zones. Existing zones are reconciled on upgrade
- **Payment method sync command misreported success** — `manage.py sync_payment_methods` synced methods correctly but the summary line at the end said "Successfully synced: 0, Failed: 1" due to a cosmetic counter bug. The summary now matches reality

## [1.5.3] - 2026-06-27

### Fixed

- **Affiliate portal had no obvious way for existing affiliates to log in** — Returning affiliates landing on the affiliate portal page only saw a small login icon in the navigation. The hero and CTA buttons branched on three states and the fall-through case (logged-in non-affiliate visitors, e.g. a storefront admin who was inspecting the portal) showed no action button at all. The portal now always shows an "Affiliate Login" button alongside the registration CTA for anyone who isn't already an affiliate, taking the visitor straight to their dashboard after sign-in

## [1.5.2] - 2026-06-27

### Fixed

- **Discounted products were added to the cart at full price** — Products on sale via a percentage discount, fixed amount off, or fixed sale price would show the discount on the product page, but the cart and checkout charged the original price. Items added to the cart now correctly use the sale price, the cart subtotal reflects the discount, and the `savings` line on each item shows how much the customer is saving. Variants that inherit pricing from the parent product also benefit from product-level sales

## [1.5.1] - 2026-06-01

### Fixed

- **Cart and checkout responses cached by Cloudflare** — Storefronts behind Cloudflare APO could see stale cart data: reducing a quantity worked on the server but the UI immediately reverted to the previous value because the next read came back from Cloudflare's edge cache. Cart, checkout, account, and other per-visitor API endpoints now send strict `Cache-Control: private, no-store` headers so no shared cache will store the response. Customers will see immediate, accurate updates after every change
- **Mini-cart items missing product name and image on headless storefronts** — Items appeared as bare quantity/price rows with no name, no image, and no working remove button. The platform's cart API was returning product details nested under a `product` object, but the headless SDK reads them as flat fields. Cart items now expose `product_name`, `product_slug`, `product_image`, `variant_name`, `sku`, and `currency` alongside the existing nested structure, restoring the mini-cart's expected rendering

## [1.5.0] - 2026-06-01

### Fixed

- **Mini cart not updating after add-to-cart on headless storefronts** — Adding a product on a headless storefront (e.g. via the Spwig React SDK) could show the "added to bag" message but leave the mini cart and cart page empty. The underlying issue was that the platform could accumulate duplicate cart rows for the same anonymous visitor — silently created by concurrent page loads, currency middleware, or checkout sync — and subsequent reads would return whichever empty cart PostgreSQL handed back first. Items were never lost on the server, but customers couldn't see them. Now the database enforces one cart per anonymous session, and any pre-existing duplicates are merged automatically on the next visit

### Housekeeping

- **Cart database migration** — A one-off `cart/migrations/0006_consolidate_duplicate_carts.py` consolidates any historical duplicate carts on existing installations before the new constraint is added. No merchant action required — runs automatically on the next deploy

## [1.4.4] - 2026-05-12

### Improved

- **Checkout response shape** — The checkout session endpoint now wraps responses in a consistent `{success, session}` envelope, matching the rest of the headless SDK contract
- **Shipping method details at checkout** — Customers now see description, method type, delivery time estimates, and an icon for each shipping option, not just the name and price
- **Payment provider selection flexibility** — Headless storefronts can now identify a payment provider by either its UUID or its slug (e.g. `stripe`, `paypal`), making integration simpler

### Fixed

- **Shipping promotions ignored in final checkout total** — Free shipping thresholds and percentage discounts were correctly evaluated but the final shipping cost shown to the customer used the base method price. Promotions are now applied to the total
- **Billing address validation** — Billing address submission now properly validates required fields and accepts blank values for optional fields (company, address line 2, state, phone), matching the shipping address behaviour
- **Shipping method auto-restore at checkout** — When returning to a checkout session, the previously-selected shipping method is now correctly restored

### Housekeeping

- **Removed debug output** — Stray `print()` statements were removed from the payment provider serializer

## [1.4.3] - 2026-05-11

### Fixed

- **Checkout failed for city-state addresses** — Submitting a shipping address with an empty state field (common for city-states like Singapore, Monaco) returned a 400 error. The platform now accepts blank state values, matching how other optional address fields already behaved

## [1.4.2] - 2026-05-11

### Fixed

- **Checkout crash when state field omitted** — Submitting a shipping address without a state field at all (rather than as a blank string) caused an internal error. The state field is now treated as truly optional

## [1.4.1] - 2026-05-11

### Fixed

- **Pickup location API broken** — The pickup location API returned a 500 error due to a mismatch between the serializer and the underlying Location model fields. Merchants using local pickup as a fulfilment option can now retrieve their pickup locations correctly

## [1.4.0] - 2026-05-04

### Changed

- **Shipping Rules renamed to Shipping Promotions** — The "Shipping Rules" system has been renamed to "Shipping Promotions" throughout the platform to better reflect their purpose. Promotions modify shipping costs (free shipping, discounts, overrides) while Shipping Methods define the actual delivery options. All admin pages, wizards, and help content have been updated
- **Shipping Method types simplified** — Removed redundant method types `free_shipping` (use flat rate with $0 cost), `weight_based`, and `price_based` (use table rate instead). This reduces confusion when setting up shipping
- **Admin sidebar reorganised** — Shipping configuration (Methods, Zones, Promotions, Rate Tables) and Fulfillment operations (Shipments, Providers) are now in separate sidebar groups for clearer navigation

### Improved

- **Shipping cost calculation** — Checkout now correctly applies shipping promotions to the shipping cost. Previously, promotions were evaluated but the final cost sent to the customer used the base method cost only
- **Shipping Method admin** — The method edit page now shows an inline rate table editor and an active promotions tab, giving merchants a complete view of how a method is configured without navigating away
- **Shipping Promotion visibility control** — Promotions can now control whether a shipping method is shown or hidden at checkout (e.g., hide express shipping for orders under $50)

### Fixed

- **Promotion wizard step 5 crash** — The review step of the promotion creation wizard no longer fails with a 500 error when displaying the promotion type summary

### Housekeeping

- **Removed redundant eligibility fields** — `min_order_value`, `max_order_value`, `min_weight`, and `max_weight` have been removed from Shipping Methods. These conditions now live exclusively on Shipping Promotions, eliminating the confusion of having eligibility rules in two places
- **Pending migrations** — Included migrations for component_updates, customizable_product, domain_ssl, email_system, enterprise_sso, and payment_providers

## [1.3.11] - 2026-05-02

### Improved

- **Headless Frontend Compatibility** — Headless storefronts running on the same domain as the Spwig backend now work seamlessly. Previously, API write operations (add to cart, checkout, form submissions, etc.) could fail with a 403 error when the browser had an active admin session. This affected all merchants using a custom frontend hosted on the same domain as their store
- **Category API Pagination** — The category tree API now supports fetching the complete category hierarchy in a single request, making it easier for headless storefronts to build navigation menus without multiple paginated calls

### Fixed

- **Admin Currency Display** — The admin product editor now correctly shows each product's stored currency rather than always defaulting to the site currency. Products imported with a different currency (e.g. SGD) no longer silently display as the site default until saved
- **Media Library Scroll** — Clearing a search in the media library no longer breaks infinite scroll, requiring a page reload to browse further
- **Promotion Wizard** — The promotion creation wizard no longer fails to save in certain stacking configurations
- **Theme Activation** — Fixed a symlink issue that could prevent newly activated themes from taking effect immediately

### Housekeeping

- **Theme CSS Variables** — Replaced hardcoded color values across page builder CSS with theme token variables for consistent theming

## [1.3.10] - 2026-04-11

### Added

- **Guest Share Tracking** — Anonymous visitors (not logged in) can now contribute to your social share analytics. Previously, only logged-in customers' share clicks were recorded, which excluded the majority of real storefront traffic. Your admin dashboard will now show a more complete picture of which products, categories, and blog posts are being shared
- **Search Click Attribution for Headless Stores** — Headless and custom storefronts can now properly attribute search result clicks back to the originating search query. This enables click-through-rate analytics in the admin dashboard for any merchant running a custom frontend on top of the Spwig API

### Improved

- **Search Content Type Handling** — Admin search click tracking now accepts simpler content type names (e.g., `product` instead of `catalog.product`), making it easier to integrate third-party storefronts with search analytics
- **Search Content Type Determinism** — When installations have third-party provider packages that register models with the same name as Spwig's built-in models, search click tracking now consistently resolves to the correct first-party model every time
- **Share Target Validation** — Social share tracking now verifies that the referenced product, category, or blog post actually exists before recording the share, preventing dangling entries in your analytics from typos or stale frontend code

### Fixed

- **Search Analytics Spam Protection** — Search query tracking now correctly rejects queries below the configured minimum length, preventing analytics pollution from accidental short-query spam
- **Unnecessary Session Creation** — When search query tracking is disabled in your settings, the platform no longer creates unneeded visitor session records as a side effect of search requests

### Security

- **Content Type Whitelist for Share Tracking** — Both the existing authenticated share tracking endpoint and the new anonymous endpoint now strictly limit share events to public storefront content (products, categories, brands, collections, blog posts, pages). This prevents abuse attempts to create share records against internal models like users or admin records
- **Strict Rate Limiting for Guest Share Tracking** — The new anonymous share tracking endpoint is rate-limited to 20 requests per hour per IP address, substantially stricter than the 50/hour limit for authenticated users, to prevent spam and database pollution from guest-level access

---

## [1.3.9] - 2026-04-09

### Fixed

- **Store Currency Not Applied to New Records** — Fixed an issue where all price fields defaulted to USD regardless of the merchant's configured default currency. Merchants who set their store currency to EUR, GBP, SGD, or any other currency will now see it correctly applied when creating new products, orders, and other records through the admin or import wizards
- **Import Wizard Currency** — WooCommerce, Shopify, and Magento import wizards now use the merchant's configured store currency as the fallback instead of hardcoding USD when the source platform doesn't specify a currency
- **Admin Currency Dropdown Default** — When creating new products, vouchers, shipping rules, and other items in the admin, the currency dropdown now defaults to the merchant's store currency instead of USD

### Added

- **Bulk Currency Update Command** — New `manage.py fix_currency_defaults` management command allows merchants to bulk-update existing records from one currency to another. Includes `--dry-run` mode to preview changes before applying them
- **Currency Change Warning** — Changing the default currency in Site Settings now logs a warning with instructions for updating existing records, helping merchants avoid mixed-currency data

---

## [1.3.8] - 2026-04-09

### Added

- **Category API Translations** — The category detail API now returns translated content (name, description, meta title, meta description) based on the visitor's language, matching the existing product detail translation behaviour. Headless storefronts and third-party integrations receive fully translated category data without additional work
- **Configurator Translations** — Product configurator slot names, descriptions, and preset names are now returned in the visitor's language via the storefront API. Merchants who have translated their configurator content will see it served automatically
- **Multi-Subscription Account Portal** — Merchants with multiple subscriptions (e.g., agencies) can now manage each subscription independently from their account dashboard, including separate billing history, payment methods, and license details

### Improved

- **Translation Language Fallback** — All translation logic now falls back to the merchant's configured default store language instead of assuming English. Merchants operating in non-English primary languages will see correct content when a visitor's preferred language has no translation available
- **Product Description API Reliability** — Products with descriptions entered in the admin but not yet processed by the Translation Service now correctly return their descriptions via the catalog API instead of empty strings
- **Email Language Accuracy** — Digital product delivery emails, back-in-stock notifications, and payment error alerts now respect the merchant's default language and customer language preferences instead of defaulting to English
- **Accept-Language Header Parsing** — API requests with quality-weighted Accept-Language headers (e.g., `en;q=0.5,fr;q=0.9`) now correctly select the highest-priority language instead of always using the first entry
- **Blog Category SEO Translations** — Blog category detail API responses now include translated meta titles and meta descriptions when available, improving SEO for multi-language blogs

### Fixed

- **Category Hierarchy After Import** — Fixed an issue where parent categories could become invisible after a WooCommerce, Magento, or CSV import, causing child categories to appear as orphans in the storefront navigation
- **Migration Preview Errors** — Fixed WooCommerce import preview crashing when product data used different field names than expected

---

## [1.3.7] - 2026-04-01

### Added

- **Custom Domain Support** (Hosted) — Hosted merchants can now connect their own domain name to their store. Available in the setup wizard and under Domain Settings in the admin. Includes guided DNS setup with ownership verification, automatic SSL provisioning via Cloudflare, and the ability to switch back to the default subdomain at any time
- **Hosted Upgrade Scheduling** — Hosted merchants can now view available platform updates and schedule upgrades from the admin dashboard, with real-time progress tracking
- **Company Field on License Checkout** — Self-hosted license purchase form now collects company name

### Improved

- **Payment Method Configuration** — Payment methods are now configured independently from shipping countries, giving merchants full global control over which payment methods are available in each country regardless of whether they ship there
- **SSL Configuration** (Hosted) — Hosted stores no longer show the "SSL not configured" warning in the admin dashboard. SSL is automatically configured as managed externally during store setup
- **Faster Deployments** — New incremental static file collection reduces container startup time from 3-5 minutes to under 10 seconds for hosted instances

---

## [1.3.6] - 2026-03-31

### Added

- **Per-Country Payment Methods** — Payment providers now support configuring which payment methods are available in each country, giving merchants fine-grained control over checkout options by region
- **Hosted Auto-Activation** — New hosted store instances now activate automatically on first boot, removing the manual setup step for merchants

### Improved

- **Payment Provider Management** — The provider toggle button on the payment providers list now works correctly. The provider edit page includes a "Configure Payment Methods" card with sync, enable-all, and disable-all controls
- **Hosted Provisioning Reliability** — Checkout and provisioning pipeline hardened with automatic retries, better error handling, and email notifications if provisioning fails
- **System Upgrade Reconnection** — Fixed an issue where the upgrade progress page would not reconnect after a system restart, leaving merchants stuck on "reconnecting" indefinitely

### Fixed

- **Security Hardening** — Domain allowlist on return URLs prevents open redirects. Credential decryption now fails fast on errors instead of silently falling through. Locale detection supports all language codes including regional variants like zh-hans

---

## [1.3.5] - 2026-03-30

### Improved

- **Admin List Filters** — Fixed an issue where admin list filters were unresponsive across multiple sections of the admin panel. Filters now work correctly in all supported languages
- **Payment Provider Setup** — The payment provider configuration page now displays your webhook endpoint URL (with one-click copy), shows whether the account is in test or live mode, and provides direct links to provider signup and credentials management
- **Help Content** — Expanded and refreshed help documentation with updated translations across all 17 supported languages
- **Email Template Translations** — Wording and grammar refinements across hosted and developer email templates in all supported languages

---

## [1.3.4] - 2026-03-26

### Added

- **Page-Level Visitor Analytics** — Per-URL tracking with a dedicated admin dashboard showing page views, unique visitors, and trends for individual pages
- **Blog Translation Support** — Blog posts, categories, and tags can now be translated via the Translation Service API
- **13 New Help Topics** — Comprehensive documentation added for 3D Configurator, Bookable Products, License Key Management, Price Charming, Product Attributes, Product Brands, Product Collections, Product Reviews, Product Tags, Sales Regions, Stock Notifications, API Tokens, and Payment Transactions — all available in 17 languages

### Improved

- **Company Name on License** — License status page now shows the company name alongside the owner for business accounts
- **Platform Upgrade Resilience** — Upgrade UI now handles container recreation gracefully, maintaining progress visibility during restarts
- **Safari Admin Layout** — Fixed layout gap caused by 100vw-based width calculations in Safari
- **Help Content** — Updated documentation for product management, orders, accounts, loyalty, store settings, customer analytics, and more
- **Email Template Translations** — Wording and grammar refinements across all hosted and developer email templates in 17 languages

---

## [1.3.3] - 2026-03-23

### Added

- **Configurable Device Limit** — Merchants can set the maximum number of trusted devices per staff user from Site Settings (Security tab)
- **Staff Profile** — Staff users can view their profile, manage trusted devices, and revoke sessions from the admin header menu

### Improved

- **Hotfix System** — Hotfix apply now shows a full progress modal with live step tracking, log output, and restart warning. Post-install verification runs automatically after applying hotfixes, with automatic rollback if verification fails
- **Admin Notification Badges** — Badge counts now cover 7 additional merchant-actionable items; badges use error color tokens for better visibility

---

## [1.3.2] - 2026-03-23

### Added

- **Hosted Subscription Management** — Customers with hosted stores can manage their subscription from the account dashboard: view plan details, change billing interval, update payment method, cancel, undo cancellation, and reactivate
- **Hosted Store Email Notifications** — Full lifecycle email coverage including subscription confirmation, payment receipts, payment failure alerts, cancellation/reactivation confirmations, suspension warnings, onboarding drip series (day 3, 7, 14), and more — all in 17 languages
- **Hourly Sales Analytics** — Per-hour revenue breakdown for granular sales insights
- **Product Sales Tracking** — Products now track total sales count, and customer metrics are updated on order payment
- **Wishlist API Documentation** — OpenAPI schema docs for the wishlist product-ids endpoint

### Improved

- **Admin Messages** — Messages now support sorting, filtering, and per-user read tracking
- **Country & Currency Defaults** — Store uses merchant-configured country and currency defaults instead of hardcoded US/USD fallbacks
- **Store Name Suggestions** — When a hosted store name is unavailable, the system suggests up to 5 alternative names using suffix, prefix, and numbered variants
- **Email Template Translations** — Wording and grammar improvements across 17 languages for existing email templates

---

## [1.3.1] - 2026-03-21

### Added

- **Message Threading** — Customer messages now support multi-turn conversations. Merchants and customers can exchange multiple replies within the same message thread, making it easier to follow and resolve enquiries
- **Email Template Translations in Language Packs** — Language packs now include translated email templates, so installing a language pack automatically translates all system emails (order confirmations, shipping notifications, etc.) into that language

### Improved

- **Magento Migration** — Improved image import with deduplication, WebP generation, and thumbnail presets. Added automatic rewriting of old-store content links, better error handling, and SSL verification support
- **Hotfix System** — Hotfixes are now independent patches applied in sequence, ensuring no fixes are missed when multiple hotfixes are available. The admin interface shows individual hotfix details with a single "Apply All" action
- **Faster Static File Collection** — Smart file finders skip unnecessary files during static collection, reducing the number of files processed by 45%
- **Platform Updates** — Update progress modal now includes a close button on failure, and the update process has been streamlined

### Fixed

- Magento migration connection test error when validating credentials
- Platform update modal getting stuck open on failure or rollback
- Analytics API response consistency improvements

---

## [1.3.0] - 2026-03-20

### Added

- **Magento 2 Migration** — Migrate products, categories, customers, orders, reviews, and coupons from Magento 2 / Adobe Commerce stores via the REST API, with a guided connection wizard and data preview
- **Product Tags** — Lightweight tagging system for product organization and filtering, distinct from collections
- **Scheduled Emails** — Queue emails for delayed delivery, enabling workflows like onboarding tips sent 24 hours after store setup
- **Language Packs** — Install additional admin languages beyond the built-in 16 via the Spwig marketplace
- **Spwig-to-Spwig Sync** — Transfer settings, themes, and configuration between Spwig installations using sync tokens
- **Spwig Hosted Mail Provider** — Built-in hosted email provider with instance provisioning
- **Hosted Solution Emails** — Provisioning lifecycle emails (store ready, onboarding tips, failure notifications)
- **Mobile App API** — Staff management and invitations, role-based permissions, inventory intelligence with low stock alerts and reorder suggestions, bulk order and product operations, PDF document generation (invoices, packing slips, pick lists), branding settings, and advanced analytics with CSV/Excel export
- **Inventory Settings** — Configurable backorder defaults, reorder lead days, safety stock multiplier, velocity tracking window, and low stock alert frequency
- **Email Delivery Mode Controls** — Merchants can configure email delivery behaviour

### Improved

- **Faster container startup** — Static files are now pre-baked at Docker build time, eliminating a 3–5 minute collectstatic step on every container start
- **Theme management performance** — Page load optimized from ~8s to under 1s
- Reorganized admin sidebar with dedicated Design group and improved navigation
- Modernized sync token management page with sidebar link
- Hosting type and subscription status tracking in the license system
- Developer license discoverability with installation guide
- Updated translations across all 16 admin languages

### Fixed

- Maintenance mode toggle bypasses SiteSettings validation to prevent lock-out
- Upgrade process resilience: maintenance fallback, validation bypass, and UI hardening
- CSP violations in sync templates

---

## [1.2.0] - 2026-03-18

### Added

- **Wallet & Store Credit** - Store credit system with a full transaction ledger
  - Support for credits, debits, refunds, adjustments, and reversals
  - Integrated with the referrals reward system as a payout method
  - Admin interface for wallet management and transaction history
- **Translation Provider Marketplace** - Browse and install translation providers from the Spwig marketplace
  - Provider setup wizard with built-in testing and webhook support
- **Blog Template System** - Choose from multiple blog layouts with admin configuration
  - Theme-aware rich text editing
- **Return Request & Order Email Notifications**
  - Return request notification workflow for merchants and customers
  - Order status update emails (shipped, delivered, cancelled, refunded)
  - Order note and cancellation customer email notifications
  - Blog subscriber verification emails
  - Gift card delivery and back-in-stock notification emails
- **Mobile App API Endpoints**
  - Daily stats analytics endpoint for dashboard charts
  - Staff password reset and SSO mobile authentication
- **Provider Version History** - View changelogs across all provider browse pages (email, shipping, payment, SMS, translation)
- **iOS Universal Links** - Support for apple-app-site-association and security.txt
- **Staff Maintenance Banner** - Staff-only maintenance mode banner on storefront
- **Migration Enhancements** - CSV import pipeline, category mapping, staged item retry, report downloads
- **Loyalty Enhancements** - CSV export, rule duplication, tiering engine, badges, points history, campaign builder
- **Page Builder Enhancements** - Stock check, wishlist API, version history, save element as reusable, element builder move/preview
- **License Version Check** - Platform checks for available version upgrades
- **Preinstalled Utilities** - 5 new bundled components: background-editor, focal-point-editor, gradient-creator, shadow-editor, translation-editor
- **Help Content** - New Italian Okta SSO setup guide; updated Turkish search engines documentation
- **Localization** - Added translation support to 5 previously unlocalized admin areas

### Fixed

- Theme pagination repeating installed themes on every page
- Shipping method wizard using hardcoded USD instead of site default currency
- Blog form save error on post creation
- Various bug fixes across admin and storefront

### Changed

- **Admin UI Modernization** - Replaced all native browser dialogs with styled modal components across the admin interface
- Optimized theme browse page performance (eliminated redundant API calls)
- Improved admin styling consistency across license and site settings pages
- Updated preinstalled utility component packages

---

## [1.1.0] - 2026-03-15

### Added

- **Remote Backup Storage** - Multi-provider backup system with setup wizard
  - Google Drive and Dropbox storage providers for off-site backups
  - Restore from remote backup support
- **Shopify Migration** - Standalone migration tool for importing data from Shopify
- **API Documentation** - Internationalized API docs with multi-language support
- **Theme SDK v2.0** - Extended theme manifest with new fields for niche, style, videos, assets, and responsive tokens
- Hotfix visibility in merchant admin interface

### Fixed

- Shopify order import handling for edge cases
- Translation catalog corrections across 456 language files (~2,600 fixes)
- Help system memory optimization for low-memory installations
- Admin status badge color improvements

### Changed

- Theme manifest engine field is now optional with automatic fallback
- Manifest schema allows additional properties for forward compatibility

---

## [1.0.3] - 2026-03-13

### Added

- **Shopify Migration Wizard** - Full import pipeline with robust rollback
- **Resource-Aware Installation** - Tiered service configuration based on available resources
- 7 additional help documentation languages (Hindi, Indonesian, Italian, Korean, Turkish, Vietnamese, Thai)

### Fixed

- Domain SSL: improved fallback when background workers are unavailable
- Domain SSL: automatic NGINX SSL config on certificate upload
- Maintenance mode now persists across restarts
- Product grid styling in page builder canvas
- Various admin template fixes

### Changed

- Raised minimum RAM requirement to 4GB

---

## [1.0.2] - 2026-03-12

### Added

- **Hotfix Delivery System** - Lightweight critical patches applied at startup, avoiding full image pulls for small fixes
  - Security hotfixes bypass maintenance windows
- **License Maintenance Renewal** - Renewal pipeline with email notifications
- Refresh License button on License Status admin page
- WooCommerce migration importer improvements
- Dashboard banner for translator local service status

### Fixed

- Translator model download bug and simplified local service UI
- Theme CSS serving and role-aware login redirect

### Changed

- Reduced production image size by excluding translation source files

---

## [1.0.1] - 2026-03-12

### Fixed

- **Email Language System** - Emails now sent in the customer's browsing language instead of always English
  - Proper fallback chain: user preference, site default, then English
  - Language captured at checkout time for order-related emails
- License and marketplace checkout emails now respect the customer's locale
- Hero element background not rendering in page builder canvas
- Visitor analytics now excludes bot and admin traffic from reporting
- Improved timeout handling for provider installations

### Added

- Email templates and translations for license checkout and account invitation

---

## [1.0.0] - 2026-03-10

First stable release of the Spwig Self-Hosted eCommerce Platform.

### Platform

- **48 apps** providing full eCommerce functionality
- **Single-tenant architecture** - each merchant gets their own installation
- **Component marketplace** - themes, integrations, and utilities via updates.spwig.com
- **16 admin languages** built-in (Arabic, German, English, Spanish, French, Hindi, Indonesian, Italian, Japanese, Korean, Portuguese, Russian, Thai, Turkish, Vietnamese, Chinese)
- **AI translation service** for customer-facing content

### Core Features

- Product catalog with variants, digital products, bundles, subscriptions, and 3D configurator
- Order management with fulfillment, refunds, and multi-location inventory
- Cart with guest checkout, vouchers, gift cards, and loyalty programs
- Customer accounts with wishlists, bookings, and messaging
- Blog with social connector publishing (Facebook, Instagram, LinkedIn, Twitter)
- Visual page builder with drag-and-drop elements
- Form builder for custom merchant forms

### Integrations

- **Payment providers**: Stripe, PayPal, Square, Revolut, Airwallex, Adyen
- **Shipping providers**: FedEx, UPS, USPS, Australia Post, Canada Post, NinjaVan
- **Email providers**: Gmail API, SMTP (plus built-in SMTP server)
- **Exchange rate providers**: Fixer, XE, CurrencyLayer, ExchangeRatesAPI, Open Exchange Rates
- **SMS providers**: Twilio, Twilio WhatsApp
- **SEO generators**: DataForSEO, Semrush, AI SEO
- **Product feeds**: Google Merchant Center

### Admin & Operations

- Role-based access control with custom staff roles
- Affiliate and referral program management
- Webhook system with 30+ event types
- Setup wizard for merchant onboarding
- Headless API for custom frontends
- POS system with terminal provider support

### Infrastructure

- Docker deployment with automated updates
- Redis caching and session management
- PostgreSQL with connection pooling
- S3-compatible object storage
- Automated backup, restore, and rollback
