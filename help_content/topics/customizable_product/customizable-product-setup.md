---
slug: customizable-product-setup
title_i18n_key: Setting Up a Customizable Product
category: products
component: customizable_product
keywords:
  - design setup
  - design surfaces
  - mockup image
  - design zone
  - DPI
  - bleed
  - surface constraints
  - t-shirt design setup
  - print design setup
  - custom product setup
  - upload restrictions
  - design fees
  - pricing
  - per surface fee
  - editor mode
url_patterns:
  - /admin/customizable-product/product/\d+/design-setup/
  - /admin/catalog/product/\d+/change/
related:
  - customizable-products-overview
  - customizable-product-assets
  - customizable-product-templates
  - add-product
published: true
---

This guide walks you through the complete setup process for a customizable product, from creating the product to configuring surfaces, pricing, and upload restrictions. Two practical examples are used throughout: a **custom t-shirt** (multi-surface apparel) and a **custom poster** (single-surface print).

## Step 1: Create the product

1. Navigate to **Products > All Products** and click **+ Add Product**
2. Set **Product Type** to **Customizable Product**
3. Fill in the product name, description, images, and pricing as you would for any product
4. Save the product

After saving, a new **Open Design Editor Setup** button appears on the product form. This takes you to the dedicated setup page where you configure the visual design editor.

## Step 2: Access the design editor setup

1. Open the product you just created in the admin
2. Click the **Open Design Editor Setup** button (in the Customizable Product section)
3. The setup page opens with three tabs: **Surfaces**, **Settings**, and **Pricing**

The setup page is where you define everything about the design editor for this product.

## Step 3: Add design surfaces

A surface represents one designable face of your product. Click **+ Add Surface** to create each surface.

### T-shirt example: 3 surfaces

| Surface | Name | Dimensions | Design zone | Notes |
|---------|------|-----------|-------------|-------|
| 1 | Front | 300 x 400 mm | Centered chest area | Main design area |
| 2 | Back | 300 x 400 mm | Upper back area | Secondary design area |
| 3 | Left Sleeve | 100 x 100 mm | Upper arm area | Small logo area only |

### Poster example: 1 surface

| Surface | Name | Dimensions | Design zone | Notes |
|---------|------|-----------|-------------|-------|
| 1 | Front | 210 x 297 mm (A4) | Full printable area | Single surface, high DPI |

### Configuring each surface

For each surface, you configure the following:

**Basic information:**
- **Name** — What customers see in the surface tabs (e.g., "Front", "Back")
- **Slug** — URL-safe identifier, auto-generated from the name
- **Sort Order** — Controls the order surfaces appear (lower numbers first)

**Mockup image:**
- Click the mockup image area to open the Media Library and select a product photo showing this surface
- Use a high-quality photo of your product from the correct angle

**Design zone positioning:**
- After selecting a mockup image, a rectangular overlay appears on the preview
- **Drag** the overlay to position where the design zone should be on the mockup
- **Resize** the overlay by dragging its edges to define the design area boundaries
- The zone is stored as percentage-based coordinates, so it scales to any screen size

The design zone tells the editor exactly where on the product image the customer's design will appear. Position it carefully to match the actual printable area of your product.

**Physical dimensions:**
- **Width** and **Height** — The real-world dimensions of the design area
- **Unit** — Millimeters, inches, or pixels
- These dimensions determine the aspect ratio of the design canvas and are used to calculate print DPI

**Print settings:**
- **Minimum DPI** — The lowest acceptable dots-per-inch. Customers see a warning if their uploaded images fall below this. Default: 150
- **Recommended DPI** — The ideal resolution for best print quality. Default: 300
- **Bleed (mm)** — Extra margin outside the design area for printing bleed. Set to 0 if no bleed is needed (common for apparel), or 3mm for professional print products
- **Max Colors** — For screen printing, you can limit the number of colors. Leave blank for unlimited (digital printing)
- **Background Color** — Default canvas background color

### T-shirt vs poster print settings

| Setting | T-shirt | Poster |
|---------|---------|--------|
| Minimum DPI | 150 | 200 |
| Recommended DPI | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Max Colors | 6 (screen printing) | Blank (unlimited) |
| Background Color | Match garment color | `#ffffff` (white) |

## Step 4: Per-surface constraints

Each surface can override the global feature settings. This lets you allow different tools on different surfaces.

The constraint options are:

| Setting | Options | Description |
|---------|---------|-------------|
| **Allow Text** | Inherit / Yes / No | Whether customers can add text on this surface |
| **Allow Image Upload** | Inherit / Yes / No | Whether customers can upload images to this surface |
| **Allow Clipart** | Inherit / Yes / No | Whether customers can use clipart on this surface |
| **Max Elements** | Number or blank | Maximum design elements allowed on this surface |

When set to **Inherit**, the surface uses whatever is configured in the global settings (Step 6). When set to **Yes** or **No**, it overrides the global setting for that specific surface.

