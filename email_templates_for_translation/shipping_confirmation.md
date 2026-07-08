---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Your Order Has Shipped - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Your Order Has Shipped!
        </mj-text>
        <mj-text>
          Great news! Your order #{{ order_number }} has been shipped.
        </mj-text>
        <mj-text>
          <strong>Tracking Number:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Carrier:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Track Shipment
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Your Order Has Shipped!

Great news! Your order #{{ order_number }} has been shipped.

Tracking Number: {{ tracking_number }}
Carrier: {{ carrier }}

Track your shipment: {{ tracking_url }}
