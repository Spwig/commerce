---
slug: sso-setup-google-workspace
title_i18n_key: "SSO Setup: Google Workspace"
category: store-config
component: enterprise_sso
keywords:
  - SSO
  - Google Workspace
  - Google Cloud
  - OAuth
  - OIDC
  - enterprise login
  - Google Cloud Console
  - OAuth consent screen
  - Google identity
url_patterns:
  - /admin/enterprise_sso/ssoproviderconfig/
related:
  - sso-overview
  - sso-setup-microsoft-entra
  - sso-setup-okta
  - staff-roles
published: true
---

This guide walks you through connecting Spwig to Google Workspace for admin single sign-on. Once configured, your staff can sign in to the Spwig admin panel using their Google Workspace account.

**Note:** Google may update the Cloud Console interface over time. These instructions were written based on the interface as of early 2026. If any steps differ from what you see, refer to Google's official documentation on [setting up OAuth 2.0](https://support.google.com/cloud/answer/6158849).

## Prerequisites

- A Google Workspace subscription (Google Workspace Business, Enterprise, or Education)
- Admin access to the [Google Cloud Console](https://console.cloud.google.com)
- Your Spwig store URL (e.g., `https://your-store.com`)
- Staff members must have email addresses in Spwig that match their Google Workspace accounts

## Step 1: Create or Select a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. Click the project selector in the top bar
3. Click **New Project** (or select an existing project if you prefer)
4. Enter a project name (e.g., `Spwig SSO`)
5. Select your organization
6. Click **Create**

## Step 2: Configure the OAuth Consent Screen

1. In the Cloud Console, navigate to **APIs & Services > OAuth consent screen**
2. Select **Internal** as the user type — this restricts login to users within your Google Workspace organization
3. Click **Create**
4. Fill in the required fields:

| Field | Value |
|-------|-------|
| **App name** | `Spwig Admin` (or your store name) |
| **User support email** | Your admin email address |
| **Authorized domains** | `your-store.com` (your store's domain, without `https://`) |
| **Developer contact email** | Your admin email address |

5. Click **Save and Continue**
6. On the **Scopes** page, click **Add or Remove Scopes** and add:
   - `openid`
   - `email`
   - `profile`
7. Click **Save and Continue**
8. Review the summary and click **Back to Dashboard**

## Step 3: Create OAuth Credentials

1. Navigate to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth client ID**
3. Configure the client:

| Field | Value |
|-------|-------|
| **Application type** | Web application |
| **Name** | `Spwig SSO` |
| **Authorized redirect URIs** | `https://your-store.com/oidc/callback/` |

4. Click **Create**
5. A dialog shows your **Client ID** and **Client Secret** — copy both values. You can also download them as JSON for safekeeping.

**Important:** The redirect URI must exactly match `https://your-store.com/oidc/callback/` — including the trailing slash and the `https://` scheme. Replace `your-store.com` with your actual store domain.

## Step 4: Get the Discovery URL

Google uses a single, standard Discovery URL for all Workspace tenants:

```
https://accounts.google.com/.well-known/openid-configuration
```

This URL is the same for every Google Workspace organization — you do not need to customize it with a tenant or domain.

## Step 5: Configure in Spwig

1. In the Spwig admin, navigate to **Enterprise SSO > SSO Provider Configuration**
2. Set **Provider Name** to `Google Workspace`
3. Enter the Discovery URL: `https://accounts.google.com/.well-known/openid-configuration`
4. Click **Auto-Discover** — this populates all the endpoint fields automatically
5. Enter the **Client ID** from Step 3
6. Enter the **Client Secret** from Step 3
7. Click **Save**

### Claims Mapping

Google uses standard OIDC claim names, so the default Spwig configuration works out of the box:

| Spwig Setting | Google Claim | Default Value |
|---------------|-------------|---------------|
| Email Claim | `email` | `email` |
| First Name Claim | `given_name` | `given_name` |
| Last Name Claim | `family_name` | `family_name` |

No changes to the claims mapping are needed.

## Step 6: Enable and Test

1. Navigate to **Site Settings > Security** tab
2. Check **Enable SSO for admin login**
3. Click **Save**
4. Open the admin login page in a **private/incognito window**
5. You should see a **Sign in with Google Workspace** button
6. Click it — you should be redirected to Google's login page
7. Sign in with a Google Workspace account whose email matches a staff user in Spwig
8. You should be redirected back to the Spwig admin dashboard

## Group-Based Role Mapping

Unlike Microsoft Entra ID or Okta, Google does not include group membership in standard OIDC tokens by default. Implementing group claims with Google requires the Google Workspace Directory API and additional configuration beyond basic OIDC.

For most Google Workspace deployments, we recommend managing staff and superuser status directly in Spwig rather than through automatic role mapping:

1. Create staff accounts in Spwig with the appropriate permissions
2. Use Spwig's Staff Roles system to control access levels
3. Staff sign in via SSO, and Spwig uses their existing permissions

If you require automatic group-based role mapping, consult the [Google Workspace Admin SDK Directory API documentation](https://developers.google.com/admin-sdk/directory) for configuring custom claims.

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| **Error 400: redirect_uri_mismatch** | The redirect URI in Google Cloud doesn't match exactly | Verify the redirect URI is `https://your-store.com/oidc/callback/` with the trailing slash. Check HTTP vs HTTPS. |
| **Error 403: access_denied** | User is not in the Google Workspace organization | With "Internal" user type, only users in your organization can sign in. Verify the user's account is part of your Workspace domain. |
| **OAuth consent screen shows "This app isn't verified"** | Normal for Internal apps | This warning is expected for Internal apps and doesn't affect functionality. Users in your organization can still sign in. |
| **Login succeeds at Google but fails at Spwig** | No matching user in Spwig | Ensure a staff account exists in Spwig with the same email as the Google Workspace account. Check that Restrict to Staff is configured correctly. |
| **"Access blocked: This app's request is invalid"** | Scopes not properly configured | Verify that `openid`, `email`, and `profile` scopes are added to the OAuth consent screen. |

## Tips

- **Use "Internal" user type** — this restricts sign-in to your Google Workspace organization and doesn't require Google's app verification process.
- **Google client secrets don't expire** — unlike Microsoft Entra ID, Google OAuth client secrets do not have an expiration date. However, you can rotate them at any time from the Credentials page.
- **One project for multiple apps** — you can create multiple OAuth client IDs within the same Google Cloud project if you have multiple Spwig installations.
- **Test with a non-admin account** — create a test staff account in Spwig and use a regular Google Workspace user (not a super admin) to verify SSO works as expected.
