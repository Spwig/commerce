---
slug: voucher-import
title_i18n_key: Bulk Import Voucher Codes
category: promotions
component: vouchers
keywords:
  - voucher import
  - bulk voucher codes
  - upload voucher codes
  - CSV import vouchers
  - XLSX import vouchers
  - import discount codes
  - bulk discount codes
  - spreadsheet vouchers
  - voucher template
  - export vouchers
  - voucher wizard
  - batch voucher codes
  - import coupons
  - bulk coupons
url_patterns:
  - /admin/vouchers/vouchercode/import/
  - /admin/vouchers/vouchercode/import/preview/
  - /admin/vouchers/vouchercode/import/result/
related:
  - voucher-codes
  - voucher-examples
  - voucher-restrictions
published: true
---

The voucher import wizard lets you create hundreds of voucher codes at once by uploading a CSV or XLSX spreadsheet. This is ideal when you have pre-printed codes, loyalty programme codes from a third-party system, or simply need to launch a large campaign without adding each code by hand.

![Voucher list with Import button](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## Starting an import

Navigate to **Marketing > Vouchers** and click the **Import** button in the top-right area of the page. This opens the three-step import wizard.

## Step 1: Upload your file and set batch settings

![Import upload form](/static/core/admin/img/help/voucher-import/import-upload.webp)

The first page has two parts: the file upload and the batch discount settings.

### Preparing your file

Upload a `.csv` or `.xlsx` file up to 5 MB. The file must have a header row as the first row. The minimum requirement is a single column containing the voucher codes — every other column is optional.

The importer recognises common column names automatically. If your file uses any of the names below, Spwig will pre-select the correct mapping on the next page without any extra clicks:

| Your column name | Maps to |
|-----------------|---------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Voucher code |
| `name`, `title`, `campaign` | Internal name |
| `description`, `details`, `note` | Customer-facing description |
| `external_id`, `member_id`, `reference` | External ID |

**Tip:** Download the XLSX template first (see [Exporting vouchers as a template](#exporting-vouchers-as-a-template) below) — it uses the exact column names the importer expects, so column mapping is automatic.

### File limits

- Maximum file size: **5 MB**
- Maximum rows per import: **5,000 codes**

### Setting batch discount settings

Every voucher in the batch will share the same discount settings you configure on this page. Fill in the fields as you would when creating a single voucher:

**Discount section**

| Field | Description |
|-------|-------------|
| **Discount type** | Percentage, Fixed Amount, or Free Shipping |
| **Discount value** | The percentage (0–100) or fixed amount to deduct |
| **Max discount amount** | Optional cap on percentage discounts (e.g. cap a 20% discount at $50) |
| **Application scope** | Entire Cart, Specific Products, or Specific Categories |

**Validity section**

| Field | Description |
|-------|-------------|
| **Start date** | When codes become active (defaults to now if left blank) |
| **End date** | When codes expire (leave blank for no expiry) |
| **Days valid** | Alternative to end date — codes expire this many days after creation |

**Usage limits section**

| Field | Description |
|-------|-------------|
| **Max uses total** | Total redemptions allowed across all customers (blank = unlimited) |
| **Max uses per customer** | How many times one customer can use any code from this batch |
| **Minimum order value** | Minimum cart total required before the code applies |

**Restrictions**

Check any combination of:
- **Cannot apply to sale items** — prevents the code stacking with already-discounted products
- **Cannot combine with other vouchers** — prevents customers from using two codes on the same order
- **Cannot combine with sale items** — similar to the above but targeted at sale-price items
- **First-time customers only** — restricts the code to customers with no previous completed orders
- **Active immediately** — leave checked to make codes live the moment they are imported

When you are satisfied with the settings, click **Continue to preview**.

## Step 2: Map columns and review

![Column mapping and preview page](/static/core/admin/img/help/voucher-import/import-preview.webp)

The preview page shows four summary counters at the top:

- **Rows parsed** — total data rows found in your file
- **Will import** — new codes that will be created
- **Duplicates** — codes that already exist in your catalogue
- **Will skip (invalid)** — rows rejected due to validation errors (empty code, code too long, etc.)

### Column mapping

The **Column mapping** table lets you tell Spwig which column in your file corresponds to each voucher field. Spwig auto-detects common header names (see the table above), but you can change any mapping using the dropdown on each row.

Only the **Voucher code** column is required. The other fields — **Internal name**, **Customer-facing description**, and **External ID** — are optional. If you skip them, Spwig uses sensible defaults (the internal name defaults to "Imported voucher {code}").

### Duplicate code strategy

If any codes in your file already exist in your catalogue, you must choose how to handle them:

| Strategy | What happens |
|----------|-------------|
| **Skip duplicates** | Existing codes are left exactly as they are. Only new codes are created. |
| **Overwrite settings** | Existing codes are updated with this batch's discount settings. Their codes, usage counts, and creation dates are preserved. |
| **Fail the import** | The entire import is cancelled if even one duplicate is found. Use this when you need a guarantee that no existing codes are affected. |

Any duplicate codes found are listed in an expandable panel so you can review them before deciding.

### Data preview table

The bottom of the page shows the first 20 rows of your file so you can confirm the column mapping looks correct before committing. Rows that match existing codes are highlighted.

When everything looks right, click **Import N vouchers** to commit the batch.

## Step 3: Review the result

![Import result page](/static/core/admin/img/help/voucher-import/import-result.webp)

After the import completes you will see a summary showing:

- **Imported** — codes successfully created
- **Skipped** — codes that were not created (duplicates or invalid rows)
- **Rows processed** — total rows from your file that were evaluated
- **Failed** — rows that encountered an unexpected error

Click **View imported vouchers** to open the voucher list filtered to just the codes from this batch, making it easy to spot-check the result or bulk-activate the new codes.

If anything looks wrong — for example the wrong discount type was applied — you can use the **Overwrite settings** strategy on a re-import to correct the batch without having to delete and recreate the codes.

Click **Import another batch** to start a fresh upload, or **Back to voucher list** to return to your full catalogue.

## Exporting vouchers as a template

The voucher list supports an XLSX export action that produces a file in exactly the same column order the importer expects. This is the easiest way to get a correctly formatted template:

1. Navigate to **Marketing > Vouchers**
2. Select the vouchers you want to export (or select all)
3. Choose **Export selected vouchers to XLSX** from the **Action** dropdown
4. Click **Go**

The downloaded file has all 21 columns the importer understands, including fields that are batch-level in the import wizard (discount type, dates, usage limits, etc.). You can use this file as a reference or round-trip your existing codes through an edit → re-import cycle using the **Overwrite settings** strategy.

## Tips

- Download an XLSX export first to use as a template — the column names are pre-formatted so the auto-mapping picks them up without any adjustments on the preview page.
- Run a small test batch of 5–10 codes before importing hundreds to verify your column mapping and batch settings are correct.
- Use **Days valid** instead of a fixed **End date** when codes will be distributed over time — each code's expiry then counts from when it was imported rather than a single calendar date.
- If you receive codes from a third-party loyalty system, map the supplier's member or customer reference to the **External ID** column so you can reconcile redemptions later.
- After a large import, click **View imported vouchers** on the result page to filter the list to just the new batch — you can then bulk-edit, activate, or deactivate them as a group.
- A failed import (using the **Fail** duplicate strategy) leaves your catalogue unchanged, so it is safe to fix the file and retry as many times as needed.
