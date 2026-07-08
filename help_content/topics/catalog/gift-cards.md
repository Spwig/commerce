---
slug: gift-cards
title_i18n_key: Gift Cards
category: products
component: catalog
keywords:
  - gift card
  - gift certificate
  - voucher
  - balance
  - denomination
  - redemption
  - gift card code
url_patterns:
  - /admin/catalog/giftcard/
  - /admin/catalog/product/
  - /admin/catalog/product/\d+/change/
related:
  - add-product
  - voucher-codes
  - multi-currency-gift-cards
published: true
---

Gift cards let your customers purchase store credit that can be sent to someone as a gift or kept for personal use. Recipients receive a unique code by email that they can redeem at checkout.

![Gift card management](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Denomination Types

Control how customers choose the gift card amount:

| Type | Description |
|------|-------------|
| **Fixed Denominations** | Customers choose from preset amounts (e.g., $25, $50, $100) |
| **Custom Amount** | Customers enter any amount within a min/max range |
| **Both** | Offer preset denominations plus a custom amount option |

## Creating a Gift Card Product

### Step 1: Set Up the Product

1. Navigate to **Products > All Products** and click **+ Add Product**
2. Set **Product Type** to **Gift Card**
3. Fill in the product name and description
4. Configure denomination settings:
   - Choose a **Denomination Type** (Fixed, Custom, or Both)
   - For Fixed: set the available denomination amounts
   - For Custom: set the **Minimum** and **Maximum** allowed amounts
5. Set **Expiration Days** (0 = never expires) — this determines how long gift cards are valid after purchase
6. Save and publish the product

### Step 2: Publish and Sell

Once published, the gift card appears in your storefront like any other product. Customers can browse to it, select an amount, and add it to their cart.

## Gift Card Lifecycle

A gift card follows this lifecycle:

1. **Purchase** — Customer buys the gift card product and provides recipient details
2. **Delivery** — An email with the gift card code is sent to the recipient automatically
3. **Redemption** — The recipient enters the code at checkout to apply the balance
4. **Balance Tracking** — Each use deducts from the balance until it reaches zero

## Customer Purchase Flow

When a customer buys a gift card:

1. **Select Amount** — Choose a denomination or enter a custom amount
2. **Recipient Details** — Enter the recipient's email address and name
3. **Personal Message** — Add an optional message to include in the delivery email
4. **Sender Name** — Provide the sender's name for the email
5. **Scheduled Delivery** — Optionally schedule the email for a future date (e.g., a birthday)
6. **Checkout** — Complete the purchase like any other product

## Automatic Delivery

After purchase, the gift card is delivered automatically:

- A styled email is sent to the recipient with:
  - The unique gift card code
  - The gift card value
  - The personal message from the sender
  - A link to check the remaining balance
- If scheduled delivery was set, the email sends at the specified date and time
- The sender receives an order confirmation with the gift card details

## Managing Gift Cards in Admin

Navigate to **Products > Gift Cards** to manage all gift cards:

### Statistics Dashboard

At the top of the page, four cards show key metrics:

- **Total Gift Cards** — Total number of gift cards issued
- **Active** — Currently active cards with available balance
- **Total Balance** — Combined remaining balance across all cards
- **Partially Used** — Cards that have been partially redeemed

### Filters

Filter gift cards by:

- **Search** — Find by code, email, or recipient name
- **Status** — Active, Inactive, Expired, Fully Redeemed, or Partially Used
- **Balance** — Has Balance or Zero Balance
- **Created** — Time period (Today, This Week, This Month, This Year)

### Gift Card Details

Each gift card shows:

- **Code** — The unique redemption code (e.g., GC-XXXX-XXXX-XXXX)
- **Recipient** — Email and name
- **Status badges** — Current status with color coding
- **Balance / Initial / Redeemed** — Financial summary with percentage used
- **Key dates** — Created, issued, first used
- **Sender** — Who purchased the gift card

### Actions

For each gift card, you can:

- **Edit** — View and modify gift card details
- **View Transactions** — See the full transaction history
- **Resend Email** — Re-send the delivery email to the recipient
- **Deactivate** — Disable the card (balance is preserved but cannot be used)

## Redemption at Checkout

When a customer enters a gift card code at checkout:

1. The code is validated (active, not expired, has balance)
2. The available balance is displayed
3. The balance is applied to the order total
4. If the balance covers the full order, no additional payment is needed
5. If the balance is less than the order total, the customer pays the remainder
6. The transaction is recorded and the balance is updated

## Refund Handling

When refunding orders that used a gift card:

- **Unused gift cards** — Deactivate the gift card entirely
- **Partially used cards** — The balance must be manually adjusted via a transaction
- **Full refund** — Credit the amount back to the gift card balance through a refund transaction

## Tips

- Set reasonable expiration periods (e.g., 365 days) to comply with local gift card regulations — some jurisdictions require minimum validity periods.
- Use the "Both" denomination type to offer convenience (preset amounts) and flexibility (custom amounts).
- Monitor the Total Balance metric regularly — it represents an outstanding liability on your books.
- Use scheduled delivery for seasonal promotions — customers can buy gift cards early and have them delivered on the exact date.
- Test the full flow (purchase, email delivery, redemption) with a test order before launching.
- If you sell to customers in multiple countries, you can issue gift cards in specific currencies — see the **Multi-Currency Gift Cards** help topic for details.
