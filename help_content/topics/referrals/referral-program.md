---
slug: referral-program
title_i18n_key: Referral Program
category: promotions
component: referrals
keywords:
  - referral program
  - refer a friend
  - referral link
  - referral reward
  - store credit referral
  - discount referral
  - referral attribution
  - fraud prevention referral
  - referral tracking
  - double-sided reward
  - new customer referral
  - referral coupon
  - eligibility rules
  - referral caps
url_patterns:
  - /admin/referrals/referralprogram/
  - /admin/referrals/referralattribution/
  - /admin/referrals/referralreward/
related:
  - loyalty-program
published: true
---

The referral program lets your existing customers share a unique referral link with their friends and family. When a referred friend makes their first qualifying purchase, both the referrer and the new customer can receive a reward — driving new customer acquisition through word of mouth.

## How the referral program works

1. A customer shares their unique referral link (or code) with a friend.
2. The friend clicks the link and is tracked via a cookie for up to 30 days (configurable).
3. The friend signs up and places their first qualifying order.
4. The system creates a referral attribution record and runs fraud and eligibility checks.
5. If the attribution is approved, rewards are issued to both parties.

Your store has a single referral program configuration. Navigate to **Marketing > Referral Program** to set it up.

## Setting up your referral program

### Program status

The program has three states:

- **Draft** — The program is being configured but not yet live. Referral links are inactive.
- **Active** — The program is live. Customers can share links and earn rewards.
- **Paused** — The program is temporarily stopped. Existing attributions still process, but no new referrals are tracked.

Set the **Status** to **Active** when you are ready to launch. You can pause it at any time.

### Reward configuration

Define the rewards that are issued when a referral converts. The program supports **double-sided rewards** — meaning you can reward both the referrer (the customer who shared the link) and the referee (the new customer who used it).

Configure rewards for each recipient in the **Reward Configuration** field. The reward kinds available are:

| Reward Kind | Description |
|-------------|-------------|
| **Store Credit** | Adds credit to the customer's wallet, usable on future orders |
| **Coupon Code** | Generates a unique discount voucher code |
| **Percentage Discount** | Issues a percentage discount for use at checkout |
| **Exclusive Perk** | A custom perk (e.g., free gift, priority access) — described in the reward's description field |

**Example configuration** — $10 store credit for the referrer and $10 discount for the new customer:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Set `"double_sided": false` if you only want to reward the referrer.

### Eligibility rules

Eligibility rules determine which referrals qualify for rewards. Configure these in the **Eligibility Rules** field:

| Rule | What it does |
|------|--------------|
| `new_customer_only` | If `true`, the referred friend must be a brand new customer (no prior orders) |
| `min_order_value` | The minimum order amount (in your store currency) the referred friend must spend |
| `exclude_discounts` | If `true`, orders where the referred customer used a voucher do not qualify |
| `exclude_staff` | If `true`, staff accounts cannot be referrers or referees |

**Example** — new customers only, minimum $40 order, staff excluded:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Timing configuration

The **Timing Configuration** field controls when rewards are issued after a qualifying order:

| Setting | What it does |
|---------|--------------|
| `issue_on` | When to issue the reward: `signup` (immediately on registration), `first_purchase` (immediately after order), or `post_refund` (after the refund window expires) |
| `refund_window_days` | How many days to wait before issuing rewards when using `post_refund` (default: 14 days) |

Using `post_refund` is the most cautious approach — it waits until the return window has passed before issuing rewards, reducing the risk of rewarding orders that are later refunded.

### Caps and limits

Prevent a single referrer from earning unlimited rewards by setting caps in the **Caps & Limits** field:

| Setting | What it does |
|---------|--------------|
| `monthly_per_referrer` | Maximum number of successful referrals rewarded per month, per referrer |
| `lifetime_per_referrer` | Maximum total successful referrals rewarded ever, per referrer |
| `max_reward_per_order` | Maximum reward value (in your store currency) issued for a single referral conversion |

**Example** — 20 referrals per month, 200 lifetime, $50 maximum reward per conversion:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Tracking configuration

Configure how referral links are tracked in the **Tracking Configuration** field:

