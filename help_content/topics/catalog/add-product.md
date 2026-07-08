---
slug: add-product
title_i18n_key: Adding a Product
category: products
component: catalog
keywords:
  - product
  - add product
  - create product
  - new product
  - catalog
  - SKU
  - pricing
  - inventory
  - media
  - images
  - SEO
url_patterns:
  - /admin/catalog/product/
  - /admin/catalog/product/add/
  - /admin/catalog/product/\d+/change/
related:
  - custom-fields
published: true
---

This guide walks you through creating a new product in your store. The product form is organized into sections covering basic info, media, pricing, inventory, SEO, and more — so you can fill in everything in one go or come back to complete sections later.

## Getting started

From the sidebar, navigate to **Products > All Products** to see your product catalog. Click the **+ Add Product** button in the top-right corner to open the product creation form.

![Product list page](/static/core/admin/img/help/add-product/product-list-page.webp)

## Basic information

The **Basic Information** section is where you define your product's core identity.

![Add product form](/static/core/admin/img/help/add-product/add-product-form.webp)

### Required fields

- **Name** — The product name shown to customers. Click the globe icon to add translations for other languages.
- **Slug** — URL-friendly version of the name (auto-generated). Customize it if needed.
- **SKU** — Your internal stock keeping unit code.
- **Product Type** — Choose from: Simple, Variable, Digital, Bundle, Gift Card, Customizable, Configurable, or Booking.
- **Category** — Assign the product to a category for organization and storefront navigation.

### Status and visibility

Found in the **Status** section at the bottom of the form:

- **Status** — Set to **Draft** while working, **Published** when ready to sell, or **Discontinued** for products you no longer offer.
- **Is Featured** — Check to highlight this product on your storefront.
- **Is Digital Product** — Check if this product includes digital downloads (files, licenses). Can be combined with any product type.
- **Hide from Storefront** — Hides the product from catalog listings while keeping it available as a configurator option or bundle component.

### Optional fields

- **Brand** — Associate with a brand if applicable.
- **Tags** — Assign tags for lightweight product organization and filtering.

### Product descriptions

- **Short Description** — Appears in product listings and cards. Keep it brief and compelling.
- **Full Description** — Detailed product description shown on the product detail page. Use the rich text editor to add formatting, images, videos, and tables.

Both description fields support the translation feature — click the globe icon to provide content in other languages.

### Features and specifications

The **Product Details** section contains two structured data fields:

- **Features** — Key-value pairs for product highlights (e.g., "Battery Life: 20 hours").
- **Specifications** — Technical details for the specifications tab on the product page (e.g., "Processor: Intel i7").

## Media

The **Media** section lets you manage product images using the integrated Media Library.

![Media tab](/static/core/admin/img/help/add-product/media-tab.webp)

1. Click **+ Add Images from Media Library** to open the media picker.
2. Select existing images or upload new ones directly.
3. Drag images to reorder them — the **first image** becomes the primary product image shown in listings and cards.

The **Gallery Type** is configured under **Product Page Design** (see below).

## Pricing

Set your product's pricing and configure sales.

![Pricing tab](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Regular pricing

- **Regular Price** — The standard retail price customers will see. The currency is set alongside the price amount.
- **Cost** — Your cost of goods, used for profit calculations. This is never shown to customers.

### Sale settings

Configure temporary discounts:

- **Sale Type** — Choose from: No Sale, Fixed Sale Price, Amount Off, or Percentage Off.
- **Sale Value** — The discount amount or percentage.
- **Sale Start Date / Sale End Date** — Schedule when the sale activates and expires. Leave empty for an immediate start or no end date.

### Multi-currency pricing

If multi-currency is enabled on your store, a **Pricing Strategy** field appears:

- **Dynamic Pricing** — Prices in other currencies are automatically calculated using your configured exchange rates.
- **Fixed Pricing** — Set a specific price for each currency independently using the **Multi-Currency Pricing** section that appears below.

## Inventory

Manage stock levels and physical product attributes.

![Inventory tab](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Stock management

- **Track Inventory** — Enable to track stock quantities (enabled by default).
- **Low Stock Threshold** — Get alerts when stock drops below this number (default: 5).
- **Allow Backorders** — Enable to accept orders even when out of stock.
- **Out of Stock Action** — Override the site-wide or category behavior when this product runs out: hide it, show it as unavailable, show a "Notify Me" button, or allow backorders.

Stock quantities are managed per warehouse. After saving the product, use the **Stock Items** section at the bottom of the form (or navigate to **Products > Stock Items**) to set quantities at each warehouse location.

### Pre-order

For products that are not yet available, expand the **Pre-Order** section:

- **Is Pre-order** — Enable pre-order purchasing even when out of stock.
- **Pre-order Release Date** — Expected availability date shown to customers.
- **Pre-order Message** — Custom message (e.g., "Ships March 2026").

### Physical attributes

Enter the product's weight (kg) and dimensions (length, width, height in cm) for accurate shipping calculations. You can also select a **Preferred Shipping Package** to use specific box dimensions when calculating shipping rates.

### Product identifiers

Standard product codes for marketplace listings and inventory systems:

- **GTIN** — Global Trade Item Number
- **EAN** — European Article Number
- **UPC** — Universal Product Code (US)
- **ISBN** — For books
- **ASIN** — Amazon identifier
- **MPN** — Manufacturer Part Number

### International shipping / customs

Required for international shipments (expand the **International Shipping / Customs** section):

- **HS Code** — Harmonized System classification code
- **Country of Origin** — Where the product is manufactured
- **Customs Unit Price** — Declared value per unit for customs
- **Export License Number** — Required only for controlled or restricted items
- **Export License Expiry** — Expiration date of the export license

## SEO

Optimize your product's search engine visibility.

![SEO tab](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta Title** — The title shown in search engine results. Click the globe icon to translate.
- **Meta Description** — A brief description for search results (max 160 characters). Click the globe icon to translate.
- **Auto-generate SEO** — Check to automatically generate SEO content when the product is saved.

A live **Search Result Preview** shows exactly how your product will appear in Google search results.

## Product page design

The **Product Page Design** section lets you control how the product's storefront page looks:

- **Page Template** — Choose a layout template (Classic, Full Width, Gallery Focus, Digital) or leave empty to use the site default.
- **Gallery Type** — How product images display: Standard Gallery, Carousel, Grid Layout, Zoom Gallery, or 360° View.
- **Show Related Products** — Display related products at the bottom of the page.
- **Show Reviews** — Display customer reviews.
- **Show Specifications** — Display the specifications tab.

## Sales channel

The **Sales Channel** field (in the Status section) controls where the product can be sold:

- **All Channels** — Available online and in-store (POS).
- **Online Only** — Not available through POS terminals.
- **In-Store Only** — Not listed online; only available at your physical store.

A **Barcode** field is also available for POS barcode scanning.

## Saving your product

When you're ready, use the save buttons in the top-right corner. Your product will be visible on the storefront once its status is set to **Published**.

## Tips

- Start with **Draft** status so you can perfect the product before customers see it.
- Upload multiple images — products with several photos convert better.
- Fill in the **SEO** fields to improve discoverability in search engines.
- Use **Categories**, **Brands**, and **Tags** to help customers navigate your catalog.
- For variable products (e.g., different sizes or colors), choose the **Variable Product** type and add variants after saving.
- Use **Features** and **Specifications** to add structured product data that displays in dedicated tabs on the product page.
