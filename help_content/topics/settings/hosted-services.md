---
slug: hosted-services
title_i18n_key: Spwig Hosted Services
category: settings
component: core
keywords:
  - hosted services
  - GeoIP
  - geocoder
  - push notifications
  - usage quota
  - free tier
  - Community edition
  - service limits
  - upgrade plan
  - address lookup
  - visitor country detection
  - mobile push
  - quota warning
  - bandwidth usage
  - service usage
url_patterns:
  - /admin/
related:
  - multi-currency-setup
  - configuring-autocomplete
  - cdn-setup
published: true
---

Spwig includes three optional cloud services that your store can use without you having to configure or host anything yourself: **GeoIP** detects where your visitors are located, **Geocoder** turns customer addresses into map coordinates, and **Push** sends instant notifications to your mobile Spwig admin app. On the Community (free) edition, each service comes with a generous monthly allowance. When any service approaches its limit, Spwig warns you in the admin so you can decide whether to upgrade before your customers notice anything.

## The three hosted services

### GeoIP — visitor country detection

GeoIP looks up the country of each visitor based on their IP address. Your store uses this information to automatically display the right currency when a customer arrives, and to pre-fill the country field during checkout. For example, a visitor from Germany will see prices in euros, and a visitor from Japan will see prices in yen — without having to choose manually.

Each page load where GeoIP runs a lookup counts against your monthly quota. Repeat visits from the same browser session do not each consume a lookup; the result is cached for the session. GeoIP lookups only happen on the storefront, not in your admin panel.

### Geocoder — address to coordinates

Geocoder translates customer-typed addresses into geographic coordinates (latitude and longitude). Your store uses these coordinates for two purposes: calculating distance-based shipping costs when you have pickup points or radius-based shipping rules, and powering the address autocomplete suggestions on the checkout page so customers can find their address quickly.

A geocoder lookup is triggered when a customer selects or confirms an address during checkout. Like GeoIP, results are cached so the same address is only looked up once per session.

### Push — admin app notifications

Push delivers real-time notifications to your Spwig merchant mobile app. When a new order arrives, when stock drops below a threshold, or when a customer sends a message, Push sends an instant notification to your device so you can respond without having to keep the admin panel open.

Each notification sent to your device counts as one push request against your monthly quota.

## The Community free tier

On the Community edition of Spwig, each service is included at no cost up to a monthly request limit. The exact limits are set by Spwig and can vary; your admin dashboard always shows the current figures for your install. Paid plans (Starter, Growth, Pro, Pro Plus) and self-hosted installs with a paid licence have higher limits for each service.

When a service reaches 100% of its Community quota, requests to that service stop until the next calendar month resets the counter. The impact on your store depends on which service is affected:

| Service | What happens at 100% |
|---------|----------------------|
| GeoIP | Currency auto-detection falls back to your store's default currency. Customers can still change currency manually. |
| Geocoder | Address autocomplete stops offering suggestions. Customers can still type their address manually. Shipping rate calculation continues using the last known coordinates. |
| Push | New admin app notifications are queued but not delivered until the next month or an upgrade. |

Your store continues to operate normally in all cases — no orders are lost and customers can still check out. The effects are limited to convenience features.

## Reading the dashboard tile

The **Spwig services usage** tile appears on your admin dashboard home page. It shows a progress bar for each of the three services.

Each row in the tile follows the same layout:

- **Service name** (left) — GeoIP, Address lookup (Geocoder), or Push notifications.
- **Progress bar** (centre) — fills left to right as usage increases. The colour of the bar changes as limits approach:
  - **Green** — usage is below 80%. Everything is running normally.
  - **Amber** — usage is between 80% and 99%. The service is still running but getting close to the limit.
  - **Red** — usage has hit 100%. The service is now throttled for this month.
- **Usage counts** (right) — the exact number of requests used out of the total allowed, for example `3,241 / 10,000`. The label in parentheses shows the time window, typically `(this month)`.

