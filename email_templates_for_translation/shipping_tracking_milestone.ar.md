---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
طلبك #{{ order_number }} هو {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تحديث التوصيل: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          أخبار سعيدة! لقد وصل طلبك إلى ميلestone مهم في رحلته إليك.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الطلب:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رقم الطلب:</strong> {{ order_number }}<br/>
              <strong>رقم التتبع:</strong> {{ tracking_number }}<br/>
              <strong>الشركة الناقلة:</strong> {{ carrier_name }}<br/>
              <strong>الموقع الحالي:</strong> {{ current_location }}<br/>
              <strong>التوصيل المتوقع:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تتبع حزمتك
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          لديك أسئلة حول توصيلك؟ <a href="{{ support_url }}">اتصل بالدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تحديث التوصيل: {{ milestone_status }}

مرحباً {{ customer_name }},

أخبار سعيدة! لقد وصل طلبك إلى ميلestone مهم في رحلته إليك.

📦 {{ milestone_status }}
{{ milestone_description }}

تفاصيل الطلب:
- رقم الطلب: {{ order_number }}
- رقم التتبع: {{ tracking_number }}
- الشركة الناقلة: {{ carrier_name }}
- الموقع الحالي: {{ current_location }}
- التوصيل المتوقع: {{ estimated_delivery }}

تتبع حزمتك: {{ tracking_url }}

لديك أسئلة حول توصيلك؟ اتصل بالدعم: {{ support_url }}
