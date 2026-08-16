---
slug: product-bulk-actions
title_i18n_key: Product Bulk Actions
category: products
component: catalog
keywords:
  - bulk actions
  - product bulk actions
  - export customs data
  - customs CSV
  - international shipping readiness
  - HS code
  - country of origin
  - customs unit price
  - export license
  - mark as published
  - mark as featured
  - export to CSV
  - delete products
  - product management
  - select products
url_patterns:
  - /admin/catalog/product/
related:
  - add-product
  - stock-bulk-actions
  - sales-regions
published: true
---

The **Products** list lets you act on many products at once instead of opening each one individually. From the **Bulk Actions** dropdown in the toolbar above the product grid you can publish or unpublish products, feature or unfeature them, export data to CSV, check which products are ready for international shipping, or delete them — all in a single step.

Navigate to **Products > All Products** to use these actions.

![The Products list toolbar with three product cards selected and the Bulk Actions dropdown showing every option, including Export Customs Data (CSV) and Check International Shipping Readiness](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Running a Bulk Action

1. Use the filters panel or the **Search** box to narrow down the products you want, if needed
2. Check the box in the top-left corner of each product card you want to include — the **Bulk Actions** bar shows a running count of how many products are selected
3. Choose an action from the **Bulk Actions** dropdown
4. Click **Apply**

Actions that change or export data run immediately; **Delete Selected** asks you to confirm first, since it's the only action here that isn't easily undone from the list itself.

## Available Actions

| Action | What it does |
|--------|---------------|
| **Mark as Published** | Sets the selected products' status to Published so they're visible on the storefront. |
| **Mark as Draft** | Sets the selected products' status to Draft, hiding them from the storefront while you keep editing. |
| **Mark as Featured** | Enables **Is Featured** on the selected products. |
| **Remove Featured** | Disables **Is Featured** on the selected products. |
| **Export to CSV** | Downloads a CSV of the selected products' ID, name, SKU, status, featured flag, and price. |
| **Export Customs Data (CSV)** | Downloads a CSV of customs information for the selected products. See below. |
| **Check International Shipping Readiness** | Shows a summary of which selected products have the customs data they need for international shipments. See below. |
| **Delete Selected** | Moves the selected products to the recycle bin, after a confirmation prompt. |

## Export Customs Data (CSV)

Use this when you need a customs declaration sheet to hand to a freight forwarder, courier, or customs broker — for example, before a large international shipment, or when setting up a new carrier that asks for HS codes and origin data up front.

Select the products, choose **Export Customs Data (CSV)** from the dropdown, and click **Apply**. Spwig downloads a file named `product_customs_data.csv` with one row per product and these columns:

| Column | Source |
|--------|--------|
| **SKU** | The product's SKU |
| **Name** | The product name |
| **HS Code** | The Harmonized System classification code |
| **Country of Origin** | Where the product is manufactured |
| **Customs Unit Price** | The declared value per unit for customs |
| **Export License** | The export license number, if the product requires one |
| **License Expiry** | The export license's expiration date, if set |
| **International Ready** | `Yes` or `No` — whether the product has the minimum data required for international shipping (see below) |

These fields come from the **International Shipping / Customs** section of the product form. If a product is missing one, its column is left blank in the export — fill in the missing data on the product before you rely on this file for an actual shipment.

## Check International Shipping Readiness

Use this to audit a batch of products before you start shipping them internationally, without opening each product individually or waiting on a full CSV export.

Select the products, choose **Check International Shipping Readiness**, and click **Apply**. Spwig checks each selected product against three required fields — **HS Code**, **Country of Origin**, and **Customs Unit Price** — and shows a notification summarizing the result:

- If every selected product has all three fields filled in, you'll see a confirmation that all of them are ready.
- If some are missing data, the notification reports how many are ready and how many aren't, and lists each product that isn't ready along with which fields it's missing (for example, "Blue Ceramic Mug (missing: hs_code, country_of_origin)"). If more than 10 products are missing data, the notification lists the first 10 and tells you how many more there are.

This action only reads data — it doesn't change anything on the products, so it's safe to run as often as you like while you're filling in customs information across your catalog.

**Export License Number** and **Export License Expiry** aren't part of the readiness check. They only apply to controlled or restricted items, so a product can be "ready" for international shipping without them.

## Tips

- Run **Check International Shipping Readiness** on your whole catalog (or a category at a time) before your first international order — it's much faster than discovering a missing HS code when a shipment is already at the border.
- Keep **Export Customs Data (CSV)** for handing to brokers and carriers, and **Check International Shipping Readiness** for your own internal checklist — the CSV is a record, the readiness check is a to-do list.
- Fill in **HS Code**, **Country of Origin**, and **Customs Unit Price** on the product form (under **International Shipping / Customs**) as you add new products, so you don't end up doing it in bulk later.
- The product grid loads more products automatically as you scroll (infinite scroll), and your checkbox selections carry over as new products load in — so you can scroll to build up a large selection before applying an action. Changing a filter or reloading the page clears your selection, though, so apply the action before you adjust filters.
- **Mark as Draft** is a fast way to pull several products off the storefront at once — for example, ahead of a stock recount — without changing anything else about them.
