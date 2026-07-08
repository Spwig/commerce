---
slug: creating-affiliate-programs
title_i18n_key: Creating Affiliate Programs
category: affiliates
component: affiliate
keywords:
  - affiliate program
  - create program
  - commission structure
  - percentage commission
  - fixed commission
  - cookie lifetime
  - payout threshold
  - program settings
  - affiliate commission
  - referral program
  - program rules
  - commission type
  - auto-approve affiliates
url_patterns:
  - /en/admin/affiliate/program/add/
  - /en/admin/affiliate/program/
related:
  - affiliate-program
published: true
---

Affiliate programs define how your partners earn commissions when they refer customers to your store. Each program has its own commission structure, tracking rules, and payout thresholds. You can create multiple programs to serve different affiliate segments — such as influencers, content creators, or bulk referral partners.

![Programs List](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Program Components

Every affiliate program consists of:

- **Name and Description** — Identify the program and explain it to affiliates
- **Commission Structure** — How much affiliates earn per sale (percentage or fixed amount)
- **Cookie Lifetime** — How long referral tracking lasts after a click (1-365 days)
- **Auto-Approve** — Whether new affiliates join automatically or require manual review
- **Minimum Payout Threshold** — How much affiliates must earn before requesting a payout
- **Status** — Active, paused, or archived

## Commission Types

Choose between two commission models when creating your program:

| Type | How It Works | When to Use | Example Calculation |
|------|-------------|-------------|---------------------|
| **Percentage** | Affiliate earns a percentage of the order subtotal | Scalable rewards that grow with order value | 10% of $150 order = $15 commission |
| **Fixed Amount** | Affiliate earns a flat amount per sale | Predictable costs; best for high-volume, low-margin products | $25 per sale regardless of order value |

**Percentage commissions** scale naturally — affiliates earn more when they refer high-value customers. This aligns their incentives with yours and is the most common model (typically 5–15%).

**Fixed commissions** work well for services, subscriptions, or bulk referral programs where you want predictable per-sale costs. They're easy to understand and budget for, but may undercompensate affiliates who bring in large orders.

## Creating a Program

Navigate to **Marketing > Affiliate Programs** and click **+ Add Program**.

### Step-by-Step Setup

1. **Program Name**
   Enter a descriptive name visible to affiliates (e.g., "Partner Program" or "Influencer Tier").

2. **Slug**
   A URL-friendly identifier auto-generated from the name. Used in URLs and internal references. You can customize it if needed.

3. **Description**
   Optional text explaining the program benefits and terms. Affiliates see this when reviewing programs they can join.

4. **Commission Type**
   Select **Percentage** or **Fixed Amount**.

5. **Commission Value**
   - For percentage: Enter a value between 0 and 100 (e.g., `10` for 10%)
   - For fixed amount: Enter the dollar amount per sale (e.g., `25.00` for $25)

6. **Cookie Lifetime Days**
   How many days the tracking cookie lasts (1–365). See the section below for guidance.

7. **Auto-Approve Affiliates**
   - **Checked** — New affiliates join automatically
   - **Unchecked** — You manually review and approve each application

8. **Minimum Payout**
   The minimum balance an affiliate must accumulate before requesting a payout (e.g., `50.00` for $50).

9. **Status**
   Set to **Active** to accept new affiliates and track referrals.

10. **Save** the program.

## Cookie Lifetime Explained

The cookie lifetime determines how long Spwig remembers that a customer clicked an affiliate's referral link.

### How It Works

1. A customer clicks an affiliate's link
2. Spwig sets a tracking cookie in the customer's browser
3. If the customer completes a purchase **within the cookie lifetime**, the order is attributed to the affiliate
4. If the cookie expires before purchase, the affiliate does not earn a commission

### Choosing a Duration

| Duration | Use Case | Typical Scenario |
|----------|----------|------------------|
| **1–7 days** | Impulse purchases, flash sales | Fast-moving consumer goods, limited-time offers |
| **30 days** | Standard e-commerce | General online retail, default recommendation |
| **60–90 days** | Considered purchases | Higher-ticket items, B2B, services |
| **180+ days** | Long sales cycles | Enterprise software, subscriptions, luxury goods |

**Industry standard is 30 days.** This balances fair attribution for affiliates with practical tracking limits. Shorter lifetimes favor customers who convert quickly; longer lifetimes give customers time to research and return to complete their purchase.

### Technical Note

Cookie lifetime only affects **attribution**. Approved commissions remain valid indefinitely — the cookie lifetime just determines whether an order is credited to the affiliate in the first place.

## Auto-Approve Settings

The auto-approve setting controls whether new affiliate applications require manual review.

### When to Enable Auto-Approve

- **Public programs** — You want to grow your affiliate base quickly without bottlenecks
- **Low-risk products** — Fraud or brand risk is minimal
- **High-volume programs** — You expect many applications and can't review each manually

### When to Require Manual Review

- **Invite-only programs** — You only accept pre-vetted partners
- **Premium programs** — High commission rates or exclusive benefits
- **Brand-sensitive products** — You need to ensure affiliates align with your brand values
- **Fraud prevention** — You want to screen for suspicious accounts

### Security Considerations

Manually reviewing affiliates helps prevent:
- Self-referral schemes (affiliates creating fake accounts to earn commissions)
- Trademark violations (affiliates bidding on your brand terms in paid search)
- Brand misalignment (affiliates promoting your products in inappropriate contexts)

For most stores, starting with **manual approval** is safer. You can always enable auto-approve later once you've established trust patterns.

## Minimum Payout Threshold

The minimum payout threshold prevents administrative overhead from processing many small payouts.

### Why Set a Minimum

- **Reduces transaction fees** — Payment processors charge per transaction, so batching payouts saves money
- **Simplifies accounting** — Fewer payout events mean less reconciliation work
- **Industry standard** — Most affiliate programs have minimums ($25–$100)

### Typical Thresholds

| Threshold | Use Case |
|-----------|----------|
| **$25–$50** | High-volume programs where affiliates hit the minimum quickly |
| **$50–$100** | Standard threshold for most programs |
| **$100–$200** | Premium programs or international payouts with high processing fees |

### Balancing Affiliate Satisfaction

Setting the threshold **too high** frustrates affiliates who may wait months to receive their first payout. Setting it **too low** creates administrative burden and eats into your margins with fees.

**Recommendation:** Start at $50. This is low enough that active affiliates reach it within their first few sales, but high enough to batch payouts efficiently.

### No Maximum

There is no maximum balance — affiliates can accumulate earnings indefinitely before requesting a payout. Some affiliates prefer to batch their requests quarterly or annually for tax planning.

## Program Status Management

Programs can be in one of three statuses:

| Status | Description | Behavior |
|--------|-------------|----------|
| **Active** | Program is running | Accepts new affiliates, tracks referrals, calculates commissions |
| **Paused** | Temporarily disabled | Existing affiliates remain but no new sign-ups; existing referral cookies still work |
| **Archived** | Permanently closed | No new affiliates, no new referrals tracked; historical data preserved for reporting |

### When to Pause a Program

- You're revising commission rates or terms
- You're over budget for affiliate payouts this quarter
- You're testing a new program structure and want to prevent new affiliates from joining the old one

Paused programs still honor existing tracking cookies and pending commissions — you're just preventing new affiliates from joining.

### When to Archive a Program

- You've replaced the program with a new structure
- The program was time-limited (e.g., seasonal campaign)
- You're consolidating multiple programs into one

Archived programs remain in the database for historical reporting but are removed from active management views.

## Example Programs

### Example 1: Influencer Program (Percentage)

| Field | Value |
|-------|-------|
| Name | Influencer Program |
| Commission Type | Percentage |
| Commission Value | 10 |
| Cookie Lifetime Days | 30 |
| Auto-Approve | Unchecked (manual review) |
| Minimum Payout | 50.00 |
| Status | Active |

**Use Case:** Recruit social media influencers and content creators. The 10% commission scales with order value, rewarding affiliates who attract high-spending customers. Manual approval ensures you vet each influencer's audience and brand alignment.

### Example 2: Bulk Referral Program (Fixed)

| Field | Value |
|-------|-------|
| Name | Referral Partner Program |
| Commission Type | Fixed Amount |
| Commission Value | 25.00 |
| Cookie Lifetime Days | 7 |
| Auto-Approve | Checked |
| Minimum Payout | 100.00 |
| Status | Active |

**Use Case:** Partner with deal sites, coupon aggregators, and referral networks that drive high volume. The $25 flat commission keeps costs predictable, and the short cookie lifetime (7 days) targets fast converters. Auto-approve enabled since these partners typically self-serve.

### Example 3: Premium Partner (High Percentage)

| Field | Value |
|-------|-------|
| Name | Premium Partner Tier |
| Commission Type | Percentage |
| Commission Value | 15 |
| Cookie Lifetime Days | 90 |
| Auto-Approve | Unchecked |
| Minimum Payout | 200.00 |
| Status | Active |

**Use Case:** Exclusive program for top-performing affiliates or strategic partners. Higher commission (15%) rewards their quality traffic, and the 90-day cookie lifetime accommodates longer consideration cycles. Manual approval only — this is an invite-only tier.

## Tips

- Start with a **percentage commission** (5–15%) for most programs — it's easier to explain to affiliates and scales naturally with order value.
- Use **30-day cookie lifetime** as a baseline — it's the industry standard and balances fair attribution with practical tracking limits.
- Enable **manual approval** initially to vet affiliates, then switch to auto-approve once you've established trust patterns and fraud controls.
- Set your **minimum payout** to $50–$100 to balance affiliate satisfaction (not too high to reach) with administrative efficiency (not too many small payouts).
- Create **separate programs** for different affiliate segments (influencers, content sites, deal aggregators) so you can track performance and adjust commissions independently.
- Monitor the **analytics dashboard** regularly to spot high-performing affiliates and adjust commission rates to retain top partners.
