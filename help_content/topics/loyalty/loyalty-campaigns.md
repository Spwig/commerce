---
slug: loyalty-campaigns
title_i18n_key: Loyalty Campaigns
category: promotions
component: loyalty
keywords:
  - loyalty campaign
  - double points
  - points event
  - campaign automation
  - loyalty trigger
  - birthday bonus
  - win-back campaign
  - points expiry
  - loyalty segment
  - customer segment
  - campaign execution
  - loyalty automation
  - scheduled campaign
  - loyalty rewards
url_patterns:
  - /admin/loyalty/loyaltycampaign/
  - /admin/loyalty/loyaltysegment/
  - /admin/loyalty/loyaltycampaignexecution/
related:
  - loyalty-program
published: true
---

Loyalty campaigns let you run time-limited promotions and automated rewards that go beyond your everyday earning rules. Use them to run double-points weekends, reward customers on their birthday, win back inactive shoppers, and deliver targeted bonuses to specific groups of members.

Each campaign defines a trigger or schedule, the members it applies to, and the actions to take. Once active, campaigns fire automatically — you set them up once and Spwig handles the rest.

## Types of campaigns

| Type | When it fires |
|------|---------------|
| **Trigger-Based** | When a specific event occurs (e.g., a purchase is placed, a birthday is detected) |
| **Scheduled** | On a repeating schedule (daily, weekly, monthly) |
| **Manual** | Only when you explicitly run it from the admin |
| **Behavioral** | When a customer matches a behavioral pattern (e.g., browsing without buying) |

## Creating a campaign

Navigate to **Promotions > Loyalty Campaigns** and click **+ Add Loyalty Campaign**.

### Step 1: basic information

- **Name** — a clear, descriptive name visible only in the admin (e.g., `Birthday Bonus — 200 Points`)
- **Slug** — auto-generated from the name; used internally
- **Description** — optional notes about the campaign's purpose
- **Campaign Type** — select the type from the table above

### Step 2: trigger or schedule

**For trigger-based campaigns**, set the **Trigger Event** that fires the campaign. Available triggers include:

| Trigger | Description |
|---------|-------------|
| Order Placed | Fires when a member completes an order |
| First Purchase | Fires on a member's very first order |
| Customer Birthday | Fires on the member's birthday |
| Membership Anniversary | Fires each year on the member's join anniversary |
| Cart Abandoned | Fires when a cart is abandoned without checkout |
| Tier Promotion | Fires when a member moves up to a higher tier |
| Points Expiring Soon | Fires when a member has points about to expire |
| Inactive 90 Days | Fires when a member has not purchased in 90 days |
| Review Submitted | Fires when a member submits a product review |
| Referral Converted | Fires when a referred customer makes a purchase |

You can add **Trigger Conditions** as a JSON object to further filter when the campaign fires. For example, to only trigger for orders over $100:

```json
{
  "min_order_amount": 100
}
```

**For scheduled campaigns**, set the **Schedule Type** (Daily, Weekly, Monthly, or Custom Cron) and configure timing in the **Schedule Config** field:

```json
{
  "hour": 9,
  "minute": 0
}
```

### Step 3: actions

