---
template_type: form_submission_approved
category: Form Builder
---

# Email Template: form_submission_approved

## Subject
✓ Ваша {{ form_name }} была одобрена!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Одобрено!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Великолепные новости!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваша {{ form_name }} была одобрена!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали подачи:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Форма:</strong> {{ form_name }}<br/>
              <strong>Подана:</strong> {{ submission_date }}<br/>
              <strong>Одобрена:</strong> {{ approval_date }}<br/>
              <strong>Номер ссылки:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if approval_message %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Сообщение от нашей команды:
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
          Что происходит дальше?
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
          Вопросы? <a href="{{ support_url }}">Связаться с поддержкой</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ОДОБРЕНО!

Великолепные новости!

Здравствуйте {{ submitter_name }},

Ваша {{ form_name }} была одобрена!

ДЕТАЛИ ПОДАЧИ:
- Форма: {{ form_name }}
- Подана: {{ submission_date }}
- Одобрена: {{ approval_date }}
- Номер ссылки: {{ submission_id }}

{% if approval_message %}
СООБЩЕНИЕ ОТ НАШЕЙ КОМАНДЫ:
{{ approval_message }}
{% endif %}

ЧТО ПРОИСХОДИТ ДАЛЕЕ?
{{ next_steps }}

{% if cta_url %}{{ cta_text|default:'View Details' }}: {{ cta_url }}{% endif %}

{% if support_url %}Вопросы? Связаться с поддержкой: {{ support_url }}{% endif %}