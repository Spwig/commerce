---
slug: ai-seo-generator
title_i18n_key: AI SEO Generator
category: marketing-seo
component: seo_generator
keywords:
  - SEO generator
  - AI SEO
  - meta title
  - meta description
  - SEO content
  - automated SEO
  - SEO provider
  - generate SEO
  - product SEO
  - bulk SEO
  - SEO automation
  - search optimization
  - AI content generation
url_patterns:
  - /admin/seo_generator/seoprovideraccount/
related:
  - add-product
  - product-feeds
  - social-sharing
published: true
---

The AI SEO Generator automatically writes meta titles, meta descriptions, and other SEO content for your products using an AI provider. Instead of manually writing SEO copy for every product, you can generate accurate, optimized content in bulk with a single action.

Your store comes with a built-in SEO generator that works immediately. You can also install additional AI provider components from the Spwig component marketplace for access to more powerful language models.

## How the SEO generator works

The SEO generator reads your product's name, description, category, and attributes, then uses the configured AI provider to write SEO content tailored to that product. The generated content is saved directly to the product's SEO fields.

You can generate SEO content for individual products from the product edit page, or run bulk generation across multiple products from the product list.

## Setting up an SEO provider

### Using the built-in provider

Your store includes a built-in SEO provider that generates SEO content deterministically from your product data — no external API keys are needed. It is automatically set as the primary provider on new installations.

To verify it is active:

1. Navigate to **Marketing > SEO Providers**
2. Check that the built-in provider appears with a **PRIMARY** badge and an **ACTIVE** status
3. If no providers are listed, click **+ Add SEO Provider Account** and set **Provider Key** to `deterministic`

### Connecting an AI provider component

For richer, more contextual SEO content, you can install an AI provider component (such as an OpenAI or Claude-based provider) from the Spwig component marketplace.

1. Install the provider component through the component update system (ask your store administrator)
2. Navigate to **Marketing > SEO Providers**
3. Click **+ Add SEO Provider Account**
4. Fill in the form:

**Provider Information section:**
- **Site** — select your store
- **Provider Component** — choose the installed AI provider component
- **Provider Key** — leave blank when using a component-based provider
- **Account Name** — a descriptive name such as `OpenAI SEO Provider`

**Configuration section:**
- **Is Active** — check to enable this provider
- **Is Primary** — check to use this as the default provider for all SEO generation
- **Priority** — lower numbers are tried first in the fallback chain
- **Settings** — provider-specific settings as a JSON object (e.g., model name, tone, language)

5. Click **Save**

Only one provider can be set as primary. If you mark a new provider as primary, the previous primary is automatically demoted.

### Provider fallback chain

If your primary provider fails (for example, due to an API outage), your store automatically falls back to the next active provider in priority order. This ensures SEO generation continues to work even if one provider is temporarily unavailable.

## Generating SEO content for a product

### Individual product

1. Navigate to **Products > Products** and open any product
2. Scroll to the **SEO** section of the product form
3. Click the **Generate SEO** button
4. The AI provider generates a meta title and meta description based on the product's details
5. Review the generated content and edit it if needed
6. Click **Save** to apply the changes

### Bulk generation

To generate or update SEO content for multiple products at once:

1. Navigate to **Products > Products**
2. Select the products you want to update using their checkboxes, or select all
3. Open the **Action** dropdown
4. Choose **Generate SEO content** (or similar action name — check the dropdown for the exact label)
5. Click **Go**

Spwig queues the generation tasks and processes them in the background. Refresh the product list after a minute or two to see the updated SEO fields.

## Reviewing SEO coverage

The SEO generator tracks which products already have SEO content. To identify products that still need SEO:

1. Navigate to **Products > Products**
2. Use the **SEO Status** filter (if available) to show products with missing meta titles or descriptions
3. Select those products and run the bulk generation action

## Provider settings

The **Settings** field on an SEO provider account accepts a JSON object with provider-specific configuration. Common options include:

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

These settings vary by provider component. Refer to the provider's documentation for the full list of available options.

## Managing multiple providers

If you have more than one SEO provider account configured, the provider list shows their status at a glance:

- **PRIMARY badge** — this provider is used for all SEO generation by default
- **ACTIVE badge** — the provider is enabled
- **INACTIVE badge** — the provider is disabled and will not be used

To change which provider is primary, open the provider account you want to promote, check the **Is Primary** box, and save. The system automatically ensures only one provider holds the primary flag at any time.

## Tips

- Generate SEO content for new products immediately after creating them — it takes only seconds and gives search engines something useful to index right away
- Review AI-generated meta descriptions before publishing if your products have unusual or technical names; the generator works best with clear, descriptive product names
- Set `"max_title_length": 60` and `"max_description_length": 160` in provider settings to keep generated content within Google's recommended character limits
- Run bulk SEO generation after importing a large product catalog to quickly populate all SEO fields
- If you update a product's description significantly, regenerate its SEO content to keep the meta tags aligned with the new copy
- The built-in deterministic provider is a good starting point; upgrade to an AI-powered component once your catalog is set up and you want richer, more natural-sounding SEO copy
