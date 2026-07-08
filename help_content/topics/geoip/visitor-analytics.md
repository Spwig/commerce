---
slug: visitor-analytics
title_i18n_key: Visitor Analytics
category: customers
component: geoip
keywords:
  - visitor analytics
  - page views
  - traffic stats
  - daily traffic
  - per-URL analytics
  - page statistics
  - unique visitors
  - traffic trends
  - bot filtering
  - device breakdown
  - returning visitors
  - store traffic
  - analytics dashboard
url_patterns:
  - /admin/geoip/dailypagestats/
  - /admin/geoip/dailytrafficstats/
  - /admin/geoip/pageview/
  - /admin/geoip/visitorlocation/
related:
  - geoip-setup
  - customer-analytics
  - business-rules
published: true
---

Visitor Analytics gives you a clear picture of how customers are moving through your store. You can see which pages attract the most visits, how overall traffic trends over time, which devices your customers use, and how new versus returning visitors compare — all without needing any external analytics tools.

## Overview of the analytics screens

Your store tracks visitor activity automatically once the GeoIP system is active. The data is organized into three views, each giving you a different level of detail.

### Daily traffic summary

Navigate to **Customers > Daily Traffic Stats** to see your store's overall traffic for each day. Each row represents one calendar day and shows:

| Column | What it tells you |
|--------|-------------------|
| **Date** | The day the traffic was recorded |
| **Total Views** | All page views, including bots |
| **Unique Visitors** | Distinct visitors (by session) |
| **Bot Views** | Views from crawlers and automated tools |
| **New Visitors** | Sessions with no prior history |
| **Returning Visitors** | Sessions from visitors seen before |
| **Desktop Views** | Views from desktop browsers |
| **Mobile Views** | Views from mobile devices |
| **Tablet Views** | Views from tablet devices |

Use the date hierarchy navigation at the top of the list to quickly jump to a specific month or year. The totals update once daily through an automated background process, so figures for the current day will appear the following morning.

### Per-page statistics

Navigate to **Customers > Daily Page Stats** to see traffic broken down by individual page. Each row shows one URL path on one day, so you can compare the performance of specific pages over time.

| Column | What it tells you |
|--------|-------------------|
| **Date** | The day these stats apply to |
| **URL Path** | The normalized page path (e.g., `/products/blue-widget`) |
| **Views** | Total views for that page that day |
| **Unique Visitors** | Distinct visitors who viewed that page |
| **Bot Views** | Views from bots on that page |
| **Entries** | How many sessions started on this page (it was their landing page) |

Use the **URL Path** search box to find statistics for a specific page. For example, search for `/products/` to see all product page traffic, or search for a specific product slug to focus on one item.

### Individual page view events

Navigate to **Customers > Page Views** for a raw log of every tracked page navigation. This is a read-only record — you cannot add or edit entries. Use it to investigate specific sessions or to verify that tracking is recording correctly.

Each record shows:
- **URL Path** — the page that was visited
- **Session** — a short identifier for the visitor's session
- **Source** — whether the visit came from the headless frontend or the standard storefront
- **Is Bot** — whether the visitor was identified as automated traffic
- **Is Entry Page** — whether this was the first page in their session
- **Timestamp** — the exact time of the visit

You can filter by **Is Bot**, **Source**, and **Is Entry Page** using the sidebar filters, and navigate by date using the date hierarchy at the top.

## Reading traffic trends

The daily traffic summary is your best tool for spotting trends. Look for patterns such as:

- **Traffic spikes** after running a promotion or sending a marketing email
- **Gradual growth** over weeks and months as your store gains organic visibility
- **Weekend vs. weekday patterns** to understand when your customers are most active
- **Mobile vs. desktop splits** to decide whether to prioritize mobile-optimized design changes

The **New Visitors** and **Returning Visitors** columns together tell you how well you are retaining customers. A healthy store typically sees a mix of both — a high proportion of new visitors suggests strong acquisition, while a higher returning share suggests customer loyalty is building.

## Identifying your top pages

The per-page statistics view, sorted by views in descending order (the default), immediately shows you which pages drive the most traffic on any given day. Look for:

- **High-entry, low-view pages** — pages that attract visitors from search or ads but may not hold attention
- **High-view pages with many unique visitors** — popular destination pages worth keeping fresh
- **Product pages with rising view counts** — products that may be gaining search visibility

### Example: finding a product's traffic

To check how much traffic your best-selling product received last week:

1. Navigate to **Customers > Daily Page Stats**
2. Use the date hierarchy to select the relevant week
3. In the search box, enter the product's URL slug (e.g., `/blue-widget`)
4. Review the **Views**, **Unique Visitors**, and **Entries** across the days shown

## Visitor location data

Navigate to **Customers > Visitor Locations** to see a session-level view of where your visitors are located. Each record represents one visitor session and includes:

- Country and city (resolved automatically by the GeoIP system)
- Device type (desktop, mobile, tablet)
- Currency and language preferences the visitor selected
- UTM campaign attribution (source, medium, campaign name)
- Bot and admin traffic flags

You can filter visitors by country, device type, UTM source, and whether they were bots or admin staff. Use the **Is Bot** filter set to false to focus on genuine customer traffic, and the **Is Admin Traffic** filter to exclude your own testing sessions from analysis.

## Tips

- Bot views are tracked separately and excluded from unique visitor counts automatically — your traffic figures reflect real customer activity
- The **Entries** column in per-page stats tells you which pages act as your store's front door from search and ads; optimizing those pages has the biggest impact
- Filter visitor locations by **UTM Source** to measure how much traffic a specific marketing channel (e.g., an email newsletter or a Google ad) is actually sending
- Daily stats are aggregated overnight — if you need to check same-day traffic, use the Page Views log directly
- The device breakdown in the daily summary helps you prioritize design work; if more than half your visits are mobile, ensure your product pages and checkout look great on small screens
