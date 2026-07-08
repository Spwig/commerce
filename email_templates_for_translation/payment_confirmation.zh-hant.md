---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
付款確認 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          付款確認
        </mj-text>
        <mj-text>
          您的訂單 #{{ order_number }} 的付款已成功處理。
        </mj-text>
        <mj-text>
          <strong>已支付金額：</strong>{{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>付款方式：</strong>{{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
付款確認

您的訂單 #{{ order_number }} 的付款已成功處理。

已支付金額：{{ amount_paid }}
付款方式：{{ payment_method }}