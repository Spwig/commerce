---
slug: audiences
title_i18n_key: Audiences
category: marketing-seo
component: email_marketing
keywords:
  - segment
  - audience
  - target audience
  - customer segment
  - dynamic segment
  - static segment
  - segment rules
  - rule builder
  - starter audiences
  - add starter audiences
  - lifetime value
  - loyalty segment
  - affiliate audience
  - campaign studio
  - RFM segment
url_patterns:
  - /admin/email_marketing/segment/
  - /admin/email_marketing/segment/add/
  - /admin/email_marketing/segment/[0-9a-f-]+/change/
  - /admin/campaigns/segments/seed-starters/
related:
  - ab-testing
  - subscriber-tags
  - recurring-campaigns
  - triggered-journeys
  - customer-segments
published: true
---

A **Segment** is a saved audience you can point a campaign, a journey, or an A/B test at — Campaign Studio's own Segments list calls them "Targeted audiences," and this guide uses both words for the same thing. Every segment is either **dynamic**, defined by rules Spwig re-evaluates each time it's used, or **static**, an explicit list of subscribers you choose by hand.

This guide covers building a dynamic segment's rules — including newer fields that target your store's own customer value buckets, loyalty programme, and affiliates — and the one-click **Add starter audiences** button that builds a set of ready-made segments from whatever data your store already has.

## Dynamic vs. static segments

| Kind | How it works | Best for |
|---|---|---|
| **Dynamic (rules)** | You define conditions — e.g. "Total spent is at least $500." Spwig recalculates who matches every time the segment is used, so membership changes automatically as your subscribers do. | Ongoing audiences that should always be current, like "VIP customers" or "hasn't ordered in 90 days." |
| **Static (fixed list)** | An explicit list of subscribers you add or remove by hand. Membership never changes unless you change it. | A one-off list — everyone from a specific event, or a hand-picked group for a one-time send. |

Choose the kind with the **Kind** field when you create a segment. The rest of this guide is about dynamic segments — static ones are just a member list with no rules to configure.

## Building a dynamic segment

Open **Campaign Studio > Segments**, then click **+ New Segment** (or open an existing dynamic segment) to reach the **Audience rules** builder. Click **+ Add condition** to add a rule, choose what to check and how, and set whether a subscriber must match **all** or **any** of your conditions. A live count in the top-right corner — e.g. "8 matching subscribers" — updates a moment after each change, so you can see exactly who qualifies before you save.

