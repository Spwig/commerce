---
slug: manage-categories
title_i18n_key: Managing Categories
category: products
component: catalog
keywords:
  - categories
  - category
  - organize
  - hierarchy
  - product organization
  - navigation
  - collections
  - category tree
url_patterns:
  - /admin/catalog/category/
related:
  - add-product
  - design-themes
published: true
---

Categories help you organize your product catalog so customers can browse and find products easily. Navigate to **Products > Categories** in the admin sidebar.

![Category list](/static/core/admin/img/help/manage-categories/category-list.webp)

## Category List

The category management page shows all your categories as cards with:

- **Thumbnail image** — Visual identifier for the category
- **Name and slug** — Display name and URL-friendly identifier
- **Product count** — Number of products assigned to this category
- **Status** — Published or draft

Use the **filter tabs** at the top to quickly view All, Published, or Draft categories. The **search bar** lets you find categories by name.

## Creating a category

1. Click **+ Add Category** in the top right
2. Fill in the **Basic Information**:
   - **Name** — The display name customers will see. Click the globe icon to add translations.
   - **Slug** — Auto-generated from the name, used in URLs
   - **Parent Category** — Leave empty for a top-level category, or select a parent to create a subcategory
   - **Description** — Rich text description shown on the category page. Click the globe icon to translate.
3. Select images in the **Media** section from your Media Library:
   - **Image** — The main category image shown in navigation menus and category cards
   - **Banner Image** — A wider banner image displayed at the top of the category page
   - **Icon** — An icon class or identifier for compact representations
4. Configure **Display Options**:
   - **Page Template** — Override the site default layout (Grid, List, Carousel, Masonry, Featured, Accordion)
   - **Products Per Page** — Number of products shown per page in this category
   - **Show Subcategories** — Display child category links at the top of the page
5. Configure **SEO fields** (meta title, description) and optionally enable **Auto-generate SEO**
6. Set **Status** fields: **Is Active** (published), **Is Featured**, and **Sort Order**
7. Click **Save**

## Category Hierarchy

Categories support unlimited nesting to create a tree structure:

- **Top-level categories** — Main navigation items (e.g., "Clothing", "Electronics")
- **Subcategories** — Nested under a parent (e.g., "Clothing > Men's > T-Shirts")

The parent category dropdown shows the full hierarchy path to help you pick the right level.

## Category settings

### Visibility

- **Is Active** — The category appears on the storefront and in navigation when checked. Uncheck to hide it from customers without deleting it.
- **Is Featured** — Mark categories as featured to highlight them on your homepage or in special navigation sections. Featured categories can be displayed using the Page Builder's category grid element.
- **Sort Order** — Control how categories appear in navigation menus. Lower numbers appear first.

### Out of stock behavior

The **Out of Stock Action** field lets you override the site-wide or category default for products in this category that run out of stock. Options are: hide from listings, show as unavailable, show a "Notify Me" button, or allow backorders.

## Assigning Products to Categories

There are two ways to assign products:

1. **From the product edit form** — Select a category in the Category dropdown on the Basic Info tab
2. **Bulk assignment** — Select multiple products from the product list and use the bulk action to assign them to a category

Each product can belong to one primary category. Use tags or collections for additional grouping.

## Category Pages on the Storefront

Each published category automatically gets a dedicated page showing:
- Category name and description
- Banner image (if set)
- Product grid with all assigned products
- Filtering and sorting options

The category page URL follows the pattern: `yourstore.com/category/category-slug/`

## Tips

- Keep your category tree shallow — 2-3 levels deep is ideal for navigation usability.
- Use descriptive category names that match what customers search for.
- Add category images for a more visual browsing experience.
- Set up your category structure before adding products to keep things organized.
- Use the category description for SEO — include relevant keywords naturally.
