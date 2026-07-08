---
slug: managing-synonyms-redirects
title_i18n_key: Managing Synonyms and Redirects
category: search
component: search
keywords:
  - synonyms
  - search synonyms
  - term mapping
  - search redirects
  - search terms
  - equivalent terms
  - query expansion
  - search aliases
  - redirect search
  - search forwarding
  - bidirectional synonyms
  - language synonyms
  - search optimization
  - search intelligence
url_patterns:
  - /admin/search/synonym/
  - /admin/search/synonym/add/
  - /admin/search/searchredirect/
  - /admin/search/searchredirect/add/
related:
  - search-engines-explained
  - search-settings-overview
  - search-analytics-dashboard
published: true
---

Synonyms and redirects make your search smarter by handling equivalent terms and routing specific queries to targeted pages. Synonyms expand searches to include related terms ("laptop" also finds "notebook"), while redirects send queries like "sale" directly to your sales page. This guide explains how to create and manage both features to improve search relevance and customer experience.

Use synonyms for term equivalence and redirects for navigation shortcuts.

![Synonyms List](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Understanding Synonyms

Synonyms tell the search system that certain terms should be treated as equivalent. When a customer searches for one term, the system automatically includes results matching the synonym terms.

**Example**: Create a synonym mapping "laptop" → "notebook", "portable computer". Now when someone searches "laptop", they also get results for products containing "notebook" or "portable computer" in their names or descriptions.

Synonyms are especially valuable for:
- British vs American English (jumper/sweater, trainers/sneakers)
- Brand vs generic terms (tissues/Kleenex)
- Common misspellings (accommodate/accomodate)
- Industry jargon vs plain language (CPU/processor)

## Creating Synonyms

Navigate to **Search > Synonyms** and click **+ Add Synonym**.

![Add Synonym Form](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - The original search term that triggers synonym expansion

**Synonyms** - JSON array of equivalent terms, e.g. `["sweater", "pullover", "jumper"]`

**Bidirectional** - Default: Checked. When enabled, synonym relationships work both ways:
- Search "laptop" finds "notebook" products
- Search "notebook" finds "laptop" products

Uncheck for one-way mappings (see below).

**Language** - Optional. Restrict this synonym to searches in a specific language. Leave blank to apply to all languages.

**Engine** - Optional. Restrict this synonym to a specific search engine. Leave blank to apply globally.

**Active** - Whether this synonym is currently used. Uncheck to temporarily disable without deleting.

## Bidirectional Examples

Most synonyms should be bidirectional - true equivalents that work in both directions:

| Term | Synonyms | Use Case |
|------|----------|----------|
| laptop | notebook, portable computer | American/British English + generic terms |
| sofa | couch, settee | Regional variations |
| trainers | sneakers, running shoes | UK/US English |
| mobile | cell phone, cellular | International variations |

With bidirectional enabled, all these terms find the same products regardless of which term the customer uses.

## Unidirectional Examples

Uncheck "Bidirectional" for one-way relationships:

**Common Use Cases**:
- **Misspellings**: Term: "acco

mmodate" → Synonyms: `["accommodate"]` (one-way so correct spelling doesn't find misspelling)
- **Specific → Generic**: Term: "MacBook" → Synonyms: `["laptop"]` (MacBooks are laptops, but not all laptops are MacBooks)
- **Abbreviations**: Term: "CPU" → Synonyms: `["processor"]` (CPU finds processor products, but processor searches shouldn't always include CPU)

## Language-Specific Synonyms

Use the Language field to create region-appropriate synonyms:

**Example**: British English store
- Term: "jumper", Synonyms: `["sweater", "pullover"]`, Language: English (UK)
- Term: "trainers", Synonyms: `["sneakers"]`, Language: English (UK)

**Example**: Multi-language store
- Term: "ordinateur portable", Synonyms: `["laptop", "notebook"]`, Language: French
- Term: "zapatos", Synonyms: `["shoes"]`, Language: Spanish

Language-specific synonyms only apply when a customer is browsing in that language.

## Engine-Specific Synonyms

Most synonyms should apply globally (leave Engine field blank). Use engine-specific synonyms only when different search contexts need different term mappings:

**Example**: You have separate "shop" and "blog" engines
- Blog synonym: Term: "tutorial" → Synonyms: `["guide", "how-to"]`, Engine: blog
- This synonym only applies to blog searches, not product searches

## Understanding Redirects

Search redirects send specific queries directly to designated pages, bypassing normal search results. Use redirects when you know exactly where a customer should go.

**Example**: Create a redirect for "sale" → `/products/sale/`. Now when someone searches "sale", they skip search results and land directly on your sales page.

Redirects are perfect for:
- Common navigation shortcuts ("returns" → returns policy page)
- Seasonal promotions ("summer sale" → summer collection)
- Popular categories ("laptops" → laptop category page)
- Policy pages ("shipping" → shipping information)

![Redirects List](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Match Types

Redirects support four match types that control how strictly the search query must match:

**Exact** - Case-insensitive exact match. Query must exactly match the term (ignoring capitalization).
- Term: "sale"
- Matches: "sale", "SALE", "Sale"
- Does NOT match: "summer sale", "on sale"

**Contains** - Query contains the term anywhere.
- Term: "sizing"
- Matches: "sizing guide", "help with sizing", "what sizing"
- Does NOT match: "size chart" (different word)

**Starts With** - Query begins with the term.
- Term: "return"
- Matches: "returns", "return policy", "returning items"
- Does NOT match: "how to return" (doesn't start with term)

**Regex** - Pattern matching using regular expressions. **⚠️ Performance caution** - complex regex patterns slow down searches. Use sparingly.
- Pattern: `^(laptop|notebook)s?$`
- Matches: "laptop", "laptops", "notebook", "notebooks"
- Use only if other match types don't work

## Creating Redirects

Navigate to **Search > Redirects** and click **+ Add Redirect**.

![Add Redirect Form](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - The search query to match

**Match Type** - Exact, Contains, Starts With, or Regex (see above)

**Redirect URL** - Where to send the customer. Can be relative (`/products/sale/`) or absolute (`https://example.com/page/`)

**Redirect Type** - HTTP status code:
- **302 (Temporary)**: Recommended. Browser doesn't cache, you can change destination later
- **301 (Permanent)**: Browser and search engines cache. Only use for permanent redirects

**Engine** - Optional. Restrict to specific search engine

**Hit Count** - Auto-incremented each time this redirect is used. Helps identify popular shortcuts.

**Active** - Enable/disable this redirect

## Redirect Examples

| Term | Match Type | URL | Use Case |
|------|-----------|-----|----------|
| sale | Exact | `/products/sale/` | Direct "sale" searches to sales page |
| clearance | Exact | `/clearance/` | Skip search for clearance items |
| sizing | Contains | `/pages/size-guide/` | Any query about sizing goes to guide |
| return | Starts With | `/pages/returns/` | Return-related queries go to policy |

All use 302 (temporary) redirects for flexibility.

## Redirect Type: 302 vs 301

**302 (Temporary)** - Recommended for most redirects
- Browser makes fresh request each time
- You can change destination URL anytime
- Safer choice if you're not sure

**301 (Permanent)** - Use sparingly
- Browser caches the redirect
- Search engines update their indexes
- Harder to change later

**Recommendation**: Use 302 unless you're absolutely certain the redirect will never change.

## Hit Count Analytics

The Hit Count field auto-increments each time a redirect fires. Use this to:
- Identify most-used navigation shortcuts
- Find redirects that are never used (consider removing)
- Discover popular search patterns

Review hit counts monthly to optimize your redirect strategy.

## Finding Synonym Opportunities

**Use Zero-Results Queries**: Navigate to **Search > Search Analytics** and filter for zero-result queries. These reveal:
- Terms customers use that don't match your product descriptions
- Regional variations you haven't considered
- Common misspellings

**Workflow**:
1. Review zero-result queries weekly
2. Identify patterns (same terms appearing repeatedly)
3. Add synonyms to map customer language to your product names
4. Monitor if zero-results decrease

## Tips

- **Monitor zero-result queries weekly for synonym ideas** - They reveal gaps between customer language and your product descriptions
- **Start with common synonyms, expand based on data** - Begin with obvious regional variations, then add based on actual search behavior
- **Use bidirectional for true equivalents** - Most synonyms should work both ways (laptop ↔ notebook)
- **Avoid complex regex patterns** - Regex matching is slower than other match types; use only when necessary
- **Use 302 redirects (temporary) by default** - Gives you flexibility to change destinations later
- **Test synonyms with real queries** - Search for synonym terms to verify they return expected results
- **Language-specific synonyms for multi-language stores** - Create region-appropriate term mappings for each language you support
