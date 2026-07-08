---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Ваш заказ №{{ order_number }} находится на этапе {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обновление доставки: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Хорошие новости! Ваш заказ достиг важного этапа на пути к вам.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали заказа:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Номер заказа:</strong> {{ order_number }}<br/>
              <strong>Номер отслеживания:</strong> {{ tracking_number }}<br/>
              <strong>Поставщик:</strong> {{ carrier_name }}<br/>
              <strong>Текущее место нахождения:</strong> {{ current_location }}<br/>
              <strong>Ожидаемая доставка:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Отслеживать вашу посылку
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Вопросы по доставке? <a href="{{ support_url }.json">Связаться с поддержкой</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Обновление доставки: {{ milestone_status }}

Здравствуйте, {{ customer_name }},

Хорошие новости! Ваш заказ достиг важного этапа на пути к вам.

📦 {{ milestone_status }}
{{ milestone_description }}

ДЕТАЛИ ЗАКАЗА:
- Номер заказа: {{ order_number }}
- Номер отслеживания: {{ tracking_number }}
- Поставщик: {{ carrier_name }}
- Текущее место нахождения: {{ current_location }}
- Ожидаемая доставка: {{ estimated_delivery }}

Отслеживать вашу посылку: {{ tracking_url }}

Вопросы по доставке? Связаться с поддержкой: {{ support_url }}