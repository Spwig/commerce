---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
لقد تم شحن طلبك #{{ order_number }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 تم شحن الطلب!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          في الطريق!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          أخبار سارة! لقد تم شحن طلبك وسينتقل إليك.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الشحن:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رقم الطلب:</strong> {{ order_number }}<br/>
              <strong>رقم المتابعة:</strong> {{ tracking_number }}<br/>
              <strong>الشاحن:</strong> {{ carrier_name }}<br/>
              <strong>الوصول المقدر:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تتبع حزمتك
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 تم شحن الطلب!

في الطريق!

Hi {{ customer_name }},

أخبار سارة! لقد تم شحن طلبك وسينتقل إليك.

تفاصيل الشحن:
- رقم الطلب: {{ order_number }}
- رقم المتابعة: {{ tracking_number }}
- الشاحن: {{ carrier_name }}
- الوصول المقدر: {{ estimated_delivery }}

تتبع حزمتك: {{ tracking_url }}