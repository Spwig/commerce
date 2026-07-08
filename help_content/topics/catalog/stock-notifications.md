---
slug: stock-notifications
title_i18n_key: Stock Notifications
category: products
component: catalog
keywords:
  - stock notification
  - back in stock
  - notify me
  - out of stock
  - low stock
  - stock alert
  - stock display
  - backorder
  - stock status
  - inventory alert
  - restock notification
  - stock settings
url_patterns:
  - /admin/catalog/stockdisplaysettings/
  - /admin/catalog/stocknotification/
related:
  - inventory-warehouses
  - add-product
published: true
---

Stock notifications let customers sign up to be emailed when an out-of-stock product becomes available again. Stock display settings control what customers see on product pages — such as stock status labels, low stock warnings, and what happens when a product runs out.

## Stock display settings

Stock display settings are store-wide defaults that apply to all products unless overridden at the category or product level.

Navigate to **Catalog > Stock Display Settings** to configure these options. There is one settings record for your store — click it to edit.

### Stock status display

| Setting | Description |
|---------|-------------|
| **Show Stock Status** | Display "In Stock" or "Out of Stock" labels on product pages |
| **Show Low Stock Warning** | Show a "Only X left" message when stock is running low |
| **Low Stock Threshold** | The quantity at or below which the low stock warning appears (default: 5) |
| **Show Exact Quantity** | Show the precise number remaining (e.g., "Only 3 left!") instead of a generic warning |

### Out-of-stock behaviour

The **Out of Stock Action** setting determines what customers see when a product has no stock available:

| Action | What customers see |
|--------|-------------------|
| **Hide from listings** | The product is removed from category pages and search results |
| **Show as unavailable** | Product is visible but cannot be added to cart |
| **Show "Notify Me" button** | Customers can register their email to be notified when stock returns |
| **Allow backorders** | Customers can purchase the product even when stock is zero |

Set **Out of Stock Message** to customise the text shown when a product is unavailable (default: `Out of Stock`).

Set **Backorder Message** to customise the text shown for backorderable products (default: `Available on backorder`).

### Shipping and delivery display

| Setting | Description |
|---------|-------------|
| **Show "Ships From" location** | Display the warehouse name on the product page |
| **Show Estimated Delivery** | Display estimated delivery dates calculated from warehouse location |

### Allow backorders (site-wide)

Check **Allow Backorders** to allow customers to purchase any out-of-stock product by default. Individual products and categories can override this setting.

## Back-in-stock notifications

When you set the out-of-stock action to **Show "Notify Me" button**, customers can enter their email address on the product page to receive an email when the product is restocked.

### Viewing notification requests

Navigate to **Catalog > Stock Notifications** to see all customer notification requests. Each record shows:
- Customer email address
- Product and variant (if applicable)
- Preferred warehouse (if the customer selected a regional preference)
- When the request was created
- When the notification was sent (blank if not yet sent)

### When notifications are sent

Spwig sends back-in-stock emails automatically when a product's stock level rises above zero. The **Notified At** field records when the email was sent.

Customers receive one notification email. Once notified, they need to sign up again if the product goes out of stock a second time.

### Filtering notification requests

Use the admin filters to find:
- Requests for a specific product
- Requests that have already been notified (to see who has been contacted)
- Requests that are still pending (customers waiting for a restock)

## Product-level overrides

The site-wide stock display settings can be overridden per product or category. On the product edit form, look for the **Stock** section where you can set a product-specific **Out of Stock Action** that differs from the global default.

This is useful when you want most products to allow backorders but keep a few products set to "Notify Me" — or when a specific product should be hidden when out of stock.

## Tips

- Set **Low Stock Threshold** to the reorder point you typically use, so customers are warned about limited availability before you run out entirely.
- Use the **Show "Notify Me" button** option instead of hiding out-of-stock products — customers who sign up represent real demand that can justify a restock order.
- Enable **Show Exact Quantity** sparingly. For most stores, showing "Only 3 left!" works better than showing the exact number, as it creates urgency without revealing your full inventory picture.
- Check the stock notifications list before placing a new order — the number of pending notification requests tells you how much demand exists for that product.
- If you use backorders, update your **Backorder Message** to set accurate expectations (e.g., "Ships in 2-3 weeks — order now to reserve your place").
- Combine out-of-stock notifications with email marketing: when you restock a popular product, send a campaign to everyone who signed up, not just the automatic notification email.
