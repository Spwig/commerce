---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
退款已完成 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          退款已完成
        </mj-text>
        <mj-text>
          已為訂單 #{{ order_number }} 處理退款。
        </mj-text>
        <mj-text>
          <strong>退款金額：</strong>{{ refund_amount }}
        </mj-text>
        <mj-text>
          退款將在 {{ refund_days }} 個營業日內顯示在您的帳戶中。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退款已完成

已為訂單 #{{ order_number }} 處理退款。

退款金額：{{ refund_amount }}

退款將在 {{ refund_days }} 個營業日內顯示在您的帳戶中。