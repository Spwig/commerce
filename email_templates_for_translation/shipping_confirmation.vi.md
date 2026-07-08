---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Đơn hàng của bạn đã được giao - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Đơn hàng của bạn đã được giao!
        </mj-text>
        <mj-text>
          Tin vui! Đơn hàng #{{ order_number }} của bạn đã được giao.
        </mj-text>
        <mj-text>
          <strong>Số theo dõi:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Người vận chuyển:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Theo dõi vận chuyển
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Đơn hàng của bạn đã được giao!

Tin vui! Đơn hàng #{{ order_number }} của bạn đã được giao.

Số theo dõi: {{ tracking_number }}
Người vận chuyển: {{ carrier }}

Theo dõi vận chuyển: {{ tracking_url }}
