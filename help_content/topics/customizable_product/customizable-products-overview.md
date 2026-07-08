---
slug: customizable-products-overview
title_i18n_key: Customizable Products
category: products
component: customizable_product
keywords:
  - customizable product
  - design editor
  - product designer
  - custom t-shirt
  - custom print
  - canvas editor
  - personalized product
  - product customization
  - design your own
  - custom merchandise
  - print on demand
  - product personalization
url_patterns:
  - /admin/catalog/product/
  - /admin/catalog/product/\d+/change/
  - /admin/customizable-product/
related:
  - add-product
  - customizable-product-setup
  - customizable-product-assets
  - customizable-product-templates
  - customizable-product-orders
published: true
---

Customizable products let your customers design their own products using a visual editor directly on your storefront. Whether you sell custom t-shirts, personalized posters, branded merchandise, or greeting cards, this feature gives customers the tools to add text, upload images, and use clipart to create unique designs — all without leaving your store.

## How it works

A customizable product combines a standard Spwig product with a **visual design editor**. You define the product's designable surfaces (such as the front and back of a t-shirt), upload mockup images so customers can see their design in context, and set the rules for what customers can do on each surface.

When a customer visits a customizable product on your storefront, they see a live canvas editor overlaid on your product mockup. They can add text, upload their own images, and browse your clipart library to build their design. The editor shows the design exactly as it will look on the finished product.

### Two use cases

Customizable products work well across two common scenarios:

| Use case | Example | Surfaces | Typical setup |
|----------|---------|----------|---------------|
| **Apparel design** | Custom t-shirts, hoodies, tote bags | Multiple (front, back, sleeves) | Bold fonts, humor/sports clipart, per-surface constraints |
| **Print design** | Posters, greeting cards, business cards | Single (front only) | High DPI, bleed settings, elegant fonts, decorative borders |

The setup process is the same for both — the difference lies in how many surfaces you define, what clipart and fonts you provide, and how you configure print settings.

## Key concepts

### Design configuration

Every customizable product has a **design configuration** that controls the overall editor behavior: which tools are available (text, image upload, clipart), upload limits, and pricing rules. This is the master control panel for the product's design editor.

### Surfaces

A **surface** is a designable face of your product. A t-shirt typically has three surfaces (front, back, sleeve), while a poster has just one. Each surface has its own mockup image, design zone position, physical dimensions, and print quality settings.

### Design zone

The **design zone** is the rectangular area on the mockup image where customers can place their design elements. You position this zone visually in the admin setup page by dragging and resizing it over the mockup image. The zone defines where designs appear on the finished product.

### Templates

**Design templates** are pre-made starting designs that you create for customers. Instead of starting from a blank canvas, customers can browse your template gallery, pick one they like, and customize it. Templates can include locked elements that customers cannot modify — for example, a company logo that must always appear in the same position.

### Clipart and fonts

You build a **clipart library** of images that customers can add to their designs, organized into categories (e.g., "Sports", "Borders", "Holiday"). You can also upload **custom fonts** beyond the standard system fonts, giving customers more creative options.

### Pricing

The design editor supports a flexible pricing model with four fee components:

| Fee type | Description |
|----------|-------------|
| **Base design fee** | Flat fee added when any customization is applied |
| **Per surface fee** | Additional fee for each surface used beyond the first |
| **Per upload fee** | Fee for each customer-uploaded image |
| **Per text fee** | Fee for each text element added |

Pricing updates in real time as the customer adds elements, so there are no surprises at checkout.

## Editor modes

Spwig offers two editor modes:

- **Canvas Editor** — A full visual design editor with a live canvas, text tools, image upload, clipart browser, and real-time preview on the product mockup. This is the recommended mode for most customizable products.
- **Simple Form** — A traditional form-based approach where customers fill in text fields and upload images without a visual canvas. Suitable for products with minimal customization (e.g., engraving a name on a piece of jewelry).

## Merchant workflow

Setting up a customizable product follows this workflow:

1. **Create the product** — Add a new product with type set to **Customizable Product**
2. **Set up surfaces** — Define each designable face, upload mockup images, and position the design zones
3. **Configure settings** — Choose which tools to enable, set upload limits, and configure pricing
4. **Add assets** — Build your clipart library and upload custom fonts
5. **Create templates** — Design pre-made starting points with optional lock controls
6. **Test and publish** — Preview the editor on the storefront and verify everything works

For detailed setup instructions, see [Setting Up a Customizable Product](/admin/customizable-product/).

## Customer experience

When a customer visits a customizable product on your storefront:

1. **Browse templates** — They can start from a pre-made template or begin with a blank canvas
2. **Switch surfaces** — Tabs at the top let them switch between surfaces (e.g., front and back of a t-shirt)
3. **Add elements** — The tool panel provides text, image upload, and clipart tools
4. **Customize** — They can adjust fonts, colors, sizes, positions, and apply image filters
5. **See pricing** — The design fee updates in real time as they add elements
6. **Save designs** — Registered customers can save designs to continue editing later
7. **Add to cart** — The design is linked to the cart item and frozen when the order is placed

## What happens after ordering

When a customer places an order containing a customized product:

- The design is **frozen as a snapshot** — it cannot be modified after purchase
- The system generates **high-resolution fulfillment files** for each surface
- You can download these print-ready files from the order detail page in your admin panel
- The files are rendered at the DPI you configured for each surface

For details on fulfilling customized orders, see [Fulfilling Customizable Product Orders](/admin/orders/).

## Tips

- Start with a simple product (one surface, like a poster) to learn the setup process before tackling multi-surface products like t-shirts.
- Upload high-quality mockup images — they're the first thing customers see and set the quality expectation for the entire experience.
- Create 3-5 design templates for each product to reduce the "blank canvas" intimidation and inspire customers.
- Use per-surface constraints to control what customers can do on each surface. For example, allow only a small logo upload on a t-shirt sleeve while allowing full design freedom on the front.
- Set minimum DPI requirements appropriate to your print method — 150 DPI for screen printing, 300 DPI for high-quality digital printing.
- Test the full customer flow (design, save, add to cart, checkout) before publishing a customizable product.
