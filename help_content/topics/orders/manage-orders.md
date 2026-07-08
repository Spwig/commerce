---
slug: manage-orders
title_i18n_key: Managing Orders
category: orders-shipping
component: orders
keywords:
  - orders
  - order management
  - fulfillment
  - shipping
  - status
  - refund
  - cancel
  - shipment
  - tracking
url_patterns:
  - /admin/orders/order/
  - /admin/orders/order/\d+/change/
related:
  - setup-shipping
published: true
---

This guide covers everything you need to manage customer orders — from reviewing new orders to processing shipments and handling refunds.

## Order List

Navigate to **Orders > All Orders** in the sidebar to see all orders. The list shows each order's number, status, customer, total, and date.

![Order list](/static/core/admin/img/help/manage-orders/order-list.webp)

Use the filters at the top to narrow down orders by status, date range, or search by order number or customer name.

## Order Detail

Click any order to open its detail page. Here you'll find everything about the order organized into clear sections.

![Order detail](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Order Information

The top section shows:

- **Order Number** — The unique identifier for this order
- **Status** — Current order status (Pending, Processing, Shipped, Delivered, Cancelled, Refunded)
- **Payment** — Payment status (Unpaid, Partially Paid, Paid, Refunded, Partially Refunded, Failed, Pending)
- **Source** — How the customer arrived: Direct, Referral, Email, Social Media, Loyalty Program, Organic Search, UTM Campaign
- **Test** — A TEST badge appears on orders placed through sandbox/test payment accounts
- **Customer** — Name and email of the customer who placed the order
- **Created** — When the order was placed

### Order Items

The items section lists everything the customer ordered:

- Product name and SKU
- Quantity ordered
- Unit price and line total
- Any applied discounts

### Payment Details

Shows the payment method used, transaction ID, and payment status. For orders awaiting payment, you can track the payment gateway status here.

### Shipping Address

The customer's delivery address. If the billing address differs, both are shown.

## Order Lifecycle

Orders typically move through these statuses:

1. **Pending** — New order received, awaiting payment confirmation
2. **Processing** — Payment confirmed, preparing for shipment
3. **Shipped** — Order dispatched with tracking information
4. **Delivered** — Customer received the order
5. **Cancelled** — Order cancelled before fulfillment
6. **Refunded** — Order has been refunded

## Processing an Order

### 1. Review the Order

Check that:

- Items and quantities are correct
- Shipping address is complete
- Payment has been received
- Any customer notes are addressed

### 2. Create a Shipment

To ship the order:

1. Click **Create Shipment** on the order detail page
2. Select which items to include (for partial shipments, select only some items)
3. Choose the shipping carrier and service
4. Enter the tracking number
5. Click **Save Shipment**

The order status automatically updates to **Shipped** and the customer receives a shipping notification email with tracking information.

### 3. Mark as Delivered

Once the customer confirms delivery or the tracking shows delivered, update the status to **Delivered**.

## Order Actions

### Adding Notes

Add internal notes or customer-visible messages:

1. Scroll to the **Notes** section on the order detail page
2. Type your message
3. Choose whether it's an internal note (staff only) or a customer notification
4. Click **Add Note**

Customer-visible notes trigger an email notification.

### Processing a Refund

To issue a refund:

1. Click **Refund** on the order detail page
2. Select the items to refund (or enter a custom amount)
3. Choose a refund reason
4. Confirm the refund

Refunds are processed through the original payment gateway. The customer receives an email confirmation.

### Cancelling an Order

To cancel:

1. Click **Cancel Order**
2. Select a cancellation reason
3. Choose whether to restock the items
4. Confirm

The customer is notified automatically and a refund is initiated if payment was already taken.

## Bulk Actions

From the order list, you can select multiple orders and apply bulk actions:

- **Mark as Processing / Shipped / Delivered / Cancelled** — Move orders to the selected status at once
- **Mark as Paid / Unpaid / Payment Pending** — Update payment status across multiple orders simultaneously
- **Generate packing slips** — Create printable packing slips for selected orders
- **Generate commercial invoices** — Create commercial invoices (useful for international shipments)
- **Generate customs forms** — Create customs declaration forms for cross-border orders
- **Generate licenses** — Manually trigger license key generation for digital products

## Shipping Documents

Once a shipment has been created for an order, shipping documents become available in the **Documents** section on the order detail page:

- **Packing Slip** — Printable list of items in the shipment
- **Commercial Invoice** — Required for international orders
- **Customs Form** — Customs declaration for cross-border shipments

Documents can be downloaded as PDF from the order detail page, or generated in bulk from the order list.

## Order Notifications

Customers automatically receive emails at key stages:

- **Order confirmation** — Immediately after placing the order
- **Payment received** — When payment is confirmed
- **Shipping notification** — When a shipment is created (includes tracking link)
- **Delivery confirmation** — When marked as delivered

Configure email templates in **Settings > Email Configuration**.

## Tips

- Process orders daily to maintain fast shipping times.
- Use the status filters to focus on orders that need attention (Pending and Processing).
- Add internal notes to track any special handling requirements.
- For high-volume periods, use bulk actions to update multiple orders at once.
- Set up shipping rules to automate carrier selection based on order weight and destination.
