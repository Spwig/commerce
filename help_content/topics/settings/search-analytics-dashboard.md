---
slug: search-analytics-dashboard
title_i18n_key: Search Analytics Dashboard
category: search
component: search
keywords:
  - search analytics
  - search insights
  - search queries
  - search tracking
  - zero results
  - search trends
  - top searches
  - search metrics
  - query analytics
  - search performance
  - search data
  - search reports
  - search statistics
url_patterns:
  - /admin/search/searchquery/
related:
  - search-settings-overview
  - managing-synonyms-redirects
  - search-performance-optimization
published: true
---

The Search Analytics dashboard tracks every search query on your store, providing insights into what customers search for, which searches succeed or fail, and how fast your search system responds. Use this data to identify popular products, discover missing inventory, create synonyms, and optimize search performance.

Analytics tracking must be enabled in **Search Settings > Analytics tab** for data to appear.

![Analytics Dashboard](/static/core/admin/img/help/search-analytics-dashboard/analytics-dashboard.webp)

## Dashboard Overview

Navigate to **Search > Search Analytics** to access the dashboard. The page shows:

**Statistics Cards** - Quick metrics for today and the past week:
- Total searches today
- Total searches this week
- Zero-result queries (searches returning no products)
- Average response time in milliseconds

**Top Queries Table** - Most frequent search terms with result counts

**Zero-Result Queries** - Searches that returned no results (critical for improvement)

**Query List** - All individual search records with filters

## Today's Statistics

**Total Searches Today** - Count of all search requests since midnight in your store's timezone. Includes both autocomplete and full search page requests.

**Unique Queries Today** - Count of distinct search terms used today. If 5 customers all search "laptop", this counts as 1 unique query despite 5 total searches.

**Zero-Results Today** - Searches today that returned no products. High zero-result counts indicate missing products or poor synonym coverage.

Real-time data updates as searches occur.

## Weekly Statistics

**Week Total** - Total searches in the past 7 days

**Unique Queries** - Distinct search terms used this week

**Week-over-Week Growth** - Percentage change vs previous week (if displayed)

Use weekly data to spot trends: increased search volume often correlates with traffic growth or marketing campaigns.

## Average Response Time

⚠️ **PERFORMANCE MONITORING**

Average time (in milliseconds) to execute search queries. Target response times:

| Query Type | Target | Warning Threshold |
|------------|--------|-------------------|
| Autocomplete | < 200ms | > 300ms consistently |
| Full Search | < 500ms | > 800ms consistently |

If average response time exceeds warning thresholds:
1. Check **Search Settings > Caching tab** - increase cache TTLs
2. Review **Deep Indexing tab** - disable expensive features (document indexing, review indexing on large catalogs)
3. See [Search Performance Optimization](/en/admin/help/search-performance-optimization/) guide

## Top Queries

The Top Queries table shows the most frequently searched terms:

**Use This Data To**:
- **Feature popular products** - If "wireless headphones" is a top search, feature those products prominently on your homepage
- **Stock decisions** - High search volume for a category indicates demand
- **Identify trends** - Seasonal searches reveal what's currently popular
- **Content creation** - Write blog posts or guides about frequently searched topics

Review top queries monthly to align your merchandising with customer interests.

## Zero-Result Queries

**CRITICAL FOR IMPROVEMENT** - Zero-result queries are a goldmine for optimizing your store.

Zero-result queries occur for three main reasons:

### 1. Missing Products

Customers search for products you don't sell.

**Example**: Repeated searches for "yoga mats" but you only sell fitness equipment, not yoga supplies.

**Action**: Consider adding these products to your catalog if searches are frequent.

### 2. Missing Synonyms

Customers use terms that don't match your product descriptions.

**Example**: Customers search "laptop" but your products all say "notebook computer".

**Action**: Create synonyms mapping customer terms to your product language. See [Managing Synonyms and Redirects](/en/admin/help/managing-synonyms-redirects/).

### 3. Poor Fuzzy Matching

Typos or misspellings don't match even with fuzzy search enabled.

**Example**: Search "accomodate" doesn't find "accommodate" products.

**Action**:
- Lower the similarity threshold in **Search Settings > Fuzzy Matching tab** (from 0.80 to 0.75)
- Add unidirectional synonyms for common misspellings

**Weekly Workflow**:
1. Review zero-result queries every Monday
2. Categorize: Missing products, missing synonyms, or misspellings
3. Add synonyms for frequently searched terms
4. Note product gaps for inventory planning

## Query Details

Click any query in the list to view full details:

**Fields Tracked**:
- **Query text** - What the customer searched for
- **Timestamp** - When the search occurred
- **Result count** - How many results were returned
- **Response time** - Milliseconds to execute (performance monitoring)
- **User** - Logged-in customer (if user tracking enabled)
- **Session ID** - Anonymous session identifier
- **Language** - Store language during search
- **Engine** - Which search engine processed the query

## Filtering and Search

Use filters to analyze specific segments:

**Date Hierarchy** - Filter by date, month, or year

**Language Filter** - See searches by language (valuable for multi-language stores)

**Engine Filter** - Compare search behavior across different engines

**Zero-Result Toggle** - Show only queries that returned no results

**Search Box** - Find specific query text

## Exporting Data

Click **Export** to download query data as CSV for deeper analysis in Excel or data tools.

**CSV includes**:
- All query text
- Timestamps
- Result counts
- Response times
- Language and engine data

Use exports for:
- Trend analysis over time
- Identifying seasonal search patterns
- Performance auditing
- Presentation to stakeholders

## Privacy Considerations

Search analytics tracking respects privacy:

**User Tracking** (optional) - Links searches to logged-in customer accounts. Disable for GDPR/CCPA compliance in **Search Settings > Analytics tab**.

**Session Tracking** (default) - Uses anonymous session IDs to track search patterns without identifying customers. Privacy-friendly.

**Data Retention** - Search queries remain in database indefinitely. Implement a custom retention policy if required for compliance.

## Using Analytics to Improve Search

Actionable insights from search analytics:

**Weekly Tasks**:
- Review zero-results and add synonyms for common terms
- Monitor response times and optimize if consistently slow
- Identify top searches and ensure those products are well-stocked

**Monthly Tasks**:
- Analyze top queries to inform product selection
- Export data to identify seasonal trends
- Review language-specific search patterns
- Track redirect hit counts to optimize navigation shortcuts

**Quarterly Tasks**:
- Audit synonym effectiveness (have zero-results decreased?)
- Compare search volume growth vs overall traffic
- A/B test weight changes and measure result relevance
- Review if new product categories should be added based on search demand

## Tips

- **Zero-result queries are goldmines for improvement** - They directly tell you what customers want that you don't provide
- **Review analytics Monday mornings** - Start your week by optimizing based on previous week's data
- **Response time >300ms consistently = investigate** - Check caching settings first, then deep indexing features
- **Export CSV for trend analysis** - Spreadsheet analysis reveals patterns not obvious in admin interface
- **Create synonyms before adding products** - If customers search for "tablet cases" but you call them "protective covers", add synonym first
- **Track seasonal search patterns** - "Winter boots" in October, "swimsuit" in March - stock inventory accordingly
