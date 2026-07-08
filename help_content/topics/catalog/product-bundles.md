---
slug: product-bundles
title_i18n_key: Product Bundles
category: products
component: catalog
keywords:
  - bundle
  - package
  - bundle pricing
  - components
  - grouped
  - kit
  - bundle product
url_patterns:
  - /admin/catalog/product/
  - /admin/catalog/product/\d+/change/
related:
  - add-product
  - configurable-products
published: true
---

Product bundles let you sell pre-assembled packages of products at a bundled price. This is perfect for gift sets, starter kits, or any combination of products you want to offer together at a discount.

![Bundle components admin](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Pricing Strategies

Choose how the bundle price is calculated:

| Strategy | Description |
|----------|-------------|
| **Fixed Price** | Set one flat price for the entire bundle, regardless of component prices. |
| **Percentage Discount** | Automatically calculate the price as a percentage off the combined component prices. |
| **Sum of Components** | Bundle price equals the total of all component prices (useful for grouped display without a discount). |

## Creating a Bundle

### Step 1: Create the Product

1. Navigate to **Products > All Products** and click **+ Add Product**
2. Set **Product Type** to **Product Bundle**
3. Fill in the bundle name, description, and images
4. Save the product

### Step 2: Add components

After saving, scroll down to the **Bundle Items** section on the product form:

1. Click **Add another Bundle Item**
2. Search for and select a product using the **Component Product** field
3. Set the **Quantity** for each component (e.g., 2x face masks in a skincare set)
4. Set the **Sort Order** to control display order
5. Optionally check **Is Optional** (customers can exclude this item)
6. If the component is a variable product, choose either:
   - Leave **Allow Variant Selection** unchecked and pick a **fixed variant** — all customers get the same variant
   - Check **Allow Variant Selection** — customers choose their preferred variant at checkout

### Step 3: Configure pricing

In the **Bundle Pricing** section (collapsed by default under the main Pricing section):

1. Select your **Bundle Pricing Strategy**
2. For **Fixed Price** — enter the bundle price in the main **Regular Price** field above
3. For **Percentage Discount** — set the **Bundle Discount Percentage** (e.g., 15.00 for 15% off the component total)
4. For **Sum of Components** — the price is calculated automatically from component prices

## What can be bundled

| Product Type | Can Be a Component? |
|-------------|-------------------|
| Simple Product | Yes |
| Variable Product | Yes (fixed variant or customer choice) |
| Digital Product | Yes |
| Customizable Product | Yes |
| Booking Product | Yes |
| Configurable Product | No |
| Product Bundle | No (bundles cannot be nested) |
| Gift Card | No |

## Stock Management

Bundle stock is managed through its components:

- **All components must be in stock** for the bundle to be purchasable
- When a bundle is ordered, stock is deducted from each component product individually
- If any component runs out of stock, the bundle becomes unavailable
- Component stock levels are checked in real time during checkout

## Optional Components

Mark a component as **Optional** to let customers customize their bundle:

- Optional components are included by default but can be removed by the customer
- The bundle price adjusts accordingly when optional components are excluded
- At least one component must be non-optional (required)

## Customer Experience

When a customer views a bundle on your storefront:

1. **Component List** — All included products are displayed with images and quantities
2. **Bundle Savings** — The discount compared to buying items individually is shown
3. **Variant Selection** — For components with variant selection enabled, customers choose their preferred option
4. **Optional Items** — Customers can toggle optional components on or off
5. **Single Add to Cart** — The entire bundle is added as one item

## Tips

- Use the Percentage Discount strategy for the most flexible pricing — it adjusts automatically when component prices change.
- Show the savings amount prominently in your product description to encourage bundle purchases.
- Keep bundles to 3-5 components for the best customer experience. Too many items can feel overwhelming.
- Use optional components to offer a "base" and "premium" version of the same bundle.
- Regularly check that all component products are still active and in stock.
