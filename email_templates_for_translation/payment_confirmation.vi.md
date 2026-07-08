---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Xác nhận thanh toán - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Xác nhận thanh toán
        </mj-text>
        <mj-text>
          Your payment for order #{{ order_number }} has been successfully processed.
        </mj-text>
        <mj-text>
          <strong>Amount Paid:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Payment Method:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Xác nhận thanh toán

Your payment for order #{{ order_number }} has been successfully processed.

Amount Paid: {{ amount_paid }}
Payment Method: {{ payment_method }}