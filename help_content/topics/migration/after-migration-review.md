---
slug: after-migration-review
title_i18n_key: After Your Migration
category: migration
component: migration
keywords:
  - after migration checklist
  - verify migrated data
  - link rewriting
  - migration link suggestions
  - download migration report
  - migration report PDF
  - configure tax after migration
  - configure shipping after migration
  - going live after migration
  - reset customer passwords
  - migration next steps
  - point DNS to Spwig
url_patterns:
  - /admin/migration/migrationjob/
  - /admin/migration/migrationjob/wizard/step6/
related:
  - migration-overview
  - migration-troubleshooting
  - migration-field-mapping
  - migrate-from-woocommerce
published: true
---

A completed migration is the start of your review, not the end of it. Step 6 of the wizard gives you a summary of what came across, a tool for fixing links that still point at your old site, and a report you can download for your records. This topic walks through what to check before you consider the move finished, including the tax, shipping, and go-live work the wizard itself does not do for you.

## Reading your results

At the top of the completion page you'll see a row of stat cards — one per data type (Products, Categories, Customers, Orders, and so on) — followed by an **Import Summary** table with Imported, Skipped, Failed, and Total columns for every step that ran.

- **Imported** — items created successfully in Spwig.
- **Skipped** — items your source platform had, but Spwig did not create. This is almost always expected: with **Skip existing items** on in step 3, anything matching an item that already existed in Spwig (by SKU, email, etc.) is left alone rather than duplicated. A high skip count after a retry usually just means the first attempt already created those records.
- **Failed** — items Spwig tried and could not create, due to a data problem, a missing dependency, or an error on the source side. A nonzero failed count is worth investigating; see [Migration Troubleshooting](migration-troubleshooting) for how to read the logs and what your cleanup options are.

> **Note:** If any step shows failures, don't assume the store rolled anything back to compensate — it doesn't. Whatever imported before the failure is sitting in your store alongside everything that succeeded. Review it the same way you would a normal partial result.

## Link Rewriting

Products, pages, and blog posts imported from your old platform often contain links back to their original domain — an image URL, a "related product" link, an internal cross-reference. If Spwig detects any of these in the content it just imported, a **Link Rewriting** panel appears on the completion page.

Each detected link is grouped by the page or product it came from, and shown with:

- **Original URL** — the link exactly as it appeared in the imported content.
- **Suggested URL** — Spwig's best guess at the equivalent page on your new store, if one was found.
- **Match** — a confidence percentage for that suggestion. Links with no reasonable match show as **None** and have no suggested URL to approve.

For each link you can **Approve** the suggestion or **Skip** it, one at a time. **Auto-approve high confidence** approves every suggestion at or above 85% in one click — a time-saver, but still worth spot-checking afterward. Suggestions below that threshold are the ones worth opening by hand: a 50-70% match might be the right product under the wrong name, or it might be nowhere close, and only a human glance can tell.

Approving or skipping only marks a link — nothing in your content changes until you click **Apply Approved Links**, which rewrites every approved link at once. That means it's safe to work through the list over more than one sitting before committing.

> **Tip:** Leave any link you're not sure about as **Skip** rather than approving a guess. You can always fix a stray old-domain link manually later; a wrong rewrite applied to dozens of products is more work to undo.

## Verifying your data

Treat the stat cards as a starting point, not proof that everything is correct. Spend a few minutes spot-checking:

- **Products** — Open a handful of products, especially ones with variants (size, color, etc.), and confirm variant options and prices came through correctly, and that images attached and show on the storefront, not just in the admin.
- **Categories** — Confirm the category hierarchy looks right, particularly if you migrated from Shopify, where collections import as a flat list rather than a nested tree.
- **Customer accounts** — Spot-check emails and addresses on a few records. Migrated customers do not carry their old password over — Spwig has no way to read it from the source platform — so **customers will need to reset their password** the first time they sign in. Consider a heads-up email once you go live.
- **Orders** — Check that totals, statuses, and line items on a sample of orders match what you saw on the old platform.
- **Extension-derived products** — If you migrated from WooCommerce with extensions like Subscriptions, Bundles, Gift Cards, Composite Products, or Bookings, spot-check products that used them. Extension data that can't be read doesn't block the product from importing — it still comes across, just without that extra configuration — so these products are the most likely to need a manual touch-up.

