---
slug: sales-regions
title_i18n_key: Sales Regions
category: products
component: catalog
keywords:
  - sales region
  - region
  - geographic pricing
  - product visibility
  - regional pricing
  - country
  - market
  - region restriction
  - product availability
  - regional catalog
  - territory
  - APAC
  - currency by region
url_patterns:
  - /admin/catalog/salesregion/
  - /admin/catalog/productregionvisibility/
related:
  - inventory-warehouses
  - add-product
  - product-variants
published: true
---

Sales regions let you define geographic markets for your store and control which products are available in each region. This is useful when you sell across multiple countries or territories and need different product catalogs, regional currencies, or stock availability per location.

## What is a sales region?

A sales region is a named geographic area made up of one or more countries. Each region has a default currency, a priority, and can be linked to one or more warehouses. When a customer browses your store, Spwig determines their region based on their location and applies the appropriate currency and product visibility rules.

Common use cases:
- Showing only locally available products to customers in each country
- Assigning region-specific default currencies (e.g., NZD for New Zealand customers)
- Controlling which warehouses fulfil orders for each region
- Hiding products that are not yet available in certain markets

## Creating a sales region

1. Navigate to **Catalog > Sales Regions**
2. Click **+ Add Sales Region**
3. Fill in the region details:

| Field | Description | Example |
|-------|-------------|---------|
| **Region Name** | Display name for this region | `Asia-Pacific` |
| **Region Code** | Short unique identifier | `APAC` |
| **Countries** | ISO country codes included in this region | `["NZ", "AU", "SG", "FJ"]` |
| **Default Currency** | ISO currency code for this region | `NZD` |
| **Priority** | Higher priority regions are matched first | `10` |
| **Active** | Whether this region is currently in use | Checked |

4. Click **Save**

### Country codes

Enter countries as a JSON list of two-letter ISO codes. For example:
- New Zealand and Australia: `["NZ", "AU"]`
- Singapore only: `["SG"]`
- All of Europe: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Priority

If a customer's country matches more than one region, the region with the highest priority number is used. Set a higher priority for more specific regions (e.g., give `NZ` a priority of 20 and `APAC` a priority of 10 so New Zealand customers are matched to the NZ region first).

## Controlling product visibility by region

By default, every product is visible in all regions. To restrict a product to specific regions, use **Product Region Visibility** records.

### Restricting a product to specific regions

1. Navigate to **Catalog > Product Region Visibility**
2. Click **+ Add Product Region Visibility**
3. Select the **Product**
4. Select the **Region**
5. Set **Visible** to on or off as required
6. Click **Save**

Once any visibility record exists for a product, Spwig applies the rules. Products with no visibility records remain visible everywhere.

### Common patterns

**Limit to one region only**

Add one visibility record per region you want to support, setting **Visible** to `Yes` for the allowed regions. Customers in other regions will not see the product.

**Exclude from one region**

Add a single visibility record for the region you want to exclude and set **Visible** to `No`. The product remains visible in all other regions.

### Editing visibility from the product page

You can also manage region visibility directly from the product edit form. On the **Region Visibility** section of the product, you will find an inline table showing all regions and their visibility setting for that product.

## Regional currency

Each region has a default currency. Customers browsing from within that region see prices displayed in the region's currency. The currency used is determined at checkout.

To set up pricing in multiple currencies, configure exchange rates under **Settings > Exchange Rates**. Prices can be converted automatically or set manually per currency.

## Linking warehouses to regions

Warehouses are linked to regions when you create or edit a warehouse under **Catalog > Warehouses**. Each warehouse belongs to one region, which controls which region's stock is used to fulfil orders.

For more detail on warehouses, see the **Inventory and Warehouses** help topic.

## Tips

- Keep region codes short and descriptive (`NZ`, `APAC`, `EU`, `US`) — they are used internally and in logs.
- Use higher priority numbers for smaller, more specific regions so they take precedence over broader catch-all regions.
- If you only sell to one country, you do not need to configure regions at all — Spwig works fine with a single global catalog.
- Test region-based visibility by previewing your store while filtering by a specific region in the admin.
- Product visibility records only need to be created when you want to restrict products. Leaving a product with no visibility records makes it universally available.
- Review your visibility rules whenever you add a new region to ensure existing product restrictions are correct.
