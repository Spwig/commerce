---
slug: sso-overview
title_i18n_key: Admin Single Sign-On (SSO)
category: store-config
component: enterprise_sso
keywords:
  - SSO
  - single sign-on
  - OIDC
  - OpenID Connect
  - enterprise login
  - identity provider
  - Microsoft Entra
  - Azure AD
  - Google Workspace
  - Okta
  - admin authentication
  - staff login
  - role mapping
  - group mapping
url_patterns:
  - /admin/enterprise_sso/ssoproviderconfig/
  - /admin/core/sitesettings/
related:
  - sso-setup-microsoft-entra
  - sso-setup-google-workspace
  - sso-setup-okta
  - staff-roles
published: true
---

Single Sign-On (SSO) lets your staff sign in to the admin panel using your organization's identity provider instead of a separate username and password. Spwig supports any identity provider that uses the OpenID Connect (OIDC) protocol, including Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, and others.

## What Is Enterprise SSO?

Enterprise SSO is different from social login (signing in with a personal Google or Facebook account). With enterprise SSO:

- Staff authenticate through your **organization's identity provider** — the same system they use for email, internal tools, and other business applications
- Your IT team controls access centrally — when someone leaves the organization, disabling their account in the identity provider immediately revokes their Spwig access
- Multi-factor authentication (MFA) is enforced by the identity provider, giving you a consistent security policy across all applications
- Staff don't need to remember a separate password for Spwig

## How It Works

When SSO is enabled, the admin login page shows a **Sign in with [Provider]** button. The authentication flow works like this:

1. Staff member clicks the SSO button on the Spwig login page
2. They are redirected to your identity provider's login page (e.g., Microsoft login)
3. They authenticate with the identity provider (including any MFA the provider requires)
4. The identity provider redirects them back to Spwig with a secure authorization code
5. Spwig exchanges the code for user information and creates a session
6. The staff member lands in the admin dashboard, fully authenticated

This uses the industry-standard **OpenID Connect (OIDC)** protocol, which is supported by virtually all enterprise identity providers.

## Enabling SSO

SSO is configured in two places:

1. **Site Settings > Security tab** — Enable or disable SSO and control password login visibility
2. **SSO Provider Configuration** — Enter your identity provider's OIDC details

### Step 1: Configure your identity provider

Before enabling SSO in Spwig, you need to register Spwig as an application in your identity provider. See the provider-specific guides:

- **Microsoft Entra ID** — see the Microsoft Entra ID setup guide
- **Google Workspace** — see the Google Workspace setup guide
- **Okta** — see the Okta setup guide
- **Other providers** — any OIDC-compliant provider works. Register a web application with redirect URI `https://your-store.com/oidc/callback/` and consult your provider's documentation for the OIDC Discovery URL, Client ID, and Client Secret.

### Step 2: Configure SSO Provider in Spwig

Navigate to the **SSO Provider Configuration** page (linked from the Security tab or accessible at **Enterprise SSO > SSO Provider Configuration** in the admin sidebar). Enter:

1. **Provider Name** — displayed on the login button (e.g., "Microsoft Entra ID")
2. **OIDC Discovery URL** — your provider's `.well-known/openid-configuration` URL. Click **Auto-Discover** to automatically populate the endpoint fields.
3. **Client ID** and **Client Secret** — from your identity provider's app registration

The client secret is stored encrypted and never displayed after saving.

### Step 3: Enable SSO in Site Settings

Navigate to **Site Settings > Security** tab and check **Enable SSO for admin login**. The SSO button will immediately appear on the admin login page.

## SSO Settings

| Setting | Description |
|---------|-------------|
| **Enable SSO for admin login** | Shows the SSO button on the admin login page. Does not affect regular password login unless you also disable it. |
| **Allow password login on admin page** | When unchecked, the password form is hidden behind a collapsible toggle. Staff see only the SSO button by default. The password form can still be accessed by clicking "Sign in with local account" or by appending `?password=1` to the login URL. |

### Login Page Behavior

| SSO Enabled | Password Login | Result |
|-------------|---------------|--------|
| Off | On | Standard login page with username/password form only |
| On | On | SSO button at the top, "or" divider, then password form below |
| On | Off | SSO button only. Password form is behind a "Sign in with local account" toggle |
| Off | Off | Not possible — password login is automatically re-enabled if SSO is disabled or not configured |

