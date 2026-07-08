---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
您的订单已发货 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          您的订单已发货！
        </mj-text>
        <mj-text>
          好消息！您的订单 #{{ order_number }} 已发货。
        </mj-text>
        <mj-text>
          <strong>运单号：</strong>{{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>承运商：</strong>{{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          跟踪发货
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您的订单已发货！

好消息！您的订单 #{{ order_number }} 已发货。

运单号：{{ tracking_number }}
承运商：{{ carrier }}

跟踪发货：{{ tracking_url }}

