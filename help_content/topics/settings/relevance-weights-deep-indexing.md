---
slug: relevance-weights-deep-indexing
title_i18n_key: Relevance Weights and Deep Indexing
category: search
component: search
keywords:
  - relevance weights
  - search weights
  - deep indexing
  - index settings
  - search relevance
  - result ranking
  - search scoring
  - attribute indexing
  - sku indexing
  - review indexing
  - document indexing
  - custom field indexing
  - search depth
  - indexing performance
  - weight tuning
url_patterns:
  - /admin/search/searchsettings/
related:
  - search-settings-overview
  - search-performance-optimization
  - configuring-autocomplete
published: true
---

Relevance weights and deep indexing control how search results are ranked and what product data gets searched. Weights are importance multipliers - a 2.0 weight means matches in that field are twice as important as a 1.0 weight. Deep indexing determines whether the search looks beyond basic product names into SKUs, attributes, reviews, and even document contents. This guide explains both systems, when to adjust them, and critical performance implications.

The defaults work well for most e-commerce stores. Only adjust if you have specific ranking or indexing needs.

![Weights Tab](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Understanding Weights

Weights are multipliers (0.0-2.0 scale) applied when text matches are found in different fields. Higher weights mean matches in that field rank higher in results.

**Example**: If a product has "laptop" in both its name (weight 1.50) and description (weight 0.80):
- Name match contributes 1.50 to relevance score
- Description match contributes 0.80
- Combined score determines ranking vs other products

Weights allow you to prioritize certain fields over others when ranking search results.

## Weight Categories and Defaults

Navigate to **Search Settings > Weights tab** to view all weight settings:

| Field | Default Weight | Rationale |
|-------|---------------|-----------|
| **weight_name** | 1.50 | Product names most important - customers expect exact name matches at top |
| **weight_sku** | 1.20 | SKUs are specific identifiers - important for B2B and returning customers |
| **weight_description** | 0.80 | Descriptions provide context but less important than exact name matches |
| **weight_categories** | 0.80 | Category matches helpful for browsing but not as specific as name/SKU |
| **weight_attributes** | 0.70 | Color, size, material searches - useful but supporting information |
| **weight_brands** | 0.70 | Brand filtering important but not primary search criterion for most stores |
| **weight_blog_posts** | 0.60 | Blog content less important in e-commerce focused search (lowest priority) |
| **weight_reviews** | 0.50 | User-generated content least controlled - lowest weight |

These defaults assume a typical e-commerce store where product discovery is the primary search goal.

## When to Adjust Weights

Adjust weights when your store's priorities differ from typical e-commerce patterns:

**SKU-Heavy Stores (B2B, Wholesale)** - Increase `weight_sku` to 1.8-2.0 so product code searches dominate results. B2B customers often search by exact SKU.

**Brand-Focused Stores** - Increase `weight_brands` to 1.2-1.5 when customers primarily shop by brand (designer clothing, luxury goods).

**Content-Heavy Stores** - Increase `weight_blog_posts` to 0.9-1.2 if you're a content publisher or educational retailer where blog posts are as important as products.

**Attribute-Heavy Stores (Fashion)** - Increase `weight_attributes` to 1.0-1.2 when customers frequently search by color, size, style attributes.

## Weight Adjustment Examples

| Store Type | Recommended Adjustments |
|-----------|------------------------|
| **B2B Wholesale** | weight_sku: 2.0, weight_name: 1.3, weight_description: 0.6 - Prioritize product codes |
| **Fashion Boutique** | weight_attributes: 1.2, weight_brands: 1.2, weight_name: 1.4 - Color/style/brand important |
| **Content Publisher** | weight_blog_posts: 1.2, weight_name: 1.3, weight_reviews: 0.7 - Content as important as products |
| **General E-commerce** | Use defaults - Balanced for typical online stores |

Adjust one weight at a time and test before making additional changes.

## Deep Indexing Overview

⚠️ **PERFORMANCE WARNING** - Each deep indexing option adds query complexity and overhead.

Deep indexing extends search beyond basic product name/description into additional data:

![Deep Indexing Tab](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Navigate to **Search Settings > Deep Indexing tab** to configure.

## Index SKUs

**Default**: ON, **Performance Impact**: Low

Includes product and variant SKUs in search index. Triggers variant JOIN (minor cost).

**When to keep ON**: Essential for B2B stores where customers know product codes. Also helpful for returning customers who remember SKU from previous orders.

**When to disable**: Never, unless you literally have no SKUs assigned. Performance impact is negligible.

## Index Attributes

**Default**: ON, **Performance Impact**: Medium

Includes product attributes (color, size, material, custom attributes) in search index. Joins to attributes table.

**When to keep ON**: Important for fashion, configurable products, or any store where customers search by product characteristics ("red dress", "large t-shirt").

**When to disable**: Catalogs >20,000 products with many attributes per product may see 50-100ms overhead. Only disable if performance is critical and customers don't search by attributes.

## Index Custom Fields

**Default**: ON, **Performance Impact**: Medium

Includes merchant-defined custom fields from JSONField in search. Requires JSONField traversal.

**When to keep ON**: If you use custom fields for searchable product data (warranty info, specifications, compatibility details).

**When to disable**: If you don't use custom fields, or custom fields contain non-searchable data (internal notes, accounting codes). Disabling saves JSONField processing overhead.

## Index Reviews

**Default**: ON, **Performance Impact**: Medium-High

Includes approved review titles and comments in search. Joins to reviews table and adds text search overhead.

**When to keep ON**: Review-heavy catalogs where customers search for products based on review content ("waterproof laptop bag" might appear in review text).

**When to disable**: Catalogs >20,000 products or stores with many reviews per product. Adds 100-200ms overhead on large catalogs.

## Index Documents

**Default**: OFF, **Performance Impact**: VERY HIGH 🚨

**NEVER ENABLE CASUALLY** - Most expensive search feature.

Document indexing extracts text from PDF, DOCX, and XLSX files attached to digital products, making file contents searchable.

**Technical Details**:
- Uses PyPDF2, python-docx, and openpyxl libraries
- Synchronous file I/O and text extraction on search
- Tracks files via MD5 checksum (reindexes only when file changes)
- Potential timeouts on large files (>10MB PDFs)

**Performance Impact**:
- Very expensive initial indexing (minutes to hours for large libraries)
- Significant query overhead (100-500ms additional latency)
- Memory intensive for large documents

**Only enable if**:
- You sell digital products with searchable documents (ebooks, reports, manuals)
- Catalog is small (<500 digital products)
- Server has adequate resources
- You've tested impact thoroughly

**For digital product stores**: Consider whether customers truly need to search document contents, or if searching product name/description is sufficient.

## Performance Impact Table

| Feature | Default | Impact | Use When |
|---------|---------|--------|----------|
| Index SKUs | ON | Low | Always (B2B essential) |
| Index Attributes | ON | Medium | Configurable products |
| Index Custom Fields | ON | Medium | Using custom fields |
| Index Reviews | ON | Medium-High | Review-heavy store |
| Index Documents | OFF | Very High | Digital products only (test first) |

Impact assumes typical catalogs. Large catalogs (>50,000 products) experience proportionally higher overhead.

## Testing Weight Changes

When adjusting weights, follow this testing workflow:

1. **Change one weight at a time** - Don't adjust multiple weights simultaneously; you won't know which change caused results
2. **Small increments** - Adjust by ±0.2 at a time (e.g., 1.0 → 1.2, not 1.0 → 1.8)
3. **Test with real queries** - Use actual customer search terms from analytics, not random tests
4. **Monitor analytics** - Compare result relevance before/after using top queries
5. **Wait 1-2 weeks** - Give customers time to interact with new rankings
6. **Measure click-through rates** - Are customers clicking results more/less than before?

## Performance vs Accuracy Trade-offs

More indexing = better search results but slower performance:

**Scenario: Small Catalog (<1,000 products)**
- Enable all indexing options (SKUs, attributes, custom fields, reviews)
- Performance impact minimal
- Comprehensive search capabilities

**Scenario: Medium Catalog (1,000-10,000 products)**
- Keep SKUs, attributes, custom fields ON
- Consider disabling reviews if >10 reviews per product average
- Monitor response times

**Scenario: Large Catalog (>10,000 products)**
- Keep SKUs ON (low impact)
- Disable reviews indexing (high impact)
- Disable custom fields if unused
- NEVER enable document indexing
- Consider Elasticsearch at >50,000 products

Balance based on your catalog size and server resources.

## Engine-Specific Weight Overrides

When creating a search engine via the wizard (Step 3), you can override global weights for that specific engine.

**Use Case**: Blog-focused engine
- Create "blog" engine
- Override `weight_blog_posts` to 1.5 (vs global 0.60)
- Blog content now ranks higher in blog engine searches

Most engines should NOT override weights - leave blank to inherit global settings.

## Tips

- **NEVER enable document indexing unless absolutely critical** - Highest performance cost of any search feature
- **B2B stores: Increase weight_sku to 2.0** - Product codes are primary search method
- **Test weight changes during low-traffic hours** - Observe performance impact before peak times
- **Monitor response times after enabling indexing** - Check analytics dashboard for slowdowns
- **Disable reviews indexing on catalogs >20K products** - Significant performance hit
- **One weight change at a time for testing** - Can't determine cause/effect with simultaneous changes
- **Document extraction requires PyPDF2/docx/openpyxl** - Verify these libraries are installed before enabling document indexing
