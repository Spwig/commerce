---
slug: affiliate-tracking-links
title_i18n_key: Affiliate Tracking & Links
category: affiliates
component: affiliate
keywords:
  - affiliate tracking
  - tracking link
  - affiliate link
  - cookie tracking
  - attribution
  - click tracking
  - affiliate cookies
  - referral tracking
  - link statistics
  - conversion tracking
url_patterns:
  - /en/admin/affiliate/link/
  - /en/admin/affiliate/click/
related:
  - understanding-commissions
  - affiliate-program-overview
  - creating-affiliate-programs
published: true
---

Affiliate tracking powers the entire commission system by connecting customer purchases to the affiliates who referred them. This guide explains how tracking links work, what data Spwig records when customers click those links, and how the cookie-based attribution system determines which affiliate earns each commission.

Understanding tracking mechanics helps you troubleshoot attribution issues, analyze link performance, and educate your affiliates on how to maximize their conversions.

## What is a Tracking Link?

A tracking link is a unique URL that redirects customers to your store while recording the affiliate's identity in a cookie. Each affiliate can create multiple tracking links pointing to different destinations — the homepage, specific products, collection pages, or landing pages.

Example tracking link format:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

This link redirects to the destination while setting a tracking cookie that associates future purchases with the affiliate who owns link code `a2b7f8c4d1e9`.

Affiliates generate these links from their portal dashboard. They copy the full URL and share it in blog posts, social media, emails, or any channel where they reach potential customers.

## Tracking Link Components

Every tracking link contains these elements:

| Component | Example | Description |
|-----------|---------|-------------|
| **Base URL** | `https://yourstore.com` | Your store's domain |
| **Tracking Path** | `/affiliate/track/` | Spwig's tracking endpoint |
| **Link Code** | `a2b7f8c4d1e9` | Auto-generated 12-character unique identifier |
| **Destination** | Set when link is created | Where the customer lands after redirect (homepage, product, etc.) |

When an affiliate creates a link, Spwig generates the unique 12-character code automatically. The affiliate never needs to manually create or edit this code — they simply choose the destination and Spwig handles the rest.

### Link Labels (Optional)

Affiliates can add a label to each link for their own organization:
- "Instagram Bio Link"
- "YouTube Description"
- "Black Friday Email Campaign"

Labels help affiliates track which promotional channels perform best. They're visible only to the affiliate and you — customers never see the label.

## How Tracking Works

The tracking and attribution process follows five steps from click to commission:

### 1. Customer Clicks Link
A potential customer clicks the affiliate's tracking link from any promotional channel (social media post, blog article, email newsletter).

### 2. Click Recorded
Spwig's tracking endpoint records click details:
- IP address
- User agent (browser and device)
- HTTP referrer (where the click came from)
- Timestamp
- Session identifier

This data appears in the **Clicks** admin at **Affiliate > Clicks** for analytics and fraud detection.

### 3. Cookie Set
The tracking system sets a cookie in the customer's browser before redirecting them. The cookie contains:
- Affiliate ID (who should earn the commission)
- Program ID (which commission structure applies)
- Link code (which specific link was clicked)

### 4. Customer Purchases
The customer browses your store and completes a purchase. This can happen immediately or days/weeks later, as long as they purchase within the cookie lifetime window.

### 5. Commission Created
At checkout, Spwig checks for the affiliate cookie. If found and still valid (within cookie lifetime), the system creates a commission record with **Pending** status tied to the affiliate, program, and order.

## Cookie-Based Attribution

The tracking cookie is the core mechanism that links purchases to affiliates. Understanding how cookies work helps you set optimal attribution windows and troubleshoot tracking issues.

### Cookie Structure

| Property | Value |
|----------|-------|
| **Name** | `aff_{program_id}` (e.g., `aff_7` for program ID 7) |
| **Value** | JSON containing affiliate ID, link code, timestamp |
| **Domain** | Your store's domain |
| **Path** | `/` (site-wide access) |
| **Duration** | Program's cookie lifetime (1–365 days) |
| **HttpOnly** | `true` (prevents JavaScript access for security) |
| **SameSite** | `Lax` (allows tracking from external referrers) |
| **Secure** | `true` on HTTPS sites (recommended) |

### Cookie Lifetime Window

The cookie lifetime determines how long customers have to make a purchase after clicking an affiliate link. This window is set per program at **Marketing > Affiliate Programs** when you create or edit a program.

