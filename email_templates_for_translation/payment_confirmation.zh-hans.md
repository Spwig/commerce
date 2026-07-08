---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
付款确认 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          付款确认
        </mj-text>
        <mj-text>
          您的订单 #{{ order_number }} 的付款已成功处理。
        </mj-text>
        <mj-text>
          <strong>已支付金额：</strong>{{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>支付方式：</strong>{{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
付款确认

您的订单 #{{ order_number }} 的付款已成功处理。

已支付金额：{{ amount_paid }}
支付方式：{{ payment_method }}