---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
Ваш заказ №{{ order_number }} отправлен!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 Заказ отправлен!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          В пути!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Великолепные новости! Ваш заказ отправлен и уже в пути к вам.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали доставки:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Order #:</strong> {{ order_number }}<br/>
              <strong>Tracking #:</strong> {{ tracking_number }}<br/>
              <strong>Carrier:</strong> {{ carrier_name }}<br/>
              <strong>Est. Delivery:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Отслеживать посылку
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 ЗАКАЗ ОТПРАВЛЕН!

В ПУТИ!

Здравствуйте, {{ customer_name }},

Великолепные новости! Ваш заказ отправлен и уже в пути к вам.

ДЕТАЛИ ДОСТАВКИ:
- Заказ №: {{ order_number }}
- Номер отслеживания: {{ tracking_number }}
- Перевозчик: {{ carrier_name }}
- Ожидаемая доставка: {{ estimated_delivery }}

Отслеживать посылку: {{ tracking_url }}