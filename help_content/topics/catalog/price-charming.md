---
slug: price-charming
title_i18n_key: Price Charming Rules
category: products
component: catalog
keywords:
  - price charming
  - psychological pricing
  - .99 pricing
  - charm pricing
  - round prices
  - price endings
  - "9.99"
  - price rounding
  - currency pricing
  - pricing strategy
url_patterns:
  - /admin/catalog/pricecharmongrule/
related:
  - add-product
  - promotion-examples
  - combining-discounts
published: true
---

Price charming (also called psychological pricing) automatically adjusts your product prices to end in specific digits that feel more attractive to customers. For example, instead of displaying a price of $20.00, price charming can show $19.99 — a widely used technique that makes prices appear lower at a glance.

Spwig applies price charming rules automatically across your store, per currency, so you only need to set each rule once.

## How price charming works

When a product price is calculated (including after promotions or discounts), Spwig checks whether an active price charming rule exists for that currency. If one does, the price is adjusted before it is displayed to customers. The adjustment applies to prices above your chosen minimum threshold.

You can configure separate rules for each currency your store accepts. For example, you might use `.99` endings for USD but round to the nearest `¥10` for JPY.

## Creating a price charming rule

1. Navigate to **Catalog > Price Charming Rules**
2. Click **+ Add Price Charming Rule**
3. Select the **Currency** this rule applies to (e.g., `USD`, `EUR`, `NZD`)
4. Choose a **Rule Type** (see the table below)
5. Optionally set a **Minimum Price Threshold** to exclude very low prices
6. Check **Apply to Sale Prices** if you also want charming applied when items are on sale
7. Ensure **Active** is checked
8. Click **Save**

Only one rule can exist per currency. If you need to change a rule, edit the existing one.

## Rule types

| Rule Type | Example | Best for |
|-----------|---------|----------|
| **Charm .99 ending** | $20.50 → $19.99 | Most retail products — the classic psychological price |
| **Charm .95 ending** | $20.50 → $19.95 | Slightly softer alternative to .99 |
| **Charm .90 ending** | $20.50 → $19.90 | Round-feeling but still below the next dollar |
| **Round Down** | $19.50 → $19.00 | Stores that prefer whole numbers |
| **Round Up** | $19.50 → $20.00 | Rounding up slightly for clean displays |
| **Round to nearest 5** | $23.00 → $25.00 | High-traffic retail and markets |
| **Round to nearest 10** | $23.00 → $20.00 | Larger-priced items such as appliances |
| **Round to nearest 100** | $1,234 → $1,200 | High-value items like furniture or electronics |
| **Custom ending** | Any — specify below | When your brand uses a specific ending like `.88` |

### Custom endings

If you choose **Custom ending**, enter the ending value in the **Custom Ending** field. For example, enter `0.88` to make all prices end in `.88` (common in some Asian markets).

## Minimum price threshold

Use the **Minimum Price Threshold** field to skip charming for very low-priced items where the adjustment would look odd. For example, setting a threshold of `5.00` means products priced under $5 are shown at their actual calculated price with no charming applied.

Leave it at `0` to apply charming to all prices.

## Sale prices

By default, charming is applied to both regular and sale prices. If you want your sale prices to display their exact calculated values (useful for time-limited promotional pricing where exact figures matter), uncheck **Apply to Sale Prices**.

## Deactivating a rule

To temporarily stop charming without deleting the rule, uncheck **Active** and save. The rule is preserved and can be re-enabled at any time.

## Tips

- Start with `.99` endings if you are unsure — it is the most widely recognised psychological pricing technique and works well across most product types.
- Set a minimum threshold if you sell low-cost items (under $5) so that a $3.50 item does not charm down to $2.99.
- Check your prices after enabling a new rule by viewing a product on the storefront — charmed prices display in real time.
- Japanese Yen and similar whole-number currencies work best with **Round to nearest 10** or **Round to nearest 100**, as decimal endings look unusual.
- Price charming is applied after all discounts and promotions, so your sale prices will also appear charmed unless you uncheck **Apply to Sale Prices**.
- You can have different rule types for different currencies, which is useful if you sell to multiple markets with different pricing conventions.
