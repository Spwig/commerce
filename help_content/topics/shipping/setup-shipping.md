---
slug: setup-shipping
title_i18n_key: Setting Up Shipping
category: orders-shipping
component: shipping
keywords:
  - shipping
  - carriers
  - rates
  - zones
  - shipping methods
  - FedEx
  - UPS
  - DHL
  - shipping rules
  - free shipping
url_patterns:
  - /admin/shipping/
  - /admin/cart/shippingmethod/
  - /admin/shipping/carrierpreset/
  - /admin/shipping/shippingzone/
related:
  - manage-orders
published: true
---

This guide explains how to configure shipping for your store — from setting up basic shipping methods to connecting live carrier integrations for real-time rates.

## Shipping Overview

Spwig offers two approaches to shipping:

- **Manual Shipping Methods** — Fixed-rate methods you define (e.g., "Standard Shipping — $5.99")
- **Carrier Integrations** — Real-time rates from providers like FedEx, UPS, and DHL

You can use either approach or combine both.

## Shipping Methods

Shipping methods are the options your customers see at checkout. Navigate to **Orders > Shipments** in the sidebar to manage them.

![Shipping methods](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Creating a Shipping Method

1. Click **Add Shipping Method**
2. Fill in the details:
   - **Name** — Display name shown to customers (e.g., "Express Delivery")
   - **Description** — Brief description of the service
   - **Price** — Fixed shipping cost
   - **Estimated Delivery** — Delivery time estimate (e.g., "3-5 business days")
3. Click **Save**

## Shipping Zones

Shipping zones define geographic regions where your shipping methods apply. Navigate to the **Shipping Zones** section to manage them.

![Shipping zones](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Creating a Zone

1. Click **Add Shipping Zone**
2. Configure the zone:
   - **Zone Name** — Internal name (e.g., "US Domestic", "Europe")
   - **Countries** — Select which countries belong to this zone
   - **States/Regions** — Optionally narrow down to specific states
   - **Postal Code Patterns** — Use patterns like "9*" to target specific areas
3. Assign shipping methods to this zone
4. Click **Save**

### Zone Priority

When a customer's address matches multiple zones, the most specific zone takes priority. A zone with state-level targeting takes precedence over a country-level zone.

## Carrier Integrations

Connect with shipping carriers to offer real-time calculated rates at checkout.

![Shipping carriers](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Available Providers

Browse and install shipping providers from the marketplace.

![Shipping providers](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

Supported carriers include:

- **FedEx** — Ground, Express, International
- **UPS** — Ground, 2-Day, Overnight, Worldwide
- **DHL** — Express, eCommerce
- **USPS** — Priority, First Class, Media Mail
- And more available through the Marketplace

### Setting Up a Carrier

1. Go to the shipping providers page and click **Install** on your preferred carrier
2. Follow the setup wizard:
   - **Step 1** — Review provider details
   - **Step 2** — Configure general settings
   - **Step 3** — Enter your API credentials (account number, API key, etc.)
   - **Step 4** — Enable specific services (Ground, Express, etc.)
   - **Step 5** — Test the connection
3. Once connected, the carrier's rates appear automatically at checkout

### API Credentials

Each carrier requires an API account:

- **FedEx** — Register at the FedEx Developer Portal, create an app, and copy your API key and secret
- **UPS** — Register at the UPS Developer Kit, request an access key
- **DHL** — Contact DHL for API credentials through their business portal

## Shipping Rules

Create advanced rules to control when and how shipping methods are offered.

### Common Rules

- **Free shipping over $50** — Set a cart minimum for free shipping
- **Flat rate for lightweight orders** — Fixed rate when order weight is below a threshold
- **Disable express for remote areas** — Hide express options based on postal codes
- **Percentage markup** — Add a handling fee as a percentage of carrier rates

### Creating a Rule

1. Navigate to the shipping rules section
2. Click **Add Rule**
3. Set conditions (cart total, weight, zone, etc.)
4. Define the action (adjust rate, hide method, enable free shipping)
5. Save the rule

Rules are evaluated in order — the first matching rule applies.

## Free Shipping

### Store-Wide Free Shipping

Enable free shipping globally in **Settings > Store Settings**:

- Toggle on **Free Shipping**
- Optionally set a minimum order amount
- Choose which regions qualify

### Promotional Free Shipping

Create time-limited free shipping offers:

1. Go to **Marketing > Sales & Promotions**
2. Create a new promotion
3. Set condition: "Cart total over X"
4. Set action: "Free shipping"
5. Configure start and end dates

## International Shipping

For international orders, ensure your products have:

- **HS Code** — Harmonized System tariff classification
- **Country of Origin** — Manufacturing country
- **Customs Value** — Declared value for customs

These fields are on the **Inventory** tab of each product. Carriers use this information to generate customs documentation automatically.

## Tips

- Start with manual shipping methods to get your store running quickly, then add carrier integrations later.
- Create shipping zones for your most common destinations first.
- Always test your shipping configuration by placing test orders with different addresses.
- Use the rate markup feature to cover handling and packaging costs.
- Set up free shipping thresholds to increase average order value.
