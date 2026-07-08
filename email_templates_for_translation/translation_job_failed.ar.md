---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ فشل مهمة الترجمة: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ فشل مهمة الترجمة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          خطأ في الترجمة
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تواجه مهمة الترجمة بالجملة خطأ و لم يمكن إكمالها.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل المهمة:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رقم مهمة:</strong> {{ job_id }}<br/>
              <strong>نوع المحتوى:</strong> {{ content_type }}<br/>
              <strong>اللغات المستهدفة:</strong> {{ target_languages }}<br/>
              <strong>فشل في:</strong> {{ failed_at }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              إنجاز جزئي
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} من {{ total_items }} من العناصر تم ترجمتها بنجاح قبل حدوث الخطأ.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الأسباب الشائعة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • مشاكل في اتصال واجهة برمجة تطبيقات خدمة الترجمة<br/>
          • ائتمانات ترجمة غير كافية<br/>
          • محتوى مصدري غير صالح أو تالف<br/>
          • زوج لغات غير مدعوم
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات الموصى بها:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. تحقق من إعدادات خدمة الترجمة الخاصة بك<br/>
          2. تأكد من توفر ائتمانات الترجمة<br/>
          3. تحقق من رسالة الخطأ لمعرفة المشكلات المحددة<br/>
          4. إعادة المحاولة مهمة الترجمة
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          إعادة المحاولة
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          التحقق من الإعدادات
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
❌ مهمة الترجمة فشلت

خطأ في الترجمة

تواجه مهمة الترجمة بالجملة خطأ و لم يمكن إكمالها.

تفاصيل المهمة:
- رقم مهمة: {{ job_id }}
- نوع المحتوى: {{ content_type }}
- اللغات المستهدفة: {{ target_languages }}
- فشل في: {{ failed_at }}
- كود الخطأ: {{ error_code }}

رسالة الخطأ:
{{ error_message }}

{% if partial_completion %}
إنجاز جزئي:
{{ items_completed }} من {{ total_items }} من العناصر تم ترجمتها بنجاح قبل حدوث الخطأ.
{% endif %}

الأسباب الشائعة:
• مشاكل في اتصال واجهة برمجة تطبيقات خدمة الترجمة
• ائتمانات ترجمة غير كافية
• محتوى مصدري غير صالح أو تالف
• زوج لغات غير مدعوم

الإجراءات الموصى بها:
1. تحقق من إعدادات خدمة الترجمة الخاصة بك
2. تأكد من توفر ائتمانات الترجمة
3. تحقق من رسالة الخطأ لمعرفة المشكلات المحددة
4. إعادة المحاولة مهمة الترجمة

إعادة المحاولة: {{ retry_url }}
التحقق من الإعدادات: {{ settings_url }}

إذا استمرت المشكلة، يرجى التواصل مع الدعم مع رمز الخطأ {{ error_code }}.