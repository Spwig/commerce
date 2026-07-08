---
slug: search-performance-optimization
title_i18n_key: Search Performance Optimization
category: search
component: search
keywords:
  - search performance
  - search optimization
  - search speed
  - slow search
  - search caching
  - database optimization
  - search tuning
  - performance monitoring
  - search bottlenecks
  - query optimization
  - response time
  - search efficiency
  - scaling search
  - search load
  - index optimization
url_patterns:
  - /admin/search/searchsettings/
  - /admin/search/searchquery/
related:
  - search-settings-overview
  - relevance-weights-deep-indexing
  - search-analytics-dashboard
  - configuring-autocomplete
published: true
---

Search performance directly impacts customer experience and conversions. Slow searches frustrate customers and increase bounce rates. This comprehensive guide identifies common performance bottlenecks in Spwig's database-native search system, provides optimization strategies, and establishes performance targets. Use this guide when search response times exceed acceptable thresholds or you're planning for catalog growth.

Target response times: <200ms autocomplete, <500ms full search. Follow the optimization checklist below to achieve these targets.

## Understanding Performance Metrics

Monitor these metrics in **Search > Search Analytics**:

**Response Time** - Milliseconds to execute a search query (server-side only, excludes network latency)

**Cache Hit Rate** - Percentage of searches served from cache vs database

**Query Count** - Number of database queries per search (fewer is better)

**Database Query Time** - Time spent in database vs application code

## Performance Targets

| Query Type | Target | Acceptable | Requires Optimization |
|------------|--------|------------|----------------------|
| Autocomplete | <200ms | 200-300ms | >300ms consistently |
| Full Search | <500ms | 500-800ms | >800ms consistently |
| Admin Search | <1000ms | 1000-1500ms | >1500ms consistently |

If your average response times exceed "Requires Optimization" thresholds, implement the strategies below.

## Monitoring Performance

**Analytics Dashboard Average Response Time**

Navigate to **Search > Search Analytics** to view average response time across all searches. This is your primary performance monitoring metric.

**When to Investigate**: Average response time >300ms for autocomplete or >800ms for full search consistently over multiple days.

**Weekly Monitoring**: Review analytics every Monday to catch performance degradation early.

## Known Performance Bottlenecks

Spwig's database-native search has several documented bottlenecks to avoid:

### CTR Calculation N+1 Queries

**What It Is**: The click-through rate calculation in AnalyticsService executes separate queries for each aggregated result item.

**Impact**: Severe on high-traffic stores with many tracked queries.

**Code Location**: `search/services/analytics_service.py` - `get_click_through_rate()` method

**Mitigation**: Avoid calling CTR calculations in production. This is primarily an admin analytics feature that should be computed asynchronously, not during customer-facing requests.

### Stock Aggregation

**What It Is**: `with_stock_totals()` computes on_hand quantities across all warehouses per product.

**Impact**: Expensive on catalogs >1,000 products. Called when `in_stock` filter is used or stock status is displayed in autocomplete.

**Trigger**: **Search Settings > Autocomplete** - "Show Stock Status" option

**Recommendation**: NEVER enable stock status in autocomplete on large catalogs. Adds 200-500ms per request.

### Variant Joins

**What It Is**: SKU searches trigger JOIN on variants table to search variant SKUs.

**Impact**: 2-3x slower on products with many variants (10+ variants per product).

**Mitigation**: Uses `.distinct()` to avoid duplicates, which adds overhead. Necessary for SKU functionality - don't disable unless SKUs are unused.

### Product Counts in Autocomplete

**What It Is**: Category/Brand autocomplete results show product counts ("Electronics (234)")

**Impact**: Each content type with counts enabled adds 2 extra queries. Queries include joins and aggregations.

**Trigger**: **Search Settings > Autocomplete** - "Show Product Count" for categories/brands

**Recommendation**: Disable product counts. Saves 2-4 queries per autocomplete request. Single biggest autocomplete optimization.

