---
slug: product-reviews
title_i18n_key: Product Reviews
category: products
component: catalog
keywords:
  - product reviews
  - customer reviews
  - approve review
  - reject review
  - review moderation
  - reviews dashboard
  - star rating
  - verified purchase
  - review management
  - customer feedback
  - review approval
  - helpful count
  - review images
  - customer journey
related:
  - add-product
  - product-collections
  - product-brands
url_patterns:
  - /admin/catalog/productreview/
  - /admin/catalog/productreview/dashboard/
published: true
---

Product reviews let customers rate and write about their experience with a product. Reviews you approve appear on the product page in your storefront, where they help other shoppers decide what to buy. Spwig gives you full control over which reviews go live — nothing is published until you approve it.

Reviews live under **Products > Reviews** in the sidebar, which opens as a group: the top link takes you to the **Reviews Dashboard**, and **Moderate Reviews** takes you straight to the review list.

## The Reviews Dashboard

Navigate to **Products > Reviews** to open the dashboard — a single-screen overview of how reviews are performing across your store.

![Reviews Dashboard](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

At the top, six KPI cards summarise your review activity:

| Card | What it shows |
|---|---|
| **Total Reviews** | All reviews ever submitted, approved or not |
| **Average Rating** | The mean star rating across every review |
| **Pending Moderation** | Reviews waiting for your approval or rejection |
| **Approval Rate** | The share of all reviews you've approved |
| **Verified Purchases** | The share of reviews left by customers with a confirmed order for that product |
| **New (30 days)** | Reviews submitted in the last 30 days |

Below the KPIs, three charts give you more detail:

- **Rating Distribution** — a bar chart of how many reviews fall into each star rating (1–5). A cluster of 1-star reviews here is worth investigating immediately.
- **Review Volume (12 weeks)** — a line chart of review counts week by week, so you can spot spikes after a promotion or a drop-off that needs attention.
- **Reviewers' Purchase Channel** — a donut chart of the marketing channel (direct, email, paid search, organic social, and so on) that drove the *purchase* behind each review. This reuses your attribution data and is genuinely useful for seeing which channels bring in customers who go on to leave reviews — but it is **not** a record of how the customer found the review form itself. Spwig doesn't track that separately; see "What the journey does and doesn't tell you" further down this guide.

Two lists round out the dashboard:

- **Top Reviewed Products** — your most-reviewed products, each with its review count and average rating, linking straight to the product.
- **Awaiting Moderation** — your most recent pending reviews, so you can jump directly into anything that needs a decision without leaving the dashboard.

## The review list

Click **Moderate Reviews** (or **Products > Reviews > Moderate Reviews**) to see every review as a card, with filters above the list.

![Product Reviews list with filters and pending review cards](/static/core/admin/img/help/product-reviews/review-list.webp)

Each card shows the product thumbnail, review title, star rating, an **Approved**/**Pending** badge, a **Verified Purchase** badge when it applies, a preview of the comment, and who wrote it and when.

### Filtering reviews

Use the filters panel to narrow the list:

- **Search** — matches product name, customer username, or review title
- **Rating** — show only reviews with a specific star rating (useful for investigating 1-star complaints)
- **Approval** — quickly separate approved from pending reviews
- **Verified** — filter to reviews from customers with a confirmed order for that product

Filtering runs instantly without reloading the page.

## Approving and rejecting reviews

Reviews are not visible on your storefront until you approve them. You can approve or reject reviews individually or in bulk.

### Bulk actions

1. In the review list, tick the checkboxes next to the reviews you want to act on
2. Select **Approve selected reviews** or **Reject selected reviews** from the action dropdown
3. Click **Go**

This is the fastest way to work through a batch of new reviews.

### Individual review

1. Click the edit icon on a review card, or its title, to open the review
2. On the **Review** tab, check or uncheck **Is approved**
3. Click the checkmark button in the header to save

## The review edit page

Opening a review gives you a dashboard-style view built around that one review — a header with the product name, the star rating, an **Approved**/**Pending** badge, a **Verified Purchase** badge when it applies, who wrote the review and when, and a stats row (**Rating**, **Helpful Votes**, **Customer Orders**, **Lifetime Spend**). Below that, the detail is organised into four tabs.

![Review edit page — Review tab with image gallery](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Review tab

This is where you moderate the review itself:

- **Review Images** — if the customer attached photos, they appear here as a thumbnail gallery; click any thumbnail to open the full-size image in a new tab. Photo reviews are a strong trust signal for shoppers, so this is worth a glance before you approve.
- **Rating**, **Title**, **Comment** — the content the customer submitted
- **Is approved** — controls whether the review is visible on your storefront
- **Is verified purchase** — flags the review as coming from a confirmed buyer; Spwig sets this automatically when a fulfilled order for the product exists (see the **Purchase** tab), but you can override it here if needed
- **Images** — the underlying list of image URLs behind the gallery above; you don't normally need to touch this, but it stays editable for edge cases (for example, removing one photo from a multi-image review)

You cannot edit the review's wording — approving or rejecting, and managing images, is the extent of what you control here.

### Customer & Journey tab

![Review edit page — Customer & Journey tab](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

This tab gives you context on who left the review: total orders, how many reviews they've written, their average rating given, how long they've been a customer, and their contact details, with a link to open their full customer record.

Below that sits the **Traffic-source journey** — the channels, campaigns, and referrers that brought this customer to your store, pulled from your attribution data and shown as a timeline.

#### What the "journey" does and doesn't tell you

Read this timeline as the customer's **arrival and purchase journey** — how they originally found your store and went on to buy. It is **not** a record of the visit in which they wrote this review. Spwig does not track where a customer was, or what device or session they used, at the moment they submitted a review. If the timeline shows "Email > summer-skincare" three weeks before the review date, that tells you the email campaign likely drove the *purchase* — it says nothing about whether the customer came back from a search result, a bookmark, or a follow-up email to actually leave the review. Treat this tab as useful marketing context, not as a literal trace of the review submission.

### Purchase tab

![Review edit page — Purchase tab](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

This tab lists every order in which the customer bought the reviewed product — order number, date, total, status, and the purchase channel for that order. If any of those orders has reached a fulfilled status (shipped or delivered), you'll see a confirmation note that this is a verified purchase — the same signal that sets **Is verified purchase** automatically on the Review tab.

If no matching order appears here, the reviewer either bought the product before your store tracked orders in Spwig, or they never actually purchased it — worth knowing before you decide how much weight to give the review.

### Advanced tab

Metadata you rarely need to touch: **Helpful Count** (how many customers marked the review as helpful), import provenance if the review was migrated from another platform, and the created/updated timestamps.

## Tips

- Check the **Awaiting Moderation** list on the dashboard first thing — it's the fastest way to see what needs a decision without opening the full review list
- A cluster of 1-star reviews on the same product in the **Rating Distribution** chart is a clear signal to investigate packaging, product quality, or your listing copy
- Use the **Verified** filter when deciding how to handle borderline reviews — feedback from customers with a confirmed order carries more weight in any dispute
- Approve reviews promptly, including critical ones — a visible negative review paired with no response can look worse than a handled complaint, and slow-to-appear reviews discourage customers from leaving future feedback
- Don't over-read the **Traffic-source journey** or the dashboard's **Reviewers' Purchase Channel** chart — both describe how the customer arrived and purchased, not how they arrived to write the review
- Reviews with photos are worth a closer look before approving; product photos from real customers are some of the most persuasive content on your storefront
