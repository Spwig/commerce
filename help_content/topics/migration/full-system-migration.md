---
slug: full-system-migration
title_i18n_key: Full System Migration
category: migration
component: migration
keywords:
  - full migration
  - system migration
  - spwig to spwig
  - server move
  - transfer data
  - products
  - customers
  - orders
  - media
url_patterns:
  - /admin/migration/syncjob/
  - /admin/migration/syncjob/fullmig/step1/
  - /admin/migration/syncjob/fullmig/step2/
  - /admin/migration/syncjob/fullmig/step3/
  - /admin/migration/syncjob/fullmig/step4/
  - /admin/migration/syncjob/fullmig/step5/
related:
  - sync-token-management
  - settings-sync
published: true
---

Full System Migration transfers your entire store -- settings, products, customers, orders, media files, and all other data -- from one Spwig installation to another. Use this when moving to a new server or setting up a complete copy of your store.

## When to Use Full Migration

- **Server relocation**: Moving your store to a new hosting provider or server
- **Creating a staging copy**: Setting up a complete staging environment from production
- **Disaster recovery**: Restoring a complete store from a backup instance

Full Migration includes everything that Settings Sync does, plus all transactional data (products, customers, orders, reviews, inventory, media, etc.).

## What Gets Migrated

Full Migration can transfer all settings categories plus these data categories:

| Category | Description |
|----------|-------------|
| **Installed Components** | Themes, provider integrations, and utility components with their package files |
| **Products, Categories & Brands** | Products, variants, images, categories, brands, and attributes |
| **Media Library** | All uploaded media files and assets |
| **Customers & Addresses** | Customer accounts, profiles, and addresses |
| **Order History** | Orders, order items, and transaction records |
| **Product Reviews** | Customer reviews and ratings |
| **Stock Levels** | Per-warehouse inventory quantities and reorder points |
| **Digital Products & Licenses** | Digital assets, license templates, and license pools |
| **Gift Cards & Voucher Usage** | Gift card balances and voucher usage records |
| **Store Credit & Wallets** | Customer wallet balances and transaction history |
| **Loyalty Program Members** | Loyalty members, points, transactions, and badges |
| **Active Subscriptions** | Subscription plans, active subscriptions, and billing history |
| **Shipments & Tracking** | Shipment records and tracking events |
| **Refunds, Returns & Order Notes** | Refund records, return requests, and notes |
| **Affiliate Members** | Affiliate accounts, referral codes, and commission history |

## Step-by-Step Guide

### Step 1: Connect to Source Instance

1. Navigate to **Data Migration > Spwig-to-Spwig Sync** in the admin sidebar
2. Click **Start Full Migration**
3. Connect to the source store (the store you are migrating **from**):
   - Enter the source store's URL
   - Paste the sync token from the source store
   - Name the connection (e.g., "Old Production Server")
4. Click **Test Connection** to verify
5. Click **Next**

> **Important:** Full Migration always **pulls** data from the connected store into this store. Run the wizard on the **destination** (new) store.

### Step 2: Choose Scope

Select which data categories to include in the migration. Categories are organized into groups:

- **Settings**: Store configuration, themes, providers, content
- **Data**: Products, customers, orders, media, and other transactional data

Some categories have dependencies (e.g., Orders depend on Customers and Products). Dependencies are automatically included when you select a category.

Categories with special indicators:
- **Key icon**: Contains credentials that are transferred securely
- **File icon**: Includes binary files (images, media, packages)
- **Warning icon**: Special considerations for production environments

### Step 3: Pre-flight Checks

Before the migration starts, automatic pre-flight checks verify:

- **Connection health**: The source store is reachable and authenticated
- **Version compatibility**: Both stores are running compatible Spwig versions
- **Disk space**: Sufficient storage is available for media files
- **Database readiness**: The destination database can receive the data

If any checks fail, you will see specific guidance on how to resolve the issue before proceeding.

### Step 4: Migration Progress

The migration runs in the background. You can safely navigate away -- the process will continue.

The progress page shows:
- Overall percentage with estimated time remaining
- Per-category completion status
- Live activity log with transfer details
- Media transfer stats (files and bytes transferred) for the media category

For large stores with many products and media files, the migration may take some time. The media transfer phase is typically the longest.

### Step 5: Results

After the migration completes, the results page shows:

- Summary statistics (migrated, skipped, failed items)
- Per-category breakdown with status
- Error details for any failed items

## Post-Migration Checklist

After a successful migration, complete these steps on your new store:

1. **Activate your license** on the new installation
2. **Re-enter payment provider credentials** that were skipped during migration (sandbox/test keys are not transferred to production)
3. **Configure DNS** to point your domain to the new server
4. **Test the checkout flow** with a test order
5. **Verify email sending** works correctly
6. **Check media files** and images are loading properly

## Rollback

After a Full Migration completes, you have **24 hours** to rollback. A rollback deletes all migrated data from the destination store, restoring it to its pre-migration state.

To rollback:
1. Go to the results page or the Sync Dashboard
2. Click **Rollback Migration** and confirm
3. Wait for the rollback to complete

> **Warning:** Rollback permanently removes all migrated data. Any changes made on the destination store after the migration (new orders, customer signups, etc.) will also be affected.

After 24 hours, the rollback option expires.

## Tips

- **Run on the destination store**: The Full Migration wizard should be run on the **new** store, pulling data from the old one
- **Migrate to a clean installation**: For best results, run the migration on a fresh Spwig installation before going live
- **Check disk space**: Ensure the destination has enough storage for all media files
- **Keep the source running**: Don't shut down the source store until you have verified everything works on the destination
- **Plan for DNS transition**: After verifying the migration, update your DNS records to point to the new server
