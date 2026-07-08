---
slug: product-brands
title_i18n_key: Product Brands
category: products
component: catalog
keywords:
  - product brands
  - brand page
  - brand management
  - brand logo
  - brand SEO
  - filter by brand
  - brand story
  - manufacturer
  - brand listing
  - featured brand
  - brand banner
  - brand website
related:
  - add-product
  - product-collections
  - manage-categories
  - sales-promotions
url_patterns:
  - /admin/catalog/brand/
published: true
---

Brands let you associate products with their manufacturer or label and give customers a way to browse your store by brand. Each brand gets its own page on your storefront where customers can discover all products from that brand, read the brand story, and follow a link to the brand's website.

Navigate to **Catalog > Brands** to manage your brands.

## Why use brands

Brands serve two purposes in Spwig:

1. **Organisation** — products are tagged with a brand, making it easy for customers who are loyal to a particular label to find what they are looking for
2. **Merchandising** — brand pages are a dedicated space to showcase the brand's story, logo, and full product range, which can improve conversion for brand-conscious shoppers

Brands also work with the promotions system — you can run a sale that applies to all products from a specific brand without having to select products individually.

## Creating a brand

1. Navigate to **Catalog > Brands**
2. Click **+ Add Brand**
3. Fill in the **Basic Information** section:
   - **Name** — the brand name as it will appear on your storefront (must be unique)
   - **Slug** — the URL path for the brand page (auto-filled from the name; you can customise it)
   - **Description** — a short description of the brand shown on the brand page
   - **Website** — the brand's official website URL (optional — shown as a link on the brand page)
4. Add brand assets:
   - **Logo** — the brand's logo image, used in brand listings and on the brand page
   - **Banner Image** — a wide banner image displayed at the top of the brand page
5. Write the **Brand Story** (optional) — a longer editorial piece about the brand's history, values, or what makes it special. This appears on the brand's storefront page and can be an effective way to tell a brand's story to interested customers.
6. Configure **SEO** fields:
   - **Meta Title** — the page title shown in search engine results
   - **Meta Description** — the short description shown below the title in search results
7. Set display options:
   - **Show Brand Page** — controls whether the brand has a publicly accessible page. Uncheck to hide a brand from the storefront while keeping it in the system.
   - **Is Active** — controls whether the brand is available to assign to products and visible in the store
   - **Is Featured** — marks the brand for featured placement in your theme (e.g., a homepage row of brand logos)
8. Click **Save**

## Assigning products to a brand

Brands are assigned on individual product records, not from the brand management page. To assign a brand to a product:

1. Navigate to **Catalog > Products** and open the product
2. In the product form, find the **Brand** field
3. Search for and select the appropriate brand
4. Save the product

Once a brand is assigned, the product will appear on that brand's storefront page automatically.

## Brand pages on your storefront

Each brand with **Show Brand Page** enabled gets its own page at `/brand/{slug}/`. The page displays:

- The brand logo and banner image
- The brand name and description
- The brand story (if provided)
- A link to the brand's website (if provided)
- All active products assigned to that brand

Customers can reach brand pages by clicking a brand name on a product page, or through links you create in your navigation or page builder.

## SEO for brand pages

Filling in the **Meta Title** and **Meta Description** fields for each brand helps your brand pages appear well in search results. Effective brand SEO titles typically combine the brand name with what the brand sells:

| Brand | Good Meta Title |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

If you leave the SEO fields blank, your theme will fall back to the brand name.

### Automatic SEO generation

If **SEO Auto Generated** is enabled on a brand, Spwig will automatically generate meta title and description content when the brand is saved. This is convenient for stores with many brands but gives you less control over the exact wording. You can always override the generated content by typing in the fields directly and disabling the auto-generation toggle.

## Featured brands

The **Is Featured** flag is used by themes to display a curated row or grid of brand logos — commonly on the homepage. Only a small number of brands should be featured at a time; consult your theme documentation to understand how many featured brands display optimally.

## Tips

- Upload a brand logo as a PNG or WebP with a transparent background — it will display cleanly on any background colour in your theme
- Write a compelling brand story even for lesser-known brands; customers who are unfamiliar with a brand appreciate context that helps them decide whether the products are right for them
- If you run promotions targeting specific brands, make sure the brand name in Spwig matches exactly — promotions use the brand relationship on products to determine eligibility
- Deactivate a brand rather than deleting it when you stop carrying its products — deletion removes the brand reference from all associated products, whereas deactivation preserves the history
- Use the **Is Featured** flag sparingly; a homepage showing 20 brand logos loses impact compared to 6–8 carefully chosen ones
