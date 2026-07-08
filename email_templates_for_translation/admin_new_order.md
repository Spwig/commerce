---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
New Order Received - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          New Order Received
        </mj-text>
        <mj-text>
          A new order has been placed on your store.
        </mj-text>
        <mj-text>
          <strong>Order Number:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Customer:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Total:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          View in Admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
New Order Received

A new order has been placed on your store.

Order Number: {{ order_number }}
Customer: {{ customer_name }}
Total: {{ order_total }}

View in admin: {{ admin_order_url }}
