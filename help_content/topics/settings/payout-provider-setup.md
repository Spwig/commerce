---
slug: payout-provider-setup
title_i18n_key: Payout Provider Setup
category: affiliates
component: affiliate
keywords:
  - payout provider
  - paypal setup
  - airwallex setup
  - payout integration
  - automated payouts
  - payout configuration
  - paypal credentials
  - airwallex api
  - provider webhook
  - payout api
  - payment provider setup
  - affiliate payout setup
url_patterns:
  - /admin/payout_providers/payoutprovideraccount/
related:
  - payout-processing
  - affiliate-program-overview
published: true
---

Payout provider setup allows you to configure PayPal and Airwallex for automated affiliate payments. This guide shows you how to connect your payment provider accounts, configure webhooks, and test your integration.

## Supported Payout Providers

Spwig integrates with two payout providers to automate affiliate payments:

| Provider | Payment Method | Processing | Batch Support | Best For |
|----------|----------------|------------|---------------|----------|
| **PayPal** | PayPal account transfers | API-based | Yes (up to 15,000) | Most affiliates, global reach |
| **Airwallex** | International bank transfers | API-based | No (individual) | Bank transfers, international payments |

### Key Differences

**PayPal Payouts**:
- Requires affiliate to have PayPal account (payment email)
- Processes batches of up to 15,000 payouts at once
- Faster processing (1-2 business days)
- Lower setup complexity
- Fees: ~2% or $0.25-$1.00 per payment
- Single webhook for entire batch

**Airwallex**:
- Supports direct bank transfers
- Processes individual payouts one at a time
- Longer processing (2-5 business days)
- Supports multiple currencies and countries
- Fees vary by destination country
- Individual webhook per payout

You can configure both providers and let affiliates choose their preferred payment method.

## Why Use Payout Providers?

Integrating payment providers offers significant benefits over manual payments:

- **Automated processing** — No manual data entry or payment execution
- **Batch efficiency** — Process dozens or hundreds of payouts with one click
- **Webhook confirmations** — Automatic status updates when payments complete
- **Reduced errors** — System validates account details before processing
- **Audit trail** — Complete record of transactions and provider responses
- **Faster payments** — Affiliates receive funds more quickly
- **Scalability** — Handle growing affiliate programs without proportional admin work

Without provider integration, you must process each payment manually through your bank or PayPal dashboard, then return to Spwig to mark payouts as completed.

## PayPal Setup

Follow these steps to configure PayPal Payouts for automated affiliate payments.

### Prerequisites

Before you begin, you need:
- A PayPal Business account (personal accounts cannot use Payouts API)
- Access to PayPal Developer Dashboard
- Production approval for Payouts API (after sandbox testing)

### Step 1: Create PayPal App

