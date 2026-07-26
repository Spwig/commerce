---
slug: migrate-from-woocommerce
title_i18n_key: Migrating from WooCommerce
category: migration
component: migration
keywords:
  - woocommerce migration
  - import from woocommerce
  - wordpress store import
  - woocommerce rest api
  - consumer key consumer secret
  - spwig migration bridge plugin
  - affiliate data import
  - woocommerce extensions
  - migrate wordpress products
  - woocommerce subscriptions import
url_patterns:
  - /admin/migration/migrationjob/
  - /admin/migration/migrationjob/wizard/step1/
  - /admin/migration/migrationjob/wizard/step2/
  - /admin/migration/migrationjob/wizard/step3/
related:
  - migration-overview
  - migration-field-mapping
  - after-migration-review
  - migration-troubleshooting
published: true
---

If your store currently runs on WooCommerce, Spwig's migration wizard can import your products, customers, orders and content directly over WooCommerce's REST API. This guide covers getting API credentials, running the import, and two WooCommerce-specific features worth knowing about first: the optional Migration Bridge plugin for affiliate data, and built-in support for several popular WooCommerce extensions.

## Before You Begin

WooCommerce has the broadest support of any source platform in the migration wizard. The following import cleanly: categories (with hierarchy), products, images and variants, customers and addresses, orders, reviews, coupons, and blog posts with their categories, tags and images.

Affiliate profiles, commission records and payout history can also be imported, but only if you install the Spwig Migration Bridge plugin first — see below. Without it, that data is simply skipped.

Also keep in mind:

- Products from certain WooCommerce extensions (subscriptions, bundles, bookings, gift cards) land in the matching Spwig feature, but not every detail carries over — see **WooCommerce extension support** below.
- Custom fields on your products, customers and orders are detected automatically and need mapping in a later step. See [Migration Field Mapping](migration-field-mapping).
- The wizard's **Import tax settings** and **Import shipping zones and methods** options are not applied to imported data. Set up tax rates and shipping in Spwig yourself afterward — see [After Your Migration](after-migration-review).
- The **Price adjustment** option on the same step *does* take effect for WooCommerce imports, changing each product's base price as it is created. Leave it set to **None** unless you deliberately want every price shifted.

Have your WordPress admin login handy, and know roughly how many products, customers and orders you're importing so you can sanity-check the counts the wizard shows you.

## Getting REST API Credentials

Spwig connects to WooCommerce using a REST API key generated from your WordPress admin. This key only needs **Read** access — Spwig only reads from your store during a migration, it never writes anything back.

1. In WordPress, go to **WooCommerce > Settings > Advanced > REST API**
2. Click **Add key**
3. Give it a description (for example, `Spwig Migration`) and set **Permissions** to **Read**
4. Click **Generate API key**
5. Copy the **Consumer Key** (`ck_...`) and **Consumer Secret** (`cs_...`) to a safe place

> **Important:** WooCommerce shows the Consumer Secret only once, at the moment you generate it. If you navigate away before copying it, you'll need to generate a new key.

## Connecting Your Store

Go to **Data Import & Export > Start New Migration** in the Spwig admin and choose **WooCommerce** on step 1. On step 2, enter:

- **Store URL** — your store's full web address, for example `https://mystore.com`
- **Consumer Key** and **Consumer Secret** — the values you just copied

Leave **Test connection before proceeding** checked (on by default) so Spwig confirms it can reach your store and authenticate before you continue — this catches typos and permission problems immediately rather than partway through the import. Click **Next** once it succeeds.

## Reviewing and Selecting Data

Step 3 pulls live counts from your store — categories, products, customers, orders, reviews and coupons — plus a sample of the first five products so you can confirm it's reading the right site. Each data type's checkbox is auto-checked when its count is above zero, and disabled at zero.

**Import Options:**

- **Skip existing items** (on) — matches incoming records against what's already in Spwig (SKU for products, email for customers) and skips duplicates. Leave it on unless you're starting from an empty store.
- **Import product images** (on) — slower, but worth it.
- **Preserve original IDs where possible** (off) — the wizard itself labels this "not recommended." Leave it off unless you have a specific technical reason to keep WooCommerce's numeric IDs.
- **Batch size** — 10, 25 (default), 50 or 100 records at a time. Smaller batches suit flaky connections; larger batches finish faster on a stable one.

