---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Обновление запроса на возврат - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Обновление запроса на возврат
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          Мы рассмотрели ваш запрос на возврат для заказа <strong>#{{ order_number }}</strong> и на данный момент не можем его одобрить.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Причина:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Если у вас есть вопросы по этому решению или вы считаете, что произошла ошибка, пожалуйста, свяжитесь с нашей службой поддержки.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Обновление запроса на возврат - Заказ #{{ order_number }}

Здравствуйте, {{ customer_name }},

Мы рассмотрели ваш запрос на возврат для заказа #{{ order_number }} и на данный момент не можем его одобрить.

{% if rejection_reason %}Причина: {{ rejection_reason }}{% endif %}

Если у вас есть вопросы по этому решению или вы считаете, что произошла ошибка, пожалуйста, свяжитесь с нашей службой поддержки.