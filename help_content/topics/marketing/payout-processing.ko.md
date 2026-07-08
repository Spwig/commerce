---
title: Payout Processing
---

Payout processing allows you to pay affiliates for their approved commissions. This guide shows you how to create, manage, and process payouts through PayPal or bank transfer providers.

![Payout List](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Payout Overview

A payout is a payment batch that groups multiple approved commissions for a single affiliate. Think of it as writing a check for all outstanding earnings.

Key characteristics:
- **Includes multiple commissions** — One payout can cover dozens of approved commissions
- **Requires minimum threshold** — Most programs have minimum payout amounts ($50-$100 typical)
- **Processed via providers** — PayPal or Airwallex handle the actual money transfer
- **Has lifecycle** — Pending → Processing → Completed (or Failed)

## Payout Workflow

The complete payout process follows six steps:

1. **Affiliate earns commissions** — Sales attributed to affiliate tracking links
2. **Merchant approves commissions** — Review and approve pending commissions
3. **Balance reaches minimum** — Affiliate's approved balance meets program threshold
4. **Affiliate requests payout** — Affiliate submits payout request in their dashboard
5. **Merchant processes payout** — You create and process the payout
6. **Payment completed** — Provider sends funds, commissions marked as paid

## Viewing Payouts

Navigate to **Affiliate Program > Payouts** to access the payout management dashboard.

The statistics panel shows:
- **Pending** — Payouts created but not yet processed
- **Processing** — Currently being sent to payment provider
- **Completed** — Successfully paid
- **Failed** — Payment failed (requires attention)

The list view displays:
- Affiliate name and code
- Payout amount
- Payment method (PayPal or Bank Transfer)
- Status badge
- Creation and completion dates
- Action buttons

Use filters to narrow by:
- Affiliate
- Payment method
- Status
- Date range

## Creating a Payout

Follow these steps to create a new payout:

1. **Navigate** to **Affiliate Program > Payouts**
2. **Click** the **+ Add Payout** button
3. **Select affiliate** from the dropdown
4. **Review approved commissions** — System displays all unpaid, approved commissions for this affiliate
5. **Select commissions to include** — Check the boxes for commissions to pay (usually all)
6. **Verify total amount** — System calculates the sum automatically
7. **Choose payment method** — PayPal or Bank Transfer (based on affiliate's preference)
8. **Select provider account** — Choose which PayPal/Airwallex account to use
9. **Add notes** (optional) — Internal notes for record keeping
10. **Click Save** — Payout created with status "Pending"

The payout is now ready to process.

## Processing Payouts

You have two options for processing payouts: manual or provider-based.

### Manual Processing

Use manual processing when you handle payments outside the system (checks, wire transfers, etc.):

1. Select the payout in the list
2. Click **Mark as Processing** action
3. Complete payment through your external method
4. Return to the payout
5. Click **Mark as Completed** action
6. Commissions automatically update to "Paid" status

Manual processing provides flexibility but requires more administrative work.

### Provider Processing (Recommended)

Provider processing automates payments through PayPal or Airwallex:

1. **Select payout(s)** in the list (you can process multiple)
2. **Click** the **Process with Provider** action
3. **Confirm** in the dialog
4. **System queues task** — Celery worker handles the API call
5. **Provider processes payment**:
   - **PayPal**: Batches up to 15,000 payouts per request
   - **Airwallex**: Individual bank transfers
6. **Webhook updates status** — Provider confirms completion
7. **Commissions marked as paid** — System updates all included commissions

Provider processing is faster, more reliable, and creates an automatic audit trail.

## Payout Methods

Spwig supports two payout methods with different requirements:

| Method | Provider | Requirements | Processing Time | Fees | Best For |
|--------|----------|--------------|-----------------|------|----------|
| **PayPal** | PayPal Payouts | Affiliate must have valid `payment_email` | 1-2 business days | ~2% or $0.25-$1.00 per payment | Most affiliates, global reach |
| **Bank Transfer** | Airwallex | Bank account details (account number, routing, SWIFT) | 2-5 business days | Varies by country | International affiliates, large amounts |

Affiliates configure their payment method and details in their dashboard. The system automatically selects the appropriate provider based on their preference.

### Payment Method Selection Logic

When processing a payout, Spwig selects the provider as follows:

1. Check affiliate's preferred payment method (PayPal or Bank Transfer)
2. Match to configured provider account (PayPal → PayPal, Bank → Airwallex)
3. Fall back to first available provider if preference unavailable
4. Display error if no providers configured

## Payout Status Flow

Understanding payout statuses helps you track payment progress:

| Status | Meaning | Next Action |
|--------|---------|-------------|
| **Pending** | Created but not yet sent to provider | Process with provider or mark as processing |
| **Processing** | Submitted to payment provider, awaiting confirmation | Wait for webhook or check provider dashboard |
| **Completed** | Payment successful, funds sent | None — commissions marked as paid |
| **Failed** | Payment failed (see error details) | Review error, fix issue, retry or cancel |
| **Cancelled** | Manually cancelled before completion | None — commissions remain unpaid |

### Success Path

Pending → Processing → Completed

This is the happy path. Provider webhooks automatically update the status as payment progresses.

### Failure Path

Pending → Processing → Failed

When a payment fails, the payout status changes to Failed and you must investigate.

## Handling Failed Payouts

Failed payouts require manual intervention. Common failure reasons:

| Cause | Provider Error | Solution |
|-------|----------------|----------|
| Invalid account | "Recipient account not found" | Verify affiliate's payment email or bank details |
| Insufficient balance | "Insufficient funds" | Add funds to your provider account |
| Bank details error | "Invalid routing number" | Ask affiliate to update bank information |
| Account restriction | "Recipient cannot receive payments" | Contact affiliate to resolve their account status |
| Provider issue | "Service temporarily unavailable" | Wait and retry after a few hours |

### How to Retry a Failed Payout

1. **View the failed payout** — Click it in the list
2. **Read error message** — Check the **Provider Response** field for details
3. **Fix the underlying issue** — Update affiliate details, add provider funds, etc.
4. **Reset status** — Change status back to Pending (edit form)
5. **Process again** — Use **Process with Provider** action

### How to Cancel and Recreate

If retrying does not work:

1. **Open the failed payout**
2. **Change status to Cancelled**
3. **Save the payout**
4. **Create a new payout** — Follow the creation steps again
5. **Process the new payout**

Cancelled payouts do not mark commissions as paid, so they remain eligible for new payouts.

## Payout Provider Integration

Processing payouts requires a configured payout provider account. Spwig integrates with:

- **PayPal Payouts API** — For PayPal payments
- **Airwallex** — For international bank transfers

### Setup Requirements

Before processing payouts:
1. Configure at least one provider in **Settings > Payout Providers**
2. Add API credentials (Client ID, Secret, API Key)
3. Set to production mode (sandbox for testing)
4. Configure webhook URL in provider dashboard
5. Verify connectivity with a test payout

See the [Payout Provider Setup](#) guide for detailed configuration instructions.

### Provider Selection by Affiliate

Affiliates choose their preferred payment method in their dashboard:
- PayPal: Enter `payment_email`
- Bank Transfer: Enter bank account details

The system automatically routes payouts to the matching provider.

## Payout Schedule Best Practices

Establish a regular payout schedule to build trust with affiliates:

| Schedule | Frequency | Workload | Affiliate Satisfaction | Recommended For |
|----------|-----------|----------|------------------------|-----------------|
| Weekly | Every Friday | High | Excellent | New programs, high-volume |
| Bi-weekly | 1st and 15th | Medium | Good | Medium-volume programs |
| Monthly | 1st of month | Low | Acceptable | Established programs |
| Quarterly | Every 3 months | Very low | Poor | Not recommended |

Consider your program size and administrative capacity when choosing a schedule.

## Processing Best Practices

Follow these guidelines for smooth payout operations:

- **Batch payouts by schedule** — Process all eligible payouts on the same day each week/month
- **Verify details before processing** — Double-check affiliate payment information, especially for large amounts
- **Monitor provider balance** — Ensure sufficient funds in your PayPal/Airwallex account
- **Set clear minimum thresholds** — Communicate payout minimums in program terms ($50-$100 typical)
- **Document your schedule** — Add payout schedule to affiliate terms and portal settings
- **Use provider processing** — Avoid manual processing unless absolutely necessary
- **Review failed payouts immediately** — Address failures within 24 hours
- **Keep provider webhooks configured** — Webhooks enable automatic status updates
- **Export payout reports regularly** — Download monthly reports for accounting

## Payout Records and Reporting

Each payout creates an immutable record with:
- Affiliate information
- Included commission IDs
- Total amount
- Payment method and provider
- Creation and completion timestamps
- Provider transaction ID (after processing)
- Provider response data (for debugging)
- Internal notes

Access this data by clicking any payout in the list. Use the admin interface export feature to download payout reports for accounting or tax purposes.

## Tips

- Process payouts on a fixed schedule (every Friday at 2pm, for example) so affiliates know when to expect payment.
- Always use provider processing instead of manual processing — it is faster, more reliable, and creates better audit trails.
- Set minimum payout thresholds in your programs to reduce administrative overhead — $50 or $100 is standard.
- Monitor your provider account balance before processing large batches to avoid failures.
- Test your payout integration in sandbox mode before going live with real payments.
- Add a note to every payout explaining what period it covers (e.g., "Commissions for January 2026").
- Check failed payouts immediately — delays frustrate affiliates and damage trust.
- Communicate delays proactively — if you cannot process on schedule, notify affected affiliates in advance.