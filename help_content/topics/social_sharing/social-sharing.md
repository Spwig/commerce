---
slug: social-sharing
title_i18n_key: Social Sharing
category: marketing-seo
component: social_sharing
keywords:
  - social sharing
  - share buttons
  - social media
  - Facebook share
  - Twitter share
  - Pinterest share
  - WhatsApp share
  - LinkedIn share
  - share tracking
  - share counts
  - social buttons
  - blog auto-share
  - share analytics
url_patterns:
  - /admin/social_sharing/socialsharingsettings/
  - /admin/social_sharing/socialshare/
  - /admin/social_sharing/sharecount/
related:
  - blog-management
  - ai-seo-generator
  - loyalty-program
published: true
---

Social sharing buttons let customers share your products, blog posts, and pages to social networks directly from your storefront. You control which platforms appear, how the buttons look, where they are placed, and whether sharing activity is tracked and counted.

## Configuring social sharing settings

All social sharing behavior is controlled from a single settings page. Navigate to **Marketing > Social Sharing Settings** (the page redirects automatically to the settings form — there is only one settings record).

### Placement: where buttons appear

The **Placement** section controls which types of content show share buttons automatically.

| Setting | Description |
|---------|-------------|
| **Enable on Products** | Show share buttons on product detail pages |
| **Enable on Categories** | Show share buttons on category listing pages |
| **Enable on Blog Posts** | Show share buttons on blog post pages |
| **Enable on Custom Pages** | Show share buttons on custom store pages |

Check the content types where you want buttons to appear. You can enable any combination — for example, products and blog posts only.

**Placement Position** controls where on the page the buttons are displayed:

| Option | Description |
|--------|-------------|
| **Below Content** (default) | Shown after the main content |
| **Above Content** | Shown before the main content |
| **Sidebar** | Shown in the page sidebar |
| **Floating (sticky)** | Sticks to the side of the viewport as the visitor scrolls |

### Appearance: how buttons look

The **Appearance** section controls which platforms are shown and how the buttons are styled.

**Enabled Platforms** — leave empty to show all supported platforms, or enter a JSON array to restrict which platforms appear:

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Supported platform keys: `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Button Style** options:

| Style | Description |
|-------|-------------|
| **Icon Only** (default) | Shows only the platform icon |
| **Icon + Label** | Shows the icon and the platform name |
| **Label Only** | Shows only the platform name as text |

**Button Size** — choose **Small**, **Medium** (default), or **Large** to match your storefront's design.

**Layout Direction** — arrange buttons **Horizontally** (default, side by side) or **Vertically** (stacked).

**Show Title** — when checked, a "Share" heading appears above the button group.

**Mobile Visibility** controls button display on small screens:

| Option | Description |
|--------|-------------|
| **Always Show** (default) | Buttons visible on all devices |
| **Hide on Mobile** | Buttons hidden on mobile devices |
| **Mobile Only** | Buttons shown only on mobile devices |

### Tracking settings

**Show Share Counts** — when checked, a count badge appears on each button showing how many times that platform has been shared. Counts update in real time as shares are recorded.

**Track Shares** — when checked, every share click is recorded in the share analytics. Disabling this stops new records from being saved but does not delete existing data. Tracking also awards loyalty badges to customers who share (if the loyalty program is active).

Click **Save** at the bottom of the form to apply your changes. Settings take effect immediately.

## Viewing share activity

### Individual share events

Navigate to **Marketing > Social Shares** to see a log of every recorded share event. Each entry shows:

- **Platform** — which social network was used (shown as a color-coded badge)
- **Shared Content** — the type and name of the content that was shared (e.g., `product: Blue Widget`)
- **User** — the customer who shared, or "Anonymous" for visitors who were not logged in
- **Device Type** — desktop, mobile, or tablet
- **Shared At** — the date and time of the share

The share log is read-only — entries are created automatically when customers click share buttons. Use the **Platform** and **Device Type** filters to explore sharing patterns, and the date hierarchy to look at specific time periods.

### Share counts by content

Navigate to **Marketing > Share Counts** to see aggregated share totals grouped by content item and platform. This view makes it easy to identify your most-shared products and posts.

Each entry shows:
- **Content** — the type and name of the item (e.g., `product: Blue Widget`)
- **Platform** — the social network
- **Share Count** — total shares recorded on that platform
- **Last Updated** — when the count was last recalculated

The list is sorted by share count descending, so your most viral content appears at the top. Share counts are updated automatically whenever a new share event is recorded — there is no need to refresh them manually.

## Understanding how shares are tracked

When a customer clicks a share button, Spwig records:

1. Which platform they shared on
2. What content was shared (product, blog post, page, etc.)
3. Whether they were logged in (if so, the share is linked to their account for loyalty integration)
4. Their device type
5. The URL that was shared

The share count for that platform and content item is then incremented automatically. If **Show Share Counts** is enabled, the updated count appears on the button the next time the page loads.

## Loyalty integration

If your loyalty program is active and **Track Shares** is enabled, customers who are logged in earn loyalty badges when they share content. The social share badge is part of the loyalty program's action-based rules.

To configure point awards for sharing, navigate to **Customers > Loyalty Rules** and look for rules with the **Action-Based** type and **Social Share** action type.

## Tips

- Enable sharing on products and blog posts first — these are the content types customers are most likely to share organically
- Pinterest is particularly valuable for visual product categories like fashion, home decor, and food — prioritize it in the `enabled_platforms` list for those stores
- WhatsApp sharing drives strong conversion from warm referrals, especially on mobile; consider using **Mobile Only** display mode for WhatsApp while keeping other platforms visible on all devices
- If you notice share counts are inflated, check whether test traffic (from admin sessions) was counted before the **Is Admin Traffic** flag was fully working — you can reset counts by clearing entries from the share analytics
- Review the Share Counts list monthly to identify your most-shared products and feature them more prominently on your homepage or in marketing emails
