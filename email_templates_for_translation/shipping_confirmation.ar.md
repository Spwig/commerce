---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
لقد تم شحن طلبك - الطلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          لقد تم شحن طلبك!
        </mj-text>
        <mj-text>
          أخبار سارة! لقد تم شحن طلبك #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>رقم المتابعة:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>الشاحن:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          تتبع الشحن
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
لقد تم شحن طلبك!

أخبار سارة! لقد تم شحن طلبك #{{ order_number }}.

رقم المتابعة: {{ tracking_number }}
الشاحن: {{ carrier }}

تتبع شحنتك: {{ tracking_url }}