---
slug: search-settings-overview
title_i18n_key: Understanding Search Settings
category: search
component: search
keywords:
  - search settings
  - configure search
  - search configuration
  - enable search
  - search options
  - autocomplete settings
  - search preferences
  - store search
  - product search
  - search setup
  - search system
  - search controls
url_patterns:
  - /admin/search/searchsettings/
related:
  - search-engines-explained
  - configuring-autocomplete
  - search-performance-optimization
  - relevance-weights-deep-indexing
published: true
---

The SearchSettings interface controls all global search behavior in your Spwig store. This single configuration page uses an 8-tab interface to organize search options, from basic enablement to advanced performance tuning. Changes here apply to all search engines unless overridden at the engine level.

This guide walks through each tab, explaining what each setting does and when to adjust it.

![Search Settings General Tab](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## The 8-Tab Interface

SearchSettings is a singleton model - only one configuration record exists (pk=1) for your entire store. The interface is divided into eight tabs:

| Tab | Purpose |
|-----|---------|
| **General** | Enable/disable search, set basic parameters |
| **Autocomplete** | Configure predictive search dropdown behavior |
| **Content Types** | Choose which types of content are searchable |
| **Deep Indexing** | Control what product data gets indexed (performance impact) |
| **Fuzzy Matching** | Typo tolerance and similarity thresholds |
| **Weights** | Relevance multipliers for ranking results |
| **Caching** | Response time vs freshness trade-offs |
| **Analytics** | Query tracking and privacy settings |

Each tab focuses on a specific aspect of search configuration.

## General Tab

The General tab contains core settings that affect all searches:

**Enable Search** - Master toggle for the search system. When disabled, all search features are inactive across your store, including autocomplete and the search results page.

**Minimum Query Length** - Default: 2 characters. Searches shorter than this are rejected. Setting this to 1 allows single-character searches (e.g., "A") but increases server load.

**Results Per Page** - Default: 20 items. Controls pagination for search results pages. Higher values (30-50) reduce pagination clicks but increase page load time.

## Content Types Tab

![Content Types Settings](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Toggle which content types appear in search results:

- **Products** - Physical, digital, and subscription products
- **Categories** - Product categories
- **Brands** - Product brands
- **Blog Posts** - Blog content

**Performance Note**: Fewer content types = faster searches. Each enabled type adds additional database queries. If you don't have a blog, disable Blog Posts to improve response times.

## Deep Indexing Tab

⚠️ **PERFORMANCE WARNING** - These settings have significant performance implications.

![Deep Indexing Settings](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Deep indexing controls what product-related data gets included in searches:

**Index SKUs** - Default: ON, Low impact. Includes product and variant SKUs in search. Essential for B2B stores where customers search by product codes.

**Index Attributes** - Default: ON, Medium impact. Includes product attributes (color, size, material) in search. Adds JOIN to attributes table. Important for fashion and configurable products.

**Index Custom Fields** - Default: ON, Medium impact. Includes merchant-defined custom fields in search results. Requires JSONField traversal.

**Index Reviews** - Default: ON, Medium-High impact. Includes approved review titles and comments in search. Joins to reviews table and adds text search overhead. Helpful for review-heavy catalogs.

**Index Documents** - Default: OFF, **VERY HIGH IMPACT** ⚠️

Document indexing extracts text from PDF, DOCX, and XLSX files attached to digital products. This feature:

- Requires very expensive initial indexing
- Adds significant query overhead on every search
- Can cause timeouts on large files
- **Should ONLY be enabled for digital product stores with searchable documents**
- **NEVER enable casually** - test performance impact thoroughly

## Fuzzy Matching Tab

![Fuzzy Matching Settings](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

Fuzzy matching uses Levenshtein distance to handle typos:

**Enable Fuzzy Matching** - Allows searches to match similar terms (e.g., "laptop" matches "labtop")

**Similarity Threshold** - Default: 0.80 (80% similarity). Range: 0.0-1.0. Higher values require closer matches and run faster. Lower values catch more typos but may return irrelevant results.

**Max Edit Distance** - Default: 2 character changes. Maximum number of insertions, deletions, or substitutions allowed. Lower values (1) improve performance but catch fewer typos.

## Weights Tab

Weights control relevance scoring - how results are ranked. The Weights tab shows default multipliers for each searchable field:

- weight_name: 1.50 (product names most important)
- weight_sku: 1.20
- weight_description: 0.80
- weight_categories: 0.80
- weight_attributes: 0.70
- weight_brands: 0.70
- weight_blog_posts: 0.60
- weight_reviews: 0.50

These defaults work well for most e-commerce stores. For detailed information on adjusting weights and understanding their impact, see the [Relevance Weights and Deep Indexing](/en/admin/help/relevance-weights-deep-indexing/) topic.

## Caching Tab

![Caching Settings](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

Caching dramatically improves search performance by storing recent results:

**Autocomplete Cache TTL** - Default: 60 seconds. How long autocomplete results are cached. Shorter TTL (30-45s) = fresher results but more database queries. Longer TTL (90-120s) = faster but potentially stale results.

**Results Cache TTL** - Default: 300 seconds (5 minutes). Full search results page cache duration. Longer TTL significantly improves performance but delays visibility of new products.

**Trade-offs**: Caching is the single most effective performance optimization. If searches are slow, increase these values before disabling features.

## Analytics Tab

![Analytics Settings](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Track Search Queries** - Enables search analytics dashboard. Records query text, result count, response time, and timestamp.

**Track User Information** - Associates searches with logged-in users. Disable for privacy compliance (GDPR, CCPA).

**Track Session Information** - Uses session IDs to track anonymous user searches. Useful for identifying search patterns without personal data.

## Singleton Pattern

SearchSettings uses a singleton pattern - only one settings record exists in your database (pk=1). When you navigate to Search Settings in the admin, you're always editing the same record.

There is no "Add" or "Delete" option - just "Change". All search engines inherit these settings unless they specify per-engine overrides (rare).

## Tips

- **Keep defaults unless you have a specific need** - The default settings are optimized for typical e-commerce stores
- **NEVER enable document indexing casually** - Only for digital product stores with searchable documents, and test performance impact first
- **Monitor response times in analytics** - Target <200ms for autocomplete, <500ms for full search
- **Increase cache TTL if performance is slow** - Caching is the easiest performance win
- **Review zero-result queries weekly** - They reveal missing products or needed synonyms
- **Disable unused content types** - If you don't have a blog, turn off Blog Posts to speed up searches
