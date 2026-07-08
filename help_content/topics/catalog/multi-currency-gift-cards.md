---
slug: multi-currency-gift-cards
title_i18n_key: Multi-Currency Gift Cards
category: products
component: catalog
keywords:
  - multi-currency gift card
  - gift card currency
  - foreign currency gift card
  - NZD gift card
  - SGD gift card
  - international gift card
  - gift card exchange rate
  - currency-specific gift card
  - regional gift card
  - gift card redemption currency
  - cross-border gift card
  - gift card balance currency
url_patterns:
  - /admin/catalog/product/
  - /admin/catalog/product/\d+/change/
  - /admin/catalog/giftcard/
related:
  - gift-cards
  - add-product
  - voucher-codes
published: true
---

If you sell to customers in multiple countries, you can issue gift cards in specific currencies. For example, a New Zealand customer can buy a $50 NZD gift card and the recipient redeems it in NZD — the face value stays the same regardless of exchange rate fluctuations.

This feature requires multi-currency to be enabled with at least one exchange rate provider configured.

## How it works

When you set a **Gift Card Currency** on a gift card product, the system converts the product price into the target currency at the time of purchase using the current exchange rate. The resulting gift card is denominated in that currency and can only be redeemed by customers shopping in the same currency.

| Step | What happens |
|------|-------------|
| **Product setup** | You set the gift card product price in your base currency and choose a target currency (e.g., NZD) |
| **Purchase** | A customer buys the gift card. The base price is converted to NZD at the current exchange rate |
| **Gift card created** | The gift card is issued with its value in NZD (e.g., NZ$78.50) |
| **Redemption** | The recipient applies the code at checkout while shopping in NZD. The NZD balance is deducted |

## Prerequisites

Before setting up multi-currency gift cards, make sure you have:

1. **Multi-currency enabled** — Go to **Settings > Store Settings** and enable multi-currency support
2. **Supported currencies configured** — Add the currencies you want to offer (e.g., NZD, SGD, EUR)
3. **Exchange rate provider connected** — Go to **Settings > Exchange Rates** and configure a provider so that live rates are available

## Setting up a multi-currency gift card product

### Step 1: Create or edit a gift card product

1. Navigate to **Products > All Products**
2. Click **+ Add Product** or open an existing gift card product
3. Set **Product Type** to **Gift Card**

### Step 2: Set the gift card currency

1. Click the **Gift Card** tab
2. Configure your denomination settings as usual (fixed amounts, custom amounts, or both)
3. At the bottom of the Gift Card tab, find the **Gift Card Currency** dropdown
4. Select the target currency (e.g., **NZD - New Zealand Dollar**)
5. Save the product

The dropdown shows all currencies enabled in your store settings. Selecting **Store base currency (default)** means gift cards will be issued in your base currency — this is the standard behavior.

### Step 3: Set pricing

Set the product price in your base currency as you normally would. When a customer purchases this gift card, the price is automatically converted to the target currency using the current exchange rate.

**Example:** Your base currency is USD. You create a gift card product priced at $50 USD with Gift Card Currency set to NZD. If the exchange rate is 1 USD = 1.57 NZD, the resulting gift card will have a value of NZ$78.50.

## Currency matching and redemption

Multi-currency gift cards use **same-currency redemption** — the customer's active shopping currency must match the gift card's currency.

### What customers experience

- A customer shopping in **NZD** can apply an NZD gift card at checkout
- A customer shopping in **USD** cannot apply an NZD gift card — they will see a message explaining the currency mismatch
- Customers can switch their shopping currency using the currency selector on your storefront before applying the gift card

### How the balance works

The gift card balance is always tracked in its native currency:

- A NZ$78.50 gift card starts with NZ$78.50 balance
- If a customer makes a NZ$30 purchase, the remaining balance is NZ$48.50
- The balance does not fluctuate with exchange rates — the face value is fixed

When the gift card is applied at checkout, the system converts the discount to your base currency internally for order calculations, but the gift card balance is always deducted in its native currency.

## Managing multi-currency gift cards

Navigate to **Products > Gift Cards** to view all issued gift cards. Multi-currency gift cards display with their native currency:

- **Balance** shows in the gift card's currency (e.g., NZ$48.50)
- **Transactions** record amounts in the gift card's currency
- **Initial value** shows the converted amount at time of purchase

### Checking exchange rate details

Each gift card transaction records the exchange rate used at the time of the transaction. This provides a full audit trail for accounting purposes.

## Examples

### Example 1: Regional gift card for New Zealand

**Scenario:** You operate from the US but have customers in New Zealand. You want to sell NZD-denominated gift cards.

| Setting | Value |
|---------|-------|
| Product name | NZ Gift Card |
| Product type | Gift Card |
| Price | $50.00 (USD — your base currency) |
| Denomination type | Fixed Denominations |
| Fixed denominations | 25, 50, 100, 200 |
| Gift Card Currency | NZD - New Zealand Dollar |
| Expiration | 365 days |

When a customer selects the $50 denomination:
- The system converts $50 USD to NZD at the current rate
- A gift card is created with the NZD equivalent (e.g., NZ$78.50)
- The recipient can redeem it while shopping in NZD

### Example 2: Multiple currency gift cards

**Scenario:** You sell to customers in Singapore, Australia, and the UK. Create three gift card products:

1. **SG Gift Card** — Gift Card Currency: SGD
2. **AU Gift Card** — Gift Card Currency: AUD
3. **UK Gift Card** — Gift Card Currency: GBP

Each product converts your base price to the target currency at purchase time. Customers in each region can redeem the gift card in their local currency.

### Example 3: Mixed gift card offering

**Scenario:** You want to offer both base-currency and regional gift cards.

- **Store Gift Card** — Gift Card Currency: *Store base currency (default)* — redeemable in your base currency
- **NZ Gift Card** — Gift Card Currency: NZD — redeemable in NZD only

Both products can coexist in your catalog. Customers see which currency a gift card is denominated in when checking the balance.

## Tips

- Start with one regional currency and test the full flow (purchase, delivery, redemption) before adding more currencies.
- The exchange rate at the time of purchase determines the gift card value. If rates change significantly, the gift card value stays fixed — this protects both you and your customers.
- Make the currency clear in the product name (e.g., "NZ Gift Card" or "Gift Card (NZD)") so customers know what they are buying.
- Gift cards without a currency set continue to work exactly as before in your base currency — existing products are not affected.
- Monitor your exchange rate provider to ensure rates are up to date. Stale rates could lead to over- or under-valued gift cards.
- Consider your denominations carefully. A $25 USD denomination converts to approximately NZ$39 — round denominations in the target currency may look better. You can create separate products with denominations that are round numbers in the target currency.