## The Spwig Migration Bridge Plugin

WooCommerce has no built-in concept of an affiliate program, so if you run one through a WooCommerce affiliate extension, that data lives in tables the standard REST API can't see. The **Spwig Migration Bridge** is a small companion plugin you install on your WordPress site to expose it.

The Bridge plugin unlocks:

- **Affiliate profiles** — your affiliates' details and referral codes
- **Commission records** — commission history tied to each affiliate
- **Payout history** — past payouts made to affiliates

It's entirely optional — skip it if you don't run an affiliate program or don't need that history in Spwig.

> **Note:** Affiliate data can only be imported if orders and customers are also being imported in the same migration, since commissions and payouts are tied to specific orders and customers.

To install it:

1. On step 3, if the plugin isn't already detected on your site, you'll see a **Download Bridge Plugin** button with install instructions
2. Download the plugin ZIP
3. In WordPress, go to **Plugins > Add New > Upload Plugin**, choose the ZIP, click **Install Now**, then **Activate**
4. Return to the Spwig wizard and refresh the page — an **Affiliates** checkbox and an **Affiliate Program Data** block will appear, showing the counts found

You can deactivate and remove the Bridge plugin from WordPress once your migration is complete.

## WooCommerce Extension Support

If your store uses certain popular extensions, the products they create are recognized during import and mapped into the matching Spwig feature rather than imported as plain products:

| WooCommerce extension | Lands in |
|---|---|
| Subscriptions | Spwig subscription plans |
| Product Add-Ons | Spwig product add-ons |
| Product Bundles | Spwig product bundles |
| Gift Cards (WooCommerce, YITH and PW variants) | Spwig gift cards |
| Composite Products | Spwig composite products |
| Bookings and Accommodation Bookings | Spwig bookings |

> **Note:** Extension data import never blocks the underlying product from being created. If a product's extension-specific data can't be read, the product still imports — just as a regular product, without its subscription, bundle, booking or gift-card configuration.

Spot-check your subscription, bundle, booking and gift card products after the import to confirm their extension-specific settings came across, rather than assuming a successful import carried every detail.

## Custom Fields

If you've added custom meta fields to your WooCommerce products, customers or orders, Spwig samples about ten records of each type to detect which fields exist. You'll map each one to a Spwig custom field slot or a general Meta Data field on step 4. See [Migration Field Mapping](migration-field-mapping) for the full walkthrough, including how mappings are saved for future migrations.

## Running the Import

Once you've reviewed step 3 and confirmed your mappings on step 4, start the import. It runs in the background — you can close the browser window and it keeps going. Step 5 shows live progress with a row per data type (categories, products, customers, orders, reviews, coupons, blog posts, and affiliates/commissions/payouts if the Bridge plugin was used) plus an expandable activity log.

Step 6 shows your results: what was imported, skipped or failed, plus a **Link Rewriting** tool if internal links to your old WooCommerce domain were found in imported content. Review the summary carefully, then work through the checklist in [After Your Migration](after-migration-review) — it covers verifying your data, setting up tax rates and shipping (which the wizard does not configure for you), and rewriting internal links.

## Revoke Your API Key

Once you've confirmed the migration completed successfully, go back to **WooCommerce > Settings > Advanced > REST API** in WordPress and revoke or delete the key you created for Spwig. There's no reason to leave an active API key on your old store once you're done with it.

## Tips

- **Generate the API key right before you need it** — since the Consumer Secret is shown only once, create it immediately before starting step 2 rather than in advance.
- **Read-only really is enough** — never grant Write or Read/Write permissions; Spwig only ever reads from your WooCommerce store.
- **Install the Bridge plugin before you start the import** — you'll need to add it and refresh the wizard before importing, so check for it up front rather than partway through.
- **Spot-check extension-backed products** — subscriptions, bundles, bookings and gift cards are the products most likely to need a manual check after import.
- **A partial import isn't cleaned up automatically** — see [Migration Troubleshooting](migration-troubleshooting) before retrying a failed import.
- **Revoke the API key when you're done** — don't leave old integrations active on a store you've migrated away from.
