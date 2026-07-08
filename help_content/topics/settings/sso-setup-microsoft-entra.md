---
slug: sso-setup-microsoft-entra
title_i18n_key: "SSO Setup: Microsoft Entra ID"
category: store-config
component: enterprise_sso
keywords:
  - SSO
  - Microsoft
  - Entra ID
  - Azure AD
  - Azure Active Directory
  - OIDC
  - enterprise login
  - app registration
  - tenant
  - client secret
  - group claims
  - conditional access
url_patterns:
  - /admin/enterprise_sso/ssoproviderconfig/
related:
  - sso-overview
  - sso-setup-google-workspace
  - sso-setup-okta
  - staff-roles
published: true
---

This guide walks you through connecting Spwig to Microsoft Entra ID (formerly Azure Active Directory) for admin single sign-on. Once configured, your staff can sign in to the Spwig admin panel using their Microsoft work account.

**Note:** Microsoft may update the Entra admin center interface over time. These instructions were written based on the interface as of early 2026. If any steps differ from what you see, refer to Microsoft's official documentation on [registering an application with the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Prerequisites

- An Azure subscription with access to Microsoft Entra ID
- **Application Administrator** or **Global Administrator** role in your Entra ID tenant
- Your Spwig store URL (e.g., `https://your-store.com`)
- Staff members must have email addresses in Spwig that match their Microsoft accounts

## Step 1: Register an Application

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com)
2. Navigate to **Identity > Applications > App registrations**
3. Click **New registration**
4. Configure the registration:

| Field | Value |
|-------|-------|
| **Name** | `Spwig Admin SSO` (or any name you prefer) |
| **Supported account types** | **Accounts in this organizational directory only** (Single tenant) |
| **Redirect URI** | Platform: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. Click **Register**

**Important:** The redirect URI must exactly match `https://your-store.com/oidc/callback/` — including the trailing slash. Replace `your-store.com` with your actual store domain.

## Step 2: Note the Application IDs

After registration, you'll see the application's **Overview** page. Note these two values — you'll need them later:

| Value | Where to Find It | What It's For |
|-------|-----------------|---------------|
| **Application (client) ID** | Overview page, top section | Enter as **Client ID** in Spwig |
| **Directory (tenant) ID** | Overview page, top section | Used to build the Discovery URL |

## Step 3: Create a Client Secret

1. In the app registration, navigate to **Certificates & secrets**
2. Click **New client secret**
3. Enter a description (e.g., `Spwig SSO`) and choose an expiration period
4. Click **Add**
5. **Copy the Value immediately** — it is only shown once. This is the client secret you'll enter in Spwig.

**Do not copy the Secret ID** — you need the **Value** column, not the ID column.

**Set a reminder** to rotate the secret before it expires. When a secret expires, SSO will stop working until you create a new one and update it in Spwig.

## Step 4: Configure API Permissions

1. Navigate to **API permissions**
2. Verify that **Microsoft Graph > User.Read** (delegated) is listed. This is added by default.
3. If the `openid`, `email`, and `profile` permissions are not listed, click **Add a permission > Microsoft Graph > Delegated permissions** and add them.
4. Click **Grant admin consent for [your organization]** if prompted.

## Step 5: Build the Discovery URL

The OIDC Discovery URL follows this format:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

Replace `{tenant-id}` with the **Directory (tenant) ID** from Step 2.

Example: if your tenant ID is `a1b2c3d4-e5f6-7890-abcd-ef1234567890`, the Discovery URL is:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Step 6: Configure Group Claims (Optional)

If you want Spwig to automatically assign staff or superuser status based on Entra ID group membership:

1. In the app registration, navigate to **Token configuration**
2. Click **Add groups claim**
3. Select the group types to include (typically **Security groups**)
4. Under **Customize token properties by type**, for the **ID** token, select **Group ID**
5. Click **Add**

**Important:** Entra ID sends group **Object IDs** (UUIDs like `a1b2c3d4-...`), not group display names. When configuring role mapping in Spwig, you must use these Object IDs.

To find a group's Object ID:
1. In the Entra admin center, go to **Identity > Groups > All groups**
2. Click the group
3. Copy the **Object ID** from the group's overview page

### Group Limit

Microsoft Entra ID includes a maximum of **200 groups** in the token. If a user belongs to more than 200 groups, the groups claim is replaced with a link to the Microsoft Graph API. For organizations with many groups, consider creating a dedicated security group for Spwig access and using [group filtering](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) to limit which groups are included.

## Step 7: Configure in Spwig

1. In the Spwig admin, navigate to **Enterprise SSO > SSO Provider Configuration**
2. Set **Provider Name** to `Microsoft Entra ID`
3. Paste the Discovery URL from Step 5 into **OIDC Discovery URL**
4. Click **Auto-Discover** — this populates all the endpoint fields automatically
5. Enter the **Client ID** from Step 2
6. Enter the **Client Secret** (the Value) from Step 3
7. If you configured group claims in Step 6:
   - Set **Groups Claim** to `groups`
   - In **Staff Groups**, enter the Object IDs of groups whose members should be staff (comma-separated)
   - In **Superuser Groups**, enter the Object IDs of groups whose members should be superusers (comma-separated)
8. Click **Save**

## Step 8: Enable and Test

1. Navigate to **Site Settings > Security** tab
2. Check **Enable SSO for admin login**
3. Click **Save**
4. Open the admin login page in a **private/incognito window**
5. You should see a **Sign in with Microsoft Entra ID** button
6. Click it — you should be redirected to Microsoft's login page
7. Sign in with a Microsoft account whose email matches a staff user in Spwig
8. You should be redirected back to the Spwig admin dashboard

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| **AADSTS50011: The redirect URI does not match** | The redirect URI in Entra doesn't match exactly | Verify the redirect URI is `https://your-store.com/oidc/callback/` with the trailing slash. Check for HTTP vs HTTPS mismatch. |
| **AADSTS700016: Application not found** | Wrong Client ID or tenant | Double-check the Client ID and that the Discovery URL uses the correct tenant ID |
| **Login succeeds at Microsoft but fails at Spwig** | No matching user in Spwig | Ensure a staff account exists in Spwig with the same email address as the Microsoft account. Check that the user has staff status if Restrict to Staff is enabled. |
| **Groups claim is empty** | Group claims not configured | Follow Step 6 to add a groups claim to the token configuration |
| **Groups claim returns a URL instead of IDs** | User is in more than 200 groups | Use group filtering to limit groups in the token, or assign specific groups |
| **SSO stops working after a few months** | Client secret expired | Create a new client secret in Entra and update it in Spwig's SSO Provider Configuration |

## Tips

- **Use security groups** for role mapping, not Microsoft 365 groups or distribution lists. Security groups are designed for access control and work most reliably with OIDC claims.
- **Single tenant is recommended** — selecting "Accounts in this organizational directory only" restricts SSO to your organization's users. Multi-tenant configurations require additional validation.
- **Set a long secret expiration** — choose 24 months when creating the client secret, and set a calendar reminder at 22 months to rotate it.
- **Conditional access** — you can create conditional access policies in Entra ID that apply specifically to the Spwig app registration. For example, require MFA, block sign-in from untrusted locations, or require compliant devices.
- **Test with a non-admin account** — create a test staff account in Spwig to verify SSO works before rolling it out to your entire team.
