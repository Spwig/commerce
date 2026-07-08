---
slug: abandoned-carts
title_i18n_key: Abandoned Carts
category: customers
component: customers
keywords:
  - abandoned cart
  - cart recovery
  - lost sales
  - cart abandonment
  - recovery email
  - cart value
  - checkout dropout
  - recover abandoned orders
  - abandonment reason
  - cart tracking
  - recovery workflow
related:
  - customer-segments
  - customer-analytics
  - customer-wallet
url_patterns:
  - /admin/customers/abandonedcart/
published: true
---

An abandoned cart is created when a logged-in customer adds items to their cart but does not complete checkout within 24 hours. Spwig automatically tracks these carts so you can understand lost revenue, identify patterns in why customers leave, and take action to recover sales.

Navigate to **Customers > Abandoned Carts** to view all recorded abandonments.

## What you can see in the abandoned carts list

The list view shows each abandoned cart with the following information at a glance:

| Column | Description |
|---|---|
| **Customer** | The customer's name and email |
| **Abandoned At** | Date and time the cart was flagged as abandoned |
| **Total Value** | The monetary value of items in the cart at time of abandonment |
| **Total Items** | Number of items in the cart |
| **Estimated Reason** | Spwig's best guess at why the cart was abandoned |
| **Recovery Status** | Whether this cart has been recovered (turned into a completed order) |
| **Days Since Abandonment** | How long ago the cart was abandoned |

### Filtering abandoned carts

Use the filters on the right-hand side to narrow the list:

- **Estimated Reason** — filter by the abandonment reason (e.g., show only carts where the estimated reason was high shipping cost)
- **Recovered** — filter to show only recovered or unrecovered carts
- **Abandoned At** — filter by date range to focus on recent abandonments or a specific campaign period

## Understanding abandonment reasons

Spwig records an estimated reason for each abandonment. These reasons are based on signals captured during the checkout process and are not guaranteed to be exact, but they provide a useful starting point for diagnosing drop-off patterns.

| Reason | What it may indicate |
|---|---|
| **Unknown** | No specific signal was captured — the most common reason |
| **High Shipping Cost** | The customer may have been deterred by the shipping cost shown at checkout |
| **Total Too High** | The overall order total may have been higher than expected |
| **Checkout Issues** | The customer encountered a problem during the checkout process |
| **Payment Failed** | A payment attempt was made but failed |
| **Comparison Shopping** | The customer likely visited to compare prices |
| **Saved for Later** | The customer intentionally saved items for a future visit |

If you see a large proportion of carts with the same reason — for example, a significant cluster of "High Shipping Cost" abandonments — that is a signal worth investigating in your shipping settings or checkout presentation.

## Viewing an individual abandoned cart

Click any row in the list to open the detail view. You will see:

- **Abandonment Details** — the customer, the cart reference, when it was abandoned, and the estimated reason
- **Cart Summary** — the number of items and total value at the time of abandonment
- **Recovery Tracking** — whether the cart was recovered, when it was recovered, and which order it converted into

The **Cart** field links directly to the underlying cart record, so you can see exactly which products were in the cart.

## Recovery workflow

Spwig tracks whether each abandoned cart eventually converts into a completed order. When a customer returns and completes a purchase from an abandoned cart, the record is automatically marked as **Recovered** and the resulting order is linked.

The **Recovery Emails Sent** counter shows how many automated recovery emails have been sent to the customer for this cart. This helps you understand whether your email campaigns are prompting customers to return.

### Manual recovery actions

The abandoned carts view is read-only — it is a record of what happened, not a tool for editing cart contents. To act on abandoned carts:

1. Note the customer's email address from the abandoned cart record
2. Use your email system or marketing tools to send a personalised message
3. Consider attaching a voucher code to give the customer an incentive to complete the purchase
4. Monitor the **Recovered** status over the following days to see if the outreach worked

## Analysing cart abandonment trends

Look at the abandoned carts list regularly as a health check on your checkout process:

- A sudden spike in abandonments may indicate a technical problem with checkout or payment
- Consistently high cart values in unrecovered carts represent your highest-opportunity recovery segment
- Compare the ratio of recovered to unrecovered carts over time to measure the effectiveness of your recovery emails

The **Customer Analytics** section of each customer profile also shows their personal cart abandonment rate, so you can identify customers who frequently add to cart but rarely complete a purchase.

## Tips

- Sort by **Total Value** (descending) to identify the highest-value carts worth prioritising for personal outreach
- Use the **Abandoned At** date filter to review abandonments from a specific campaign or promotional period — a spike during a flash sale may mean your promotion attracted browsers rather than buyers
- Pair the abandoned cart data with voucher campaigns: send a time-limited discount code to customers with high-value unrecovered carts to create urgency
- A cart that has been abandoned for more than 7 days is unlikely to recover on its own — if recovery emails are enabled, these are the carts that need the most attention
- Guest customers do not appear in abandoned carts — this tracking applies only to customers with registered accounts
