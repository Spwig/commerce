---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Ваш заказ отправлен - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Ваш заказ отправлен!
        </mj-text>
        <mj-text>
          Отличные новости! Ваш заказ #{{ order_number }} был отправлен.
        </mj-text>
        <mj-text>
          <strong>Номер отслеживания:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Поставщик:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Отслежить поставку
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ваш заказ отправлен!

Отличные новости! Ваш заказ #{{ order_number }} был отправлен.

Номер отслеживания: {{ tracking_number }}
Поставщик: {{ carrier }}

Отслежить поставку: {{ tracking_url }}

Спасибо, что выбрали Spwig!