### Example: T-shirt sleeve constraint

For the t-shirt's sleeve surface, you might want to restrict customization to a small logo only:

| Setting | Value | Reason |
|---------|-------|--------|
| Allow Text | No | Too small for readable text |
| Allow Image Upload | Yes | Allow a small logo upload |
| Allow Clipart | No | Keep it simple |
| Max Elements | 1 | Only one logo |

The front and back surfaces would remain set to **Inherit**, allowing all tools as defined in the global settings.

### Example: Poster constraint

For a poster, all surfaces typically inherit from the global config since there's only one surface and all tools should be available. No per-surface overrides are needed.

## Step 5: Configure upload restrictions

On the **Settings** tab, configure how customers can upload files:

| Setting | Description | T-shirt example | Poster example |
|---------|-------------|-----------------|----------------|
| **Max Upload Size** | Maximum file size per upload | 10 MB | 20 MB |
| **Max Uploads Per Surface** | How many images per surface | 5 | 3 |
| **Allowed Upload Types** | Accepted file formats | JPG, PNG, WebP | JPG, PNG, WebP |

Larger file size limits are recommended for print products where customers need to upload high-resolution images.

## Step 6: Editor settings

On the **Settings** tab, configure the global editor behavior:

**Editor Mode:**
- **Canvas Editor** — Full visual editor with live canvas preview. Recommended for most products.
- **Simple Form** — Traditional form fields for basic customization (e.g., engraving text only).

**Feature toggles (global defaults):**
- **Allow Text** — Let customers add text elements
- **Allow Image Upload** — Let customers upload their own images
- **Allow Clipart** — Let customers browse and use your clipart library

These global settings apply to all surfaces unless overridden by per-surface constraints (Step 4).

## Step 7: Configure pricing

On the **Pricing** tab, set the design fees that are added to the product's base price:

| Fee | Description |
|-----|-------------|
| **Base Design Fee** | Flat fee added when any customization is applied |
| **Per Surface Fee** | Additional fee for each surface used beyond the first |
| **Per Upload Fee** | Fee for each customer-uploaded image |
| **Per Text Fee** | Fee for each text element added |

### Example: T-shirt pricing

| Fee | Amount | Rationale |
|-----|--------|-----------|
| Base Design Fee | $5.00 | Covers setup cost for any custom order |
| Per Surface Fee | $2.00 | Each additional surface adds printing cost |
| Per Upload Fee | $1.00 | Custom images require processing |
| Per Text Fee | $0.50 | Text is simpler than images to produce |

**Calculation example:** A customer designs a t-shirt with text on the front and a logo on the back:
- Base design fee: $5.00
- 1 extra surface (back): $2.00
- 1 uploaded logo: $1.00
- 1 text element: $0.50
- **Total design fee: $8.50** (added to the product's base price)

### Example: Poster pricing

| Fee | Amount | Rationale |
|-----|--------|-----------|
| Base Design Fee | $0.00 | No base fee — the product price covers it |
| Per Surface Fee | $0.00 | Single surface, not applicable |
| Per Upload Fee | $2.00 | High-resolution processing |
| Per Text Fee | $0.00 | Text is included in the base experience |

**Calculation example:** A customer creates a poster with 2 uploaded photos and 3 text elements:
- Base design fee: $0.00
- 2 uploaded photos: $4.00
- 3 text elements: $0.00
- **Total design fee: $4.00**

The design fee is displayed to customers in real time as they add elements, so they can see the cost impact of each addition before adding to cart.

## Setup comparison at a glance

| Aspect | Custom T-shirt | Custom Poster |
|--------|---------------|---------------|
| Surfaces | 3 (front, back, sleeve) | 1 (front) |
| Mockup images | 3 product photos | 1 product photo |
| Zone positioning | Chest/back/arm areas | Full printable area |
| Dimensions | 300x400mm, 100x100mm | 210x297mm (A4) |
| DPI minimum | 150 | 200 |
| Bleed | 0 mm | 3 mm |
| Max colors | 6 | Unlimited |
| Per-surface constraints | Sleeve restricted | None needed |
| Pricing model | Base + surface + upload + text | Upload-only fees |

## Tips

- Always test the design editor from the customer's perspective after completing setup. Visit the product page on the storefront and try adding text, uploading an image, and switching surfaces.
- Upload mockup images that closely match the actual product appearance. For t-shirts, photograph each angle separately. For posters, use a clean flat-lay photo or a frame mockup.
- Position the design zone conservatively — it's better to define a slightly smaller zone than to have designs printing into seams or edges.
- Set the minimum DPI based on your print method: 150 for screen printing, 200 for standard digital printing, 300 for high-quality offset printing.
- Use 3mm bleed for any product that will be trimmed after printing (posters, business cards, flyers). Set bleed to 0 for products where the design is applied to an existing surface (t-shirts, mugs, phone cases).
- Start with simple pricing and adjust based on customer feedback. Many merchants begin with just a base design fee and add per-element fees later.
