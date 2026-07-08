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
url_patterns:
  - /admin/core/sitesettings/
related:
  - getting-started-overview
  - design-themes
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
