---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
تحديث على استمارة {{ form_name }} الخاصة بك

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تحديث على استمارة التقديم الخاصة بك
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          شكرًا لتقديمك استمارة {{ form_name }}. بعد مراجعة دقيقة، لا يمكننا الموافقة على استمارة التقديم الخاصة بك في الوقت الحالي.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل التقديم:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>نموذج:</strong> {{ form_name }}<br/>
              <strong>تم التقديم:</strong> {{ submission_date }}<br/>
              <strong>تم المراجعة:</strong> {{ rejection_date }}<br/>
              <strong>رقم المراجع:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          السبب:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if can_resubmit %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              يمكنك إعادة التقديم
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ resubmit_instructions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if resubmit_url %}
        <mj-button href="{{ resubmit_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          أرسل مرة أخرى
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          تواصل مع الدعم
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          إذا كانت لديك أسئلة حول هذا القرار، فلا تتردد في التواصل معنا.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تحديث على استمارة التقديم الخاصة بك

مرحباً {{ submitter_name }},

شكرًا لتقديمك استمارة {{ form_name }}. بعد مراجعة دقيقة، لا يمكننا الموافقة على استمارة التقديم الخاصة بك في الوقت الحالي.

تفاصيل التقديم:
- نموذج: {{ form_name }}
- تم التقديم: {{ submission_date }}
- تم المراجعة: {{ rejection_date }}
- رقم المراجع: {{ submission_id }}

{% if rejection_reason %}
السبب:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
يمكنك إعادة التقديم:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}أرسل مرة أخرى: {{ resubmit_url }}{% endif %}
{% if support_url %}تواصل مع الدعم: {{ support_url }}{% endif %}

إذا كانت لديك أسئلة حول هذا القرار، فلا تتردد في التواصل معنا.