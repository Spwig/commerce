---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Payment Confirmed - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Payment Confirmed
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
Payment Confirmed

Your payment for order #{{ order_number }} has been successfully processed.

Amount Paid: {{ amount_paid }}
Payment Method: {{ payment_method }}
