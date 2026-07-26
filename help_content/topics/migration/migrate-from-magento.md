---
slug: migrate-from-magento
title_i18n_key: Migrating from Magento
category: migration
component: migration
keywords:
  - migrate from Magento
  - Magento 2 import
  - Adobe Commerce migration
  - Magento integration access token
  - Magento REST API
  - import Magento products
  - Magento reviews not importing
  - Magento System Integrations
  - switch from Magento
  - Magento Community Edition
  - Magento customers and orders
  - Magento CMS pages
url_patterns:
  - /admin/migration/migrationjob/
  - /admin/migration/migrationjob/wizard/step1/
  - /admin/migration/migrationjob/wizard/step2/
  - /admin/migration/migrationjob/wizard/step3/
  - /admin/migration/migrationjob/wizard/step5/
  - /admin/migration/migrationjob/wizard/step6/
related:
  - migration-overview
  - migration-field-mapping
  - after-migration-review
  - migration-troubleshooting
published: true
---

Spwig can import your catalog, customers, orders, coupons, and CMS pages directly from a live Magento 2 or Adobe Commerce store using Magento's REST API. This guide walks through generating the integration credentials Magento requires, running the migration wizard, and the one significant gap merchants coming from Magento need to plan around: product reviews.

Only **Magento 2 and Adobe Commerce** are supported. Magento 1 reached end of life years ago and does not expose the REST API this migration relies on — if you are still on Magento 1, use [Importing from CSV Files](csv-import) instead.

## Before You Begin

Review [Data Migration Overview](migration-overview) for general planning guidance. For Magento specifically:

- **Categories** — imported with their hierarchy intact.
- **Products** — imported, including images.
- **Customers and addresses** — imported.
- **Orders** — imported.
- **Coupons** — imported as Spwig vouchers, sourced from Magento's sales rules.
- **CMS pages** — imported as Spwig pages.
- **Reviews** — usually **not** imported. See the next section before you rely on this.
- Variants are supported for configurable products.

> **Note:** Magento migrations do not carry over affiliate programs, commissions, or payouts — Spwig's affiliate bridge integration is only available for WooCommerce stores.

### The Review Limitation

Magento Community Edition does not expose a REST endpoint for product reviews — the `/reviews` route simply doesn't exist on a stock Community installation. Spwig checks for it before importing and, if it isn't there, logs a message and continues with the rest of your migration rather than failing the whole job. Your categories, products, customers, orders, coupons, and pages still come across; only reviews are skipped.

Reviews **will** import if your store runs **Adobe Commerce** (which exposes this endpoint) or if your Magento installation has a custom module adding a compatible reviews route.

If you're on Magento Community and need your reviews in Spwig, export them separately (most review extensions offer a CSV export) and bring them in afterward using the reviews file in [Importing from CSV Files](csv-import), keyed to your products by `product_id`.

## Step 1: Choose Magento

From the migration dashboard at **Data Import & Export**, click **Start New Migration** and select **Magento** as your platform.

## Step 2: Connect to Your Store

You'll need your Magento store's URL and an integration access token. Magento's admin doesn't hand out a simple API key the way some platforms do — you create an **Integration**, which is a scoped credential Magento treats like a connected app.

### Creating an Integration Access Token

1. In your Magento admin, go to **System > Integrations**.
2. Click **Add New Integration**.
3. Set the name to `Spwig Migration` so it's easy to identify later.
4. Open the **API** tab and set **Resource Access** to **All**.
5. Click **Save**, then click **Activate**.
6. Confirm by clicking **Allow** on the popup that lists the permissions being granted.
7. Copy the access token shown after activation — Magento only displays it once.

> **Note:** Resource Access is set to **All** because Magento's resource tree is very granular — hundreds of individual permissions covering catalog, sales, customers, and CMS — with no single "read everything" toggle short of selecting all of them. The migration only ever reads from your store; it never writes back, and you can revoke the integration once your migration is verified (covered at the end of this guide).

