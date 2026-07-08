---
slug: shipping-providers
title_i18n_key: Shipping Providers
category: orders-shipping
component: shipping
keywords:
  - shipping provider
  - carrier
  - FedEx
  - UPS
  - shipping zone
  - shipping promotion
  - rate table
  - tracking
  - label
  - shipping rates
url_patterns:
  - /admin/shipping/provideraccount/
  - /admin/shipping/shippingzone/
  - /admin/shipping/shippingpromotion/
related:
  - setup-shipping
published: true
---

Shipping providers connect your store to carrier APIs for live shipping rates, label generation, and package tracking. Spwig supports major carriers worldwide and also lets you set up manual rate tables for carriers without API integration.

![Shipping providers](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Available Carriers

| Carrier | Regions | Key Features |
|---------|---------|-------------|
| **FedEx** | Global | Live rates, label printing, tracking, multi-package |
| **UPS** | Global | Live rates, label printing, tracking, address validation |
| **USPS** | United States | Domestic and international rates, tracking |
| **NinjaVan** | Southeast Asia | Last-mile delivery, cash on delivery support |
| **Canada Post** | Canada | Domestic and international, parcel and letter rates |
| **Australia Post** | Australia | Domestic and international, parcel and express |

## Connecting a Carrier

Navigate to **Settings > Shipping Providers** and click **Connect Provider** to launch the setup wizard.

### Step 1: Select Provider

Choose from the available shipping carriers. Each card shows the carrier's supported regions and features.

### Step 2: Setup Instructions

Review the carrier-specific setup guide:
- How to create a developer/business account with the carrier
- Where to find your API credentials
- Required account settings (e.g., shipper number, meter number)

### Step 3: Enter Credentials

Enter the API credentials for your carrier account. The required fields vary by carrier:

- **API Key / Secret** — Authentication credentials
- **Account Number** — Your carrier account or shipper number
- **Meter Number** — Required by some carriers (e.g., FedEx)
- **Sandbox Mode** — Enable to test with the carrier's sandbox API before going live

### Step 4: Test Connection

Click **Test Connection** to verify your credentials. The wizard confirms:
- API authentication succeeds
- Account permissions are valid
- Rate queries return expected results

### Step 5: Configure and Save

Finalize the settings:
- **Active** — Enable or disable the carrier
- **Display Name** — The name shown to customers at checkout
- **Origin Address** — The warehouse or fulfillment address for rate calculations

## Shipping Zones

Shipping zones define geographic areas for rate calculations. Navigate to **Settings > Shipping Zones** to manage them.

### Creating a Zone

1. Click **+ Add Zone**
2. Give the zone a name (e.g., "Domestic", "Europe", "Asia Pacific")
3. Define the zone's coverage using one or more of:
   - **Countries** — Select specific countries
   - **States/Provinces** — Narrow to specific regions within a country
   - **Postal Code Patterns** — Match postal/ZIP codes using patterns (e.g., "90*" for Los Angeles area)
4. Set the **Priority** — When zones overlap, the highest priority zone is used

### Zone Matching

When a customer enters their shipping address at checkout, the system:
1. Checks postal code patterns first (most specific)
2. Then state/province matches
3. Then country matches
4. Uses the highest-priority matching zone

## Shipping Promotions

Shipping promotions apply conditional modifiers to shipping rates. Navigate to **Settings > Shipping Promotions** to configure them.

### Promotion Types

| Promotion Type | Description |
|-----------|-------------|
| **Discount %** | Reduce the shipping rate by a percentage |
| **Discount Fixed** | Reduce the shipping rate by a fixed amount |
| **Override Cost** | Override the rate with a specific amount |
| **Free Shipping** | Set the shipping cost to zero |
| **Surcharge %** | Add a percentage surcharge to the rate |
| **Surcharge Fixed** | Add a fixed surcharge to the rate |

### Conditions

Each promotion can have one or more conditions that must be met:

| Condition | Example |
|-----------|---------|
| **Cart Value** | Free shipping on orders over $100 |
| **Total Weight** | Surcharge for orders over 30 kg |
| **Item Count** | Discount for orders with 5+ items |
| **Shipping Zone** | Apply promotion only to domestic shipments |
| **Shipping Method** | Apply to specific carrier methods |
| **Products** | Special rates for specific products |
| **Customer Group** | VIP customers get free shipping |
| **Date Range** | Holiday shipping promotions |

### Promotion Priority

- Promotions are evaluated in priority order (lowest number first)
- **Stop Further Promotions** — When enabled, if this promotion matches, no further promotions are checked
- Multiple promotions can stack (e.g., a 10% discount promotion plus a free shipping threshold promotion)

## Rate Tables

Rate tables provide tiered pricing based on order attributes. Navigate to **Settings > Shipping Rate Tables** to configure them.

### Table Types

Create rate tiers based on:
- **Weight** — Price tiers by total order weight (e.g., 0-1 kg = $5, 1-5 kg = $10)
- **Order Value** — Price tiers by cart subtotal
- **Quantity** — Price tiers by item count

### Creating a Rate Table

1. Click **+ Add Rate Table**
2. Name the table and select the tier type
3. Add tiers with min/max ranges and prices
4. Assign the rate table to a shipping zone

Rate tables are useful when you don't use carrier API rates and want to define your own pricing structure.

## Shipping Packages

Define standard packaging sizes for accurate rate calculations. Navigate to **Settings > Shipping Packages**.

For each package type, set:
- **Name** — Description (e.g., "Small Box", "Large Flat Rate")
- **Dimensions** — Length, width, height
- **Max Weight** — Maximum weight the package can hold
- **Default** — Use this package when no specific packaging is assigned

Carriers use package dimensions for dimensional weight calculations, which can affect shipping rates.

## Manual Carriers (Carrier Presets)

For carriers without API integration, create manual carrier presets:

1. Navigate to **Settings > Carrier Presets**
2. Click **+ Add Preset**
3. Configure:
   - **Carrier Name** — Display name for checkout
   - **Tracking URL Template** — URL pattern with a `{tracking_number}` placeholder (e.g., `https://track.carrier.com/?id={tracking_number}`)
   - **Estimated Delivery** — Delivery time range to display to customers
4. Pair with a rate table for pricing

Manual carriers provide tracking links and delivery estimates without live API integration.

## Multi-Warehouse Shipping

If you have multiple warehouses, shipping can be calculated from different origins:

- **Country-Specific Warehouse** — Assign warehouses to specific countries for shorter shipping distances
- **Fallback Chain** — Define which warehouse ships when the primary warehouse is out of stock
- **Per-Product Assignment** — Some products may only ship from specific warehouses

The system automatically selects the best warehouse based on the customer's location and product availability.

## Tips

- Connect carrier APIs for **live rates** whenever possible — they're more accurate than flat-rate tables and adjust for weight, dimensions, and destination.
- Create a **"Rest of World"** shipping zone as a catch-all for countries not covered by specific zones.
- Use the **Free Shipping** promotion type with a cart value condition as a sales incentive (e.g., "Free shipping on orders over $75").
- Test shipping rate calculations with different addresses and cart contents before going live.
- Set up **Carrier Presets** with tracking URL templates for any local carriers that don't have API integrations — customers still get tracking links.
- Use **Shipping Packages** to get accurate dimensional weight pricing from carriers like FedEx and UPS.
