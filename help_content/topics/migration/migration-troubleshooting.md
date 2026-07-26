---
slug: migration-troubleshooting
title_i18n_key: Migration Troubleshooting
category: migration
component: migration
keywords:
  - migration failed
  - migration connection error
  - migration retry
  - migration cancel
  - migration rollback
  - migration timeout
  - migration stuck
  - migration logs
  - Shopify connection failed
  - WooCommerce connection failed
  - Magento connection failed
  - migration cleanup
url_patterns:
  - /admin/migration/migrationjob/
  - /admin/migration/migrationjob/wizard/step2/
  - /admin/migration/migrationjob/wizard/step5/
  - /admin/migration/migrationjob/wizard/step6/
related:
  - migration-overview
  - after-migration-review
  - migrate-from-woocommerce
  - migrate-from-shopify
published: true
---

Most migrations complete without incident, but connections fail, imports time out, and occasionally a run stops partway through. This topic covers diagnosing a failed connection, reading the progress log while an import runs, and — most importantly — what your options really are once something goes wrong, including what Retry, Cancel, and Rollback actually do.

## Connection failures at step 2

The **Test connection before proceeding** checkbox is on by default and is your first diagnostic — it validates credentials against the source platform before you commit to the rest of the wizard. If it fails, the error message usually points at one of these:

- **WooCommerce** — Store URL missing `https://` or with a trailing path segment; a mistyped or regenerated Consumer Key/Secret; or a REST API key created without **Read** permission at **WooCommerce > Settings > Advanced > REST API**.
- **Shopify** — Store Domain not in `yourstore.myshopify.com` form; Client ID/Secret from the wrong app; or, most commonly, an app created in the Dev Dashboard but never actually **installed** — creating an app version isn't enough, you need the custom distribution link and a click on **Install**. Spwig also warns if `read_products`, `read_customers`, or `read_orders` weren't included in the app's scopes.
- **Magento 2** — Store URL pointing at the storefront instead of the API root, or an integration token that was created but never activated (**Save > Activate > Allow**).
- **SSL issues** — an expired, self-signed, or misconfigured certificate fails the connection before credentials are checked, showing as a generic error rather than an authentication one. If credentials look right, check the certificate next.

Re-run the connection test after each fix rather than changing several credentials at once — it isolates which one was wrong.

## Reading the live log at step 5

While an import runs, step 5 shows a log of activity as it happens. Click **Show Details** to expand it into individual entries — level and message — instead of just the current step summary. This is the fastest way to see what's happening if progress looks stalled: a wall of "skipped" entries for one data type usually just means Skip existing items is working as intended, not that anything is stuck.

The log view shows only the **most recent 500 entries**, so on a large migration the earliest entries scroll out of view while the import is still running. If you need the complete log once a data type has finished, use **Download Logs** on the results page instead — it has no such limit.

## What a failed migration actually means

This is the most important thing to understand if a migration fails.

When a migration fails, the completion page tells you plainly what happened: items imported before the error are still in your store, nothing was removed automatically, and fixing the problem and running the import again will skip whatever already made it in the first time. Take that at face value. No step in the import runs inside a database transaction that could be rolled back as a unit — whatever imported successfully before the point of failure, products, categories, customers, orders, whatever the job got through, remains in your store exactly as created. A failed migration is a **partial** migration, not an undone one.

Failure also marks the job as no longer rollbackable, so the **Rollback** button will not be available on a failed **import** — it only appears once a migration has completed, or if a rollback of a completed migration itself failed partway through, in which case Spwig offers the button again so you can retry. The one situation where you'd most want an automated undo — a failed import — is still exactly the situation where the button isn't offered.

So, when a migration fails:

1. **Review what actually imported**, using the Imported/Skipped/Failed counts and the downloaded logs to build a picture of what's in your store versus what didn't make it.
2. **Decide how to clean up.** For a small amount of partial data, review it manually and delete what you don't want through the normal admin list views. For a larger or messier partial import, it's often faster to clear the imported data out yourself before starting fresh than to reconcile it item by item.
3. **Re-run with Skip existing items enabled**, whichever cleanup path you take — it's what prevents the data that did survive from being duplicated on the next attempt.

## Retry

**Retry** restarts the import completely from the beginning. It clears the job's previous counters and logs and re-imports everything from scratch — it does **not** continue from wherever the failed attempt stopped. Keep **Skip existing items** enabled so items that already made it in the first time aren't duplicated on the second pass.

