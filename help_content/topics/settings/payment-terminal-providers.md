---
slug: payment-terminal-providers
title_i18n_key: Payment Terminal Providers
category: point-of-sale
component: pos_app
keywords:
  - payment providers
  - stripe terminal
  - card payments
  - payment processing
  - card readers
  - payment integration
  - stripe api
  - payment credentials
  - connection status
  - payment setup
  - terminal payments
  - pos payments
  - card processing
  - payment configuration
url_patterns:
  - /admin/pos_app/posterminalprovider/
related:
  - pos-system-overview
  - card-reader-management
  - managing-pos-terminals
published: true
---

Payment terminal providers enable credit and debit card acceptance at your POS terminals. Stripe Terminal is the primary supported provider, offering modern card readers (S700, WisePOS E, P400), competitive processing rates, and seamless integration. Configure provider accounts with API credentials, monitor connection status in real-time, and manage multiple providers if operating in different regions. The provider system is extensible—additional payment processors can be integrated via the provider framework if Stripe Terminal doesn't operate in your market.

Use payment providers to accept card payments securely, track payment processing status, and manage reader assignments across terminals.

![Payment Provider List](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Payment Provider Overview

Payment providers are third-party services that process card payments on behalf of your business:

**Provider Responsibilities**:
- Authorize card transactions in real-time
- Communicate with physical card readers
- Handle payment security (PCI compliance, encryption)
- Transfer funds to your bank account (settlement)
- Provide transaction reporting and dispute management

**Spwig's Role**:
- Routes payment requests to configured provider
- Stores encrypted provider credentials
- Monitors connection status
- Associates readers with terminals
- Records payment outcomes in orders

## Stripe Terminal (Primary Provider)

Stripe Terminal is the recommended payment provider for most merchants:

**Features**:
- Modern EMV chip card readers
- Contactless (NFC) payment support (Apple Pay, Google Pay, tap-to-pay cards)
- Integrated dispute management
- Real-time authorization
- Developer-friendly API
- Available in 40+ countries

**Pricing** (as of 2024, verify current rates):
- Transaction fees: 2.7% + $0.05 per in-person transaction (US)
- No monthly fees, no setup fees, no PCI compliance fees
- Card reader hardware: One-time purchase ($59-$299 depending on model)

**Supported Regions**:
- United States, Canada, United Kingdom, European Union, Australia, Singapore, and more
- Check Stripe's availability: https://stripe.com/terminal

**Supported Readers**:
- BBPOS WisePOS E (all-in-one Android terminal)
- Stripe Reader S700 (countertop reader)
- Verifone P400 (legacy reader, still supported)

## Setting Up Stripe Terminal

**Step 1: Create Stripe Account**
- Sign up at stripe.com
- Complete business verification (bank account, tax ID)
- Activate payments

**Step 2: Enable Stripe Terminal**
- In Stripe Dashboard, navigate to **Products > Terminal**
- Click **Get Started**
- Accept Terminal terms of service

**Step 3: Create Location**
- Stripe Terminal requires a "Location" representing your physical retail site
- Navigate to **Terminal > Locations**
- Click **Create Location**
- Enter store address and details
- Save location ID (looks like `tml_1ABC123...`)

**Step 4: Generate API Key**
- Navigate to **Developers > API Keys**
- Locate your **Secret Key** (starts with `sk_live_...` for production, `sk_test_...` for testing)
- Copy the secret key (do not share publicly)

**Step 5: Configure in Spwig**
- Navigate to **POS > Payment Providers**
- Click **+ Add Payment Provider**
- Select **Provider**: "Stripe Terminal"
- Enter **API Secret Key** (from Step 4)
- Enter **Location ID** (from Step 3)
- Save

**Step 6: Test Connection**
- After saving, provider status should change to "Connected" (green)
- If status shows "Error" (red), verify API key and location ID
- Check error message in provider detail view

![Payment Provider Add Form](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Provider Configuration Fields

**Provider Key** - Select the payment processor:
- **stripe_terminal** - Stripe Terminal (recommended)
- **manual** - Manual payment entry (for testing only, no actual processing)
- Additional providers may appear if installed via component system

**Credentials (Encrypted)** - JSON structure containing API credentials:
- Automatically encrypted before storage
- Never visible in plain text after saving
- Example structure (Stripe Terminal):
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Provider Settings** - Additional configuration (provider-specific):
- Statement descriptor (appears on customer's credit card statement)
- Auto-capture (immediately capture authorized payments vs manual capture)
- Currency override (if provider account uses different currency than store)

**Connection Status** - Real-time status indicator:
- **Connected** (green) - Provider is reachable and configured correctly
- **Error** (red) - Connection failed or invalid credentials
- **Unknown** (gray) - Not yet tested (immediately after creation)

**Last Tested** - Timestamp of most recent connection test
- Updates automatically when transactions are processed
- Manually trigger test via **Test Connection** admin action

## Connection Status Monitoring

The system monitors provider connectivity to alert you of issues before customers attempt payments:

**Automatic Testing**:
- Every payment transaction triggers connection test (by necessity)
- Background job tests connection every 6 hours (preventative monitoring)

**Status Meanings**:

**Connected** - Provider API is reachable, credentials are valid, ready to process payments

**Error** - Common causes:
- Invalid API key (revoked, expired, or incorrect)
- Invalid location ID (location deleted in Stripe, wrong ID entered)
- Network connectivity issues (firewall blocking Stripe API)
- Stripe service outage (rare)

**Unknown** - Provider never tested yet (newly created account pending first transaction)

**Resolving Error Status**:
1. Check error message in provider detail view (explains specific issue)
2. Verify API key is still valid in Stripe Dashboard
3. Verify location ID still exists in Stripe Dashboard
4. Test connection manually via **Test Connection** admin action
5. Update credentials if needed

![Payment Provider Detail](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## Supported Card Readers Comparison

Stripe Terminal offers multiple reader hardware options:

| Model | Type | Payment Methods | Display | Best For | Price |
|-------|------|-----------------|---------|----------|-------|
| **WisePOS E** | All-in-one | EMV chip, NFC, swipe | 5" color touchscreen | Full-featured retail POS | ~$299 |
| **S700** | Countertop | EMV chip, NFC, swipe | Monochrome LCD | Standard retail checkout | ~$249 |
| **P400** | Countertop | EMV chip, NFC, swipe | Monochrome LCD | Legacy deployments | ~$299 |

**WisePOS E Advantages**:
- Android-based (runs apps, can display custom content)
- Color touchscreen (better UX for tip prompts, signature capture)
- Integrated receipt printer (optional)
- Fastest transaction speed

**S700 Advantages**:
- Lower cost than WisePOS E
- Compact footprint
- Splash-resistant design

**P400** (older model):
- Still supported but not recommended for new deployments
- Slower chip card processing than S700/WisePOS E

All readers connect to Spwig POS via Stripe Terminal API (no direct USB/Bluetooth connection to POS device required).

## Security Considerations

**Credential Encryption**:
- All provider credentials are encrypted at rest in database
- Encryption uses application secret key (defined in application settings)
- Credentials never appear in logs or error messages

**API Key Permissions**:
- Use **restricted API keys** in production (limit permissions to Terminal only)
- Don't use unrestricted secret keys (broader access than needed = security risk)
- In Stripe Dashboard, create restricted key with only **Terminal** permissions

**PCI Compliance**:
- Stripe Terminal handles PCI compliance (card data never touches Spwig servers)
- Card numbers processed entirely on reader hardware → Stripe servers → card networks
- Spwig only stores payment outcomes (approved/declined), never card details

**Key Rotation**:
- Rotate API keys annually as security best practice
- When rotating, update credentials in provider configuration
- Old keys can be revoked in Stripe Dashboard after confirming new key works

## Multiple Providers

Some merchants need multiple provider accounts:

**Multi-Currency Operations**:
- US stores use Stripe US account (processes USD)
- European stores use Stripe EU account (processes EUR)
- Configure separate provider per currency

**Backup Providers**:
- Primary provider (Stripe Terminal)
- Backup provider (manual entry) for when readers malfunction
- Cashier selects provider when initiating payment

**Testing vs Production**:
- Test provider with `sk_test_...` API key
- Production provider with `sk_live_...` API key
- Switch providers after testing phase

## Troubleshooting Common Issues

**Issue 1: Status shows "Error" with message "Invalid API key"**
- **Cause**: API key revoked or incorrectly copied
- **Solution**: Generate new API key in Stripe Dashboard, update provider credentials, test connection

**Issue 2: Reader not discovered during payment**
- **Cause**: Reader not registered to provider's location
- **Solution**: In Stripe Dashboard, verify reader is registered to same location ID used in provider config

**Issue 3: Payments declined despite valid card**
- **Cause**: Stripe account not fully activated (verification pending)
- **Solution**: Complete business verification in Stripe Dashboard (bank account, tax ID)

**Issue 4: Connection status shows "Unknown" and never updates**
- **Cause**: Provider never tested (no transactions attempted)
- **Solution**: Use **Test Connection** admin action to manually trigger connectivity test

## Tips

- **Test mode before production** - Use Stripe test API keys (`sk_test_...`) for initial setup and testing
- **One provider per currency** - Don't try to process EUR with USD-based Stripe account; create separate providers
- **Monitor connection status weekly** - Proactive monitoring prevents payment failures at checkout
- **Restrict API key permissions** - Limit Stripe API keys to only Terminal permissions (principle of least privilege)
- **Document location IDs** - Keep record of which Stripe location corresponds to which physical store
- **Test reader assignment** - After provider setup, test payment with actual card reader to verify end-to-end flow
- **Keep Stripe contact updated** - Ensure business contact info in Stripe matches current (important for disputes, compliance)
