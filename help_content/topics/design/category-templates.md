---
slug: category-templates
title_i18n_key: Category Page Templates
category: design-content
component: catalog
keywords:
  - category template
  - category layout
  - product grid
  - product list
  - product carousel
  - masonry
  - featured products
  - accordion categories
  - category display
  - page template
  - category design
  - products per row
  - pagination
  - category banner
  - sort bar
url_patterns:
  - /admin/catalog/category/
  - /theme/template-config/
related:
  - design-themes
  - page-builder
  - checkout-trust-badges
published: true
---

Category page templates control how your products are displayed when customers browse a category — whether that's a classic grid, a horizontal list, a scrollable carousel, or a dramatic featured layout. You can set a single default that applies across your entire store, and then override it on any individual category that needs a different treatment.

## Where to find the settings

There are two places to configure category templates:

- **Site-wide default** — Navigate to **Design > Page Templates** and scroll to the **Category** section. The template you choose here applies to every category page unless overridden.
- **Per-category override** — Navigate to **Catalog > Categories**, open any category, and click the **Display** tab. Setting a template here overrides the site-wide default for that category only. All other categories continue to use the default.

## The six templates

### Grid

The Grid template arranges products in a responsive card grid — the most familiar layout for online shopping. Products display as uniform cards with image, name, price, and add-to-cart button.

**Best for:** General-purpose stores, fashion, homeware, electronics — any store where consistent product presentation matters.

| Option | Description |
|--------|-------------|
| **Products per row** | How many cards appear per row on desktop (2, 3, 4, or 5) |
| **Show category banner** | Display the category's banner image at the top of the page |
| **Show subcategories** | Show clickable subcategory chips below the banner |
| **Show category description** | Display the category's description text |
| **Card image fallback** | Show a placeholder image when a product has no photo |

### List

The List template displays products as horizontal rows — image on one side, product details (name, description, price) on the other. This gives each product more breathing room and makes it easier for customers to compare at a glance.

**Best for:** Stores with complex products that benefit from a short description preview, such as tools, appliances, or B2B catalogues.

| Option | Description |
|--------|-------------|
| **Show product image** | Include the product image in each row |
| **Image position** | Whether the image appears on the left or right side |
| **Show short description** | Display a product excerpt below the product name |
| **Show category banner** | Display the category's banner image at the top |
| **Show subcategories** | Show clickable subcategory chips below the banner |
| **Show category description** | Display the category's description text |

### Carousel

The Carousel template groups products into horizontal scrolling rows — similar to the "continue browsing" sections on streaming platforms. Customers swipe or click arrows to browse through products without leaving the page.

**Best for:** Large catalogues with many products in a single category, gift shops, bookstores, or any store where browsing and discovery are a priority.

| Option | Description |
|--------|-------------|
| **Slides per view** | How many products are visible at once on desktop (3, 4, or 5) |
| **Row size** | How many products per carousel row before starting a new row below (4, 6, 8, or 12) |
| **Show navigation arrows** | Show previous/next arrow buttons on each row |
| **Show dots** | Show a progress bar and page counter (e.g. "1 / 3") below each row |
| **Autoplay** | Automatically advance slides |
| **Autoplay speed** | Time in milliseconds between each auto-advance |
| **Infinite loop** | Wrap back to the first slide after reaching the last |
| **Show category banner** | Display the category's banner image at the top |
| **Show subcategories** | Show clickable subcategory chips below the banner |

### Masonry

The Masonry template creates a Pinterest-style staggered grid where each card adapts to its image's natural height. The result is a varied, editorial feel rather than a uniform grid.

**Best for:** Photography, art prints, handmade goods, interior design, or any category where the visual character of products varies and you want to showcase them in a more dynamic way.

| Option | Description |
|--------|-------------|
| **Columns** | Number of columns across the page (2, 3, or 4) |
| **Gap size** | Space between cards — small, medium, or large |
| **Show category banner** | Display the category's banner image at the top |
| **Show subcategories** | Show clickable subcategory chips below the banner |
| **Show category description** | Display the category's description text |

### Featured

The Featured template promotes a small number of products as large hero cards at the top of the page, with the remaining products displayed in a supporting grid below. It draws immediate attention to your priority products.

**Best for:** New arrivals sections, bestseller pages, curated collections, or seasonal categories where you want to spotlight specific products.

| Option | Description |
|--------|-------------|
| **Featured products count** | How many products receive hero treatment at the top (1, 2, or 3) |
| **Hero layout** | Display the hero cards full-width or as a split layout side by side |
| **Show category banner** | Display the category's banner image at the top |
| **Show subcategories** | Show clickable subcategory chips below the banner |
| **Show category description** | Display the category's description text |

### Accordion

