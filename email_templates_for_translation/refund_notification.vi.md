---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Hoàn tiền đã được xử lý - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Hoàn tiền đã được xử lý
        </mj-text>
        <mj-text>
          Một khoản hoàn tiền đã được xử lý cho đơn hàng #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Số tiền hoàn lại:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          Số tiền hoàn lại sẽ xuất hiện trong tài khoản của bạn trong vòng {{ refund_days }} ngày làm việc.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hoàn tiền đã được xử lý

Một khoản hoàn tiền đã được xử lý cho đơn hàng #{{ order_number }}.

Số tiền hoàn lại: {{ refund_amount }}

Số tiền hoàn lại sẽ xuất hiện trong tài khoản của bạn trong vòng {{ refund_days }} ngày làm việc.