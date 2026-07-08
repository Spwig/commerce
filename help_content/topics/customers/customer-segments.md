---
slug: customer-segments
title_i18n_key: Customer Segments
category: customers
component: customers
keywords:
  - customer segments
  - segment rules
  - targeted marketing
  - customer groups
  - VIP customers
  - at-risk customers
  - high value customers
  - frequent buyers
  - segment criteria
  - customer classification
  - marketing segments
  - customer targeting
related:
  - customer-analytics
  - abandoned-carts
  - customer-wallet
url_patterns:
  - /admin/customers/customersegment/
published: true
---

Customer segments let you automatically classify your customers into meaningful groups based on their purchase behaviour. Once customers are segmented, you can use those groups to focus your marketing efforts — for example, offering loyalty rewards to VIP customers or sending win-back campaigns to customers who haven't purchased in a while.

Spwig evaluates segment criteria against each customer's metrics and assigns them to the highest-priority segment they qualify for. This happens automatically as customer data is updated.

## Available segment types

Spwig comes with a set of built-in segment types. Each segment type has a fixed internal identifier, but you can customise the display name, description, criteria, and colour to match how you think about your customers.

| Segment Type | Typical Use |
|---|---|
| **Guest Customer** | Customers who checked out without creating an account |
| **New Customer** | Customers who have recently made their first purchase |
| **Regular Customer** | Customers with a steady purchase history |
| **Frequent Buyer** | Customers who buy often (short time between orders) |
| **High Value** | Customers with high total spending |
| **VIP Customer** | Your most valuable and loyal customers |
| **Bargain Hunter** | Customers who tend to purchase during sales |
| **At Risk** | Customers who haven't purchased in a while |
| **Inactive** | Customers who have been absent for an extended period |

## Understanding segment criteria

Each segment is defined by a combination of criteria. Spwig checks these against the stored metrics for each customer. All criteria within a segment are combined — a customer must satisfy every condition set to qualify.

### Spending criteria

- **Min Total Spent** — the customer must have spent at least this amount across all completed orders
- **Max Total Spent** — the customer must not have spent more than this amount

Use a spending range to identify a specific tier. For example, setting Min to $500 and Max to $2,000 would target mid-tier customers.

### Order count criteria

- **Min Orders** — the customer must have at least this many completed orders
- **Max Orders** — the customer must not have more than this many completed orders

Combining Min Orders with a spending minimum is a reliable way to define VIP customers: they buy frequently *and* spend generously.

### Recency criteria

- **Min Days Since Last Purchase** — the customer's most recent order must be at least this many days ago
- **Max Days Since Last Purchase** — the customer's most recent order must be within this many days

Recency criteria are essential for at-risk and inactive segments. For example, setting Min Days to 90 and Max Days to 365 identifies customers who have gone quiet but haven't been completely lost.

## Segment priority

When a customer qualifies for more than one segment, the segment with the **highest priority** value wins. You can set the priority for each segment in the **Display Settings** section of the segment form.

The **Guest Customer** segment is always evaluated first, independently of priority order, because guest status is determined by account type rather than purchase criteria.

## Viewing and managing segments

Navigate to **Customers > Customer Segments** to see all your configured segments. The list shows each segment's display name, internal type, assigned colour, priority, the current count of matching customers, and whether the segment is active.

![Customer Segments List](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Creating or editing a segment

1. Navigate to **Customers > Customer Segments**
2. Click an existing segment to edit it, or click **+ Add Customer Segment** to create a new one
3. Fill in the **Segment Information** tab:
   - **Name** — select the internal segment type from the dropdown
   - **Display Name** — the human-readable name shown in the admin (e.g., "VIP Customers")
   - **Description** — a brief internal note explaining what this segment represents
4. Set criteria across the relevant tabs:
   - **Criteria - Spending** — minimum and maximum total spend
   - **Criteria - Orders** — minimum and maximum order count
   - **Criteria - Recency** — minimum and maximum days since last purchase
5. Configure **Display Settings**:
   - **Color** — a hex colour used to visually identify this segment in lists
   - **Priority** — a higher number means this segment is evaluated first
   - **Is Active** — uncheck to disable the segment without deleting it
6. Click **Save** to apply the changes

### Example: Configuring a VIP segment

Here is a realistic example for a high-value VIP segment:

| Field | Value |
|---|---|
| Name | `vip` |
| Display Name | VIP Customers |
| Min Total Spent | $1,000 |
| Min Orders | 5 |
| Max Days Since Last Purchase | 180 |
| Priority | 90 |
| Color | `#FFD700` |

This says: a customer qualifies as VIP if they have spent at least $1,000, placed at least 5 orders, and made a purchase within the last 6 months.

### Example: Configuring an At Risk segment

| Field | Value |
|---|---|
| Name | `at_risk` |
| Display Name | At Risk |
| Min Days Since Last Purchase | 60 |
| Max Days Since Last Purchase | 180 |
| Priority | 30 |
| Color | `#FF6B35` |

## Using segments for targeted marketing

Segments are displayed on customer profiles throughout the admin, so your team immediately knows which tier each customer belongs to. Use this information to:

- **Run targeted voucher campaigns** — create vouchers restricted to customers in a specific segment, then use your email system to send them only to that group
- **Prioritise support** — flag VIP or high-value customers so your team can provide priority service
- **Plan re-engagement** — review the At Risk and Inactive segments regularly to identify customers who need a win-back email or special offer
- **Adjust marketing spend** — focus acquisition budget on channels that bring in high-value customers by analysing which cohorts segments they convert into

## Tips

- Start with the built-in segment types before creating custom criteria — they cover the most common segmentation needs out of the box
- Review the customer count on each segment periodically; a VIP segment with zero customers or an At Risk segment growing rapidly are both worth investigating
- Use the **Priority** field deliberately — if your criteria overlap between segments (e.g., a customer qualifies for both Frequent Buyer and High Value), the higher-priority segment wins
- Deactivate segments you are not currently using rather than deleting them — you can reactivate them later without reconfiguring the criteria
- Segment criteria are checked against stored customer metrics, which are recalculated automatically. If segment counts look stale, metrics can be recalculated from the Customer Metrics section of the admin
