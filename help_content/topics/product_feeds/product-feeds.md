---
slug: product-feeds
title_i18n_key: Product Feeds
category: marketing-seo
component: product_feeds
keywords:
  - product feed
  - Google Shopping
  - Facebook Catalog
  - product catalog feed
  - feed provider
  - feed sync
  - XML feed
  - CSV feed
  - feed generation
  - shopping ads
  - product data export
  - feed download
  - sync schedule
  - feed management
url_patterns:
  - /admin/product_feeds/feedprovideraccount/
  - /admin/product_feeds/productfeed/
  - /admin/product_feeds/feedsynclog/
related:
  - add-product
  - manage-categories
published: true
---

Product feeds let you export your catalog to shopping platforms such as Google Shopping and Facebook Catalog. Once connected, your product data is automatically synchronized on a schedule so your ads always reflect your current prices, stock, and product details.

Your store uses a provider component system for feeds. Each feed provider (Google, Facebook, or others) is installed as a component and then connected through a provider account. You can run multiple feed providers at the same time — for example, one feed for Google Shopping and a separate one for Facebook.

## Connecting a feed provider

Before you can sync your catalog, you need to install and connect at least one feed provider component.

### Installing a provider component

Provider components are available in the Spwig component marketplace. Your store administrator installs them through the component update system. Once a provider component is installed, it appears as an option when creating a feed provider account.

### Creating a feed provider account

1. Navigate to **Marketing > Feed Providers**
2. Click **+ Add Feed Provider Account**
3. Fill in the form:

**Provider Information section:**
- **Site** — select your store (there is only one)
- **Provider Component** — choose the installed feed provider (e.g., Google Shopping, Facebook Catalog)
- **Account Name** — a descriptive name such as `Google Shopping — Main` or `Facebook Catalog — US`

**Configuration section:**
- **Is Active** — check to enable feed generation and syncing
- **Is Primary** — check if this is your main feed provider for this platform type
- **Priority** — controls the sort order in the list (lower numbers appear first)
- **Config** — provider-specific settings (see below)

4. Click **Save**

### Feed configuration options

The **Config** field accepts a JSON object with the following options:

| Option | Values | Description |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | How often the feed is automatically regenerated |
| `format_preference` | `xml`, `csv`, `json` | Output format (most platforms prefer XML) |
| `include_variants` | `true` / `false` | Include product variants as separate feed entries |
| `target_country` | Country code e.g. `"US"` | Target country for the feed |
| `content_language` | Language code e.g. `"en"` | Language of the product data |

#### Example configuration for daily XML feed targeting the US:

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Filtering which products appear in the feed

You can control exactly which products are included by adding a `product_filter` section to the config:

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Filter option | Description |
|---------------|-------------|
| `status` | Only include products with these statuses. Use `["published"]` for live products only. |
| `in_stock_only` | Set to `true` to exclude out-of-stock products |
| `categories` | Limit to specific category IDs |
| `brands` | Limit to specific brand IDs |

You can also exclude specific products by their IDs using `exclude_products`:

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Monitoring sync status

The feed provider accounts list shows the sync status of each connected feed at a glance:

- **PENDING** — no sync has run yet, or the feed is waiting to be generated
- **SYNCING** — a sync is currently in progress
- **SUCCESS** — the last sync completed without errors
- **ERROR** — the last sync failed; the error message is shown on the account detail page

The list also shows the number of products in the current feed and when the last sync ran.

## Viewing generated feeds

Navigate to **Marketing > Product Feeds** to see the generated feed files. Each entry represents one generated feed snapshot and shows:

- **Provider Account** — which feed this belongs to
- **Format** — XML, CSV, or JSON
- **Product Count** — number of products included
- **Size** — file size of the generated feed
- **Generated At** — when it was created
- **Expires At** — when this cached version expires
- **Status** — whether the feed is still valid or has expired
- **Download Count** — how many times this feed has been downloaded

Feeds are read-only in the admin — they are generated automatically by the sync process.

## Viewing sync history

Navigate to **Marketing > Feed Sync Logs** to see a full history of every sync attempt for all your feed accounts. Each log entry records:

- The provider account that was synced
- The sync type (Full, Incremental, Manual, or Scheduled)
- Status (Success, Partial Success, Failed, etc.)
- Products synced, failed, and skipped
- Duration of the sync
- Any error messages

The sync log dashboard at the top of the page shows overall statistics: total syncs, success rate, and average sync duration. Use the **Account** and **Sync Type** filters to narrow down to a specific feed.

### What to do when a sync fails

1. Navigate to **Marketing > Feed Sync Logs** and find the failed entry
2. Click the log entry to view the full **Error Message** and **Error Details**
3. Common causes include:
   - Missing required product fields (title, price, image)
   - Invalid or expired API credentials — reinstall the provider component to refresh credentials
   - Network errors connecting to the provider's API
4. Once the issue is resolved, the next scheduled sync will run automatically, or you can trigger a manual sync from the provider account

## Tips

- Set `"sync_interval": "daily"` for most use cases — Google and Facebook don't require more frequent updates unless you have very high price volatility
- Always include `"in_stock_only": true` in your product filter to avoid advertising products customers can't buy
- Use a descriptive account name that includes the platform and target market (e.g., `Google Shopping — UK`) so it's easy to manage multiple feeds
- The **Products in Feed** count on the provider account tells you immediately if fewer products than expected are being included — check your product filter settings if the count seems low
- Mark one account as **Primary Feed** for each provider type; some reporting tools use this to identify your main feed
- Review the sync log after any bulk changes to your product catalog to confirm the updated data was picked up correctly
