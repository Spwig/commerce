---
slug: ui-translations-management
title_i18n_key: UI Translations Management
category: translations
component: translation_service
keywords:
  - ui translations
  - interface translations
  - frontend strings
  - button translations
  - label translations
  - message translations
  - customize translations
  - translation overrides
  - ui text
  - frontend text
  - translation customization
url_patterns:
  - /admin/translations/ui-translations/
related:
  - translation-service
  - translation-coverage
  - translation-jobs
published: true
---

The UI Translations page allows you to customize how frontend interface strings—buttons, labels, error messages, and other UI text—appear in each language. Unlike product or page content translations, these are the fixed interface elements that customers see throughout your store. Customize them to match your brand voice or improve clarity for your specific audience.

This page shows all translatable UI strings and lets you override the default translations provided by Spwig.

## Understanding UI Translations

UI translations are the text strings that make up your store's interface:

**Examples of UI Strings**:
- Buttons: "Add to Cart", "Checkout", "Search"
- Labels: "Price", "Quantity", "Shipping Address"
- Messages: "Item added to cart", "Order confirmed", "Invalid email address"
- Navigation: "Home", "Shop", "Contact Us"
- Form fields: "Email", "Password", "First Name"

Spwig includes default translations for approximately 300 UI strings in all supported languages. The UI Translations page lets you override any of these defaults with your own custom translations.

## Why Customize UI Translations?

**Brand Voice**: Change "Add to Cart" to "Buy Now" or "Get Yours" to match your brand personality

**Regional Variations**: Adjust translations for specific markets (British English vs American English, European Spanish vs Latin American Spanish)

**Clarity**: If the default translation doesn't make sense for your products or audience, replace it with clearer text

**Industry-Specific Terms**: Use terminology your customers expect (e.g., "Book Appointment" instead of "Add to Cart" for service-based stores)

## Searching for Strings

Use the search box to find specific UI strings:

**Search by English text**: Type "add to cart" to find that button's translations

**Search by translation**: Type text in any language to find matching translations

**Search by key**: If you know the translation key (e.g., `cart.add_item`), search for it directly

The page updates instantly as you type, showing only matching strings.

## Viewing Translation Details

Each UI string shows:

**English Source Text** - The default English version (your reference point)

**Translation Key** - The internal identifier used in code (e.g., `cart.add_to_cart`)

**Language Columns** - Current translation for each active language

**Override Status** - Whether you've customized the translation (highlighted if overridden)

## Creating Translation Overrides

To customize a UI string's translation:

1. **Find the string** using search (e.g., search "add to cart")
2. **Click the language cell** you want to customize
3. **Enter your custom translation** in the popup editor
4. **Save** - Your override takes effect immediately

The original default translation is preserved - you're creating an override that takes priority.

## Reverting to Defaults

To remove a custom override and restore the default translation:

1. **Click the overridden translation** (these are highlighted)
2. **Click "Revert to Default"** in the editor
3. **Confirm** - The default translation is restored immediately

You can revert individual language overrides without affecting your overrides in other languages.

## Filtering by Override Status

Use the filter dropdown to view:

**All Strings** - Every UI string in the system (~300 total)

**Only Overridden** - Strings where you've created custom translations

**Only Defaults** - Strings still using Spwig's default translations

This helps you review which strings you've customized and identify gaps.

## Common Customization Examples

| English Default | Custom Override | Use Case |
|----------------|----------------|----------|
| Add to Cart | Buy Now | More direct call-to-action |
| Checkout | Secure Checkout | Emphasize security |
| Search | Find Products | More specific to e-commerce |
| Contact Us | Get in Touch | Friendlier tone |
| Subscribe | Join Our Newsletter | Clearer value proposition |

## Translation Validation

When entering custom translations, validate that:

**Length fits UI space** - Translations may be longer/shorter than English (German words are often longer, for example)

**Maintains meaning** - Don't change functionality in translation (a "Cancel" button shouldn't say "Delete")

**Consistent terminology** - Use the same translation for repeated terms throughout the interface

**Appropriate formality** - Match the tone of your target market (formal vs casual)

## Multi-Language Consistency

When customizing a string for multiple languages:

1. **Start with your default language** - Set the baseline
2. **Customize other languages** to match the same intent
3. **Test in each language** to verify layout and meaning
4. **Use native speakers** when possible to review non-English customizations

Inconsistent customizations across languages create a confusing customer experience.

## Bulk Export/Import

For extensive customizations, consider using the export/import workflow:

1. **Export** current translations as JSON or CSV
2. **Edit in spreadsheet** or text editor (easier for bulk changes)
3. **Import** updated translations back to the system

This workflow is available through the Translation Jobs page for managing large-scale translation projects.

## Tips

- **Search before customizing** - Make sure you're editing the right string; some similar strings serve different purposes
- **Test on frontend after saving** - Verify your custom translation appears correctly in the actual UI
- **Keep translations concise** - Shorter is usually better for buttons and labels
- **Document your overrides** - Keep notes on why you customized specific strings for future reference
- **Use consistent terminology** - If you customize "Cart" to "Basket", do it consistently across all related strings
- **Consider mobile layouts** - Long translations may wrap or truncate on small screens
- **Review after language updates** - When Spwig adds new default translations, review and customize them to maintain consistency
