---
slug: customizable-product-orders
title_i18n_key: Fulfilling Customizable Product Orders
category: products
component: customizable_product
keywords:
  - design snapshot
  - fulfillment files
  - print-ready files
  - rendered images
  - order fulfillment
  - saved designs
  - design draft
  - high resolution
  - print files
  - customer designs
  - order processing
  - customizable order
url_patterns:
  - /admin/customizable_product/designsnapshot/
  - /admin/customizable_product/saveddesign/
  - /admin/orders/order/\d+/change/
related:
  - customizable-products-overview
  - manage-orders
  - customizable-product-setup
published: true
---

When a customer designs a product and places an order, their design is frozen and stored alongside the order. This guide explains how custom designs flow through the order lifecycle and how to access the print-ready files you need for fulfillment.

## Design lifecycle

A customer's design goes through several stages from creation to fulfillment:

### 1. Design creation

The customer uses the visual editor on the storefront to create their design. As they work, their progress is saved automatically in the browser. Registered customers can also save designs to their account for later editing.

### 2. Design draft

When the customer clicks **Add to Cart**, the current design state is saved as a **design draft**. The draft includes:

- The complete canvas state for every surface (element positions, text content, uploaded images, clipart, styling)
- A pricing breakdown showing all applicable design fees
- Thumbnail previews of each surface

The draft is linked to the cart item via a unique token. This ensures the exact design the customer created is preserved even if they continue shopping before checking out.

**Draft expiration:** Design drafts automatically expire after 7 days if the customer doesn't complete the order. This prevents accumulation of abandoned designs.

### 3. Design snapshot

When the customer completes checkout and the order is placed, the design draft is converted into an **immutable design snapshot**. This is the permanent record of the design:

- The snapshot cannot be modified by the customer after purchase
- It contains the exact same design data as the draft
- It is permanently linked to the specific order item

This immutability is important — it ensures that what the customer ordered is exactly what you produce and ship, with no possibility of changes after payment.

### 4. Fulfillment file rendering

After the order is placed, the system automatically generates **high-resolution fulfillment files** for each surface of the design. These are composite images that combine all design elements (text, images, clipart) into a single print-ready file at the DPI configured for each surface.

The rendering happens asynchronously in the background. For most designs, rendering completes within a few seconds. The snapshot's **Rendered** status indicates whether fulfillment files are ready.

## Accessing design data in orders

### Order detail page

When you view an order that contains customizable products in the admin panel:

1. Navigate to **Orders > All Orders**
2. Open the order containing the customized product
3. The order item for the customizable product shows the design information, including surface previews and a link to the design snapshot

### Design snapshots list

You can also browse all design snapshots directly:

1. Navigate to **Customizable Products > Design Snapshots**
2. The list shows all snapshots linked to order items
3. Click a snapshot to view the full design data, rendered images, and fulfillment files

Each snapshot shows:

| Field | Description |
|-------|-------------|
| **Order Item** | Link to the associated order item |
| **Design Data** | The complete canvas state (JSON) |
| **Rendered Images** | Per-surface preview thumbnails |
| **Fulfillment Files** | High-resolution composite files for printing |
| **Rendered** | Whether rendering is complete |
| **Render Completed At** | Timestamp of when files were generated |

## Downloading fulfillment files

The fulfillment files are what you send to your print provider or use in your production process.

**For a custom t-shirt order:**
- Download the **Front** surface file (e.g., 300 DPI composite PNG)
- Download the **Back** surface file
- Download the **Sleeve** surface file (if designed)
- Send all files to your screen printer or DTG (direct-to-garment) printer

**For a custom poster order:**
- Download the single **Front** surface file at print resolution
- The file includes bleed area if bleed was configured for the surface
- Send to your poster/card printer

Each file is a single composite image containing all design elements merged together, rendered at the DPI you configured for that surface.

## Saved designs

Registered customers can save their designs to their account for later editing. As a merchant, you can view these saved designs in a read-only list:

1. Navigate to **Customizable Products > Saved Designs**
2. The list shows all customer-saved designs with the customer name, product, design name, and date

Saved designs are:
- **Customer-owned** — They belong to the customer's account
- **Read-only for merchants** — You can view but not modify them
- **Separate from orders** — A saved design only becomes an order when the customer adds it to cart and checks out
- **Reusable** — Customers can load a saved design, modify it, and order multiple times

## Fulfillment workflow

### Standard workflow

1. **Receive order** — The order appears in your order list with the customized items
2. **Verify rendering** — Check that the design snapshot shows **Rendered: Yes**. If rendering hasn't completed yet, wait a few moments and refresh
3. **Download files** — Download the fulfillment file for each designed surface
4. **Review quality** — Open the files and verify the design meets your print quality standards (check DPI, element positioning, and text readability)
5. **Send to production** — Forward the files to your print provider or production team
6. **Ship and complete** — After production, ship the product and mark the order as fulfilled

### T-shirt fulfillment example

1. Order received: "Custom Team T-shirt" with designs on front and back
2. Open order → view design snapshot
3. Download `front.png` (300 DPI, 300x400mm) and `back.png` (300 DPI, 300x400mm)
4. Send both files to your DTG printer with the garment color and size from the order's variant selection
5. After printing and quality check, ship to customer

### Poster fulfillment example

1. Order received: "Custom A4 Poster" with a single designed surface
2. Open order → view design snapshot
3. Download `front.png` (300 DPI, 210x297mm with 3mm bleed)
4. Send to your poster printing service
5. After printing and trimming, ship to customer

## Troubleshooting

**Issue:** Design snapshot shows "Rendered: No" and rendering hasn't completed

- **Cause:** The background rendering task may have failed or is still processing
- **Solution:** Wait a few minutes. If rendering doesn't complete, check the background task logs. You can also view the design data directly in the snapshot to confirm the customer's design is preserved

**Issue:** Fulfillment file appears lower quality than expected

- **Cause:** The customer may have uploaded low-resolution images
- **Solution:** Check the surface's DPI settings. If minimum DPI warnings were configured, the customer would have been warned during the design process. For future products, consider increasing the minimum DPI requirement

**Issue:** Customer requests a change to their design after ordering

- **Solution:** Design snapshots are immutable by design. If the customer needs changes, they should place a new order with the updated design. If you agree to make an exception, the customer can use their saved design (if they saved one) as a starting point for a new order

## Tips

- Always verify that rendering is complete before starting production. Check the **Rendered** field on the design snapshot.
- Keep DPI settings appropriate for your print method. Higher DPI produces better quality but larger file sizes. 300 DPI is standard for most professional print products.
- Encourage customers to save their designs before ordering. If there's a production issue and the order needs to be remade, the saved design makes reordering straightforward.
- Build a buffer into your production timeline for customizable products. Unlike standard products, each item requires individual file handling.
- If you process high volumes of customizable orders, consider automating the file download step by integrating with your print provider's API.
