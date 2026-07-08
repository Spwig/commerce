---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 بدأت مهمة الترجمة: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 بدأت مهمة الترجمة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          مهمة ترجمة كمّية قيد التنفيذ
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تم بدء مهمة الترجمة الكمية الخاصة بك ونحن الآن نقوم بمعالجتها.
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
              <strong>اللغة الأصلية:</strong> {{ source_language }}<br/>
              <strong>لغات الوجهة:</strong> {{ target_languages }}<br/>
              <strong>عدد العناصر المراد ترجمتها:</strong> {{ item_count }}<br/>
              <strong>الوقت الذي بدأ فيه:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          التقدير الزمني لإكمال المهمة:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (بناءً على {{ word_count }} كلمة)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ماذا يحدث بعد ذلك:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. خدمة الترجمة بالذكاء الاصطناعي تُعالج محتواك<br/>
          2. يتم حفظ الترجمات كمسودات للتدقيق<br/>
          3. سيتم إرسال بريد إلكتروني إليك عندما تكتمل المهمة<br/>
          4. قم بمراجعة ونشر الترجمات من خلال لوحة التحكم الخاصة بك
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض حالة المهمة
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          يمكنك إغلاق هذا البريد الإلكتروني. سنخطرك عندما تكتمل الترجمة.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 بدأت مهمة الترجمة

مهمة ترجمة كمّية قيد التنفيذ

تم بدء مهمة الترجمة الكمية الخاصة بك ونحن الآن نقوم بمعالجتها.

تفاصيل المهمة:
- رقم مهمة: {{ job_id }}
- نوع المحتوى: {{ content_type }}
- اللغة الأصلية: {{ source_language }}
- لغات الوجهة: {{ target_languages }}
- عدد العناصر المراد ترجمتها: {{ item_count }}
- الوقت الذي بدأ فيه: {{ started_at }}

الوقت المقدر لإكمال المهمة:
{{ estimated_completion }}
(بناءً على {{ word_count }} كلمة)

ماذا يحدث بعد ذلك:
1. خدمة الترجمة بالذكاء الاصطناعي تُعالج محتواك
2. يتم حفظ الترجمات كمسودات للتدقيق
3. سيتم إرسال بريد إلكتروني إليك عندما تكتمل المهمة
4. قم بمراجعة ونشر الترجمات من خلال لوحة التحكم الخاصة بك

عرض حالة المهمة: {{ job_status_url }}

يمكنك إغلاق هذا البريد الإلكتروني. سنخطرك عندما تكتمل الترجمة.