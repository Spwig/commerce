---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Получен запрос на возврат - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Получен запрос на возврат
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          Заказ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Мы получили ваш запрос на возврат для заказа <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали возврата:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Причина:</strong> {{ return_reason }}<br/>
              <strong>Товары:</strong> {{ items_count }} товар(а/ов)<br/>
              <strong>Статус:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что происходит далее?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Наша команда рассмотрит ваш запрос на возврат в течение 24–48 часов<br/>
          2. После одобрения мы отправим вам этикетку для возврата по электронной почте<br/>
          3. Упакуйте товары и прикрепите этикетку возврата<br/>
          4. Отвезите посылку в ближайшее отделение доставки<br/>
          5. Возврат средств будет обработан после получения и проверки товаров
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Если у вас есть вопросы, пожалуйста, не стесняйтесь обращаться к нам.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ПОЛУЧЕН ЗАПРОС НА ВОЗВРАТ
Заказ #{{ order_number }}

Здравствуйте, {{ customer_name }},

Мы получили ваш запрос на возврат для заказа #{{ order_number }}.

ДЕТАЛИ ВОЗВРАТА:
- Причина: {{ return_reason }}
- Товары: {{ items_count }} товар(а/ов)
- Статус: {{ return_status }}

ЧТО ПРОИСХОДИТ ДАЛЕЕ?
1. Наша команда рассмотрит ваш запрос на возврат в течение 24–48 часов
2. После одобрения мы отправим вам этикетку для возврата по электронной почте
3. Упакуйте товары и прикрепите этикетку возврата
4. Отвезите посылку в ближайшее отделение доставки
5. Возврат средств будет обработан после получения и проверки товаров

Если у вас есть вопросы, пожалуйста, не стесняйтесь обращаться к нам.