1. **Navigate** to [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
2. **Sign in** with your PayPal Business account
3. **Click** **My Apps & Credentials** in the left sidebar
4. **Select** the **Live** tab (or Sandbox for testing)
5. **Click** **Create App**
6. **Enter app name** (e.g., "Spwig Affiliate Payouts")
7. **Select app type**: Merchant
8. **Click** **Create App**

PayPal generates your credentials.

### Step 2: Get API Credentials

After creating the app:

1. **Copy Client ID** — Long alphanumeric string
2. **Click** **Show** under Secret
3. **Copy Client Secret** — Keep this confidential
4. **Note the mode** — Sandbox or Live

### Step 3: Enable Payouts Feature

PayPal apps require explicit permission to use Payouts:

1. **Scroll** to **Features** section in your app
2. **Find** **Payouts** feature
3. **Click** **Add** if not already enabled
4. **Submit for approval** if using Live mode (approval takes 1-2 business days)

### Step 4: Add Provider in Spwig

Now add the PayPal account to Spwig:

1. **Navigate** to **Settings > Payout Providers**
2. **Click** **+ Add PayPal Account**
3. **Fill in the form**:
   - **Account Name**: Descriptive label (e.g., "Main PayPal Account")
   - **Client ID**: Paste from PayPal Developer Dashboard
   - **Client Secret**: Paste from PayPal Developer Dashboard
   - **Mode**: Select Sandbox (testing) or Production (live)
   - **Is Active**: Check to enable
4. **Click Save**

Spwig validates the credentials by requesting an access token. If validation fails, double-check your Client ID and Secret.

### Step 5: Test Connection

Verify your PayPal integration:

1. Create a test payout in **Affiliate Program > Payouts**
2. Use your own PayPal email as the recipient
3. Set amount to $0.01 (if in Production) or any amount (if Sandbox)
4. Process with provider
5. Check PayPal account for incoming payment
6. Verify webhook updates payout status in Spwig

If using Sandbox mode, create a test PayPal account at [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts) to receive test payouts.

## Airwallex Setup

Airwallex supports international bank transfers for affiliates who prefer direct deposit.

### Prerequisites

Before you begin, you need:
- An Airwallex account (create at [airwallex.com](https://www.airwallex.com))
- Verified business account status
- API access enabled (contact Airwallex support if needed)
- Sufficient balance in your Airwallex account

### Step 1: Generate API Credentials

1. **Sign in** to [Airwallex Dashboard](https://www.airwallex.com/app/)
2. **Navigate** to **Settings > API Keys**
3. **Click** **Create API Key**
4. **Enter description**: "Spwig Affiliate Payouts"
5. **Select permissions**: Enable **Payouts** (read and write)
6. **Click** **Generate**
7. **Copy API Key** — Shown only once
8. **Copy Client ID** — Displayed with the key

### Step 2: Note Your Environment

Airwallex provides two environments:

- **Demo**: For testing with fake transactions
- **Production**: For real money transfers

Make sure you know which environment your API key belongs to.

### Step 3: Add Provider in Spwig

Add the Airwallex account to Spwig:

1. **Navigate** to **Settings > Payout Providers**
2. **Click** **+ Add Airwallex Account**
3. **Fill in the form**:
   - **Account Name**: Descriptive label (e.g., "Airwallex EUR Account")
   - **API Key**: Paste from Airwallex dashboard
   - **Client ID**: Paste from Airwallex dashboard
   - **Environment**: Select Demo or Production
   - **Is Active**: Check to enable
4. **Click Save**

Spwig validates credentials by querying your account balance.

### Step 4: Verify Supported Countries

Airwallex supports transfers to many countries but not all. Check the [Airwallex coverage](https://www.airwallex.com/global-business-account/global-transfers) page to confirm your affiliates' countries are supported.

Common supported countries include:
- United States
- United Kingdom
- European Union countries
- Australia
- Canada
- Singapore
- Hong Kong

### Step 5: Test Bank Transfer

Test your Airwallex integration:

1. Create a test payout for an affiliate with bank details
2. Use a small amount ($1-$5) if in Production mode
3. Process with provider
4. Check Airwallex dashboard for transaction
5. Wait for webhook confirmation
6. Verify payout completes in Spwig

Demo mode processes instantly. Production mode takes 2-5 business days.

## Provider Selection Logic

When you process a payout, Spwig automatically selects the appropriate provider based on the affiliate's payment method.

### Selection Flow

1. **Check affiliate payment method**:
   - If `payment_email` is set → Affiliate prefers PayPal
   - If bank details are set → Affiliate prefers Bank Transfer
2. **Match to provider**:
   - PayPal email → Use active PayPal provider account
   - Bank details → Use active Airwallex provider account
3. **Fall back to first available** if preferred provider is not configured
4. **Display error** if no matching provider exists

### Multiple Provider Accounts

You can configure multiple accounts for the same provider (e.g., two PayPal accounts for different regions). Spwig selects the first active account that matches the payment method. To control which account is used, reorder them in the admin list or set only one as active.

## Testing Payout Integration

Always test your provider integration before processing live payments to affiliates.

### Sandbox/Demo Mode Testing

1. **Set provider to sandbox mode** (PayPal Sandbox or Airwallex Demo)
2. **Create test affiliate** with test payment details
3. **Create test commissions** and approve them
4. **Create test payout** including those commissions
5. **Process with provider** using the action menu
6. **Monitor Celery logs** for API requests
7. **Check provider dashboard** for transaction
8. **Wait for webhook** to update payout status
9. **Verify commissions marked as paid**

### Production Testing

Before going live:

1. **Switch to production mode** in provider settings
2. **Create a small test payout** to yourself ($0.01-$1.00)
3. **Process it** and wait for completion
4. **Verify funds received** in your own account
5. **Check webhook fired** and updated status
6. **Review provider transaction fees**

### Common Test Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Invalid credentials" | Wrong API key or mode mismatch | Re-check credentials, verify sandbox vs production |
| Webhook never fires | URL not configured in provider | Add webhook URL in provider dashboard |
| Payout stays in Processing | Webhook signature failed | Check webhook secret matches |
| No provider available | No active provider for payment method | Enable at least one provider account |

## Batch Processing (PayPal)

PayPal supports batch processing for efficiency and cost savings.

### How Batching Works

When you select multiple payouts and click **Process with Provider**:

1. Spwig groups all PayPal payouts into a single batch
2. System sends one API request with all payout details (up to 15,000)
3. PayPal processes the entire batch as a single transaction
4. Webhook returns with batch results
5. Spwig updates all payouts based on batch response

### Batch Advantages

- **Reduced API calls** — One request for hundreds of payouts
- **Lower fees** — Some PayPal fee structures favor batching
- **Faster processing** — Parallel execution for entire batch
- **Single webhook** — Easier monitoring and logging

### Batch Limits

PayPal imposes these limits:
- Maximum 15,000 recipients per batch
- Maximum $100,000 total per batch
- Processing typically completes within minutes

If you exceed 15,000 payouts, Spwig automatically splits into multiple batches.

## Individual Processing (Airwallex)

Airwallex processes payouts one at a time, which provides different tradeoffs.

### How Individual Processing Works

When you process Airwallex payouts:

1. System sends separate API request for each payout
2. Airwallex queues transfers individually
3. Each transfer completes independently (2-5 days)
4. Individual webhook fires when each transfer completes
5. Spwig updates payouts as webhooks arrive

### Individual Processing Advantages

- **Better error isolation** — One failure does not block others
- **Per-payout tracking** — Individual transaction IDs
- **More payment details** — Bank-specific information per transfer
- **Flexible timing** — Transfers complete at different rates

### Processing Time

Unlike PayPal's instant batching, Airwallex transfers take longer:
- Domestic transfers: 1-2 business days
- International transfers: 3-5 business days
- Some countries: Up to 7 business days

Set affiliate expectations accordingly in your program terms.

## Webhook Configuration

Webhooks enable automatic payout status updates when providers complete transactions.

### Webhook URL Format

Configure this URL in your provider dashboard:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

Replace `{provider}` with:
- `paypal` for PayPal webhooks
- `airwallex` for Airwallex webhooks

Examples:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### PayPal Webhook Setup

1. **Navigate** to [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
2. **Click** your app name
3. **Scroll** to **Webhooks** section
4. **Click** **Add Webhook**
5. **Enter webhook URL** (format above)
6. **Select events**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Click Save**

PayPal provides a webhook signing key. Spwig uses this to verify webhook authenticity.

### Airwallex Webhook Setup

1. **Navigate** to [Airwallex Dashboard](https://www.airwallex.com/app/)
2. **Go to** **Settings > Webhooks**
3. **Click** **Create Webhook**
4. **Enter webhook URL** (format above)
5. **Select events**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Click Create**

Airwallex signs webhooks with your API secret.

### Webhook Security

Webhooks are validated using these mechanisms:

- **Signature verification** — Provider signs webhook payload with secret key
- **Timestamp checking** — Rejects old webhooks (prevents replay attacks)
- **IP allowlisting** (optional) — Restrict to provider IP ranges
- **HTTPS required** — Webhooks only work over SSL

Never disable signature verification in production.

### Testing Webhooks

Most providers offer webhook testing tools:

**PayPal**: Use "Simulator" in Developer Dashboard to fire test webhooks

**Airwallex**: Create a test transfer in Demo mode and watch for webhook

You can also check webhook logs in Spwig at **Settings > System Logs** (if logging is enabled).

## Troubleshooting

### Invalid Credentials Error

**Symptom**: "Authentication failed" when saving provider account

**Causes**:
- Wrong Client ID or Secret
- Sandbox credentials used in Production mode (or vice versa)
- API key expired or revoked
- Account not verified

**Solutions**:
- Re-copy credentials from provider dashboard
- Verify mode matches (sandbox vs production)
- Regenerate API keys
- Contact provider support to verify account status

### Webhook Not Received

**Symptom**: Payout stuck in "Processing" status indefinitely

**Causes**:
- Webhook URL not configured in provider dashboard
- HTTPS certificate invalid
- Firewall blocking provider IPs
- Webhook signature validation failing

**Solutions**:
- Double-check webhook URL in provider settings
- Verify SSL certificate is valid
- Whitelist provider IP ranges in firewall
- Check Celery logs for signature errors
- Test webhook with provider's simulator tool

### Payout Failed

**Symptom**: Payout status changes to "Failed" with error message

**Causes**:
- Invalid affiliate payment details (wrong email or bank account)
- Insufficient balance in provider account
- Recipient account cannot receive payments
- Country not supported (Airwallex)
- Payout exceeds provider limits

**Solutions**:
- Review error in **Provider Response** field
- Verify affiliate's payment details are correct
- Add funds to provider account
- Ask affiliate to check their account status
- Check provider's country and currency support
- Split large payouts if they exceed limits

### Mode Mismatch

**Symptom**: Test payouts work but production payouts fail

**Causes**:
- Provider set to Sandbox mode but using production affiliate accounts
- API credentials from wrong environment

**Solutions**:
- Switch provider mode to Production
- Regenerate production API credentials
- Verify webhook URL points to production domain

## Security Best Practices

Protect your payout integration with these security measures:

### Credential Storage

- **Never commit credentials to version control** — Use environment variables or secure storage
- **Rotate API keys quarterly** — Generate new keys every 3 months
- **Use separate keys for sandbox and production** — Never mix environments
- **Limit API permissions** — Only grant Payouts access, not full account control

Spwig stores provider credentials encrypted in the database. Keep your database backups secure.

### Webhook Security

- **Always verify signatures** — Never skip signature validation
- **Use HTTPS exclusively** — HTTP webhooks are not supported
- **Implement IP allowlisting** — Restrict webhooks to provider IP ranges
- **Log all webhooks** — Monitor for suspicious activity
- **Rate limit webhook endpoints** — Prevent abuse

### Access Control

- **Limit staff access** — Only trusted staff should process payouts
- **Use two-factor authentication** — Require 2FA for staff accounts
- **Audit payout actions** — Review who processed which payouts
- **Separate duties** — Different staff for approval vs processing

### Monitoring

- **Check failed payouts daily** — Address issues promptly
- **Monitor provider account balances** — Ensure sufficient funds
- **Review transaction logs weekly** — Catch anomalies early
- **Set up alerts** — Email notifications for large or failed payouts

## Tips

- Test your integration thoroughly in sandbox mode before switching to production — catch issues with fake money.
- Configure both PayPal and Airwallex to give affiliates payment choice — different affiliates prefer different methods.
- Set webhook URLs during initial setup and verify they fire correctly — webhooks are critical for automation.
- Keep provider account balances topped up to avoid failed payouts during batch processing.
- Use descriptive account names if you configure multiple providers (e.g., "PayPal USD", "PayPal EUR").
- Rotate API credentials every quarter as a security best practice.
- Document your webhook URLs and credentials in a secure password manager shared with your team.
- Monitor failed payouts immediately — delays frustrate affiliates and damage program reputation.
- Always use HTTPS for your Spwig installation — webhooks require SSL certificates.
- Contact provider support if you encounter persistent errors — they can verify your account status and permissions.
