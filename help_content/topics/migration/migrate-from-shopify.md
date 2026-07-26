---
slug: migrate-from-shopify
title_i18n_key: Migrating from Shopify
category: migration
component: migration
keywords:
  - shopify migration
  - import from shopify
  - shopify app setup
  - shopify client id secret
  - shopify api scopes
  - read_all_orders
  - shopify collections
  - shopify custom distribution
  - migrate shopify store
  - shopify metafields
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

If your store currently runs on Shopify, Spwig's migration wizard can import your products, customers, orders and content by connecting to a small custom app you create in the Shopify Partners dashboard. Shopify's platform is more locked-down than most, so most of this guide is about creating that app correctly — the connection itself is a five-minute step once the app exists.

## Before You Begin

Two Shopify-specific limits matter enough to call out here, not just further down in a table:

> **Important:** Shopify has no reviews API, so **customer reviews are not migrated at all**, regardless of which app scopes you grant. If you need your reviews, export them separately from whatever review app you're using (Judge.me, Yotpo, Loox, etc.) and import them into Spwig on your own.

> **Important:** By default, Spwig can only read **orders from the last 60 days**. To bring across your full order history, you must add the `read_all_orders` scope when you create your app — see the scope list below. This is easy to miss since the app still connects and imports successfully without it; it just silently limits how far back your order history goes.

Everything else transfers well: categories (as Collections — see below), products, images, variants, customers and addresses, discounts, and blog content. Custom fields are the other notable gap — see **Shopify metafields** near the end of this guide.

Also keep in mind:

- The wizard's **Import tax settings** and **Import shipping zones and methods** options are not applied to imported data. Set up tax rates and shipping in Spwig yourself afterward — see [After Your Migration](after-migration-review).
- The **Price adjustment** option on the same step *does* take effect for Shopify imports, changing each product's base price as it is created. Leave it set to **None** unless you deliberately want every price shifted.
- You'll need access to a Shopify Partners account to create the app. If you don't already have one, Shopify lets you create one for free at partners.shopify.com.

## Creating the Shopify App

Spwig connects to Shopify through a custom app you create and install on your own store. This mirrors the in-product **Shopify API Setup Guide** modal (opened via **Open Setup Guide** on step 2 of the wizard), so the steps below match what you'll see there exactly — you can follow either one.

### Step 1: Create the app

