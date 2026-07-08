---
template_type: component_deprecated_warning
category: Component Updates
---

# Email Template: component_deprecated_warning

## Subject
⚠️ سيتم إيقاف {{ component_name }} في {{ deprecation_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ إشعار الإيقاف
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          سيتم إيقاف المكون
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} سيتم إيقافه ولا يُنصح باستخدامه anymore. يرجى التخطيط للمиграة إلى حل بديل.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              مخطط إيقاف المكون:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المكون:</strong> {{ component_name }}<br/>
              <strong>النسخة الحالية:</strong> {{ current_version }}<br/>
              <strong>تاريخ الإيقاف:</strong> {{ deprecation_date }}<br/>
              <strong>نهاية الدعم:</strong> {{ end_of_support_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          السبب في الإيقاف:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ deprecation_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ما يعنيه ذلك:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • سيتم استمرار عمل المكون حتى {{ end_of_support_date }}<br/>
          • لن يتم إضافة ميزات جديدة<br/>
          • سيتم توفير تحديثات الأمان حتى نهاية الدعم<br/>
          • بعد {{ end_of_support_date }}, لن يُقدم المكون تحديثات أخرى
        </mj-text>

        {% if recommended_alternative %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          البديل المقترح:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              {{ alternative_name }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ alternative_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if migration_guide %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ migration_guide }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">عرض دليل الهجرة</a>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        {% if alternative_url %}
        <mj-button href="{{ alternative_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض البديل
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          التواصل مع الدعم
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ إشعار الإيقاف

سيتم إيقاف المكون

{{ component_name }} سيتم إيقافه ولا يُنصح باستخدامه anymore. يرجى التخطيط للمиграة إلى حل بديل.

مخطط إيقاف المكون:
- المكون: {{ component_name }}
- النسخة الحالية: {{ current_version }}
- تاريخ الإيقاف: {{ deprecation_date }}
- نهاية الدعم: {{ end_of_support_date }}

السبب في الإيقاف:
{{ deprecation_reason }}

ما يعنيه ذلك:
• سيتم استمرار عمل المكون حتى {{ end_of_support_date }}
• لن يتم إضافة ميزات جديدة
• سيتم توفير تحديثات الأمان حتى نهاية الدعم
• بعد {{ end_of_support_date }}, لن يُقدم المكون تحديثات أخرى

{% if recommended_alternative %}
البديل المقترح:
{{ alternative_name }}
{{ alternative_description }}
{% endif %}

{% if migration_guide %}عرض دليل الهجرة: {{ migration_guide }}{% endif %}
{% if alternative_url %}عرض البديل: {{ alternative_url }}{% endif %}
التواصل مع الدعم: {{ support_url }}