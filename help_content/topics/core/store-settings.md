---
slug: store-settings
title_i18n_key: Configuring Store Settings
category: store-config
component: core
keywords:
  - settings
  - configuration
  - store info
  - timezone
  - currency
  - branding
  - logo
  - favicon
  - language
  - maintenance
  - SEO
  - inventory intelligence
  - reorder lead time
  - safety stock
  - sales velocity
  - backorders
  - low stock alerts
  - tax id
  - invoice footer
  - packing slip
  - document logo width
  - PDF invoice logo
  - communications
  - double opt-in
  - marketing consent
  - GDPR
  - TCPA
  - preference center
  - unsubscribe reasons
  - SMS verification
url_patterns:
  - /admin/core/sitesettings/
related:
  - getting-started-overview
  - design-themes
  - email-configuration
published: true
---

Store Settings is the central place to configure your store's identity, localization, branding, and operational preferences. Navigate to **Settings > Store Settings** to get started.

![Store settings general tab](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## General Tab

The **General** tab holds your store's core identity settings.

### Store Identity

- **Store Name** — The display name shown in page titles, emails, and the admin header.
- **Tagline** — A short description of your store, used in SEO and social sharing.
- **Site URL** — Your store's public web address. This is used in emails, sitemap generation, and link building.

### Contact Information

- **Contact Email** — Receives order notifications and is shown in customer communications.
- **Phone Number** — Optional support phone number displayed in the footer and emails.

### Business Address

Enter your complete address (street, city, state, postal code, country). This is used for:
- Shipping origin calculations
- Tax calculations
- Legal requirements and invoices

## Branding

### Logo

Upload your store logo (PNG or SVG recommended, ~200x50px with transparent background). The logo appears in:
- The storefront header
- Email templates
- The admin panel

### Favicon

Upload a square favicon (ICO or PNG, 32x32px). It appears as:
- The browser tab icon
- Bookmark icon
- Mobile home screen icon

## Localization

### Default Language

Choose your store's primary language from 10 supported options:

| Language | Code |
|----------|------|
| English | en |
| Spanish | es |
| French | fr |
| German | de |
| Portuguese | pt |
| Japanese | ja |
| Chinese Simplified | zh-hans |
| Chinese Traditional | zh-hant |
| Russian | ru |
| Arabic | ar |

The default language controls the admin interface language and the fallback for storefront content.

### Timezone

Select your store's timezone for accurate order timestamps, scheduled promotions, and reporting.

### Currency

- **Default Currency** — The primary currency for pricing and accounting.
- **Multi-Currency** — Enable to let customers view prices in their preferred currency with automatic conversion using real-time exchange rates.

Configure additional currencies in **Settings > Store Settings > Currency**.

## E-Commerce Settings

### Guest Checkout

Allow purchases without creating an account:
- Faster checkout flow
- Lower friction for first-time buyers
- Captures less customer data

### Account Creation Timing

Control when customers are prompted to create an account:

| Option | Description |
|--------|-------------|
| **After Purchase (Recommended)** | Prompt for account creation after a successful order — leverages post-purchase goodwill for best conversion |
| **During Checkout** | Create an account before payment is processed |
| **Before Checkout** | Require an account before shopping (not recommended — reduces conversion) |

You can also set a custom **Account Creation Message** to explain the benefits of registering.

### Inventory Defaults

- **Track Inventory** — Enable stock tracking globally
- **Low Stock Threshold** — Stock level at which low-stock alerts are sent to the admin email (default: 10 units)

### Inventory Intelligence

![Inventory Intelligence card showing Default Reorder Lead Time, Safety Stock Multiplier, Velocity Calculation Window, Allow Backorders by Default, and Low Stock Alert Frequency fields](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

These settings tune the automatic reorder, safety-stock, and sales-velocity calculations, and control how out-of-stock and low-stock situations are handled.

- **Default Reorder Lead Time (Days)** — How many days it typically takes to receive restock from your supplier once you place an order (default: 14). Forecasting uses this to flag products that need reordering *now* to avoid a stockout before the new stock arrives.
- **Safety Stock Multiplier** — A buffer applied on top of expected demand to absorb sales spikes or supplier delays. For example, a multiplier of `1.5` builds in a 50% buffer above your calculated safety stock; `2.0` doubles it. Raise this for products where running out is costly (best sellers, seasonal items); lower it for slow-moving stock you don't want to over-order.
- **Velocity Calculation Window (Days)** — The look-back window Spwig uses to calculate each product's sales velocity, which in turn drives reorder suggestions and days-of-supply figures (default: 30). A shorter window reacts faster to recent demand shifts; a longer window smooths out seasonal spikes so a single busy week doesn't skew the forecast.
- **Allow Backorders by Default** — The initial backorder setting applied to newly created products (off by default). Each product can still override it individually on its own product page, and existing products keep whatever setting they already have — changing this only changes the default new products start with, it does not retroactively update your catalog.
- **Low Stock Alert Frequency** — How often your Spwig mobile app is notified about low stock: **Real-time** sends a push notification the moment a product crosses its low-stock threshold; **Daily Digest** and **Weekly Summary** instead send a single push summarizing all currently low-stock products on that schedule. This setting only takes effect while **Low Stock Alerts** (Email Settings, below) is enabled — with alerts off, no notifications go out on any frequency.

### Documents & Invoicing

![Documents & Invoicing card showing Tax ID / VAT Number, Invoice Footer Text, Packing Slip Footer Text, and Document Logo Width fields filled in with example values](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

These fields populate the invoices and packing slips Spwig generates for orders — for example when a merchant downloads or emails a PDF invoice, or prints a packing slip for a shipment.

- **Tax ID / VAT Number** — Your business tax identification number. Printed on generated invoices so they meet local tax documentation requirements.
- **Invoice Footer Text** — Free text shown at the bottom of every generated invoice. Common uses: payment terms ("Payment due within 30 days"), a thank-you message, or bank transfer details.
- **Packing Slip Footer Text** — Free text shown at the bottom of every generated packing slip. Common uses: return instructions or a note to the warehouse/fulfillment team.
- **Document Logo Width (px)** — The width of your store logo as it appears on generated PDF invoices and packing slips (default: 200px). Height scales automatically to match, so your logo's proportions are preserved. The logo image itself comes from your **Logo** (Branding, above) — SVG logos aren't drawn on PDF documents, so upload a PNG or JPG version of your logo if you use vector art on the storefront.

## Email Settings

Configure email delivery settings in **Settings > Email Accounts** and **Settings > Email Templates**. See [Email Configuration](/help/email-configuration) for full details.

Key email settings available in Store Settings:

- **Order Confirmation Emails** — Toggle automatic confirmation emails on or off
- **Shipping Notification Emails** — Toggle shipping update notifications on or off
- **Low Stock Alerts** — Send alerts to the admin email when stock falls below the threshold
- **Email Delivery Mode** — Live (normal delivery), Paused (hold all emails), or Log Only (record but never send)
- **Test Redirect Email** — Redirect all outgoing emails to a single address for testing

## Security Settings

### Two-Factor Authentication (2FA)

Control whether staff are required to use two-factor authentication:

| Setting | Description |
|---------|-------------|
| **Optional** | Staff can choose to enable 2FA but it is not required |
| **Recommended** | Staff see a prompt encouraging them to set up 2FA |
| **Required** | Staff cannot access the admin until 2FA is enabled |

- **Grace Period (Days)** — How many days staff have to set up 2FA after enforcement is enabled
- **Allow Trusted Devices** — Let staff skip 2FA verification on recognized devices for a set number of days

## Cookie Consent

Configure the cookie consent banner shown to storefront visitors:

- **Cookie Consent Enabled** — Show or hide the cookie banner
- **Banner Position** — Where the banner appears on screen (bottom bar, corner popup, etc.)
- **Consent Mode** — Simple notice, opt-in, or opt-out
- **Banner Title and Text** — Customizable heading and description shown to visitors
- **Category Descriptions** — Separate descriptions for analytics, marketing, and functional cookies

All banner text fields support translations for multilingual stores.

## Communications

The **Communications** tab controls how your store obtains, confirms, and lets customers manage consent for marketing email and SMS. These settings shape your legal compliance posture (GDPR for email, TCPA for SMS), so review them with your own legal counsel before launch — Spwig provides the controls, not the advice.

![Communications tab showing Email Marketing Consent, Preferences & Unsubscribe, and SMS Consent cards](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Email Marketing Consent

- **Enable Double Opt-In for Marketing Emails** — When on, a customer who opts into marketing email is sent a confirmation email and must click the link in it before Spwig sends them any marketing message. When off, ticking the marketing opt-in box is enough on its own. Enabled by default, in line with GDPR best practice.
- **Default Marketing Opt-In State** — The initial marketing opt-in state applied to newly created customer accounts. Off by default (GDPR opt-out), so new customers start unsubscribed from marketing email until they actively opt in.

When double opt-in is on, opting in triggers a confirmation email with a verification link. Until the customer clicks it, they're recorded as opted in but unconfirmed, and marketing sends skip them — transactional email (order confirmations, shipping updates, password resets) is never affected by this setting.

### Preferences & Unsubscribe

- **Enable Customer Preference Center** — When on, customers can manage their email and SMS preferences from a self-service page linked from their account dashboard. When off, that page and its supporting API return unavailable and the dashboard link is hidden. One-click unsubscribe links in your emails keep working either way — that escape hatch is required for compliance and isn't affected by this toggle.
- **Collect Unsubscribe Reasons** — When on, the one-click unsubscribe page asks the customer for a brief reason before confirming: *I receive too many emails*, *The content isn't relevant to me*, *I never signed up for this*, *I'm no longer interested*, or *Other*. The reason a customer selects is recorded to the consent audit trail so you can review unsubscribe patterns over time.

### SMS Consent

- **Require SMS Verification** — When on (the default), a customer must verify their phone number with a one-time code before Spwig sends them any SMS, including marketing texts. When off, ticking the SMS opt-in box is enough on its own to start sending. This default was changed to **on** for TCPA safety — turn it off only if you have another verification step in your signup flow.

## Maintenance Mode

Enable maintenance mode to take your store offline temporarily:
- Displays a custom maintenance message to visitors
- You can link a **Maintenance Page** built in the Page Builder for a fully branded maintenance experience
- Restricts access to admin users only
- Useful during major updates or migrations

## Social Media

Link your store's social media profiles. These appear in the footer and email templates:

- **Facebook URL**
- **Twitter URL**
- **Instagram URL**
- **LinkedIn URL**

## SEO Defaults

Set default meta tags used when pages do not have their own SEO settings:

- **Meta Title** — Default page title (60 characters max)
- **Meta Description** — Default description shown in search results (160 characters max)
- **Meta Keywords** — Default comma-separated keywords

## Tax Settings

Configure tax collection at **Settings > Tax Settings**:

1. **Calculation Method** — By shipping address, billing address, or store location
2. **Tax Rates** — Define rates by region and product tax class
3. **Tax Display** — Show prices with tax, without tax, or both

## Tips

- Set your timezone correctly before processing any orders — it affects all timestamps and reports.
- Enable guest checkout to improve conversion rates.
- Fill in your business address for accurate shipping and tax calculations.
- Upload both a logo and favicon for a professional, branded experience.
- Use the **After Purchase** account creation timing for best registration rates.
- Enable two-factor authentication enforcement for staff to protect your store admin.
- Test email flows using the **Test Redirect Email** setting before going live.
- Set the **Default Reorder Lead Time** to match your slowest regular supplier — reorder forecasting applies this single value across your whole catalog, so err on the side of your longest-lead-time products.
- Shorten the **Velocity Calculation Window** if you run frequent promotions or restocks and want forecasting to react quickly to the last few days' sales; lengthen it for a steadier, less spike-prone view of demand.
- If you turn on **Allow Backorders by Default**, remember it only sets the starting point for products created *after* the change — revisit existing products individually if you want backorders enabled across your current catalog too.
- Match **Low Stock Alert Frequency** to how actively you manage stock: **Real-time** for fast-moving catalogs where every stockout risk needs immediate attention, **Daily Digest** or **Weekly Summary** to avoid alert fatigue on a larger catalog.
- Fill in your **Tax ID / VAT Number** and footer text before your first real invoice goes out to a customer — both fields are blank by default.
- If your **Logo** is an SVG, upload a PNG or JPG version too — **Document Logo Width** has no effect on PDFs because Spwig can't draw SVG artwork on generated invoices and packing slips.
- Leave **Enable Double Opt-In for Marketing Emails** on unless you have a specific reason to turn it off — it's the safer default for GDPR and it protects your sender reputation by keeping unverified addresses off your marketing sends.
- Leave **Default Marketing Opt-In State** off. Pre-checking marketing consent for new accounts undermines the GDPR opt-in requirement even if a customer could technically un-tick it.
- Don't disable **Enable Customer Preference Center** just to simplify your account dashboard — without it, customers can still unsubscribe from a single message type, but they lose the ability to fine-tune preferences (e.g. keep shipping updates but drop the newsletter).
- Keep **Require SMS Verification** on unless your signup flow already confirms phone numbers another way (e.g. an SMS-based login) — the setting exists specifically to keep you inside TCPA rules.

## Troubleshooting

**Changes not appearing on the storefront:**
- Clear your browser cache
- Run a cache clear from the admin panel
- Check if maintenance mode is accidentally enabled

**Emails not sending:**
- Verify your email provider settings in Email Configuration
- Check that the **Email Delivery Mode** is set to **Live**
- Ensure the **Test Redirect Email** is blank if you want emails sent to real recipients

**Currency conversion not working:**
- Verify your exchange rate provider is connected
- Check API credentials in the exchange rate settings
- Try updating rates manually

**Marketing emails aren't reaching customers who opted in:**
- Check whether **Enable Double Opt-In for Marketing Emails** is on — if so, the customer must click the confirmation link in the verification email before marketing sends resume
- Ask the customer to check spam/junk for the confirmation email
- Confirm the customer's marketing opt-in is still on in their preferences — an unsubscribe click turns it back off

**Customers say they can't find the preference center:**
- Check that **Enable Customer Preference Center** is on — when it's off, the dashboard link is hidden and the page is unavailable by design
- The unsubscribe link in any marketing email always works regardless of this setting, so point customers there as a fallback
