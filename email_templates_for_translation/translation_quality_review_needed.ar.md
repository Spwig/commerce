---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ تمت اكتشاف ترجمات ذات جودة منخفضة: {{ content_type }} - {{ low_quality_count }} عنصر يحتاج مراجعة

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ تحذير جودة الترجمة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          يُنصح بمراجعة
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          انتهت وظيفة الترجمة الخاصة بك، ولكن {{ low_quality_count }} ترجمة حصلت على درجة أقل من عتبة الجودة وتحتاج إلى مراجعة قبل النشر.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ملخص المهمة:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رقم المهمة:</strong> {{ job_id }}<br/>
              <strong>نوع المحتوى:</strong> {{ content_type }}<br/>
              <strong>المجموع:</strong> {{ total_items }}<br/>
              <strong>متوسط الجودة:</strong> {{ average_quality }}%<br/>
              <strong>جودة منخفضة:</strong> {{ low_quality_count }} عنصر ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تحليل الجودة:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ممتاز (95-100%):</strong> {{ excellent_count }} عنصر<br/>
              <strong>جيد (85-94%):</strong> {{ good_count }} عنصر<br/>
              <strong>مقبول (70-84%):</strong> {{ fair_count }} عنصر<br/>
              <strong>ضعيف (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} عنصر</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          المشكلات الشائعة في جودة الترجمة:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} مرات
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات الموصى بها:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. مراجعة الترجمات المرصودة في لوحة الإدارة<br/>
          2. تعديل الترجمات ذات الجودة المنخفضة يدويًا<br/>
          3. تفكير في إعادة ترجمة العناصر ذات الجودة المنخفضة<br/>
          4. نشر فقط بعد إكمال المراجعة
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          مراجعة الترجمات
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض العناصر ذات الجودة المنخفضة
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 نصيحة: درجات الجودة أقل من 85% تشير إلى مشاكل محتملة في القواعد النحوية أو السياق أو الدقة. يُنصح بشدة بمراجعة البشرية قبل النشر.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ تحذير جودة الترجمة

يُنصح بمراجعة

انتهت وظيفة الترجمة الخاصة بك، ولكن {{ low_quality_count }} ترجمة حصلت على درجة أقل من عتبة الجودة وتحتاج إلى مراجعة قبل النشر.

ملخص المهمة:
- رقم المهمة: {{ job_id }}
- نوع المحتوى: {{ content_type }}
- المجموع: {{ total_items }}
- متوسط الجودة: {{ average_quality }}%
- جودة منخفضة: {{ low_quality_count }} عنصر ({{ low_quality_percentage }}%)

تحليل الجودة:
- ممتاز (95-100%): {{ excellent_count }} عنصر
- جيد (85-94%): {{ good_count }} عنصر
- مقبول (70-84%): {{ fair_count }} عنصر
- ضعيف (<70%): {{ poor_count }} عنصر

المشكلات الشائعة في جودة الترجمة:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} مرات
{% endfor %}

الإجراءات الموصى بها:
1. مراجعة الترجمات المرصودة في لوحة الإدارة
2. تعديل الترجمات ذات الجودة المنخفضة يدويًا
3. تفكير في إعادة ترجمة العناصر ذات الجودة المنخفضة
4. نشر فقط بعد إكمال المراجعة

مراجعة الترجمات: {{ review_url }}
عرض العناصر ذات الجودة المنخفضة: {{ low_quality_url }}

💡 نصيحة: درجات الجودة أقل من 85% تشير إلى مشاكل محتملة في القواعد النحوية أو السياق أو الدقة. يُنصح بشدة بمراجعة البشرية قبل النشر.