---
slug: region-availability
title_i18n_key: Region Availability
category: products
component: catalog
keywords:
  - region availability
  - region restriction
  - sell in specific regions
  - product region visibility
  - restrict products by country
  - sales region
  - ship-to selector
  - region selector
  - does not ship to
  - hide from listings
  - region detection
  - allowlist blocklist
  - shipping countries
  - region switcher
  - geographic availability
url_patterns:
  - /admin/catalog/product/
  - /admin/catalog/stockdisplaysettings/
  - /admin/catalog/salesregion/
  - /admin/catalog/productregionvisibility/
  - /admin/shipping/shippingcountry/
related:
  - sales-regions
  - add-product
  - multi-currency-setup
  - setup-shipping
  - geoip-setup
published: true
---

Region availability controls which of your Sales Regions a product can be sold in, and how shoppers outside those regions experience your catalog. Use it when a product is licensed for certain countries only, when stock is reserved for a local market, or when you're rolling a new product out region by region.

This builds on **Sales Regions**, which group countries into named markets (see the Sales Regions guide for setting those up). Once your regions exist, you can restrict individual products to them and decide how restricted products appear to shoppers who can't buy them.

## Restricting a product to specific regions

Every product has a **Region availability** setting on its edit page. Open **Products > All Products**, select a product, and find it in the **Status** section alongside **Status**, **Featured**, and **Hide from Storefront**.

