---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Refund Processed - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Refund Processed
        </mj-text>
        <mj-text>
          A refund has been processed for order #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Refund Amount:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          The refund will appear in your account within {{ refund_days }} business days.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Refund Processed

A refund has been processed for order #{{ order_number }}.

Refund Amount: {{ refund_amount }}

The refund will appear in your account within {{ refund_days }} business days.
