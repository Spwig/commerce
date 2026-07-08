---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 تحذير نقدي: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 تحذير نظام نقدي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          مطلوب انتباه فوري
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تم اكتشاف مشكلة صحية نقدية في تثبيت Spwig الخاص بك.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 مشكلة نقديّة
            </mj-text>
            <mj-text color="#991b1b">
              <strong>المتر:</strong> {{ metric_name }}<br/>
              <strong>القيمة الحاليّة:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>المستوى النقدي:</strong> {{ critical_threshold }}<br/>
              <strong>تم اكتشافه:</strong> {{ detected_at }}<br/>
              <strong>الخطورة:</strong> نقدي
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          التأثير:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات الفورية المطلوبة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الاتجاه:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ تحذير تدهور الخدمة
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              قد تؤدي هذه المشكلة إلى انقطاعات في الخدمة أو تدهور في الأداء. قم بمعالجتها فورًا لمنع تأثيرها على العملاء.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض لوحة تحكم النظام
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض سجلات النظام
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 تحذير نظام نقدي

مطلوب انتباه فوري

تم اكتشاف مشكلة صحية نقدية في تثبيت Spwig الخاص بك.

🚨 مشكلة نقديّة:
- المتر: {{ metric_name }}
- القيمة الحاليّة: {{ current_value }}
- المستوى النقدي: {{ critical_threshold }}
- تم اكتشافه: {{ detected_at }}
- الخطورة: نقدي

التأثير:
{{ impact_description }}

الإجراءات الفورية المطلوبة:
{{ recommended_actions }}

{% if trend_data %}
الاتجاه:
{{ trend_data }}
{% endif %}

⚠️ تحذير تدهور الخدمة:
قد تؤدي هذه المشكلة إلى انقطاعات في الخدمة أو تدهور في الأداء. قم بمعالجتها فورًا لمنع تأثيرها على العملاء.

عرض لوحة تحكم النظام: {{ dashboard_url }}
عرض سجلات النظام: {{ logs_url }}