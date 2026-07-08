---
title: Affiliate Analytics & Reports
---

Affiliate analytics help you track the performance of your affiliate program and identify your top-performing partners. This guide shows you how to use the merchant dashboard, interpret statistics, analyze revenue trends, and make data-driven decisions to optimize your affiliate program.

## Merchant Dashboard

Navigate to **Affiliate Program > Dashboard** to access the comprehensive affiliate analytics overview.

The merchant dashboard provides a real-time snapshot of your entire affiliate program's performance, including active programs, affiliate counts, commission activity, and revenue trends. This is your central hub for monitoring program health and making strategic decisions.

![Merchant Dashboard](/static/core/admin/img/help/affiliate-analytics/merchant-dashboard.webp)

## Dashboard Statistics

The dashboard displays key performance indicators in card format at the top of the page.

### Overview Statistics

| Statistic | Description | Example Value |
|-----------|-------------|---------------|
| **Total Programs** | Total programs created (active count shown in parentheses) | 3 programs (2 active) |
| **Active Affiliates** | Approved affiliates currently promoting your products | 47 affiliates |
| **Pending Applications** | New affiliate applications awaiting your review | 8 pending |
| **Total Clicks** | Lifetime clicks across all affiliate tracking links | 12,543 clicks |
| **Total Commissions** | Number of commission records ever created | 287 commissions |
| **Pending Amount** | Total value of approved commissions awaiting payout | $4,235.50 |

These statistics give you an at-a-glance view of program scale and financial obligations.

### Understanding the Metrics

- **Active count** — Shows how many programs are currently accepting applications and generating commissions
- **Pending applications** — Indicates your review workload (high numbers suggest you should review applications more frequently)
- **Total clicks** — Measures overall affiliate engagement and promotional activity
- **Pending amount** — Represents your current payout liability to affiliates

## Revenue Chart

The dashboard includes a 30-day revenue chart powered by Chart.js showing commission trends over time.

### Chart Features

- **Time Period** — Displays the last 30 days of commission activity
- **Daily Breakdown** — Each bar represents commissions created on that day
- **Hover Details** — Hover over any bar to see the exact date and commission total
- **Trend Analysis** — Quickly spot growth patterns, seasonal trends, and anomalies

### Reading the Chart

**Example Analysis:*

```
Day 1-7:   $150-$200/day  → Baseline performance
Day 8-14:  $300-$450/day  → Campaign spike (investigate what worked)
Day 15-21: $100-$150/day  → Post-campaign dip (expected)
Day 22-30: $200-$250/day  → Returning to baseline
```

Use this chart to:

- **Identify successful campaigns** — Spikes indicate effective promotions
- **Spot seasonal patterns** — Plan inventory and affiliate outreach around high-traffic periods
- **Detect problems** — Sudden drops may indicate broken tracking links or program issues
- **Validate changes** — Compare revenue before and after commission rate adjustments

## Top Performing Affiliates

The dashboard includes a table showing your top 10 highest-earning affiliates.

### Affiliate Performance Metrics

| Column | Description | Example |
|--------|-------------|---------|
| **Affiliate** | Affiliate's name and unique code | Sarah Johnson (AFF-12345) |
| **Total Revenue** | All-time sales attributed to this affiliate | $18,450.00 |
| **Orders** | Number of successful orders referred | 87 orders |
| **Commission Count** | Number of commission records created | 87 commissions |
| **Total Payouts** | Amount paid to this affiliate to date | $2,767.50 |

The table is **sorted by total revenue** (highest to lowest) to help you quickly identify your most valuable partners.

### Using Top Affiliate Data

**Identify VIP Partners:*

Review the top performers and consider:

- **Exclusive rates** — Offer your top 3 affiliates higher commission rates (e.g., increase from 10% to 12%)
- **Early access** — Give top affiliates early notification of new products or sales
- **Custom creatives** — Provide personalized banners or product images
- **Direct support** — Assign a dedicated contact for your best partners

**Example:*

