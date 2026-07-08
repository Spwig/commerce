---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ تحذير من صحة النظام: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ تحذير من صحة النظام
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تجاوز ngima al-muwaqqa3a
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تجاوز مؤشر صحة النظام ngima al-muwaqqa3a fi 3ar8at Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل التحذير:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المؤشر:</strong> {{ metric_name }}<br/>
              <strong>القيمة الحالية:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>ngima al-muwaqqa3a:</strong> {{ warning_threshold }}<br/>
              <strong>ngima al-mu3arradha:</strong> {{ critical_threshold }}<br/>
              <strong>تم الكشف:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          التأثير المحتمل:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات الموصى بها:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تحليل الاتجاه:
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

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 الإجراء المطلوب: رغم أن هذا التحذير ليس خطيرًا بعد، فإن معالجته الآن يمكن أن تمنع مشاكل الخدمة المستقبلية.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض لوحة تحكم النظام
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض المؤشرات التفصيلية
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ تحذير من صحة النظام

تجاوز ngima al-muwaqqa3a

تجاوز مؤشر صحة النظام ngima al-muwaqqa3a fi 3ar8at Spwig.

تفاصيل التحذير:
- المؤشر: {{ metric_name }}
- القيمة الحالية: {{ current_value }}
- ngima al-muwaqqa3a: {{ warning_threshold }}
- ngima al-mu3arradha: {{ critical_threshold }}
- تم الكشف: {{ detected_at }}

التأثير المحتمل:
{{ impact_description }}

الإجراءات الموصى بها:
{{ recommended_actions }}

{% if trend_data %}
تحليل الاتجاه:
{{ trend_data }}
{% endif %}

💡 الإجراء المطلوب: رغم أن هذا التحذير ليس خطيرًا بعد، فإن معالجته الآن يمكن أن تمنع مشاكل الخدمة المستقبلية.

عرض لوحة تحكم النظام: {{ dashboard_url }}
عرض المؤشرات التفصيلية: {{ metrics_url }}