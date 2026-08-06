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
  - region-availability
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

1. Navigate to **Inventory > Sales Regions**. If you don't see it, turn on **Enable Multi-Warehouse** under **Settings > Store Settings > E-Commerce** to reveal the menu item — you don't need to actually use multiple warehouses for this, it only unlocks the link. You can also go straight to `/admin/catalog/salesregion/`.
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

By default, every product is visible in all regions. To restrict a product, open it under **Products > All Products** and set its **Region availability** field (in the Status section) to either allow it only in specific regions or in all regions except specific ones, then choose the regions in the table below that field.

This also determines what shoppers outside a product's available regions see — whether the product is hidden from listings entirely, or shown with a "Does not ship to [region]" notice. See the **Region Availability** guide for the full walkthrough, including that display setting and the storefront Ship-To Selector.

## Regional currency

Each region has a default currency. If your store explicitly supports more than one currency (**Settings > Multi-Currency**), a customer's displayed currency switches to their region's default currency whenever their region changes — whether that's from the automatic region prompt or the Ship-To Selector. Stores with only one currency, or that haven't deliberately enabled multi-currency, always display that single currency regardless of region.

To set up pricing in multiple currencies, configure exchange rates under **Settings > Exchange Rates**. Prices can be converted automatically or set manually per currency.

## Linking warehouses to regions

Warehouses are linked to regions when you create or edit a warehouse under **Catalog > Warehouses**. Each warehouse belongs to one region, which controls which region's stock is used to fulfil orders.

For more detail on warehouses, see the **Inventory and Warehouses** help topic.

## Tips

- Keep region codes short and descriptive (`NZ`, `APAC`, `EU`, `US`) — they are used internally and in logs.
- Use higher priority numbers for smaller, more specific regions so they take precedence over broader catch-all regions.
- If you only sell to one country, you do not need to configure regions at all — Spwig works fine with a single global catalog.
- Only set a product's **Region availability** away from **Available in all regions** when you actually need to restrict it — the default keeps products universally available with no upkeep.
- Review each product's region rules whenever you add a new Sales Region, so restrictions still match what you intend.
- Add the Ship-To Selector to your header (see the **Region Availability** guide) so you can switch regions yourself and check restricted products behave as expected.
