---
slug: voucher-campaign-ideas
title_i18n_key: Voucher Campaign Ideas
category: promotions
component: vouchers
keywords:
  - voucher campaign
  - discount code ideas
  - welcome discount
  - free shipping code
  - seasonal voucher
  - loyalty voucher
  - referral code
  - promo code campaign
url_patterns:
  - /admin/vouchers/vouchercode/
related:
  - voucher-codes
  - voucher-examples
  - combining-discounts
published: true
---

This guide covers proven voucher campaigns you can set up in minutes. Each campaign includes the exact settings to configure so you can go from idea to live promotion quickly. Create all vouchers at **Marketing > Vouchers** and click **+ Add Voucher**.

![Welcome Voucher](/static/core/admin/img/help/voucher-campaign-ideas/welcome-voucher.webp)

## 1. Welcome Discount for New Customers

Offer first-time buyers an incentive to complete their purchase. A welcome discount builds trust and reduces hesitation for customers who have never ordered from your store.

| Field | Value |
|-------|-------|
| **Code** | `WELCOME15` |
| **Name** | Welcome discount — new customers |
| **Discount type** | Percentage Discount |
| **Discount value** | 15 |
| **Application scope** | Entire Cart |
| **Max uses per customer** | 1 |
| **Max uses total** | 0 (unlimited) |
| **First time customers only** | Checked |
| **Start date / End date** | Leave both empty — always active |

Promote this code in your signup confirmation email, on your homepage banner, or in a pop-up for first-time visitors. Because **First time customers only** is checked, returning customers cannot redeem it even if they find the code.

## 2. Free Shipping Threshold

Encourage larger orders by offering free shipping once the cart reaches a minimum value. Set the **Discount value** to an amount that covers your highest standard shipping cost.

| Field | Value |
|-------|-------|
| **Code** | `FREESHIP50` |
| **Name** | Free shipping on orders over $50 |
| **Discount type** | Fixed Amount Discount |
| **Discount value** | 15.00 (or your max shipping cost) |
| **Application scope** | Entire Cart |
| **Min order value** | 50.00 |
| **Max uses per customer** | 0 (unlimited) |
| **Cannot combine with other vouchers** | Checked |

Display this code prominently on your product pages and in the cart. Customers close to the threshold will often add another item to qualify, increasing your average order value.

## 3. Seasonal Campaign Codes

Run time-limited promotions tied to holidays, seasons, or events. Set a strict date range so the voucher activates and expires automatically.

| Field | Value |
|-------|-------|
| **Code** | `SUMMER25` |
| **Name** | Summer sale 2025 |
| **Discount type** | Percentage Discount |
| **Discount value** | 25 |
| **Max discount amount** | 50.00 |
| **Application scope** | Entire Cart |
| **Start date** | June 1 |
| **End date** | August 31 |
| **Cannot combine with other vouchers** | Checked |
| **Cannot combine with sale items** | Checked |

**Shared vs. unique codes** — A shared code like `SUMMER25` is simple to promote but can spread beyond your intended audience. For tighter control, use bulk generation to create unique single-use codes (each with **Max uses total** set to 1). Distribute unique codes through targeted emails so every customer gets their own.

## 4. Loyalty Reward Voucher

Reward your best customers with a fixed-amount voucher they can apply to their next order. Send it by email after a customer reaches a spending milestone or as a thank-you for repeat purchases.

| Field | Value |
|-------|-------|
| **Code** | `VIP20` |
| **Name** | VIP loyalty reward |
| **Discount type** | Fixed Amount Discount |
| **Discount value** | 20.00 |
| **Application scope** | Entire Cart |
| **Min order value** | 100.00 |
| **Max uses per customer** | 1 |
| **Max uses total** | 0 (unlimited) |
| **Days valid** | 90 |

Setting **Days valid** to 90 gives customers three months to redeem the reward from the date of first use. The **Min order value** of $100 ensures the discount applies to meaningful orders.

## 5. Influencer / Referral Code

Give influencers or brand ambassadors a personal code they share with their audience. Each code is tied to one person, making it easy to track which partner drives the most sales.

| Field | Value |
|-------|-------|
| **Code** | `SARAH10` |
| **Name** | Influencer — Sarah |
| **Discount type** | Percentage Discount |
| **Discount value** | 10 |
| **Application scope** | Entire Cart |
| **Max uses total** | 0 (unlimited) |
| **Max uses per customer** | 1 |

Create a separate voucher for each influencer so you can compare redemption counts on the voucher dashboard. Review each code's usage regularly to measure ROI and decide which partnerships to continue.

## 6. Flash Discount Code

Create urgency with a deep discount available for a very short window. Pair the code with an announcement bar or email blast to drive immediate traffic.

| Field | Value |
|-------|-------|
| **Code** | `FLASH40` |
| **Name** | 24-hour flash sale |
| **Discount type** | Percentage Discount |
| **Discount value** | 40 |
| **Max discount amount** | 75.00 |
| **Application scope** | Entire Cart |
| **Start date** | Friday 9:00 AM |
| **End date** | Saturday 9:00 AM |
| **Max uses total** | 200 |
| **Exclude sale items** | Checked |

Capping **Max uses total** at 200 protects your margins. Once the cap is reached, the code stops working automatically. Mention the limited quantity in your marketing — "first 200 customers only" — to amplify urgency.

## Campaign Quick Reference

| Campaign | Code Example | Type | Value | Key Settings |
|----------|-------------|------|-------|--------------|
| Welcome discount | `WELCOME15` | Percentage | 15% | First time only, per-customer = 1 |
| Free shipping | `FREESHIP50` | Fixed Amount | $15 | Min order $50, no combining |
| Seasonal sale | `SUMMER25` | Percentage | 25% | Date range, max discount $50 |
| Loyalty reward | `VIP20` | Fixed Amount | $20 | Min order $100, 90-day validity |
| Influencer code | `SARAH10` | Percentage | 10% | Per-customer = 1, track by code |
| Flash discount | `FLASH40` | Percentage | 40% | 24-hour window, 200 max uses |

## Tips

- **Keep codes short and memorable** — All-caps, no special characters. Customers type these at checkout, so `SUMMER25` beats `summer-sale-2025-promo`.
- **Track redemption counts** — Check the voucher dashboard regularly to see which campaigns perform best. Compare total redemptions against revenue to calculate ROI.
- **Test before launch** — Place a test order with the code to confirm it applies correctly, respects the minimum order value, and combines (or does not combine) as expected.
- **Rotate codes for repeat campaigns** — Use a new code each season (e.g., `SUMMER25`, `SUMMER26`) so you can measure each campaign independently and prevent old codes from circulating.
- **Set max discount amounts on percentage vouchers** — A 25% discount on a $1,000 order is $250. Use the **Max discount amount** field to cap the dollar value and protect your margins.
- **Use the announcement bar** — Pair flash and seasonal codes with your storefront announcement bar so every visitor sees the promotion immediately.
