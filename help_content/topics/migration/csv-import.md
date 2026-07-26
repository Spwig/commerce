---
slug: csv-import
title_i18n_key: Importing from CSV Files
category: migration
component: migration
keywords:
  - CSV import
  - import from CSV
  - migrate from BigCommerce
  - migrate from PrestaShop
  - migrate from Squarespace
  - migrate from Wix
  - CSV template download
  - column mapping CSV
  - products CSV required
  - spreadsheet import
  - bulk import products customers orders
  - CSV migration errors
url_patterns:
  - /admin/migration/migrationjob/
  - /admin/migration/migrationjob/wizard/step1/
  - /admin/migration/migrationjob/wizard/step2/
  - /admin/migration/migrationjob/wizard/step4/
related:
  - migration-overview
  - migration-field-mapping
  - after-migration-review
  - migration-troubleshooting
published: true
---

CSV import is the fallback migration route for any store Spwig doesn't connect to directly. If you're coming from BigCommerce, PrestaShop, Squarespace, Wix, a spreadsheet you've maintained by hand, or a bespoke system with no API Spwig understands, this is where you land — export your data to CSV files and upload them here instead of connecting live.

This guide covers when to use CSV, what it cannot bring across, the five files involved, how to prepare them, and how column mapping works.

## When to Use CSV Instead of an API Connection

Spwig connects directly to WooCommerce, Shopify, and Magento 2/Adobe Commerce — see [Data Migration Overview](migration-overview) for those. For any other platform, CSV is your only option; there is no direct integration for BigCommerce, PrestaShop, Squarespace, or Wix. It's also the right choice if you're consolidating data from a spreadsheet, retiring a custom-built store, or want to control exactly what gets imported by curating the files yourself.

## What CSV Cannot Do

Before you prepare anything, know what this route leaves behind — this is the single biggest source of surprise for merchants using CSV import:

- **No product images.** Products import with no images attached; upload them afterward.
- **No variants.** Every product is created as a simple product. Rebuild size/color/style structures in Spwig after the import.
- **No coupons.** Discount codes and promotions aren't part of the CSV format.
- **No blog content.** There is no CSV file for posts or articles.

None of this blocks the import — it just means products need follow-up work once they're in Spwig. See [After Your Migration](after-migration-review) for the full post-import checklist.

## The Five Files

The wizard's CSV step offers five file inputs, each with a **Download Template** button. Start from these templates rather than building files from scratch — they guarantee the right column names and let auto-detection do more of the work in step 4.

| File | Required? |
|---|---|
| Products | **Required** |
| Categories | Optional |
| Customers | Optional |
| Orders | Optional |
| Reviews | Optional |

Products is the only file Spwig insists on — the rest can be left empty if you don't have that data yet.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: Step 2 with CSV selected, showing the five file inputs and their Download Template buttons
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Products (Required)

| Column | Description |
|---|---|
| `id` | Unique identifier in your source data; not shown to customers. |
| `name` | The product title. **Essential.** |
| `slug` | URL-friendly version of the name; auto-generated from `name` if blank. |
| `description` | The description shown on the storefront. |
| `price` | The product's regular price. **Essential.** |
| `sku` | Stock keeping unit — used for matching when **Skip existing items** is enabled. |
| `stock_quantity` | Units currently in stock. |
| `category` | Category name this product belongs to. Must match a `name` in your categories file. |

### Categories

| Column | Description |
|---|---|
| `id` | Unique identifier in your source data. |
| `name` | The category name. **Essential.** |
| `slug` | URL-friendly version of the name; auto-generated if blank. |
| `description` | Category description text. |
| `parent_id` | The `id` of this category's parent. Blank means top-level. |

### Customers

| Column | Description |
|---|---|
| `id` | Unique identifier in your source data. |
| `email` | Customer's email address. **Essential** — links orders and reviews to the right customer. |
| `first_name` | Customer's first name. |
| `last_name` | Customer's last name. |
| `phone` | Customer's phone number. |

