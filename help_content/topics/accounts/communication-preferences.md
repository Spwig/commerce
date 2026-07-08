---
slug: communication-preferences
title_i18n_key: Communication Preferences
category: customers
component: accounts
keywords:
  - communication
  - preferences
  - email
  - SMS
  - marketing
  - newsletter
  - notifications
  - opt-in
  - opt-out
  - GDPR
  - unsubscribe
  - consent
  - TCPA
  - CAN-SPAM
  - double opt-in
  - verification
  - transactional
url_patterns:
  - /admin/accounts/communicationpreference/
  - /accounts/preferences/
related:
  - managing-customer-accounts
  - email-configuration
published: true
---

Communication preferences allow customers to control which emails and SMS messages they receive from your store. This system ensures GDPR compliance and helps you respect customer communication preferences across all channels.

Navigate to **Customers > Communication Preferences** in the admin sidebar to manage customer communication preferences.

## Understanding Communication Preferences

The communication preferences system gives customers granular control over the messages they receive. This includes:

- **Transactional emails** — Essential order confirmations, shipping updates, account security emails (always on)
- **Marketing emails** — Newsletters, promotions, product recommendations (requires opt-in)
- **App-specific notifications** — Blog posts, loyalty points, referral rewards, affiliate commissions
- **SMS notifications** — Text message notifications (requires explicit opt-in per TCPA)

All marketing communications require customer consent and email verification to ensure GDPR compliance.

## Preference Types Explained

### Transactional Communications (Always Enabled)

Transactional messages are essential for your customer's account and orders. These **cannot be disabled** by customers:

| Type | Description | Examples |
|------|-------------|----------|
| **Order Confirmations** | Confirmation when order is placed | Order #12345 has been received |
| **Shipping Updates** | Notifications when order status changes | Your order has been shipped |
| **Payment Confirmations** | Payment received, refund processed | Payment of $49.99 confirmed |
| **Account Security** | Password resets, email verification | Reset your password |

### Marketing Communications (Opt-In Required)

Marketing messages require customer consent and email verification:

| Type | Description | Default |
|------|-------------|---------|
| **Newsletter** | General newsletters and updates | Opt-out |
| **Promotional Offers** | Sales, discounts, special offers | Opt-out |
| **Product Recommendations** | Personalized product suggestions | Opt-out |
| **Back in Stock** | Notifications when products return | Opt-out |

Customers must **verify their email address** before receiving any marketing emails (GDPR double opt-in requirement).

### App-Specific Preferences

Customers can control notifications from specific features:

**Blog Notifications**
- New blog post published (immediate, weekly digest, or monthly digest)
- Category-specific subscriptions
- Frequency preferences

**Loyalty Program**
- Points earned notifications
- Tier upgrades
- Rewards unlocked
- Points expiring soon
- Birthday bonuses
- Campaign offers

**Referral Program**
- Reward issued (referrer and referee)
- Successful referral signup
- Reward expiring soon
- Referral invitations

**Affiliate Program**
- Commission earned
- Commission approved or rejected
- Payout processed, completed, or failed
- Monthly performance reports

### SMS Notifications (Explicit Opt-In Required)

All SMS notifications require **explicit opt-in** per TCPA regulations. Customers must actively check the SMS opt-in box:

- **Transactional SMS** — Order shipped, delivered (opt-in required)
- **Marketing SMS** — Promotions, special offers (separate opt-in required)

Even transactional SMS requires opt-in because sending unsolicited text messages is regulated more strictly than email.

## Managing Customer Preferences in Admin

### Viewing All Preferences

Navigate to **Customers > Communication Preferences** to see all customer preferences:

| Column | Description |
|--------|-------------|
| **User Email** | Customer's email address (links to user admin) |
| **Email Status** | Green ✓ if emails enabled, gray ○ if disabled |
| **SMS Status** | Green ✓ if SMS enabled, gray ○ if disabled |
| **Marketing Status** | "Opted In" or "Opted Out" badge |
| **Verification Status** | 📧✓ if email verified, 📱✓ if SMS verified |
| **Consent Source** | Where customer consented (registration, checkout, preference center) |
| **Updated At** | Last time preferences were changed |

### Filtering Preferences

Use the filter sidebar to find customers:

- **Email Enabled** — Yes/No
- **SMS Enabled** — Yes/No
- **Email Marketing** — Yes/No (opted in to marketing)
- **SMS Marketing** — Yes/No (opted in to SMS marketing)
- **Email Verified** — Yes/No (verified their email address)
- **SMS Verified** — Yes/No (verified their phone number)
- **Consent Source** — Registration, Checkout, Preference Center, API, Migration
- **Language Code** — Preferred language for communications

