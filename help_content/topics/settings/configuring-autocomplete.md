---
slug: configuring-autocomplete
title_i18n_key: Configuring Autocomplete
category: search
component: search
keywords:
  - autocomplete
  - search suggestions
  - predictive search
  - autocomplete settings
  - search as you type
  - instant search
  - autocomplete display
  - product thumbnails
  - search preview
  - autocomplete speed
  - debounce
  - autocomplete results
  - search dropdown
url_patterns:
  - /admin/search/searchsettings/
related:
  - search-settings-overview
  - search-performance-optimization
  - relevance-weights-deep-indexing
published: true
---

Autocomplete, also called predictive search or search-as-you-type, displays results while customers type their queries. This dramatically improves user experience by helping customers find products faster and reducing zero-result searches. This guide explains how to configure autocomplete behavior, display settings, and performance trade-offs.

Autocomplete is enabled by default with sensible settings. Only adjust these if you have specific performance concerns or display preferences.

![Autocomplete Settings](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Enabling Autocomplete

Navigate to **Search > Search Settings** and click the **Autocomplete** tab.

**Enable Autocomplete** - Master toggle for predictive search. When enabled, search inputs show results dropdown as customers type.

**Max Results Per Type** - Default: 8 items. How many results to show for each content type (products, categories, brands, blog posts). Lower values (5-6) reduce API payload size and render faster. Higher values (10-12) give customers more options but slow down response.

## Debounce Timing

⚠️ **PERFORMANCE WARNING** - Debounce timing significantly affects server load.

**Debounce Delay** - Default: 300ms. How long to wait after the last keystroke before triggering an autocomplete request.

This setting balances responsiveness with server load:

| Delay | User Experience | Server Impact |
|-------|----------------|---------------|
| **100ms** | Very responsive | 3x more API calls than 300ms - high load |
| **200ms** | Responsive | 1.5x more API calls than 300ms |
| **300ms** | Good balance (recommended) | Baseline |
| **400ms** | Slightly sluggish | Fewer API calls - lower load |
| **500ms** | Noticeably delayed | 50% fewer calls but feels slow |

**Recommendation**: Keep between 250-350ms. Only increase above 350ms if your server is struggling with autocomplete load. Never go below 200ms unless you have a very fast server and small catalog.

## Display Settings for Products

These toggles control what information appears in product autocomplete results:

**Show Thumbnail** - Default: ON. Displays product image next to result. **Performance impact**: Adds image query and increases JSON payload size. Disable for faster autocomplete on slow connections.

**Show Description** - Default: OFF. Displays product short description. **Performance impact**: Adds text processing and significantly increases payload size. Keep disabled unless descriptions are critical for product selection.

**Show Price** - Default: ON. Displays product price. **Performance impact**: Low - price data already loaded with product. Safe to keep enabled.

**Show SKU** - Default: ON. Displays product SKU. **Performance impact**: Low - SKU already indexed. Essential for B2B stores.

**Show Stock Status** - Default: OFF. **⚠️ MAJOR PERFORMANCE WARNING**

Displays "In Stock", "Low Stock", or "Out of Stock" badges. **NEVER enable this on large catalogs**.

Stock status requires `with_stock_totals()` aggregation - computing on_hand quantities across all warehouses for every product in autocomplete results. This adds:
- Significant database load (aggregation queries)
- 200-500ms additional latency on catalogs >1,000 products
- Potential timeouts on catalogs >10,000 products

Only enable if absolutely critical and you have <500 products.

## Display Settings for Blog Posts

**Show Featured Image** - Default: ON. Blog post thumbnail in autocomplete results.

**Show Excerpt** - Default: ON. Brief preview text from post content.

**Excerpt Length** - Default: 60 characters. How much preview text to show.

These settings have minimal performance impact since blog posts are typically few in number compared to products.

## Display Settings for Categories and Brands

**Show Thumbnail/Logo** - Default: ON. Category or brand image in results.

**Show Product Count** - Default: OFF. **⚠️ PERFORMANCE WARNING**

Displays how many products are in each category or brand (e.g., "Electronics (234)").

**NEVER enable this on large catalogs**. Product counts are recomputed on every autocomplete request:
- Each content type with counts enabled adds 2 extra queries
- Queries include joins and aggregations
- 100-300ms additional latency typical
- Increases linearly with number of categories/brands

Only enable if you have <50 categories/brands AND <1,000 products total.

## Caching

**Autocomplete Cache TTL** - Default: 60 seconds (set in Caching tab).

Autocomplete results are cached to improve performance. The 60-second TTL means:
- First customer searching "laptop" triggers database query
- Next 59 seconds, all "laptop" searches return cached results
- After 60 seconds, cache expires and next search refreshes data

**Recommendation for TTL**:
- **45-60s**: Good balance for most stores (default)
- **90-120s**: Better performance if product inventory changes rarely
- **30s**: More current results if you add products frequently

Increasing cache TTL is the single easiest way to improve autocomplete performance.

## Multi-Language Autocomplete

If you have multiple languages configured, autocomplete automatically searches translated content stored in JSONField translations.

**How it works**:
- Customer searches in Spanish: "zapatos"
- System searches Spanish product name translations
- Results show Spanish product names from JSONField data
- Falls back to base language if Spanish translation missing

**Performance**: Minimal overhead for 1-3 languages. With 5+ languages, slight increase in query complexity.

## Testing Autocomplete

After configuring settings, test the autocomplete experience:

1. **Open your store's homepage** in an incognito window
2. **Click the search box** to focus it
3. **Type a common product name** slowly (e.g., "laptop")
4. **Observe**:
   - How quickly results appear after you stop typing (debounce working?)
   - Which information displays (thumbnails, prices, SKUs as configured)
   - Whether results are relevant (check relevance weights if not)
5. **Test mobile** - Ensure dropdown is touch-friendly and readable

## Tips

- **Disable product descriptions for speed** - Descriptions significantly increase payload size with minimal value in autocomplete context
- **NEVER enable stock status on large catalogs** - Stock aggregation kills autocomplete performance
- **Test on mobile with touch targets** - Autocomplete results must be easily tappable on phones
- **Monitor response times weekly** - Target <200ms for autocomplete requests
- **Increase cache TTL if slow** - Easiest performance optimization
- **Product counts are expensive - disable unless critical** - Each category/brand count adds 2 queries to every autocomplete request
