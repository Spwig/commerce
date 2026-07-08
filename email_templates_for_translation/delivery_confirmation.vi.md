---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
Đơn hàng đã giao - Đơn #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Order Delivered
        </mj-text>
        <mj-text>
          Your order #{{ order_number }} has been delivered!
        </mj-text>
        <mj-text>
          We hope you enjoy your purchase. If you have any questions or concerns, please don't hesitate to contact us.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          View Order
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Order Delivered

Your order #{{ order_number }} has been delivered!

We hope you enjoy your purchase. If you have any questions or concerns, please don't hesitate to contact us.

View order: {{ order_url }}