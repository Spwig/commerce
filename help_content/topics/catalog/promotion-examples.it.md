---
title: Esempi di promozioni
---

This guide shows concrete examples of how to configure different promotion types. Each example includes the exact field values to enter in the promotion wizard so you can follow along or adapt them for your store.

![Promotion Card](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## Example: Percentage Off a Category

**Scenario:** 30% off all shoes for the winter clearance.

Navigate to **Marketing > Sales & Promotions** and click **+ Create Promotion**. Enter the following values at each step of the wizard:

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | Winter Clearance — 30% Off Shoes |
| Basics | Description | End-of-season clearance for all footwear |
| Basics | Active | Checked |
| Discount | Type | Percentage Off |
| Discount | Value | 30 |
| Schedule | Start Date | Jan 15, 2026 |
| Schedule | End Date | Feb 28, 2026 |
| Products | Apply To | Categories |
| Products | Selected | Shoes, Boots, Sandals |

This creates a time-limited sale that automatically discounts every product in the selected categories. A $120 pair of boots becomes $84, and a $60 pair of sandals becomes $42.

## Example: Fixed Amount Off a Collection

**Scenario:** $15 off items in the Summer Essentials collection.

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | Summer Essentials — $15 Off |
| Basics | Active | Checked |
| Discount | Type | Amount Off |
| Discount | Value | 15.00 |
| Schedule | Start Date | Jun 1, 2026 |
| Schedule | End Date | (empty — no expiration) |
| Products | Apply To | Collections |
| Products | Selected | Summer Essentials |

> **Note:** The $15 discount applies to each eligible product individually. A $50 product becomes $35, a $30 product becomes $15. Leaving the End Date empty means the promotion runs indefinitely until you deactivate it manually.

## Example: Fixed Sale Price for Clearance

**Scenario:** Set all clearance items to $9.99.

| Step | Field | Value |
|------|-------|-------|
| Basics | Name | Final Clearance — Everything $9.99 |
| Basics | Active | Checked |
| Discount | Type | Fixed Sale Price |
| Discount | Value | 9.99 |
| Schedule | Start Date | (today) |
| Products | Apply To | Collections |
| Products | Selected | Final Clearance |

> **Note:** Fixed Sale Price sets the exact selling price regardless of the original price. A $75 item and a $25 item both become $9.99. Use this for clearance racks or uniform pricing where you want every item at the same price point.

![Category Promotion](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## Choosing the Right Discount Type

| Type | How It Works | Best For | Example |
|------|-------------|----------|---------|
| **Percentage Off** | Reduces price by a percentage | Broad sales where products have varying prices | 20% off — $100 becomes $80, $50 becomes $40 |
| **Amount Off** | Subtracts a fixed dollar amount | Promotions with a specific dollar saving message | $15 off — $100 becomes $85, $50 becomes $35 |
| **Fixed Sale Price** | Sets the exact selling price | Clearance, uniform pricing, "everything at $X" | $9.99 — all items become $9.99 regardless of original price |

## Choosing the Right Target

| Target | How It Works | Best For |
|--------|-------------|----------|
| **All Products** | Applies to every product in your store | Sitewide sales, store-wide events |
| **Categories** | Applies to all products in selected categories | Department sales, seasonal clearance by type |
| **Brands** | Applies to all products from selected brands | Brand partnerships, brand-specific events |
| **Collections** | Applies to all products in selected collections | Curated promotions, themed sales |
| **Products** | Applies to individually selected products | Hand-picked deals, limited selections |

## Scheduling Patterns

Three common patterns for setting up promotion schedules:

| Pattern | Start Date | End Date | Use Case |
|---------|-----------|----------|----------|
| **Immediate, ongoing** | Today | (empty) | Permanent price reductions, long-term sales |
| **Date range** | Future date | Future date | Seasonal events, holiday sales |
| **Future start, no end** | Future date | (empty) | New permanent pricing that starts on a specific date |

Setting a Start Date in the future creates a scheduled promotion. It will appear in the **Scheduled** tab on the promotions dashboard and activate automatically when the date arrives. Leaving the End Date empty means the promotion stays active until you deactivate it manually.

## Tips

- **Use descriptive names** — Include the discount value and target in the name (e.g., "Summer 20% Off Shoes") so you can quickly identify promotions on the dashboard.
- **Check the affected products count** — The Review step shows how many products will be discounted. If the number seems wrong, go back and check your targeting.
- **Start small** — If you are unsure about a discount, start with a smaller percentage and increase it if needed.
- **Use Amount Off for marketing** — "$15 off" is a concrete saving that is easy to communicate in ads and email campaigns.
- **Use Percentage Off for fairness** — A percentage discount scales with price, giving proportional savings across different price points.