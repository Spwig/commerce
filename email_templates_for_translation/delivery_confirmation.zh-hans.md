---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
订单已送达 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          订单已送达
        </mj-text>
        <mj-text>
          您的订单 #{{ order_number }} 已送达！
        </mj-text>
        <mj-text>
          希望您喜欢您的购买。如果您有任何问题或疑虑，请随时联系我们。
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          查看订单
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
订单已送达

您的订单 #{{ order_number }} 已送达！

希望您喜欢您的购买。如果您有任何问题或疑虑，请随时联系我们。

查看订单：{{ order_url }}