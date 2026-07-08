---
slug: customer-analytics
title_i18n_key: Understanding Customer Analytics
category: customers
component: customers
keywords:
  - customer analytics
  - RFM score
  - customer lifetime value
  - CLV
  - LTV
  - customer segments
  - Champions
  - At Risk
  - purchase frequency
  - customer metrics
  - repeat customers
  - retention
  - churn
  - cohort analysis
url_patterns:
  - /admin/customers/customermetrics/
  - /admin/accounts/customerprofile/
related:
  - managing-customer-accounts
  - accounts-vs-customers
published: true
---

Customer analytics gives you a clear picture of who your best customers are, who is at risk of churning, and how much each customer is worth to your business over time. Spwig automatically calculates these metrics from order data so you always have an up-to-date view of customer health.

## Where to Find Analytics

Customer analytics data appears in two places:

- **Customers > All Customers** — The list view shows each customer's value, segment, and order counts at a glance. Open any customer to see a full analytics summary.
- **Customers > Customer Metrics** — A dedicated table of all calculated metrics including LTV, purchase frequency, cart abandonment rate, and probabilistic forecasts.

## Customer Segments

Spwig automatically groups customers into segments based on their purchasing behavior. Segments update automatically as customer activity changes.

| Segment | Description |
|---------|-------------|
| **Champions** | Recent, frequent buyers with high spend — your most valuable customers |
| **Loyal Customers** | Regular buyers with consistent purchase history |
| **At Risk** | Previously active customers who have not purchased recently (typically 90+ days) |
| **Hibernating** | Low engagement and a long gap since their last purchase |
| **Lost** | Have not purchased in a very long time with very low engagement |

Use segments to target your marketing — send win-back campaigns to At Risk customers, reward Champions with early access or VIP perks, and nurture new customers with welcome sequences.

## RFM Analysis

RFM (Recency, Frequency, Monetary) scoring is the method Spwig uses to rank and segment customers. Each customer gets three scores:

### Recency Score

How recently did the customer last purchase?

- Scale: 1 (purchased a long time ago) to 5 (purchased very recently)
- A score of 5 means the customer is actively buying

### Frequency Score

How often does the customer purchase?

- Scale: 1 (rarely) to 5 (very frequently)
- Repeat buyers score higher than one-time customers

### Monetary Score

How much has the customer spent in total?

- Scale: 1 (low total spend) to 5 (high total spend)
- Based on total completed order value

**Reading RFM Scores**

| Score | What It Means |
|-------|--------------|
| 5-5-5 | Champion — best possible customer |
| 1-5-5 | High spender but hasn't purchased recently — at risk |
| 5-1-1 | Recent purchaser, very early in the relationship |
| 1-1-1 | Lost customer — disengaged with low spend history |

## Customer Lifetime Value (LTV)

Lifetime Value represents the total revenue a customer has generated or is predicted to generate over their relationship with your store. Spwig supports three LTV calculation methods:

| Method | Description |
|--------|-------------|
| **Simple (RFM)** | Calculated from historical order data — total spent, frequency, and recency |
| **Cohort-based** | Groups customers by their first purchase month to identify patterns over time |
| **Probabilistic** | Uses BG/NBD modeling to predict future purchases and likely customer lifespan |

Each LTV calculation shows a **confidence score** (0–100%). Customers with more order history have higher confidence scores. A score above 80% is considered high confidence.

### Cohort Analysis

Customers are assigned a **cohort month** based on when they placed their first order. Cohort analysis lets you compare how different groups of customers behave over time — for example, customers acquired in December may have different retention rates than those acquired in July.

## Key Metrics Explained

| Metric | Description |
|--------|-------------|
| **Total Spent** | Sum of all completed order values |
| **Lifetime Value** | Calculated or predicted total customer value |
| **Average Order Value** | Total spent divided by completed orders |
| **Purchase Frequency** | Average days between purchases |
| **Days Since Last Purchase** | Recency indicator — high numbers signal at-risk customers |
| **Cart Abandonment Rate** | Percentage of carts started but not completed |
| **Probability Alive** | Probabilistic estimate that the customer is still actively buying (0.0 to 1.0) |
| **Predicted Purchases (12m/24m)** | Expected future purchases over the next 12 or 24 months |

## Refreshing Metrics

Analytics are calculated automatically, but you can manually trigger a recalculation for specific customers:

1. Navigate to **Customers > All Customers**
2. Select the customers you want to recalculate
3. Choose **Refresh customer metrics** from the **Action** dropdown
4. Click **Go**

This is useful after importing customers or making significant changes to order data.

## Using Analytics for Marketing

### Targeting Champions

Your Champions segment deserves priority treatment:
- Give them early access to new products or sales
- Request reviews and testimonials
- Enroll them automatically in your highest loyalty tier
- Send exclusive offers and rewards

### Re-engaging At Risk Customers

Customers who haven't purchased in 90+ days need attention:
- Send a personalized win-back email with a special discount
- Remind them of products they browsed or added to their wishlist
- Ask for feedback — sometimes customers churn for fixable reasons

### New Customer Nurturing

Customers with only one order need encouragement to return:
- Send a follow-up email 7–14 days after their first order
- Offer a second-purchase discount
- Recommend products based on their first purchase

## Tips

- Check the **At Risk** segment weekly — the sooner you reach out to lapsing customers, the higher your win-back rate.
- A high cart abandonment rate signals a checkout problem worth investigating — review your checkout flow.
- Use the **Cohort-based** LTV method if you have been running your store for 12+ months and want more accurate long-term projections.
- Export customer data for Champions and use it to create lookalike audiences in your advertising platforms.
- The **Probability Alive** field is most useful for deciding whether to invest in win-back campaigns — if it is below 0.1, the customer is unlikely to return regardless of incentives.
- Segment by **Account Type: Registered** before doing any analytics review — guest accounts inflate your customer count without the behavioral history needed for accurate analysis.
