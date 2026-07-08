---
slug: digital-products
title_i18n_key: Digital Products
category: products
component: catalog
keywords:
  - digital
  - download
  - license
  - software
  - digital delivery
  - license key
  - license provider
  - downloadable
  - file delivery
url_patterns:
  - /admin/catalog/licenseprovider/
  - /admin/catalog/product/
related:
  - add-product
  - product-variants
published: true
---

Digital products let you sell downloadable files, software licenses, and other non-physical goods. Spwig supports standalone digital products, as well as hybrid products that combine physical and digital delivery.

![License providers](/static/core/admin/img/help/digital-products/license-providers.webp)

## Types of Digital Products

### Standalone Digital Product

Set the **Product Type** to **Digital Product** for items that are purely digital:
- Software applications
- E-books and PDFs
- Music and audio files
- Digital artwork and templates

### Hybrid Products

Any product type can include digital delivery by checking **Is Digital Product** on the Basic Info tab. This is useful for:
- **Variable digital products** — Software with Basic/Pro/Enterprise editions
- **Customizable digital products** — Custom-designed digital assets
- **Physical + digital bundles** — A book that includes a digital download

## Setting Up a Digital Product

### Step 1: Create the Product

1. Navigate to **Products > All Products** and click **+ Add Product**
2. Set **Product Type** to **Digital Product** (or check **Is Digital Product** on another product type)
3. Fill in the product details (name, description, price)
4. Save the product

### Step 2: Add downloadable files

After saving the product, a **Digital Assets** section appears at the top of the product form. Click **Add another Digital Asset** to upload the files customers will receive after purchase. For each file, you can set:

- **File** — Upload the file to deliver to customers.
- **Filename** — Display name shown to customers in their downloads.
- **Version** — Optional version label (e.g., "v2.1.0").
- **Requires License** — Check if this file requires a license key to activate.
- **Download Limit** — Maximum number of times the file can be downloaded (0 = unlimited).
- **Expiration Days** — Number of days the download link remains active after purchase.
- **Is Active** — Uncheck to temporarily disable downloads for this file.

### Step 3: Configure license delivery (optional)

If your digital product requires license keys:

1. Navigate to **Products > License Providers**
2. Connect a license provider (see below)
3. On the product edit form, scroll to the **Licensing** section and assign the license provider

## License Providers

License providers are external services that generate and manage software license keys automatically when a customer purchases your product.

### Available Provider Types

| Provider | Description |
|----------|-------------|
| **Spwig Built-in License Server** | Simple license key generation built into the platform |
| **Keygen.sh** | Full-featured license management API |
| **LicenseSpring** | Enterprise license management |
| **Cryptlex** | Software licensing with offline support |
| **Custom API** | Connect any license system via REST API |

### Connecting a license provider

1. Navigate to **Products > License Providers**
2. Click **+ Add License Provider**
3. Fill in the provider details:
   - **Name** — A label for this connection (e.g., "Keygen Production")
   - **Provider Type** — Select the service you are integrating with
   - **API Endpoint** — The provider's API base URL
   - **API Key** — Your authentication key or token
   - **API Secret** — Secondary credential if required by the provider
4. Configure sync settings: when to sync (on order, on activation, on deactivation)
5. Save and use the **Test Connection** action to verify the credentials work

### Provider Card

Each connected provider shows:
- **Status badges** — Active/Inactive and connection status
- **API endpoint** — The configured server URL
- **Sync capabilities** — Order, Activation, and Deactivation sync support
- **Action buttons** — Configure, Test, and Sync Now

### Sync Capabilities

License providers can sync on three events:

- **Order** — Automatically generate a license key when a customer completes a purchase
- **Activation** — Track when a customer activates their license
- **Deactivation** — Handle license deactivation for refunds or transfers

## Customer Experience

### After Purchase

When a customer buys a digital product:

1. **Order confirmation** — Shows that digital delivery is included
2. **Email delivery** — Download links and/or license keys are sent automatically
3. **Account page** — Customers can access their downloads from their account dashboard
4. **Download page** — Secure, time-limited download links

### Download Security

Digital file downloads are protected by:
- Unique, time-limited download tokens
- Optional download count limits
- Expiry dates after which links become inactive
- Login requirement (for registered customers)

## Tips

- Set reasonable download limits (3-5 downloads) to prevent abuse while allowing re-downloads.
- Use expiry days that match your support period (e.g., 365 days for a year of access).
- Test the full purchase flow with a test order to ensure download links and license keys are delivered correctly.
- For software products, connect a license provider to automate key generation rather than managing keys manually.
- Use the hybrid product feature when selling physical goods that include digital extras (e.g., printed book + PDF).
