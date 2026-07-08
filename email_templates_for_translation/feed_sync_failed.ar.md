---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ فشل التزامن مع {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ فشل التزامن
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          خطأ في التزامن
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          فشل في تزامن {{ feed_name }} مع {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الفشل:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المصدر:</strong> {{ feed_name }}<br/>
              <strong>المنصة:</strong> {{ platform_name }}<br/>
              <strong>وقت الفشل:</strong> {{ failed_at }}<br/>
              <strong>كود الخطأ:</strong> {{ error_code }}
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الأسباب الشائعة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • بيانات API غير صحيحة أو رمز تحقق منتهي الصلاحية<br/>
          • مشاكل في اتصال الشبكة<br/>
          • تجاوز حدود معدلات API للمنصة<br/>
          • تنسيق المصدر لا يتوافق مع متطلبات المنصة
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              الإجراء المقترح
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          إعادة المحاولة
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          التحقق من إعدادات المصدر
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ فشل التزامن

خطأ في التزامن

فشل في تزامن {{ feed_name }} مع {{ platform_name }}.

تفاصيل الفشل:
- المصدر: {{ feed_name }}
- المنصة: {{ platform_name }}
- وقت الفشل: {{ failed_at }}
- كود الخطأ: {{ error_code }}

رسالة الخطأ:
{{ error_message }}

الأسباب الشائعة:
• بيانات API غير صحيحة أو رمز تحقق منتهي الصلاحية
• مشاكل في اتصال الشبكة
• تجاوز حدود معدلات API للمنصة
• تنسيق المصدر لا يتوافق مع متطلبات المنصة

{% if recommended_action %}
الإجراء المقترح:
{{ recommended_action }}
{% endif %}

إعادة المحاولة: {{ retry_url }}
التحقق من إعدادات المصدر: {{ admin_feed_url }}