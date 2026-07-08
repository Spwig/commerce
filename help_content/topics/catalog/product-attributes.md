---
slug: product-attributes
title_i18n_key: Product Attributes
category: products
component: catalog
keywords:
  - product attributes
  - attribute values
  - size attribute
  - color attribute
  - product variants
  - variation options
  - color swatch
  - button group
  - dropdown select
  - attribute types
  - variant options
  - product options
  - size chart
  - material options
related:
  - product-variants
  - add-product
  - configurable-products
url_patterns:
  - /admin/catalog/productattribute/
  - /admin/catalog/attributevalue/
published: true
---

Product attributes define the dimensions along which a product can vary — for example, Size, Colour, or Material. Once you have created an attribute and its possible values, you can assign it to any variable product and Spwig will generate the variation selector that customers use at checkout.

Navigate to **Catalog > Product Attributes** to manage attributes and their values.

## How attributes work

Attributes are reusable across your entire catalogue. You create them once and assign them to as many products as needed. Each attribute has:

- A **name** that identifies it (e.g., "Size")
- A **display type** that controls how the selector appears on the product page
- One or more **values** that represent the available options (e.g., "Small", "Medium", "Large")

When you assign an attribute to a product, you also specify which of its values are available for that particular product. This means a "Size" attribute might have values S through 3XL, but a specific t-shirt might only offer S, M, and L.

## Attribute display types

The **Type** field on an attribute controls how the selection widget appears on your storefront product page:

| Type | Appearance | Best for |
|---|---|---|
| **Dropdown Select** | A dropdown menu the customer opens to choose a value | Attributes with many values (e.g., a size range with 10+ sizes) |
| **Color Swatch** | Coloured circles or squares the customer clicks | Colour attributes where visual identification helps |
| **Button Group** | Pill-shaped buttons displayed inline | Attributes with a small number of values (e.g., S, M, L, XL) |
| **Radio Buttons** | Traditional radio button list | Any attribute where you want a clear, accessible list layout |

Choose the display type that matches how your customers think about the attribute. For colour, swatches are almost always better than a dropdown. For size, button groups work well when there are fewer than 8 options.

## Creating an attribute

1. Navigate to **Catalog > Product Attributes**
2. Click **+ Add Product Attribute**
3. Enter the **Name** (e.g., `Size`, `Colour`, `Material`)
4. The **Slug** is filled automatically — you can leave it as-is
5. Select the **Type** (Dropdown, Color Swatch, Button Group, or Radio Buttons)
6. Check **Is Required** if customers must select this attribute before they can add the product to their cart — this is appropriate for most sizing and colour attributes
7. Set a **Sort Order** — attributes with lower numbers appear first in the variation selector on the product page
8. Add attribute values directly in the **Values** section (see below)
9. Click **Save**

## Adding attribute values

Attribute values are the individual options within an attribute. You can add them directly while creating or editing an attribute, using the inline values form at the bottom of the attribute detail page.

For each value:

- **Value** — the display label (e.g., `Small`, `Red`, `Cotton`)
- **Slug** — auto-filled from the value; used in URLs and variant identifiers
- **Color Hex** — only relevant for **Color Swatch** type attributes. Enter a hex colour code (e.g., `#FF0000` for red) so the swatch shows the correct colour.
- **Sort Order** — controls the order values appear in the selector. Assign lower numbers to values you want to appear first.

### Ordering values logically

For size attributes, set the sort order so sizes run small to large:

| Value | Sort Order |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

For colour attributes, you might sort alphabetically or group similar colours together — whatever makes the most sense for your customers.

## Managing attribute values separately

You can also manage attribute values independently at **Catalog > Attribute Values**. This list is useful when you need to find or update a specific value across your catalogue without opening each attribute individually. The list is filterable by attribute name.

## Assigning attributes to products

Attributes are assigned at the product level, not globally. To add an attribute to a product:

1. Navigate to **Catalog > Products** and open a variable product
2. In the **Variations** tab, find the **Attributes** section
3. Select the attribute you want to add
4. Choose which of the attribute's values are available for this product
5. Save the product — Spwig will generate the corresponding variant combinations

For detailed guidance on setting up product variants, see the **Product Variants** help topic.

## Practical examples

### Example: Clothing size attribute

| Field | Value |
|---|---|
| Name | Size |
| Type | Button Group |
| Is Required | Yes |
| Sort Order | 1 |
| Values | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Example: Colour swatch attribute

| Field | Value |
|---|---|
| Name | Colour |
| Type | Color Swatch |
| Is Required | Yes |
| Sort Order | 2 |
| Values | Black (#000000), White (#FFFFFF), Navy (#001F5B), Red (#CC0000) |

### Example: Material attribute

| Field | Value |
|---|---|
| Name | Material |
| Type | Dropdown Select |
| Is Required | No |
| Sort Order | 3 |
| Values | 100% Cotton, Cotton/Polyester Blend, Merino Wool, Linen |

## Tips

- Create attributes that represent genuine purchasing decisions customers make — if customers don't need to choose it, it may not need to be an attribute
- Use consistent naming across your catalogue: if some products use "Colour" and others use "Color", customers and your team will find the inconsistency confusing
- The sort order on both attributes and values matters — put the most important attribute first (usually Size or Colour) and order values in a logical sequence
- Color Swatch type requires accurate hex codes; test the colours in a browser colour picker before saving to ensure the swatch matches the actual product colour
- If you need to rename an attribute (e.g., from "Color" to "Colour"), update the **Name** field rather than creating a new attribute — changing the name does not affect existing product assignments
