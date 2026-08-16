# Spwig Features

> 282 features · 20 categories. Every entry is derived from real, code-verified capabilities. Auto-generated from the Spwig source code.

## Categories

- [Product Catalog](#product-catalog) (16)
- [3D Product Configurator](#3d-product-configurator) (4)
- [Cart & Checkout](#cart-checkout) (17)
- [Payments](#payments) (13)
- [Orders & Returns](#orders-returns) (7)
- [Shipping & Fulfillment](#shipping-fulfillment) (10)
- [Point of Sale](#point-of-sale) (23)
- [Subscriptions & Recurring](#subscriptions-recurring) (9)
- [Customer Analytics](#customer-analytics) (15)
- [Marketing & Growth](#marketing-growth) (39)
- [Email & Communications](#email-communications) (13)
- [Blog & Content](#blog-content) (11)
- [Design & Storefront](#design-storefront) (16)
- [Page Builder](#page-builder) (9)
- [Media Library](#media-library) (5)
- [Search & Discovery](#search-discovery) (7)
- [Internationalization](#internationalization) (16)
- [Agentic Commerce](#agentic-commerce) (6)
- [Enterprise & Security](#enterprise-security) (9)
- [Platform & Administration](#platform-administration) (37)

## Product Catalog

- **Booking Products** — Merchants sell appointments, rentals, and events with availability rules, dynamic pricing, deposits, waitlists, rescheduling, cancellation, and iCal calendar output.
- **Custom Design Pricing & Checkout** — A configured design is priced by surfaces, uploads, clipart, and text, held as a time-limited cart draft, validated at cart, and frozen onto the order at checkout.
- **Custom Field Validation** — Entered values are checked against each field's type, required flag, ranges, choices, and formats, with per-field error reporting.
- **Custom Fields** — Add your own typed fields to products, categories, orders, and customers, organized into groups and ordered as you like.
- **Design Templates** — Staff author and manage ready-made canvas templates for a product, with locking of individual elements to guide customer edits.
- **Field Data Entry & Storefront Display** — Staff enter custom-field values on records, and grouped values display on the storefront with select labels and defaults applied.
- **Field Recycle Bin & Recovery** — Deleted fields and groups go to a recycle bin where stored data is retained for restore, or can be permanently removed.
- **Gift Cards** — Merchants issue funded gift cards and accept them as tender at checkout with balance tracking, holds, captures, and refunds.
- **License Key Management** — Merchants auto-generate license keys, enforce device activation limits, validate licenses locally or via external providers, and notify integrations of lifecycle events.
- **Multi-Surface Product Setup** — Staff define per-product design surfaces with dimensions, zones, print/DPI settings, mockups, and which of text, uploads, and clipart are allowed on each.
- **Multi-Warehouse Inventory** — Merchants track stock across warehouses with allocation, fulfillment on shipment, availability checks, adjustments, and an immutable movement audit trail.
- **Print-Ready Fulfillment Files** — After checkout the ordered design is composited per surface at target DPI into print-ready image files for production.
- **Product Design Editor** — Customers personalize a product on a live canvas with text, uploaded images, clipart, and custom fonts within the limits set for each surface.
- **Product Purchase Requirements** — Merchants gate purchases on required prerequisite products the customer already owns or has in cart, enforcing compatibility and upgrade paths.
- **Saved Customer Designs** — Signed-in customers save, reload, and delete their own named product designs across sessions.
- **Stock Reservation** — Temporary cart-level stock holds prevent overselling from add-to-cart through checkout, then convert into order allocations or POS fulfillment.

## 3D Product Configurator

- **3D Product Model Setup** — Attach a 3D model to a configurable product and store its parsed scene structure for configuration.
- **Interactive 3D & AR Viewer** — Show shoppers an interactive 3D/AR product viewer with configurable camera, lighting, and a saved scene thumbnail.
- **Texture & Material Library** — Upload and manage texture image assets that configuration options apply to the model.
- **Visual Configuration Options** — Link product configuration options to visual changes on the 3D model: material colors, part visibility, and swappable geometry.

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

- **Card Reader Integration** — Discover, assign, and monitor card readers per terminal and push branded splash screens to the device.
- **Cart Building & Customer Lookup** — Browse the catalog, add items by barcode/SKU, apply promo vouchers, and attach or create a walk-in customer.
- **Checkout & Split-Tender Payments** — Complete a sale across cash, card, terminal-card, gift-card, and split tenders, recording payments.
- **Customer-Facing Display** — Pair a secondary customer-facing screen to a terminal using a rotating pairing code.
- **Customer-Facing Display** — Pair a secondary screen that shows live cart and payment status plus store-scoped promotional slides.
- **Digital Receipts** — Send order receipts to customers by email, SMS, or WhatsApp.
- **Integrated Card Reader Payments** — Take card payments through an integrated card reader by creating, capturing, and cancelling payment intents.
- **Inventory Control** — View stock and movements across locations and adjust warehouse stock for receipts, damage, recounts, and returns.
- **Loyalty at the Counter** — Preview loyalty points and rewards before a sale and award earned points on completed orders.
- **Offline Mode & Sync** — Queue sales and stock adjustments while offline and replay them idempotently, plus fetch data deltas to keep terminals in sync.
- **Parked Carts** — Save a mid-transaction cart, list parked carts, and restore one later to serve multiple customers.
- **Parked Carts** — Save a mid-transaction cart, restore it later, and auto-clear parked carts after their expiry.
- **Receipts & Digital Delivery** — Apply store-scoped receipt templates and send receipts by email, SMS, WhatsApp, or a public receipt link.
- **Refunds & Voids** — Refund POS orders in full or by item, and void same-shift orders with automatic shift-total reversal.
- **Sales Reporting** — View daily POS sales totals and top-selling product metrics.
- **Shift & Cash Management** — Open and close shifts with opening float, cash-in/out movements, and running totals.
- **Shift Management** — Open and close cashier shifts with cash-in/out movements and expected-versus-counted cash reconciliation.
- **Staff Discount Controls** — Apply manual line or cart discounts within per-staff limits, with manager-PIN override for over-limit amounts.
- **Staff Discount Controls** — Enforce per-staff discount limits and require manager PIN approval for discounts that exceed them.
- **Staff Login & Biometric Terminal Unlock** — Log staff in and unlock terminals via WebAuthn biometrics, PIN, or staff card with lockout auditing.
- **Terminal Lock & Unlock** — Lock and unlock terminals via cashier/manager PIN, staff card, biometrics, or remote admin, with full audit logging and lockout rules.
- **Terminal Management** — Register and pair POS terminals, return their configuration, and record heartbeats.
- **Terminal Setup & Device Pairing** — Register POS terminals, issue pairing codes, and verify payment provider connectivity before going live.

## Subscriptions & Recurring

- **Cancellation & Reactivation** — Cancel subscriptions immediately or at period end with recorded reasons, expire them on schedule, and reactivate eligible canceled subscriptions within a set window.
- **Failed Payment Recovery (Dunning)** — Automatically retries failed charges with backoff, re-attempts payment during a grace period, and cancels only after recovery attempts are exhausted.
- **Free Trials** — Offer trial periods that automatically convert to paid, active subscriptions when the trial ends.
- **Lifecycle Reminder Emails** — Send automated emails for trials ending, upcoming renewals, and payment events tied to subscription activity.
- **Pause & Resume** — Subscribers can pause an active subscription and resume it later, either manually or on a set auto-resume date.
- **Recurring Billing Engine** — Charges subscribers on each billing cycle and processes provider webhook and fallback events to keep subscription status and periods in sync.
- **Stored Payment Methods** — Securely tokenize customer payment methods, update the card on a subscription, and delete tokens when no active subscription depends on them.
- **Subscription Plans & Pricing** — Publish subscription plans and tiers with product-derived recurring prices, tier discounts, and quantity pricing that customers can browse and subscribe to.
- **Upgrades, Downgrades & Scheduled Changes** — Let subscribers switch plans or tiers with prorated charges or credits, either immediately or scheduled for the next renewal, with the option to cancel a pending change.

## Customer Analytics

- **Abandoned Cart Recovery** — Detects abandoned carts, sends staged recovery emails, and marks carts as recovered.
- **Cohort Analysis** — Groups customers by acquisition and tracks per-cohort retention, cumulative revenue, and average LTV over time.
- **Communication Preferences & Consent** — Customers control which email and SMS messages they receive, with verified double opt-in and one-click unsubscribe, while transactional messages stay protected.
- **Customer Accounts & Guest Checkout** — Shoppers can buy as a guest and later upgrade to a full account, with duplicate email records consolidated automatically.
- **Customer Analytics** — Aggregates cross-customer analytics including revenue by segment, churn-risk distribution, and cohort retention.
- **Customer Notes** — Lets staff record typed customer notes with follow-up requirements and mark them completed.
- **Customer Savings Tracker** — Summarizes a customer's realized voucher, sale, and loyalty savings and estimates potential future savings.
- **Customer Segmentation** — Assigns each customer to the highest-priority matching segment based on spend, order count, and purchase recency.
- **Lifetime Value (LTV)** — Estimates each customer's lifetime value using RFM, cohort-historical, and probabilistic (BG/NBD) methods with value tiers and churn risk.
- **Loyalty Status** — Derives a customer's loyalty tier, points, progress to the next tier, and tier benefits from their spend.
- **Opt-In Insights & Recommended Defaults** — Merchants see opt-in adoption trends and get rule-based engagement scores that suggest the right message frequency per customer.
- **Privacy & Data Rights (GDPR)** — Merchants can export or irreversibly erase a customer's data and keep an immutable audit trail of every preference change with retention limits.
- **Product Recommendations** — Ranks a customer's favorite products, categories, and brands and generates in-stock personalized recommendations.
- **RFM Scoring** — Scores each customer on recency, frequency, and monetary value from their delivered-order history.
- **Social Login** — Customers can sign in with Google, Apple, and other providers once the store's OAuth apps are configured.

## Marketing & Growth

- **Achievement Badges** — Members automatically earn badges when they meet order-count, spend, streak, timing, or referral criteria.
- **Affiliate Notifications & Reports** — Affiliates receive language-aware emails for account, membership, commission, and payout events plus a monthly performance summary.
- **Affiliate Payouts** — Send single or batched affiliate commission payouts through PayPal or Airwallex, with fee/arrival estimates and in-flight cancellation.
- **Affiliate Programs** — Create and run multiple affiliate programs with percentage or fixed commissions, cookie lifetimes, and minimum payout thresholds, and activate, pause, or archive them.
- **Affiliate Recruitment & Approval** — Sign up affiliates, let them apply to programs, and approve, suspend, reject, or auto-approve their accounts and memberships.
- **Automatic & Bulk SEO Fill-In** — Fill missing SEO metadata automatically on save, or generate it for many items in one batch.
- **Automatic Feed Sync** — Feeds regenerate and upload to providers on hourly, daily, or weekly schedules, with sync logging and cleanup of expired feeds.
- **Bulk Voucher Generation & Import/Export** — Generate up to 1,000 unique codes at once and import or export voucher batches as CSV/XLSX.
- **Commissions & Payouts** — Approve, reject, or reverse affiliate commissions and pay affiliates via PayPal or Airwallex through threshold-based or affiliate-requested payouts with full status tracking.
- **Feed Channel Connections** — Connect and manage marketplace provider accounts with encrypted credentials, connection testing, enable/disable, and a designated primary account.
- **Feed Provider Components** — Install and update marketplace feed provider components from the component registry.
- **Gift Cards & Store Credit** — Issue voucher-backed gift cards, check balances, and redeem against orders until the balance is spent.
- **Link Tracking & Attribution** — Affiliates generate unique tracking links whose clicks are recorded and attributed to orders via last-click cookies, with automatic cleanup of expired click data.
- **Loyalty Campaigns** — Merchants run triggered and scheduled multi-step campaigns that award points, send emails, issue rewards, award badges, or move members between segments.
- **Loyalty Points** — Customers earn points on orders, actions, and manual awards against an immutable ledger with accurate, reconciled balances.
- **Loyalty Tiers** — Members are promoted or demoted across tiers based on lifetime points, spend, and orders, with a grace period before demotion.
- **Marketplace Product Feeds** — Generate product feeds for Google Shopping, Meta, and other marketplaces in RSS/XML, CSV/TSV, or JSON, with previews and downloadable exports.
- **Member Segments** — Members are grouped into manual or rule-based segments (by points, spend, orders, recency, and more) for campaign targeting.
- **Payout Provider Accounts** — Connect, test, enable/disable, delete, and set a default account for each payout provider (PayPal, Airwallex).
- **Payout Provider Components** — Install and update payout-provider component packages from the update server with version switching.
- **Payout Status & Webhooks** — Ingest and signature-verify provider webhooks, log them for audit, and reconcile each payout to completed, failed, or cancelled.
- **Provider Credential Protection** — Provider credentials are encrypted at rest and masked in logs.
- **Referral Attribution & Approval** — A referred customer's first delivered order is attributed to the referrer, and each attribution can be approved, rejected, or auto-expired after the review period.
- **Referral Fraud Detection** — Eligibility rules and a 0-100 fraud risk score screen referrals, with high-risk attributions rescreened and auto-rejected to block abuse.
- **Referral Funnel Analytics** — Merchants see referral funnel totals, conversions, reward values, top referrers, and per-referrer stats, with old low-value events pruned on a retention schedule.
- **Referral Links & Invitations** — Each customer gets a unique referral link and QR code they can share, and can email invitations directly to friends.
- **Referral Rewards** — Referrers and, for double-sided programs, referees receive wallet credit, coupons, or perks that are issued, redeemed, expired, or revoked automatically across their lifecycle.
- **Rewards & Redemption** — Members redeem points for rewards or discounts with stock checks, secure codes, fulfillment tracking, and point refunds on cancel or expiry.
- **SEO Content Generator** — Generate meta titles, descriptions, and keywords for products, categories, brands, pages, and blog posts.
- **SEO Coverage & Gaps** — See per-type and overall SEO completeness and list which items are missing or have length issues.
- **SEO Provider Integrations** — Connect, install, and update SEO providers, with one primary provider account enforced per site.
- **Share Event Tracking** — Every share by a logged-in customer or guest is validated and recorded with platform, device, and session details.
- **Share Rewards & History** — Logged-in customers can earn loyalty badges for sharing and view their own share history and totals by platform.
- **Sharing Analytics Dashboard** — Staff can review share totals, trends, platform distribution, top content, and top sharers, with search and filtering of individual share events.
- **Social Proof Share Counts** — Storefront pages can display live per-platform and total share counts for each product or content item.
- **Storefront Share Buttons** — Customers can share products, categories, blog posts, and pages via configurable share buttons that merchants toggle per content type.
- **Voucher Application** — Customers apply and remove discount codes at checkout with eligibility, stacking, and minimum-value rules enforced.
- **Voucher Usage Reporting** — See per-voucher usage counts, unique customers, total and average discount, and recent redemptions.
- **Vouchers & Coupons** — Create percentage, fixed-value, or gift-card discount codes with usage rules and restrictions.

## Email & Communications

- **AI Template Translation** — Templates are auto-translated into multiple languages with a manual verify/reject step for quality control.
- **DNS & Deliverability Setup** — Owners validate SPF/DKIM/DMARC across resolvers, get recommended DNS records, DKIM-sign outgoing mail, and track validation history.
- **Email Queue & Delivery** — Emails are queued respecting customer preferences, sent via the account provider, scheduled for later, and retried or released when held.
- **Email Template Library** — Store owners activate, clone, and render branded transactional email templates with a system fallback always in place.
- **Newsletters** — Owners send a staff-managed newsletter template to resolved recipient lists as individual queued emails.
- **Open & Click Tracking** — Owners see when emails are opened and which links are clicked, with safe redirect handling and room for provider bounce/complaint events.
- **Sending Account Setup** — Owners connect a mail provider with encrypted credentials, test the connection, and generate DKIM keys before going live.
- **SMS Consent & Safe Sending** — Skip messages to customers who opted out by message type, and block real delivery to non-whitelisted numbers while in sandbox mode.
- **SMS Messaging** — Send plain or template-based text messages to customers through a configured SMS provider and track each message's send/delivery state.
- **SMS Provider Components** — Install and update SMS-provider integrations from the component marketplace, activating the selected version.
- **SMS Provider Setup** — Add and configure SMS/WhatsApp provider accounts with validated, encrypted credentials, connection testing, and a default account per channel.
- **Template Versioning** — Every template edit is snapshotted so owners can view history and revert to any prior version.
- **WhatsApp Messaging** — Send pre-approved parameterized WhatsApp template messages and track their outcome in the outbox.

## Blog & Content

- **Announcement Import & Export** — Export announcements with their display settings, expiry, images, translations, and link targets, and import them into another store, updating or removing by title.
- **Announcement Pop-ups** — Open a modal for an announcement with its full body, banner or background image and overlay, a resolved call-to-action link, and close via button, backdrop, or Escape.
- **Blog Posts & Content Modes** — Create, edit, publish, and unpublish blog posts written in rich text or built with the page builder.
- **Categories & Tags** — Organize posts with hierarchical categories and flat tags that readers can browse.
- **Email Subscribers** — Readers subscribe with double opt-in and receive new-post, weekly, or monthly digest emails by their preferences.
- **Multilingual Announcements** — Display announcement title, body, and link text in the shopper's language using stored per-language translations.
- **Reader Engagement** — Show estimated reading time and related posts, and track per-post view counts.
- **RSS Feed** — Publish a configurable RSS feed of recent posts with excerpt or full content and featured-image enclosures.
- **Scheduled Publishing** — Set a future date and time for a post and have it publish automatically.
- **Social Auto-Sharing** — Connect social accounts and auto-share posts on publish, with token refresh and retry of failed shares.
- **Store Announcements** — Show scheduled, priority-ordered announcements to shoppers that auto-hide once they expire, each linking to a product, category, blog post, page, or custom URL.

## Design & Storefront

- **4-Level Token Cascade** — Design tokens resolve in a fixed priority order (brand, theme, component, system) so overrides stay predictable.
- **Automated Form Actions** — Each submission can trigger auto-reply emails, notification emails to your team, and signed webhooks to external systems.
- **Brand Customization** — Change colors, typography, spacing, and component tokens without code and preview the result before publishing.
- **Conditional Logic** — Rules show, hide, require, or preset fields and steps based on what the visitor enters.
- **Custom CSS** — Inject named CSS snippets that are sanitized to strip dangerous rules before they reach the storefront.
- **Dark Mode** — Themes generate dark-mode CSS with responsive variants that respond to the visitor's system preference.
- **Form Builder** — Staff build and edit multi-step forms in a visual builder with reorderable fields and one-click duplication.
- **Form Recycle Bin** — Deleted forms move to a recycle bin where staff can restore them or permanently remove them.
- **Header & Footer Builder** — Assemble header and footer zones from widgets using theme presets and preview each widget as it will render.
- **Page Security Tiers** — Page tiers govern which components and token customizations are allowed on sensitive pages.
- **Response Export** — Download completed responses as a CSV with submission metadata and per-field values.
- **Spam Protection** — A honeypot field blocks bot submissions in the browser; reCAPTCHA settings are configurable but not yet enforced server-side.
- **Submissions & File Uploads** — Visitors submit forms with validated required fields and file attachments, and can save partial drafts to finish later.
- **Theme Developer Tools** — Build themes in an isolated dev session, staging files from the Theme SDK with live CSS compile and validation.
- **Theme System** — Install, activate, and update theme packages from the marketplace, with bundled presets and tokens applied automatically.
- **Trusted Components** — Marketplace components are validated, signed, and integrity-checked before they render, detecting tampering.

## Page Builder

- **Custom Element Builder** — Staff can create, name, list, search, edit, and delete reusable custom elements from an admin builder.
- **Draft, Publish & Version History** — Pages save as numbered drafts, publish with history tracking, and can be reverted to any prior snapshot.
- **Dynamic Data Binding** — Bind element content fields to live model data so elements render real product and record values on the storefront.
- **Element Visibility Rules** — Show or hide page elements based on geography, user, device, time, behavior, and commerce conditions combined into nested AND/OR rule groups.
- **Multilingual Pages** — Translate page and element content per language, via AI or manual entry, with source text kept as fallback.
- **Page Settings & SEO** — Configure per-page metadata, authentication requirement, header/footer, and design settings.
- **Page Templates & Duplication** — Create new draft pages from reusable templates or duplicate an existing page with its nested elements.
- **Visual Element Editor** — Build an element's structure by adding, moving, editing, and deleting nested elements with multi-column layout presets and live canvas preview.
- **Visual Page Builder** — Staff build storefront pages from nested, reorderable elements that render to the live store, with auto-generated preview thumbnails.

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

- **AI Content Translation** — Merchants translate products, pages, and other content into active languages using AI, with per-field locking and job retry/cancel controls.
- **Automatic Currency & Language** — Suggests and stores the right currency and language per visitor based on their detected country, with per-country defaults.
- **Automatic Rate Updates** — Scheduled provider-backed rate fetching for supported currencies, with source-priority selection and cleanup of stale cached rates.
- **Currency Conversion** — Convert amounts between currencies using a resolved rate with optional markup and target-currency rounding.
- **Exchange Rate Providers** — Connect, install, update, and manage external currency-rate providers, with one designated as the site's primary source.
- **External Translation Providers** — Merchants connect and test third-party translation provider accounts with encrypted credentials.
- **Geo Business Rules** — Triggers actions such as setting currency, showing banners, or redirecting based on visitor country, region, mobile, and VPN status.
- **GeoIP Provider Management** — Lets staff configure, test, toggle, and check availability of geolocation providers from the admin.
- **GeoIP Visitor Location Detection** — Resolves each visitor's country, region, and city from their IP with browser-hint fallback, bot/device classification, and manual correction.
- **Locked Order Exchange Rates** — Each order records the exact resolved rate and its source, so historical orders keep their original conversion.
- **Manual Exchange Rates** — Set, edit, activate, lock, and bulk-manage your own currency-pair rates that take precedence over provider rates.
- **Store Languages** — Merchants activate, deactivate, order, and set the default language for their storefront.
- **Storefront Text Customization** — Merchants override, auto-translate, lock, and import/export any storefront UI string per language.
- **Translation Coverage & Progress** — Merchants see how much content is translated per language and track bulk translation job progress before and during runs.
- **Visitor & Traffic Analytics** — Tracks page views and sessions, then reports dashboard KPIs, daily trends, session journeys, campaign attribution, and country/device breakdowns.
- **Visitor Data Retention** — Automatically purges old raw page views and stale visitor records on configurable retention windows while keeping aggregated stats.

## Agentic Commerce

- **Agent Identity Verification** — Every agent request is cryptographically signature-verified against a fetched key directory before it is trusted.
- **Agent Trust & Safety Controls** — Merchants set who may read or buy, block or unblock individual agents, gauge readiness, and kill all agent access instantly.
- **Agentic Checkout** — AI agents can build a cart, add addresses and shipping, and complete a paid checkout on the buyer's behalf.
- **AI Shopping Agent Discovery** — AI shopping agents can discover, search, and read your live catalog through UCP, ACP, and MCP endpoints.
- **Signed Order Mandates** — Each paid agent order gets a merchant-signed AP2 mandate attesting the amount and line items, retrievable by the owning agent.
- **Tamper-Evident Agent Audit Trail** — Every agent event is appended to an HMAC-linked hash chain that can be re-verified to prove it was not altered.

## Enterprise & Security

- **Admin Access Control** — Gate which admin areas each staff member can open based on their roles, including read-only accounts and superuser overrides.
- **Automatic User Provisioning** — First-time SSO sign-ins create a matching staff account, and names are kept in sync from provider claims on each login.
- **Identity Provider Setup** — Store one OpenID Connect provider's endpoints, credentials, and claim mappings, with the client secret encrypted at rest.
- **Mobile App Single Sign-On** — Staff sign in to the admin mobile app through the same identity provider, with per-device token issuance.
- **POS Staff Permissions** — Control which staff can use the POS and what actions and limits apply, merged across all of a user's roles for login.
- **Role & Access Control** — Identity-provider groups set staff and admin permissions, restrict sign-in to staff, and satisfy MFA for SSO users.
- **Single Sign-On (Web)** — Staff sign in to the admin through your existing OpenID Connect identity provider instead of a separate password.
- **Staff Assignment** — Add or remove staff members from a role, with their access permissions refreshed immediately.
- **Staff Roles & Permissions** — Create, edit, clone, and delete staff roles with per-category view or full access levels, plus eight ready-made predefined roles.

## Platform & Administration

- **Add-on Removal** — Uninstall language packs and utilities, cleaning up their data and updating the registry.
- **Advanced Product Type Import** — Carries over bookings, bundles, gift cards, subscriptions, configurable products, and product add-ons into their matching Spwig product types.
- **API Tokens & Access Control** — Programmatic access is gated by database-backed tokens with read/write scopes, type and IP restrictions, expiry, and usage recording.
- **Automatic HTTPS (Let's Encrypt)** — Free Let's Encrypt certificates are issued over HTTP validation and renewed automatically so the store stays on HTTPS.
- **Automatic Retries & Endpoint Health** — Failed deliveries retry with exponential backoff, unhealthy endpoints auto-disable, and admins can retry or re-enable them manually.
- **Bring Your Own SSL Certificate** — Upload your own PEM certificate and key, or fall back to a generated self-signed certificate, and serve it immediately.
- **Component Marketplace** — Browse the catalogue of available components from the update server and install them into the store.
- **Component Marketplace** — Browse, filter, and install themes, widgets, and provider components from the Spwig marketplace with local install status shown.
- **Component Reviews & Ratings** — Read reviews on marketplace components and submit your own 1-to-5 star rating with title and comment.
- **Component Updates** — Keep installed components current by checking for new versions, verifying, installing, and activating them across update channels.
- **Content Link & Image Repair** — Scans migrated product, blog, and category HTML to relink internal hyperlinks to their new Spwig targets and pull inline images into the media library.
- **Cookie Consent & GDPR Audit** — Visitor cookie choices are normalized, classified, and stored as an auditable GDPR consent record.
- **Custom Domain Connection** — Point your own domain at your store, verify ownership, and revert to the default myspwig.com subdomain at any time.
- **Delivery Logs & Health Stats** — View filterable delivery records and per-endpoint 24-hour success rate, response time, and health, with old records auto-purged on a retention schedule.
- **Endpoint Testing & Sandbox Mode** — Send a synthetic test event to check reachability and timing, and block external deliveries while in sandbox mode.
- **Error & Bug Reporting** — Backend and frontend errors are captured, deduplicated by fingerprint, and merchant bug reports are transmitted to the update server for support.
- **Event-Driven Delivery** — Store events are packaged and sent to every subscribed endpoint, synchronously or in the background.
- **Import Job Control & Recovery** — Cancel, retry, or reset import jobs, re-run individual failed items, recover jobs whose worker died, and trim logs from finished jobs.
- **In-Store Help Center & Search** — Merchants and staff find answers via keyword and semantic help search, with context-aware suggestions, view tracking, and helpfulness feedback.
- **Inbound Signature Verification** — Incoming webhooks are authenticated with a timestamped, constant-time HMAC signature check and rejected if invalid or stale.
- **License Management** — Fetch and verify a freshly signed license and secrets from the update server and persist the updated license data.
- **Licensing & Installation Integrity** — License acceptance is recorded, the installation identity is tamper-checked with an HMAC fingerprint, and platform secrets are auto-refreshed before expiry.
- **Migration Rollback** — Reverse an import or store-sync within its rollback window, removing records it created while retaining rows you have since depended on.
- **Paid Component Purchasing** — See which paid components the store's license entitles it to and get a spwig.com purchase link for the rest.
- **Payload Signing & Secrets** — Every outgoing payload is signed with HMAC-SHA256, and endpoint secrets can be rotated on demand.
- **Platform Upgrades** — Check for and run full platform version upgrades with prechecks, package verification, and scheduled hosted upgrade windows.
- **Real-Time Sales Notifications** — Sales, refunds, and developer-signup events are appended to an HQ-only Sales Bell event log for live monitoring.
- **Security Hotfixes** — Detect missing hotfixes for the current platform version and apply or roll them back.
- **Shopper Currency Selection** — Visitors can pick a supported currency for their session, validated against the site's configured currencies.
- **Soft Delete & Restore** — Records are hidden on deletion but retained, so accidentally deleted objects can be restored intact.
- **SSL Monitoring** — Track each certificate's domain, issuer, expiry, and validity, with automatic renewal before certificates lapse.
- **Store Migration Wizard** — Import products, categories, customers, and orders from WooCommerce, Shopify, Magento, or CSV with field mapping and value transformation.
- **Store Settings & Config Validation** — Global site settings persist as a single authoritative record and reject incompatible changes such as disabling in-use warehouse or currency modes.
- **Store-to-Store Sync** — Migrate settings or full data categories between two Spwig stores over token-authenticated endpoints, including media transfer.
- **Trusted Devices & 2FA Remembering** — Users can mark a device as trusted to skip 2FA until it expires or is revoked, with automatic cleanup of expired and revoked devices.
- **Update Rollback & Recovery** — Revert components or hotfixes to a prior working version, with post-install health checks and update locks to guard stability.
- **Webhook Endpoints** — Create, edit, activate, and delete webhook endpoints and pick which store events each one subscribes to.
