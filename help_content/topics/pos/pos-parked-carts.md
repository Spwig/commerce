---
slug: pos-parked-carts
title_i18n_key: Parking and Resuming POS Transactions
category: point-of-sale
component: pos_app
keywords:
  - park cart
  - parked cart
  - pause transaction
  - hold transaction
  - resume sale
  - POS hold
  - serve next customer
  - multiple transactions
  - suspend cart
  - POS parked carts
  - restore cart
  - interrupt sale
  - POS queue
url_patterns:
  - /admin/pos_app/parkedcart/
related:
  - pos-overview
  - pos-terminal-setup
  - pos-shifts-cash-management
  - getting-started-with-pos
published: true
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/parkedcart/
  filename: parked-cart-list.webp
  description: Parked cart list view (may be empty on fresh install — capture anyway)
  save-to: core/static/core/admin/img/help/pos/
-->

Parked carts let your cashiers pause a transaction and immediately start serving the next customer — without losing a single item or discount. When you are ready, the original cart is restored exactly as it was and the sale continues from where it left off.

## What parking a cart does

When a cashier taps **Park** on the POS register, Spwig saves a complete snapshot of the current cart to the server. The register clears so a fresh transaction can begin straight away. The parked cart is stored and tied to the terminal it was created on.

Nothing is lost in the snapshot. The parked cart preserves:

- Every item and its quantity
- Any customer that was attached to the sale
- Manual discounts applied to the cart or individual items

The parked cart stays available on the same terminal for up to **24 hours**. After that, Spwig automatically removes it. Carts that have already been restored are removed immediately after restoration and do not count toward the 24-hour window.

## How to park a transaction

You must have at least one item in the cart before you can park. An empty cart cannot be parked.

1. While a sale is in progress, tap the **Park** button in the POS register.
2. Spwig saves the cart and clears the register. You will see a confirmation and the cart count in the parked-carts area will update.
3. Start the next customer's transaction on the now-empty register.

If the customer has been attached to the sale before parking, their name will appear in the parked cart list for easy identification.

## How to resume a parked transaction

1. Tap the **Parked Carts** area or icon on the POS register. You will see a list of all carts currently parked on this terminal, showing the customer name (if one was attached), item count, total amount, the cashier who parked it, and the time it was parked.
2. Tap the cart you want to resume.
3. If your current register has items in it, the POS will clear those items before restoring the parked cart. Make sure you have either completed or parked the current transaction before resuming another one.
4. The parked cart's items, customer attachment, and manual discounts are all restored. The sale continues as normal.

## Parked cart visibility

Parked carts are **tied to the terminal** they were created on. Any cashier logged in to the same terminal can see and resume any parked cart on that terminal — there is no per-cashier restriction on who can pick up a parked cart.

Carts parked on a different terminal, even at the same store location, are not visible on your current terminal.

## Cancelling a parked cart from the POS

A cashier can delete a parked cart directly from the parked-carts list on the terminal — tap the cart and use the delete or discard option. Deleted parked carts are permanently removed and cannot be recovered.

## Automatic expiry and cleanup

Each parked cart expires **24 hours after it was parked**. Spwig runs a background task that removes expired carts that were never resumed. There is nothing you need to do — the cleanup happens automatically.

If you need to clear parked carts before the 24-hour window, a cashier can delete them one at a time from the parked-carts list on the terminal.

## Shifts and parked carts

There is no hard link between a parked cart and the shift that was open when it was parked. Closing a shift does **not** automatically delete or cancel any parked carts on that terminal. Parked carts survive shift changes and remain available for the full 24-hour window.

This means:

- A cart parked at the end of a morning shift can be resumed by a cashier on a later shift.
- If you do not want parked carts to carry over between shifts, have cashiers clear the parked-carts list before closing their shift.

## Tips

- Park a cart the moment a customer says "I just need to grab one more thing" — it is faster than asking them to wait in line again or re-adding items manually.
- If the parked-carts list is getting long, check whether a previous cashier left transactions unresolved at the end of their shift and clear any stale carts.
- Attach a customer to the sale before parking when you can — their name appears in the list, making it much easier to find the right cart when they return.
- Parked carts expire after 24 hours, so they are not suitable for holding transactions overnight across multiple business days.
- Remember that resuming a parked cart will clear whatever is currently in the register. Complete or park the active transaction before picking up a different parked cart.