The **Actions** field defines what happens when the campaign triggers. Enter a JSON array of action objects. The most common action is awarding bonus points:

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Birthday bonus — thank you for being a member!"
  }
]
```

Other available actions include sending an email notification or awarding a badge. Refer to your provider component documentation for the full list.

### Step 4: targeting

Control which members the campaign applies to using the targeting fields:

- **Target All Members** — checked by default; the campaign applies to every active loyalty member
- **Target Segment** — restrict the campaign to members in a specific segment (see [Segments](#managing-member-segments) below)
- **Target Tiers** — restrict the campaign to members in specific loyalty tiers

### Step 5: limits and cooldowns

- **Max Triggers Per Member** — how many times the same member can benefit from this campaign. Set to `1` for one-time bonuses like a birthday reward. Leave blank for unlimited.
- **Cooldown Days** — minimum days between campaign triggers for the same member. For example, set to `365` to prevent a birthday campaign from firing more than once per year.

### Step 6: campaign dates

Set **Start Date** and **End Date** to make the campaign time-limited. Leave both blank for an ongoing campaign.

Campaigns can be in one of these statuses:

| Status | Description |
|--------|-------------|
| **Draft** | Created but not yet active; safe to configure and test |
| **Active** | Running and will fire when conditions are met |
| **Paused** | Temporarily stopped without losing configuration |
| **Ended** | Past its end date; no longer firing |
| **Archived** | Hidden from the active list but preserved for records |

After filling in all fields, click **Save**. Then change the status to **Active** to start the campaign.

## Practical examples

### Example: double points weekend

**Scenario:** Award 2x points on all purchases placed during a specific weekend.

| Field | Value |
|-------|-------|
| Name | `Double Points Weekend — March` |
| Campaign Type | Trigger-Based |
| Trigger Event | Order Placed |
| Actions | `[{"type": "award_points_multiplier", "multiplier": 2.0}]` |
| Start Date | Friday evening |
| End Date | Sunday midnight |
| Target All Members | Checked |

### Example: birthday bonus

**Scenario:** Give every loyalty member 200 bonus points on their birthday.

| Field | Value |
|-------|-------|
| Name | `Birthday Bonus` |
| Campaign Type | Trigger-Based |
| Trigger Event | Customer Birthday |
| Actions | `[{"type": "award_points", "points": 200, "description": "Happy birthday from us!"}]` |
| Max Triggers Per Member | 1 |
| Cooldown Days | 365 |
| Target All Members | Checked |

### Example: win-back campaign

**Scenario:** Send 100 bonus points to members who haven't purchased in 90 days.

| Field | Value |
|-------|-------|
| Name | `90-Day Win-Back Bonus` |
| Campaign Type | Trigger-Based |
| Trigger Event | Inactive 90 Days |
| Actions | `[{"type": "award_points", "points": 100, "description": "We miss you — here are some bonus points"}]` |
| Max Triggers Per Member | 1 |
| Cooldown Days | 180 |
| Target All Members | Checked |

## Managing member segments

Segments let you target campaigns at specific groups of loyalty members. Navigate to **Promotions > Loyalty Segments** to manage them.

### Segment types

| Type | Description |
|------|-------------|
| **Rule-Based** | Membership determined by rules (e.g., members with over 1,000 points) |
| **Dynamic Calculation** | Membership calculated on-demand from real-time criteria |
| **Manual Assignment** | Members are added to the segment manually |

### Creating a segment

1. Navigate to **Promotions > Loyalty Segments** and click **+ Add Loyalty Segment**
2. Fill in:
   - **Name** — descriptive name (e.g., `High-Value Customers`, `Silver Tier Members`)
   - **Slug** — auto-generated
   - **Criteria Type** — how membership is determined
   - **Criteria Config** — JSON object defining the membership rules
3. Click **Save**

#### Example: segment for members with 500+ points

```json
{
  "min_available_points": 500
}
```

#### Example: segment for Gold tier members only

```json
{
  "tier_slugs": ["gold"]
}
```

The **Member Count** column in the segment list shows how many members currently match. Click a segment and use the **Refresh Member Count** action to recalculate it if your data has changed.

## Tracking campaign performance

### Campaign execution history

Navigate to **Promotions > Campaign Executions** to see a record of every time a campaign has fired for any member. Each execution record shows which campaign ran, which member it ran for, and the outcome.

### Reviewing a campaign's reach

Open any campaign record to see the **Times Triggered** count and when the campaign last fired. This gives you a quick view of how many members have benefited from the campaign.

## Tips

- Create campaigns in **Draft** status first so you can review all settings before they go live
- Use **Max Triggers Per Member** on all one-time bonus campaigns (birthday, first purchase, sign-up) to prevent customers from earning the bonus more than once
- Combine a **Target Segment** with a trigger-based campaign to run tier-exclusive promotions — for example, double points on purchases only for Gold and Platinum members
- Set a **Cooldown Days** value on win-back campaigns so members are not bombarded if they make a small purchase and then go inactive again shortly after
- The campaign list is your best tool for keeping track of what promotions are currently active — review it before launching new offers to ensure campaigns don't stack unintentionally
- Archive ended campaigns rather than deleting them so you have a historical record of what promotions you ran and when