If the tile cannot reach the Spwig update server to fetch your current usage (for example, if your server has no outbound internet access), the counts column shows a dash (`—`) for that service. This does not mean the service is broken; it means the usage display is temporarily unavailable.

### The Upgrade button

When any service reaches 80% or more, an **Upgrade** button appears in the top-right corner of the tile. Clicking it opens the Spwig upgrade page where you can compare plans and raise your service limits. The button disappears once usage drops back below 80% at the start of the next month.

## The quota warning banner

In addition to the dashboard tile, a banner appears at the top of every admin page whenever any service crosses the 80% threshold. The banner only appears on Community installs.

**Amber banner — approaching the limit (80–99%)**

> **Approaching hosted-services limit:** One of your Spwig services is over 80% of its Community-tier quota. Upgrade to raise the limit before it's hit.

This banner is an early heads-up. Your services are still running, and you have time to decide whether to upgrade before the month ends.

**Red banner — limit reached (100%)**

> **Spwig services limit reached:** One of your hosted services has hit its Community-tier quota. Upgrade to keep them running without interruption.

This banner appears when at least one service has hit 100% and is now throttled. Clicking **Upgrade** on either banner opens the same upgrade page as the tile button.

The banner disappears automatically at the start of the next calendar month when the counters reset, or immediately after you upgrade to a paid plan.

## Email alert at 90%

When any service crosses 90% of its quota, Spwig also sends a one-time warning email to the address configured in your store settings (**Settings > Store Settings > Contact > Admin Email**). The email is sent at most once per service per calendar month, so you won't be flooded with messages. No email is sent at 100% because at that point the in-admin banner already makes the situation clear.

If you don't receive the email, check that your admin email address is set correctly under **Settings > Store Settings**.

## Upgrading your plan

When you upgrade from Community to any paid plan, the higher limits take effect immediately — no store restart or configuration change is needed. The dashboard tile will show the new, higher limit the next time it refreshes (within five minutes).

To upgrade, click the **Upgrade** button on the dashboard tile or quota banner, or visit the Spwig upgrade page directly. Paid plans include the same three hosted services (GeoIP, Geocoder, Push) at raised monthly limits, plus access to Spwig-hosted email delivery and priority support.

## Self-hosting and Pro licences

If you run a self-hosted Spwig install with a paid licence, your licence tier determines your service limits, the same as the equivalent hosted plan. Your store still needs outbound internet access to reach `updates.spwig.com` for the platform to fetch and verify your tier configuration. The usage counters displayed in the dashboard tile are pulled from the hosted service endpoints at `geoip.spwig.com`, `geocoder.spwig.com`, and `push.spwig.com`.

There is currently no option to replace GeoIP, Geocoder, or Push with self-hosted alternatives — these services are provided exclusively by Spwig's infrastructure and are included in all editions.

## Tips

- **Check the tile regularly at the end of busy months** — a sales event or promotion can spike GeoIP and Geocoder lookups significantly. The tile gives you advance notice before customers are affected.
- **Currency fallback is invisible to most customers** — if GeoIP hits its limit, customers will see your store's default currency. This is rarely a serious problem for stores that primarily serve one market; it matters more for genuinely international stores.
- **Address autocomplete is a convenience, not a blocker** — when Geocoder is throttled, customers can still type and submit their address normally. If you run frequent promotions that drive high checkout traffic, consider upgrading before busy periods.
- **Push throttling does not lose notifications permanently** — queued notifications from the throttled period are not delivered retroactively when the month resets or after an upgrade. If you rely heavily on push for time-sensitive order alerts, upgrading before the limit is reached ensures you don't miss anything.
- **The 5-minute cache means the tile isn't perfectly real-time** — usage figures are refreshed roughly every five minutes in the background. During unusually high-traffic periods, the actual usage may be slightly ahead of what the tile shows.
- **Set your admin email address** — the 90% warning email only works if **Settings > Store Settings > Admin Email** is filled in. It's worth confirming this is set correctly so you get the heads-up before problems arise.
