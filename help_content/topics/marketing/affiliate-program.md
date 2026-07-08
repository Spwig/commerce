---
slug: affiliate-program
title_i18n_key: Affiliate Program
category: affiliates
component: affiliate
keywords:
  - affiliate
  - affiliate program
  - commission
  - referral
  - affiliate link
  - payout
  - affiliate portal
  - referral tracking
  - affiliate code
url_patterns:
  - /admin/affiliate/affiliateprogram/
  - /admin/affiliate/affiliate/
  - /admin/affiliate/commission/
related:
  - store-settings
published: true
---

The affiliate program lets you recruit partners who promote your products and earn commissions on the sales they generate. Affiliates share unique referral links, and Spwig automatically tracks clicks, attributes orders, and calculates commissions.

![Affiliate programs](/static/core/admin/img/help/affiliate-program/program-list.webp)

## How It Works

1. You create one or more **affiliate programs** with commission rates and rules
2. Affiliates **sign up** through a public portal or are added manually
3. Each affiliate gets a **unique referral link** with a tracking code
4. When a customer clicks the link and makes a purchase, a **commission** is recorded
5. You review and approve commissions, then process **payouts**

## Creating a Program

Navigate to **Marketing > Affiliate Programs** and click **Add Program**.

### Program Settings

| Setting | Description |
|---------|-------------|
| **Name** | Program name visible to affiliates (e.g., "Partner Program") |
| **Commission Type** | **Percentage** of order total or **Fixed** amount per sale |
| **Commission Rate** | The percentage or fixed amount affiliates earn |
| **Cookie Lifetime** | How many days the referral tracking cookie lasts (default: 30 days) |
| **Minimum Payout** | Minimum earnings before an affiliate can request a payout |
| **Auto-Approve Affiliates** | Automatically accept new affiliate applications, or require manual approval |
| **Status** | Active, paused, or closed |

### Commission Types

- **Percentage** — Affiliates earn a percentage of each referred order's subtotal (e.g., 10% of a $100 order = $10 commission)
- **Fixed** — Affiliates earn a flat amount per sale regardless of order value (e.g., $5 per sale)

## Managing Affiliates

Navigate to **Marketing > Affiliates** to view and manage affiliate accounts.

### Affiliate Details

Each affiliate has:
- **Affiliate Code** — A unique code used in referral URLs (auto-generated or custom)
- **Referral Link** — The full tracking URL the affiliate shares (e.g., `yourstore.com/?ref=CODE`)
- **Status** — Pending, approved, or rejected
- **Payment Method** — How the affiliate receives payouts (PayPal or bank transfer)
- **Program Membership** — Which programs the affiliate belongs to

### Adding Affiliates Manually

1. Click **Add Affiliate**
2. Select an existing customer account or create a new one
3. Assign the affiliate to one or more programs
4. Set the affiliate code (or leave blank to auto-generate)

### Affiliate Portal

Affiliates access a public-facing portal where they can:
- View their dashboard with earnings and click statistics
- Copy their referral links
- Track commission history
- Request payouts

The portal URL is automatically available at `/affiliate/` on your store.

## Tracking and Commissions

### How Tracking Works

1. A customer clicks an affiliate's referral link
2. A tracking cookie is set in the customer's browser (lasting the configured cookie lifetime)
3. If the customer places an order within the cookie lifetime, the order is attributed to the affiliate
4. A commission record is created with status **Pending**

### Commission Statuses

| Status | Description |
|--------|-------------|
| **Pending** | Commission recorded, awaiting review |
| **Approved** | Verified and ready for payout |
| **Rejected** | Commission denied (e.g., fraudulent order or returned item) |
| **Paid** | Commission included in a completed payout |

### Reviewing Commissions

Navigate to **Marketing > Commissions** to review pending commissions:

1. Check the order details to verify the sale is legitimate
2. Click **Approve** to confirm, or **Reject** with a reason
3. Approved commissions accumulate toward the affiliate's payout balance

## Payouts

When an affiliate's approved commission balance reaches the minimum payout threshold, you can process a payout.

### Processing Payouts

1. Navigate to **Marketing > Payouts**
2. Select affiliates with available balances
3. Choose the payment method:
   - **PayPal** — Send funds directly to the affiliate's PayPal email
   - **Bank Transfer** — Record a manual bank transfer
4. Confirm and process the payout
5. The payout status updates to **Completed** and commissions are marked as **Paid**

### Payout Providers

Spwig integrates with payment providers for automated payouts:
- **PayPal** — Automated mass payouts via PayPal API
- **Airwallex** — International payouts with competitive exchange rates
- **Manual** — Record payouts processed outside of Spwig

## Referral Links

Each affiliate's referral link follows this pattern:

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Affiliates can also create links to specific products or categories:

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

The `ref` parameter works on any page — the tracking cookie is set regardless of the landing page.

## Program Analytics

The affiliate program dashboard shows:
- **Total Clicks** — How many times referral links have been clicked
- **Total Orders** — Orders attributed to affiliates
- **Total Commissions** — Sum of all commissions (pending, approved, and paid)
- **Active Affiliates** — Number of approved affiliates currently generating referrals

## Tips

- Start with a **percentage-based commission** (5–15%) — it scales naturally with order value and is easy for affiliates to understand.
- Set a **30-day cookie lifetime** as a baseline — this gives customers time to return and complete their purchase while still attributing the sale to the affiliate.
- Enable **auto-approve** for public programs to reduce friction, or use manual approval for invite-only programs where you want to vet each affiliate.
- Set a reasonable **minimum payout** (e.g., $25–$50) to avoid processing many small transactions.
- Customize the **affiliate portal** to match your brand — affiliates are more likely to promote your store when the experience feels professional.
- Monitor commissions regularly for **fraudulent patterns** such as self-referrals, unusually high return rates, or suspicious click volumes.
