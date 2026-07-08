---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ فشل التحديث: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ فشل التحديث
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          خطأ في التثبيت
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          فشل تثبيت التحديث لـ {{ component_name }} إلى الإصدار {{ target_version }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الفشل:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المكون:</strong> {{ component_name }}<br/>
              <strong>الإصدار المستهدف:</strong> {{ target_version }}<br/>
              <strong>فشل في:</strong> {{ failed_at }}<br/>
              <strong>رمز الخطأ:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          رسالة الخطأ:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>السجل الكامل للخطأ:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ما يجب عليك فعله:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. تحقق من متطلبات النظام والاعتماديات<br/>
          2. تحقق من سجل الخطأ للحصول على التفاصيل<br/>
          3. جرّب التثبيت مرة أخرى أو تواصل مع الدعم<br/>
          4. لا يزال متجرك يعمل على {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          إعادة المحاولة
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          التواصل مع الدعم
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ فشل التحديث

خطأ في التثبيت

فشل تثبيت تحديث {{ component_name }} إلى الإصدار {{ target_version }}.

تفاصيل الفشل:
- المكون: {{ component_name }}
- الإصدار المستهدف: {{ target_version }}
- فشل في: {{ failed_at }}
- رمز الخطأ: {{ error_code }}

رسالة الخطأ:
{{ error_message }}

{% if error_log %}
السجل الكامل للخطأ:
{{ error_log|truncatewords:50 }}
{% endif %}

ما يجب عليك فعله:
1. تحقق من متطلبات النظام والاعتماديات
2. تحقق من سجل الخطأ للحصول على التفاصيل
3. جرّب التثبيت مرة أخرى أو تواصل مع الدعم
4. لا يزال متجرك يعمل على {{ current_version }}

إعادة المحاولة: {{ retry_url }}
التواصل مع الدعم: {{ support_url }}