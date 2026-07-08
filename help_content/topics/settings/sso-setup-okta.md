---
slug: sso-setup-okta
title_i18n_key: "SSO Setup: Okta"
category: store-config
component: enterprise_sso
keywords:
  - SSO
  - Okta
  - OIDC
  - enterprise login
  - Okta application
  - authorization server
  - group claims
  - Okta admin
url_patterns:
  - /admin/enterprise_sso/ssoproviderconfig/
related:
  - sso-overview
  - sso-setup-microsoft-entra
  - sso-setup-google-workspace
  - staff-roles
published: true
---

This guide walks you through connecting Spwig to Okta for admin single sign-on. Once configured, your staff can sign in to the Spwig admin panel using their Okta account.

**Note:** Okta may update their admin console interface over time. These instructions were written based on the Okta admin console as of early 2026. If any steps differ from what you see, refer to Okta's official documentation on [creating an OIDC app integration](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Prerequisites

- An Okta organization (any tier — free developer accounts work for testing)
- **Super Administrator** or **Application Administrator** role in Okta
- Your Spwig store URL (e.g., `https://your-store.com`)
- Staff members must have email addresses in Spwig that match their Okta accounts

## Step 1: Create an Application

1. Sign in to the [Okta Admin Console](https://your-org-admin.okta.com)
2. Navigate to **Applications > Applications**
3. Click **Create App Integration**
4. Select:

| Field | Value |
|-------|-------|
| **Sign-in method** | OIDC - OpenID Connect |
| **Application type** | Web Application |

5. Click **Next**

## Step 2: Configure the Application

Fill in the application settings:

| Field | Value |
|-------|-------|
| **App integration name** | `Spwig Admin SSO` (or any name you prefer) |
| **Grant type** | Authorization Code (should be selected by default) |
| **Sign-in redirect URIs** | `https://your-store.com/oidc/callback/` |
| **Sign-out redirect URIs** | `https://your-store.com/en/admin/login/` |
| **Controlled access** | Choose based on your needs (see below) |

For **Controlled access**, choose one of:

- **Allow everyone in your organization to access** — all Okta users can sign in (you can still control Spwig access with the Restrict to Staff setting)
- **Limit access to selected groups** — only users in specific Okta groups can sign in
- **Skip group assignment for now** — you'll assign users or groups manually later

Click **Save**.

**Important:** The sign-in redirect URI must exactly match `https://your-store.com/oidc/callback/` — including the trailing slash.

## Step 3: Get Client Credentials

After saving, the application's **General** tab shows your credentials:

| Value | Where to Find It |
|-------|-----------------|
| **Client ID** | General tab, Client Credentials section |
| **Client Secret** | General tab, Client Credentials section (click the eye icon to reveal) |

Copy both values — you'll need them for Spwig.

## Step 4: Build the Discovery URL

The Discovery URL depends on your Okta organization and authorization server:

**Default authorization server (most common):**
```
https://your-org.okta.com/.well-known/openid-configuration
```

**Custom authorization server (if configured):**
```
https://your-org.okta.com/oauth2/{authorization-server-id}/.well-known/openid-configuration
```

Replace `your-org.okta.com` with your actual Okta domain. You can find your Okta domain in the admin console URL bar or under **Settings > Account**.

**Tip:** Most organizations use the Org Authorization Server (the default). Only use a custom authorization server URL if your Okta administrator has set one up specifically.

## Step 5: Assign Users or Groups

If you chose "Skip group assignment" in Step 2, you need to assign users before they can sign in:

1. In the application's **Assignments** tab, click **Assign**
2. Choose **Assign to People** or **Assign to Groups**
3. Select the users or groups and click **Assign**
4. Click **Done**

Users who are not assigned to the application will see an error when attempting SSO.

## Step 6: Configure Group Claims (Optional)

If you want Spwig to automatically set staff or superuser status based on Okta group membership:

1. Navigate to **Security > API** in the admin console
2. Select your **Authorization Server** (use "default" if you haven't created a custom one, or the Org Authorization Server)
3. Go to the **Claims** tab
4. Click **Add Claim**
5. Configure the claim:

| Field | Value |
|-------|-------|
| **Name** | `groups` |
| **Include in token type** | ID Token, Always |
| **Value type** | Groups |
| **Filter** | Matches regex: `.*` (to include all groups) |
| **Include in** | Any scope (or `openid` if you want to limit it) |

6. Click **Create**

**Tip:** Unlike Microsoft Entra ID which sends Object IDs, Okta sends **group names** by default. This makes role mapping more intuitive — you can use the display names of your Okta groups directly in Spwig's Staff Groups and Superuser Groups fields.

### Filtering Groups

If your users belong to many Okta groups and you only want specific ones included in the token:

- Change the filter from `.*` to a more specific regex, e.g., `^Spwig.*` to only include groups starting with "Spwig"
- Or use **Starts with**, **Equals**, or **Contains** filters instead of regex

## Step 7: Configure in Spwig

1. In the Spwig admin, navigate to **Enterprise SSO > SSO Provider Configuration**
2. Set **Provider Name** to `Okta`
3. Enter the Discovery URL from Step 4
4. Click **Auto-Discover** — this populates all the endpoint fields automatically
5. Enter the **Client ID** from Step 3
6. Enter the **Client Secret** from Step 3
7. If you configured group claims in Step 6:
   - Set **Groups Claim** to `groups`
   - In **Staff Groups**, enter the names of Okta groups whose members should be staff (comma-separated)
   - In **Superuser Groups**, enter the names of Okta groups whose members should be superusers (comma-separated)
8. Click **Save**

## Step 8: Enable and Test

1. Navigate to **Site Settings > Security** tab
2. Check **Enable SSO for admin login**
3. Click **Save**
4. Open the admin login page in a **private/incognito window**
5. You should see a **Sign in with Okta** button
6. Click it — you should be redirected to Okta's login page
7. Sign in with an Okta account that is assigned to the application and whose email matches a staff user in Spwig
8. You should be redirected back to the Spwig admin dashboard

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| **The redirect URI is not allowed** | Redirect URI doesn't match the application config | Verify the sign-in redirect URI is exactly `https://your-store.com/oidc/callback/` with the trailing slash |
| **User is not assigned to the client application** | User not assigned to the Okta app | Assign the user or their group to the application in the Assignments tab |
| **Login succeeds at Okta but fails at Spwig** | No matching user in Spwig | Ensure a staff account exists in Spwig with the same email. Check the Restrict to Staff setting. |
| **Groups claim is empty** | Groups claim not configured on the authorization server | Follow Step 6 to add a groups claim. Make sure you're adding it to the correct authorization server. |
| **Wrong authorization server** | Discovery URL uses a different auth server than where groups claim is configured | Verify the Discovery URL matches the authorization server where you configured the groups claim |
| **"The client_id provided is invalid"** | Client ID doesn't match or app is inactive | Check that the Client ID is correct and the application status is Active in Okta |

## Tips

- **Okta sends group names, not IDs** — this makes role mapping straightforward. Enter the exact group display name (e.g., `Spwig Admins`) in Spwig's Staff Groups or Superuser Groups fields.
- **Use group assignment for access control** — assign specific Okta groups to the Spwig application rather than allowing all users. This way, only the intended staff can sign in.
- **Okta client secrets don't expire by default** — but you can rotate them at any time from the application's General tab for security best practices.
- **Test with a non-admin account** — use a regular Okta user (not a super admin) assigned to the application to verify SSO works as expected.
- **MFA in Okta** — configure Okta's global session policy or authentication policies to require MFA. This will apply to all SSO logins to Spwig without needing to configure MFA separately in Spwig.
