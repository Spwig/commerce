---
slug: configurable-products
title_i18n_key: Configurable Products
category: products
component: catalog
keywords:
  - configurable
  - configuration
  - slots
  - options
  - compatibility
  - presets
  - build-to-order
  - custom pc
  - product configurator
url_patterns:
  - /admin/catalog/product/
  - /admin/catalog/product/\d+/change/
related:
  - add-product
  - product-variants
  - digital-products
published: true
---

Configurable products let customers build their own product by choosing options from different configuration slots. This is ideal for build-to-order items like custom PCs, personalized gift boxes, or made-to-order furniture where each component is a real product in your catalog.

![Product configurator admin](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## How It Works

A configurable product is made up of **slots** (categories of choices) and **options** (the actual products customers can pick). For example, a custom PC might have slots for Processor, Graphics Card, RAM, and Storage — each slot containing several product options to choose from.

## Pricing Strategies

Choose how the final price is calculated:

| Strategy | Description |
|----------|-------------|
| **Sum of Components** | Final price = total of all selected option prices. No base price needed. |
| **Base Price + Adjustments** | Start with the product's base price, then add/subtract price adjustments per option. |
| **Fixed Price** | One flat price regardless of which options the customer selects. |

## Setting Up a Configurable Product

### Step 1: Create the Product

1. Navigate to **Products > All Products** and click **+ Add Product**
2. Set **Product Type** to **Configurable Product**
3. Choose your **Pricing Strategy** (Sum of Components is most common)
4. Fill in the product name, description, and other basic details
5. Save the product

### Step 2: Add Configuration Slots

After saving, switch to the **Configuration** tab to set up your slots.

1. Click **+ Add Slot** to create a new configuration category
2. For each slot, configure:
   - **Name** — What the customer sees (e.g., "Processor", "Color")
   - **Icon** — Font Awesome icon class for visual identification
   - **Required** — Whether the customer must make a selection
   - **Min/Max Selections** — How many options the customer can pick (default: exactly 1)
   - **Sort Order** — Controls the order slots appear in the configurator wizard

### Step 3: Add Options to Each Slot

Each slot needs product options for customers to choose from:

1. Click **Manage Options** on a slot
2. Search for and add existing products from your catalog
3. For each option, configure:
   - **Price Adjustment** — Amount to add or subtract (used with Base + Adjustments pricing)
   - **Default** — Pre-select this option when the configurator loads
   - **Popular** — Show a "Popular" badge to help customers decide
   - **Quantity** — How many units of this component are included
   - **Compatibility Tags** — Tags used for batch compatibility rule generation

**Tip:** Component products can be hidden from the storefront by checking **Hide from Storefront** on the component product's Basic Info tab. This keeps them available as configurator options without cluttering your product catalog.

### Step 4: Define Compatibility Rules

Compatibility rules prevent customers from selecting incompatible combinations:

| Rule Type | Description |
|-----------|-------------|
| **Requires** | When option A is selected, only the listed options are available in the target slot |
| **Excludes** | When option A is selected, the listed options are hidden from the target slot |

To add rules:

1. Scroll to the **Compatibility Rules** section on the Configuration tab
2. Click **+ Add Rule**
3. Select the **source option** (the trigger)
4. Choose the **rule type** (Requires or Excludes)
5. Select the **target slot** and the **affected options**

You can also auto-generate rules from compatibility tags assigned to options, which is faster when managing many combinations.

### Step 5: Create Presets (Optional)

Presets are pre-built configurations that give customers a quick starting point:

1. Scroll to the **Configuration Presets** section
2. Click **+ Add Preset**
3. Give the preset a name and description (e.g., "Gaming Build", "Budget Starter")
4. Select the options for each slot
5. Optionally upload a preview image and mark as **Featured**

Customers can start from a preset and then customize individual slots to their preference.

## Customer Experience

When a customer views a configurable product on your storefront:

1. **Wizard Interface** — Slots are presented as steps, guiding the customer through each choice
2. **Filtering** — Incompatible options are automatically hidden based on compatibility rules
3. **Popular Badges** — Options marked as popular display a badge to aid decision-making
4. **Presets** — Featured presets appear as quick-start options
5. **Price Updates** — The total price updates in real time as options are selected
6. **Summary** — A review step shows all selected options before adding to cart

## Tips

- Start with the "Sum of Components" pricing strategy — it's the most intuitive for customers and easiest to maintain.
- Use compatibility rules to prevent invalid configurations rather than relying on customer knowledge.
- Create 2-3 presets for your most popular configurations to reduce decision fatigue.
- Hide component products from the storefront if they should only be available through the configurator.
- Test the full configuration flow on the frontend after setup to ensure all rules work as expected.
