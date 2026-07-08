---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ اكتمال الترجمة: {{ content_type }} ({{ language_count }} لغات)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ اكتمال الترجمة!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          جاهزة الترجمات الخاصة بك
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          أخبار سارة! تم الانتهاء من مهمة الترجمة الضخمة الخاصة بك بنجاح.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ملخص المهمة:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رقم المهمة:</strong> {{ job_id }}<br/>
              <strong>نوع المحتوى:</strong> {{ content_type }}<br/>
              <strong>اللغات:</strong> {{ target_languages }}<br/>
              <strong>العناصر المترجمة:</strong> {{ items_translated }}<br/>
              <strong>إجمالي الكلمات:</strong> {{ word_count }}<br/>
              <strong>اكتمال:</strong> {{ completed_at }}<br/>
              <strong>المدة:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          جودة الترجمة:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>الدرجة المتوسطة للجودة:</strong> {{ quality_score }}%<br/>
              <strong>جودة عالية:</strong> {{ high_quality_count }} عناصر<br/>
              <strong>توصية بالتدقيق:</strong> {{ review_needed_count }} عناصر
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ توصية بالتدقيق
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} ترجمة حصلت على درجة أقل من 85% ويجب مراجعتها قبل النشر.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الخطوات التالية:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. مراجعة الترجمات في لوحة التحكم الخاصة بك<br/>
          2. تعديل أي ترجمات تحتاج إلى تحسين<br/>
          3. نشر الترجمات لجعلها نشطة<br/>
          4. ستكون محتوياتك متعددة اللغات متاحة للعملاء
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          مراجعة الترجمات
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          النشر الكامل
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ اكتمال الترجمة!

ترجماتك جاهزة

أخبار سارة! تم الانتهاء من مهمة الترجمة الضخمة الخاصة بك بنجاح.

ملخص المهمة:
- رقم المهمة: {{ job_id }}
- نوع المحتوى: {{ content_type }}
- اللغات: {{ target_languages }}
- العناصر المترجمة: {{ items_translated }}
- إجمالي الكلمات: {{ word_count }}
- اكتمال: {{ completed_at }}
- المدة: {{ job_duration }}

جودة الترجمة:
- درجة الجودة المتوسطة: {{ quality_score }}%
- جودة عالية: {{ high_quality_count }} عناصر
- توصية بالتدقيق: {{ review_needed_count }} عناصر

{% if review_needed_count > 0 %}
⚠️ توصية بالتدقيق:
{{ review_needed_count }} ترجمة حصلت على درجة أقل من 85% ويجب مراجعتها قبل النشر.
{% endif %}

الخطوات التالية:
1. مراجعة الترجمات في لوحة التحكم الخاصة بك
2. تعديل أي ترجمات تحتاج إلى تحسين
3. نشر الترجمات لجعلها نشطة
4. ستكون محتوياتك متعددة اللغات متاحة للعملاء

مراجعة الترجمات: {{ review_url }}
{% if can_publish_all %}نشر كل شيء: {{ publish_all_url }}{% endif %}