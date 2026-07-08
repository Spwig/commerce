---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
Ваш заказ №{{ order_number }} был отменён

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Заказ отменён
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваш заказ <strong>#{{ order_number }}</strong> был отменён.
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Причина:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Если была произведена оплата, возврат средств будет обработан в соответствии с первоначальным способом оплаты.
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть детали заказа
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Заказ отменён

Здравствуйте, {{ customer_name }},

Ваш заказ #{{ order_number }} был отменён.

{% if cancellation_reason %}Причина: {{ cancellation_reason }}{% endif %}

Если была произведена оплата, возврат средств будет обработан в соответствии с первоначальным способом оплаты.

{% if order_url %}Просмотреть детали заказа: {{ order_url }}{% endif %}

Вопросы по этой отмене?
Электронная почта: {{ support_email }}
Телефон: {{ support_phone }}