### Document Indexing

**What It Is**: Text extraction from PDF/DOCX/XLSX files during search queries.

**Impact**: Extremely expensive (file I/O + text extraction). Synchronous blocking operations.

**Trigger**: **Search Settings > Deep Indexing** - "Index Documents"

**Recommendation**: Almost never worth the performance cost. ONLY enable for small digital product catalogs (<500 products) after thorough testing.

## Cache Configuration

Caching is the single most effective performance optimization.

**Autocomplete Cache** - Default: 60s
- **Recommended Range**: 45-90s
- **Higher TTL (90-120s)**: Better performance if inventory changes infrequently
- **Lower TTL (30-45s)**: More current results if you add products hourly

**Results Cache** - Default: 300s (5 minutes)
- **Recommended Range**: 180-600s
- **Higher TTL (600s/10min)**: Significant performance improvement for static catalogs
- **Lower TTL (180s)**: More current if frequently updating product data

**Optimization Strategy**: If searches are slow, double your cache TTL before disabling features. Going from 60s → 120s autocomplete cache cuts database load in half.

## Autocomplete Optimization Checklist

Apply these changes to autocomplete settings for maximum performance:

**1. Increase Debounce to 300-400ms**
- Location: **Search Settings > Autocomplete** - "Debounce Delay"
- Impact: Reduces API calls by waiting longer between keystrokes
- Trade-off: Slightly less responsive (imperceptible to most users)

**2. Reduce Max Results from 8 to 5-6**
- Location: **Search Settings > Autocomplete** - "Max Results Per Type"
- Impact: Smaller result sets = faster queries and smaller JSON payloads
- Trade-off: Fewer options shown (usually sufficient)

**3. Disable Product Counts (BIGGEST WIN)**
- Location: **Search Settings > Autocomplete** - Uncheck "Show Product Count" for categories/brands
- Impact: Saves 2-4 queries per autocomplete request
- Trade-off: No product counts in dropdown (rarely needed)

**4. Disable Stock Status**
- Location: **Search Settings > Autocomplete** - Uncheck "Show Stock Status"
- Impact: Eliminates expensive stock aggregation
- Trade-off: No stock badges (not critical in autocomplete context)

**5. Disable Product Descriptions**
- Location: **Search Settings > Autocomplete** - Uncheck "Show Description"
- Impact: Reduces text processing and payload size
- Trade-off: Less preview text (product name usually sufficient)

**6. Increase Cache TTL to 90s**
- Location: **Search Settings > Caching** - "Autocomplete Cache TTL"
- Impact: More requests served from cache
- Trade-off: Results up to 90 seconds stale (acceptable for most stores)

**Expected Improvement**: Applying all 6 optimizations typically reduces autocomplete response time by 50-70%.

## Deep Indexing Optimization

Each deep indexing option adds overhead. Disable based on catalog size:

| Catalog Size | Recommended Deep Indexing |
|--------------|---------------------------|
| **<1,000 products** | All ON (minimal impact) |
| **1,000-10,000** | Keep SKUs, Attributes, Custom Fields ON; Disable Reviews |
| **10,000-20,000** | Keep SKUs, Attributes ON; Disable Custom Fields, Reviews |
| **20,000-50,000** | Keep SKUs ON only; Disable all else |
| **>50,000** | Keep SKUs ON; Consider Elasticsearch migration |

**Document Indexing**: ALWAYS OFF unless critical (digital products with searchable documents AND <500 products total).

## Content Type Optimization

Disable unused content types in **Search Settings > Content Types**:

- **No blog?** Disable "Blog Posts" - saves queries
- **No brand filtering?** Disable "Brands" - saves queries
- **Shop-only store?** Disable "Categories" and "Blog Posts"

Each disabled content type removes database queries from every search.

## Database Optimization

Spwig creates necessary indexes via migrations. Trust them - don't create additional indexes without profiling.

