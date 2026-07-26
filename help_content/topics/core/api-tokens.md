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
  - API scopes
  - web analytics API
  - token permissions
url_patterns:
  - /admin/core/apitoken/
related:
  - staff-roles
  - webhooks-overview
published: true
---

API tokens are secure keys that allow external services and integrations to communicate with your store. When a third-party service or tool needs to access your store's data or trigger actions, it sends an API token with each request so your store can verify the request is authorised. You create and manage all tokens, including exactly which parts of your store they can reach, from the API Tokens section of your admin.

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

## API scopes: controlling what a token can reach

Every token also has an **API Scopes** section that decides exactly which parts of your store it is allowed to call. Instead of a token having blanket access to everything, you grant access one area at a time — and at the level the integration actually needs.

**A token with no scopes selected cannot reach any API**, even if it is otherwise active and valid. This is the default for a brand-new token, so an integration will not work until you deliberately grant it access.

For each scope, you choose one of three access levels:

| Access Level | What it allows |
|--------------|-----------------|
| **No access** | The token cannot call any endpoint in this area |
| **Read** | The token can retrieve data from this area, but not change anything |
| **Read & Write** | The token can retrieve data and also create, update, or delete it |

Scopes are grouped to match the areas of your admin:

| Group | Scope | Read & Write available? | Grants access to |
|-------|-------|:---:|-------------------|
| Analytics | **Sales Analytics** | Read only | Sales dashboards, KPIs, product/customer/category analytics, comparisons and exports |
| Analytics | **Web Analytics** | Read only | Visitor and traffic analytics: overview, trends, top pages, geography and referrers |
| Catalog | **Products** | Yes | Products, variants, images, stock adjustments and attribute assignment |
| Catalog | **Categories** | Yes | Product categories, including images and banners |
| Catalog | **Brands** | Yes | Product brands |
| Catalog | **Attributes** | Yes | Product attribute definitions |
| Catalog | **Inventory** | Yes | Inventory dashboards, stock velocity, movements, reorder suggestions and inventory settings |
| Orders | **Orders** | Yes | Orders, order notes, status/tracking updates, cancellations, refunds and order documents |
| Customers | **Customer Messages** | Yes | Customer messages from contact forms and order notes, including status updates and replies |
| Store & Settings | **Store Settings** | Yes | Store settings, available languages and branding (name, colours, logo) |
| Users & Access | **Staff & Roles** | Yes | Staff accounts, invitations, roles and the permission catalogue |

The two **Analytics** scopes are always read-only — reporting data has no "write" concept, so the picker only offers **No access** or **Read** for them.

![The API Scopes picker, with an access note above the Analytics and Catalog scope groups](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)

Below the scope picker, a read-only **"This token can access:"** summary lists every scope you have granted and its level, so you can double-check a token's access at a glance without decoding the picker.

![The "This token can access" summary listing each granted scope and its Read or Read & Write level](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)

### Whose permissions a token actually uses

A token's scopes describe the *ceiling* of what it can do — but the token also inherits the real-world permissions of the staff member who created it:

- The token can never act with **superuser** powers, even if the creating staff member is a superuser.
- **Read & Write** on a scope only works if the creating staff member's role also permits write access to that area. If their role is view-only for, say, Products, a token they create with "Products: Read & Write" can still only read — the role acts as a second gate on top of the scope.
- If the staff member who created a token is deleted, or their account is deactivated, the token immediately loses API access, regardless of its scopes — there is no longer a permitted user for it to act as.

This means the safest way to scope a token tightly is to create it while logged in as a staff member whose own role already matches the access you want the token to have.

## Creating an API token

1. Navigate to **Settings > API Tokens**
2. Click **+ Add API Token**
3. Enter a **Name** that clearly describes what the token is for (e.g., `Zapier Product Sync` or `Help System API`)
4. Select the appropriate **Token Type**
5. Optionally add a **Description** with more detail about the integration
6. In **API Scopes**, choose **No access**, **Read**, or **Read & Write** for each area the integration needs — leave every other scope at **No access**
7. Configure the **Active** status, **Expiry Date**, and **Allowed IPs** as needed (see below)
8. Click **Save**

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

**Expiry and IP restrictions are checked independently of scopes.** An expired or off-allowlist token is rejected before its scopes are even considered, and a token with generous scopes is still rejected the moment it expires or is called from an unlisted IP.

## Calling the API with a token

Integrations authenticate to Spwig's admin API by sending the token in an `Authorization` header:

```
Authorization: Bearer <your-token-value>
```

Every admin API endpoint lives under `/api/admin/...`. The developer building your integration decides which endpoints to call — your job as the merchant is to make sure the token's **API Scopes** cover those endpoints. If a request is rejected with a permissions error, the first thing to check is whether the token has been granted the right scope at the right access level.

### Example: reading web traffic analytics

Spwig exposes a `GET /api/admin/analytics/traffic/` endpoint that returns visitor and traffic analytics for your store — an overview of visits and unique visitors, trends over time, top pages, visitor geography, and referrer sources. To let a reporting tool or dashboard read this data:

1. Create a token (or edit an existing one) for that integration
2. In **API Scopes**, set **Web Analytics** to **Read**
3. Save the token and provide it to the integration

Because **Web Analytics** is a read-only scope, there is no "Read & Write" option to choose — the integration can only retrieve analytics data, never change your store's configuration.

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
| API Scopes | **Orders**: Read & Write |
| Active | Yes |
| Expires At | *(leave blank)* |
| Allowed IPs | *(leave blank — Zapier uses dynamic IPs)* |

Only the **Orders** scope is granted, so even if this token were ever exposed, it could not touch products, customer messages, staff accounts, or any other part of your store. After saving, copy the full token value and paste it into Zapier's Spwig integration settings.

## Tips

- Give every token a clear, specific name — `Shopify Sync v2` is far more useful than `Token 3` when you are troubleshooting months later
- Create one token per integration — if an integration is compromised, you can revoke just that token without disrupting any others
- **Grant only the scopes an integration actually needs** — a reporting tool only needs Read access to Sales Analytics or Web Analytics, not Read & Write on Products or Staff & Roles
- Check the **"This token can access:"** summary on the change form before handing a token to a third party — it is the fastest way to confirm you haven't granted more than intended
- Remember that write access also depends on the creating staff member's own role — if a scope shows Read & Write but writes are still failing, check that user's role permissions too
- Set an expiry date for tokens used in one-off projects or temporary integrations — this reduces the risk of forgotten tokens remaining active indefinitely
- Review your token list every few months and deactivate any tokens with a **Last Used** date that is unexpectedly old, as these may belong to integrations that are no longer running
- If you suspect a token has been exposed, deactivate it immediately, create a replacement, and update the affected integration before re-enabling access
