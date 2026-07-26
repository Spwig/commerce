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
  - manual gift card
  - issue gift card
url_patterns:
  - /admin/catalog/giftcard/
  - /admin/catalog/giftcard/add/
  - /admin/catalog/product/
  - /admin/catalog/product/\d+/change/
related:
  - add-product
  - voucher-codes
  - multi-currency-gift-cards
  - pos-system-overview
published: true
---

Gift cards are store credit that customers can buy for someone else — or for themselves — delivered by email as a unique redemption code. You can also issue a gift card directly from the admin without a customer purchase.

Selling gift cards is live. When a customer buys one, the card is created and emailed automatically once their payment clears — never before, so nobody receives a code for a payment that later fails.

A few things worth knowing before you enable a gift card product:

- **A gift card is money, not a discount.** It comes off the final bill after tax and shipping, and it does not reduce the tax you owe. That is the opposite of a voucher, which reduces the price of the goods.
- **Cards are single-currency.** A card bought in euros can only be spent on a euro order. If you sell in several currencies, create a separate gift card product for each one. This protects you from exchange-rate movements on a balance that might not be spent for a year.
- **Gift cards cannot be discounted.** A voucher will not apply to a gift card line, because selling £100 of credit for £80 loses you £20 every time.
- **A gift card cannot buy another gift card.** This closes a route people use to launder stolen card details.
- **Buying a gift card does not earn loyalty points.** The points are earned when the card is spent on goods, so nobody earns twice on the same money.

![Gift card management](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Denomination Types

These settings control how a customer chooses the amount when buying a gift card:

| Type | Description |
|------|-------------|
| **Fixed Denominations** | Customers choose from preset amounts (e.g., $25, $50, $100) |
| **Custom Amount** | Customers enter any amount within a min/max range |
| **Both** | Offer preset denominations plus a custom amount option |

## Creating a Gift Card Product

Every gift card — whether it will eventually be sold or is issued by hand today — needs a Gift Card type product behind it first.

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

### Step 2: Publishing

Publish the product when you're ready to sell it. Customers can buy it from your storefront straight away, and the card is emailed automatically once their payment clears.

The product is also what you select from when issuing a card by hand — so it's worth creating one even if you only ever plan to give cards away.

## Creating a Gift Card by Hand

This is the only way to create a funded gift card right now, and it works fully today.

1. Navigate to **Products > Gift Cards** and click **+ Add Gift Card**
2. Choose the **Product** — this must be an existing Gift Card type product (see above)
3. Enter the **Initial Value** — the starting balance, in whatever amount you choose. Unlike a customer purchase, this isn't limited to the product's denomination settings
4. Optionally set an **Expires At** date, and leave **Active** checked so the card can be redeemed
5. Fill in the **Recipient** section, further down the same page:
   - **Recipient Email** — required; where the delivery email will be sent
   - **Recipient Name**, **Sender Name**, and **Personal Message** — all optional
   - **Scheduled Send At** — optional; leave blank and send whenever you're ready, or set a future date/time (e.g., a birthday)
6. Click **Save**

The redemption code is generated automatically and the starting balance is set from the Initial Value — you don't fill either of those in yourself.

**Saving the card does not email it.** To deliver it, go back to the gift card list, select the card's checkbox, choose **Send gift card emails** from the Actions dropdown, and click **Go**. The same action re-sends the email if you need to resend it later.

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
- **Sender** — Who purchased (or who issued) the gift card

### Actions

- Click a gift card to **edit** its details and view its full **transaction history**, shown inline on the same page
- Select one or more cards and use the **Actions** dropdown to **Send gift card emails** (delivers or re-sends the delivery email) or **Mark selected gift cards as inactive** (deactivates — balance is preserved but the card can no longer be redeemed)

## Redemption Today

**In store**, at your Point of Sale terminal:

1. The cashier takes the code at the payment step
2. The code is validated — active, not expired, has balance, and in the same currency as the sale
3. The balance is applied to the full amount owed, including tax and delivery
4. If the balance doesn't cover the whole sale, the customer pays the rest another way
5. The balance is deducted and the transaction recorded

Note the cashier takes the code at **payment**, not when building the basket. A gift card is money the customer has already handed over, so it settles the bill rather than discounting the goods.

**Online**, the checkout has a gift card field on the payment step. The customer enters their code, the balance comes off the amount due — after tax and delivery — and any remainder is charged to their card as usual. If the card covers the whole order, no other payment is needed. The balance is only actually deducted once payment is confirmed, so an abandoned checkout never touches the card.

Recipients can also check their remaining balance any time at the link in their delivery email.

## Refund Handling

When refunding orders or sales that used a gift card:

- **A gift card the customer bought, still unused** — the card is deactivated and its balance zeroed, so the credit disappears along with the refund.
- **A gift card the customer bought and has partly spent** — this needs your judgement. Deactivating it would take back credit they have already used, so the balance is left alone and flagged for you to adjust by hand.
- **A gift card used to pay for the order being refunded** — the refund goes back to the card first, before any card or bank payment. Refunding money to a bank that the merchant never actually collected is the worse mistake, and returning value where it came from also closes off a known fraud route. If the original card has since expired or been deactivated, a replacement card is issued to the same recipient with no expiry date.
- **Full refund** — Credit the amount back to the gift card balance through a refund transaction

## Tips

- Use manual issuance for goodwill credits, customer service resolutions, or any case where you want to hand a customer store credit without a storefront purchase.
- Set reasonable expiration periods (e.g., 365 days) to comply with local gift card regulations — some jurisdictions require minimum validity periods.
- Use the "Both" denomination type to offer convenience (preset amounts) and flexibility (a custom amount).
- Monitor the Total Balance metric regularly — it represents an outstanding liability on your books.
- A card spends the same way online and in person — at web checkout on the payment step, or at the register. The delivery email includes a balance-check link recipients can use any time.
- If you sell to customers in multiple countries, you can issue gift cards in specific currencies — see the **Multi-Currency Gift Cards** help topic for details.
