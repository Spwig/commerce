---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ تم حل: عادت {{ metric_name }} إلى طبيعتها

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ تم حل المشكلة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          استعادة حالة النظام
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          أخبار جيدة! تم حل مشكلة حالة النظام الخاصة بـ {{ metric_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الاستعادة:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المقاس:</strong> {{ metric_name }}<br/>
              <strong>القيمة الحالية:</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>الحد الطبيعي:</strong> {{ normal_threshold }}<br/>
              <strong>تم اكتشاف المشكلة:</strong> {{ issue_detected_at }}<br/>
              <strong>تم الاستعادة:</strong> {{ recovered_at }}<br/>
              <strong>المدة:</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ حالة النظام: طبيعية
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              عادت {{ metric_name }} إلى المستويات الطبيعية وتعمل ضمن المعايير القابلة القبول.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص الحل:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات المتخذة:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ actions_taken }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if preventive_measures %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات الوقائية:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ preventive_measures }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض لوحة تحكم النظام
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض تقرير الحادث
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ تم حل المشكلة

استعادة حالة النظام

أخبار جيدة! تم حل مشكلة حالة النظام الخاصة بـ {{ metric_name }}.

تفاصيل الاستعادة:
- المقاس: {{ metric_name }}
- القيمة الحالية: {{ current_value }}
- الحد الطبيعي: {{ normal_threshold }}
- تم اكتشاف المشكلة: {{ issue_detected_at }}
- تم الاستعادة: {{ recovered_at }}
- المدة: {{ issue_duration }}

✓ حالة النظام: طبيعية
{{ metric_name }} عادت إلى المستويات الطبيعية وتعمل ضمن المعايير القابلة القبول.

{% if resolution_summary %}
ملخص الحل:
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
الإجراءات المتخذة:
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
الإجراءات الوقائية:
{{ preventive_measures }}
{% endif %}

عرض لوحة تحكم النظام: {{ dashboard_url }}
{% if incident_report_url %}عرض تقرير الحادث: {{ incident_report_url }}{% endif %}