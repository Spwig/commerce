---
slug: license-key-management
title_i18n_key: License Key Management
category: products
component: catalog
keywords:
  - license key
  - license template
  - license pool
  - license provider
  - software license
  - activation
  - key generation
  - external license
  - keygen
  - licensespring
  - cryptlex
  - key format
  - bulk keys
  - license sync
url_patterns:
  - /admin/catalog/licensekeytemplate/
  - /admin/catalog/licenseprovider/
  - /admin/catalog/licensepool/
  - /admin/catalog/licensekey/
related:
  - digital-products
  - add-product
published: true
---

License key management lets you control how software license keys are generated, stored, and delivered to customers when they purchase digital products. Spwig supports built-in key generation, pre-loaded key pools, and integrations with external license management services.

## Overview

There are three ways to manage license keys in Spwig:

| Method | Best for |
|--------|---------|
| **License templates** | Automatically generate unique keys in a custom format at the time of purchase |
| **License pools** | Pre-generate a batch of keys in advance for bulk distribution |
| **External providers** | Delegate key generation and management to a third-party service like Keygen.sh |

These methods can be combined — for example, a pool can use a custom template to define the key format, and can optionally sync generated keys to an external provider.

## License key templates

A license key template defines the *format* of generated keys. Templates use a pattern with placeholders that Spwig fills in at generation time.

### Creating a template

1. Navigate to **Catalog > License Key Templates**
2. Click **+ Add License Key Template**
3. Enter a **Name** (e.g., `Standard App License`)
4. Configure the **Pattern** using placeholders (see below)
5. Set the **Prefix** and **Suffix** if needed (e.g., a prefix of `MYAPP` adds `MYAPP-` to every key)
6. Choose the **Separator** character (default: `-`)
7. Set the **Character Set** — the characters used for random segments. The default excludes ambiguous characters like `0` and `O`, `1` and `I`
8. Set **Min/Max Length** for validation
9. Click **Save**

### Pattern placeholders

| Placeholder | Description | Example output |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N random characters from the character set | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | N-digit checksum for validation | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | The template's prefix value | `MYAPP` |
| `{SUFFIX}` | The template's suffix value | `PRO` |
| `{ORDER_ID}` | The order number | `10045` |
| `{PRODUCT_SKU}` | The product's SKU | `SOFTPRO` |
| `{DATE:FORMAT}` | Formatted date | `{DATE:YYMMDD}` → `260318` |

**Example pattern**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

This produces keys like: `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Previewing keys

After saving a template, a **Generate Sample Key** action is available on the template list. Use this to verify your pattern produces keys in the expected format before assigning the template to a product.

## License pools

A license pool is a batch of pre-generated keys for a product. Pools are useful when:
- You need keys for physical packaging (retail boxes, printed cards)
- You work with resellers who need batches of keys
- You want keys generated in advance rather than on demand

### Creating a license pool

1. Navigate to **Catalog > License Pools**
2. Click **+ Add License Pool**
3. Fill in the pool details:

| Field | Description |
|-------|-------------|
| **Name** | Descriptive name (e.g., `Retail Pack Q1 2026`) |
| **Product** | The product these keys are for |
| **License Template** | Template for key format (defaults to the product's template) |
| **Total Keys** | How many keys to generate |
| **Key Type** | Perpetual, subscription, or trial |
| **Max Activations** | How many devices each key can activate on |
| **Expires After Days** | Days until the license expires after first activation (leave blank for no expiry) |
| **Pool Expires At** | Date after which unused keys from this pool become invalid |
| **Sync to Provider** | Optionally sync generated keys to an external license provider |

4. Click **Save** — Spwig begins generating the keys in the background

### Pool status

| Status | Meaning |
|--------|---------|
| **Generating** | Keys are being created in the background |
| **Ready** | All keys generated and available for distribution |
| **Depleted** | All keys have been assigned to orders |
| **Expired** | The pool's expiry date has passed |

### Monitoring a pool

The pool list shows how many keys have been distributed vs. total keys generated. Open a pool to see the full list of keys and their individual statuses.

## External license providers

External providers are third-party license management services that handle key generation and activation tracking. When a customer completes a purchase, Spwig communicates with the provider to generate and register the key.

### Supported providers

| Provider | Type |
|----------|------|
| **Spwig Built-in License Server** | Built-in — no external account needed |
| **Keygen.sh** | Cloud-based license management API |
| **LicenseSpring** | Enterprise license management |
| **Cryptlex** | License management with offline support |
| **Custom API** | Any REST-based license system |

### Connecting a provider

1. Navigate to **Catalog > License Providers**
2. Click **+ Add License Provider**
3. Fill in the provider details:

| Field | Description |
|-------|-------------|
| **Name** | A label for this connection (e.g., `Keygen Production`) |
| **Provider Type** | Select from the supported providers |
| **API Endpoint** | The provider's API base URL |
| **API Key** | Authentication key for the provider |
| **API Secret** | If required by the provider |

4. Configure sync behaviour:
   - **Sync on Order** — Automatically sync when a customer completes a purchase
   - **Sync on Activation** — Report device activations to the provider
   - **Sync on Deactivation** — Report deactivations (useful for licence transfers and refunds)
   - **Bidirectional Sync** — Allow the provider to update Spwig records via webhooks

5. Click **Save**, then click **Test Connection** to verify the credentials work

### Connection status

Each provider shows one of three connection statuses:

| Status | Meaning |
|--------|---------|
| **Not Tested** | Connection has not been verified yet |
| **Connected** | Last test was successful |
| **Error** | Connection test failed — check the error message |

### Syncing existing licenses

To manually push existing license keys to a provider (for initial setup or after a failed sync), use the **Sync Now** action from the provider list.

## Monitoring sync activity

Navigate to **Catalog > External License Syncs** to review the sync log. Each record shows:
- The license key that was synced
- The provider it was sent to
- Direction (Spwig → Provider or Provider → Spwig)
- Status (Pending, Success, Failed)
- Error details for failed syncs

Failed syncs are retried automatically. You can also force a retry by editing the record and clearing the error.

## Tips

- Use the default character set (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) to avoid ambiguous characters that customers often misread — it excludes `0`, `O`, `1`, and `I`.
- Add a `{CHECKSUM}` segment to your template pattern so customers and your support team can quickly detect mistyped keys.
- For high-volume products, use a pool rather than on-demand generation to ensure keys are delivered instantly at checkout.
- Set **Pool Expires At** on seasonal or time-limited key batches so old unused keys are automatically invalidated.
- Always test the provider connection after setup and after any credential changes — a broken connection means customers do not receive their keys.
- If using bidirectional sync, configure your provider's webhook URL to point to your store's license webhook endpoint.
