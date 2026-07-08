---
slug: geoip-setup
title_i18n_key: GeoIP Setup
category: customers
component: geoip
keywords:
  - GeoIP
  - geolocation
  - IP lookup
  - geographic tracking
  - location provider
  - MaxMind
  - IP2Location
  - DB-IP
  - CDN headers
  - visitor country
  - IP address location
  - setup geolocation
url_patterns:
  - /admin/geoip/geoipprovider/
  - /admin/geoip/geolocation/
  - /admin/geoip/countrymapping/
related:
  - visitor-analytics
  - business-rules
  - customer-analytics
published: true
---

GeoIP lets your store automatically detect where each visitor is coming from based on their IP address. This powers location-based features throughout your store — from showing the right currency by default, to running geographic business rules, to seeing country-level breakdowns in your analytics.

Your store comes pre-configured with the Spwig GeoIP service, so geographic detection works out of the box. You can also connect additional providers for higher accuracy, use a database you download yourself, or rely on headers from a CDN for zero-latency lookups.

## How providers work

Navigate to **Customers > GeoIP Providers** to see the providers configured for your store. Each provider handles IP-to-location lookups using a different method. When a visitor arrives, your store queries the active providers in priority order and uses the first successful result.

Multiple providers can be active at once — lower priority numbers are tried first. If the highest-priority provider fails or returns no data, the next one is tried automatically.

### Available provider types

| Provider | Description |
|----------|-------------|
| **Spwig GeoIP** | Default cloud-based lookup via Spwig's service. Requires no setup. |
| **MaxMind GeoLite2** | Offline database from MaxMind. High accuracy. Requires a free license key. |
| **DB-IP Lite** | Offline database from DB-IP. Download from their website. |
| **IP2Location LITE** | Offline database from IP2Location. Requires a free registration. |
| **CDN Edge Headers** | Reads location headers injected by your CDN (e.g., Cloudflare). Zero latency. |
| **Browser Hints** | Uses browser-provided timezone/language as a soft location signal. |
| **Custom Provider** | A provider component installed from the Spwig component marketplace. |

## Adding a provider

### Using the Spwig GeoIP service (default)

The Spwig GeoIP provider is added automatically on new installations. Check that it appears in the list and that **Is Active** is checked. No additional configuration is required.

### Adding a MaxMind GeoLite2 database

MaxMind offers a free offline database that gives accurate results without sending lookups to an external service.

1. Register for a free account at maxmind.com and generate a license key
2. Navigate to **Customers > GeoIP Providers** and click **+ Add GeoIP Provider**
3. Fill in the form:
   - **Name**: `MaxMind GeoLite2` (or any descriptive name)
   - **Provider Type**: MaxMind GeoLite2
   - **Is Active**: checked
   - **Priority**: `1` (lower than the Spwig default to try it first, or higher to use as fallback)
   - **License Key**: paste your MaxMind license key
   - **Database URL**: the download URL from your MaxMind account dashboard
4. Click **Save**

After saving, select the provider in the list and use the **Update selected provider databases** action to verify the database URL is reachable.

### Adding CDN edge headers

If your store sits behind a CDN that injects geolocation headers (such as Cloudflare's `CF-IPCountry`), you can use those headers for instant, zero-latency country detection.

1. Navigate to **Customers > GeoIP Providers** and click **+ Add GeoIP Provider**
2. Set **Provider Type** to **CDN Edge Headers**
3. Set **Priority** to `0` (highest priority, since headers are the fastest source)
4. In the **Config** field, specify which header your CDN uses:
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. Click **Save**

### Testing a provider

After adding a provider, you can verify it is working correctly:

1. In the GeoIP Providers list, select the provider using its checkbox
2. Open the **Action** dropdown and choose **Test selected providers**
3. Click **Go**

Spwig will send a test lookup for a known IP address (Google's public DNS, `8.8.8.8`) and show you the result. A successful test displays the country returned and the response time in milliseconds.

## Setting provider priority

When multiple providers are active, the **Priority** field controls which is tried first. Lower numbers mean higher priority.

For example, to use CDN headers first (fastest) and fall back to Spwig GeoIP:

| Provider | Priority |
|----------|----------|
| CDN Edge Headers | 0 |
| Spwig GeoIP | 10 |

You can edit the priority directly in the list view — the **Priority** column is editable inline.

## Monitoring provider performance

Each provider record tracks its own accuracy statistics:

- **Total Lookups** — total number of IP lookups attempted
- **Successful Lookups** — lookups that returned a result
- **Failed Lookups** — lookups that returned no data or an error
- **Average Response (ms)** — mean response time in milliseconds
- **Accuracy** — percentage of successful lookups

If a provider shows a low accuracy rate or high response times, consider adjusting its priority or disabling it in favor of a better-performing option.

## Country mappings

Navigate to **Customers > Country Mappings** to configure per-country defaults for currency, language, tax, and shipping. Each country entry controls:

- **Default Currency** — the currency pre-selected for visitors from that country
- **Default Language** — the language shown to visitors from that country
- **Tax Rate** — the default tax percentage applied for that country
- **Is EU Member** / **Requires VAT** — used for EU tax compliance logic
- **Shipping Zone** — links the country to a shipping zone
- **Supports COD** — enables Cash on Delivery for that country

You can edit the **Is Active**, **Default Currency**, and **Default Language** fields directly in the list without opening each record.

## Tips

- The Spwig GeoIP provider works immediately without configuration — only add extra providers if you need higher accuracy or offline operation
- If you use Cloudflare, the CDN Edge Headers provider is the best choice: it adds no latency and does not count against any API quota
- Keep only the providers you actually need active — having many active providers does not improve accuracy if the first one already succeeds
- Check the accuracy statistics weekly and disable any provider with a success rate below 80%
- Country mappings are used as defaults; customers can always change their currency and language manually in the storefront
