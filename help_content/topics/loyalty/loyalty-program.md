---
slug: loyalty-program
title_i18n_key: Loyalty Program
category: promotions
component: loyalty
keywords:
  - loyalty
  - rewards
  - points
  - tiers
  - membership
  - loyalty points
  - rewards program
  - customer retention
  - badges
  - campaigns
url_patterns:
  - /admin/loyalty/dashboard/
  - /admin/loyalty/loyaltymember/
  - /admin/loyalty/loyaltytier/
  - /admin/loyalty/loyaltyreward/
  - /admin/loyalty/loyaltyrule/
related:
  - voucher-codes
  - sales-promotions
  - customer-management
published: true
---

The Loyalty Program lets you reward customers for purchases and engagement with a points-based system. Customers earn points, advance through tiers, and redeem rewards. Navigate to **Marketing > Loyalty Program** in the admin sidebar.

![Loyalty dashboard](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Loyalty Dashboard

The dashboard provides a comprehensive overview of your loyalty program:

### Key Metrics

- **Total Members** — Total enrolled customers
- **Active Members (30d)** — Members who earned or redeemed points in the last 30 days
- **Points Outstanding** — Total unredeemed points across all members
- **Redemption Rate** — Percentage of earned points that have been redeemed
- **Points Earned (30d)** — Points earned in the last 30 days
- **Points Redeemed (30d)** — Points redeemed in the last 30 days
- **Avg Points/Member** — Average points balance per member
- **Active Rules** — Number of earning rules currently active

### Quick Actions

The dashboard has shortcut cards to manage all aspects of the program:
- **Members** — View and manage loyalty members
- **Tiers** — Configure membership tiers
- **Rewards** — Set up the rewards catalog
- **Redemptions** — View redemption history
- **Rules** — Configure how points are earned
- **Badges** — Manage achievement badges
- **Campaigns** — Run special loyalty campaigns
- **Segments** — Create member segments for targeting

### Charts and Analytics

- **Member Enrollment Trend** — New member signups over time
- **Points Earned vs Redeemed** — Track point flow balance
- **Tier Distribution** — See how members are distributed across tiers

## Setting Up the Program

### Step 1: Create Tiers

Tiers define membership levels with increasing benefits:

1. Navigate to **Loyalty > Tiers**
2. Create tiers like Bronze, Silver, Gold, Platinum
3. For each tier, set:
   - **Name** — Tier display name
   - **Rank** — Sort order (lower rank = lower tier, e.g., Bronze = 1, Silver = 2)
   - **Color** — Visual accent color displayed on member badges
   - **Min Points Earned** — Lifetime points earned to qualify for this tier
   - **Min Spend** — Total spend amount to qualify for this tier
   - **Min Orders** — Number of orders to qualify for this tier
   - **Points Multiplier** — Bonus earning rate for members in this tier (e.g., 2.0 = 2x points)

A member qualifies for a tier if **any** of the three thresholds is met. You can use just one threshold or combine all three.

### Step 2: Configure Earning Rules

Rules define how customers earn points:

1. Navigate to **Loyalty > Rules**
2. Create rules using one of the four rule types:

| Rule Type | Description | Example |
|-----------|-------------|---------|
| **Spend** | Points per amount spent | 1 point per $1 |
| **Item** | Points per item purchased | 50 points per product in a specific category |
| **Action** | Points for a specific action | 200 points for signing up |
| **Event** | Points for a calendar event | Birthday bonus points |

3. Configure additional rule settings:
   - **Scope / Scope Filters** — Limit the rule to specific products, categories, or customer tiers
   - **Min Order Amount** — Minimum cart value for the rule to apply
   - **Allowed Tiers** — Restrict the rule to specific membership tiers
   - **Is Exclusive** — When enabled, this rule cannot stack with other rules
   - **Points Pending Days** — Number of days before earned points become available (useful to account for return windows)
   - **Points Expire Days** — Number of days after earning before points expire (leave blank for no expiry)
   - **Start / End Date** — Restrict the rule to a date range

### Step 3: Set Up Rewards

Rewards are what customers can redeem their points for:

1. Navigate to **Loyalty > Rewards**
2. Create rewards like:
   - **$5 Off Coupon** — 500 points
   - **Free Shipping** — 300 points
   - **10% Discount** — 1000 points

### Step 4: Create Badges (Optional)

Badges recognize customer achievements:

1. Navigate to **Loyalty > Badges**
2. Create badges for milestones:
   - **First Purchase** — Awarded after first order
   - **Big Spender** — Awarded after spending $500+
   - **Loyal Customer** — Awarded after 10 orders

Badges can include bonus point awards when earned.

## Managing Members

### Member List

View all loyalty members with their:
- Current tier and status
- Points balance
- Enrollment date
- Recent activity

### Top Point Earners

The dashboard highlights your most active members with a leaderboard showing rank, name, tier, and points earned in the period.

### Recent Transactions

A transaction log shows all recent point activity. Transaction types include:

| Type | Meaning |
|------|---------|
| **Earn** | Points credited from a qualifying purchase or rule |
| **Redeem** | Points spent on a reward |
| **Bonus** | Extra points from a badge, campaign, or manual award |
| **Adjustment** | Manual point correction made by a staff member |
| **Revoke** | Points removed (e.g., after order cancellation) |
| **Expire** | Points that have passed their expiry date |

### Manual Point Adjustments

You can manually add or deduct points for any member:

1. Open the member's detail page
2. Click **Adjust Points**
3. Enter the point amount (positive to add, negative to deduct)
4. Enter a reason for the adjustment
5. Click **Save**

The adjustment is recorded as a transaction and is visible in the member's transaction history.

## Campaigns

Loyalty campaigns let you run special promotions:
- **Double points weekends** — Temporarily increase earning rates
- **Bonus point events** — Award extra points for specific actions
- **Tier upgrade promotions** — Lower the threshold for tier advancement

## Tips

- Start with simple earning rules (1 point per $1 spent) and expand over time.
- Set achievable reward thresholds to keep members engaged — if rewards feel unreachable, members lose interest.
- Use badges to gamify the experience and encourage specific behaviors.
- Monitor the Redemption Rate — a healthy program has a 10-30% redemption rate.
- Run campaigns during slow periods to boost engagement.
- Use the Points Earned vs Redeemed chart to ensure your program is sustainable.
