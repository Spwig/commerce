---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ فشل إنشاء المغذي: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ فشل إنشاء المغذي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          خطأ في الإنشاء
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          فشل إنشاء مغذي المنتج {{ feed_name }} بسبب خطأ.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الخطأ:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المغذي:</strong> {{ feed_name }}<br/>
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
          <strong>سُجل الأخطاء:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:30 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الأسباب الشائعة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • نقص البيانات المطلوبة للمنتج (العنوان، السعر، الصورة)<br/>
          • تنسيق البيانات غير الصحيح للمنتج<br/>
          • مشاكل في اتصال قاعدة البيانات<br/>
          • مساحة تخزين غير كافية أو ذاكرة قليلة
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          إعادة المحاولة
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض إعدادات المغذي
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          إذا استمرت المشكلة، يرجى التواصل مع الدعم مع رمز الخطأ {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ فشل إنشاء المغذي

خطأ في الإنشاء

فشل إنشاء مغذي المنتج {{ feed_name }} بسبب خطأ.

تفاصيل الخطأ:
- المغذي: {{ feed_name }}
- فشل في: {{ failed_at }}
- رمز الخطأ: {{ error_code }}

رسالة الخطأ:
{{ error_message }}

{% if error_log %}
سُجل الأخطاء:
{{ error_log|truncatewords:30 }}
{% endif %}

الأسباب الشائعة:
• نقص البيانات المطلوبة للمنتج (العنوان، السعر، الصورة)
• تنسيق البيانات غير الصحيح للمنتج
• مشاكل في اتصال قاعدة البيانات
• مساحة تخزين غير كافية أو ذاكرة قليلة

إعادة المحاولة: {{ retry_url }}
عرض إعدادات المغذي: {{ admin_feed_url }}

إذا استمرت المشكلة، يرجى التواصل مع الدعم مع رمز الخطأ {{ error_code }}.