---
slug: revenue-attribution
title_i18n_key: Revenue Attribution
category: marketing
component: attribution
keywords:
  - revenue attribution
  - multi-touch attribution
  - attribution model
  - last touch
  - first touch
  - linear attribution
  - time decay
  - position based attribution
  - marketing channels
  - UTM tracking
  - campaign performance
  - customer journey
  - Sankey diagram
  - influenced revenue
  - marketing ROI
url_patterns:
  - /admin/insights/attribution/
related:
  - visitor-analytics
  - affiliate-analytics
  - referral-program
  - voucher-campaign-ideas
  - staff-roles
published: true
---

Revenue Attribution shows you where your sales actually come from — not just the last link a customer clicked before they bought, but every channel that played a part in getting them there. If a customer reads a blog post you shared on social media, then comes back a week later through a Google search, then finally buys after clicking a link in a newsletter, all three of those touches contributed to that sale. This dashboard credits all of them, using a model you choose, so you can see your marketing the way it actually works instead of the way "last click wins" pretends it works.

![The Revenue Attribution dashboard: the attribution model switcher, the KPI strip with the "Reconciles to net revenue" badge, revenue by channel, revenue over time, the customer-journey flow, and the campaigns table](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## Where to find it

Navigate to **Insights > Revenue Attribution** in the sidebar. Insights is a dedicated menu group above Products, so Revenue Attribution has its own home separate from your order and customer reports.

Insights is gated by the **Insights & Analytics** permission category. If you don't see it in your sidebar, ask a store administrator to grant you that permission — see [Staff Roles & Permissions](/help/staff-roles) for how to manage staff access.

## Understanding multi-touch attribution

Most stores are used to thinking in terms of "where did this order come from?" as if there's a single answer. In reality, customers rarely buy on their first visit. They discover you one way, come back another way, and convert a third way — sometimes across several visits spread over days or weeks. Each of those visits is a **touch**: a recorded arrival at your store carrying a signal about where it came from (an email link, a search result, a social post, an affiliate link, and so on).

**Multi-touch attribution** means recognizing every touch in that journey and deciding how much credit each one deserves for the eventual sale, instead of handing 100% of the credit to whichever channel happened to be clicked last. This matters because last-click reporting systematically undervalues the channels that do the early discovery work — your blog, your organic search presence, your social posts — because they rarely get to be the final click before checkout.

## Choosing an attribution model

The model switcher at the top of the dashboard is the most important control on the page. Click any model and every number on the dashboard — the KPI strip, the channel bars, the chart, the campaigns table — instantly re-credits itself to match. This is a live preview: switching models here changes how you're looking at your existing revenue, it doesn't rewrite any records or change your store's saved default model.

![The attribution model switcher — Last touch, First touch, Linear, Time decay and Position 40/20/40 — with the "Re-attributes live · no reprocessing" indicator](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Model | What it does | Best for |
|-------|---------------|----------|
| **Last touch** | Gives full credit to the last channel before the order, ignoring earlier touches (except pure "direct" visits, which are skipped in favor of the last real source) | A quick, familiar view — how most basic analytics tools report revenue |
| **First touch** | Gives full credit to whichever channel first brought the customer to your store | Understanding what's driving new customer discovery and top-of-funnel growth |
| **Linear** | Splits credit evenly across every touch in the journey | A balanced, no-opinion view when you don't want any single channel favored |
| **Time decay** | Gives more credit to touches closer to the order, less to touches further back | Campaigns with a short consideration window, where recent nudges matter most |
| **Position 40/20/40** | Gives 40% credit to the first touch, 40% to the last touch, and splits the remaining 20% across everything in between | Recognizing both "who found us" and "who closed the sale" while still crediting the middle of the journey |

There's no single "correct" model — each one answers a different question. A common approach is to check **First touch** to see what's driving discovery, then **Last touch** or **Position 40/20/40** to see what's driving conversions, and use both views together rather than picking one and ignoring the rest.

## Reading the KPI strip

Just below the model switcher, four figures summarize the selected period and model:

- **Attributed revenue** — the total revenue credited across all channels for the current model. It carries a **Reconciles to net revenue** badge when the figures add up correctly to your store's actual net revenue for the period — in other words, the model is splitting real revenue between channels, not inventing or losing any of it.
- **Orders** — how many orders fall in the selected date range.
- **Avg. touches / order** — the average number of recorded touches per order. A number above 1 confirms that most of your customers' journeys involve more than a single visit, which is exactly why multi-touch attribution matters for your store.
- **Leading channel** — whichever channel currently holds the largest share of attributed revenue under the selected model, with its share percentage and revenue.

## Revenue by channel

The **Revenue by channel** card shows a horizontal bar for each channel, sized by attributed revenue. Switch the attribution model and watch the bars smoothly reorder themselves by rank — this is the same underlying revenue, just re-split by a different set of rules, so a channel that looks strong under **Last touch** may drop several places under **First touch** if it mostly plays a supporting role.

## Revenue over time

The **Revenue over time** chart stacks attributed revenue by channel across each day in the selected range, so you can see not just how much each channel is worth but when it's contributing. Use it to spot seasonal patterns, confirm a campaign's impact landed on the days you expected, or check whether a channel's contribution is growing or fading over the period.

## How customers actually arrive

The **How customers actually arrive** panel is a journey flow chart connecting the channel that first brought a customer in (on the left) to the channel present when they converted (on the right). Thicker ribbons mean more revenue flowed through that path. This is the clearest way to see multi-step journeys at a glance — for example, a thick ribbon from Organic Search to Email tells you that search is bringing people in, but your email marketing is what's bringing them back to buy.

![The customer-journey flow chart, with the Influenced lens selected, showing first-touch channels on the left flowing to the channel each order converted on](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

Use the **Attributed** / **Influenced** toggle above the chart to switch lenses:

- **Attributed** splits each order's revenue across the model you selected, so the totals add up to 100% of attributed revenue — the same figures shown elsewhere on the dashboard.
- **Influenced** credits *every* channel that touched an order with that order's *full* value, counted once per order. This deliberately does not add up to 100% — a channel can be "influenced" by revenue that's also fully counted for another channel. It exists to surface the reach a channel had that last-click reporting hides entirely, such as a blog post or a social share that got someone interested even though they didn't click it on their final visit.

## Campaigns

The **Campaigns** table breaks down revenue, orders, and average order value (AOV) for each of your tagged campaigns — links or codes you've marked with a campaign name, including campaign-tagged voucher codes (see [Voucher Campaign Ideas](/help/voucher-campaign-ideas)). Use it to compare how individual promotions, influencer codes, or marketing pushes performed against each other, independent of which channel carried them.

## Date range and exporting your data

Use the date range selector in the top-right to switch between **Last 7 days**, **Last 14 days**, **Last 30 days**, **Last 90 days**, and **Month to date**. The whole dashboard refreshes for the new period.

Click **Export CSV** to download the channel breakdown for the currently selected model and date range — useful for pulling numbers into a spreadsheet or sharing with a partner agency.

## How touches get recorded

Spwig automatically captures a touch whenever a visitor arrives at your store carrying a recognizable source signal, and only when the visitor has given **Analytics** consent in your store's cookie banner (if you don't run a consent banner, tracking is on by default, as your store's own policy dictates). This keeps revenue attribution on the same privacy footing as the rest of your storefront's analytics.

Several sources are tagged automatically, with no setup required:

| Channel | How it's identified |
|---------|----------------------|
| **Email** | Links in your marketing emails (not order or shipping emails) |
| **Organic / Paid Search** | Search engine referrers, or `utm_medium` values marking a paid search campaign |
| **Organic / Paid Social** | Social network referrers, or social `utm_medium` values |
| **Affiliate** | Links generated through your Affiliate program |
| **Refer a Friend** | Links generated through your customer referral program |
| **Campaign** | Any link or code carrying a campaign tag, including campaign-tagged voucher codes |
| **External Link** | An inbound link from another website that isn't otherwise categorized |
| **Direct** | No source signal was present — the visitor typed your address, used a bookmark, or arrived from an app with no referrer |

Blog posts that were auto-shared to your connected social accounts are automatically tagged, so traffic they generate shows up under the right social channel rather than being lost to Direct or External Link.

You can also tag your own links by hand using standard `utm_source`, `utm_medium`, and `utm_campaign` parameters on any URL pointing at your store — useful for print materials, partner newsletters, or any channel Spwig doesn't auto-tag.

## Limitations to keep in mind

- **Attribution follows a browser, not a person.** If a customer researches on their phone and buys on their laptop, those are two separate journeys as far as tracking is concerned — there's no way to link activity across different devices. This means some credit that "should" go to an earlier touch on another device will land on Direct instead.
- **Direct is where untracked revenue lands.** A high Direct share doesn't necessarily mean people are typing your URL from memory — it can also mean a customer's earlier touches happened on a different device, or that a link they used wasn't tagged.
- **Declined consent means no touch is recorded.** Visitors who decline analytics consent in your cookie banner are not tracked, so their orders will show up as Direct even if they arrived via a channel you'd otherwise recognize.

## Tips

- Check more than one model before drawing conclusions — a channel that looks weak under **Last touch** can be your strongest discovery driver under **First touch**.
- If **Direct** makes up a large share of your revenue, look at whether more of your marketing links could be tagged with `utm_source`/`utm_medium`/`utm_campaign` — untagged traffic has nowhere else to land.
- Use the **Influenced** lens on the journey flow chart when you're deciding whether to keep investing in a channel like organic search or blog content that rarely gets the last click but consistently starts journeys.
- Compare **Avg. touches / order** over time — a rising number usually means customers are taking longer to decide, which is a useful signal when planning follow-up email or retargeting timing.
- Export the CSV for the model and period you're reporting on before you switch models again, since the export reflects whichever model is selected at the moment you click **Export CSV**.
