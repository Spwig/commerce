---
slug: affiliate-program-overview
title_i18n_key: Affiliate Program Overview
category: affiliates
component: affiliate
keywords:
  - affiliate program
  - affiliate marketing
  - partner program
  - commission tracking
  - referral program
  - what is affiliate program
  - affiliate dashboard
  - affiliate overview
url_patterns:
  - /en/affiliate/merchant/
  - /en/admin/affiliate/program/
related:
  - affiliate-program
published: true
---

The Spwig affiliate program feature lets you recruit partners who promote your products in exchange for commissions. This marketing channel extends your reach through influencers, bloggers, content creators, and brand ambassadors who share unique tracking links with their audiences. When someone clicks an affiliate's link and makes a purchase, the affiliate earns a commission and you gain a customer.

This overview explains what the affiliate program is, who it's for, and how merchants use it to build a partner network that drives sales.

![Merchant Dashboard](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Key Concepts

Understanding these core terms will help you configure and manage your affiliate program:

| Term | Definition |
|------|------------|
| **Affiliate** | A partner who promotes your products and earns commissions on referred sales |
| **Program** | A commission structure with rates, rules, and settings (you can create multiple programs) |
| **Tracking Link** | A unique URL containing the affiliate's code (e.g., `yourstore.com/?ref=CODE`) |
| **Commission** | The payment an affiliate earns for a referred sale, calculated based on the program rules |
| **Cookie Lifetime** | How long (in days) the tracking cookie persists after a customer clicks an affiliate link |
| **Payout** | A bulk payment that settles multiple approved commissions at once |
| **Merchant Dashboard** | Your admin interface for managing programs, affiliates, commissions, and payouts |
| **Affiliate Portal** | The public-facing dashboard where affiliates view earnings, get tracking links, and request payouts |

## How It Works

The affiliate workflow follows four main stages:

### 1. Apply
Affiliates discover your program and submit applications through the public affiliate portal at `/affiliate/` on your store. You can enable **auto-approval** for open programs or **manual review** for invite-only partnerships.

### 2. Approve
You review pending applications in **Marketing > Affiliates**. Check each applicant's website, social media presence, and audience fit before approving. Once approved, the affiliate receives login credentials and can access their dashboard.

### 3. Promote
Approved affiliates get unique referral links from their portal. They share these links in blog posts, social media, email newsletters, or wherever they connect with their audience. Spwig sets a tracking cookie when someone clicks the link.

### 4. Earn
When a referred customer completes a purchase within the cookie lifetime, Spwig creates a commission record. You review and approve commissions in **Marketing > Commissions**, then process payouts when affiliates reach the minimum payout threshold.

## Merchant Workflow Overview

As the merchant, you manage the entire program lifecycle from your admin panel:

### Creating Programs
Start by creating one or more affiliate programs at **Marketing > Affiliate Programs**. Each program has its own commission structure, cookie lifetime, and approval settings. You might create separate programs for influencers (higher commission) versus general partners (lower commission).

### Reviewing Applications
New affiliate applications appear at **Marketing > Affiliates** with a **Pending** status. Review each application to verify the partner is a good fit for your brand. Approve to activate their account or reject with a reason.

### Approving Commissions
When affiliates generate sales, commissions appear at **Marketing > Commissions** with a **Pending** status. Review the linked order to verify it's legitimate (not a self-referral, not a returned order), then approve or reject accordingly.

### Processing Payouts
Once affiliates accumulate approved commissions above your minimum payout threshold, process bulk payouts at **Marketing > Payouts**. Spwig integrates with PayPal and Airwallex for automated payouts, or you can record manual bank transfers.

## Affiliate Workflow Overview

Understanding how affiliates experience your program helps you design better onboarding and support:

### Apply
Affiliates visit your affiliate portal, read the program details (commission rate, cookie lifetime, payout terms), and submit an application with their contact info and promotional channels.

### Create Links
After approval, affiliates log into their dashboard to generate tracking links. They can create generic store links or links to specific products/categories they want to promote.

### Promote
Affiliates share their tracking links wherever they connect with potential customers — blog posts, YouTube videos, Instagram stories, email newsletters, or comparison sites.

### Request Payouts
Affiliates track their earnings in real time through the affiliate portal dashboard. When their approved balance reaches the minimum payout threshold, they can request a payout.

## Where to Find Each Feature

| Feature | Admin Location | Description |
|---------|---------------|-------------|
| **Programs** | Marketing > Affiliate Programs | Create and configure commission structures |
| **Affiliates** | Marketing > Affiliates | Review applications, manage affiliate accounts |
| **Commissions** | Marketing > Commissions | Review and approve pending commissions |
| **Payouts** | Marketing > Payouts | Process bulk payments to affiliates |
| **Settings** | Marketing > Affiliate Settings | Global settings, payout providers, portal customization |
| **Dashboard** | Marketing > Affiliate Dashboard | Analytics overview with clicks, orders, and commission totals |

The affiliate-facing portal is automatically available at `/affiliate/` on your store's public URL.

## Common Use Cases

Here are four proven ways merchants use the Spwig affiliate program to grow their business:

### Influencer Partnerships
Partner with social media influencers who have engaged audiences in your niche. Offer higher commission rates (15–20%) to attract quality influencers who can drive significant traffic. Use tracking links to measure ROI for each partnership.

### Brand Ambassadors
Build a network of loyal customers who become brand advocates. Offer these repeat customers affiliate accounts so they can earn commissions when they refer friends and family. This works especially well for niche products with passionate communities.

### Content Creators
Recruit bloggers, YouTubers, and podcasters who create buying guides, reviews, or comparison content. Affiliates with evergreen content can generate consistent referrals month after month.

### Referral Networks
Allow existing customers to join your program and earn commissions by sharing products they love. This creates a viral loop where satisfied customers become promoters, bringing in new customers who may also become affiliates.

## Tips

- **Start with one program** — Create a general partner program with a 10% commission rate and 30-day cookie lifetime. You can add specialized programs later once you understand which partners perform best.
- **Set clear expectations** — Document your approval process, commission timelines, and payout schedule in the affiliate portal. Transparency builds trust and reduces support requests.
- **Monitor for fraud** — Review commissions carefully for red flags like self-referrals (affiliates buying from their own links), unusually high return rates, or suspicious click patterns. Reject fraudulent commissions immediately.
- **Communicate regularly** — Send monthly updates to your affiliates with program news, promotional calendar highlights, and top performer recognition. Active communication keeps affiliates engaged and promoting.
- **Optimize for mobile** — Most affiliates share links on social media where the majority of clicks come from mobile devices. Test your checkout flow on phones to ensure a smooth experience for referred customers.
- **Provide creative assets** — Make it easy for affiliates to promote your products by providing banner images, product photos, and pre-written copy they can use in their content.
