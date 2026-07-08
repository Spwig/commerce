---
slug: product-collections
title_i18n_key: Product Collections
category: products
component: catalog
keywords:
  - product collections
  - collections
  - featured products
  - manual collection
  - automatic collection
  - seasonal collection
  - product grouping
  - storefront collections
  - collection page
  - collection SEO
  - curated products
  - product display
related:
  - manage-categories
  - product-brands
  - add-product
  - sales-promotions
url_patterns:
  - /admin/catalog/collection/
published: true
---

Collections let you group products together for display on your storefront. Unlike categories — which organise your entire catalogue into a permanent hierarchy — collections are flexible, curated groupings you create for a specific purpose. A collection might highlight new arrivals, showcase items for a seasonal campaign, or present a hand-picked selection of bestsellers.

Navigate to **Catalog > Collections** to manage your collections.

## Collections vs categories

Both categories and collections group products, but they serve different purposes:

| | Categories | Collections |
|---|---|---|
| **Purpose** | Permanent catalogue structure | Flexible, curated groupings |
| **Hierarchy** | Yes — nested parent/child structure | No — flat groupings |
| **Products per group** | Each product belongs to one category | A product can appear in many collections |
| **Typical use** | Shop navigation menu, browse by department | Landing pages, campaigns, featured sets |

Use categories for "how your shop is organised" and collections for "what you want to spotlight right now".

## Collection types

When creating a collection, choose a type that matches how you want to manage the product list:

| Type | How products are added |
|---|---|
| **Manual Selection** | You choose exactly which products appear, one by one |
| **Automatic Rules** | Products are added automatically based on criteria you define |
| **Featured Products** | A curated editorial selection, managed manually |
| **Seasonal** | A time-based selection, typically managed manually for campaigns |

Manual and Featured types give you precise control. Automatic collections can grow with your catalogue without ongoing maintenance.

## Creating a collection

1. Navigate to **Catalog > Collections**
2. Click **+ Add Collection**
3. Fill in the **Basic Information** section:
   - **Name** — the name of the collection as it will appear on your storefront
   - **Slug** — the URL path for the collection page (auto-filled from the name; you can customise it)
   - **Description** — a description displayed on the collection's storefront page
4. Select a **Collection Type**
5. Add products:
   - For **Manual Selection** and **Featured Products** types: use the **Products** field to search for and add products
   - For **Automatic** type: define the criteria in the **Auto Criteria** field
6. Upload images:
   - **Image** — the main collection image used on listing pages and thumbnails
   - **Banner Image** — a wider banner image displayed at the top of the collection page
7. Configure **SEO** fields (optional but recommended):
   - **Meta Title** — the page title shown in search results
   - **Meta Description** — the description shown below the title in search results
8. Set **Display Options**:
   - **Is Active** — controls whether the collection is visible on your storefront
   - **Is Featured** — marks the collection for featured placement in your theme
   - **Sort Order** — controls the order in which collections appear in listing pages (lower numbers appear first)
9. Click **Save**

## Adding products to a collection

For manual collections, use the **Products** autocomplete field to search your catalogue and select items. You can add as many products as you need — there is no limit.

Products can belong to multiple collections at the same time. For example, a product could be in both your "Summer Sale" collection and your "Bestsellers" collection without any conflict.

## Displaying collections on your storefront

Each collection automatically gets its own page at `/collection/{slug}/`. You can link to collection pages from your navigation menu, the page builder, or promotional banners.

The **Is Featured** flag is used by your theme to determine which collections appear in featured spots — for example, a homepage grid of highlighted collections. Check with your theme documentation to understand exactly how featured collections are displayed.

## Managing collection visibility

- **Is Active** controls whether the collection page is publicly accessible. An inactive collection is hidden from customers but preserved in the admin so you can reactivate it later.
- **Sort Order** determines the order in which collections appear on listing pages. Assign lower numbers to collections you want to appear first.

## SEO for collections

Each collection has its own **Meta Title** and **Meta Description** fields. These control what appears in search engine results when someone finds your collection page. If you leave these blank, your theme will typically fall back to the collection name and description.

Good collection SEO titles are descriptive and specific:
- "Summer Dresses 2026 — Floral & Lightweight Styles" performs better than "Summer Collection"
- "Men's Running Shoes — Lightweight & Breathable" performs better than "Running Shoes"

## Tips

- Keep collection names short and clear — they appear as page headings and link text in your storefront navigation
- Use seasonal or campaign collections with a start and end plan: create the collection, activate it when the campaign begins, and deactivate it (rather than delete it) when it ends so you can reference it later
- The **Sort Order** field is worth setting deliberately — the default is 0 for all collections, which means they sort alphabetically. Assign specific numbers to control which collections appear most prominently
- A collection with no products will show an empty page to customers — either add products before activating, or leave the collection inactive until it is ready
- Check the **Is Featured** flag only for collections you genuinely want to highlight; most themes reserve featured slots for a small number of collections and the display can look crowded if too many are flagged
