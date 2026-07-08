---
slug: customizable-product-templates
title_i18n_key: Design Templates for Customizable Products
category: products
component: customizable_product
keywords:
  - design templates
  - template editor
  - pre-made designs
  - lock controls
  - lock position
  - lock content
  - lock delete
  - template categories
  - starting design
  - visual template editor
  - design starting point
  - template lock
  - template builder
url_patterns:
  - /admin/customizable-product/product/\d+/template-editor/
  - /admin/customizable-product/product/\d+/design-setup/
related:
  - customizable-products-overview
  - customizable-product-setup
  - customizable-product-assets
published: true
---

Design templates are pre-made starting designs that you create for your customers. Instead of facing a blank canvas, customers can browse your template gallery, pick a design they like, and customize it to their taste. Templates significantly improve conversion because they reduce the effort and creativity needed to get started.

## Why templates matter

Most customers visiting a customizable product page are not graphic designers. A blank canvas can be intimidating. Templates solve this by providing:

- **Inspiration** — Customers see what's possible with your product
- **Speed** — Starting from a template is faster than building from scratch
- **Quality** — Your professionally designed templates ensure a better end result
- **Guidance** — Templates show customers where to place elements for the best look

## Creating a template

Templates are created from the **Design Editor Setup** page for each product.

1. Navigate to the product's **Design Editor Setup** page
2. Switch to the **Templates** section (visible in the setup page tabs or as a scrollable section)
3. Click **+ Add Template**
4. Fill in the template details:
   - **Name** — Descriptive name customers will see (e.g., "Team Spirit", "Birthday Celebration")
   - **Slug** — URL-safe identifier, auto-generated from the name
   - **Description** — Optional short description
   - **Category** — Group related templates (e.g., "Birthday", "Business", "Holiday", "Sports")
   - **Sort Order** — Controls the order templates appear in the gallery
5. Save the template

## The visual template editor

After creating a template, you can open the **visual template editor** to design the canvas layout. This is where you place text, images, and clipart on each surface, and set lock controls for individual elements.

### Working with the canvas

The template editor provides the same canvas tools available to customers:

- **Text tool** — Add text elements with font, size, color, and alignment options
- **Image tool** — Add images from the Media Library
- **Clipart tool** — Browse and add clipart from your library

You work on one surface at a time. Use the **surface tabs** at the top of the canvas to switch between surfaces (e.g., switch from Front to Back for a t-shirt template).

### Adding elements

1. Select a tool from the tool panel (Text, Image, or Clipart)
2. Click **Add Text**, upload an image, or click a clipart to add it to the canvas
3. Position and resize the element by dragging on the canvas
4. Use the properties panel to adjust styling (font, color, size, alignment, etc.)
5. Repeat for each element you want in the template

### Saving the template

When you're done designing, click **Save Template**. The system captures a thumbnail preview image automatically from the canvas state. This thumbnail is what customers see when browsing the template gallery.

## Lock controls

Lock controls are a powerful feature that lets you restrict what customers can do with specific elements in a template. This is essential for maintaining brand consistency, ensuring design quality, and enforcing business rules.

When an element is selected in the template editor, you can set five types of locks:

| Lock | Effect | Use case |
|------|--------|----------|
| **Lock Position** | Customer cannot move the element | Keep a logo in its designated spot |
| **Lock Size** | Customer cannot resize the element | Prevent a logo from being distorted |
| **Lock Rotation** | Customer cannot rotate the element | Keep text horizontal and readable |
| **Lock Content** | Customer cannot edit the text or replace the image | Protect brand names, required legal text |
| **Lock Delete** | Customer cannot remove the element | Ensure mandatory elements always appear |

Locks can be combined. For example, a company logo might have all five locks enabled (can't move, resize, rotate, edit, or delete it), while a "Your Name Here" text field might only lock position and size (customer can edit the text content but not reposition it).

### Example: "Team Spirit" t-shirt template

A t-shirt template designed for sports teams:

**Front surface elements:**

| Element | Type | Locks | Customer can... |
|---------|------|-------|----------------|
| Team logo (top center) | Image | Position, Size, Content, Delete | Nothing — logo is fully locked |
| Player name | Text | Position, Size | Edit the name text |
| Player number | Text | Position, Size | Edit the number |

**Back surface elements:**

| Element | Type | Locks | Customer can... |
|---------|------|-------|----------------|
| Team name (top) | Text | Position, Size, Content, Delete | Nothing — team name is fixed |
| Custom message | Text | Position | Edit text, resize, and rotate |

This template ensures the team branding is consistent across all orders while letting customers personalize their name and number.

### Example: "Birthday Card" poster template

A greeting card template for a print product:

**Front surface elements:**

| Element | Type | Locks | Customer can... |
|---------|------|-------|----------------|
| Decorative border | Image | Position, Size, Rotation, Delete | Nothing — border frames the design |
| "Happy Birthday" text | Text | Position | Edit text, change font/color/size |
| Photo placeholder | Image | Position, Size | Replace with their own photo |
| Small stars clipart | Clipart | Delete | Move, resize, but not remove |

This template provides a professional framework while giving customers creative freedom within the safe areas.

## Template categories

Use categories to organize templates when you have more than a handful. Customers can filter templates by category in the storefront editor.

Good category structures:

**For a t-shirt store:**
- Sports
- Business
- Events
- Humor
- Seasonal

**For a print/poster store:**
- Birthday
- Wedding
- Holiday
- Motivational
- Corporate

Keep category names short and intuitive. Customers should immediately understand what kind of designs they'll find in each category.

## How templates appear to customers

On the storefront, the design editor includes a **Templates** tab in the tool panel. Customers see:

1. **Template gallery** — Thumbnail previews of all available templates, filterable by category
2. **One-click loading** — Clicking a template loads it onto the canvas instantly
3. **Full customization** — After loading, customers can modify any unlocked element
4. **Start fresh option** — Customers can always choose to start with a blank canvas instead

When a customer loads a template, all elements appear on the canvas with their lock states active. Locked elements show visual indicators (such as restricted handles) so customers understand which parts they can and cannot change.

## Tips

- Create at least 3-5 templates per product to give customers meaningful choice. A single template feels limiting; too many can be overwhelming.
- Make your best and most versatile template the first one (lowest sort order) — it sets the tone for the entire product.
- Use lock controls strategically. Lock only what truly needs to be fixed. Over-locking frustrates customers and makes them feel like they can't personalize the product.
- Test every template from the customer's perspective. Load it in the storefront editor, try to edit locked elements (verify they're truly locked), and check that unlocked elements feel natural to customize.
- Update templates seasonally. Add holiday-themed templates before major holidays and archive them afterward.
- Use meaningful template names that help customers understand the design style at a glance — "Bold Athletic" is more helpful than "Template 1".
