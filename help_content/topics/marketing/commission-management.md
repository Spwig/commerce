---
slug: commission-management
title_i18n_key: Commission Management
category: affiliates
component: affiliate
keywords:
  - commission management
  - approve commission
  - reject commission
  - commission review
  - pending commission
  - commission approval
  - commission notes
  - bulk commission approval
  - commission workflow
  - reviewing commissions
url_patterns:
  - /en/admin/affiliate/commission/
  - /en/affiliate/merchant/
related:
  - understanding-commissions
  - payout-processing
  - affiliate-program-overview
published: true
---

Commission management is the process of reviewing and approving affiliate earnings to ensure only legitimate sales are credited. This guide shows you how to review pending commissions, approve valid ones, reject fraudulent or returned orders, and manage commissions efficiently using bulk actions.

## Commission Dashboard

Navigate to **Marketing > Commissions** to access the commission management dashboard.

The dashboard provides an overview of commission activity across all affiliate programs:

| Statistic | Description |
|-----------|-------------|
| **Pending Commissions** | Number of commissions awaiting your review |
| **Approved Commissions** | Commissions confirmed and ready for payout |
| **Paid Commissions** | Commissions that have been paid to affiliates |
| **Rejected Commissions** | Commissions declined due to fraud, returns, or policy violations |
| **Pending Payout Amount** | Total value of approved but unpaid commissions |

These statistics help you track your review workload and monitor the financial impact of your affiliate program.

![Commission Dashboard](/static/core/admin/img/help/commission-management/commission-dashboard.webp)

## Viewing Commissions

The commission list displays all commission records in chronological order.

### List Columns

| Column | Description |
|--------|-------------|
| **Affiliate** | Affiliate's name and unique code |
| **Program** | The affiliate program that generated this commission |
| **Order** | Order number (click to view full order details) |
| **Amount** | Commission value in your store's currency |
| **Status** | Pending, Approved, Rejected, or Paid |
| **Created** | When the commission was generated |

### Filtering Commissions

Use the filter sidebar to narrow down commissions:

- **By Status** — Show only pending, approved, rejected, or paid commissions
- **By Affiliate** — View commissions for a specific partner
- **By Program** — See commissions from a particular affiliate program
- **By Date Range** — Filter by creation date

### Searching Commissions

Use the search bar to find specific commissions:

- Enter an **order number** to find a commission for a specific sale
- Enter an **affiliate code** to see all commissions for one partner

## Commission Details

Click any commission in the list to view its full details.

### Detail Fields

The detail view shows:

- **Order Information** — Click the order number to view the complete order in a new tab, including items, shipping address, payment status, and customer details
- **Affiliate Information** — Affiliate's name, code, payment email, and program membership status
- **Program Details** — Program name, commission type (percentage or fixed), and commission rate
- **Timestamps** — Created date, approved/rejected date, and paid date
- **Notes Section** — Internal notes visible only to merchants (explained below)

This information helps you verify the legitimacy of the commission before approving it.

## Approving Commissions

Approving a commission confirms it is valid and adds it to the affiliate's available balance, making it eligible for payout.

### When to Approve

Approve commissions when:

- **Order fulfilled successfully** — Product shipped or digital goods delivered
- **No returns or refunds** — Customer has not requested a return (consider waiting 14-30 days after fulfillment)
- **Quality standards met** — Sale meets your program's terms (e.g., not a self-referral, customer used genuine payment method)
- **No fraud detected** — Order passes fraud screening (check IP, billing/shipping address mismatch, unusual order patterns)

### How to Approve

**Single Commission Approval:**

1. Navigate to **Marketing > Commissions**
2. Click the commission you want to approve
3. Click the **Approve** button at the top of the detail page
4. Optionally add a note (e.g., "Approved after successful delivery")
5. The status changes to **Approved** and the commission is added to the affiliate's balance

**Bulk Approval:**

1. Navigate to **Marketing > Commissions**
2. Check the boxes next to commissions you want to approve
3. Select **Approve Selected** from the **Actions** dropdown
4. Click **Go**
5. All selected commissions change to **Approved** status

Approved commissions appear in the affiliate's dashboard as available balance and can be included in the next payout batch.

## Rejecting Commissions

Rejecting a commission removes it from the affiliate's balance and marks it as ineligible for payout.

### When to Reject

Reject commissions when:

- **Fraudulent order** — Order shows signs of fraud (stolen payment method, IP mismatch, affiliate using their own link)
- **Customer returned product** — Customer returned items for a full refund
- **Quality issues** — Sale does not meet program terms (e.g., affiliate violated advertising guidelines)
- **Terms violation** — Affiliate used prohibited promotion methods (spam, trademark bidding, cookie stuffing)
- **Order cancelled** — Customer cancelled before fulfillment

### How to Reject

**Single Commission Rejection:**

1. Navigate to **Marketing > Commissions**
2. Click the commission you want to reject
3. Click the **Reject** button at the top of the detail page
4. **Add a note** explaining the reason (highly recommended for dispute resolution)
5. The status changes to **Rejected**

**Bulk Rejection:**

