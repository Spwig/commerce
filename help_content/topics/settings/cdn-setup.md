---
slug: cdn-setup
title_i18n_key: CDN Setup
category: settings
component: core
keywords:
  - CDN
  - content delivery network
  - performance
  - page speed
  - caching
  - Cloudflare
  - CloudFront
  - global delivery
  - latency
  - static assets
  - speed optimization
  - international customers
url_patterns:
  - /admin/
related:
  - store-settings
  - search-performance-optimization
  - shipping-zones
published: true
---

A Content Delivery Network (CDN) stores copies of your store's images, stylesheets, and scripts on servers around the world. When a customer visits your store, these files are served from the server closest to them rather than from your main hosting server. This reduces page load times, especially for customers located far from where your store is hosted.

Spwig already optimizes static asset delivery out of the box with Brotli and gzip pre-compression, fingerprinted asset caching with 1-year immutable headers, and proper content negotiation. Adding a CDN is optional, but it can further improve speed for stores with an international customer base.

## Does Your Store Need a CDN?

Not every store benefits equally from a CDN. Use these guidelines to decide:

**A CDN is recommended if**:
- Your customers are spread across multiple countries or continents
- Your store features many product images or media-heavy pages
- You want the fastest possible page load times worldwide
- You sell to regions far from your hosting server (e.g., server in Europe, customers in Asia)

**A CDN is likely unnecessary if**:
- Your customers are mostly local or within the same country as your server
- Your store has a small catalog with few images
- Your hosting provider already includes a built-in CDN

When in doubt, a CDN does not hurt performance. Services like Cloudflare offer free tiers, so there is no cost to try.

## How Spwig Works with CDNs

Spwig is CDN-ready by default. You do not need to change any code or settings inside your Spwig admin panel. Here is what Spwig already does for you:

- **Fingerprinted static files** -- Every CSS, JavaScript, and image file includes a unique version hash in its filename. This means CDNs can safely cache these files for a long time without serving outdated content.
- **Long-lived cache headers** -- Static assets are served with 1-year immutable cache headers, telling CDNs and browsers to cache them aggressively.
- **Pre-compressed files** -- Spwig pre-compresses assets using Brotli and gzip, so your CDN can deliver smaller files without extra processing.
- **Proper content negotiation** -- Spwig sends the correct content-type and encoding headers that CDNs rely on for proper caching.

All you need to do is point your domain's DNS to the CDN provider, and everything works automatically.

## Setting Up Cloudflare

Cloudflare is the most popular CDN and offers a free tier that works well for most stores. Follow these steps:

**Step 1: Create a Cloudflare Account**
- Visit cloudflare.com and sign up for a free account

**Step 2: Add Your Domain**
- Click **Add a Site** and enter your store's domain name
- Select the **Free** plan (sufficient for most stores)

**Step 3: Update Your DNS Nameservers**
- Cloudflare will show you two nameservers (e.g., `anna.ns.cloudflare.com`)
- Log in to your domain registrar (where you purchased your domain)
- Replace your current nameservers with the Cloudflare nameservers
- DNS changes can take up to 24 hours to take effect

**Step 4: Configure SSL/TLS**
- In the Cloudflare dashboard, go to **SSL/TLS**
- Set the encryption mode to **Full (strict)**
- This ensures all traffic between Cloudflare and your server stays encrypted

**Step 5: Verify It Is Working**
- Once DNS propagates, visit your store and check for the `cf-cache-status` header in your browser (see Verifying Your CDN below)

## Setting Up AWS CloudFront

If you already use Amazon Web Services, CloudFront integrates naturally with your infrastructure:

1. Open the **CloudFront** console in your AWS account
2. Create a new **Distribution** with your store's domain as the origin
3. Set the **Origin Protocol Policy** to "HTTPS Only"
4. Under **Cache Behavior**, set **Cache Policy** to "CachingOptimized" for static assets
5. Add your store's domain as an **Alternate Domain Name (CNAME)**
6. Attach an SSL certificate from AWS Certificate Manager
7. Update your domain's DNS to point to the CloudFront distribution URL

CloudFront pricing is usage-based. For most stores, costs are minimal since Spwig's fingerprinted assets are cached for long periods.

## Recommended CDN Settings

For the best results, configure your CDN to cache the right content and skip the rest.

