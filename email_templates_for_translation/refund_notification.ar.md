---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
تم معالجة الاسترجاع - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          تم معالجة الاسترجاع
        </mj-text>
        <mj-text>
          تم معالجة استرجاع لطلب #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>مبلغ الاسترجاع:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          سيظهر الاسترجاع في حسابك خلال {{ refund_days }} أيام عمل.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تم معالجة الاسترجاع

تم معالجة استرجاع لطلب #{{ order_number }}.

مبلغ الاسترجاع: {{ refund_amount }}

سيظهر الاسترجاع في حسابك خلال {{ refund_days }} أيام عمل.