## Configuring tax and shipping

The wizard's step 4 options for importing tax settings and shipping zones record your preferences, but they are not applied to the import — no tax rates or shipping zones are created from them. This is expected: **tax and shipping setup is a normal, separate step you complete directly in Spwig** after the data import finishes, the same as you would when setting up a new store.

The **Price adjustment** control on that same step is the exception — it does take effect for WooCommerce, CSV and Shopify imports, shifting each product's base price as it is created. If you set one and your prices look wrong, that is where the change came from. See [Migration Field Mapping](migration-field-mapping) for the details.

Before you go live, configure:

- Your tax rates — see [Tax Configuration](tax-configuration) for setting up rates by country, state, or region, including any exemptions your products need.
- Your shipping zones and methods — see [Setting Up Shipping](setup-shipping) to recreate the shipping options your customers had on your old platform.

Do this before testing checkout, so your test order reflects real totals.

## Downloading your report

The completion page offers three downloads:

- **Download PDF** — a formatted summary with job metadata, per-step counts, and a list of errors, capped at the **first 20 errors**.
- **Download CSV** — the same summary in spreadsheet form, capped at the **first 50 errors**.
- **Download Logs** — every log entry for the job, with no cap.

If your failed count is small, the PDF or CSV is enough. For a migration with a large number of failures, download the logs instead — the only one of the three with the complete record rather than a truncated sample.

> **Tip:** Migration job records — including their logs and reports — stay in Spwig indefinitely; nothing removes them on a schedule. Download a copy anyway if you want it for offline records or to share with someone who doesn't have admin access, but there's no countdown forcing you to do it today.

## Going live

Once you're satisfied with your data, tax, and shipping setup:

1. **Test checkout end to end.** Add a product to the cart, complete checkout, and confirm tax, shipping, and payment all calculate and process correctly, ideally with a real payment method in test mode.
2. **Update your DNS** to point your domain at Spwig only once that test succeeds. Don't switch DNS first and debug afterward — customers could hit a broken checkout in the meantime.
3. **Keep your old store available, in a read-only or "closed" state**, until you're confident the new one is handling orders correctly. This gives you a fallback without risking orders being placed on the old platform after the switch.

## Revoking source-platform credentials

Once you've verified the migration is complete and don't expect to run it again, go back to your source platform and revoke or delete the API key, app, or integration you created for it (see [Migrating from WooCommerce](migrate-from-woocommerce) or the equivalent platform guide for where that credential lives). Spwig doesn't need standing access to your old store after the import finishes, so removing it closes off a credential you no longer use.

## Tips

- **Skipped is usually fine, failed is not** — a large skipped count after a retry with Skip existing items on is expected; a nonzero failed count deserves a look at the logs.
- **Don't rush Apply Approved Links** — approvals and skips are free to change right up until you click Apply, so take your time on the low-confidence ones.
- **Set up tax and shipping before your first live sale**, not after — the import doesn't do this for you, and an unconfigured tax rate is easy to miss until a customer complains.
- **Warn customers about password resets** if you're emailing your customer list about the move, so the first login isn't a surprise.
- **Download your report before the 90-day mark** if you need it for accounting or compliance records.
- **Keep the old store around, read-only, for a while** — it costs little and gives you a safety net during your first days live on Spwig.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: Migration completion page showing the stat cards and Imported/Skipped/Failed/Total summary table
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Link Rewriting panel with grouped suggestions, confidence percentages, and the Approve/Skip/Apply Approved Links controls
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->
