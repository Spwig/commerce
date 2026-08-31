# Spwig Features

> 274 features · 20 categories. Every entry is derived from real, code-verified capabilities. Auto-generated from the Spwig source code.

## Categories

- [Product Catalog](#product-catalog) (14)
- [3D Product Configurator](#3d-product-configurator) (4)
- [Cart & Checkout](#cart-checkout) (17)
- [Payments](#payments) (13)
- [Orders & Returns](#orders-returns) (7)
- [Shipping & Fulfillment](#shipping-fulfillment) (10)
- [Point of Sale](#point-of-sale) (26)
- [Subscriptions & Recurring](#subscriptions-recurring) (9)
- [Customer Analytics](#customer-analytics) (15)
- [Marketing & Growth](#marketing-growth) (39)
- [Email & Communications](#email-communications) (10)
- [Blog & Content](#blog-content) (12)
- [Design & Storefront](#design-storefront) (14)
- [Page Builder](#page-builder) (9)
- [Media Library](#media-library) (5)
- [Search & Discovery](#search-discovery) (7)
- [Internationalization](#internationalization) (15)
- [Agentic Commerce](#agentic-commerce) (6)
- [Enterprise & Security](#enterprise-security) (9)
- [Platform & Administration](#platform-administration) (33)

## Product Catalog

- **Booking Products** — Merchants sell appointments, rentals, and events with availability rules, dynamic pricing, deposits, waitlists, rescheduling, cancellation, and iCal calendar output.
- **Custom Field Validation** — Entered values are checked against each field's type, required flag, ranges, choices, and formats, with per-field error reporting.
- **Custom Fields** — Add your own typed fields to products, categories, orders, and customers, organized into groups and ordered as you like.
- **Design Editor Setup** — Merchants configure per-product editor toggles, upload limits, pricing rates, print surfaces, and reusable design templates.
- **Field Data Entry & Storefront Display** — Staff enter custom-field values on records, and grouped values display on the storefront with select labels and defaults applied.
- **Field Recycle Bin & Recovery** — Deleted fields and groups go to a recycle bin where stored data is retained for restore, or can be permanently removed.
- **Gift Cards** — Merchants issue funded gift cards and accept them as tender at checkout with balance tracking, holds, captures, and refunds.
- **License Key Management** — Merchants auto-generate license keys, enforce device activation limits, validate licenses locally or via external providers, and notify integrations of lifecycle events.
- **Multi-Warehouse Inventory** — Merchants track stock across warehouses with allocation, fulfillment on shipment, availability checks, adjustments, and an immutable movement audit trail.
- **Print-Ready Fulfillment** — At checkout a customer's design is frozen to the order and rendered into print-ready files at the surface's target DPI.
- **Product Design Editor** — Customers personalize a product on a Fabric.js canvas with text, uploaded images, clipart, and custom fonts, with live per-design pricing.
- **Product Purchase Requirements** — Merchants gate purchases on required prerequisite products the customer already owns or has in cart, enforcing compatibility and upgrade paths.
- **Saved Customer Designs** — Signed-in customers save named designs, reload them later, and delete ones they no longer want.
- **Stock Reservation** — Temporary cart-level stock holds prevent overselling from add-to-cart through checkout, then convert into order allocations or POS fulfillment.

## 3D Product Configurator

- **3D & AR Product Viewer** — Shoppers view and rotate the product in a configurable 3D viewer with camera, lighting, AR, and auto-generated thumbnail.
- **3D Asset Management** — Add, list, and delete a product's texture, geometry, and option-mapping assets, scoped to that product to prevent cross-product access.
- **3D Model Setup** — Upload a GLB model and Spwig parses it into a configurable scene graph, keeping it current as the parser updates.
- **Visual Product Options** — Link a product's configuration-slot options to live visual changes — color, texture, part swaps, and show/hide of model parts.

## Cart & Checkout

- **Booking Checkout** — Booking cart items are converted into confirmed booking records with their schedule, resource, and person details at checkout.
- **Checkout & Order Placement** — Customers set addresses, pick an eligible payment method, and place a validated order with live-recalculated totals converted into a warehouse-allocated order.
- **Empty Cart Recommendations** — An empty cart shows curated in-stock product suggestions from recently viewed, related, on-sale, trending, and featured products.
- **Gift Card & Wallet Payment** — Buyers can pay with gift-card balance or store wallet credit via authorization holds that can be released, and orders fully covered by tenders settle without a gateway charge.
- **Guest Checkout** — Anonymous shoppers can complete a purchase without an account, including digital-only carts that skip shipping.
- **Guest Checkout** — Shoppers can buy without an account, or create one at checkout, and each anonymous browser can only open its own order confirmation.
- **Guided Checkout** — Buyers move through a session-based checkout that captures contact and addresses, keeps totals current, and validates readiness before placing the order.
- **Payment Method Selection** — Buyers are shown only payment providers active and eligible for their country, currency, and amount, and the selected provider is applied to the checkout.
- **Session & User Carts** — Shoppers keep one persistent cart across anonymous and logged-in sessions, with anonymous carts merging into their account on login.
- **Shipping Calculation** — Available shipping methods are filtered by zone and cart eligibility, priced via shipping rules and promotions, and selectable at checkout.
- **Shipping Selection** — Buyers see eligible shipping methods for their destination with rule-adjusted rates and pickup options, and the chosen method's cost and delivery estimate are applied.
- **Stock Reservation** — Adding an item holds its stock through checkout and releases it on removal or clearing, preventing overselling.
- **Subscription Checkout** — Subscription cart items are converted into recurring subscriptions on their plan and pricing tier using the stored payment token during order creation.
- **Tax Calculation** — Taxes are computed by geographic address specificity and product eligibility, with reusable named tax presets.
- **Voucher Application** — Customers apply and remove discount codes at checkout, with currency, minimum-order, per-customer, and combination rules enforced.
- **Voucher Redemption** — Applied discount codes are locked and re-validated against caps and validity at order time, with usage counted atomically and the order rolled back if limits are exceeded.
- **Wishlists** — Customers save items to wishlists with notes, priority, and back-in-stock/on-sale alerts, and share a wishlist via a public URL.

## Payments

- **3DS / Strong Customer Authentication** — Route card payments through the provider's 3DS/SCA second-factor step and complete settlement once the customer has authenticated.
- **Checkout Payment Processing** — Create a payment against a checkout order for the net amount due, confirm it, mark it paid on success or failed for retry, and cancel and release stock if abandoned.
- **Customer Wallet History** — Customers can view their wallet balance and full newest-first transaction ledger, filterable by type, source, and status, from their account pages and API.
- **Immutable Wallet Ledger & Reconciliation** — Every wallet movement is recorded in a tamper-proof ledger, currency mismatches are rejected, and balances are reconciled against the ledger to detect drift.
- **Pay with Wallet at Checkout** — Customers can hold and spend their wallet balance during a checkout session, with holds captured on payment, released on cancel, and expired if abandoned.
- **Payment Analytics** — See aggregated payment and provider performance, revenue over time, transaction status, method distribution, coverage, webhook stats, and refund metrics.
- **Payment Providers & Connections** — Install a payment provider from encrypted credentials, verify the connection, mount its checkout SDK on the storefront, and get emailed if the frontend SDK fails to load.
- **Per-Country Payment Methods** — Sync the payment methods a provider offers in each country, enable or disable them per country or globally, and show only eligible providers at checkout.
- **Store Credit Wallet** — Each customer gets a single wallet in the store's default currency that can be credited and debited, showing the balance available to spend.
- **Transaction Lifecycle & Refunds** — Track each payment from settlement through full or partial refunds with idempotent capacity checks, order cancellation, and a declared void-authorization step before capture.
- **Wallet Administration** — Administrators can search and inspect customer wallets and transactions and freeze a wallet to block all credit, debit, and hold activity.
- **Wallet Refunds & Reversals** — Merchants can refund all or part of a wallet payment back to the customer's balance and reverse eligible credits, with per-capture limits enforced.
- **Webhook Verification & Status Sync** — Ingest provider webhooks with signature verification and deduplication, replay stored unprocessed events, and poll providers to reconcile local payment state on divergence.

## Orders & Returns

- **Multi-Currency Orders** — Each order stores both customer-currency and base-currency amounts using the exchange rate locked at purchase.
- **One-Click Reorder** — Customers rebuild their cart from a past order, re-checking current availability and stock and skipping items no longer for sale.
- **Order Lifecycle & Tracking** — Merchants move orders through validated statuses, cancel eligible orders, and give customers live tracking with fulfillment milestones.
- **Order Statistics & Best-Sellers** — Customers see their order history and spend summaries while paid orders feed accurate per-product sales counts.
- **Refund Workflow** — Merchants issue full or partial refunds that pay back across the original captures by tender priority with full state tracking.
- **Returns & RMA** — Customers request returns on delivered orders and merchants approve, label, track, inspect, and close them end to end.
- **Versioned Addresses** — Customers manage reusable shipping and billing addresses; edits fork a new version so past orders keep their original address.

## Shipping & Fulfillment

- **Carrier Provider Integrations** — Connect carrier accounts to fetch live rate quotes, purchase labels, and test connectivity.
- **In-Store Pickup** — Offer store pickup with operating-hours and prep-time checks and bookable 30-minute slots.
- **Local Delivery Radius** — Check whether a destination falls within your own fleet's delivery range from a dispatch location.
- **Multi-Warehouse Fulfillment** — Resolve the shipment origin warehouse per destination country using a priority fallback chain.
- **Rate Tables** — Look up shipping cost from tiered tables based on cart weight, price, or item quantity, scoped by zone.
- **Return Labels (RMA)** — Generate PDF return labels carrying the RMA number and return-to address for return requests.
- **Shipment Tracking** — Ingest carrier webhooks and poll providers to update shipment status and tracking events.
- **Shipping Documents** — Generate packing slips, commercial invoices, and CN22/CN23 customs forms as PDFs.
- **Shipping Rules & Promotions** — Calculate cart shipping and modify it with conditional free-shipping, discount, or surcharge promotions.
- **Shipping Zones** — Define geographic zones by country, state/province, or postal-code pattern to control where rates apply.

## Point of Sale

- **Biometric & PIN Terminal Unlock** — Unlock terminals with WebAuthn fingerprint/face, staff cards, or PINs, with lockout and manager escalation after failures.
- **Card Reader Integration** — Discover, assign, brand, and take card payments on hardware readers bound one-per-terminal.
- **Customer-Facing Display** — Serve the terminal's current config, receipt template, and active promotional slides to a paired customer screen.
- **Customer-Facing Display** — Pair a secondary screen to a terminal using a single-use, time-limited numeric pairing code.
- **Digital Receipt Delivery** — Send order receipts by email, SMS, or WhatsApp and serve a tokenised public receipt page to the shopper.
- **In-Store Customer Profiles** — Create deduplicated walk-in customers and search existing profiles with their order and loyalty details.
- **Integrated Card Reader Payments** — Take card-present payments through connected readers with create, capture, cancel, and status polling.
- **Offline Mode & Sync** — Keep selling offline with delta catalog sync and idempotent upload of queued sales and stock adjustments.
- **Parked Carts** — Save a mid-transaction cart to serve another customer, then list, restore, or delete it later.
- **Parked Carts** — Save a mid-transaction cart for later retrieval and auto-expire unrestored parked carts.
- **POS Cart & Voucher Application** — Build carts by product or barcode with variant/bundle selections, stock limits, and applied promo vouchers.
- **POS Catalog & Barcode Lookup** — Browse and search published products with terminal-warehouse stock, and resolve scanned barcodes or SKUs.
- **POS Checkout & Split-Tender Payments** — Complete in-store sales paid by cash, external card, gift card, or a mix of tenders, with change and stock updates.
- **POS Loyalty Points** — Look up a customer's tier and balance, preview points for a sale, and award points on checkout without blocking it.
- **Printed & Digital Receipts** — Generate thermal-printer receipts from the terminal's template and queue email, SMS, or WhatsApp digital receipts.
- **Refunds & Voids** — Process full or partial refunds and void same-shift sales, returning stock and adjusting shift totals.
- **Shift & Cash Management** — Open and close cashier shifts with opening/closing cash, cash-in/out movements, and drawer reconciliation.
- **Shift Management & Cash Reconciliation** — Open and close cashier shifts with opening float, cash movements, and expected-versus-counted drawer reconciliation.
- **Staff Discount Controls** — Apply staff discounts within per-staff limits and require manager PIN approval when limits are exceeded.
- **Staff Discount Controls** — Enforce per-staff discount limits, allowing, rejecting, or escalating manual discounts for manager PIN approval.
- **Staff Login & Access Control** — Authenticate staff with tokens and gate POS endpoints behind valid licence and named permission checks.
- **Stock Adjustments & Cross-Location Stock** — Adjust warehouse stock with audited movements and view a product's availability across all locations by distance.
- **Terminal Lock & Staff Unlock** — Lock terminals and unlock them via cashier/manager PIN, registered card, or biometrics, with lockout rules, remote unlock, and audit logging.
- **Terminal Management** — Pair and register terminals, monitor heartbeat and config, and lock/unlock devices with audited unlock events.
- **Terminal Management & Device Pairing** — Enable retail store locations and pair register devices with a unique code that retrieves their configuration.
- **Terminal Sales Reporting** — Daily per-terminal totals for net/total sales, refunds, transaction count, average value, and payment-method breakdown.

## Subscriptions & Recurring

- **Billing History** — Customers can view a reverse-chronological record of successful, failed, and retried subscription charges.
- **Cancellation & Reactivation** — Cancel subscriptions immediately or at period end, expire them automatically, and reactivate within a set window.
- **Failed Payment Recovery** — Automatically retry failed subscription charges with backoff during a grace period to recover lapsed payments.
- **Free Trials** — Offer trial periods that automatically convert to paid subscriptions and run first billing when the trial ends.
- **Pause & Resume** — Customers can pause an active or trial subscription and resume it later, manually or on a scheduled auto-resume date.
- **Plan Changes & Add-ons** — Customers can upgrade, downgrade, or schedule plan changes with proration and add per-cycle extras to a subscription.
- **Saved Payment Methods** — Securely capture, update, and remove the reusable card used for a customer's recurring charges.
- **Subscription Reminders** — Send customers notifications for ending trials, upcoming renewals, and expiring payment methods.
- **Subscriptions** — Sell products on recurring plans with tiered, quantity, or flat pricing, and automatically charge and create renewal orders each cycle.

## Customer Analytics

- **Abandoned Cart Recovery** — Captures abandoned carts, sends timed recovery emails, and tracks which carts were recovered.
- **Cohort Analysis** — Groups customers by acquisition month, channel, and first-purchase category and tracks retention, revenue, and average LTV over time.
- **Communication Frequency Recommendations** — Each customer gets an engagement score and a recommended messaging frequency based on order history, spend, and verified opt-in.
- **Communication Preference Center** — Customers control which emails and SMS they receive per channel and per app, and delivery is gated to honour those choices and transactional locks.
- **Consent Audit & Preference Analytics** — Every preference change is logged with source and IP, and opt-in trends and adoption are reported on a dashboard, with audit logs pruned on a retention schedule.
- **Customer Account Dashboard** — Gives logged-in customers a self-service view of their order stats, spending insights, savings, loyalty status, and favorite products.
- **Customer Analytics Dashboard** — Aggregates cross-customer metrics like revenue by segment, churn-risk distribution, purchase frequency, and cohort retention for staff.
- **Customer Data Privacy (GDPR)** — Merchants can export a customer's preference and consent data or irreversibly anonymise the customer while preserving financial records, with audit retention limits enforced.
- **Customer Notes** — Lets staff record typed customer notes with follow-up dates and completion tracking.
- **Customer Segmentation** — Assigns each customer to their highest-priority matching segment based on spend, completed orders, and purchase recency.
- **Guest Checkout & Account Creation** — Shoppers can buy as a guest and later become full account holders, with duplicate records for the same email merged automatically.
- **Lifetime Value (LTV)** — Estimates each customer's current and predicted lifetime value using RFM, cohort-historical, and probabilistic models, with value tiers and churn-risk levels.
- **Opt-In Verification (Email & SMS)** — Email double-opt-in and TCPA-compliant SMS verification confirm consent before marketing messages are sent to a customer.
- **Personalized Product Recommendations** — Suggests in-stock products for each customer from their favorite categories, purchase history, and related-product signals.
- **RFM Scoring** — Scores customers on recency, frequency, and monetary value from their delivered-order history.

## Marketing & Growth

- **Achievement Badges** — Members automatically earn badges when they meet order, spend, review, streak, timing, or referral criteria.
- **Affiliate Notifications & Reports** — Affiliates receive language-aware emails for account, commission, and payout events plus a monthly performance summary.
- **Affiliate Payouts** — Approved commissions are aggregated into payouts—requested by affiliates or generated in batch—and paid out via PayPal or Airwallex with status tracking.
- **Affiliate Payouts** — Send single or batched affiliate commission payouts through PayPal or Airwallex, with fee/arrival estimates and in-flight cancellation.
- **Affiliate Programs** — Staff create affiliate programs with fixed or percentage commissions, cookie lifetimes and payout thresholds, and can pause or archive them.
- **Affiliate Signup & Approval** — Users register as affiliates, apply to programs, and staff approve, suspend, or reject affiliates and their program memberships.
- **Automatic & Bulk SEO Fill-In** — Fill missing SEO metadata automatically on save, or generate it for many items in one batch.
- **Bulk Voucher Generation & Import/Export** — Generate up to 1,000 unique codes at once and import or export voucher batches as CSV/XLSX.
- **Commission Management** — Commissions are calculated per order, approved/rejected/paid by staff, reversed on refunds or returns, and rolled into each affiliate's balance.
- **Customer Share History** — Let signed-in customers view their own total, per-platform, and most recent shares.
- **Feed Download** — Download the latest generated feed for any account as a file, with download counts and timestamps tracked.
- **Feed Preview & Validation** — Preview a sample feed before publishing and flag items missing required fields like id, title, price, or image.
- **Fraud Detection & Attribution Review** — Scores referrals for fraud, enforces eligibility rules, and auto- or staff-approves, rejects, or expires attributions before rewards are paid.
- **Gift Cards & Store Credit** — Issue voucher-backed gift cards, check balances, and redeem against orders until the balance is spent.
- **Loyalty Campaigns** — Trigger-based, multi-step journey campaigns target member segments and tiers to award points, send emails, issue rewards, or grant badges, with A/B splits.
- **Loyalty Member Segments** — Dynamic segments re-evaluate members by tier, points, spend, orders, AOV, recency, redemptions, and other rules for targeting.
- **Loyalty Points & Rewards** — Members earn points from orders and actions on an immutable ledger and redeem them for discounts, vouchers, or wallet credit.
- **Loyalty Tiers** — Members are promoted or demoted across tiers by lifetime points, spend, and order count, with tier-based earning multipliers applied.
- **Marketplace Product Feeds** — Generate Google Shopping, Facebook/Meta, RSS, XML, CSV/TSV, and JSON Lines feeds from your published catalog with per-account category, stock, and price filters.
- **Marketplace Provider Connections** — Connect and manage marketplace accounts with a guided setup wizard, encrypted credentials, connection testing, and a designated primary account per store.
- **Payout Provider Accounts** — Connect, test, enable/disable, delete, and set a default account for each payout provider (PayPal, Airwallex).
- **Payout Provider Components** — Install and update payout-provider component packages from the update server with version switching.
- **Payout Status & Webhooks** — Ingest and signature-verify provider webhooks, log them for audit, and reconcile each payout to completed, failed, or cancelled.
- **Provider Credential Protection** — Provider credentials are encrypted at rest and masked in logs.
- **Referral Funnel Tracking & Analytics** — Tracks clicks, signups, and first-order conversions per referrer with funnel totals, top-referrer stats, and status breakdowns.
- **Referral Links & Invitations** — Each customer gets a unique referral link and QR code, and can invite friends by email with a personal message.
- **Referral Rewards** — Issues double-sided rewards as wallet credit, coupons, or perks, and emails participants across issuance, redemption, expiry, and revocation.
- **Scheduled Feed Sync** — Feeds regenerate and push to providers automatically on hourly, daily, or weekly schedules, with expired feed files cleaned up on their own.
- **SEO Content Generator** — Generate meta titles, descriptions, and keywords for products, categories, brands, pages, and blog posts.
- **SEO Coverage & Gaps** — See per-type and overall SEO completeness and list which items are missing or have length issues.
- **SEO Provider Integrations** — Connect, install, and update SEO providers, with one primary provider account enforced per site.
- **Share Tracking** — Record every guest and logged-in share event and keep per-content, per-platform share totals up to date.
- **Share-to-Earn Badges** — Automatically award loyalty badges to members when they share store content.
- **Sharing Analytics** — Give staff sharing KPIs, trends, platform and content breakdowns, plus searchable share-count and share-event reports.
- **Storefront Share Buttons** — Show configurable social share buttons on products, categories, blog posts, and pages, with live per-platform share counts.
- **Tracking Links & Attribution** — Approved affiliates generate unique tracking links; clicks set attribution cookies and orders are credited by last-click, with automatic click cleanup.
- **Voucher Application** — Customers apply and remove discount codes at checkout with eligibility, stacking, and minimum-value rules enforced.
- **Voucher Usage Reporting** — See per-voucher usage counts, unique customers, total and average discount, and recent redemptions.
- **Vouchers & Coupons** — Create percentage, fixed-value, or gift-card discount codes with usage rules and restrictions.

## Email & Communications

- **AI Template Translation** — Merchants get email templates auto-translated per site language with human verification of each translation.
- **Deliverability & Authentication** — Merchants validate SPF/DKIM/DMARC, get recommended DNS records, DKIM-sign outgoing mail, and test provider connections.
- **Delivery & Engagement Tracking** — Merchants see email opens and clicks via tracking pixels and rewritten links, with provider events for bounces and complaints.
- **Email Campaign Link Attribution** — Marketing email links are auto-tagged with UTM and attribution parameters so campaign-driven orders can be tracked.
- **Email Delivery Queue** — Emails are queued, scheduled, sent through the configured provider, retried on failure, and can be held or released.
- **Email Templates** — Merchants send transactional and marketing emails from localized, theme-styled templates that can be activated, cloned, and edited.
- **SMS Notifications** — Send transactional and templated SMS to customers with variable substitution and delivery status tracking.
- **SMS Provider Setup** — Browse, install, configure, test, and update SMS/WhatsApp providers with encrypted credentials and a default account per channel.
- **Template Versioning** — Merchants snapshot template edits, revert to earlier versions, and clone system templates to customize safely.
- **WhatsApp Messaging** — Send pre-approved parameterized WhatsApp templates to customers and track delivery in the outbox.

## Blog & Content

- **Announcement Pop-up Modals** — Open a modal with the full announcement body and an image shown as a banner or overlay background.
- **Announcement Scheduling & Targeting** — Set an expiry so announcements stop showing automatically, with per-announcement enable/disable and stored visibility rules.
- **Blog Posts & Content Modes** — Create, edit, publish, and unpublish blog posts written in rich text or built with the page builder.
- **Categories & Tags** — Organize posts with hierarchical categories and flat tags that readers can browse.
- **Clickable Announcement Links** — Link an announcement to a product, category, blog post, page, or custom URL, or leave it non-clickable.
- **Email Subscribers** — Readers subscribe with double opt-in and receive new-post, weekly, or monthly digest emails by their preferences.
- **Multilingual Announcements** — Display announcement title, body, and link text in the visitor's language using stored per-language translations.
- **Reader Engagement** — Show estimated reading time and related posts, and track per-post view counts.
- **RSS Feed** — Publish a configurable RSS feed of recent posts with excerpt or full content and featured-image enclosures.
- **Scheduled Publishing** — Set a future date and time for a post and have it publish automatically.
- **Social Auto-Sharing** — Connect social accounts and auto-share posts on publish, with token refresh and retry of failed shares.
- **Store Announcement Banners** — Show enabled announcements in the storefront notification zone, ordered by priority, with rotation and per-session dismissal.

## Design & Storefront

- **Automated Form Actions** — Each submission can trigger auto-reply emails, notification emails to your team, and signed webhooks to external systems.
- **Brand Customization** — Override colors, typography, and spacing tokens without code and see them compiled into a cached brand stylesheet.
- **Component Marketplace & Packaging** — Package, sign, validate, verify, and render installable storefront components with tier-aware placement enforcement.
- **Conditional Logic** — Rules show, hide, require, or preset fields and steps based on what the visitor enters.
- **Design Token Cascade** — Design tokens resolve through a priority order across brand, theme, and system sources with atomic reconciliation.
- **Form Builder** — Staff build and edit multi-step forms in a visual builder with reorderable fields and one-click duplication.
- **Form Recycle Bin** — Deleted forms move to a recycle bin where staff can restore them or permanently remove them.
- **Header, Footer & Navigation Builder** — Install header/footer presets and preview widgets and personalized navigation menus for the current visitor.
- **Page Security Tiers** — Per-tier rules sanitize authored HTML/CSS and control which components and tokens are permitted on each page.
- **Response Export** — Download completed responses as a CSV with submission metadata and per-field values.
- **Spam Protection** — A honeypot field blocks bot submissions in the browser; reCAPTCHA settings are configurable but not yet enforced server-side.
- **Submissions & File Uploads** — Visitors submit forms with validated required fields and file attachments, and can save partial drafts to finish later.
- **Theme & Component SDK** — Staff-owned development sessions let developers push, validate, compile, and package themes and components in a sandbox.
- **Theme System** — Install, activate, preview, and update versioned theme packages that compile into the storefront's live CSS.

## Page Builder

- **Custom Element Builder** — Visually compose reusable page elements from primitives, arrange them in multi-column layouts, and preview the result on a builder canvas.
- **Custom Element Library** — Create, name, search, filter, and manage a library of saved custom elements for reuse across the store.
- **Draft & Publish Version History** — Every edit is saved as a versioned draft that merchants can publish, and any prior version can be restored.
- **Dynamic Data Binding** — Bind element content to live store model fields so custom elements render current product and catalog data on the storefront.
- **Multilingual Pages** — Page and element content is served in the visitor's locale with fallback to the base language when a translation is missing.
- **Page & Element Templates** — Merchants create new pages from reusable templates, duplicate whole pages or elements, and start from shipped default pages.
- **Page Settings & SEO** — Merchants edit page metadata, access, presentation, theme, media, and translations, including per-page SEO fields.
- **Visibility & Personalization Rules** — Merchants show, hide, or personalize page elements per visitor by rules including time-based and login-required access.
- **Visual Page Editor** — Merchants build and arrange page content by adding, editing, reordering, duplicating, and deleting elements, with auto-generated page previews.

## Media Library

- **Automatic Image Optimization** — Every uploaded image is converted to WebP/AVIF with sized thumbnails and served through responsive picture sources.
- **Media Library Organization** — Organize assets into folders and tags, search and edit them, bulk-update in one action, and see where each is used.
- **Recycle Bin & Restore** — Soft-deleted assets go to a recycle bin where they can be restored or permanently purged by staff.
- **Secure Media Uploads** — Upload images, video and 3D files that are safety-checked and have their dimensions, format and metadata detected automatically.
- **Video & 3D Media Delivery** — Uploaded videos are transcoded to web formats with poster frames and streamed with seek support.

## Search & Discovery

- **Did-You-Mean Corrections** — Misspelled queries get a suggested correction drawn from the catalog vocabulary and popular past searches.
- **Document & Digital Asset Search** — Text inside PDF, DOCX, XLSX, and plain-text files is indexed and searchable with matching snippets.
- **Predictive Autocomplete** — As shoppers type, they see fast grouped suggestions per content type with instant redirects for known terms.
- **Search Analytics** — Merchants track query volume, zero-result rate, CTR, trending terms, and response time, with CSV export.
- **Search Redirects** — Merchants route specific queries straight to a chosen page using exact, contains, prefix, or regex rules.
- **Storefront Product & Content Search** — Shoppers find products, categories, brands, and blog posts with language-aware, filtered, sorted, paginated results.
- **Synonym Management** — Merchants define bidirectional synonyms per language and get recommended additions from zero-result queries.

## Internationalization

- **AI Content Translation** — Translate products, pages, and other content into other languages using local AI models, run as tracked jobs.
- **Automatic Currency & Language** — Detects a visitor's location to suggest the right currency and language, stores their chosen preferences, and lets them correct a wrong location.
- **Campaign Traffic Attribution** — Aggregates visitor counts, page views, and pages per session by UTM source, medium, and campaign to attribute traffic to marketing campaigns.
- **External Translation Providers** — Connect and test third-party translation provider accounts with encrypted credentials as an alternative to local models.
- **Geo Business Rules** — Triggers actions such as setting currency, showing a banner, or redirecting based on visitor country, region, mobile, or VPN status.
- **GeoIP Detection** — Resolves each visitor's IP to country, region, and city through a configurable, testable provider cascade with VPN/proxy detection.
- **Language Management** — Activate, deactivate, reorder, and bulk-configure storefront languages, and let shoppers switch language.
- **Live Exchange Rate Providers** — Automatically pull and refresh currency rates from external providers on a schedule, with provider priority fallback and a single primary source.
- **Locked Order Exchange Rates** — Store an immutable snapshot of the exchange rate and its source on each order for accurate historical and accounting records.
- **Manual Exchange Rates** — Set and manage your own currency-pair rates, activate or deactivate them, and lock them so provider syncs don't overwrite them.
- **Multi-Currency Conversion** — Convert amounts between currencies using cached, manual, or live rates with optional markup and correct target-currency rounding.
- **Translation Coverage Reporting** — See overall and per-language translation coverage across content, email templates, and UI strings, and the work needed to complete it.
- **Translation Locking** — Lock specific fields or UI strings per language so manual translations are never overwritten by automatic runs.
- **UI String Translation & Overrides** — Auto-translate storefront UI strings and override any of them per language, with import/export of translation packs.
- **Visitor Analytics** — Tracks page views and sessions, classifies bots and devices, and reports daily traffic, KPIs, session journeys, and country/device breakdowns with automatic data retention cleanup.

## Agentic Commerce

- **Agent Identity & Trust Controls** — Only cryptographically signed agents can transact, with per-agent verification, spend caps, tender limits, and block controls.
- **Agentic Checkout** — AI agents can create a cart, add buyer and shipping details, and place or cancel a repriced, paid order on a shopper's behalf.
- **Agentic Commerce Controls** — Turn agentic commerce on or off per protocol with an emergency kill switch, a readiness check, and an immutable audit trail of agent events.
- **AI Agent Product Discovery** — AI shopping agents can discover, search, and read your live catalog through UCP, ACP, and MCP standards.
- **Signed Payment & Order Mandates** — Each paid agent order and its payment leg is attested with a signed, verifiable AP2 mandate.
- **Store Signing Keys** — Generates, rotates, and retires the store's transport and mandate signing keys, publishing public keys as a JWKS for agents to verify.

## Enterprise & Security

- **Admin Access Control** — Every admin area and action is gated by a staff member's role, with view-only or full access enforced per permission category.
- **Automatic Staff Provisioning** — Staff accounts are created on first sign-in and their names kept in sync from identity-provider claims.
- **Group-Based Access Control** — Identity-provider group membership determines who gets staff and superuser access, and blocks non-staff sign-ins.
- **Identity Provider Setup & Security** — Connect any OIDC provider via discovery, with the client secret encrypted at rest and discovery URLs SSRF-protected.
- **Mobile Admin Sign-On** — Staff log into the admin mobile app through the same identity provider on registered devices.
- **POS Staff Permissions** — Control which staff can access POS terminals and what actions they can perform, resolved across all their assigned roles.
- **Staff Roles & Permissions** — Define custom staff roles with granular admin and POS permissions, including ready-made presets like Store Owner, Manager, and Cashier.
- **Staff Single Sign-On** — Staff sign in to the admin using your company's identity provider instead of separate store passwords.
- **Team Member Assignment** — Add or remove staff members from roles to control who has access to what.

## Platform & Administration

- **Advanced Product Type Import** — Carries bundles, composite/configurable products, subscriptions, bookings, gift cards, and product customizations across from the source store, resolving cross-product links in a second pass.
- **API Access Tokens** — Programmatic access is controlled by scoped, IP-restricted API tokens that are validated per request with usage tracking.
- **Automatic HTTPS & SSL Certificates** — Issue and auto-renew free Let's Encrypt certificates over HTTP-01, with HTTPS redirection, HSTS, and a self-signed fallback.
- **Automatic Retries & Endpoint Health** — Transient failures are retried with capped exponential backoff, failing endpoints auto-disable and can be reset, and failed deliveries can be retried manually.
- **Bring Your Own Certificate** — Upload your own PEM certificate and key, including Cloudflare Origin certificates, with metadata extraction and domain-mismatch warnings.
- **Component Marketplace** — Browse the Spwig catalogue and install themes, widgets, and provider components, verified by checksum and dependency checks.
- **Component Marketplace** — Merchants browse, filter, and view themes, widgets, and provider components from the Spwig marketplace, each annotated with its local install status.
- **Component Reviews & Ratings** — Merchants read component reviews and submit their own 1-to-5 star ratings attributed to their store.
- **Component Updates & Rollback** — Detect available component updates, apply them with post-install health checks, and roll back to a prior version if a check fails.
- **Content Link & Image Migration** — Scans migrated product, blog, and category HTML to re-point internal links to their new Spwig objects and pull referenced images into the media library.
- **Cookie Consent & GDPR Audit** — Visitor cookie choices are normalized, classified, and stored as GDPR audit records.
- **Custom Domain Setup** — Connect your own domain to the store, with DNS validation, NGINX configuration, and reachability checks handled end to end.
- **Delivery Monitoring & Log Retention** — Per-endpoint 24-hour stats (counts, success rate, response time, health) are available, and completed delivery records are pruned after a configurable retention period.
- **Error & Bug Reporting** — Application errors are captured, deduplicated, and batched to the update server, and staff can file sanitized bug reports with browser context.
- **Event-Driven Delivery** — Store events are pushed to subscribed endpoints (explicit or wildcard) as HTTP POST payloads, with each delivery attempt and its outcome recorded.
- **In-App Help Center** — Merchants and staff find answers through keyword and semantic search over help topics, with contextual suggestions on each page and helpfulness feedback.
- **Language Packs** — Install and remove per-language packs that deploy interface translations, help content, and email-template strings.
- **License Management** — Fetch and verify a freshly signed license and related secrets from the update server and persist changes.
- **Licensing & Installation Integrity** — The store records versioned license acceptance, verifies its installation fingerprint, refreshes platform secrets, and tracks revocation grace periods.
- **Managed Custom Domains (Hosted)** — On hosted installs, add, verify, and remove a custom domain through the hosting platform, reverting to the myspwig.com subdomain when detached.
- **Migration Job Control & Rollback** — Cancel, retry, reset, or fully roll back an import, recover jobs whose worker died, and reattempt individual failed items without losing real orders.
- **One-Click Component Install** — Merchants install free or entitled components directly from the marketplace via the update manager.
- **Paid Component Purchases** — Merchants check their license entitlements and buy paid components through a spwig.com checkout, then install what they own.
- **Platform Upgrades & Hotfixes** — Run blue-green platform version upgrades with prechecks, package verification, health checks, rollback, and hotfix reporting.
- **Sales Bell Alerts** — Sale, refund, and developer-signup events are logged to an HQ-only feed for real-time visibility.
- **Sandbox-Safe Testing** — In sandbox mode, external deliveries are recorded as blocked instead of being sent while localhost targets still receive test events.
- **Signed & Verified Payloads** — Every payload is signed with HMAC-SHA256, secrets can be rotated on demand, and receivers can verify signatures with an age-tolerance check.
- **Soft Delete & Recovery** — Records can be soft-deleted and restored to protect against accidental loss, with a hard-delete path for permanent removal.
- **Spwig-to-Spwig Sync** — Move settings or full data between two Spwig instances over authenticated endpoints, with version compatibility checks, media transfer, and rollback.
- **SSL Monitoring** — Track the live certificate's domain, issuer, expiry, and validity, persisting refreshed status for the store.
- **Store Migration Wizard** — Import categories, products, customers, and orders from WooCommerce, Shopify, Magento, or CSV with pre-import connection checks, field mapping, and media transfer.
- **Trusted-Device Two-Factor** — Users can mark a device as trusted to skip 2FA on future logins, with validation, revocation, and automatic expiry cleanup.
- **Webhook Endpoints** — Register, configure, update, and delete webhook endpoints with per-endpoint event subscriptions, retry and timeout settings, and a connectivity test.