```
Affiliate: Emily Chen (AFF-00123)
Revenue:   $24,500
Orders:    142
Payouts:   $2,450 (10% commission)

Action: Offer 12% commission tier + early product access
Expected impact: 20-30% revenue increase from this affiliate
```

## Recent Activity

The dashboard shows recent affiliate activity to help you stay on top of pending actions.

### Recent Applications

Displays the 5 most recent pending affiliate applications with:

- Affiliate's name
- Applied date
- Program applied to
- Quick **Review** link to approve or reject

This section helps you prioritize new affiliate reviews and avoid application backlogs.

### Recent Commissions

Shows the 10 most recently created commissions (pending status) with:

- Order number (clickable to view order details)
- Affiliate name
- Commission amount
- Created date
- Quick **Approve** or **Reject** actions

Review this section daily to keep commissions moving through the approval pipeline.

## Program-Level Statistics

Navigate to an individual program's detail page to see program-specific analytics.

### Accessing Program Statistics

1. Navigate to **Affiliate Program > Programs**
2. Click the program name you want to analyze
3. View the statistics panel on the program detail page

### Program-Specific Metrics

| Metric | Description | What It Means |
|--------|-------------|---------------|
| **Active Affiliates** | Approved affiliates in this program | 23 affiliates |
| **Total Clicks** | Clicks on tracking links for this program | 5,432 clicks |
| **Total Commissions** | Commission records created for this program | 127 commissions |
| **Pending Commissions** | Unpaid commission value for this program | $1,245.00 |

### Recent Program Affiliates

The program detail page shows the 10 newest affiliates who joined this program, including:

- Affiliate name and code
- Join date
- Application status

Use this to monitor program growth and identify which programs attract the most interest.

## Affiliate Performance by Program

View detailed per-affiliate statistics within a specific program.

### Viewing Affiliates by Program

1. Navigate to **Affiliate Program > Programs**
2. Click the program name
3. Scroll to the **Affiliates** section
4. Click **View All Affiliates** to see the complete list

The affiliate list is **sorted by total commissions** to highlight top performers within each program.

### Comparison Analysis

**Example: Comparing two programs**

**Influencer Program (10% commission):*
- 47 active affiliates
- 8,234 clicks
- 187 commissions
- Average commission value: $32.50

**Bulk Referral Program (fixed $25 commission):*
- 23 active affiliates
- 3,421 clicks
- 94 commissions
- Average commission value: $25.00

**Insight:** Influencer program has higher engagement and commission values, suggesting percentage-based commissions work better for this store.

## Commission Reports

The commission admin provides advanced filtering and export capabilities for detailed reporting.

### Accessing Commission Reports

Navigate to **Marketing > Commissions** to view the full commission list with filters.

### Advanced Filtering

Use the filter sidebar to create custom reports:

- **By Date Range** — Select commissions created between specific dates (e.g., January 1-31 for monthly reporting)
- **By Affiliate** — View all commissions for a single affiliate
- **By Program** — See commissions from a specific program
- **By Status** — Filter to show only pending, approved, rejected, or paid commissions

### Export Capabilities

Spwig's admin interface includes built-in export functionality:

1. Apply filters to narrow down the commission list
2. Select the commissions you want to export (or use "Select all")
3. Choose **Export Selected** from the **Actions** dropdown
4. Select format (CSV, Excel)
5. Download the report for offline analysis

**Common Reports:*

- **Monthly commission summary** — Filter by date range, export all approved commissions
- **Affiliate performance** — Filter by affiliate, export all commissions to calculate ROI
- **Program comparison** — Export commissions for each program separately, compare in spreadsheet

## Payout Reports

The payout admin provides financial tracking and reconciliation tools.

### Accessing Payout Reports

Navigate to **Affiliate Program > Payouts** to view payout history and statistics.

### Payout Statistics

The payout dashboard shows:

| Status | Description |
|--------|-------------|
| **Pending** | Payouts created but not yet processed |
| **Processing** | Payouts submitted to payment provider (PayPal/Airwallex) |
| **Completed** | Successfully paid to affiliates |
| **Failed** | Payment processing errors |

