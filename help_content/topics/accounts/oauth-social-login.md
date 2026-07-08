---
slug: oauth-social-login
title_i18n_key: OAuth & Social Login Setup
category: customers
component: accounts
keywords:
  - oauth setup
  - social login
  - google login
  - apple login
  - microsoft login
  - sign in with google
  - oauth configuration
  - social authentication
url_patterns:
  - /admin/core/sitesettings/
  - /admin/socialaccount/socialapp/
related:
  - store-settings
  - accounts-vs-customers
published: true
---

OAuth and social login allow customers to sign in to your store using their existing Google, Apple, or Microsoft accounts — no need to create and remember yet another password.

![OAuth settings](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## What is OAuth / Social Login?

OAuth is a secure authentication standard that lets customers log in using credentials from trusted providers like Google, Apple, or Microsoft.

### Benefits

- **Faster Checkout** — Customers skip the registration form and log in with one click
- **Reduced Friction** — No password creation, verification emails, or forgotten password flows
- **Better Conversion** — Studies show social login can increase conversion rates by 20-40%
- **Enhanced Security** — Credentials never pass through your store; authentication is handled by the provider
- **Customer Trust** — Customers trust established providers with their login credentials

### How It Works

1. Customer clicks "Sign in with Google" (or Apple/Microsoft) on your login page
2. They are redirected to the provider's secure login page
3. Customer authenticates with their provider credentials
4. Provider sends verified identity information back to your store
5. Customer is logged in automatically

On first login, a new customer account is created automatically using their email and profile information from the provider.

## Supported Providers

Spwig supports three major OAuth providers:

| Provider | Use Case | Credential Requirements |
|----------|----------|------------------------|
| **Google** | Most popular, easiest to set up | Client ID, Client Secret |
| **Apple** | Required for iOS apps, privacy-focused | Client ID, Team ID, Key ID, Private Key |
| **Microsoft** | Enterprise customers, Office 365 users | Client ID, Client Secret, Tenant ID |

You can enable one, two, or all three providers. Each operates independently.

## Setting Up Google OAuth

Google OAuth is the most popular option and the easiest to configure.

### Prerequisites

- A Google account
- Access to Google Cloud Console

### Step-by-Step Setup

1. **Navigate to OAuth Settings**
   - Go to **Settings > Store Settings** in your admin panel
   - Scroll to the **OAuth Providers** summary card
   - Click the **OAuth Dashboard** link to open the OAuth management page

2. **Create a Google Cloud Project**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Click **Create Project**
   - Enter a project name (e.g., "My Store OAuth")
   - Click **Create**

3. **Enable Google+ API**
   - In the left sidebar, go to **APIs & Services > Library**
   - Search for "Google+ API"
   - Click **Enable**

4. **Create OAuth Credentials**
   - Go to **APIs & Services > Credentials**
   - Click **Create Credentials > OAuth client ID**
   - Select application type: **Web application**
   - Enter a name (e.g., "Store Login")

5. **Configure Redirect URI**
   - Under **Authorized redirect URIs**, add:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Replace `yourdomain.com` with your actual domain
   - Click **Create**

6. **Copy Credentials**
   - Copy the **Client ID** and **Client Secret** from the popup

7. **Enter Credentials in Spwig**
   - Return to the OAuth Dashboard in your Spwig admin
   - Open the **Social Applications** section and add or edit the Google entry
   - Paste the **Client ID** and **Client Secret**
   - Click **Save**
   - Back on the OAuth Dashboard, set the **Google** provider to **Enabled**

### Testing

- Visit your storefront login page
- Look for the "Sign in with Google" button
- Click it and authenticate with your Google account
- You should be logged in and redirected to your customer dashboard

## Setting Up Apple OAuth

Apple OAuth is more complex than Google due to its key-based authentication system.

### Prerequisites

- An Apple Developer account (paid membership required)
- Access to Apple Developer portal

### Step-by-Step Setup

1. **Navigate to OAuth Settings**
   - Go to **Settings > Store Settings** and open the **OAuth Dashboard**

2. **Create a Service ID**
   - Log in to [Apple Developer](https://developer.apple.com/account/)
   - Go to **Certificates, Identifiers & Profiles**
   - Click **Identifiers** and then the **+** button
   - Select **Services IDs** and click **Continue**
   - Enter a description (e.g., "Store Login")
   - Enter an identifier (e.g., `com.yourstore.login`)
   - Click **Continue** and then **Register**

3. **Configure the Service ID**
   - Click on your newly created Service ID
   - Check **Sign In with Apple**
   - Click **Configure**
   - Add your domain and return URL:
     - **Domains**: `yourdomain.com`
     - **Return URLs**: `https://yourdomain.com/accounts/apple/login/callback/`
   - Click **Save** and then **Continue** and **Save** again

4. **Create a Key**
   - In the left sidebar, click **Keys** and then the **+** button
   - Enter a key name (e.g., "Store OAuth Key")
   - Check **Sign In with Apple**
   - Click **Configure** and select your Primary App ID
   - Click **Save**, then **Continue** and **Register**
   - **Download the key file** (.p8) — you cannot download it again

5. **Gather Required Information**
   You need:
   - **Client ID** (Service ID): The identifier you created (e.g., `com.yourstore.login`)
   - **Team ID**: Found in the top right of the Apple Developer portal
   - **Key ID**: Shown when you created the key
   - **Private Key**: The contents of the .p8 file you downloaded

6. **Enter Credentials in Spwig**
   - Return to the OAuth Dashboard in your Spwig admin
   - Open the **Social Applications** section and add or edit the Apple entry
   - Paste the Client ID, Team ID, and Key ID
   - Open the .p8 file in a text editor and copy its contents
   - Paste the entire key (including headers) into the **Key** field
   - Click **Save**
   - Back on the OAuth Dashboard, set the **Apple** provider to **Enabled**

### Testing

- Visit your storefront login page on a device with an Apple ID
- Click "Sign in with Apple"
- Authenticate with your Apple ID
- You should be logged in successfully

## Setting Up Microsoft OAuth

Microsoft OAuth is ideal for stores targeting business customers who use Office 365 or Azure AD.

### Prerequisites

- A Microsoft account
- Access to Azure Portal

### Step-by-Step Setup

1. **Navigate to OAuth Settings**
   - Go to **Settings > Store Settings** and open the **OAuth Dashboard**

2. **Register an Application in Azure**
   - Visit [Azure Portal](https://portal.azure.com/)
   - Go to **Azure Active Directory > App registrations**
   - Click **New registration**
   - Enter a name (e.g., "Store OAuth")
   - Select **Accounts in any organizational directory and personal Microsoft accounts**
   - Under **Redirect URI**, select **Web** and enter:
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - Click **Register**

3. **Copy Application ID**
   - On the app overview page, copy the **Application (client) ID**

4. **Create a Client Secret**
   - In the left sidebar, click **Certificates & secrets**
   - Click **New client secret**
   - Enter a description (e.g., "OAuth Secret")
   - Select an expiration period (recommended: 24 months)
   - Click **Add**
   - **Copy the secret value immediately** — it will not be shown again

5. **Enter Credentials in Spwig**
   - Return to the OAuth Dashboard in your Spwig admin
   - Open the **Social Applications** section and add or edit the Microsoft entry
   - Paste the Application (client) ID as **Client ID**
   - Paste the secret value as **Secret**
   - Optionally enter a Tenant ID (for single-tenant apps; leave blank for multi-tenant)
   - Click **Save**
   - Back on the OAuth Dashboard, set the **Microsoft** provider to **Enabled**

### Testing

- Visit your storefront login page
- Click "Sign in with Microsoft"
- Authenticate with your Microsoft account
- You should be logged in successfully

## Managing OAuth Connections

### Customer View

Customers can view and manage their connected OAuth providers from their account dashboard:

- Navigate to **My Account > Connected Accounts**
- See which providers are linked (Google, Apple, Microsoft)
- Disconnect a provider by clicking **Disconnect**
- Reconnect by logging in with that provider again

### Multiple Providers

A single customer account can be linked to multiple OAuth providers. For example, a customer can connect both Google and Apple to the same account.

If a customer tries to log in with a different OAuth provider using the same email address, Spwig automatically links it to their existing account.

### Admin Management

As an admin, you can view customer OAuth connections:

- Go to **Customers > Customers**
- Open a customer record
- Scroll to the **Connected Accounts** section
- View which providers are linked and when they were connected

You cannot disconnect providers on behalf of customers — they must do it themselves for security reasons.

## Troubleshooting

### Redirect URI Mismatch

**Error**: "Redirect URI mismatch" or "Invalid redirect_uri"

**Solution**:
- Ensure the redirect URI in your provider settings exactly matches the one in Spwig
- Check for trailing slashes — they must match
- Verify you are using `https://` (not `http://`)
- Clear your browser cache and try again

### Invalid Credentials

**Error**: "Invalid client ID" or "Authentication failed"

**Solution**:
- Double-check that you copied the Client ID and Client Secret correctly
- Ensure there are no extra spaces or line breaks
- Verify the credentials are from the correct project/app
- For Apple, ensure the Private Key includes the full contents of the .p8 file

### Provider API Not Enabled

**Error**: "API not enabled" or "Access not configured"

**Solution**:
- For Google: Ensure you enabled the Google+ API in your Google Cloud project
- For Microsoft: Verify your app registration is approved and active
- For Apple: Check that "Sign In with Apple" is enabled for your Service ID

### SSL Required

**Error**: "OAuth requires HTTPS" or "Insecure redirect URI"

**Solution**:
- OAuth providers require SSL/TLS (HTTPS) for security
- Ensure your store has a valid SSL certificate installed
- Update your redirect URIs to use `https://` instead of `http://`
- If testing locally, use a service like ngrok to create an HTTPS tunnel

### Button Not Appearing

**Issue**: The "Sign in with Google/Apple/Microsoft" button does not appear on the login page

**Solution**:
- Verify the provider is enabled in OAuth settings
- Clear your browser cache and refresh the page
- Check that your theme includes the social login template
- Review browser console for JavaScript errors

## Tips & Best Practices

### Security

- **Rotate secrets regularly** — Update Client Secrets every 12-24 months
- **Monitor failed login attempts** — Watch for unusual authentication patterns
- **Use separate credentials per environment** — Different credentials for staging and production
- **Restrict redirect URIs** — Only add the exact URIs you need

### User Experience

- **Enable all three providers** — Give customers choice; different demographics prefer different providers
- **Place buttons prominently** — Social login buttons should be above the email/password form
- **Use recognizable branding** — Keep the standard Google/Apple/Microsoft button styles
- **Test on mobile** — OAuth flows work differently on mobile browsers

### Compliance

- **Privacy Policy** — Disclose that you use OAuth providers and what data you receive
- **Terms of Service** — Comply with provider terms (Google, Apple, Microsoft each have requirements)
- **Data Minimization** — Only request the profile information you actually need

### Testing Checklist

Before going live, test:

- [ ] Login with each provider on desktop
- [ ] Login with each provider on mobile
- [ ] First-time login (account creation)
- [ ] Subsequent logins (account linking)
- [ ] Login with same email across different providers
- [ ] Disconnect and reconnect a provider
- [ ] Password reset flow still works for non-OAuth users