![The product edit form's Status section, with the Region availability dropdown set to "Only in selected regions" alongside Featured and Hide from Storefront](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Option | What it means |
|--------|---------------|
| **Available in all regions** | No restriction. The product is sold everywhere. This is the default for every product. |
| **Only in selected regions** | An allowlist. The product is sold only in the regions you select below — everywhere else, it's treated as not available. |
| **All regions except selected** | A blocklist. The product is sold everywhere *except* the regions you select below. |

### Choosing the regions

Below the Status section, a table titled **Region availability (selected regions)** lists the regions the mode above applies to.

1. Set **Region availability** to **Only in selected regions** or **All regions except selected**.
2. In the **Region availability (selected regions)** table, click **Add another Region** and choose a Sales Region.
3. Repeat for each region you want to add.
4. Click **Save**.

![The "Region availability (selected regions)" inline table with North America and Europe rows added](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

If **Region availability** is set to **Available in all regions**, anything in this table is ignored — clear the mode dropdown first if you want to remove a restriction without deleting the rows.

For a catalog-wide view of every product's region rules in one list (handy when auditing many products at once), go to **Product Region Visibility** at `/admin/catalog/productregionvisibility/`.

## Showing shoppers where a product doesn't ship

When a shopper's region doesn't match a product's availability rules, you control what they see in **Stock Display Settings**, under the **Region Availability** section. This page doesn't have a sidebar shortcut yet — open it directly at `/admin/catalog/stockdisplaysettings/`.

![Stock Display Settings, Region Availability section — the Region-restricted display dropdown, set to "Show, marked as unavailable"](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Option | What shoppers see |
|--------|-------------------|
| **Show, marked as unavailable** (default) | The product still appears in listings, with an "Unavailable" badge and a "Does not ship to [region]" notice in place of the Add to Cart button. A banner also appears at the top of listing pages ("Some products don't ship to [destination]") with a link to filter down to only the items that do ship there. |
| **Hide from listings** | The product is removed from listing and search results entirely for shoppers in that region. |

![Storefront product listing shipping to Europe — the "Some products don't ship to Europe" banner above the grid, and a product card marked "Unavailable" with a "Does not ship to Europe" notice](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

A restricted product's own page always shows a "This product doesn't ship to [region]" notice when a shopper reaches it directly (for example, from a shared link or search engine result) — this applies regardless of which listing option you choose above, since a direct link bypasses the listing entirely.

## Letting shoppers pick or discover their region

Spwig can detect a shopper's region automatically and offer a switch, and you can add a selector so shoppers can change it themselves at any time.

### Before you begin

You need two things configured for region detection and switching to work correctly:

1. **Sales Regions** — the countries in each region and each region's default currency. If you don't see **Sales Regions** under **Inventory** in the sidebar, turn on **Enable Multi-Warehouse** under **Settings > Store Settings > E-Commerce** to reveal the menu link (you don't need to actually use multiple warehouses — this setting only unlocks the menu item). You can also go straight to `/admin/catalog/salesregion/`.
2. **Shipping Countries** — the countries your store actually ships to. These are usually already in place: every country you add to a Shipping Zone is automatically added here too. To review or manually adjust the list, open `/admin/shipping/shippingcountry/` directly (it also doesn't have a sidebar link yet).

### The automatic region confirmation

Spwig detects a shopper's region from their location and applies it automatically. When that puts them in a region *other than* your store's default (primary) market — and you have two or more active Sales Regions — Spwig shows a confirmation on their first visit so they know which region they're in and can change it:

> **We've set your region to [Region]**
> We picked this from your location so you see the right products and prices. Not right? Choose your country.
> Ship to: [country picker]  **[Keep browsing]**

![The "We've set your region to North America" confirmation modal on the storefront, with a "Ship to" country picker and a Keep browsing button](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Choosing a different country in the picker switches them immediately. Dismissing it or clicking **Keep browsing** keeps their current region, and they won't be asked again on that browser. Visitors who are already in your default region aren't shown the confirmation at all.

### Adding a Ship-To Selector to your header or footer

If you'd rather let shoppers change region themselves at any time (instead of relying only on the automatic prompt), add the **Ship-To Selector** widget to your header or footer.

1. Navigate to **Design > Header Builder** (or **Footer Builder**).
2. Drag the **Ship-To Selector** widget from the Widget Library into a row.
3. Click **Save**.

![The Header Builder widget library with the Shop group highlighted, showing the Ship-To Selector widget alongside Shopping Cart, Account Menu and Language Selector](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

The widget needs no setup — it lists your active Shipping Countries automatically, and shows a shopper's current selection (or their GeoIP-detected country, if they haven't chosen one yet). Picking a different country updates their region immediately and reloads the page's product availability and pricing.

The Ship-To Selector doesn't have a dedicated settings form yet. If you want to change its button style (outline, solid, or ghost) or hide the "Ship to" label, open the widget's settings in the builder and edit the **Custom Configuration (JSON)** field directly, using `button_style` and `show_label`.

### Currency follows region

If your store supports more than one currency (set under **Settings > Multi-Currency**), switching region — whether through the prompt or the Ship-To Selector — also switches the displayed currency to that region's default currency. If your store only has one currency, or hasn't explicitly enabled a second one, currency is left alone when a shopper changes region.

## Tips

- Leave **Region availability** at **Available in all regions** unless you have a specific reason to restrict a product — it's the simplest option and needs no upkeep as you add regions later.
- Use **Only in selected regions** for a small allowlist (e.g. a product launching in one country first) and **All regions except selected** for a small blocklist (e.g. everywhere except a country where the item isn't licensed) — pick whichever needs fewer rows to set up.
- If shoppers report a product is missing that should be visible, check both the product's **Region availability** setting and whether their country is covered by an active **Sales Region** and an active **Shipping Country**.
- **Hide from listings** keeps your catalog looking clean for shoppers who can't buy certain items, but it also means merchandising and search will look thinner in those regions — **Show, marked as unavailable** is usually better if you still want shoppers to browse your full catalog even where they can't check out.
- Test region behavior by adding the Ship-To Selector to your header and switching between countries yourself before relying on GeoIP detection during a launch.
- Set your regions' priority values (on the Sales Regions page) deliberately — the highest-priority active region is the fallback for shoppers whose country can't be detected or doesn't match any region.
