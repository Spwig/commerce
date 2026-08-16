---
slug: stock-bulk-actions
title_i18n_key: Bulk Stock Actions
category: products
component: catalog
keywords:
  - stock transfer
  - transfer stock
  - damaged stock
  - lost stock
  - write off stock
  - stock write-off
  - recount stock
  - physical count
  - stock take
  - inventory count
  - stock movement
  - bulk stock action
  - warehouse transfer
  - stock adjustment
url_patterns:
  - /admin/catalog/stockitem/
related:
  - inventory-warehouses
  - stock-notifications
  - add-product
published: true
---

Beyond one-off adjustments, Spwig gives you three bulk actions on the **Stock Items** list for the inventory work that happens across many products at once: moving stock between warehouses, writing off damaged or lost units, and reconciling stock after a physical count. All three run from the same **Actions** dropdown, apply the same quantity to every stock item you select, and are fully recorded in the stock movement audit trail.

Navigate to **Products > Stock Items** to use them.

## Running a bulk stock action

1. On the **Stock Items** list, use the filters or search to find the items you want to update
2. Check the box next to each stock item to include (or use the header checkbox to select every item on the page)
3. Choose one of the three actions from the **Actions** dropdown:
   - **Transfer stock to warehouse**
   - **Record damaged/lost stock**
   - **Recount stock (physical count)**
4. Click **Go**
5. Review the confirmation page — it lists every selected stock item with its current **on hand**, **allocated**, and **available** quantities so you can double-check you selected the right items
6. Fill in the action's fields (see below) and click the submit button to apply

![The Stock Items list with the Bulk actions dropdown open, showing Transfer stock to warehouse, Record damaged/lost stock and Recount stock (physical count) alongside the other actions](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

The same quantity you enter is applied to **every** selected item — this is designed for moving, writing off, or recounting the same number of units across many SKUs at once (for example, transferring 10 units of several products into a new store location). For a single item with a different quantity, run the action again with just that item selected, or use **Adjust stock levels** instead.

## Transfer stock to warehouse

Use this to move available stock from each selected item's warehouse into a different warehouse — for example, restocking a new retail location from your main warehouse, or rebalancing inventory between regional fulfillment centers.

On the confirmation page, fill in:

| Field | Description |
|-------|-------------|
| **Destination warehouse** | Where the stock should move to. Only active warehouses appear in this list. |
| **Quantity per item** | Units to move out of each selected item's current warehouse. |
| **Reason** | Optional note, e.g. "Restocking new Auckland store". |

Click **Transfer Stock** to apply.

![The Transfer Stock confirmation page: a Selected Stock Items card listing three items with their on-hand/allocated/available figures, and a Transfer Details form with a destination warehouse, quantity, and reason filled in](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Only unreserved stock can move.** Spwig transfers from *available* stock (on hand minus units allocated to open orders) — units already promised to a customer's order stay in the source warehouse so that order can still be fulfilled. If a selected item doesn't have enough available stock to cover the quantity you entered, that item is skipped and an error explains why; the rest of the selection still transfers.

If a selected item is already stocked at the destination warehouse you chose, it's skipped automatically (there's nothing to transfer to itself), and you'll see a message telling you how many items were skipped for this reason.

Each transfer writes a paired set of movements to the audit trail — a negative **Warehouse Transfer** entry at the source and a matching positive one at the destination — so the full trail shows exactly where the stock came from and where it went.

## Record damaged/lost stock

Use this to write off units that are broken, spoiled, or missing — for example, after finding damaged goods in a delivery or investigating a discrepancy.

On the confirmation page, fill in:

| Field | Description |
|-------|-------------|
| **Quantity to write off (per item)** | Units to remove from on-hand stock for each selected item. |
| **Reason** | Optional note, e.g. "Water damage during storage". |

Click **Record Write-off** to apply.

**Reserved stock can't be written off.** On-hand stock can never drop below the quantity currently allocated to open orders — Spwig blocks the write-off for any item where the quantity you entered would eat into allocated stock, so you can't accidentally leave a paid order without the stock to fulfill it. If that happens for an item, you'll see an error naming the item and how many unreserved units it actually has available to write off.

Each write-off is recorded as a **Damaged/Lost** movement on that stock item, with a negative quantity.

## Recount stock (physical count)

Use this after a physical stock take to correct on-hand quantities to match what you actually counted — the fastest way to reconcile many items after a warehouse audit or cycle count.

On the confirmation page, fill in:

| Field | Description |
|-------|-------------|
| **Counted on-hand quantity (per item)** | The quantity you physically counted. On-hand is set to this exact number for every selected item — not added or subtracted. |
| **Reason** | Optional note, e.g. "Q3 warehouse stock take". |

Click **Apply Recount** to apply.

![The Recount Stock confirmation page: the Selected Stock Items card and a Recount Details form with the counted on-hand quantity and a reason filled in](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Unlike the other two actions, recount can move stock in either direction — up if you counted more than the system expected, down if you counted less. If the count you enter is lower than the quantity currently allocated to open orders, Spwig still applies it (a count is a fact, not something to argue with), but that item's **Available** figure will show as `0` on the stock list and its status icon will flip to Out of Stock — treat that as a signal to check whether the affected orders can still be fulfilled.

Each recount is recorded as a **Physical Recount** movement, with the quantity showing the correction (positive or negative) between the old and new on-hand figures.

## Reviewing what changed

Every transfer, write-off, and recount is logged the same way as any other stock change:

- Open a stock item and scroll to the **Stock Movements** section to see its full history
- Or navigate to **Products > Stock Movements** to browse movements across all items, filterable by type

Each entry records the movement type, the quantity change, the previous and new on-hand figures, who made the change, and the reason you entered (if any) — so a bulk transfer or write-off is just as traceable as a single manual adjustment.

## Tips

- Run **Recount stock** right after a physical stock take while the counted numbers are fresh — it's easier to catch a typo in the confirmation page than to untangle it later from the movement history.
- Always fill in **Reason** for write-offs and recounts. Six months from now, "Water damage during storage" is far more useful in the audit trail than a blank field.
- Before transferring stock, check the **Available** column on the confirmation page — it already accounts for allocated units, so you'll know immediately if a quantity is too high for one of the items you selected.
- These actions apply the same quantity to every selected item. Group your selection by items that genuinely need the same quantity moved, written off, or recounted, and handle exceptions one item at a time.
- If you use POS at a retail location, remember that warehouse's stock buffer isn't part of "available" for online orders — but bulk transfers and write-offs still work against the warehouse's real on-hand total.