Industry standard cookie lifetimes:
- **7 days**: Quick-decision products (groceries, event tickets)
- **30 days**: Standard e-commerce (the most common setting)
- **60–90 days**: Considered purchases (furniture, electronics, B2B products)
- **365 days**: Long sales cycles (luxury goods, high-ticket services)

If a customer clicks an affiliate link on January 1 and your cookie lifetime is 30 days, any purchase they make through January 30 credits that affiliate. Purchases on January 31 or later don't generate a commission because the cookie expired.

### Last-Click Attribution Model

Spwig uses **last-click attribution**: the most recent affiliate link wins. Here's how that works:

**Scenario**: A customer clicks affiliate A's link on Monday, then clicks affiliate B's link on Wednesday, then purchases on Friday.

**Result**: Affiliate B earns the commission because their link was the most recent click.

The last-click cookie overwrites previous affiliate cookies. This model is simple to understand and prevents double-commissions, though it means only one affiliate gets credit per order (the last one before purchase).

## Click Recording

Spwig records every click on every affiliate link to provide analytics for both you and the affiliate. Click data helps measure link performance, detect fraud, and optimize promotional strategies.

### Data Captured Per Click

Navigate to **Affiliate > Clicks** to view all recorded clicks. Each entry contains:

| Field | Description |
|-------|-------------|
| **Link** | Which tracking link was clicked |
| **Affiliate** | Who owns the link |
| **IP Address** | Customer's IP (for fraud detection) |
| **User Agent** | Browser and device information |
| **Referrer** | The page where the customer clicked the link (e.g., "https://instagram.com") |
| **Session ID** | Unique identifier for this browsing session |
| **Timestamp** | Exact date and time of the click |

### Rate Limiting

To prevent click fraud and bot abuse, Spwig limits clicks to **100 per minute per IP address**. If the same IP exceeds this threshold, additional clicks are ignored and don't increment click counts.

This protection prevents malicious actors from inflating click stats without blocking legitimate traffic. Real customers almost never exceed 100 clicks per minute.

### Privacy Considerations

Click data contains IP addresses and user agents for fraud detection purposes. Ensure your privacy policy discloses that you track affiliate referrals and share anonymized performance data with affiliates.

## Viewing Affiliate Links

All affiliate-generated tracking links appear in your admin panel for monitoring and management.

### Accessing the Links List

Navigate to **Affiliate > Links** to view all tracking links across all affiliates and programs. The list view displays:

- **Link Code**: The unique 12-character identifier
- **Affiliate**: Who created the link
- **Program**: Which commission structure applies
- **Label**: Optional affiliate-provided description
- **Destination**: Where the link redirects customers
- **Total Clicks**: All-time click count
- **Active Status**: Whether the link is currently tracking

### Filtering Links

Use the admin filters to narrow the list:
- **By Affiliate**: See all links for a specific partner
- **By Program**: View links promoting a particular commission structure
- **By Active Status**: Find deactivated links

This filtering helps you analyze link distribution across your affiliate network and identify top-performing links.

## Link Statistics

Each tracking link accumulates performance metrics that help affiliates optimize their promotional strategies and help you identify your best-performing partners.

### Click on a link record to view detailed statistics:

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **Total Clicks** | All recorded clicks since link creation | Count of click records |
| **Clicks (7 days)** | Recent activity indicator | Clicks in last 7 days |
| **Conversions** | Orders attributed to this link | Count of commissions from this link code |
| **Conversion Rate** | Percentage of clicks that resulted in purchases | (Conversions ÷ Total Clicks) × 100 |
| **Total Revenue** | Sum of all order values from this link | Sum of order totals for converted clicks |

### Using Statistics for Optimization

**For Affiliates**: These numbers show which promotional channels work best. If an Instagram bio link has a 5% conversion rate but a blog post link has 15%, the affiliate should focus more on blog content.

**For Merchants**: Link statistics reveal which affiliates drive quality traffic. High click counts with low conversion rates suggest the affiliate's audience isn't a good fit for your products.

## Managing Links

You can manage affiliate links from the admin panel for maintenance and troubleshooting purposes.

### Deactivating Links

To prevent a specific link from tracking new clicks while preserving historical data:

1. Navigate to **Affiliate > Links**
2. Click the link you want to deactivate
3. Uncheck **Active**
4. Click **Save**

Deactivated links still redirect customers to the destination, but they don't set tracking cookies or record clicks. This is useful when an affiliate is running a temporary campaign or you need to disable a specific promotional channel.

