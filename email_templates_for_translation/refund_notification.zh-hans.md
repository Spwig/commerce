---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
退款已完成 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          退款已完成
        </mj-text>
        <mj-text>
          已为您处理订单 #{{ order_number }} 的退款。
        </mj-text>
        <mj-text>
          <strong>退款金额：</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          退款将在 {{ refund_days }} 个工作日内出现在您的账户中。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退款已完成

已为您处理订单 #{{ order_number }} 的退款。

退款金额：{{ refund_amount }}

退款将在 {{ refund_days }} 个工作日内出现在您的账户中。