### Provider Account Breakdown

View payouts organized by payment provider:

- **PayPal** — Payouts processed via PayPal (displays total count and amount)
- **Airwallex** — Payouts processed via bank transfer (displays total count and amount)

This breakdown helps you:

- Monitor provider costs (compare PayPal fees vs Airwallex fees)
- Balance payout methods (encourage affiliates to use lower-cost options)
- Identify processing issues (high failure rates on one provider)

### Historical Payout Data

Filter and export payout history for:

- **Quarterly reports** — Calculate affiliate program costs per quarter
- **Tax documentation** — Export annual payout data for 1099 forms (US) or equivalent
- **Affiliate inquiries** — Quickly look up payment dates and amounts when affiliates have questions

## Using Analytics for Optimization

Leverage your analytics data to continuously improve program performance.

### Identify Top Performers

**Action:** Review the top affiliates table monthly and:

- **Reward excellence** — Increase commission rates for top 10% of affiliates
- **Understand tactics** — Reach out to ask what promotional methods work best
- **Replicate success** — Share top affiliate strategies with other partners (with permission)

**Example:*

```
Top Affiliate: Marcus Lee (AFF-00456)
Revenue:       $31,200 in 3 months
Method:        YouTube product reviews

Action:
1. Increase commission from 10% to 12%
2. Ask Marcus to create an affiliate case study
3. Recruit more YouTube influencers using Marcus's success story
```

### Support Low Performers

**Action:** Filter affiliates by commission count and identify those with < 5 commissions in 90 days:

- **Provide resources** — Send promotional materials, product photos, sample copy
- **Offer training** — Create a webinar showing effective promotion tactics
- **Adjust placement** — If an affiliate's audience doesn't match a program, suggest switching to a different program
- **Remove inactive** — After 6-12 months with no activity, consider removing them from the program

### Program Comparison

**Action:** Compare total commissions and click-to-conversion rates across programs:

| Program | Clicks | Commissions | Conversion Rate | Avg Commission |
|---------|--------|-------------|-----------------|----------------|
| Program A | 8,234 | 187 | 2.27% | $32.50 |
| Program B | 3,421 | 94 | 2.75% | $25.00 |

**Insights:*

- Program B has a **higher conversion rate** despite fewer clicks (better targeting)
- Program A generates **higher commission values** (better for revenue)

**Optimizations:*

- Increase commission rate for Program B to attract more affiliates (conversion is proven)
- Analyze what makes Program B convert better and apply learnings to Program A

### Seasonal Trends

**Action:** Use the revenue chart to identify seasonal patterns:

```
January:  $5,200   → Post-holiday slump
February: $4,800   → Continued low season
March:    $6,100   → Spring pickup
April:    $7,300   → Growth continues
May:      $6,800   → Stabilizing
```

**Plan campaigns:*

- **Q1 slowdown** — Launch "Spring Sale" campaign in February to boost March/April revenue
- **Holiday prep** — Recruit new affiliates in September/October for Q4 holiday sales
- **Inventory planning** — Stock up before affiliate-driven revenue spikes

## Tips

- Review the **merchant dashboard daily** to catch pending applications and commissions before they pile up — a 5-minute daily check is more efficient than a 2-hour weekly catch-up
- Use the **revenue chart to validate program changes** — if you adjust commission rates, compare the 30 days before and after to measure impact
- Export commission data **monthly** and store reports in your accounting system for easy tax preparation and financial forecasting
- Reach out to your **top 3 affiliates quarterly** to maintain relationships and gather feedback on program improvements
- Watch for **spikes in the revenue chart** and investigate what caused them — successful campaigns can be replicated with other affiliates or in future seasons
- Set up a **monthly review routine**: 1st week = review analytics, 2nd week = contact top performers, 3rd week = support low performers, 4th week = plan next month's campaigns
- Compare **click counts vs commission counts** for each affiliate to identify conversion quality — an affiliate with 5,000 clicks but only 10 commissions may be driving low-quality traffic