---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Ошибка перевода: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Ошибка задания перевода
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ошибка перевода
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваша пакетная задача перевода столкнулась с ошибкой и не может быть завершена.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали задания:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Target Languages:</strong> {{ target_languages }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Error Code:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Сообщение об ошибке:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Частичное завершение
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} из {{ total_items }} элементов были успешно переведены до возникновения ошибки.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Общие причины:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Проблемы с подключением к API сервиса перевода<br/>
          • Недостаточно кредитов для перевода<br/>
          • Недопустимый или поврежденный исходный контент<br/>
          • Неподдерживаемая пара языков
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемые действия:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Проверьте настройки сервиса перевода<br/>
          2. Убедитесь, что доступны кредиты для перевода<br/>
          3. Изучите сообщение об ошибке, чтобы определить конкретные проблемы<br/>
          4. Повторите задание перевода
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Повторить перевод
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Проверить настройки
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Если проблема сохраняется, свяжитесь с поддержкой, указав код ошибки {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ ОШИБКА ПЕРЕВОДА

Ошибка перевода

Ваша пакетная задача перевода столкнулась с ошибкой и не может быть завершена.

ДЕТАЛИ ЗАДАНИЯ:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Target Languages: {{ target_languages }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

СООБЩЕНИЕ ОБ ОШИБКЕ:
{{ error_message }}

{% if partial_completion %}
ЧАСТИЧНОЕ ЗАВЕРШЕНИЕ:
{{ items_completed }} из {{ total_items }} элементов были успешно переведены до возникновения ошибки.
{% endif %}

ОБЩИЕ ПРИЧИНЫ:
• Проблемы с подключением к API сервиса перевода
• Недостаточно кредитов для перевода
• Недопустимый или поврежденный исходный контент
• Неподдерживаемая пара языков

РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:
1. Проверьте настройки сервиса перевода
2. Убедитесь, что доступны кредиты для перевода
3. Изучите сообщение об ошибке, чтобы определить конкретные проблемы
4. Повторите задание перевода

Повторить перевод: {{ retry_url }}
Проверить настройки: {{ settings_url }}

Если проблема сохраняется, свяжитесь с поддержкой, указав код ошибки {{ error_code }}.