1. Go to your [Shopify Partners dev dashboard](https://dev.shopify.com/dashboard) and open **Apps**
2. Click **Create app**
3. Choose **Start from Dev Dashboard**
4. Enter the app name: `Spwig Migration`
5. Click **Create**

![Creating the Spwig Migration app in the Shopify dev dashboard](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Step 2: Set the App URL and scopes

On the new app's configuration page, under **Versions**, set:

- **App URL**: `https://shopify.dev/apps/default-app-home`
- **Scopes**: `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![Setting the App URL and required scopes](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Scope | Gives Spwig access to |
|---|---|
| `read_products` | Products, variants, images, collections |
| `read_customers` | Customer names, emails, addresses |
| `read_orders` | Orders from the last 60 days |
| `read_content` | Blog posts and pages |
| `read_discounts` | Discount codes and rules |
| `read_files` | Uploaded media files |

> **Note:** Want your full order history instead of just the last 60 days? Add `read_all_orders` to the scope list above.

### Step 3: Copy your Client ID and Secret

Go to **Settings > Credentials** and copy the **Client ID** and **Secret** shown there — you'll paste these into the Spwig wizard in a moment.

![Copying the Client ID and Secret from the app's Settings page](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Step 4: Generate a custom distribution link

1. Go to **Distribution** and select **Custom distribution**
2. Enter your store domain (for example, `yourstore.myshopify.com`)
3. Click **Generate link**, then **Copy** the install link it produces

![Copying the generated custom-distribution install link](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Step 5: Install the app on your store

Open the install link you just copied in your browser (make sure you're logged into your Shopify store admin), review the permissions it requests, and click **Install**.

![Installing the app on the Shopify store](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Important:** This last step is easy to miss. Generating the install link does not install the app — you have to actually open the link and click Install, or Spwig won't be able to connect. If the connection test fails in the next section, this is the first thing to check.

## Copying Your Credentials into Spwig

In the Spwig admin, go to **Data Import & Export > Start New Migration**, choose **Shopify** on step 1, and on step 2 enter:

- **Store Domain** — `yourstore.myshopify.com`
- **Client ID** — from Settings > Credentials
- **Client Secret** — from Settings > Credentials

If you'd rather follow the in-product walkthrough instead of this guide, click **Open Setup Guide** on this step — it covers the same five steps above with the same screenshots, and takes about 10 minutes end to end.

Leave **Test connection before proceeding** checked. If `read_products`, `read_customers` or `read_orders` is missing from your app's scopes, Spwig warns you before you continue — go back to the app's Versions page in the Shopify dashboard, add the missing scope, save a new version, and try again.

## Reviewing and Selecting Data

Step 3 pulls live counts from your store and shows a sample of the first five products. A few things look different from other platforms:

- **Collections, not categories** — Shopify organizes products into Collections rather than categories, and Collections don't support nesting, so the hierarchy imports flat. If your Shopify store used collections to represent a category tree, plan to rebuild that structure in Spwig's category manager after the import.
- **Discounts, not coupons** — Shopify's discount codes and rules import as Spwig discounts.
- **No Reviews row** — since Shopify has no reviews API, this data type doesn't appear on the step at all, unlike WooCommerce or CSV imports.

The **Import Options** work the same as on other platforms: **Skip existing items** (on) matches on SKU and email to avoid duplicates; **Import product images** (on) is slower but recommended; **Preserve original IDs where possible** (off) should stay off unless you have a specific reason to change it; **Batch size** defaults to 25.

## Shopify Metafields

If you use Shopify metafields to store extra data on products, customers or orders, be aware that Spwig does not detect or read them — unlike WooCommerce, there is no custom field mapping step for Shopify imports. Any data you've stored in metafields will need to be re-entered manually in Spwig using [custom fields](migration-field-mapping) after the migration, so it's worth exporting a list of your metafields and their values from Shopify before you start.

## Running the Import

Once you've reviewed step 3, start the import. It runs in the background — you can close the browser window and it keeps going. Step 5 shows live progress with a row per data type and an expandable activity log.

Step 6 shows your results: what was imported, skipped or failed, plus a **Link Rewriting** tool if internal links to your old `myshopify.com` domain were found in imported content. Review the summary carefully, then work through the checklist in [After Your Migration](after-migration-review) — it covers verifying your data, rebuilding any collection hierarchy, setting up tax rates and shipping (which the wizard does not configure for you), and re-entering anything that was stored in metafields.

## Delete the App from Shopify

Once you've confirmed the migration completed successfully, go back to your Shopify admin's **Apps** page, or the Partners dashboard, and delete the Spwig Migration app (or at minimum uninstall it from your store). There's no reason to leave read access to your store data active once the migration is done.

## Tips

- **Order history is limited by default** — if you need more than the last 60 days of orders, add `read_all_orders` to the scope list before generating your install link, not after.
- **Reviews need a separate export** — plan for this before you migrate, since there's no way to bring reviews across through the wizard at all.
- **Generating the link isn't the same as installing the app** — always complete Step 5 and click Install, or the connection test in Spwig will fail.
- **Collections come in flat** — if your category structure mattered for navigation or SEO, budget time to rebuild the hierarchy in Spwig after the import.
- **Export your metafields first** — Spwig can't read them, so capture that data from Shopify before you start if you'll need it later.
- **Delete the app once you're verified** — don't leave a live integration pointed at your old store after you've moved on.
