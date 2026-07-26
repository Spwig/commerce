---
slug: migration-field-mapping
title_i18n_key: Migration Field Mapping
category: migration
component: migration
keywords:
  - field mapping
  - map csv columns
  - custom fields migration
  - migration wizard step 4
  - woocommerce custom fields
  - shopify metafields
  - category mapping
  - tax settings import
  - price adjustment migration
  - skip csv column
  - meta data json
url_patterns:
  - /admin/migration/migrationjob/
  - /admin/migration/migrationjob/wizard/step4/
related:
  - migration-overview
  - csv-import
  - migrate-from-woocommerce
  - after-migration-review
published: true
---

Every platform names things a little differently — WooCommerce's `regular_price` isn't Shopify's `price`, and a CSV column called `barcode` might be exactly the same thing Spwig expects to see labelled `sku`. Step 4 of the migration wizard, **Configure Field Mapping**, is where you check how your source data will land in Spwig before the import actually runs. This topic covers every block on that page and applies across WooCommerce, Shopify, Magento, and CSV migrations, with platform differences called out where they matter. For credentials and the earlier wizard steps, see [Migrating from WooCommerce](migrate-from-woocommerce) or the equivalent guide for your platform.

## Automatic Mappings

This block shows, for each data type you selected in step 3, a read-only list of source fields and the Spwig field each one lands on — for example a product's `name` mapping to Spwig's product title, or a customer's `email` mapping to the account email. Only the data types you're actually importing appear here; if you didn't select Reviews in step 3, there's no Reviews section on this page.

Because these rows are read-only, there's nothing to configure — they exist so you can sanity-check the mapping before you commit to the import. If a mapping looks wrong for your data, there's no way to override it from this screen; your options are to fix the source data before migrating, or correct the affected records in Spwig after the import completes.

## CSV Column Mapping

This block only appears for CSV migrations, with one table per file you uploaded. Spwig auto-detects likely matches from your column headers — for example a `sku` mapping also recognizes headers like `barcode`, `part_number`, or `item_number` — so in most cases you won't need to touch anything here.

Each CSV column gets a dropdown listing the fields Spwig expects for that file type:

- **products** — `id, name, slug, description, price, sku, stock_quantity, category`
- **categories** — `id, name, slug, description, parent_id`
- **customers** — `id, email, first_name, last_name, phone`
- **orders** — `id, customer_email, order_date, status, total, currency`
- **reviews** — `id, product_id, customer_email, rating, comment, date`

Every dropdown also includes **— Skip this column —**, which excludes that column from the import entirely. Override the auto-detected mapping when your header uses a naming convention Spwig didn't recognize, or when a column genuinely doesn't correspond to anything Spwig imports (an internal note field, for instance) — pick Skip rather than forcing it onto the nearest available field.

## Custom Fields

This block is WooCommerce-only. Spwig samples 10 products, customers, and orders from your store and lists any custom meta fields it finds beyond the standard WooCommerce fields, along with the detected type and an example value.

For each field, choose where it should land:

- **Map to** — Custom Field 1, 2, or 3 for products (Custom Field 1 or 2 for customers and orders), or **Meta Data (JSON)** as a catch-all if you have more custom fields than the numbered slots, or leave it as **— Skip this field —**.
- **Transform** — how the value should be converted on the way in: As Text, As Number (Integer), As Decimal, As True/False (Boolean), As JSON, As Date, As URL, or As Email.

> **Note:** Shopify metafields are not detected by this feature at all — Shopify migrations never show a Custom Fields block, no matter how much metafield data your store has. If you rely on Shopify metafields for product specs, customer attributes, or similar, plan on re-entering that data in Spwig manually after the import.

If Spwig doesn't detect any custom fields in your sample, you'll see a confirmation message instead of this block, and there's nothing further to configure.

## Category Mapping

When some of your source categories don't have an obvious match in Spwig, this block offers three choices: **Create new categories**, **Assign to default category** (an "Uncategorized" catch-all), or **Skip items with unmapped categories**.

> **Note:** Whichever option you pick here, Spwig currently creates a matching category automatically for any product that has source category data, and only falls back to "Uncategorized" for products with no category information at all. You don't need to agonize over this choice — if you end up with categories you don't want, it's quicker to merge or delete them in **Catalog > Categories** after the import than to rely on this setting.

## Tax, shipping, and price settings

The last block, **Tax & Shipping Settings**, has three controls: **Import tax settings**, **Import shipping zones and methods**, and a **Price adjustment** type and value.

The two checkboxes don't currently affect the import — no tax rates or shipping zones come across from your old platform regardless of how they're set. Configure both directly in Spwig once the import finishes: tax rates under **Settings > Tax & Currency**, shipping zones and methods under **Settings > Shipping**.

**Price adjustment** behaves differently depending on your source platform:

- **WooCommerce, CSV, and Shopify migrations** — this control works as described. Choose **Percentage** or **Fixed Amount**, enter a value (for example `10` for a 10% increase, or `-5` for a $5 decrease), and every product's base price is adjusted by that amount as it's imported. It applies to the base price only — sale/compare-at prices come across unadjusted.
- **Magento migrations** — the same control appears on the page, but it has no effect; Magento prices import unchanged no matter what you enter. If you need a blanket price change on a Magento migration, apply it afterward using Spwig's catalog bulk price tools rather than this field.

> **Warning:** If you're migrating from WooCommerce, CSV, or Shopify and don't want prices changed, leave **Price adjustment** set to **None**. It's the one control on this page that genuinely alters your data, and it's easy to assume — incorrectly — that it behaves the same way as the tax and shipping checkboxes right above it.

## Mappings are saved for next time

Whatever you configure on this page is saved with the migration job, and Spwig reuses it as your starting point for future migrations from the same platform — useful if you run a phased migration (categories and products first, orders later) or need to re-import after fixing a data issue. You can also revisit and adjust saved mappings after a migration completes from the **Field Mappings** button on the migration dashboard, without having to rerun the whole wizard.

## Tips

- **Check the Automatic Mappings block even though you can't edit it** — catching a wrong mapping before you click Start Import is much cheaper than fixing hundreds of imported records afterward.
- **Rename ambiguous CSV headers before uploading** if auto-detection didn't recognize them, rather than trying to force a mismatched field through the dropdown.
- **Use Meta Data (JSON) as your custom-field overflow** — it's the only mapping target that doesn't cap out after two or three fields.
- **Don't rely on this page for tax, shipping, or (on Magento) pricing** — treat those as a manual setup task for right after the import, not something the wizard handles for you.
- **Leave Price adjustment at None on your first run** of a new migration, then use a small test batch to confirm the math before applying it to your full catalog.
