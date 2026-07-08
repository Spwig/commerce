---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Возврат обработан - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Возврат обработан
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
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
          Ваш возврат по заказу <strong>#{{ order_number }}</strong> был проверен, и возврат средств был обработан.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Детали возврата
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Сумма возврата:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Плата за возврат:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Примечание:</strong> Возврат может отразиться на вашем счете в течение 5–10 рабочих дней, в зависимости от вашего платежного провайдера.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Если у вас есть вопросы относительно вашего возврата, пожалуйста, свяжитесь с нашей службой поддержки.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Возврат обработан - Заказ #{{ order_number }}

Здравствуйте, {{ customer_name }},

Ваш возврат по заказу #{{ order_number }} был проверен, и возврат средств был обработан.

Детали возврата:
- Сумма возврата: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Плата за возврат: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Примечание: Возврат может отразиться на вашем счете в течение 5–10 рабочих дней, в зависимости от вашего платежного провайдера.

Если у вас есть вопросы относительно вашего возврата, пожалуйста, свяжитесь с нашей службой поддержки.