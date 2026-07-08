---
slug: api-tokens
title_i18n_key: API Tokens
category: settings
component: core
keywords:
  - API token
  - API key
  - external integration
  - webhook token
  - access token
  - token security
  - revoke token
  - integration authentication
  - help system token
  - instance sync
  - IP restriction
  - token expiry
  - create API token
url_patterns:
  - /admin/core/apitoken/
related:
  - staff-roles
  - webhooks
published: true
---

API tokens are secure keys that allow external services and integrations to communicate with your store. When a third-party service or tool needs to access your store's data or trigger actions, it sends an API token with each request so your store can verify the request is authorised. You create and manage all tokens from the API Tokens section of your admin.

## When you need an API token

You will typically need to create an API token when:

- Connecting an external service or automation tool that needs to read from or write to your store
- Setting up a webhook receiver that needs to authenticate incoming calls
- Configuring the Spwig Help System for your installation
- Building a custom integration using Spwig's API
- Synchronising data between your Spwig store and another system

Each integration should have its own token so you can revoke access for one service without affecting others.

## Token types

When creating a token, you choose a type that describes its purpose. The type is for your reference and helps you keep track of what each token does.

| Type | Purpose |
|------|---------|
| **Help System** | Used by the Spwig help documentation system |
| **External Integration** | Third-party services, automation tools (e.g., Zapier), or data sync tools |
| **Webhook** | Authentication for webhook receivers or endpoints |
| **Custom** | Any other purpose that doesn't fit the above categories |
| **Instance Sync** | Synchronisation between Spwig installations or external Spwig services |

## Creating an API token

1. Navigate to **Settings > API Tokens**
2. Click **+ Add API Token**
3. Enter a **Name** that clearly describes what the token is for (e.g., `Zapier Product Sync` or `Help System API`)
4. Select the appropriate **Token Type**
5. Optionally add a **Description** with more detail about the integration
6. Configure the **Active** status, **Expiry Date**, and **Allowed IPs** as needed (see below)
7. Click **Save**

After saving, the full token value is displayed on the detail page. **Copy it immediately** — the token is masked in the list view for security and cannot be retrieved in full again after you leave this page.

![API Token Detail](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Token value security

Spwig shows the complete token value only once: immediately after you save a new token. After that, the list view shows only a masked version (e.g., `spw_••••••••••••••••••••3f8a`).

If you lose a token value, you cannot recover it. You will need to delete the old token and create a new one, then update the integration that was using it.

**Never share token values in emails, chat messages, or source code.** Treat them like passwords.

## Setting an expiry date

The **Expires At** field sets a date and time after which the token will stop working automatically. Leave it blank for tokens that should not expire.

Expiry dates are useful for:

- Temporary integrations with a fixed end date
- Tokens given to third parties where you want automatic access removal
- Adding an extra layer of security to high-privilege integrations

When a token expires, requests using it are rejected. You can extend access by updating the **Expires At** date or creating a replacement token.

## Restricting to specific IP addresses

The **Allowed IPs** field accepts a list of IP addresses. When the list is not empty, the token only works when the request comes from one of those addresses.

For example, if your analytics tool runs on a server at `203.0.113.42`, adding that IP means the token cannot be misused from any other location, even if it is leaked.

Leave **Allowed IPs** empty to allow requests from any IP address.

## Monitoring token usage

The token list shows:

- **Usage Count** — total number of times the token has been used
- **Last Used** — when the token was last used to make a request

These fields help you identify unused tokens (candidates for revocation) and spot unexpected activity. A sudden spike in usage count may indicate a token is being used by someone other than the intended integration.

## Revoking a token

To immediately stop a token from working without deleting it:

1. Click on the token name
2. Uncheck **Active**
3. Save

The token remains in your list for reference but is rejected on any subsequent requests. This is useful when you need to temporarily suspend an integration while investigating an issue.

To permanently remove a token:

1. Select its checkbox in the list
2. Choose **Delete selected API tokens** from the action menu
3. Confirm deletion

Once deleted, a token cannot be recovered. If the integration still needs access, create a new token and update the integration's configuration.

## Example: setting up a Zapier integration

**Scenario:** You want to connect your store to Zapier to automate order notifications.

| Field | Value |
|-------|-------|
| Name | `Zapier Order Automation` |
| Token Type | External Integration |
| Description | Used by Zapier to read new orders and trigger notifications |
| Active | Yes |
| Expires At | *(leave blank)* |
| Allowed IPs | *(leave blank — Zapier uses dynamic IPs)* |

After saving, copy the full token value and paste it into Zapier's Spwig integration settings.

## Tips

- Give every token a clear, specific name — `Shopify Sync v2` is far more useful than `Token 3` when you are troubleshooting months later
- Create one token per integration — if an integration is compromised, you can revoke just that token without disrupting any others
- Set an expiry date for tokens used in one-off projects or temporary integrations — this reduces the risk of forgotten tokens remaining active indefinitely
- Review your token list every few months and deactivate any tokens with a **Last Used** date that is unexpectedly old, as these may belong to integrations that are no longer running
- If you suspect a token has been exposed, deactivate it immediately, create a replacement, and update the affected integration before re-enabling access
