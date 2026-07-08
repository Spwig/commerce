---
slug: custom-elements
title_i18n_key: Custom Elements
category: design-content
component: element_builder
keywords:
  - custom element
  - element builder
  - page builder element
  - data binding
  - product element
  - category element
  - create element
  - visual builder
  - custom block
  - dynamic content
  - bind product data
  - reusable element
  - element library
url_patterns:
  - /admin/element_builder/customelement/
related:
  - page-builder
  - design-themes
published: true
---

Custom elements let you build reusable page builder blocks that are tailored to your store's needs. You design an element visually using the page builder's existing tools, then optionally connect it to live store data — such as product names, prices, or images — so the element automatically populates with real content when placed on a page. Once created, your custom elements appear in the page builder's element library alongside the built-in blocks.

![Custom Elements Library](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## When to use custom elements

Custom elements are most valuable when you find yourself building the same layout repeatedly. Instead of recreating a "featured product card" from scratch on every page, you build it once as a custom element and drop it wherever you need it. If the element is data-bound, it pulls current product information automatically — no manual updates needed when prices or names change.

Common uses:

- Product highlight cards that show name, price, and main image
- Category promo blocks with banner, title, and link
- Brand showcase panels with logo and description
- Blog post teasers with featured image, title, and excerpt

## Creating a new custom element

1. Navigate to **Design > Custom Elements**
2. Click **+ Add Custom Element**
3. Spwig immediately creates a draft element and opens the **Visual Builder** — you do not need to fill in a form first
4. In the Visual Builder, build your element's layout using the available page builder tools
5. When you are satisfied with the design, configure the element's settings (name, data binding, icon) in the sidebar
6. Set **Active** to on when you are ready to publish the element to the library
7. Save the element

The element is now available in the page builder's element panel under the category you assigned.

## The visual builder

The Visual Builder is a dedicated canvas for designing your element. It works like the standard page builder but focuses on a single element rather than an entire page. You can:

- Add and arrange child elements (text blocks, images, containers, etc.)
- Set styling, spacing, and layout for each child
- Preview how the element will look with sample data

Changes in the Visual Builder are saved directly to the element definition. There is no separate publish step — saving in the builder updates the element immediately for any pages that already use it.

## Configuring element settings

Each custom element has these settings:

| Field | Description |
|-------|-------------|
| **Name** | Display name shown in the element library |
| **Slug** | URL-safe identifier, auto-generated from the name |
| **Description** | Optional note about what this element is for |
| **Target Model** | The store model to bind data from (see below) |
| **Icon** | Icon shown in the element library |
| **Category** | Groups related elements together in the library |
| **Active** | Whether the element is available in the page builder |

## Data binding

Data binding connects parts of your element's layout to live store data. When a page editor places a data-bound element on a page, they select a specific record (for example, a product), and all bound fields populate automatically from that record.

### Choosing a target model

The **Target Model** setting determines which type of store data the element can display. The available models are:

| Model | What it provides |
|-------|-----------------|
| **Product** | Name, price, stock status, images, description, SKU, category, brand, and more |
| **Category** | Name, description, image, banner, product count, and URL |
| **Brand** | Name, logo, description, brand story, and URL |
| **Blog Post** | Title, excerpt, featured image, author, publish date, and URL |

Leave **Target Model** empty to create a static element with no dynamic data. Static elements are useful for fixed design components like decorative banners or layout spacers.

### How bindings work

Within the Visual Builder, you can mark individual child elements as data-bound by selecting the model field they should display. For example:

- A **text** child element can be bound to **Product Name**, so it shows the selected product's name
- An **image** child element can be bound to **Main Image**, so it shows the product's primary photo
- A **text** child element can be bound to **Price**, so it always reflects the current price

Each binding maps one element content field to one model field. You can add multiple bindings to a single custom element — for instance, binding a text block to **Product Name** and a separate image block to **Main Image** at the same time.

### Image thumbnail presets

For image bindings, you can optionally specify a **Thumbnail Preset** (such as `thumbnail` or `medium`). This controls the size of the image that is loaded, helping pages load faster by serving the appropriately sized image for the element's layout.

## Deactivating and reactivating elements

Deactivating an element removes it from the element library so it cannot be added to new pages. Existing pages that already use the element are not affected — the element continues to render on those pages.

To deactivate:

1. Navigate to **Design > Custom Elements**
2. Click on the element name
3. Uncheck **Active**
4. Save

To reactivate, follow the same steps and check **Active** again.

## Filtering the element library

The element list supports filtering by:

- **Active / Inactive** — show only published or only draft elements
- **Target Model** — filter by the model an element is bound to
- **Category** — filter by element category
- **Search** — search by name, slug, or description

This helps when you have many custom elements and need to find a specific one quickly.

## Example: product highlight card

**Goal:** A card element that shows a product's main image, name, and price.

| Setting | Value |
|---------|-------|
| Name | Product Highlight Card |
| Target Model | Product |
| Category | Products |
| Icon | fas fa-box |

In the Visual Builder, add:
- An **Image** element bound to **Main Image** with thumbnail preset `medium`
- A **Text** element bound to **Product Name**
- A **Text** element bound to **Price**

Once saved and activated, the element appears in the page builder under the Products category. When a page editor adds it to a page, they select which product to feature, and the card auto-populates.

## Tips

- Give elements descriptive names that include their purpose and the data type — for example, "Product Highlight Card" rather than "Card 1" — so the library stays easy to navigate as it grows
- Use the **Category** field to group related elements (Products, Blog, Promotions) — this keeps the element library organised for your page editors
- Test data-bound elements by adding them to a draft page and selecting a real record before publishing, to confirm the binding is pulling the right information
- Deactivate outdated elements rather than deleting them — this preserves any pages that still reference them and gives you the option to reactivate later
- Static elements (no target model) are ideal for layout patterns you reuse across the site, such as dividers, CTA panels, or branded spacers