### Editing Link Details

You can modify:
- **Label**: Update the affiliate-provided description
- **Destination**: Change where the link redirects (useful if you move a product page)
- **Active status**: Enable or disable tracking

You cannot edit the link code — it's permanent and tied to all historical click and commission data.

### Deleting Inactive Links

Delete links that are no longer in use and have no historical clicks or conversions. This keeps your link list clean without losing valuable analytics data.

**Warning**: Deleting a link removes all associated click records. Only delete links with zero clicks or when you're absolutely certain you don't need the historical data.

## Attribution Model

Understanding Spwig's attribution logic helps you set expectations with affiliates and troubleshoot commission disputes.

### Last-Click Attribution

As mentioned earlier, Spwig uses last-click attribution: if a customer clicks multiple affiliate links before purchasing, only the most recent affiliate earns a commission.

**Pros**:
- Simple to understand and explain
- Prevents double-commissions
- Rewards affiliates who close the sale

**Cons**:
- Earlier affiliates who introduced the customer get no credit
- Doesn't reflect multi-touch customer journeys
- May incentivize "link hijacking" (affiliates targeting high-intent customers who were already referred by someone else)

### Cookie Lifetime Determines Eligibility

Only purchases within the cookie lifetime window generate commissions. If the cookie expires before checkout, no commission is created even if the customer returns through a bookmark.

**Example**: 30-day cookie lifetime
- Customer clicks link January 1 → Cookie set, expires January 31
- Customer purchases January 25 → Commission created
- Customer purchases February 5 → No commission (cookie expired)

### Session Tracking

In addition to the cookie, Spwig tracks the session ID for each click. This enables multi-visit attribution within the same session even if cookies are blocked or cleared.

If a customer clicks a link, browsing your store triggers multiple page loads, and then they purchase — all in the same session — the affiliate gets credit even without a persistent cookie.

## Troubleshooting

Common tracking issues and how to resolve them:

### Link Not Tracking Clicks

**Symptoms**: Click count stays at zero despite affiliate reports of sharing the link.

**Causes and fixes**:
1. **Link is deactivated**: Check the **Active** status in the link detail page
2. **Program is inactive**: Navigate to **Affiliate > Programs** and verify the program status is **Active**
3. **Affiliate account is deactivated**: Check the affiliate's account status at **Affiliate > Affiliates**
4. **Rate limiting**: Check if the same IP is generating excessive clicks (bot traffic)

### Low Conversion Rate

**Symptoms**: High click counts but very few orders attributed.

**Causes and fixes**:
1. **Cookie lifetime too short**: Increase the program's cookie lifetime if your products require research and consideration
2. **Destination page quality**: Check the landing page — is it mobile-friendly? Does it load quickly? Is the product in stock?
3. **Audience mismatch**: The affiliate's audience may not be the right fit for your products
4. **Browser blocking cookies**: Some privacy tools block third-party cookies, though Spwig uses first-party cookies which are less likely to be blocked

### Duplicate Click Records

**Symptoms**: Same customer generates multiple click records in rapid succession.

**Cause**: This is normal behavior. Each page load of the tracking link creates a click record. If a customer clicks, the page loads slowly, and they click again, you'll see multiple records.

**Fix**: No action needed. The rate limiter prevents abuse (100 clicks/minute/IP), and duplicate clicks from the same session don't affect attribution — only one cookie is set.

## Tips

- **Test tracking before launch** — Create a test affiliate account, generate a tracking link, click it in an incognito browser, and complete a test purchase. Verify the commission appears with the correct affiliate attribution.
- **Educate affiliates on cookie lifetime** — Make sure affiliates understand they only earn commissions on purchases within the cookie window. This helps them set realistic expectations and focus on high-intent traffic.
- **Monitor click patterns for fraud** — Unusually high click counts from a single IP or clicks with no user agent string may indicate bot traffic. Review these affiliates carefully before approving commissions.
- **Use link labels consistently** — Encourage affiliates to label their links by channel (Instagram, Blog, Email) so you can both analyze which promotional channels drive the best conversions.
- **Consider longer cookie lifetimes for high-ticket products** — If your average order value is high and customers typically research before buying, extend the cookie lifetime to 60–90 days to capture those delayed conversions.
- **Check referrer data for channel insights** — The referrer field shows where clicks originate. If you see lots of clicks from "instagram.com" or "youtube.com", you know which social platforms your affiliates use most effectively.
