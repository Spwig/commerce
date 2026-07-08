---
slug: inventory-warehouses
title_i18n_key: Inventory & Warehouses
category: products
component: catalog
keywords:
  - inventory
  - stock
  - warehouse
  - warehouses
  - stock levels
  - fulfillment
  - stock management
  - low stock
  - out of stock
url_patterns:
  - /admin/catalog/warehouse/
  - /admin/catalog/stockitem/
related:
  - add-product
  - product-variants
  - manage-orders
published: true
---

The warehouse system lets you manage inventory across multiple locations, set fulfillment priorities, and track stock levels in real time. Navigate to **Products > Warehouses** in the admin sidebar to manage your warehouse locations.

![Warehouse list](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Warehouses

### Warehouse List

The warehouse page shows all your inventory locations as cards with:

- **Name and code** — Warehouse identifier (e.g., "Main Warehouse", code "MAIN-WH")
- **Sales region** — Geographic region assignment
- **Status badges** — Active/inactive, retail location
- **Statistics** — Products stocked, fulfillment priority, stock buffer percentage
- **Location** — City and country
- **Last updated** — When stock levels were last modified

### Creating a warehouse

1. Click **+ Add Warehouse**
2. Fill in the **Basic Information**:
   - **Name** — Descriptive label (e.g., "US East Warehouse")
   - **Code** — Short unique identifier (e.g., "US-EAST") — must be unique across all warehouses
   - **Sales Region** — Assign to a geographic region for fulfillment routing
   - **Active** — Enable to include in fulfillment
3. Fill in the **Address** section with the full warehouse address
4. Configure **Fulfillment Settings**:
   - **Fulfillment Priority** — Higher numbers = higher priority for order fulfillment
   - **Stock Buffer Percentage** — Percentage of stock to reserve as a safety buffer (0–100)
   - **Shipping Location** — Optionally link to a pickup location if this warehouse supports customer pickup
5. Configure **Customer Display** (optional):
   - **Display Name** — Customer-facing label (e.g., "Ships from Australia"). Leave blank to use the warehouse name.
   - **Show on Frontend** — Display this warehouse's origin to customers on product pages
6. Configure **POS / Retail Store** (optional):
   - **Retail Location** — Check if this warehouse also serves as a physical store with POS terminals
   - **POS Display Name** — Short name shown in the POS interface
   - **Store Group** — Assign to a POS store group for settings inheritance
7. Add **Contact Information** if needed (name, email, phone)
8. Click **Save**

### Fulfillment Priority

When an order comes in, the system selects the best warehouse based on:

1. **Priority value** — Higher priority warehouses are preferred
2. **Stock availability** — Must have sufficient stock
3. **Region matching** — Warehouses in the customer's region are preferred

For example, if you have a US warehouse (priority 100) and a EU warehouse (priority 60), US orders will fulfill from the US warehouse first.

### Stock Buffer

The stock buffer reserves a percentage of inventory that won't be sold online. This is useful for:
- Physical retail stores that need floor stock
- Safety stock to prevent overselling
- Reserved inventory for wholesale orders

A 10% buffer on 100 units means only 90 units are available for online orders.

## Stock Items

Stock items represent the actual inventory of a specific product at a specific warehouse.

### Viewing Stock Levels

1. Click the **stock icon** on any warehouse card to see its stock items
2. Or navigate to a product's **Inventory** tab to see stock across all warehouses

Each stock item shows:
- **Product name** and variant (if applicable)
- **On hand** — Total physical inventory
- **Allocated** — Quantity reserved for pending orders
- **Available** — On hand minus allocated (what can be sold)

### Adding stock

1. Navigate to **Products > Stock Items** and click **+ Add Stock Item**, or
2. Open a product's edit form and use the **Stock Items** inline section at the bottom
3. Select the **product** and **warehouse** (and optionally a **variant** for variable products)
4. Enter the **on hand** quantity
5. Set the **low stock threshold** — this per-item threshold triggers a low stock alert
6. Save

### Stock Movements

Every change to inventory is tracked as a **stock movement**:

| Movement Type | Description |
|--------------|-------------|
| **Receipt** | New stock received from supplier |
| **Sale** | Stock deducted for a fulfilled order |
| **Return** | Stock returned from a customer |
| **Adjustment** | Manual correction (count discrepancy) |
| **Transfer** | Moved between warehouses |
| **Reservation** | Temporarily held for an active cart |

Stock movements provide a complete audit trail of inventory changes.

## Inventory Tracking on Products

### Enabling inventory tracking

On a product's **Inventory** section:

1. Toggle **Track Inventory** to enable stock management for this product
2. Set the **Low Stock Threshold** — triggers dashboard alerts when stock at any warehouse falls below this level
3. Configure **Allow Backorders** if you want to accept orders when out of stock
4. Optionally set an **Out of Stock Action** to override the site-wide or category behavior for this specific product

After enabling tracking, manage actual stock quantities using the **Stock Items** inline section at the bottom of the product form, or through **Products > Stock Items**.

### Multi-Warehouse Stock

When inventory tracking is enabled, the Inventory tab shows stock levels across all warehouses in a summary table:

- Total on hand across all locations
- Per-warehouse breakdown
- Available quantities after reservations and allocations

## Low Stock Alerts

The system automatically monitors stock levels and alerts you when:
- A product falls below its **low stock threshold**
- A product reaches **zero available stock**

Low stock alerts appear on:
- The **Shop Dashboard** in the Actions Required section
- The product list with a visual indicator

## Tips

- Start with a single warehouse and add more as your business grows.
- Set fulfillment priorities based on shipping speed and cost to each region.
- Use stock buffers for retail locations to ensure floor stock availability.
- Review stock movements regularly to identify shrinkage or discrepancies.
- Set low stock thresholds based on your reorder lead time — if it takes 2 weeks to restock, set the threshold to cover 2 weeks of sales.
- Enable inventory tracking before going live to avoid overselling.
