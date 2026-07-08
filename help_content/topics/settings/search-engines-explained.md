---
slug: search-engines-explained
title_i18n_key: Search Engines Explained
category: search
component: search
keywords:
  - search engine
  - multiple search engines
  - context search
  - shop search
  - blog search
  - search configuration
  - content filtering
  - search exclusions
  - search wizard
  - custom search
url_patterns:
  - /admin/search/searchengine/
  - /admin/search/searchengine/add/
  - /admin/search/engine/wizard/step-1/
related:
  - search-settings-overview
  - managing-synonyms-redirects
  - search-performance-optimization
published: true
---

Search engines in Spwig are not external services like Elasticsearch or Algolia - they're configuration contexts within your store's database-native search system. Each engine defines which content types to search, what to exclude, and how results should be ranked. This guide explains what search engines are, when to create multiple engines, and how to configure them.

Most merchants use a single default "shop" engine. Create multiple engines only when you need different content mixes or exclusions for different use cases.

![Search Engines List](/static/core/admin/img/help/search-engines-explained/search-engines-list.webp)

## What Are Search Engines?

A search engine in Spwig is a named configuration that specifies:

- **Which content types to search** (products, categories, brands, blog posts)
- **What to exclude** (specific categories or brands you want hidden from search)
- **Custom relevance weights** (optional per-engine weight overrides)
- **Active status** (engines can be temporarily disabled)

Each engine has a unique slug used in API calls and frontend code to specify which engine should handle a search request.

## When to Create Multiple Engines

Most stores need only one engine. Create additional engines for these scenarios:

| Use Case | Example |
|----------|---------|
| **Different content mixes** | Shop engine searches products only; Blog engine searches blog posts only |
| **Selective exclusions** | Main shop engine hides clearance category; Clearance engine shows only clearance items |
| **Department-specific search** | Electronics engine excludes clothing categories; Clothing engine excludes electronics |
| **B2B vs B2C separation** | Wholesale engine shows only bulk products; Retail engine shows consumer products |

If you're not sure whether you need multiple engines, stick with one. Adding engines creates complexity without benefits unless you have a specific use case.

## The 4-Step Wizard

![Wizard Step 1 - Basic Info](/static/core/admin/img/help/search-engines-explained/wizard-step1-basic.webp)

Navigate to **Search > Setup Wizard** to create a new engine through a guided 4-step process:

### Step 1: Basic Information

**Engine Name** - Friendly display name (e.g., "Shop Search", "Blog Search"). Used in admin interface only.

**Slug** - URL-safe identifier (e.g., "shop-search", "blog-search"). Used in API calls and frontend code. Auto-generated from name if left blank.

**Active** - Whether this engine is available for searches. Inactive engines return no results.

### Step 2: Content Types

Select which types of content this engine will search:

- Products (includes all product types: physical, digital, subscriptions)
- Categories
- Brands
- Blog Posts

**Tip**: Select only content types relevant to this engine's purpose. A blog-focused engine doesn't need products enabled.

### Step 3: Weights (Optional)

![Wizard Step 3 - Weights](/static/core/admin/img/help/search-engines-explained/wizard-step3-weights.webp)

Optionally customize relevance weights for this specific engine. If skipped, the engine inherits global weights from SearchSettings.

Most engines should skip this step and use global defaults. Only customize weights if this engine has unique ranking needs (e.g., a blog engine might increase weight_blog_posts to 1.2).

### Step 4: Review & Create

Review your configuration and click **Create Engine** to save.

## Engine Configuration Fields

If you edit an engine directly (bypassing the wizard), you'll see these fields:

**Name and Slug** - Display name and URL identifier

**Active Status** - Toggle to enable/disable

**Content Types** - JSON array like `["product", "category"]`

**Weight Overrides** - JSON object like `{"weight_name": 1.8}` (empty if using global weights)

**Excluded Categories** - M2M relationship to Category model. Products in these categories won't appear in search results.

**Excluded Brands** - M2M relationship to Brand model. Products with these brands won't appear in search results.

## Using Exclusions

Exclusions hide specific content from search results for this engine:

**Example: Hide Clearance Items**

1. Create a "Main Shop" engine
2. In the Excluded Categories field, select your "Clearance" category
3. In the Excluded Brands field, select any budget brands you want hidden
4. Save

Now searches through the "Main Shop" engine won't return clearance products, even though they're visible on your site. You could create a separate "Clearance" engine that searches ONLY clearance items.

## Using Engines in Frontend

Your frontend code specifies which engine to use via API calls:

```javascript
// Use the "shop" engine (most common)
fetch('/api/search/?q=laptop&engine=shop')

// Use the "blog" engine
fetch('/api/search/?q=ecommerce tips&engine=blog')

// Default engine if no engine parameter specified
fetch('/api/search/?q=laptop')
```

The engine slug becomes a query parameter. If no engine is specified, Spwig uses the first active engine alphabetically.

## Engine-Specific Synonyms and Redirects

Both Synonym and SearchRedirect models have an optional `engine` foreign key. If set, that synonym or redirect applies ONLY to searches through that specific engine.

**Example**: A blog engine could have synonyms like "tutorial" → "guide" that don't apply to product searches.

Most synonyms and redirects should NOT be engine-specific - leave the engine field blank to apply them globally.

## Tips

- **Start with one engine** - Create the default "shop" engine and use it for everything until you have a clear need for multiple engines
- **Use descriptive slugs** - Choose slugs like "shop", "blog", "wholesale" that clearly indicate the engine's purpose
- **Test engines before activating** - Create engines in inactive state, test via API, then activate
- **Don't create engines unless needed** - More engines = more configuration complexity with no benefit if they all do the same thing
- **Review analytics per engine** - Search Analytics dashboard can filter by engine to see which engines are used most
