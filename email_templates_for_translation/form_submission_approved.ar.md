---
template_type: form_submission_approved
category: Form Builder
---

# Email Template: form_submission_approved

## Subject
✓ تم تأكيد {{ form_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ تمت الموافقة!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          أخبار جيدة!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم تأكيد إرسال {{ form_name }}!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الإرسال:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>نموذج:</strong> {{ form_name }}<br/>
              <strong>تم الإرسال:</strong> {{ submission_date }}<br/>
              <strong>تمت الموافقة:</strong> {{ approval_date }}<br/>
              <strong>رقم المراجع:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if approval_message %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          رسالة من فريقنا:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ approval_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ماذا يحدث بعد ذلك؟
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>

        <mj-spacer height="30px" />

        {% if cta_url %}
        <mj-button href="{{ cta_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          {{ cta_text|default:'View Details' }}
        </mj-button>
        {% endif %}

        {% if support_url %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          هل لديك أسئلة؟ <a href="{{ support_url }}">اتصل بالدعم</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ تمت الموافقة!

أخبار جيدة!

Hi {{ submitter_name }},

تم تأكيد إرسال {{ form_name }}!

تفاصيل الإرسال:
- نموذج: {{ form_name }}
- تم الإرسال: {{ submission_date }}
- تمت الموافقة: {{ approval_date }}
- رقم المراجع: {{ submission_id }}

{% if approval_message %}
رسالة من فريقنا:
{{ approval_message }}
{% endif %}

ماذا يحدث بعد ذلك؟
{{ next_steps }}

{% if cta_url %}{{ cta_text|default:'View Details' }}: {{ cta_url }}{% endif %}

{% if support_url %}هل لديك أسئلة؟ اتصل بالدعم: {{ support_url }}{% endif %}