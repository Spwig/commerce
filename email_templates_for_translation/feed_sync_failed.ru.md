---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ Синхронизация {{ feed_name }} с {{ platform_name }} завершилась неудачно

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Синхронизация не удалась
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ошибка синхронизации
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Не удалось синхронизировать {{ feed_name }} с {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали сбоя:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Общие причины:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Неверные учетные данные API или истекший токен<br/>
          • Проблемы с подключением к сети<br/>
          • Превышение лимитов API платформы<br/>
          • Формат Feed не соответствует требованиям платформы
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Рекомендуемое действие
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Повторить синхронизацию
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Проверить настройки Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ СИНХРОНИЗАЦИЯ НЕ УДАЛСЯ

Ошибка синхронизации

Не удалось синхронизировать {{ feed_name }} с {{ platform_name }}.

ДЕТАЛИ СБОЯ:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

СООБЩЕНИЕ ОБ ОШИБКЕ:
{{ error_message }}

ОБЩИЕ ПРИЧИНЫ:
• Неверные учетные данные API или истекший токен
• Проблемы с подключением к сети
• Превышение лимитов API платформы
• Формат Feed не соответствует требованиям платформы

{% if recommended_action %}
РЕКОМЕНДУЕМОЕ ДЕЙСТВИЕ:
{{ recommended_action }}
{% endif %}

Повторить синхронизацию: {{ retry_url }}
Проверить настройки Feed: {{ admin_feed_url }}