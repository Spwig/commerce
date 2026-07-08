---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
تم التأكيد على الدفع - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          تم التأكيد على الدفع
        </mj-text>
        <mj-text>
          تم معالجة دفعتكم لطلب #{{ order_number }} بنجاح.
        </mj-text>
        <mj-text>
          <strong>المبلغ المدفوع:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>طريقة الدفع:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تم التأكيد على الدفع

تم معالجة دفعتكم لطلب #{{ order_number }} بنجاح.

المبلغ المدفوع: {{ amount_paid }}
طريقة الدفع: {{ payment_method }}