---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ Не удалось создать фид: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Не удалось создать фид
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ошибка генерации
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Фид {{ feed_name }} не удалось создать из-за ошибки.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали ошибки:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
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

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Ошибка в логах:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:30 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Частые причины:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Отсутствуют обязательные данные о товаре (название, цена, изображение)<br/>
          • Неверный формат данных о товаре<br/>
          • Проблемы с подключением к базе данных<br/>
          • Недостаточно места на диске или памяти
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Повторить генерацию
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть настройки фида
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
❌ НЕ УДАЛОСЬ СОЗДАТЬ ФИД

Ошибка генерации

Фид {{ feed_name }} не удалось создать из-за ошибки.

ДЕТАЛИ ОШИБКИ:
- Фид: {{ feed_name }}
- Сбой произошел: {{ failed_at }}
- Код ошибки: {{ error_code }}

СООБЩЕНИЕ ОБ ОШИБКЕ:
{{ error_message }}

{% if error_log %}
ЛОГ ОШИБКИ:
{{ error_log|truncatewords:30 }}
{% endif %}

ЧАСТЫЕ ПРИЧИНЫ:
• Отсутствуют обязательные данные о товаре (название, цена, изображение)
• Неверный формат данных о товаре
• Проблемы с подключением к базе данных
• Недостаточно места на диске или памяти

Повторить генерацию: {{ retry_url }}
Просмотреть настройки фида: {{ admin_feed_url }}

Если проблема сохраняется, свяжитесь с поддержкой, указав код ошибки {{ error_code }}.