1. Navigate to **Marketing > Commissions**
2. Check the boxes next to commissions you want to reject
3. Select **Reject Selected** from the **Actions** dropdown
4. Click **Go**
5. All selected commissions change to **Rejected** status

Rejected commissions are removed from the affiliate's balance and cannot be paid. They remain visible in the commission history for record-keeping.

## Bulk Actions

Bulk actions allow you to approve or reject multiple commissions at once, saving time when processing large batches.

### Using Bulk Actions

1. Navigate to **Marketing > Commissions**
2. Filter the list to show only the commissions you want to process (e.g., filter by status **Pending**)
3. Check the box next to each commission, or click the header checkbox to select all on the current page
4. Choose an action from the **Actions** dropdown:
   - **Approve Selected** — Mark all selected commissions as approved
   - **Reject Selected** — Mark all selected commissions as rejected
5. Click **Go**
6. Review the confirmation message showing how many commissions were updated

### Efficient Bulk Processing

- **Filter by program** — Approve all commissions from a trusted high-performing affiliate at once
- **Filter by date range** — Process commissions older than 14 days (past your return window)
- **Review high-value separately** — Use bulk actions for small commissions, manually review large ones

## Commission Notes

The notes field allows you to document your decisions and communicate with your team.

### Adding Notes

Notes can be added:

- **During approval** — Click the commission, add a note in the Notes field, then click **Approve**
- **During rejection** — Add a note explaining the rejection reason
- **Anytime** — Click the commission, add or edit the note in the Notes field, and save

### When to Use Notes

- **Rejected commissions** — Always document the reason ("Customer returned order #12345 on 2/10/26")
- **High-value commissions** — Note verification steps taken ("Verified delivery via tracking #ABC123")
- **Disputed commissions** — Document communication with the affiliate
- **Fraud patterns** — Note suspicious activity for future reference

Notes are **internal only** — affiliates cannot see them. They serve as your record-keeping tool.

## Commission Flow

Here's the complete commission management workflow:

```
Order Placed → Commission Created (Pending)
                      ↓
              Merchant Reviews
                      ↓
                ┌─────┴─────┐
                ↓           ↓
            Approved     Rejected
                ↓           ↓
        Ready for Payout  Not Payable
                ↓
        Included in Payout
                ↓
              Paid
```

**Timeline Example:**

- **Day 1:** Customer places $100 order via affiliate link → $10 commission created (Pending)
- **Day 15:** Order fulfilled and return window passed → Merchant approves commission
- **Day 20:** Merchant processes monthly payout batch → Commission status changes to Paid
- **Day 21:** Affiliate receives payment via PayPal

## Best Practices

### Review Window

Establish a consistent review schedule:

- **Daily reviews** — Process pending commissions every morning (recommended for high-volume programs)
- **Weekly reviews** — Set aside time each Monday to approve the previous week's commissions
- **Bi-weekly reviews** — Align with your payout schedule (approve commissions mid-month, process payouts end-of-month)

### Quality Assurance Checks

Before approving commissions, verify:

1. **Order is fulfilled** — Check order status in admin
2. **Payment is confirmed** — Verify payment method processed successfully
3. **Return window passed** — Wait 14-30 days after delivery to account for returns
4. **No fraud flags** — Review order for suspicious patterns (mismatched addresses, high-risk countries, multiple orders from same IP)
5. **Affiliate in good standing** — Check affiliate's history for previous fraud or violations

### Fraud Prevention

Watch for these red flags:

- **Self-referrals** — Affiliate placing orders using their own tracking link
- **Cookie stuffing** — Abnormally high click-to-conversion ratio with low order values
- **Duplicate orders** — Multiple orders from the same customer/IP via the same affiliate link
- **Geolocation mismatches** — Affiliate in Country A driving sales exclusively in Country B
- **Chargebacks** — High chargeback rate on affiliate-referred orders

If you detect fraud, **reject the commissions** and consider terminating the affiliate's program membership.

### Communication with Affiliates

- **Set expectations** — Clearly document your commission approval policy in the program terms
- **Be transparent** — If you reject commissions, consider sending the affiliate an email explaining why (use notes as reference)
- **Respond to disputes** — If an affiliate questions a rejection, review the notes and order details
- **Publish guidelines** — Create a "Commission Approval Policy" page on your affiliate portal to avoid confusion

## Tips

- Approve commissions **after your return window closes** (typically 14-30 days) to avoid approving orders that customers later return
- Use **bulk actions with filters** to efficiently process commissions from trusted affiliates while manually reviewing new or high-risk partners
- Document rejection reasons in the **notes field** — this protects you if an affiliate disputes the decision and helps you identify patterns
- Watch for **self-referrals** — it's a common violation where affiliates use their own links to earn commissions on personal purchases
- Set a **minimum approval threshold** — for example, auto-approve commissions under $10 but manually review anything over $50 to balance efficiency with risk
- Create a **fraud checklist** — standardize your review process with a list of red flags (IP mismatches, suspicious order patterns, high-risk payment methods)
- Monitor **rejection rates by affiliate** — if one affiliate has many rejections, it may indicate fraud or a need for additional training on program terms