![The Audience rules builder with Customer segment, Loyalty tier, Lifetime value, and Affiliate conditions set, and a live matching-subscriber count](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

A condition with a fixed **is true**-style check — **Has ordered**, **Opted into marketing**, **Loyalty member**, **Affiliate** — needs nothing beyond picking the field itself; there's no operator or value to set.

## What you can target

| Field | What it checks |
|---|---|
| **Total spent** | Lifetime order total. |
| **Number of orders** | Completed order count. |
| **Lifetime value** | The customer's calculated lifetime value. |
| **Average order value** | Average amount per completed order. |
| **Days since last order** | How long since the customer's most recent order — target 90+ days for a win-back audience. |
| **Has ordered** | Whether the customer has at least one completed order. |
| **Opted into marketing** | Whether the subscriber has consented to marketing email. |
| **Language** | The subscriber's stored language. |
| **Source** | How the subscriber joined — Storefront signup, Import, Order, Added manually, or API. |
| **Joined after** | Subscribers who joined on or after a chosen date. |
| **Has tag** | Whether the subscriber carries a [tag](/help/subscriber-tags) you've created. |
| **Customer segment** | Whether the customer falls into one of your store's own named [customer segments](/help/customer-segments) — Guest Customer, New Customer, Regular Customer, Frequent Buyer, High Value, VIP Customer, Bargain Hunter, At Risk, or Inactive. |
| **Loyalty member** | Whether the customer is an active member of your loyalty programme. |
| **Loyalty points** | The member's current available point balance. |
| **Loyalty tier** | Which loyalty tier the member currently holds. |
| **Affiliate** | Whether the customer is one of your active affiliate partners. |

**Customer segment**, the two **Loyalty** value fields, **Loyalty tier**, and **Affiliate** are newer additions, and each only shows up in the condition picker once your store actually has that kind of data: the loyalty fields appear once your loyalty programme has members and at least one active tier, **Affiliate** appears once you have at least one affiliate, and **Customer segment** appears once you have at least one active customer segment configured. You won't see an option on a fresh store that couldn't possibly match anyone.

One current limitation worth knowing: for any condition with a dropdown of choices — **Language**, **Source**, **Has tag**, **Customer segment**, **Loyalty tier** — the **is any of** operator still only lets you pick one value at a time. If you want to match several (say, customers in either your VIP or High Value segment), add one condition per value and set **Match** to **any**.

## Add starter audiences

Building a rule from scratch for every obvious audience — your VIPs, your loyalty members, everyone who's gone quiet — is tedious when Spwig can already see who qualifies. On the Segments list, click **Add starter audiences** and Spwig creates a set of ready-made, editable dynamic segments from whatever customer, loyalty, and affiliate data your store already has.

![The Segments list with the New Segment and Add starter audiences buttons](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Starter | Targets | Needs |
|---|---|---|
| **VIP customers** | Your VIP customer segment | An active VIP customer segment |
| **High-value customers** | Your VIP and High Value customer segments | An active VIP or High Value customer segment |
| **Repeat buyers** | Your Frequent Buyer and Regular customer segments | An active Frequent Buyer or Regular customer segment |
| **New customers** | Your New customer segment | An active New customer segment |
| **Lapsing customers** | Customers who've ordered before but not in the last 90 days | Any customer order history |
| **Loyalty members** | Everyone active in your loyalty programme | An active loyalty programme with members |
| **Top loyalty tier** | Members in your highest-ranked loyalty tier | At least one active loyalty tier |
| **Affiliates** | Your active affiliate partners | At least one affiliate |

Spwig only creates the starters it actually has data for — a store with no loyalty programme yet simply won't get a **Loyalty members** starter, rather than an empty one that could never match anyone. Spwig confirms exactly what it added, for example: "Added 7 starter audience(s): High-value customers, Repeat buyers, New customers, Lapsing customers, Loyalty members, Top loyalty tier, Affiliates."

![Success message confirming which starter audiences were just added](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

It's safe to click **Add starter audiences** more than once. Spwig never creates a duplicate of a starter that already exists, so clicking it again after setting up (say) your loyalty programme for the first time only adds whatever's newly available — if everything's already set up, it simply says so.

![Info message shown when every starter audience already exists](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

If you delete a starter you don't want, clicking **Add starter audiences** again won't bring it back — Spwig treats it as a segment you removed on purpose, not one to recreate.

Once seeded, a starter is an ordinary dynamic segment: open it from the list to review or adjust its rules, rename it, or delete it, exactly as you would any segment you built yourself.

## Who these audiences actually reach

The customer, loyalty, and affiliate conditions above only match subscribers whose email is linked to a customer account — an anonymous newsletter signup won't match a **Loyalty member** or **VIP** condition, even correctly so, since Spwig has no order or loyalty history to check them against. If a lot of your customers have accounts but haven't subscribed yet, ask whoever manages your Spwig installation to run a subscriber sync — it creates a Subscriber record for every existing customer account in one step, so these audiences have real people to match against.

However many subscribers a segment counts, that number describes who *could* receive a campaign, not who will. Every send still checks each subscriber's own marketing consent first, so a segment is never a way around it.

## Tips

- Start from a starter audience and adjust it rather than building the same rule by hand — once created, a starter is no different from any segment you built yourself.
- Boolean conditions like **Loyalty member**, **Affiliate**, and **Has ordered** need no operator or value — just add the condition and you're done.
- Combine the newer fields with the originals for tighter targeting, e.g. **Loyalty member** plus **Opted into marketing**, rather than relying on a single condition alone.
- If a segment's rules reference something that's since been removed — a deleted customer segment, an emptied-out tag, and so on — Spwig treats it as matching nobody rather than falling back to your entire subscriber list. Broken targeting under-sends; it never blasts everyone by accident.
- If a segment's member count looks stale, open it and save again, or use the **Rebuild member counts** bulk action from the Segments list, to recalculate it immediately.
- Watch the live "matching subscribers" count while you build a rule — it's the fastest way to catch a condition that's narrower (or broader) than you intended before you save.