**PostgreSQL Maintenance** (if using PostgreSQL):
- Run `VACUUM ANALYZE` weekly to update query planner statistics
- Large catalogs benefit from monthly `VACUUM FULL` (requires downtime)

**Monitor Database Query Time**: During development, identify slow queries using profiling tools. Most query optimization is already implemented:
- `.select_related('brand', 'category')` on products
- `.prefetch_related('images')` for thumbnails
- `.distinct()` for variant searches

## Fuzzy Matching Performance

Levenshtein distance is computationally expensive (O(m*n) complexity):

**Threshold Optimization**:
- **Higher threshold (0.85 vs 0.80)**: Faster but catches fewer typos
- **Lower threshold (0.75 vs 0.80)**: Slower but more forgiving

**Max Edits Optimization**:
- **Lower max edits (1 vs 2)**: Faster but misses more misspellings
- **Higher max edits (2 vs 3)**: Slower but catches more typos

**Library Performance**: Spwig uses `rapidfuzz` if available (10x faster than pure Python). Ensure it's installed: `pip install rapidfuzz`

## Synonym and Redirect Performance

**Synonym Query Expansion**: Each synonym adds OR clauses to the search query. Limit to 10-20 synonyms per term maximum.

**Regex Match Type**: Regex redirects are slower than exact/contains/starts_with. Avoid complex patterns.

**Recommendation**: Use simple match types whenever possible. Reserve regex for cases where other match types don't work.

## Large Catalog Optimization (>10,000 products)

Specific strategies for large catalogs:

**1. Aggressive Caching**
- Autocomplete: 90-120s TTL
- Results: 600s (10min) TTL
- Accept staleness for performance

**2. Minimal Deep Indexing**
- SKUs only (disable attributes, custom fields, reviews)
- Test performance with/without attributes

**3. Reduced Autocomplete Results**
- Max 5 results per type (down from 8)
- Reduces query overhead

**4. Disable Stock Status Everywhere**
- In autocomplete
- In search results if displayed

**5. Consider Elasticsearch at >50K Products**
- Database-native search suitable up to ~50,000 products
- Beyond that, Elasticsearch recommended for:
  - Complex faceted search
  - High concurrent search load (>100 searches/sec)
  - Consistently >500ms response times despite optimization

## Multi-Language Performance

JSONField JSONB indexing (PostgreSQL) makes multi-language efficient:

- **1-3 languages**: Minimal overhead (5-10ms)
- **5+ languages**: Minor increase in query complexity (20-40ms)
- **10+ languages**: Noticeable overhead (50-100ms)

Overhead scales linearly with language count.

## Emergency Performance Fixes

If searches are critically slow (>2s response times), apply these immediate fixes in order:

**Immediate** (apply now):
1. Disable document indexing
2. Disable product counts in autocomplete
3. Increase cache TTLs to 120s autocomplete / 600s results

**Quick** (apply within 24 hours):
4. Disable stock status in autocomplete
5. Reduce autocomplete max results to 5
6. Disable product descriptions in autocomplete

**Medium** (apply within week):
7. Disable reviews indexing if >20K products
8. Review and disable unused content types
9. Increase debounce to 400ms

**Expected Improvement**: These 9 fixes typically reduce response times by 60-80% on large catalogs.

## Tips

- **Monitor response times weekly** - Catch performance degradation early
- **Cache increases are first optimization** - Doubling cache TTL is easiest win
- **Product counts in autocomplete = expensive** - Biggest autocomplete performance killer
- **Document indexing almost never worth it** - Performance cost rarely justifies benefit
- **Test one change at a time** - Can't identify cause/effect with simultaneous changes
- **Benchmark with realistic data volumes** - Test with production-size catalogs
- **Stock aggregation kills performance on large catalogs** - Avoid displaying stock in autocomplete
- **Consider Elasticsearch at 50K+ products** - Database-native search has limits
