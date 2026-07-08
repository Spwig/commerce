---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
تم التسليم - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          تم التسليم
        </mj-text>
        <mj-text>
          تم تسليم طلبك #{{ order_number }}!
        </mj-text>
        <mj-text>
          نأمل أن تستمتع بطلبك. إذا كانت لديك أي أسئلة أو مخاوف، لا تتردد في الاتصال بنا.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          عرض الطلب
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تم التسليم

طلبك #{{ order_number }} قد تم تسليمه!

نأمل أن تستمتع بطلبك. إذا كانت لديك أي أسئلة أو مخاوف، لا تتردد في الاتصال بنا.

عرض الطلب: {{ order_url }}