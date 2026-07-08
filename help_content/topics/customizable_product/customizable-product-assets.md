---
slug: customizable-product-assets
title_i18n_key: Clipart and Fonts for Customizable Products
category: products
component: customizable_product
keywords:
  - clipart
  - clipart library
  - clipart categories
  - clipart assets
  - custom fonts
  - font upload
  - WOFF2
  - TTF
  - font management
  - design assets
  - SVG clipart
  - font picker
  - global clipart
  - product clipart
url_patterns:
  - /admin/customizable_product/clipartcategory/
  - /admin/customizable_product/clipartasset/
  - /admin/customizable_product/customfont/
related:
  - customizable-products-overview
  - customizable-product-setup
  - customizable-product-templates
  - media-library
published: true
---

The design editor comes with two types of creative assets you can provide to customers: **clipart** (ready-made graphics they can add to their designs) and **custom fonts** (beyond the standard system fonts). Building a well-curated asset library makes the editor more useful and helps customers create better designs faster.

## Clipart library

Clipart gives customers a library of pre-made graphics they can add to their designs with a single click. Instead of requiring customers to find and upload their own images for common elements like icons, borders, or decorative graphics, you provide them ready to use.

### Creating clipart categories

Clipart is organized into categories that customers can browse. Categories help customers find what they need quickly.

1. Navigate to **Customizable Products > Clipart Categories**
2. Click **+ Add Clipart Category**
3. Fill in:
   - **Category Name** — What customers see (e.g., "Sports", "Borders", "Holiday")
   - **Slug** — Auto-generated from the name
   - **Icon** — A Font Awesome icon class for the category tab (e.g., `fas fa-football-ball`)
   - **Sort Order** — Controls the order categories appear in the editor
4. Click **Save**

**Example categories for a t-shirt store:**

| Category | Icon | Example clipart |
|----------|------|-----------------|
| Sports | `fas fa-football-ball` | Team logos, sports equipment, athletic symbols |
| Humor | `fas fa-laugh` | Memes, funny quotes, cartoon characters |
| Nature | `fas fa-leaf` | Animals, flowers, landscapes |
| Geometric | `fas fa-shapes` | Patterns, abstract shapes, tribal designs |

**Example categories for a print/poster store:**

| Category | Icon | Example clipart |
|----------|------|-----------------|
| Borders | `fas fa-border-all` | Decorative frames, corner ornaments |
| Seasonal | `fas fa-snowflake` | Holiday icons, seasonal motifs |
| Icons | `fas fa-icons` | Stars, hearts, arrows, check marks |
| Backgrounds | `fas fa-image` | Textures, gradients, patterns |

### Adding clipart assets

Each clipart asset is an image file (PNG or SVG) that customers can place on their canvas.

1. Navigate to **Customizable Products > Clipart Assets**
2. Click **+ Add Clipart Asset**
3. Fill in:
   - **Name** — Descriptive name (e.g., "Gold Star", "Football Helmet")
   - **Category** — Select from your clipart categories
   - **Image Asset** — Click to open the Media Library and select or upload the image file
   - **Scope** — Choose availability (see below)
   - **Tags** — Searchable keywords for this clipart (e.g., `["star", "gold", "decoration"]`)
   - **Sort Order** — Controls position within the category
4. Click **Save**

### Understanding clipart scope

Each clipart asset has a scope that controls where it's available:

| Scope | Description | Use case |
|-------|-------------|----------|
| **Available to All Products** | Appears in the clipart browser for every customizable product | General-purpose graphics like stars, borders, and common icons |
| **Specific Product Only** | Appears only for one selected product | Product-specific graphics like branded logos or product-themed artwork |

For most assets, use **Available to All Products**. Reserve product-specific scope for assets that only make sense in the context of one product — for example, team-specific logos for a team merchandise product.

### Clipart file guidelines

