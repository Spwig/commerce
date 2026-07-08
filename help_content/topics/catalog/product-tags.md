---
slug: product-tags
title_i18n_key: Product Tags
category: products
component: catalog
keywords:
  - product tag
  - tag
  - label
  - filter
  - organize products
  - product organization
  - tagging
  - product search
  - product filtering
  - catalog organization
url_patterns:
  - /admin/catalog/producttag/
  - /admin/catalog/product/
related:
  - add-product
  - promotion-examples
  - product-variants
published: true
---

Product tags are short, free-form labels you can attach to products for flexible organisation and filtering. Tags are lightweight compared to categories — they do not have a hierarchy or dedicated pages, but they are fast to create and easy to apply to many products at once.

Common uses for tags:
- Grouping products by theme (`summer`, `gift-idea`, `clearance`)
- Marking products for internal purposes (`staff-pick`, `new-arrival`, `bundle-candidate`)
- Creating filterable collections in promotions and campaigns
- Quickly finding related products across different categories

## Creating a tag

Tags are created automatically when you add them to a product, but you can also manage them directly:

1. Navigate to **Catalog > Product Tags**
2. Click **+ Add Product Tag**
3. Enter the tag **Name** (e.g., `New Arrival`)
4. The **Slug** is generated automatically from the name (`new-arrival`) — you can edit it if needed
5. Click **Save**

Tag slugs must be unique. The slug is used internally and in URLs when tags are used for storefront filtering.

## Adding tags to a product

1. Navigate to **Products > All Products**
2. Open the product you want to tag
3. Find the **Tags** field on the product edit form
4. Type to search for an existing tag or type a new tag name to create one on the fly
5. Select or create as many tags as needed
6. Save the product

## Managing existing tags

### Viewing all tags

The tag list at **Catalog > Product Tags** shows all tags in alphabetical order. Click any tag to edit its name or slug.

### Renaming a tag

1. Navigate to **Catalog > Product Tags**
2. Click the tag you want to rename
3. Update the **Name** field
4. The slug does not update automatically when you rename — update it manually if needed to keep it consistent
5. Click **Save**

Note: renaming a tag updates it everywhere it is used, since products reference the same tag object.

### Deleting a tag

1. Navigate to **Catalog > Product Tags**
2. Check the box next to the tag(s) you want to delete
3. Select **Delete selected product tags** from the **Action** dropdown
4. Confirm the deletion

Deleting a tag removes it from all products it was assigned to. Products are not deleted — only the tag label is removed.

## Tips

- Keep tag names short and consistent — use lowercase or Title Case and pick one convention and stick with it across your catalogue.
- Avoid duplicating category logic in tags. Tags work best for cross-cutting concerns (like `new-arrival` or `staff-pick`) that do not fit neatly into your category structure.
- Use a `clearance` or `sale` tag to mark products for time-limited promotions — it makes it easy to find and update those products later.
- Tags are not visible to customers by default. Their primary purpose is to help you organise and filter products in the admin.
- If you find yourself creating many tags that overlap with your categories, it may be worth reviewing your category structure instead.
