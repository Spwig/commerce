---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ تم تراجع {{ component_name }} إلى v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ تم التراجع بالكامل
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          استعادة المكون
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم استعادة {{ component_name }} بنجاح إلى الإصدار السابق.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل التراجع:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المكون:</strong> {{ component_name }}<br/>
              <strong>تم التراجع من:</strong> v{{ failed_version }}<br/>
              <strong>تم استعادة إلى:</strong> v{{ previous_version }}<br/>
              <strong>تم الانتهاء:</strong> {{ completed_at }}<br/>
              <strong>المدة:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          السبب في التراجع:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ حالة المتجر
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              الآن متجرك يعمل على الإصدار المستقر {{ previous_version }}. يجب أن يتم استعادة جميع الوظائف.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>استعادة البيانات:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الخطوات التالية:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض تفاصيل المكون
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض تقرير الحادث
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          إذا استمرت في مواجهة مشاكل، يرجى التواصل مع الدعم.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ تم التراجع بالكامل

استعادة المكون

تم استعادة {{ component_name }} بنجاح إلى الإصدار السابق.

تفاصيل التراجع:
- المكون: {{ component_name }}
- تم التراجع من: v{{ failed_version }}
- تم استعادة إلى: v{{ previous_version }}
- تم الانتهاء: {{ completed_at }}
- المدة: {{ rollback_duration }}

{% if rollback_reason %}
السبب في التراجع:
{{ rollback_reason }}
{% endif %}

✓ حالة المتجر:
الآن متجرك يعمل على الإصدار المستقر {{ previous_version }}. يجب أن يتم استعادة جميع الوظائف.

{% if data_restored %}
استعادة البيانات: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
الخطوات التالية:
{{ next_steps }}
{% endif %}

عرض تفاصيل المكون: {{ component_url }}
{% if incident_report_url %}عرض تقرير الحادث: {{ incident_report_url }}{% endif %}

إذا استمرت في مواجهة مشاكل، يرجى التواصل مع الدعم.