---
slug: combining-discounts
title_i18n_key: Combining Discounts
category: promotions
component: catalog
keywords:
  - combining discounts
  - stacking discounts
  - discount priority
  - promotion stacking
  - voucher and sale
  - discount strategy
  - multiple discounts
  - discount layers
url_patterns:
  - /admin/catalog/promotion/
  - /admin/vouchers/vouchercode/
related:
  - sales-promotions
  - voucher-codes
  - running-a-sale
  - promotion-examples
published: true
---

The platform offers four types of discounts that can work together: product sales, promotions, voucher codes, and gift cards. Understanding how they interact helps you run effective campaigns without unexpected results or unintended double-discounting.

## The Four Discount Layers

Each discount type operates at a different level and is visible to customers in different ways.

| Layer | Where It's Set | How It's Applied | Visible To Customer |
|-------|---------------|-----------------|-------------------|
| **Product Sale** | Product edit form > Sale section | Automatically changes the displayed price | Yes — shown as a crossed-out original price |
| **Promotion** | Marketing > Sales & Promotions | Automatically applied to matching products | Yes — shown as a sale price on product cards |
| **Voucher Code** | Marketing > Vouchers | Customer enters a code at checkout | Only at checkout after entering the code |
| **Gift Card** | Applied at checkout from a gift card balance | Reduces the payment total | Only at checkout |

## How Priority Works

Promotions have a **Priority** field that accepts values of 0 and up. Higher numbers mean higher priority.

When multiple promotions match the same product, the one with the **highest priority wins**. They do not stack — only one promotion applies per product.

**Example:** "Flash Sale 50% off" (priority 10) and "Summer Sale 20% off" (priority 5) both target all products. A customer sees the 50% flash sale price, not 70% combined.

Within the same priority level, the system selects the promotion that gives the largest discount to the customer.

## Stacking Rules

The following table shows which discount combinations are allowed and how to control them.

| Combination | Allowed? | How to Control It |
|-------------|----------|-------------------|
| Product Sale + Promotion | Only if enabled | Check **"Stack with Product Sales"** in the promotion's Advanced Settings |
| Promotion + Promotion | No — highest priority wins | Set Priority values to control which one applies |
| Promotion + Voucher Code | Yes | Promotion discounts the product price, voucher discounts the cart total separately |
| Voucher + Voucher | Configurable | The voucher's **"Cannot combine with other vouchers"** flag controls this (enabled by default) |
| Voucher + Sale Items | Configurable | The voucher's **"Exclude sale items"** flag controls this |
| Gift Card + Any Discount | Yes — always | Gift cards are applied last, reducing the final payment amount after all other discounts |

## Common Scenarios

### Scenario A: Sitewide promotion + voucher code

- **Setup:** 20% off everything (promotion) + customer has a $10-off voucher
- **Result:** A $100 product becomes $80 (promotion), then the $10 voucher applies to the cart total. The customer pays **$70**.

### Scenario B: Product on sale + sitewide promotion

- **Setup:** Product has a 30% product-level sale + 20% sitewide promotion exists
- **Result (stacking disabled):** Only the product sale applies. The customer pays **$70**.
- **Result (stacking enabled):** Both apply. 30% off first = $70, then 20% off = **$56**.

### Scenario C: Two promotions on the same product

- **Setup:** "Flash Sale 40% off" (priority 10) + "Summer Sale 20% off" (priority 5), both target all products
- **Result:** Flash Sale wins because it has higher priority. The customer pays **$60** on a $100 product.

### Scenario D: Voucher on a sale item

- **Setup:** Product is on sale for 25% off. Customer enters a 10% voucher code that has "Exclude sale items" enabled.
- **Result:** The voucher does not apply to that product. If the cart has non-sale items, the voucher applies only to those.

## Which Discount Type to Use

| Goal | Recommended Approach | Why |
|------|---------------------|-----|
| Move seasonal inventory | **Promotion** (category or collection targeting) | Automatic, no customer action needed, visible on product cards |
| Reward a specific customer | **Voucher Code** (single use, per-customer limit) | Targeted, trackable, feels personal |
| Quick single-product deal | **Product Sale** (on the product edit form) | Fastest to set up, no promotion wizard needed |
| Store credit or gift | **Gift Card** | Balance-based, customer manages their own credit |
| Sitewide event | **Promotion** (all products targeting) | Maximum reach, one setup covers everything |
| Win-back campaign | **Voucher Code** (first-time or returning customer restrictions) | Can target specific customer segments |

## Tips

- **Test with a real cart** — after setting up promotions and vouchers, add products to a cart and go through checkout to verify the discounts apply as expected.
- **Check the "affected products" count** — in the promotion Review step, verify the number of affected products matches your intent.
- **Use priority deliberately** — if you run multiple promotions simultaneously, always set different priority values so you control which one wins.
- **Keep stacking disabled by default** — only enable "Stack with Product Sales" when you specifically want double discounts.
- **Document your strategy** — use the promotion Description field to note why a promotion exists and how it relates to other active promotions.