| Setting | What it does |
|---------|--------------|
| `cookie_ttl_days` | How many days the referral tracking cookie stays active after a friend clicks the link (default: 30) |
| `attribution` | Attribution method — currently `last_touch` (the most recent referral link click is credited) |

### Fraud policy

The fraud detection system automatically scores each referral attribution for risk before approving it. Configure the policy in the **Fraud Policy** field:

| Setting | What it does |
|---------|--------------|
| `policy` | Overall strictness: `strict`, `balanced`, or `lenient` |
| `auto_reject_threshold` | Risk score (0–100) above which attributions are automatically rejected (default: 80) |
| `auto_approve_threshold` | Risk score below which attributions are automatically approved (default: 30) |
| `check_ip` | If `true`, checks whether the referrer and referee share the same IP address |
| `check_device` | If `true`, checks for shared device fingerprints between referrer and referee |
| `check_velocity` | If `true`, monitors for unusually high referral rates from a single source |
| `velocity_window_hours` | The time window (in hours) for velocity checking |
| `max_referrals_per_window` | Maximum referrals allowed from one source within the velocity window |

Attributions with a risk score between the auto-reject and auto-approve thresholds land in a **Pending** status and require manual review.

### Terms and conditions

Enter any legal terms and conditions for the program in the **Terms & Conditions** field. This text is shown to customers when they view the referral program. Markdown formatting is supported.

## Viewing referral attributions

Navigate to **Marketing > Referral Attributions** to see all referral cases — the link between a referrer and a referred customer.

![Referral attributions list](/static/core/admin/img/help/referral-program/attribution-list.webp)

Each attribution shows the referrer, the referred customer, the first order they placed, the current status, and the risk score.

### Attribution statuses

| Status | What it means |
|--------|---------------|
| **Pending** | Awaiting review — the risk score is in the manual review range |
| **Approved** | Referral is valid — rewards have been or will be issued |
| **Rejected** | Referral did not qualify or was flagged as fraudulent |
| **Expired** | The referral was not converted within the tracking window |

### Manually approving or rejecting attributions

For attributions in **Pending** status, you can manually approve or reject them by opening the attribution record and using the action buttons. When rejecting, choose a **Rejection Reason**:

- Self Referral
- Not New Customer
- Below Minimum Order Value
- Disposable Email
- Cap Exceeded
- Fraud Risk
- Order Refunded or Cancelled
- Manual Rejection

You can also add **Rejection Notes** for your own records.

### Filtering by risk level

Use the **Risk Level** filter in the sidebar to focus on high-risk attributions that need review:

- Low Risk (score 0–30) — Auto-approved
- Medium Risk (score 31–70) — Manual review
- High Risk (score 71–89) — Manual review, treat with caution
- Very High Risk (score 90+) — Auto-rejected

## Viewing issued rewards

Navigate to **Marketing > Issued Rewards** to see all rewards that have been issued as a result of approved attributions.

Each reward entry shows the customer, whether they are the referrer or referee, the reward kind and amount, and the current redemption status.

### Reward statuses

| Status | What it means |
|--------|---------------|
| **Pending** | The reward has been created but not yet delivered to the customer |
| **Issued** | The reward is active and available for the customer to use |
| **Redeemed** | The customer has used the reward |
| **Expired** | The reward passed its expiry date without being used |
| **Revoked** | The reward was manually cancelled (e.g., if the original order was refunded after the reward was issued) |

### Revoking a reward

If a reward needs to be cancelled — for example, the qualifying order was returned — open the reward record and use the **Revoke** action. Add a note explaining why it was revoked for your records.

## Tips

- Start with the `post_refund` timing setting. Waiting for the return window to expire before issuing rewards prevents rewarding orders that are ultimately returned.
- The `balanced` fraud policy is a good default for most stores. Switch to `strict` if you notice an unusual spike in referrals from a small number of accounts.
- Set realistic monthly and lifetime caps. If your reward value is high, a cap of 10–20 per month per referrer is reasonable to prevent abuse.
- Review **Pending** attributions weekly. Letting them sit unreviewed for too long can frustrate legitimate referrers who are waiting for their reward.
- Use the **Risk Level** filter to prioritise your manual review queue — start with the very high risk attributions before moving to medium risk.
- Keep your Terms & Conditions short and plain-language. Customers are more likely to participate when they understand the rules clearly.
