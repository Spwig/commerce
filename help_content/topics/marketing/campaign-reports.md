---
slug: campaign-reports
title_i18n_key: Campaign Reports
category: marketing-seo
component: email_marketing
keywords:
  - campaign report
  - email report
  - open rate
  - click rate
  - bounce rate
  - delivery rate
  - spam complaint
  - hard bounce
  - soft bounce
  - click-to-open rate
  - campaign performance
  - email deliverability
  - campaign studio
  - email analytics
  - engagement over time
  - top links
  - click-through rate
  - recipients list
  - recipient activity
  - email timeline
  - attributed revenue
  - revenue attribution
  - ROAS
  - return on ad spend
  - campaign spend
  - AOV
  - average order value
url_patterns:
  - /admin/campaigns/[0-9a-f-]+/report/
  - /admin/campaigns/[0-9a-f-]+/recipients/
  - /admin/email_marketing/campaign/
  - /admin/campaigns/dashboard/
related:
  - list-hygiene
  - ab-testing
  - recurring-campaigns
  - audiences
  - revenue-attribution
  - deliverability
published: true
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: The report page scrolled to the "Engagement over time" chart card, with a campaign that has several days of send history so all three lines (Sent, Opened, Clicked) show a realistic shape.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: The report page's "Top links" card, with a campaign whose email contains at least 3 distinct links and a realistic spread of Clicks/Unique/CTR values.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: The Recipients page with the filters panel open and a mixed list of rows (some opened, some clicked, some bounced) so the engagement states are visibly distinct.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: The Recipients page with the "Recipient activity" modal open for a recipient who has multiple event types (delivered, opened, at least one clicked entry naming a link).
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: A close-up of the report page's "Attributed revenue" stat card, for a campaign with a logged Spend so the orders/AOV/revenue-per-email/ROAS sub-line is fully populated.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: The Campaign Studio dashboard's stat card grid, scrolled/cropped to show the "Attributed revenue (30d)" tile alongside its neighboring cards, with a non-zero revenue figure.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: the existing report-stat-cards.webp only shows 6 cards (Recipients, Delivered, Open rate, Click rate, Bounce rate, Spam complaints). The stat grid now has a 7th "Attributed revenue" card — recapture this shot with a campaign that has both attribution data and a logged Spend so all 7 cards are visible in a realistic state.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Every campaign you send through Campaign Studio gets its own **Report** page — a single-page summary of how many people it reached, how many emails actually arrived, and how recipients responded. Use it to check a send went smoothly, spot a deliverability problem early, or compare how different campaigns perform over time.

## Opening a report

From **Campaign Studio > Campaigns**, find the campaign you want to check and click the chart icon (**Report**) on its card.

