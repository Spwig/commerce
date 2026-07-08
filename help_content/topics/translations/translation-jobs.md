---
slug: translation-jobs
title_i18n_key: Translation Jobs
category: translations
component: translation_service
keywords:
  - translation jobs
  - bulk translation
  - batch translation
  - translation queue
  - background translation
  - mass translation
  - translation tasks
  - translation workflow
  - automated translation
  - translation processing
url_patterns:
  - /admin/translations/jobs/
related:
  - translation-service
  - translation-coverage
  - ui-translations-management
published: true
---

Translation Jobs automate bulk translation of large amounts of content. Instead of manually translating products one-by-one, create a job that translates your entire catalog—or specific subsets—in the background. Jobs run asynchronously, so you can continue working while hundreds or thousands of fields are translated automatically.

Use translation jobs when activating new languages, importing new products, or catching up on untranslated content.

## What Are Translation Jobs?

A translation job is a background task that:

1. **Scans content** for translatable fields (products, pages, blog posts, etc.)
2. **Identifies untranslated or outdated fields** based on your job scope
3. **Sends fields to translation engine** (local AI model or external provider)
4. **Saves translations** back to your content
5. **Reports completion** with statistics on translated fields

Jobs run via Celery task queue, so they don't block your admin interface.

## When to Use Translation Jobs

**Launching a New Language**:
- Activate German as a new language
- Create job: Translate all products from English to German
- Result: Entire catalog available in German within minutes/hours (depending on size)

**New Product Imports**:
- Import 500 new products in English
- Create job: Translate new products to all active languages
- Result: New inventory immediately available in all markets

**Catching Up on Gaps**:
- Coverage report shows Products are only 60% translated to French
- Create job: Translate missing French product fields only
- Result: French coverage increases to ~100%

**Updating Stale Translations**:
- Translation model improved or new provider available
- Create job: Re-translate all products to Spanish
- Result: Higher quality Spanish translations throughout catalog

## Creating a Translation Job

Navigate to **Settings > Translation Jobs** and click **+ Create Job**.

### Job Configuration

**Job Name** - Descriptive label (e.g., "Translate products to German", "New blog posts - all languages")

**Content Type** - What to translate:
- Products
- Product categories
- Pages
- Blog posts
- SEO metadata
- Email templates
- All content types

**Source Language** - The language you're translating FROM (usually your default language)

**Target Language(s)** - One or more languages to translate INTO (select multiple for parallel translation)

**Scope** - What subset of content:
- **All items** - Translate everything regardless of existing translations
- **Untranslated only** - Skip fields that already have translations
- **Created/updated since date** - Only new or recently changed content
- **Specific items** - Select individual products/pages (advanced filtering)

**Translation Engine** - Which service to use:
- Local AI model (default, no API costs)
- Specific external provider (DeepL, Google, Azure, AWS)
- Auto-select (uses configured preference)

**Lock Translations** - Whether to lock translated fields against future automatic overwriting (useful for reviewed translations)

### Advanced Options

**Skip Locked Fields** - If enabled, respects existing locked translations (recommended)

**Overwrite Existing** - Re-translate even if translations exist (use for quality improvements)

**Field Filters** - Translate only specific fields (e.g., product names and descriptions, skip attributes)

**Batch Size** - How many items to process at once (default: 50, increase for faster processing if server can handle it)

**Priority** - High priority jobs run before normal priority (use sparingly)

## Job Lifecycle and Status

Jobs progress through these states:

**Queued** - Job created, waiting for worker to pick it up

**Processing** - Worker actively translating content

**Completed** - All translations finished successfully

**Failed** - Job encountered errors (check error log)

**Cancelled** - Manually stopped by admin

**Paused** - Temporarily suspended (can be resumed)

## Monitoring Job Progress

The job detail page shows:

**Progress Bar** - Percentage completed

**Statistics**:
- Total items to translate
- Items completed
- Items remaining
- Estimated time remaining

**Real-Time Log** - Stream of translation activity (useful for troubleshooting)

**Error Count** - How many fields failed to translate (with reasons)

## Job Results and Statistics

When a job completes, the results page shows:

**Summary**:
- Total fields processed
- Successfully translated
- Failed translations
- Skipped (already translated, locked, or excluded by filters)

**Per-Item Breakdown**:
- Which products/pages were translated
- How many fields per item
- Any errors encountered

**Performance Metrics**:
- Total time elapsed
- Average translations per second
- Translation engine used

## Handling Failed Translations

If some translations fail:

**Review error log** - Identifies which fields failed and why

**Common failure causes**:
- API rate limit hit (external provider)
- Translation engine timeout (very long text)
- Invalid field format (JSON parsing error)
- Model doesn't support language pair

**Retry options**:
- Fix the underlying issue
- Create new job for just the failed items
- Use different translation engine

## Canceling and Pausing Jobs

**Cancel** - Stops job immediately, discards any in-progress translations (completed translations are saved)

**Pause** - Temporarily stops job, can resume later from where it left off

**Resume** - Continues a paused job

Use pause/resume when you need to free up server resources temporarily.

## Bulk Job Strategies

**Strategy 1: Language-by-Language**:
- Create separate jobs for each target language
- Easier to monitor progress per language
- Can prioritize important languages
- Spreads load over time

**Strategy 2: All-at-Once**:
- Single job translating to all active languages
- Faster overall completion
- Higher server load during processing
- Simpler job management

**Strategy 3: Content-Type-by-Content-Type**:
- Translate products first (highest priority)
- Then categories, pages, blog posts
- Allows progressive rollout
- Easier to test and verify translations

Choose based on your server capacity, urgency, and catalog size.

## Job Scheduling

Schedule recurring jobs to handle new content automatically:

**Daily Jobs** - Translate any products created/updated in the last 24 hours

**Weekly Jobs** - Catch up on any translation gaps weekly

**After Import** - Trigger job automatically after bulk product import

**On Language Activation** - Auto-create job when you activate a new language

Scheduled jobs keep translations current without manual intervention.

## Performance Considerations

**Local AI Model**:
- ~100-500 translations/second (depends on server)
- CPU-intensive during processing
- No API rate limits
- Free (no per-translation cost)

**External Providers**:
- Rate limits vary (DeepL: 500k chars/month on free tier)
- API latency adds overhead
- Better quality but costs money
- Concurrent request limits

**Large jobs** (>10,000 fields):
- Run during off-peak hours
- Monitor server resources
- Consider splitting into smaller batches
- Test with subset first

## Tips

- **Start small** - Test jobs on a subset (e.g., 10 products) before running full catalog translation
- **Use "Untranslated only" scope** - Faster and avoids re-translating already-good content
- **Monitor first job closely** - Watch for errors or quality issues before launching larger jobs
- **Schedule jobs during low-traffic periods** - Translation is CPU/API intensive
- **Lock reviewed translations** - Prevents bulk jobs from overwriting your manual edits
- **Keep jobs focused** - Smaller, targeted jobs are easier to troubleshoot than massive "translate everything" jobs
- **Review samples after completion** - Check random translations for quality before considering job successful
- **Export/backup before major jobs** - In case you need to revert bulk changes
