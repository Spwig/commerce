---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
您的訂單已發貨 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          您的訂單已發貨！
        </mj-text>
        <mj-text>
          好消息！您的訂單 #{{ order_number }} 已發貨。
        </mj-text>
        <mj-text>
          <strong>追蹤編號：</strong>{{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>運送商：</strong>{{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          追蹤貨物
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您的訂單已發貨！

好消息！您的訂單 #{{ order_number }} 已發貨。

追蹤編號：{{ tracking_number }}
運送商：{{ carrier }}

追蹤貨物：{{ tracking_url }}