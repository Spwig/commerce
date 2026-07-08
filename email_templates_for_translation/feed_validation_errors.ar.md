---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: تمت العثور على {{ error_count }} أخطاء التحقق

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ أخطاء التحقق من المغذّي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'\'#1f2937' }}">
          تم اكتشاف مشاكل جودة البيانات
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'\'#4b5563' }}">
          تمت العثور على {{ error_count }} خطأ التحقق{{ error_count|pluralize }} في {{ feed_name }}. قد تمنع هذه المشكلات المنتجات من الظهور على {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'\'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'\'#1f2937' }}">
              ملخص التحقق:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'\'#4b5563' }}">
              <strong>المغذّي:</strong> {{ feed_name }}<br/>
              <strong>المنصة:</strong> {{ platform_name }}<br/>
              <strong>تم التحقق:</strong> {{ validated_at }}<br/>
              <strong>إجمالي المنتجات:</strong> {{ total_products }}<br/>
              <strong>المنتجات ذات الأخطاء:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'\'#1f2937' }}">
          الأخطاء الأهم:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} منتج{{ error.count|pluralize }} تأثر: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'\'#1f2937' }}">
          ما يجب إصلاحه:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'\'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'\'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض جميع الأخطاء
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          إدارة المغذّي
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'\'#6b7280' }}" align="center">
          قم بإصلاح هذه الأخطاء لضمان ظهور جميع المنتجات على {{ platform_name }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ أخطاء التحقق من المغذّي

مشاكل جودة البيانات تم اكتشافها

تم العثور على {{ error_count }} خطأ التحقق{{ error_count|pluralize }} في {{ feed_name }}. قد تمنع هذه المشكلات المنتجات من الظهور على {{ platform_name }}.

ملخص التحقق:
- المغذّي: {{ feed_name }}
- المنصة: {{ platform_name }}
- تم التحقق: {{ validated_at }}
- إجمالي المنتجات: {{ total_products }}
- المنتجات ذات الأخطاء: {{ affected_products }}

الأخطاء الأهم:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} منتج{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

ما يجب إصلاحه:
{{ fix_instructions }}

عرض جميع الأخطاء: {{ errors_url }}
إدارة المغذّي: {{ admin_feed_url }}

قم بإصلاح هذه الأخطاء لضمان ظهور جميع المنتجات على {{ platform_name }}.