### Searching Preferences

Search for customers by:
- User email
- Username
- First name
- Last name
- Unsubscribe token

### Bulk Actions

Select multiple customers and apply bulk actions:

**✓ Mark Email as Verified**
- Manually verify customer email addresses
- Useful when importing customers from another system
- Invalidates preference cache to apply changes immediately

**🚫 Unsubscribe from All Marketing**
- Disables all marketing communications (email, SMS, all apps)
- Keeps transactional emails enabled
- Use this for customers who request to be fully unsubscribed
- Respects GDPR right to withdraw consent

**📥 Export Preferences to CSV**
- Export customer preferences to spreadsheet
- Includes all preference fields and app-specific settings
- Useful for compliance audits and analysis
- Format: CSV with headers

## Customer Self-Service Preference Center

Customers can manage their own preferences at `/accounts/preferences/` when logged in.

### Preference Center Features

**Quick Actions**
- **Subscribe to All Marketing** — Enable all marketing communications in one click
- **Unsubscribe from All** — Disable all marketing communications (transactional still enabled)

**Preference Cards**
- **Transactional Emails** — Read-only (always enabled, marked as "Required")
- **Marketing Communications** — Toggle on/off with verification badge
- **Blog Preferences** — Enable/disable, select frequency (immediate, weekly, monthly)
- **Loyalty Program** — Enable/disable individual notification types
- **Referral Program** — Enable/disable reward notifications
- **Affiliate Program** — Enable/disable commission and payout notifications
- **SMS Notifications** — Opt in/out of SMS (shows verification status)

**Real-Time Updates**
- Changes save immediately via AJAX
- No page reload required
- Visual feedback when saved

### Email Verification Process

When a customer enables marketing emails:

1. Customer toggles "Marketing Emails" to ON
2. System sends verification email with unique link
3. Customer clicks verification link
4. Email marked as verified (📧✓ badge appears)
5. Marketing emails will now be sent

**Unverified customers will NOT receive marketing emails** even if the toggle is ON. This ensures GDPR double opt-in compliance.

## One-Click Unsubscribe

All marketing emails include an unsubscribe link in the footer. Clicking this link:

1. Takes customer to `/accounts/unsubscribe/<token>/` (no login required)
2. Shows what they're unsubscribing from
3. Allows optional feedback (reason for unsubscribing)
4. Disables marketing communications
5. Keeps transactional emails enabled
6. Provides link to full preference center

Customers can resubscribe at any time via the preference center.

## Compliance & Legal Requirements

### GDPR Article 7 Compliance

The system ensures full GDPR Article 7 compliance:

**✅ Proof of Consent**
- Timestamp when consent was given
- Consent source (registration, checkout, preference center)
- IP address of consent
- User agent (browser information)

**✅ Separate Consent**
- Marketing and transactional emails are separate toggles
- Each app (blog, loyalty, etc.) requires individual consent

**✅ Easy Withdrawal**
- One-click unsubscribe in all marketing emails
- Preference center available to all logged-in customers
- Unsubscribe takes effect immediately

**✅ Consent Freely Given**
- Default is opt-out for marketing (GDPR best practice)
- No pre-checked boxes (customers must actively opt in)

**✅ Specific and Informed Consent**
- Clear descriptions of what each preference controls
- Granular app-level preferences (not all-or-nothing)

**✅ Verifiable Consent**
- Double opt-in for marketing emails
- Audit trail via EmailOutbox status tracking

### TCPA Compliance (USA SMS Regulations)

All SMS notifications require **explicit opt-in**:

- Customers must actively check the SMS opt-in box
- No pre-checked boxes allowed
- Clear description of what they're opting into
- Easy opt-out via preference center
- All SMS sends are logged for compliance audit

### CAN-SPAM Compliance (USA Email Regulations)

The system ensures CAN-SPAM compliance:

- Unsubscribe link in every marketing email
- Unsubscribe processed immediately (within 10 business days required, we do it instantly)
- Clear "From" name (your shop name)
- Physical address in email footer
- No deceptive subject lines

## Understanding Email Status in EmailOutbox

When viewing **Email System > Email Outbox**, you'll see how preferences affect email delivery:

| Status | Meaning | Reason |
|--------|---------|--------|
| **Pending** | Email queued for sending | Preferences allow this email |
| **Queued** | In sending queue | Preferences allow this email |
| **Skipped** | Email not sent | Customer preference disabled |
| **Sent** | Successfully delivered | Email sent normally |

