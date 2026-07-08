---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
تم استلام طلب جديد - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          طلب جديد تم استلامه
        </mj-text>
        <mj-text>
          تم وضع طلب جديد على متجرك.
        </mj-text>
        <mj-text>
          <strong>رقم الطلب:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>العميل:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>المجموع:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          عرض في الإداري
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
طلب جديد تم استلامه

تم وضع طلب جديد على متجرك.

رقم الطلب: {{ order_number }}
العميل: {{ customer_name }}
المجموع: {{ order_total }}

عرض في الإداري: {{ admin_order_url }}