- **Format:** Use PNG for raster graphics and SVG for vector graphics. SVG files scale without quality loss, making them ideal for clipart that customers may resize significantly
- **Resolution:** PNG files should be at least 500x500 pixels for good print quality
- **Background:** Use transparent backgrounds (PNG with alpha channel or SVG) so the clipart blends naturally with the design
- **File size:** Keep individual clipart files under 500KB for fast loading in the editor

## Custom fonts

Custom fonts extend the font picker in the design editor beyond the standard system fonts. This lets you offer curated typography that matches your brand or product style.

### Adding a custom font

1. Navigate to **Customizable Products > Custom Fonts**
2. Click **+ Add Custom Font**
3. Fill in:
   - **Font Name** — Display name shown in the font picker (e.g., "Playfair Display")
   - **Font Family** — CSS font-family name used internally (e.g., `PlayfairDisplay`)
   - **Regular** — Click to upload the regular weight font file (WOFF2 or TTF) via the Media Library
   - **Bold** — Optional bold weight variant
   - **Italic** — Optional italic variant
   - **Bold Italic** — Optional bold italic variant
4. Click **Save**

The **Regular** weight is required for custom fonts. Bold, italic, and bold italic variants are optional — if not provided, the browser will attempt to synthesize these styles from the regular font, though the results may not look as polished as dedicated font files.

### System fonts vs custom fonts

You can also register system fonts that are pre-installed on most devices:

1. Add a new custom font entry
2. Check **System Font**
3. Enter the font family name exactly as it appears in CSS (e.g., `Georgia`, `Courier New`)
4. No file upload is needed for system fonts

System fonts load instantly since they're already on the customer's device. Custom uploaded fonts need to download first, which adds a small delay when the font is first selected.

### Font recommendations by product type

**For t-shirts and apparel:**
- Bold, impactful fonts work best: Impact, Anton, Bebas Neue, Oswald
- Block letters and sans-serif fonts are most readable on fabric
- Avoid thin or delicate fonts that may not print well on textured surfaces

**For posters and print products:**
- Elegant serif fonts for formal designs: Playfair Display, Merriweather, Lora
- Script fonts for invitations and cards: Great Vibes, Dancing Script, Pacifico
- Clean sans-serif for modern designs: Montserrat, Raleway, Open Sans

### Font file formats

| Format | Extension | Recommendation |
|--------|-----------|----------------|
| WOFF2 | `.woff2` | Preferred — smallest file size, fastest loading |
| TrueType | `.ttf` | Good fallback — widely compatible |

WOFF2 files are typically 30-50% smaller than TTF files, so they load faster in the customer's editor. Use WOFF2 when available.

## Managing your asset library

### Organizing for customers

The order assets appear in the editor is controlled by the **Sort Order** field on both categories and individual assets. Lower numbers appear first. Use this to:

- Put your most popular clipart categories first
- Place your best and most versatile clipart at the top of each category
- Order fonts with the most commonly used options first

### Keeping the library fresh

- Add seasonal clipart before holidays (Halloween, Christmas, Valentine's Day) and deactivate them after
- Use the **Active** checkbox to temporarily hide assets without deleting them
- Monitor which clipart and fonts customers use most and expand those categories

## Tips

- Start small — 20-30 high-quality clipart assets across 3-4 categories is better than hundreds of mediocre options. You can always add more as you learn what customers want.
- Use SVG format for clipart whenever possible. SVG files are smaller, scale perfectly to any size, and produce sharper prints than raster images.
- Test each uploaded font in the design editor to ensure all characters render correctly, especially special characters and accents if your customers use multiple languages.
- Tag clipart thoroughly — customers search by keyword, so descriptive tags like "gold", "star", "5-pointed", "decoration" help them find the right asset quickly.
- Group related clipart into the same category. If you sell team merchandise, create a category per sport rather than one giant "Sports" category.
- Regularly review your clipart library from the customer's perspective by visiting the design editor on the storefront.