When an email is **skipped**, the `skip_reason` field shows why:

- **user_preference_disabled** — Customer disabled this email type in preferences
- **email_not_verified** — Customer hasn't verified their email address
- **email_disabled** — Customer disabled all emails (master toggle)

This audit trail is important for GDPR compliance — you can prove you honored customer preferences.

## Site Settings for Preferences

Navigate to **Settings > Site Settings** to configure global preference defaults:

**Enable Double Opt-In for Marketing Emails** (Default: Yes)
- Requires email verification before sending marketing emails
- GDPR best practice
- Recommended: Leave enabled

**Default Marketing Opt-In State** (Default: No - Opt-Out)
- Default state when new customers register
- GDPR requires opt-out by default
- Recommended: Leave as opt-out (False)

**Preference Center Enabled** (Default: Yes)
- Allows customers to manage their own preferences
- Required for GDPR right to withdraw consent
- Recommended: Leave enabled

**Require SMS Verification** (Default: No)
- Require phone number verification for SMS notifications
- Optional but recommended for high-volume SMS senders
- Can be enabled if you want double opt-in for SMS

**Show Unsubscribe Reasons** (Default: Yes)
- Collect optional feedback when customers unsubscribe
- Helps understand why customers are opting out
- Recommended: Leave enabled for insights

## Best Practices

### 1. Default to Opt-Out for Marketing

Always default marketing communications to **opt-out** (unchecked):
- Complies with GDPR
- Builds trust with customers
- Reduces spam complaints
- Only send to engaged customers

### 2. Require Email Verification

Keep **Double Opt-In** enabled:
- Ensures email addresses are valid
- Confirms customer actually wants marketing emails
- Reduces bounce rate
- Required for GDPR compliance

### 3. Respect Preferences Immediately

When a customer changes preferences:
- Changes take effect immediately
- Preference cache is invalidated
- Next email send will check updated preferences
- No delay in honoring unsubscribe requests

### 4. Monitor Skipped Emails

Regularly check **Email Outbox** for skipped emails:
- High skip rate indicates customers are opting out
- May signal email content needs improvement
- Helps identify preference issues

### 5. Regular Compliance Audits

Export preferences periodically for compliance:
1. Navigate to **Communication Preferences**
2. Select all customers
3. Choose **Export Preferences to CSV**
4. Save for GDPR audit trail

Store exports for **at least 3 years** to comply with GDPR data retention requirements.

### 6. Clear Communication

When collecting consent:
- Use plain language, not legal jargon
- Explain what customers will receive
- Show frequency (daily, weekly, monthly)
- Make opt-in boxes prominent but not pre-checked

### 7. Segment by Preference

When sending marketing campaigns:
- Only send to verified, opted-in customers
- Respect app-specific preferences (don't send blog emails to customers who disabled blog)
- Use frequency preferences (don't send immediate emails to weekly digest subscribers)

## Tips

**💡 Check Preference Before Sending**

The system automatically checks preferences when you send emails using `EmailSendingService.send_template_email()`. Make sure all email sends use this service, not direct SMTP calls.

**💡 Skipped Status is Normal**

Don't be alarmed by skipped emails in the outbox — this means the system is working correctly and honoring customer preferences. It's better to skip unwanted emails than risk GDPR fines or spam complaints.

**💡 Preference Cache is 5 Minutes**

Preference checks are cached for 5 minutes for performance. When customers change preferences via the preference center or admin actions, the cache is immediately invalidated so changes take effect right away.

**💡 Guest Customers Bypass Checks**

Guest checkout customers (no account) will receive all emails normally because they have no preference record. This is intentional — they opted in by providing their email at checkout.

**💡 Transactional Emails Always Send**

Order confirmations, shipping updates, and account security emails **always send** regardless of preferences. This ensures customers receive critical information about their orders and accounts.

**💡 Use Bulk Actions Carefully**

The "Unsubscribe from All Marketing" bulk action affects **all apps** (blog, loyalty, referrals, affiliate). Only use this for customers who explicitly requested to be fully unsubscribed. For specific preferences, edit individual customer records.

**💡 Audit Trail for Compliance**

The system tracks:
- Consent timestamp and source
- IP address and user agent
- Email verification timestamp
- Every preference change via EmailOutbox skipped status

This audit trail proves GDPR compliance if authorities ever request evidence of consent.

## Related Topics

- [Managing Customer Accounts](/help/managing-customer-accounts) — Customer profile management
- [Email Configuration](/help/email-configuration) — SMTP setup and email templates