### Orders

| Column | Description |
|---|---|
| `id` | Unique identifier in your source data. |
| `customer_email` | Email of the customer who placed the order. **Essential** — links the order to a customer record. |
| `order_date` | The date the order was placed. |
| `status` | The order's status (e.g. completed, processing). |
| `total` | The order total. **Essential.** |
| `currency` | Currency code for the order total. |

### Reviews (Optional)

| Column | Description |
|---|---|
| `id` | Unique identifier in your source data. |
| `product_id` | The `id` of the product being reviewed, matching your products file. **Essential** — links the review to the right product. |
| `customer_email` | Email address of the reviewer. |
| `rating` | The star rating given. |
| `comment` | The review text. |
| `date` | The date the review was posted. |

## Preparing Your Files

- **Save as UTF-8** to avoid garbled accented characters, especially from a different source encoding.
- **Quote fields containing commas** — wrap a description or name containing a comma in double quotes so it isn't misread as a column break.
- **Include a header row.** The first row must contain your column names — a file with no header row is rejected.
- **Build category hierarchy with `parent_id`.** Give each category a unique `id`, then set a subcategory's `parent_id` to its parent's `id`. Blank means top-level.
- **Link orders to customers with `customer_email`**, matched against the `email` column in your customers file (or a guest record is created), rather than relying on internal ID numbers, which rarely line up across platforms.
- **Link reviews to products with `product_id`**, matching a value in the `id` column of your products file, or that review is skipped.

## Mapping Columns in Step 4

Step 4 shows a CSV Column Mapping panel. Spwig scans your headers and auto-detects likely matches against a list of common aliases — a `sku` field also matches `barcode`, `part_number`, or `item_number`, for example. Headers exported directly from another platform often map correctly with no manual work at all.

For each column, you can accept the auto-detected guess, override it by picking a different destination field, or choose "— Skip this column —" to exclude it. Mappings are saved and reused on future CSV migrations. See [Migration Field Mapping](migration-field-mapping) for the full picture of step 4, including automatic field mappings, category mapping, and the tax/shipping options.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Step 4 CSV Column Mapping panel showing auto-detected mappings with override dropdowns
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Common Errors and What They Mean

| Error | Meaning |
|---|---|
| `Products CSV is required.` | You tried to proceed without uploading a products file. It's the only file Spwig requires — upload one to continue. |
| `{Type} CSV has no headers.` | The named file's first row is empty or missing. Add a header row with column names and re-upload. |
| `{Type} CSV could not be read: ...` | Spwig couldn't parse the named file — usually a corrupted file, wrong encoding, or a file that isn't actually CSV despite its extension. Re-export it and confirm it opens cleanly before uploading again. |

## Running the Import

Once mapping is confirmed, start the migration from step 5. It runs in the background, so you can close the window — progress and a live log are available if you check back before it finishes. See [After Your Migration](after-migration-review) for verifying the results.

Remember that CSV import specifically leaves **product images** and **variants** for you to finish by hand — neither comes across automatically, no matter how complete your files were.

## Tips

- **Start from the Download Template button for every file** — it saves you from chasing column-name typos that would otherwise fall through to manual mapping.
- **Fix `product_id` mismatches before uploading reviews** — a review whose `product_id` doesn't match any product `id` has nothing to attach to and is skipped.
- **Don't rename headers from another platform's export** — auto-detection often recognizes them as-is via aliases, so mapping may need no manual work at all.
- **Set aside time for images and variants right after the import** — these are the two things CSV never brings across, and they're easy to forget until a customer notices a bare product page.
- **Use `parent_id` to model multi-level categories** — point a subcategory's `parent_id` at its parent's `id` to nest it; leave it blank for top-level.
- **Re-export and re-check on a "could not be read" error** — it's almost always encoding or corruption in the source file, not something to fix in Spwig.
