---
slug: migration-overview
title_i18n_key: Data Migration Overview
category: migration
component: migration
keywords:
  - migrate store to spwig
  - import from woocommerce
  - import from shopify
  - import from magento
  - csv import
  - platform migration
  - switch ecommerce platform
  - data import export
  - migration wizard
  - what data transfers
  - migrate from bigcommerce
  - migrate from wix
url_patterns:
  - /admin/migration/migrationjob/
  - /admin/migration/migrationjob/wizard/step1/
  - /admin/migration/migrationjob/wizard/step2/
  - /admin/migration/migrationjob/wizard/step3/
  - /admin/migration/migrationjob/wizard/step4/
  - /admin/migration/migrationjob/wizard/step5/
  - /admin/migration/migrationjob/wizard/step6/
related:
  - migrate-from-woocommerce
  - migrate-from-shopify
  - migrate-from-magento
  - csv-import
  - after-migration-review
published: true
---

If your products, customers, and orders currently live in WooCommerce, Shopify, or Magento — or just in a handful of CSV files — the migration tool brings that data into your new Spwig store so you don't have to re-enter it by hand. It handles categories, products, customers, orders, reviews, and coupons, and for WooCommerce it can also carry across blog content and, with a bridge plugin, your affiliate program.

Find it in the admin sidebar under **System Dashboard > Data Import/Export** (visible to superusers on self-hosted installations; if you don't see it, ask whoever manages your installation). The page, titled **Data Import & Export**, lists every migration you've started with stat cards for Total Migrations, Completed, In Progress, and Failed, plus **Start New Migration**, **View Logs**, and **Field Mappings** buttons. Migrations can only be created through the wizard.

## Supported platforms

Spwig connects directly to three platforms, plus plain CSV files:

- **WooCommerce** — the most complete path; extension data (subscriptions, bundles, gift cards, bookings) and your affiliate program can come across too.
- **Shopify** — connects through a custom app you create in your Shopify developer dashboard.
- **Magento 2** — connects through an integration token from your Magento admin.
- **CSV files** — five separate files (products, categories, customers, orders, reviews), for other platforms or hand-prepared data.

> **Note:** BigCommerce, PrestaShop, Squarespace, and Wix aren't supported as direct connections. If you're moving from one of these, export your catalog and customer data to CSV and use the CSV route instead — see [Importing from CSV Files](csv-import).

## What transfers, by platform

Coverage varies by platform — check this table against your own store before committing to a launch date.

| Data | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Categories | Yes, with hierarchy | Yes, as Collections (flat) | Yes | Yes |
| Products | Yes | Yes | Yes | Yes (required file) |
| Product images | Yes | Yes | Yes | No |
| Variants | Yes | Yes | Yes | No |
| Customers + addresses | Yes | Yes | Yes | Yes |
| Orders | Yes | Yes, last 60 days only unless the `read_all_orders` scope is added | Yes | Yes |
| Reviews | Yes | Not supported at all | Usually unavailable — Magento Community has no REST endpoint for reviews | Yes |
| Coupons / discounts | Yes | Yes | Yes | No |
| Blog / CMS content | Yes (posts, categories, tags, images) | Yes (articles) | Yes (CMS pages) | No |
| Affiliates, commissions, payouts | Yes, requires the Spwig Migration Bridge plugin | No | No | No |
| Custom field detection | Yes | No — Shopify metafields are not read | No | n/a |

Shopify merchants should plan to re-enter any metafield data (custom product specs, extra customer fields) manually after the import, since it isn't detected or transferred. For everything else, see [Migration Field Mapping](migration-field-mapping) for how source fields map onto Spwig fields.

## Planning your migration

- **Migrate before you go live**, against a Spwig install that isn't yet handling real traffic, before pointing your domain's DNS at it — that way you can review and fix things without customers seeing a half-finished catalog.
- **Keep your old store running, read-only**, until you've verified the Spwig copy is correct.
- **Budget time for tax and shipping setup afterward** — the wizard's settings for this look like they import your rates and zones, but they aren't applied (see [Migration Field Mapping](migration-field-mapping)). Configure **Settings > Tax & Currency** and **Settings > Shipping** yourself.
- **Spot-check rather than skim** — extension data imports on a best-effort basis; a product whose extension data couldn't be read still gets created, just without it. See [After Your Migration](after-migration-review) before announcing anything to customers.

## Prerequisites

- **Admin access to your source platform** to create API credentials — a REST API key in WooCommerce, a custom app in Shopify, or an integration token in Magento. Not needed for CSV.
- **Read-only scopes** wherever the source platform offers them — Spwig only reads from your old store, never writes back to it.
- **A time budget** — each run has a hard 4-hour limit. For a large store, plan a phased approach (categories and products first, orders later) rather than one pass.

> **Important:** Spwig does not encrypt the API credentials you enter in the wizard. Once the migration is verified complete, revoke or delete the credential on the source platform.

## The migration wizard, step by step

The wizard has six steps, with progress saved between them:

1. **Platform** — choose WooCommerce, Shopify, Magento, or CSV Import.
2. **Connection** — enter credentials, with an option (on by default) to test the connection first. The platform-specific guides cover exactly what to generate.
3. **Preview** — live counts from your source store, a sample of the first 5 products, and checkboxes for which data types to include plus options like batch size.
4. **Mapping** — how source fields map onto Spwig fields, any WooCommerce custom fields, and categories without an obvious match. Full detail in [Migration Field Mapping](migration-field-mapping).
5. **Import** — runs in the background; you can close the tab and it keeps going, with a live log.
6. **Complete** — a results summary, a link-rewriting tool for content referencing your old domain, and PDF/CSV report downloads.

## After your migration

A successful import isn't the finish line — see [After Your Migration](after-migration-review) for a full checklist covering data verification, fixing internal links that still point at your old domain, and the tax and shipping configuration the wizard doesn't handle for you.

## Rollback is not a safety net

Understand this before you start, not after something goes wrong. Rollback exists, but it isn't the undo button it might sound like:

- There's no automatic rollback if an import fails partway through. Whatever was imported before the failure stays in your store, and a failed import can't be rolled back from the admin — you'll need to review and clean up the partial data by hand.
- A completed migration can be rolled back, and rollback removes only what the import itself created — never more. A migrated customer who has placed a genuine order since the import keeps their account, addresses, loyalty history, and store credit, and that real order is left untouched; only the orders the import created are removed. A migrated product still referenced by any order, bundle, gift card, or configurator slot is kept too, and orders belonging to other customers are never modified.
- Affiliates, commissions, and payouts created by the import are removed, along with any affiliate account the import created — an affiliate attached to a customer who already existed keeps their account, and only the affiliate record goes. Subscription plans, pricing tiers, and booking resources created by store extensions still aren't removed — clean those up manually.
- Before you confirm, Spwig shows a preview of exactly what will be removed and what will be kept, by name and count, with the reason — calculated against your live data. Read it before confirming. Rollback then runs in the background, so it's safe to close the tab; check the migration's summary for the report once it finishes.
- Rollback is still a permanent, destructive action on the rows it does remove, so use it deliberately — and clean up by hand anything Spwig keeps that you don't actually want. But because it no longer reaches beyond what the import created, it's no longer a same-day-only tool the way it once was.
- The Rollback button stays available on a completed migration's summary for as long as the job record exists, and it's offered again if a rollback attempt itself fails partway through, so you can retry it. Records aren't removed on any schedule, so this doesn't expire on its own.

If you run into a failed or stuck migration, [Migration Troubleshooting](migration-troubleshooting) covers retrying, cancelling, and reading the logs.

## Tips

- **Start with a small test run** — categories plus a handful of products confirms field mapping looks right before the full catalog.
- **Read the platform-specific guide first** — [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify), and [Migrating from Magento](migrate-from-magento) cover exactly which credentials and scopes you need.
- **Don't skip the capability matrix above** — knowing Shopify reviews or CSV variants won't come across saves a surprise after you've switched DNS.
- **Keep your source platform's admin open in another tab** for generating or copying credentials as you go.
- **Treat the wizard's checkboxes literally** — if a setting isn't described as working here, configure it in Spwig directly rather than trusting the wizard.
