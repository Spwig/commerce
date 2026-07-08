---
slug: product-variants
title_i18n_key: Product Variants
category: products
component: catalog
keywords:
  - variants
  - variations
  - attributes
  - options
  - size
  - color
  - SKU
  - variable product
  - product options
url_patterns:
  - /admin/catalog/product/
related:
  - add-product
  - inventory-warehouses
published: true
---

Product variants let you offer a single product in multiple options — such as different sizes, colors, or materials — each with its own SKU, price, and stock level. Navigate to any **Variable Product** and click the **Variations** tab.

![Product variants](/static/core/admin/img/help/product-variants/product-variants.webp)

## Understanding Variants

A **Variable Product** is a product type that supports multiple variations. For example, a T-Shirt might come in:
- **Colors**: Blue, Red, Green
- **Sizes**: S, M, L, XL

Each combination (e.g., "Blue / Large") becomes a separate variant with its own inventory and pricing.

## Setting Up a Variable Product

### Step 1: Set the Product Type

1. Open the product edit form (or create a new product)
2. On the **Basic Info** tab, set **Product Type** to **Variable Product**
3. Save the product

### Step 2: Define Attributes

Attributes are the options that differentiate your variants (e.g., Size, Color).

1. Go to the **Variations** tab
2. In the **Product Attributes** section, click **+ Add Attribute** to assign an existing attribute, or **Create New** to define a new one
3. For each attribute, specify the available values (e.g., Small, Medium, Large)

### Step 3: Create variants

1. Scroll to the **Variants** inline section on the product form
2. Click **Add another Variant** and configure each variant:
   - **Name** — Descriptive label (e.g., "Blue / Large")
   - **SKU** — Unique stock-keeping unit code (required)
   - **Is Active** — Uncheck to hide this variant without deleting it
   - **Selected Attributes** — Choose the attribute values for this variant (e.g., Color: Blue, Size: Large)
   - **Pricing Strategy** — Choose "Inherit from Product" to use the base price, or "Custom Variant Price" to set a different price
   - **Price** — The variant-specific price (only used with "Custom Variant Price" strategy)
3. Repeat for each variant you need

## Managing Variants

### Variant Details

Each variant card shows:
- **Name** and **SKU** — Identity information
- **Price** — Current selling price
- **Stock level** — Quantity available with status indicator (In Stock / Low Stock / Out of Stock)

Click a variant card to expand and edit all its details.

### Variant-specific settings

Each variant can have its own:

| Setting | Description |
|---------|-------------|
| **Pricing Strategy** | Inherit the base product price or set a custom variant price |
| **Price** | Custom price when pricing strategy is set to "Custom Variant Price" |
| **SKU** | Unique identifier for inventory (required, must be unique) |
| **Weight** | Override the product's weight for shipping calculations (leave blank to use product weight) |
| **Length / Width / Height** | Override product dimensions for shipping (leave blank to use product dimensions) |
| **Barcode** | Variant-specific barcode for POS scanning |
| **Preferred Shipping Package** | Override the product's preferred shipping package for this variant |
| **Image** | Variant-specific product image selected from the Media Library |
| **Color Swatch** | Hex color code displayed as a swatch on color-type variants |

### Editing a Variant

1. Click the **edit icon** on the variant card
2. Modify the desired fields
3. Click **Save** to update

### Deleting a Variant

1. Click the **delete icon** on the variant card
2. Confirm the deletion

**Note:** Deleting a variant removes its inventory record. This action cannot be undone.

## Attributes

### What Are Attributes?

Attributes are reusable option definitions. Once you create an attribute like "Size" with values "S, M, L, XL", you can assign it to any variable product.

### Creating Attributes

1. On the Variations tab, click **Create New** in the Product Attributes section
2. Enter the attribute name (e.g., "Color")
3. Add values (e.g., "Red", "Blue", "Green")
4. Save the attribute

### Assigning Attributes

Attributes can be assigned to multiple products. The same "Size" attribute can be used across T-Shirts, Pants, and Shoes.

## Storefront Display

On the storefront, variable products show:
- Option selectors (dropdowns or swatches) for each attribute
- Automatic price updates when a variant is selected
- Stock availability per variant
- Variant-specific images

## Tips

- Use consistent attribute names across products for a uniform shopping experience.
- Set up all attributes before creating variants to streamline the process.
- Assign variant-specific images from the Media Library so customers can see exactly what they're ordering.
- Keep SKUs systematic (e.g., "TSHIRT-BLUE-L") for easy inventory management.
- Use the "Custom Variant Price" pricing strategy only for variants that genuinely differ in price — otherwise inherit from the base product to simplify management.
- For POS stores, set a barcode on each variant to enable scanning at the point of sale.
