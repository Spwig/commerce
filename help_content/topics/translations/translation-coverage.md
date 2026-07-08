---
slug: translation-coverage
title_i18n_key: Translation Coverage
category: translations
component: translation_service
keywords:
  - translation coverage
  - translation progress
  - translation completeness
  - untranslated content
  - translation gaps
  - translation statistics
  - coverage report
  - translation tracking
  - missing translations
  - translation overview
url_patterns:
  - /admin/translations/coverage/
related:
  - translation-service
  - translation-jobs
  - ui-translations-management
published: true
---

The Translation Coverage page provides a comprehensive view of how much of your store's content has been translated into each active language. Use this dashboard to identify translation gaps, track progress, and ensure complete multilingual coverage before launching in new markets.

Coverage is calculated across all translatable content types: products, categories, pages, blog posts, SEO fields, and more.

## Understanding Coverage Metrics

**Overall Coverage Percentage** - The percentage of all translatable fields that have been translated for a specific language

**Per-Content-Type Breakdown** - Coverage percentages for each type of content (products, pages, blog posts, etc.)

**Field-Level Detail** - Which specific fields are translated vs missing

**Total Translatable Fields** - The denominator used to calculate percentages

## Coverage Dashboard Overview

The dashboard displays:

**Language Cards** - One card per active language showing overall coverage percentage

**Content Type Tables** - Detailed breakdown by products, categories, pages, blog posts, SEO metadata, etc.

**Missing Translation Counts** - How many fields still need translation in each category

**Completion Trends** - Progress over time (if tracking enabled)

## Interpreting Coverage Percentages

| Coverage | Status | Action Needed |
|----------|--------|---------------|
| **95-100%** | Excellent | Review remaining gaps, may be intentionally untranslated |
| **80-94%** | Good | Identify and translate key missing content |
| **60-79%** | Fair | Prioritize high-visibility content (homepage, product names) |
| **<60%** | Needs Work | Run bulk translation jobs or hire translators |

Remember: 100% coverage isn't always necessary. Some fields (SKUs, internal notes, technical IDs) don't need translation.

## Content Type Breakdown

**Products** - The largest category typically:
- Product names and descriptions
- Variant names (size, color options)
- Attribute values
- Custom fields
- SEO titles and meta descriptions

**Categories** - Navigation and browsing:
- Category names and descriptions
- SEO metadata
- Custom category fields

**Pages** - Static content:
- Page titles and body content
- SEO metadata
- Custom page fields

**Blog Posts** - Content marketing:
- Post titles and content
- Excerpts and summaries
- SEO metadata

**Other Content**:
- Store policies (shipping, returns, privacy)
- Email templates
- Form labels and messages

## Identifying Translation Gaps

Click any content type to view detailed field-level coverage:

**Missing Fields View** - Shows exactly which products/pages/posts have untranslated fields

**Field Priority** - Indicates which fields are customer-facing vs internal

**Bulk Actions** - Select multiple items to translate at once

## Using Coverage to Plan Translation Work

**Launching a New Language**:
1. Check coverage for existing languages (as a baseline)
2. Activate new language
3. Coverage for new language starts at 0%
4. Create translation job to bulk-translate core content
5. Monitor coverage as job completes
6. Manually review and refine key content
7. Target 80%+ before going live

**Maintaining Existing Languages**:
1. Review coverage monthly
2. New products may decrease overall coverage
3. Set up automatic translation on product creation
4. Periodically run jobs to catch any gaps

## Prioritizing Translation Work

Focus translation efforts on high-impact content first:

**Priority 1 - Customer-Facing Text**:
- Product names and main descriptions
- Homepage and main navigation
- Checkout flow pages
- Critical policies (shipping, returns)

**Priority 2 - Supporting Content**:
- Blog posts and marketing content
- Category descriptions
- Product variant details
- Email templates

**Priority 3 - Optional Content**:
- Extended product specifications
- Internal notes and tags
- Admin-only fields

## Coverage Filters

Use filters to focus on specific content:

**By Language** - View coverage for one language at a time

**By Content Type** - Filter to products only, pages only, etc.

**By Completeness** - Show only complete items, only incomplete items, or all items

**By Date Range** - Coverage for content created/updated in a specific period

## Bulk Translation from Coverage View

When you identify gaps, launch translation jobs directly from the coverage page:

1. **Select content type** with low coverage (e.g., "Products: 45% coverage")
2. **Click "Translate Missing Fields"**
3. **Choose target language(s)**
4. **Submit job** - Translates only the missing fields
5. **Monitor job** in Translation Jobs page
6. **Return to coverage** to see updated percentages

This targeted approach is more efficient than re-translating everything.

## Coverage vs Quality

**High coverage doesn't guarantee quality**. A store can have 100% coverage with poor machine translations that haven't been reviewed.

**Recommended Workflow**:
1. Use bulk jobs to achieve high coverage quickly (quantity)
2. Review and refine key content manually (quality)
3. Lock refined translations to preserve them
4. Periodically audit translations for accuracy

## Tracking Coverage Over Time

Enable coverage tracking to monitor trends:

**Weekly Snapshots** - Coverage percentage recorded each week

**Growth Charts** - Visualize progress toward 100% coverage

**Alerts** - Notifications when coverage drops (e.g., many untranslated products added)

This helps maintain translation quality as your catalog grows.

## Tips

- **Set coverage goals** - Aim for 80% minimum before launching a new language publicly
- **Monitor after content updates** - Adding 100 new products drops coverage until they're translated
- **Focus on customer-facing content first** - Internal fields can wait
- **Use coverage to justify translation budget** - Show stakeholders exactly how much work remains
- **Schedule regular coverage reviews** - Monthly checks prevent translation debt from accumulating
- **Combine with analytics** - Translate content in languages where you have actual traffic
- **Don't obsess over 100%** - Some fields (SKUs, internal codes) don't need translation