If a migration stops because it hit the **4-hour** limit, the message you'll see is accurate: running the import again starts from the beginning and skips items that were already imported, not a continue-from-where-it-stopped resume. For a store large enough to hit the time limit, retrying the whole thing repeatedly rarely finishes; instead, reduce the scope of each run by selecting fewer data types in step 3 (products in one run, orders in another) and make several smaller passes.

## Cancel

**Cancel** is available on a running migration, and it marks the job as failed in the dashboard immediately. It does **not** stop the background import task, which keeps running and writing data until it reaches a natural stopping point. Expect imported counts to keep climbing for a while after you cancel — let them settle before deciding what to clean up, rather than acting on counts captured the moment you clicked Cancel.

## There is no pause or resume

Spwig does not support pausing an in-progress migration and picking it back up later. The **Resume** button on the dashboard is for a different case: a migration configured through the wizard but never started. It reopens the wizard where you left off configuring it — unrelated to a run already in progress.

## Rollback

> **Warning:** Rollback is a permanent, destructive action. Read this section in full before using it.

Rollback is offered on a **completed** migration, and again on one whose own rollback previously failed partway through (status **Rollback Failed**), so a stalled rollback can be retried. It removes only what the import itself created, and keeps anything your store now depends on:

- A migrated customer who has placed a genuine order since the import is **kept** — their account, addresses, loyalty history, and store credit stay with them, and that real order is left untouched. Only the orders the import created are removed.
- A migrated product still referenced by any order, bundle, gift card, or configurator slot is **kept**. Orders belonging to other customers are never modified — rollback can no longer strip line items out of an unrelated order or leave it with the wrong total.
- Whatever is kept is reported back to you by name and count, with the reason — for example "1 Product kept, still referenced by an order item" — so you know exactly what's still there and why.
- Affiliates, commissions, and payouts the import created **are** removed, along with any affiliate account the import created. An affiliate attached to a customer who already existed keeps their account; only the affiliate record goes.
- Loyalty history and store credit follow the customer: removed if the customer is removed, kept if the customer is kept.

It still does **not** remove subscription plans, pricing tiers, or booking resources created by store extensions — those survive a rollback and need cleaning up by hand if you don't want them.

Before you confirm, the confirmation page shows a preview of exactly what will be removed and what will be kept, calculated against your live data — read it before clicking **Yes, Rollback Migration**. Rollback then runs in the background rather than in your browser, so it's safe to close the tab; check the migration's status for the report of what was actually removed and kept once it finishes.

Because rollback no longer reaches beyond what the import created, it's no longer a same-day-only tool — a migrated customer's real orders and a migrated product's real sales are protected however much time has passed since the migration. It's still a permanent, destructive action on the rows it does remove, so use it deliberately rather than casually, and clean up by hand anything Spwig keeps that you don't actually want.

On availability: the Rollback button stays on a completed migration's summary for as long as the job record exists — for most platforms there's no fixed deadline. Magento is the exception and loses rollback availability after a set window, so decide quickly if you're on Magento. Job records are not removed on any schedule, so a migration stays rollbackable indefinitely unless you delete its record yourself.

## Large-store strategy and slow imports

For a store large enough that a single run risks the 4-hour limit:

- **Raise the batch size** in step 3 (up to 100) — larger batches usually mean fewer round trips and faster throughput.
- **Split the migration across multiple runs by data type** — categories and products in one run, customers and orders in a follow-up, rather than everything at once.
- **Keep Skip existing items on** for every run after the first, so repeated runs don't duplicate what already succeeded.
- **Turn off Import product images.** Downloading and processing every image is usually the single biggest factor in a slow run. You can add images to products individually, or through a separate CSV import, once the rest of the data is in place.

## Tips

- **Test the connection after every credential change**, not once at the end — it isolates which value is wrong.
- **Never assume a failed job cleaned up after itself** — check what's actually in your store before deciding on cleanup or a retry.
- **Skip existing items should stay on for every retry** — it's the only thing preventing duplicates on a second pass.
- **Don't fight the 4-hour limit with more retries** — split by data type instead.
- **Read the rollback preview before confirming** — it names exactly what will be removed and what will be kept, calculated against your live data, so there are no surprises.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step2/
  filename: step2-connection-test-failed.webp
  description: Step 2 connection form showing a failed Test Connection result and the error message
  save-to: core/static/core/admin/img/help/migration-troubleshooting/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-rollback-panel.webp
  description: Completion page Rollback panel with the warning text and Rollback Migration button on a completed job
  save-to: core/static/core/admin/img/help/migration-troubleshooting/
  viewport: 1440x900
-->
