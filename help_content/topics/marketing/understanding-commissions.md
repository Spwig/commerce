---
slug: understanding-commissions
title_i18n_key: Understanding Commissions
category: affiliates
component: affiliate
keywords:
  - commission
  - affiliate commission
  - commission calculation
  - commission lifecycle
  - pending commission
  - approved commission
  - commission tracking
  - commission status
url_patterns:
  - /en/admin/affiliate/commission/
related:
  - creating-affiliate-programs
  - commission-management
  - payout-processing
published: true
---

Commissions are earnings records created when an affiliate successfully drives a sale to your store. Each commission is tied to a specific order, affiliate, and program, and moves through a lifecycle from pending to paid. This guide explains how commissions work, how they're calculated, and how to manage them effectively.

## What is a Commission?

A commission represents the amount owed to an affiliate for referring a customer who completed a purchase. When a customer clicks an affiliate's referral link and places an order within the cookie lifetime window, Spwig automatically creates a commission record.

Each commission contains:
- **Affiliate** — The partner who referred the customer
- **Program** — The affiliate program that defines the commission rules
- **Order** — The order that generated the commission
- **Amount** — The calculated commission value
- **Status** — The current stage in the commission lifecycle
- **Dates** — Created date, approved/rejected date, and paid date

## Commission Calculation

Commissions are calculated automatically based on the program's commission type and rate.

| Commission Type | Calculation | Example |
|-----------------|-------------|---------|
| **Percentage** | Order Total × Commission % ÷ 100 | Order: $200, Rate: 10% → **$20 commission** |
| **Fixed** | Flat amount per order | Rate: $15 → **$15 commission** (regardless of order value) |

### Calculation Examples

**Percentage Commission (10%)**:
- Customer places a $50 order → $5 commission
- Customer places a $150 order → $15 commission
- Customer places a $300 order → $30 commission

**Fixed Commission ($20)**:
- Customer places a $50 order → $20 commission
- Customer places a $150 order → $20 commission
- Customer places a $300 order → $20 commission

The commission is calculated on the **order subtotal** (before shipping and taxes) and is created immediately when the order is placed.

## Commission Lifecycle

Every commission moves through a series of statuses from creation to payout:

```
Pending → Approved → Paid
   ↓
Rejected
```

### Status Definitions

| Status | Description | What Happens |
|--------|-------------|--------------|
| **Pending** | Order placed, commission awaiting review | Commission is created but not yet confirmed. Affiliate can see it but cannot withdraw funds. |
| **Approved** | Merchant confirms the sale is valid | Commission is verified and added to the affiliate's available balance. Eligible for payout. |
| **Rejected** | Merchant declines the commission | Commission is denied (e.g., order was refunded, fraudulent, or violated terms). Not eligible for payout. |
| **Paid** | Commission included in a completed payout | Affiliate has been paid. Commission is finalized and cannot be modified. |

![Commission List](/static/core/admin/img/help/commission-management/commission-list.webp)

## When Commissions Are Created

Commissions are created automatically following this sequence:

1. **Customer clicks affiliate link** — The referral URL contains the affiliate's unique tracking code (e.g., `?ref=JOHNSMITH`)
2. **Cookie is set** — A tracking cookie is stored in the customer's browser with the affiliate code
3. **Purchase within cookie lifetime** — Customer completes an order before the cookie expires (default: 30 days)
4. **System attributes the order** — Spwig checks for an active tracking cookie and identifies the referring affiliate
5. **Commission auto-created** — A commission record is generated with status **Pending**

The commission is created **immediately** when the order is placed, even before payment is confirmed. This allows merchants to review commissions while orders are being processed.

## Tracking & Attribution

Spwig uses **last-click attribution** to determine which affiliate should receive credit for a sale.

### How Attribution Works

- **Last-click model** — The most recent affiliate link clicked gets credit (even if multiple affiliates referred the customer)
- **Cookie-based tracking** — A cookie stores the affiliate code in the customer's browser
- **Cookie lifetime** — Determines the window during which a sale can be attributed (configured per program, typically 30 days)
- **IP and session tracking** — Additional data helps identify fraudulent patterns

### Attribution Example

- Day 1: Customer clicks Affiliate A's link → Cookie set for Affiliate A
- Day 5: Customer clicks Affiliate B's link → Cookie **updated** to Affiliate B (last-click wins)
- Day 7: Customer places an order → Commission goes to **Affiliate B**

If the customer returns on Day 35 (after the 30-day cookie expires) and places an order, **no commission** is created because the tracking window has closed.

## Commission Details

Navigate to **Marketing > Commissions** to view all commission records.

### Commission Fields

Each commission displays:

| Field | Description |
|-------|-------------|
| **Affiliate** | The affiliate's name and code |
| **Program** | The affiliate program name |
| **Order** | Order number (clickable link to view full order details) |
| **Amount** | Calculated commission value |
| **Status** | Current stage (Pending, Approved, Rejected, Paid) |
| **Created** | When the commission was generated |
| **Approved/Rejected Date** | When status was updated |
| **Paid Date** | When payout was processed |
| **Notes** | Internal notes about the commission |

### Viewing Order Details

Click the **order number** in the commission record to view the original order. This lets you verify:
- Order total and items purchased
- Customer information
- Payment status
- Shipping status
- Any refunds or returns

This context helps you decide whether to approve or reject the commission.

## Managing Commissions

While this guide focuses on understanding commissions, the practical steps for approving, rejecting, and paying commissions are covered in detail in the **Commission Management** help topic.

### Quick Overview

- **Approving** — Verify the order is legitimate and confirm the commission is valid
- **Rejecting** — Decline commissions for fraudulent orders, refunds, or policy violations
- **Adding notes** — Document reasons for approval or rejection for future reference
- **Processing payouts** — Group approved commissions into batch payouts

See the related help topics for step-by-step instructions on each management task.

## Tips

- Review pending commissions **daily** during your first month to establish a rhythm and catch any tracking issues early
- Set up **email notifications** to alert you when new commissions are created so you can review them while order details are fresh
- Approve commissions **after order fulfillment** (not immediately upon order placement) to account for cancellations and returns
- Use the **notes field** to document decisions, especially for rejected commissions, so you have a record if affiliates ask questions
- Look for **patterns in rejection** — if one affiliate has many rejected commissions, it may indicate fraud or misunderstanding of program terms
- Consider creating a **commission approval policy** (e.g., "approved after 14-day return window") and communicate it to affiliates to set clear expectations
