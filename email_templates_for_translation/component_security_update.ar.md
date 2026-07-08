---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 مهمة: تحديث أمان متوفر لـ {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 تحديث أمني مطلوب
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          إصلاح أمني حيوي
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم اكتشاف ثغرة أمنية في {{ component_name }}. من فضلكم قم بالتحديث فورًا لحماية متجركم.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ معلومات الأمان
            </mj-text>
            <mj-text color="#991b1b">
              <strong>المكون:</strong> {{ component_name }}<br/>
              <strong>النسخة الحالية:</strong> {{ current_version }}<br/>
              <strong>النسخة المعتمدة:</strong> {{ patched_version }}<br/>
              <strong>الشدة:</strong> {{ severity_level }}<br/>
              <strong>CVE ID:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تفاصيل الثغرة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          التأثير المحتمل:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              محاولة مؤقتة
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          الإجراء المطلوب: تثبيت التحديث فورًا
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تثبيت إصلاح الأمان
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          اقرأ الإشعار الأمني
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          إذا كنت بحاجة إلى مساعدة، يرجى التواصل مع دعم Spwig فورًا.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 تحديث أمني مطلوب

إصلاح أمني حيوي

تم اكتشاف ثغرة أمنية في {{ component_name }}. من فضلكم قم بالتحديث فورًا لحماية متجركم.

⚠️ معلومات الأمان:
- المكون: {{ component_name }}
- النسخة الحالية: {{ current_version }}
- النسخة المعتمدة: {{ patched_version }}
- الشدة: {{ severity_level }}
- CVE ID: {{ cve_id }}

تفاصيل الثغرة:
{{ vulnerability_description }}

التأثير المحتمل:
{{ impact_description }}

{% if mitigation_steps %}
محاولة مؤقتة:
{{ mitigation_steps }}
{% endif %}

الإجراء المطلوب: تثبيت التحديث فورًا

تثبيت إصلاح الأمان: {{ update_url }}
قراءة الإشعار الأمني: {{ advisory_url }}

إذا كنت بحاجة إلى مساعدة، يرجى التواصل مع دعم Spwig فورًا.