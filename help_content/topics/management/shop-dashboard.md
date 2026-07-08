---
slug: shop-dashboard
title_i18n_key: Shop Dashboard
category: getting-started
component: management
keywords:
  - shop dashboard
  - sales analytics
  - store analytics
  - revenue report
  - top products
  - visitor analytics
  - traffic sources
  - conversion funnel
  - abandoned carts
  - customer segmentation
  - voucher performance
  - sales over time
  - business metrics
  - key metrics
url_patterns:
  - /admin/management/systemmetrics/shop-dashboard/
  - /admin/management/systemmetrics/dashboard/
related:
  - database-backups
  - maintenance-mode
published: true
---

The Shop Dashboard gives you a complete view of your store's performance — revenue, orders, top products, visitor traffic, and more — all in one place. Use it to understand what is selling, where your customers come from, and how your store is trending over time.

Navigate to **Management > System Metrics** and click **Shop Dashboard** from the toolbar.

![Shop Dashboard overview](/static/core/admin/img/help/shop-dashboard/overview.webp)

## Choosing a time period

The dashboard filters all metrics by the selected period. Use the period selector at the top of the page to choose:

| Period | What it shows |
|--------|---------------|
| Today | Current day vs yesterday |
| This week | Monday to today vs last week |
| This month | Current month vs last month |
| This year | Year to date vs same period last year |
| Last 30 days | Rolling 30-day window |
| Last 90 days | Rolling 90-day window |
| Custom | Enter a specific start and end date |

Most views show a **comparison** to the equivalent period in the past, so you can see whether performance is improving or declining. Toggle the **Compare** switch off if you only want to see current figures.

## Action cards

At the top of the dashboard, action cards highlight items that need your attention right now:

- **Incomplete orders** — orders awaiting fulfilment
- **Abandoned carts** — sessions where a customer added items but did not complete checkout
- **Unread messages** — customer enquiries waiting for a reply
- **Low stock alerts** — products running low on inventory

Click any action card to navigate directly to the relevant admin section.

## Sales performance

The sales performance section shows your key revenue figures for the selected period:

- **Total revenue** — gross sales before deductions
- **Total orders** — number of completed orders
- **Average order value** — revenue divided by number of orders
- **Net profit** — revenue minus cost of goods and expenses (if configured)

Each figure shows an arrow and percentage indicating the change from the comparison period.

## Sales over time chart

The main chart plots your sales or orders over the selected period. Spwig automatically chooses the most useful grouping:

- Short periods (up to a week) group by day
- Medium periods (up to three months) group by week
- Long periods group by month

You can override the grouping using the **Group by** control above the chart. Hover over any point to see the exact value for that date.

## Top products

The top products table lists the best-selling products in the selected period, ranked by revenue. Each row shows:

- **Product name**
- **Units sold**
- **Revenue generated**

Use this to identify your strongest performers and decide where to focus promotions or stock replenishment.

## Visitor analytics

The visitor analytics section shows how many people visited your store and how they behaved:

- **Total visitors** — unique visitors to your storefront
- **Page views** — total pages viewed
- **Bounce rate** — percentage of visitors who viewed only one page
- **Views over time** — a chart showing traffic volume over the selected period

The **Geography** panel shows where your visitors are coming from, broken down by country and (where available) city.

## Traffic sources

The traffic sources panel shows how visitors found your store:

| Source | Description |
|--------|-------------|
| Direct | Visitors who typed your URL or used a bookmark |
| Organic search | Visitors from search engines |
| Social | Visitors from social media platforms |
| Referral | Visitors from other websites linking to you |
| Email | Visitors who clicked links in emails |

Use this information to understand which marketing channels drive the most traffic and where to invest.

## Conversion funnel

The conversion funnel shows how visitors move from browsing to completing a purchase:

1. **Visitors** — total unique visitors
2. **Product views** — visitors who viewed at least one product
3. **Add to cart** — visitors who added an item to their cart
4. **Checkout started** — visitors who began the checkout process
5. **Orders completed** — visitors who placed an order

The percentage at each step shows the drop-off rate. A large drop between "add to cart" and "checkout started" suggests friction in your checkout flow.

## Voucher performance

If you run voucher promotions, this section shows how they performed during the selected period:

- **Total redemptions** — how many times vouchers were used
- **Total discount given** — the sum of all voucher discounts applied
- **Revenue with vouchers** — total revenue from orders that included a voucher

## Customer segmentation

The customer segmentation panel breaks your customer base into groups:

- **New customers** — first-time buyers in the selected period
- **Returning customers** — customers who have purchased before
- **Guest checkouts** — orders placed without creating an account

Understanding the ratio of new to returning customers helps you decide whether to invest more in acquisition (marketing) or retention (loyalty programmes).

## Affiliate and loyalty summaries

If your store has an affiliate programme or loyalty scheme active, summarised performance metrics appear here — total commissions earned, total points issued, and top-performing affiliates or redeemers.

## Tips

- Check the dashboard every Monday morning for a quick weekly review — the "This week" period gives a clear snapshot of recent performance
- Use the **Custom** date range to measure the impact of a specific campaign: set the start and end dates to the campaign period
- If the conversion funnel shows a large drop at **Checkout started**, consider simplifying your checkout flow or adding trust badges
- High abandoned cart numbers alongside low conversion can indicate a pricing or shipping cost issue — review your checkout costs
- Compare periods year-over-year using the **This year** period to understand seasonal patterns in your business
- Export or screenshot the top products table before major restocking decisions to make sure you are ordering the right quantities
