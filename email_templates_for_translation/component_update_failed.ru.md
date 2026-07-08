---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Не удалось обновить: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Не удалось обновить
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ошибка установки
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Обновление {{ component_name }} до версии {{ target_version }} не удалось установить.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали ошибки:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Компонент:</strong> {{ component_name }}<br/>
              <strong>Целевая версия:</strong> {{ target_version }}<br/>
              <strong>Ошибка произошла:</strong> {{ failed_at }}<br/>
              <strong>Код ошибки:</strong> {{ error_code }}
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
          <strong>Полный журнал ошибок:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что делать:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Проверьте системные требования и зависимости<br/>
          2. Изучите журнал ошибок для получения подробной информации<br/>
          3. Попробуйте установить снова или обратитесь в службу поддержки<br/>
          4. Ваш магазин всё ещё работает на {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Повторить установку
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Обратиться в службу поддержки
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ ОБНОВЛЕНИЕ ПРОШЛО НЕУДАЧНО

Ошибка установки

Обновление {{ component_name }} до версии {{ target_version }} не удалось установить.

ДЕТАЛИ ОШИБКИ:
- Компонент: {{ component_name }}
- Целевая версия: {{ target_version }}
- Ошибка произошла: {{ failed_at }}
- Код ошибки: {{ error_code }}

СООБЩЕНИЕ ОБ ОШИБКЕ:
{{ error_message }}

{% if error_log %}
ПОЛНЫЙ ЖУРНАЛ ОШИБОК:
{{ error_log|truncatewords:50 }}
{% endif %}

ЧТО ДЕЛАТЬ:
1. Проверьте системные требования и зависимости
2. Изучите журнал ошибок для получения подробной информации
3. Попробуйте установить снова или обратитесь в службу поддержки
4. Ваш магазин всё ещё работает на {{ current_version }}

Повторить установку: {{ retry_url }}
Обратиться в службу поддержки: {{ support_url }}
