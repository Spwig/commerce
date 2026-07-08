---
slug: sms-setup
title_i18n_key: SMS Provider Setup
category: store-config
component: sms_system
keywords:
  - SMS setup
  - SMS provider
  - Twilio
  - connect SMS
  - SMS credentials
  - WhatsApp provider
  - SMS account
  - text message notifications
  - SMS configuration
  - provider credentials
  - test SMS connection
  - default SMS account
url_patterns:
  - /admin/sms_system/smsprovideraccount/
related:
  - sms-templates
  - sms-outbox
published: true
---

SMS notifications keep your customers informed at every step of their order — from confirmation through to delivery. To send SMS or WhatsApp messages from your store, you connect an SMS provider account with your credentials. Once connected, Spwig uses that account to send all outgoing text messages.

Navigate to **SMS System > SMS Provider Accounts** to manage your SMS providers.

![SMS provider accounts list](/static/core/admin/img/help/sms-setup/provider-list.webp)

## Adding an SMS provider

You can add a provider using either the **Setup Wizard** (recommended for first-time setup) or the manual form.

### Using the setup wizard

1. Navigate to **SMS System > SMS Provider Accounts**
2. Click **Setup Wizard** in the toolbar
3. Follow the guided steps:
   - **Step 1**: Choose your provider from the list of available providers
   - **Step 2**: Enter your provider credentials (API keys, Account SID, etc.)
   - **Step 3**: Set the display name and default settings, then save
4. The wizard tests the connection automatically before saving

### Adding a provider manually

1. Navigate to **SMS System > SMS Provider Accounts**
2. Click **Browse Providers** to explore available SMS providers, or click **+ Add SMS Provider Account** directly
3. In the **Provider** field, select your SMS provider from the dropdown
4. Once you select a provider, credential fields appear automatically based on what that provider requires
5. Fill in the required credential fields (these vary by provider — see the sections below for common providers)
6. Enter a **Display Name** to identify this account (e.g., `Twilio — Main`)
7. Set the **Default Settings** (see below)
8. Click **Save**

## Provider credentials

### Twilio

| Field | Where to find it |
|-------|-----------------|
| Account SID | Twilio Console → Dashboard |
| Auth Token | Twilio Console → Dashboard |
| From Number | Your Twilio phone number in E.164 format (e.g., `+15551234567`) |

### Other providers

Other installed SMS provider components will show their own specific credential fields when selected. Refer to your provider's documentation for the exact values needed — typically an API key or access token and a sender identifier.

## Default settings

After entering credentials, configure how this account is used:

- **Active** — enable or disable this account. Inactive accounts are not used for sending, even if set as default
- **Default SMS Account** — when checked, all SMS notifications from your store use this account. Only one account can be the default SMS account at a time
- **Default WhatsApp Account** — if this provider supports WhatsApp (e.g., Twilio via WhatsApp Business API), check this to use it as the default for WhatsApp messages

## Testing the connection

After saving a provider account, test that the credentials work:

1. Navigate to **SMS System > SMS Provider Accounts**
2. Click on your provider account to open it
3. Click the **Test Connection** button
4. Spwig sends a test request to the provider and updates the **Connection Status** field

| Status | Meaning |
|--------|---------|
| Connected | Credentials are valid and the provider is reachable |
| Connection Failed | Credentials are incorrect or the provider is unreachable |
| Untested | The connection has not been tested yet |

If the test fails, double-check your credentials and ensure your account has the necessary permissions at the provider's dashboard.

## Connection status column

The SMS Provider Accounts list shows a colour-coded **Connection** badge for each account:

- **Connected** (green) — account is working
- **Connection Failed** (red) — credentials have failed — update them
- **Untested** (grey) — account has not been tested yet

## Tips

- Use the Setup Wizard for your first provider — it guides you through every field and tests the connection before saving
- Only one account can be the Default SMS Account at a time. If you add a second account and mark it as default, the previous default is automatically unset
- Keep a note of your provider API credentials in a secure place. If credentials change, update them here immediately to avoid failed notifications
- Inactive accounts remain in the list but are not used for sending — useful for keeping backup credentials without activating them
- Most providers charge per message sent — monitor usage in your provider's dashboard to avoid unexpected bills
