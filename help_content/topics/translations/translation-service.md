---
slug: translation-service
title_i18n_key: Translation Service
category: translations
component: translation_service
keywords:
  - translation
  - language
  - multilingual
  - translate
  - AI translation
  - DeepL
  - localization
  - site language
  - translation model
  - NLLB
url_patterns:
  - /admin/translations/languages/
  - /admin/translations/
related:
  - store-settings
published: true
---

The translation service provides AI-powered translations for your store's product descriptions, page content, blog posts, SEO fields, and other merchant content. Translations run locally on your server or through external providers, so your content stays private and translations happen in seconds.

![Language management](/static/core/admin/img/help/translation-service/language-management.webp)

## How It Works

1. You **activate languages** for your store (e.g., English, German, Japanese)
2. When you create or edit content (products, pages, blog posts), you write in your default language
3. Click **Translate** on any translatable field to generate AI translations into your active languages
4. Translations are stored alongside the original content and served automatically based on the visitor's language

## Managing Languages

Navigate to **Settings > Languages** to manage your store's languages.

### Language Dashboard

The dashboard shows:
- **Total Languages** — All available languages in the system (100+)
- **Active Languages** — Languages currently enabled for your store
- **Model Coverage** — How many languages the installed translation model supports

### Activating Languages

1. Find the language in the **Available Languages** column
2. Click the language to move it to the **Active Languages** column
3. The language is immediately available for translations and appears in your store's language switcher

### Default Language

One language is marked as the **default**. This is:
- The language you write content in
- The fallback when a translation doesn't exist
- The language shown when visitors haven't selected a preference

## Translation Models

Spwig includes a local AI translation engine that runs entirely on your server — no data is sent to external services.

### Available Models

| Model | Languages | Speed | Quality |
|-------|-----------|-------|---------|
| **M2M100-418M** | 100 | Fast | Good for common language pairs |
| **M2M100-1.2B** | 100 | Moderate | Better quality, higher resource usage |
| **NLLB-200** | 200+ | Moderate | Best coverage, including rare languages |

### Model Selection

The language management page shows which model is installed and its language coverage. The model runs as a local service using CTranslate2 for efficient inference.

## External Providers

For stores that prefer cloud-based translation or need specific language quality, Spwig supports external translation providers.

| Provider | Description |
|----------|-------------|
| **DeepL** | Premium translation quality for European and Asian languages |
| **Google Translate** | Wide language coverage with neural machine translation |
| **Azure Translator** | Microsoft's neural translation service |
| **AWS Translate** | Amazon's machine translation with custom terminology support |

### Connecting a Provider

1. Navigate to **Settings > Translation Providers**
2. Select the provider and enter your API key
3. Set the provider as the preferred translation engine
4. Translations will use the external provider instead of the local model

You can use external providers alongside the local model — for example, use DeepL for European languages and the local model for everything else.

## Translating Content

### Field-Level Translation

Translatable fields (product names, descriptions, SEO titles, etc.) show a **translate button** next to the field. Click it to:

1. **Translate to all active languages** — Generates translations for every active language at once
2. **Translate to a specific language** — Pick individual languages to translate

Translations appear in the language tabs of the editor. You can review and manually edit any machine translation.

### Bulk Translation Jobs

For large amounts of content, use **translation jobs**:

1. Navigate to **Settings > Translation Jobs**
2. Create a new job selecting:
   - **Content type** — Products, pages, blog posts, categories, etc.
   - **Source language** — The language to translate from
   - **Target languages** — One or more languages to translate into
   - **Scope** — All content, or only untranslated fields
3. Submit the job — it runs in the background via a task queue
4. Monitor progress in the job list (queued → processing → completed)

Bulk jobs are useful when you activate a new language and want to translate your entire catalog at once.

## Translation Management

### Reviewing Translations

Each translated field tracks:
- **Translation status** — Whether the field has been machine-translated, manually edited, or is missing
- **Lock status** — Locked translations won't be overwritten by future machine translations
- **Last translated** — When the translation was last generated or edited

### Locking Translations

If you manually edit a machine translation to improve it, **lock** the field to prevent it from being overwritten the next time a bulk translation runs. Locked fields are skipped during automatic translation.

### Translation Coverage

The coverage tracker shows what percentage of your content is translated for each language. Navigate to **Settings > Languages** to see:
- Per-language completion percentages
- Which content types have gaps
- Fields that still need translation

## UI Translation Overrides

Beyond product and page content, you can customize the translations of **frontend interface strings** — buttons, labels, messages, and other UI text shown to visitors.

Navigate to **Settings > UI Overrides** to:
1. Search for a specific string (e.g., "Add to Cart")
2. Enter your preferred translation for each language
3. Save — the override takes effect immediately

There are approximately 300 frontend strings available for customization. Overrides take priority over the default translations.

## Tips

- Start by activating only the languages your customers actually use — you can always add more later.
- Use the **local AI model** for day-to-day translations — it's fast, private, and has no per-translation cost.
- Consider **DeepL** if you need the highest quality for key European languages — it consistently produces more natural translations than generic models.
- Always **review machine translations** for product names, brand terms, and marketing copy — AI handles technical content well but may miss nuance in creative text.
- **Lock** any translations you've manually refined to protect them from being overwritten during bulk translation runs.
- Use **bulk translation jobs** when activating a new language to translate your entire catalog in one pass rather than translating products one at a time.
- Customize **UI overrides** to match your brand voice — for example, change "Add to Cart" to "Buy Now" if that suits your store better.
