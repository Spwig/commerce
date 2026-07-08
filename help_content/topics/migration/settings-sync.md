---
slug: settings-sync
title_i18n_key: Settings Sync
category: migration
component: migration
keywords:
  - settings sync
  - staging
  - production
  - spwig sync
  - pull
  - push
  - configuration
  - deploy settings
  - mirror
url_patterns:
  - /admin/migration/syncjob/
  - /admin/migration/syncjob/sync/step1/
  - /admin/migration/syncjob/sync/step2/
  - /admin/migration/syncjob/sync/step3/
  - /admin/migration/syncjob/sync/step4/
related:
  - sync-token-management
  - full-system-migration
published: true
---

Settings Sync lets you copy store configuration between two Spwig installations. This is ideal for maintaining staging and production environments, where you configure and test changes on staging before deploying them to your live store.

## When to Use Settings Sync

- **Staging to Production**: Configure settings on your staging store, then push them to production
- **Production to Staging**: Pull production settings into staging to start with a matching environment
- **Backup Configuration**: Pull settings from production to a backup instance as a safeguard

Settings Sync handles configuration data only -- it does not transfer products, customers, orders, or media files. For a complete data transfer, use Full System Migration instead.

## What Can Be Synced

Settings Sync supports the following categories:

| Group | Categories |
|-------|-----------|
| **Settings** | Site Settings, Tax & Currency, Tax Rates, Languages, Blog Settings, Social Sharing, Sales Regions & Warehouses, Search Configuration, Custom Fields, Staff Roles, Customer Analytics |
| **Design** | Design & Theme, Headers/Footers/Menus |
| **Providers** | Email, SMS/WhatsApp, Payment Providers, Shipping, SEO Providers, Product Feeds, Blog Social Connectors, POS Configuration |
| **Content** | Pages & Templates, Blog Posts, Announcements, Forms, Product Collections |
| **Commerce** | Commerce Rules (Vouchers, Promotions, Loyalty, Subscriptions), Affiliate Program, Webhooks & Integrations |

> **Note:** Categories that contain credentials (payment providers, shipping accounts, etc.) are flagged with a key icon. API keys and secrets are transferred securely but may need to be re-entered for OAuth-based integrations.

## Step-by-Step Guide

### Step 1: Set Up a Connection

1. Navigate to **Data Migration > Spwig-to-Spwig Sync** in the admin sidebar
2. Click **Start Settings Sync**
3. Select a saved connection or create a new one:
   - Enter the remote store's URL (e.g., `https://staging.yourstore.com`)
   - Paste the sync token generated on the remote store
   - Give the connection a descriptive name
   - Set the role (Staging, Production, Backup, or Other)
4. Click **Test Connection** to verify it works
5. Click **Next** to proceed

### Step 2: Choose Categories and Direction

**Direction:**
- **Pull** -- Copies settings from the connected store to this store
- **Push** -- Copies settings from this store to the connected store

**Sync Mode:**
- **Add & Update** -- Adds new items and updates existing ones, but never deletes anything. This is the safest option.
- **Exact Copy** -- Makes the target match the source exactly, including removing items that exist on the target but not on the source. Use with caution.

Select the categories you want to include, then click **Next**.

### Step 3: Preview Changes

Before any changes are applied, you will see a detailed preview showing exactly what will be added, modified, or removed for each category. Review this carefully.

If pushing to a production connection, you will need to confirm that you understand the changes will affect your live store.

Click **Start Sync** when ready.

### Step 4: Monitor Progress

The sync runs in the background. You can safely navigate away from the progress page -- the sync will continue running.

The progress page shows:
- Overall completion percentage with estimated time remaining
- Per-category progress with success/failure counts
- A live activity log you can expand for detailed output

## Rollback

After a sync completes, you have **24 hours** to rollback the changes. A rollback restores the previous state of all affected settings.

To rollback:
1. Go to the **Sync Dashboard**
2. Find the completed job
3. Click **Rollback** and confirm

After 24 hours, the rollback option expires and the changes become permanent.

## Tips

- **Test on staging first**: Always sync to a staging environment first to verify the results before pushing to production
- **Use Add & Update mode**: This is the safest mode since it never deletes existing data
- **Check the preview carefully**: The diff preview shows you exactly what will change before anything is applied
- **Production connections show warnings**: When pushing to a connection marked as Production, additional safety confirmations are required