**What to cache** (static assets):
- `/static/` -- All stylesheets, scripts, fonts, and theme assets
- `/media/` -- Product images and uploaded media files
- Image files (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- Font files (`.woff`, `.woff2`)

**What NOT to cache** (dynamic pages):
- `/admin/` -- The admin panel must always serve fresh content
- `/cart/` -- Shopping cart pages contain session-specific data
- `/checkout/` -- Checkout pages must never be cached for security
- `/accounts/` -- Customer account pages contain private data
- Any page that requires login or shows personalized content

**General caching rules**:
- **Respect origin cache headers** -- Spwig sends the correct cache-control headers for each type of content. Configure your CDN to honor these headers rather than overriding them.
- **Enable Brotli compression** -- Both Cloudflare and CloudFront support Brotli. Enable it to take advantage of Spwig's pre-compressed assets.
- **Set Browser Cache TTL to "Respect Existing Headers"** -- This lets Spwig's built-in cache policy drive behavior.

## Verifying Your CDN

After setup, confirm that the CDN is serving your content correctly:

**Step 1: Open Browser Developer Tools**
- In Chrome or Firefox, press **F12** to open developer tools
- Click the **Network** tab

**Step 2: Load Your Store**
- Visit your store's homepage with developer tools open
- Click on any static file request (e.g., a `.css` or `.js` file)

**Step 3: Check the Response Headers**
- **Cloudflare**: Look for the `cf-cache-status` header. A value of `HIT` means the file was served from the CDN cache. `MISS` means it was fetched from your server (first request only).
- **CloudFront**: Look for the `x-cache` header. A value of `Hit from cloudfront` confirms CDN delivery.

**Step 4: Test from Another Location**
- Use a free tool like gtmetrix.com or webpagetest.org to test your store from different geographic locations
- Compare load times before and after CDN setup

## Common Issues

### Stale Content After Theme Changes

**Problem**: After updating your theme or making design changes, customers still see the old version.

**Solution**: Clear your CDN cache. In Cloudflare, go to **Caching > Configuration > Purge Everything**. In CloudFront, create an **Invalidation** for `/*`. Note that Spwig's fingerprinted assets usually prevent this issue since updated files get new filenames automatically. This problem most commonly affects non-fingerprinted assets like custom uploads.

---

### Mixed Content Warnings

**Problem**: Your browser shows a security warning about "mixed content" after enabling the CDN.

**Solution**: Ensure your CDN's SSL mode is set to **Full (strict)**, not "Flexible". Flexible mode can cause your server to receive HTTP requests instead of HTTPS, leading to mixed content warnings. In Cloudflare, check **SSL/TLS > Overview** and verify the mode.

---

### Admin Panel Running Slowly

**Problem**: The admin panel feels slower after adding a CDN.

**Solution**: CDNs should not cache admin pages. Create a **Page Rule** (Cloudflare) or **Cache Behavior** (CloudFront) that sets caching to "Bypass" for any URL matching `/admin/*`. This ensures admin requests go directly to your server without CDN overhead.

---

### Images Not Loading

**Problem**: Product images or media files return errors after CDN setup.

**Solution**: Verify that your CDN's origin is configured with the correct protocol (HTTPS) and port. Also check that your server's firewall allows connections from the CDN's IP ranges.

## Tips

- **Start with Cloudflare's free tier** -- It covers the needs of most stores and takes only minutes to set up
- **Always use Full (strict) SSL mode** -- Flexible mode creates security vulnerabilities and can break checkout flows
- **Clear your CDN cache after major theme updates** -- Although Spwig's fingerprinted files handle most cases, a full cache purge ensures no stale content lingers
- **Do not cache checkout or cart pages** -- Caching these pages can expose one customer's data to another
- **Test from your customers' locations** -- Use free tools like webpagetest.org to measure real-world performance from the regions where your customers shop
- **Monitor your CDN analytics** -- Both Cloudflare and CloudFront provide dashboards showing cache hit rates, bandwidth saved, and traffic by country
- **Keep your DNS TTL low during setup** -- Set DNS TTL to 300 seconds (5 minutes) while switching to a CDN, then increase it once everything is confirmed working
- **A CDN does not replace good hosting** -- Your origin server still matters for dynamic pages like checkout, cart, and admin. Choose quality hosting alongside a CDN