Back in the Spwig wizard, enter your **Store URL** and the **Access Token** you copied. Leave **Test connection before proceeding** checked (on by default) so Spwig verifies it can reach and authenticate with your store before you move forward. If the test fails, double-check the URL and that the integration is still Active in Magento. Click **Next**.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: magento-connection-step.webp
  description: Step 2 of the wizard with Magento selected, showing the Store URL and Access Token fields and the Test connection checkbox
  save-to: core/static/core/admin/img/help/migrate-from-magento/
  viewport: 1440x900
-->

## Step 3: Review What Will Be Imported

Spwig queries your Magento store and shows live counts for each data type it found: categories, products, customers, orders, coupons (sourced from sales rules), and CMS pages. Each type has a checkbox, automatically checked when Spwig found items to import and disabled when the count is zero.

You'll also see a sample of the first five products so you can sanity-check that titles, prices, and images look right before committing to the full import.

Below the counts, **Import Options** let you control how the import behaves:

- **Skip existing items** (on by default) — matches on identifiers like SKU or email so re-running the migration won't create duplicates.
- **Import product images** (on by default) — slower, but recommended; leave it on unless you have a specific reason not to.
- **Preserve original IDs where possible** (off by default) — Spwig's own UI labels this "not recommended," and that holds for almost every store.
- **Batch size** — 10, 25 (default), 50, or 100 items processed at a time. Smaller batches can help if your Magento store is slow to respond.

If you need to change how specific fields map — custom attributes, category matching, tax or shipping handling — that happens in step 4, covered in [Migration Field Mapping](migration-field-mapping). Click **Next** to proceed to mapping, then **Start Migration** once you've reviewed it.

## Running the Import

The import runs in the background — you can close the window and it will keep going. The progress page shows live status for each data type (categories, products, customers, orders, reviews, coupons) with a log you can expand for detail.

Once it finishes, you'll land on the results summary. Walk through [After Your Migration](after-migration-review) to verify what came across, handle any link rewriting for content that referenced your old Magento URLs, and take care of the tax and shipping configuration that the wizard collects but doesn't apply automatically.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step5/
  filename: magento-import-progress.webp
  description: Import progress page showing per-step status rows during a Magento migration
  save-to: core/static/core/admin/img/help/migrate-from-magento/
  viewport: 1440x900
-->

## Rollback Deadline

Magento is the one platform where rollback has a time limit. Once your migration completes, the **Rollback** button appears on the job's summary page — but for Magento specifically, that button may stop being offered after a period following completion. Other migration types (WooCommerce, Shopify, CSV) don't have this deadline, but Magento does, so don't leave verification for later.

> **Warning:** Rollback deletes more than what the migration created — including orders placed by migrated customers *after* the migration, and order items referencing migrated products, even on orders from customers you didn't migrate. It is only safe to use immediately after a migration, before any real trading has happened on the store. See [Migration Troubleshooting](migration-troubleshooting) for the full picture of what rollback does and does not undo.

Check your imported data promptly, while rollback is still available, in case you need it.

## Revoke the Integration

Once you've verified your data in Spwig — products, prices, images, customers, orders, coupons, and pages all look right — go back to **System > Integrations** in Magento, find `Spwig Migration`, and deactivate or delete it. The token isn't needed again unless you plan to re-run the migration, and removing it closes off a standing read-access credential you no longer need open.

## Tips

- **Reviews are the biggest surprise for Magento merchants** — plan for a separate export/import if you're on Community Edition and reviews matter to your store.
- **Copy the access token immediately** — Magento only shows it once when you activate the integration; if you lose it, you'll need to deactivate and recreate the integration.
- **Don't delay verification** — the Rollback button's availability is time-limited for Magento specifically, unlike other platforms.
- **Use the sample preview in step 3** to catch obvious mapping problems (wrong prices, missing images) before running the full import.
- **Coupons come from sales rules** — if a Magento coupon relies on complex conditions, check it in Spwig afterward since not every rule type has a direct equivalent.
- **Configure tax rates and shipping zones in Spwig after the import** — the wizard's tax and shipping options are saved but not applied to your store automatically.