## User Matching

When a staff member signs in via SSO, Spwig matches them to an existing user account by **email address** (case-insensitive). The email from the identity provider's claims must match the email on the staff member's Spwig account.

If no matching user is found:

- **Auto-Create Users disabled** (default) — the login is denied. You must create the staff account in Spwig first with a matching email address.
- **Auto-Create Users enabled** — a new user account is created automatically with the name and email from the identity provider's claims.

The **Restrict to Staff** setting (enabled by default) adds an additional check: even if a user account exists, the login is denied unless the user has staff status. This prevents non-staff accounts from accessing the admin panel via SSO.

## Role Mapping

If your identity provider sends group membership information in the OIDC claims, Spwig can automatically set staff and superuser status based on group membership.

To configure role mapping:

1. In the SSO Provider Configuration, set the **Groups Claim** field to the claim name your provider uses (default: `groups`)
2. In **Staff Groups**, enter comma-separated group names or IDs. Users in any of these groups are granted staff status.
3. In **Superuser Groups**, enter comma-separated group names or IDs. Users in any of these groups are granted superuser status.

Role mapping is evaluated each time a user signs in via SSO. If a user is removed from a group in the identity provider, their staff or superuser status is updated on their next SSO login.

**Important:** Microsoft Entra ID sends group **Object IDs** (UUIDs) by default, not group names. Copy the Object ID from the Azure portal when configuring role mapping. Other providers like Okta typically send group names.

## Claims Mapping

Spwig reads user information from standard OIDC claims. The defaults work with most providers, but you can customize the claim field names in the SSO Provider Configuration:

| Setting | Default | Description |
|---------|---------|-------------|
| **Email Claim** | `email` | The claim containing the user's email address |
| **First Name Claim** | `given_name` | The claim containing the user's first name |
| **Last Name Claim** | `family_name` | The claim containing the user's last name |
| **Groups Claim** | `groups` | The claim containing group memberships (leave blank to disable role mapping) |

## MFA Behavior

When a staff member signs in via SSO, Spwig's built-in two-factor authentication (2FA) requirement is automatically bypassed. This is because the identity provider is responsible for enforcing MFA as part of the SSO login flow.

If your organization requires MFA, configure it in your identity provider's conditional access policies rather than in Spwig's 2FA settings. This gives you centralized MFA management across all your applications.

## Recovery Access

If your identity provider experiences an outage or misconfiguration, you can still access the admin login form:

- **Click the toggle** — If password login is disabled, click "Sign in with local account" on the login page to reveal the password form
- **URL parameter** — Append `?password=1` to the admin login URL (e.g., `https://your-store.com/en/admin/login/?password=1`) to show the password form directly
- **Password login is always available** — Even when hidden from the UI, the password authentication backend remains active. Only the visibility of the form is affected.

Spwig also prevents you from disabling password login unless SSO is both enabled and properly configured — you cannot accidentally lock yourself out.

## Supported Providers

Spwig works with any identity provider that supports the OpenID Connect (OIDC) protocol. Detailed setup guides are available for:

- **Microsoft Entra ID** (formerly Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

For other OIDC-compliant providers (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud, etc.), the Spwig configuration steps are the same — you need the provider's OIDC Discovery URL, Client ID, and Client Secret. Consult your provider's documentation for how to register a web application and obtain these credentials. The redirect URI to use is always `https://your-store.com/oidc/callback/`.

## Tips

- **Start with password login enabled** — Enable SSO alongside password login first. Once you've confirmed SSO works for your team, you can optionally disable password login.
- **Test in an incognito window** — Use a private/incognito browser window to test SSO without being affected by your current admin session.
- **Create staff accounts first** — Unless you enable Auto-Create Users, staff members need an existing Spwig account with a matching email address before they can sign in via SSO.
- **Use the Auto-Discover button** — Enter your provider's OIDC Discovery URL and click Auto-Discover to automatically populate all endpoint fields. This is faster and less error-prone than entering endpoints manually.
- **Keep a local admin account** — Always maintain at least one local admin account with a password as a recovery option in case of identity provider issues.
- **Monitor client secret expiration** — Some providers (notably Microsoft Entra ID) issue client secrets with expiration dates. Set a calendar reminder to rotate the secret before it expires.
