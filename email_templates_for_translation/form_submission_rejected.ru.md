---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
Обновление о вашей {{ form_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обновление о вашей подаче
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Спасибо, что отправили форму {{ form_name }}. После тщательного рассмотрения мы не можем одобрить вашу подачу в данный момент.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали подачи:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Форма:</strong> {{ form_name }}<br/>
              <strong>Отправлено:</strong> {{ submission_date }}<br/>
              <strong>Проверено:</strong> {{ rejection_date }}<br/>
              <strong>Номер ссылки:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Причина:
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
              Вы можете повторно подать заявку
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
          Повторно подать заявку
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Связаться с поддержкой
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Если у вас есть вопросы по поводу этого решения, пожалуйста, не стесняйтесь обращаться.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ОБНОВЛЕНИЕ О ВАШЕЙ ПОДАЧЕ

Здравствуйте, {{ submitter_name }},

Спасибо, что отправили форму {{ form_name }}. После тщательного рассмотрения мы не можем одобрить вашу подачу в данный момент.

ДЕТАЛИ ПОДАЧИ:
- Форма: {{ form_name }}
- Отправлено: {{ submission_date }}
- Проверено: {{ rejection_date }}
- Номер ссылки: {{ submission_id }}

{% if rejection_reason %}
ПРИЧИНА:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
ВЫ МОЖЕТЕ ПОВТОРНО ПОДАТЬ ЗАЯВКУ:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}Повторно подать заявку: {{ resubmit_url }}{% endif %}
{% if support_url %}Связаться с поддержкой: {{ support_url }}{% endif %}

Если у вас есть вопросы по поводу этого решения, пожалуйста, не стесняйтесь обращаться.