The Accordion template is designed specifically for the **root categories page** — the page that shows all your top-level categories. It displays each category as an interactive panel; hovering or tapping a panel causes it to expand horizontally while the others compress. On individual category pages, the Accordion template falls back to a standard grid.

**Best for:** Stores with visually strong category images where you want the categories page itself to feel like an immersive experience — fashion brands, lifestyle stores, and stores with strong editorial identity.

| Option | Description |
|--------|-------------|
| **Panels per row** | Maximum categories per accordion row before wrapping to a new row below (4–8, default 6) |
| **Height** | How tall the accordion panels are — small, medium, large, or extra large |
| **Expand ratio** | How much wider the active (hovered) panel expands compared to inactive panels (2–5×) |
| **Transition speed** | Animation speed in milliseconds |
| **Mobile layout** | How categories display on mobile — stacked vertically, as a carousel, or as a grid |
| **Show product count** | Display a product count badge on each category panel |

## Common options (all templates)

Every template shares a set of options that control the surrounding page chrome:

| Option | Description |
|--------|-------------|
| **Show breadcrumb** | Display "Home > Categories > Name" navigation above the category |
| **Show sort bar** | Show the "Sort by" dropdown so customers can reorder results |
| **Show product count** | Display the total product count (e.g. "29 products") |
| **Show help section** | Display a "Can't find what you're looking for?" section at the bottom |
| **Default sort** | The sort order used when a customer first lands on the page |
| **Products per page** | How many products to load per page |
| **Pagination style** | How additional products are loaded: paginated pages, a "Load more" button, or infinite scroll |

## Quick comparison

Use this table to pick the right template at a glance:

| Template | Products per row | Visual character | Best product types |
|----------|-----------------|------------------|--------------------|
| **Grid** | 2–5 configurable | Uniform, clean | Everything — the safe default |
| **List** | 1 (full-width rows) | Spacious, informative | Complex or technical products |
| **Carousel** | 3–5 visible at once | Browsable, dynamic | Large catalogues, discovery |
| **Masonry** | 2–4 (staggered) | Editorial, varied | Visual/artisan products |
| **Featured** | Hero + grid below | Promotional | Curated picks, new arrivals |
| **Accordion** | N/A (categories) | Immersive, dramatic | Root categories page |

## Setting a site-wide default template

1. Navigate to **Design > Page Templates**.
2. Scroll to the **Category** section.
3. Select your preferred template from the **Template** dropdown.
4. Configure the template options that appear below the dropdown.
5. Configure the common options (sort bar, breadcrumb, pagination, etc.).
6. Click **Save Configuration**.

The selected template and its settings now apply to every category page in your store.

## Overriding the template for a specific category

You can give any individual category a different template without changing the store-wide default.

1. Navigate to **Catalog > Categories**.
2. Click the category you want to customise.
3. Click the **Display** tab at the top of the edit form.
4. Under **Template**, choose **Custom** to enable the per-category settings.
5. Select the template you want for this category.
6. Configure the template options as needed.
7. Click **Save**.

Only this category will use the custom template. All other categories continue to use the site-wide default. To revert a category back to the default, return to its Display tab and set the template back to **Use site default**.

## Example: mixing templates across categories

Here is a practical example of how different templates can serve different parts of the same store:

| Category | Template | Reason |
|----------|----------|--------|
| All categories (root page) | Accordion | Dramatic visual entry point |
| Clothing | Grid (4 per row) | Fast, familiar browsing |
| Sale | Featured | Highlights top deals immediately |
| Books | Carousel | Large catalogue, easy to browse |
| Handmade Gifts | Masonry | Varied image sizes, artisan feel |
| Industrial Tools | List | Customers need to see descriptions |

## Tips

- Start with the **Grid** template as your site-wide default — it works well for almost all product types and is the most familiar layout for shoppers. Customise individual categories from there.
- Use the **Featured** template sparingly. It works best when you can genuinely curate 1–3 standout products for that category. If all products look equally important, the hero treatment loses its effect.
- The **Accordion** template only creates its full visual impact on the root categories page. If you assign it to a product category, customers will see a plain grid — so reserve it for your top-level categories listing.
- Set **products per page** thoughtfully. 24–36 products per page works well for the Grid and Masonry templates. For the Carousel, the row size and slides-per-view settings control this experience more directly.
- Enable **Show subcategories** on parent categories so customers can jump straight to a narrower selection without needing to use the sort or filter tools.
- Test your chosen template on mobile. The Masonry and Carousel templates in particular look very different on small screens — use the **mobile layout** option on Accordion, and check that Masonry columns are not too narrow on phones.
- When using the List template with **Show short description** enabled, make sure your products actually have short descriptions set. Empty description rows look unintentional.
