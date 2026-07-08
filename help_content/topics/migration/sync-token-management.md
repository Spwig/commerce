---
slug: sync-token-management
title_i18n_key: Sync Token Management
category: migration
component: migration
keywords:
  - sync token
  - api token
  - authentication
  - spwig sync
  - connection
  - security
  - revoke token
  - generate token
url_patterns:
  - /admin/migration/syncjob/tokens/
related:
  - settings-sync
  - full-system-migration
published: true
---

Sync tokens are secure credentials that allow two Spwig installations to communicate with each other. Before you can sync settings or migrate data between stores, you need to generate a token on the **receiving** store and provide it to the **sending** store.

## How Sync Tokens Work

A sync token is a one-time-visible API key that authenticates requests between two Spwig installations. When you set up a connection, the remote store uses this token to prove it has permission to read from or write to your store.

- Tokens are generated on the store that will be **connected to** (the target)
- Each token can only be viewed once, immediately after generation
- Tokens can be revoked at any time to instantly cut off access
- A store can have multiple active tokens for different connections

## Generating a Token

1. Navigate to **Data Migration > Spwig-to-Spwig Sync** in the admin sidebar
2. Click **Manage Tokens** on the sync dashboard
3. Enter a descriptive name for the token (e.g., "Staging Server" or "Production Sync")
4. Click **Generate Token**
5. **Copy the token immediately** -- it will not be shown again

> **Important:** Store the token securely. If you lose it, you will need to generate a new one.

## Using a Token

Once you have a token from the target store:

1. Go to the **Spwig-to-Spwig Sync** dashboard on the store that will initiate the connection
2. Start a new **Settings Sync** or **Full Migration**
3. In the Connection step, enter the target store's URL and paste the token
4. Click **Test Connection** to verify it works
5. The connection will be saved for future use

## Revoking a Token

If a token is compromised or no longer needed:

1. Go to **Manage Tokens** on the sync dashboard
2. Find the token you want to revoke
3. Click the **Revoke** button
4. Confirm the revocation

Revoking a token takes effect immediately. Any active connections using that token will stop working and will need to be reconfigured with a new token.

## Best Practices

- **Name tokens descriptively** so you know which connection each token belongs to
- **Revoke unused tokens** to minimize security exposure
- **Generate separate tokens** for each connecting store rather than sharing one token across multiple stores
- **Regenerate tokens periodically** as part of your security routine, especially after staff changes