![The Campaign report page's stat card grid, showing recipients, delivered, open rate, click rate, bounce rate, and spam complaints](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

A report only has numbers to show once a campaign has actually been sent — a campaign still in **Draft** shows every stat as zero, since there's nothing to measure yet.

## The stat cards

| Card | What it shows |
|------|---------------|
| **Recipients** | How many subscribers this campaign targeted, plus a sub-line noting how many were skipped and, of those, how many were skipped specifically because the address is on your [suppression list](list-hygiene). A skip isn't always a suppression — Spwig also skips a subscriber who has no usable email address, for example — so the two counts are shown separately. |
| **Delivered** | How many emails were actually accepted by the receiving mail server and never bounced back, plus the **delivery rate** — delivered as a share of every send Spwig *attempted* (accepted by your mail server or provider, whether or not it later bounced). |
| **Open rate** | The share of *delivered* email that was opened, plus the raw **opened** count. |
| **Click rate** | The share of *delivered* email that was clicked, plus the raw **clicked** count and the **click-to-open rate** — clicks as a share of opens, a read on how compelling your content was to people who already opened it. |
| **Bounce rate** | The share of *attempted* sends that bounced, broken down into **hard** and **soft** bounces. |
| **Spam complaints** | How many recipients marked the email as spam or junk, plus the **complaint rate** — complaints as a share of *delivered* mail. |
| **Attributed revenue** | Revenue from orders Spwig can trace back to this campaign, plus the number of orders, the average order value (**AOV**), revenue per email delivered, and — once you've logged what the campaign cost — its **ROAS**. See [Attributed revenue](#attributed-revenue) below. |

## Why the rates use different denominators

Open rate, click rate, and complaint rate are all measured against **delivered** mail — the recipients who could actually see the email — while delivery rate and bounce rate are measured against **attempted** sends. This is standard email-industry practice, and it's why none of these rates can ever read above 100%: an email that bounced was never delivered, so it can't count against your open or click rate, and an email that was never even attempted (a skip) doesn't count against any of them.

## Hard bounces vs. soft bounces

- **Hard bounce** — the address is permanently undeliverable. It doesn't exist, or the domain refuses to accept mail for it at all.
- **Soft bounce** — a temporary problem: a full mailbox, a receiving server that was briefly unavailable, and similar. Soft bounces are often self-resolving.

Watch the split, not just the total. A rising **hard bounce** count usually means your list has stale or mistyped addresses; a rising **soft bounce** count is more often a temporary hiccup at the recipient's end. Any hard bounce, any spam complaint, and an address that racks up repeated soft bounces all feed Spwig's automatic [suppression list](list-hygiene) — you don't need to act on them yourself, but the report is where you'll first notice a spike worth investigating.

## Attributed revenue

Because your store and Campaign Studio live in the same system, Spwig doesn't need an external analytics platform or a tracking pixel to tell you whether a campaign actually drove sales. When a customer clicks a link in this campaign's email and lands on your store, Spwig can follow that visit through to checkout and credit the resulting order's revenue back to the campaign — that's what the **Attributed revenue** card shows.

The card's sub-line breaks the figure down further:

- **Orders** — how many orders are credited to this campaign.
- **AOV** — the average order value across those orders.
- **Revenue per email** — attributed revenue divided by the number of emails *delivered*, the same denominator the report uses for open rate and click rate.
- **ROAS** — return on ad spend, shown only once you've entered a **Spend** amount on the campaign itself. It's calculated as attributed revenue divided by spend. If the spend was logged in a different currency than your store's default, Spwig hides ROAS rather than show a figure that doesn't actually compare like for like — enter spend in your store's base currency to see it.

A few things worth knowing about how this figure is calculated:

- **It's click-through, not open-based.** A customer has to click a tracked link in the email and arrive at your store — an open alone never attributes revenue. This is deliberate: open tracking is increasingly unreliable now that services like Apple Mail Privacy Protection pre-load images for nearly every message, inflating open counts regardless of whether anyone actually read the email.
- **It follows your store's attribution model.** By default that's **last non-direct touch** with a 90-day lookback window — the same click has to lead to an order within that window to be counted, and a later direct visit doesn't erase credit already earned by this campaign's click.
- **It respects analytics consent.** Only visitors who accepted analytics consent in your store's cookie banner are tracked (if you don't run a consent banner, tracking follows your store's own default policy). A customer who declined consent can still buy — their order just won't be attributed to any channel, including this one.
- **It isn't retroactive.** Revenue tracking only covers campaigns sent after attribution tracking was switched on for your store. A campaign sent before then will show no attributed revenue here even if it drove real sales, simply because Spwig has no click data recorded for it.
- **A/B tests and recurring campaigns roll up their attributed revenue too** — see [Reports on an A/B test](#reports-on-an-ab-test) below.

You'll also find an **Attributed revenue (30d)** card on the Campaign Studio dashboard itself, summing attributed revenue from email across every campaign over the trailing 30 days — a quick pulse check without opening an individual report. For a store-wide view that includes every channel, not just email — organic search, social, affiliates, and more — see the [Revenue Attribution](/help/revenue-attribution) dashboard under **Insights**.

## Engagement Over Time

Below the stat cards, the **Engagement over time** chart plots three lines — **Sent**, **Opened**, and **Clicked** — one point per day, covering the 30 days leading up to today (or fewer, if the campaign hasn't been sending that long — the chart never starts earlier than the day of the campaign's first send).

A few things to know about how the lines are counted:

- **Opened** and **Clicked** count each recipient once — the day of their *first* open or *first* click — not every time they re-open the email or click a link again. This keeps the chart from being skewed by a handful of people who open the same email repeatedly.
- The totals behind this chart line up with the stat cards above it: **Sent** reflects mail Spwig attempted to deliver, while **Opened** and **Clicked** are both measured against delivered mail, the same as the **Open rate** and **Click rate** cards.
- The chart only appears once the campaign has at least one send recorded — a campaign still in **Draft** shows the "No sends yet" message instead, same as the stat cards.

Use this chart to see the *shape* of a send, not just its final numbers — a campaign that goes out to a large list often shows a sharp spike in opens on the first day or two, tapering off afterward. A second bump days later can point to a recipient's mail server queuing your message, or to your subject line getting noticed later than usual.

## Top Links

If your email contains links and at least one recipient has clicked one, a **Top links** table appears beneath the chart, listing every tracked link ordered by popularity.

| Column | What it shows |
|--------|---------------|
| **Link** | The destination URL as it appeared in your email. |
| **Clicks** | The total number of times that link was clicked, including repeat clicks from the same recipient. |
| **Unique** | How many distinct recipients clicked that particular link at least once. |
| **CTR** | That link's **click-through rate** — its **Unique** count as a share of delivered mail. This uses the same denominator as the report's headline **Click rate** card, so you can compare a single link's pull directly against the campaign's overall click performance. |

If your email links to several products or a mix of call-to-action buttons, this table is the quickest way to see which one actually earned the click — useful for deciding what to feature more prominently next time.

## Recipients

Click **Recipients** at the top of the report to open a full, searchable list of everyone this campaign was sent to, with each person's delivery outcome and engagement.

Two ways to narrow the list:

- **Search** — filters by email address (a partial match works, so typing part of a domain or name is enough).
- **Engagement** — filters to one state at a time: **Opened**, **Clicked**, **Delivered, not opened**, or **Bounced**. Leave it on **Everyone** to see the full list.

The list shows the most recent 100 matching recipients at a time, newest first — the count above the list always reflects the true total that matches your current filters, even if it's larger than what's shown. For a big send, narrow the list with Search or Engagement first rather than scrolling through everyone.

### Viewing a recipient's activity timeline

Click the activity icon on any recipient's row to open their **Recipient activity** timeline — every tracked event for that person's copy of the email, in order: delivered, opened, clicked (naming which link), bounced (with the bounce reason), marked as spam, or unsubscribed, each with its own timestamp.

This is the fastest way to answer a specific question about one customer — for example, confirming whether a particular subscriber actually received a campaign before following up with them by another channel, or checking which link a customer clicked before they placed an order.

## Reports on an A/B test

If the campaign you're viewing is the container for an [A/B test](ab-testing), its report aggregates across **every variant** — the whole test, combined, including **Attributed revenue** — rather than showing one variant on its own. To see how each individual variant performed, open the test's own results page instead of the report. A [recurring campaign](recurring-campaigns) works the same way: its report rolls up every occurrence it has sent.

## What good looks like

There's no single healthy number that fits every store or list — audience, industry, and content all shift the baseline — but a few patterns are worth watching for on any campaign:

- A **bounce rate** that's mostly soft bounces, with hard bounces rare, points to a clean, well-maintained list. A sudden jump in hard bounces is worth investigating before your next send.
- **Spam complaints** near zero are the goal on every send. Complaints hurt your sender reputation more than almost anything else — see [List Hygiene](list-hygiene) for why they matter beyond this one campaign.
- A **click-to-open rate** that's healthy relative to your open rate tells you the people who opened found the content worth acting on — a low click-to-open rate alongside a strong open rate usually points to the subject line working better than the content inside.

## Tips

- Check the report a little while after sending, not immediately — opens and clicks (and some bounce reports) can take time to roll in from your mail provider.
- If **Delivered** looks lower than expected, check the **Recipients** card's skip breakdown first — a batch of skips due to suppression is often the real story, not a delivery problem.
- Use the report to compare a campaign against your own past sends rather than against a generic industry number — your list, content, and audience are what set your realistic baseline.
- A spike in complaints on one particular send is worth a closer look at that campaign's content or targeting, not just a note to move on from.
- For an A/B-tested campaign, read this report for the overall outcome and the [A/B test results](ab-testing) page for which variant actually won and by how much.
- Use the **Top links** table to find your most-clicked link, then check whether it matches what you *wanted* recipients to click — if a secondary link is beating your main call to action, it may be worth moving it higher in the email next time.
- The **Recipients** page's **Opened** and **Clicked** filters are a quick way to build a follow-up audience — for example, checking who opened but didn't click before planning a reminder send to the rest of the list.
- If you paid for a promotion around a send — a boosted social post, an influencer shoutout, paid list rental — log it as the campaign's **Spend** to unlock **ROAS** on the report. It's the fastest way to see which kinds of sends are actually worth repeating.
