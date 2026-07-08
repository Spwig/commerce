---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
فشل الدفع - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          فشل الدفع
        </mj-text>
        <mj-text>
          فشل محاولة الدفع لطلب #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>العميل:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>المبلغ:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>الخطأ:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          اعرض في الادارة
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
فشل الدفع

فشل محاولة الدفع لطلب #{{ order_number }}.

العميل: {{ customer_name }}
المبلغ: {{ order_total }}
الخطأ: {{ error_message }}

اعرض في الادارة: {{ admin_order_url }}