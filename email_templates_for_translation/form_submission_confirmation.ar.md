---
template_type: form_submission_confirmation
category: Form Builder
---

# Email Template: form_submission_confirmation

## Subject
✓ تلقيتنا استمارة {{ form_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ تلقي الاستمارة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          شكرًا!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحبًا {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          شكرًا لتقديمك استمارة {{ form_name }}. تلقينا معلوماتك وسنعود إليك قريبًا.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الاستمارة:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>نموذج:</strong> {{ form_name }}<br/>
              <strong>تم الإرسال:</strong> {{ submission_date }}<br/>
              <strong>رقم المرجع:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ماذا يحدث بعد ذلك؟
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>

        {% if expected_response_time %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 الوقت المعتاد للرد: {{ expected_response_time }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if submission_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          استمارةك:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for field in submission_data %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ field.label }}:</strong> {{ field.value }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if support_url %}
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          هل لديك أسئلة؟ <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">اتصل بالدعم</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ تلقي الاستمارة

شكرًا!

مرحبًا {{ submitter_name }},

شكرًا لتقديمك استمارة {{ form_name }}. تلقينا معلوماتك وسنعود إليك قريبًا.

تفاصيل الاستمارة:
- نموذج: {{ form_name }}
- تم الإرسال: {{ submission_date }}
- رقم المرجع: {{ submission_id }}

ماذا يحدث بعد ذلك؟
{{ next_steps }}

{% if expected_response_time %}💡 الوقت المعتاد للرد: {{ expected_response_time }}{% endif %}

{% if submission_data %}استمارةك:
{% for field in submission_data %}{{ field.label }}: {{ field.value }}
{% endfor %}{% endif %}

{% if support_url %}هل لديك أسئلة؟ اتصل بالدعم: {{ support_url }}{% endif %}