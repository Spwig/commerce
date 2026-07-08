---
slug: maintenance-mode
title_i18n_key: Maintenance Mode
category: getting-started
component: management
keywords:
  - maintenance mode
  - store offline
  - temporarily close store
  - maintenance page
  - take store offline
  - site down
  - disable storefront
  - maintenance reason
  - customer-facing page
url_patterns:
  - /admin/management/systemmetrics/toggle-maintenance/
related:
  - database-backups
  - shop-dashboard
published: true
---

Maintenance mode temporarily takes your storefront offline and shows customers a "we'll be back soon" message. Your admin backend remains fully accessible during maintenance — you can continue working while customers are held at the maintenance page.

Use maintenance mode before making changes that could cause a brief inconsistent state, such as running a large product import, applying a major theme redesign, or waiting for a restore operation to complete.

![Maintenance mode toggle on the system dashboard](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Enabling maintenance mode

1. Navigate to **Management > System Metrics**
2. Click **System Dashboard** from the toolbar
3. In the **Store Status** panel, click **Enable Maintenance Mode**
4. Optionally enter a **Reason** — this is for your own reference and is not shown to customers (e.g., `Product catalog update in progress`)
5. Confirm by clicking **Enable**

Your storefront immediately starts showing the maintenance page to all visitors. The admin backend is unaffected and you can continue working normally.

## What customers see

When maintenance mode is active, every page of your storefront (the shop, product pages, checkout, and account pages) displays a branded maintenance notice. The message tells customers that the store is temporarily unavailable and encourages them to come back shortly.

Customers who are mid-session or mid-checkout at the moment maintenance mode is enabled will also see the maintenance page on their next request. No in-progress orders are lost — the data is still there when you disable maintenance mode.

## Disabling maintenance mode

1. Navigate to **Management > System Metrics**
2. Click **System Dashboard**
3. In the **Store Status** panel, you will see a banner confirming maintenance mode is active
4. Click **Disable Maintenance Mode**
5. Confirm when prompted

The storefront comes back online immediately. Customers can browse and purchase as normal.

## When Spwig enables maintenance mode automatically

Certain system operations enable maintenance mode automatically and re-enable the storefront when they finish:

- **Platform upgrades** — the upgrade process enables maintenance mode before applying changes and disables it when the upgrade is complete
- **Restore operations** — restoring from a backup puts the store in maintenance mode for the duration of the restore

If an automated operation ends unexpectedly, maintenance mode may remain active. In that case, follow the steps above to disable it manually.

## Tips

- Always let your team know before enabling maintenance mode — it affects every visitor to your storefront
- Keep maintenance windows as short as possible; even a few minutes offline can affect customer confidence
- Use the reason field as a reminder to yourself about why maintenance mode was turned on — it appears in the system log
- If you notice maintenance mode is active but did not enable it yourself, check the system log for automated operations that may have triggered it
- Plan maintenance windows during low-traffic periods (evenings or early mornings) to minimise the impact on sales
