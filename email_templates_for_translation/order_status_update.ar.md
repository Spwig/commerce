---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
تحديث حالة الطلب #{{ order_number }} - {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تحديث حالة الطلب
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
          الطلب #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          حالة طلبك <strong>#{{ order_number }}</strong> قد تم تحديثها.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الحالة السابقة:</strong> {{ old_status_display }}<br/>
              <strong>الحالة الجديدة:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض تفاصيل الطلب
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تحديث حالة الطلب - الطلب #{{ order_number }}

مرحباً {{ customer_name }},

حالة طلبك #{{ order_number }} قد تم تحديثها.

الحالة السابقة: {{ old_status_display }}
الحالة الجديدة: {{ new_status_display }}

{% if order_url %}عرض تفاصيل الطلب: {{ order_url }}{% endif %}