---
template_type: form_submission_confirmation
category: Form Builder
---

# Email Template: form_submission_confirmation

## Subject
✓ Получена ваша отправка {{ form_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ Получена отправка
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Спасибо!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Спасибо за отправку формы {{ form_name }}. Мы получили ваши данные и скоро свяжемся с вами.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали отправки:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Форма:</strong> {{ form_name }}<br/>
              <strong>Отправлено:</strong> {{ submission_date }}<br/>
              <strong>Номер ссылки:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что происходит далее?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>

        {% if expected_response_time %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Типичное время ответа: {{ expected_response_time }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if submission_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ваша отправка:
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
          Вопросы? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Связаться с поддержкой</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ Получена отправка

Спасибо!

Здравствуйте {{ submitter_name }},

Спасибо за отправку формы {{ form_name }}. Мы получили ваши данные и скоро свяжемся с вами.

ДЕТАЛИ ОТПРАВКИ:
- Форма: {{ form_name }}
- Отправлено: {{ submission_date }}
- Номер ссылки: {{ submission_id }}

ЧТО ПРОИСХОДИТ ДАЛЕЕ?
{{ next_steps }}

{% if expected_response_time %}💡 Типичное время ответа: {{ expected_response_time }}{% endif %}

{% if submission_data %}ВАША ОТПРАВКА:
{% for field in submission_data %}{{ field.label }}: {{ field.value }}
{% endfor %}
{% endif %}

{% if support_url %}Вопросы? Связаться с поддержкой: {{ support_url }}{% endif %}