---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
Заказ доставлен - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Заказ доставлен
        </mj-text>
        <mj-text>
          Ваш заказ #{{ order_number }} был доставлен!
        </mj-text>
        <mj-text>
          Мы надеемся, что вам понравился ваш покупка. Если у вас есть какие-либо вопросы или опасения, пожалуйста, не стесняйтесь обращаться к нам.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Просмотр заказа
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Заказ доставлен

Ваш заказ #{{ order_number }} был доставлен!

Мы надеемся, что вам понравился ваш покупка. Если у вас есть какие-либо вопросы или опасения, пожалуйста, не стесняйтесь обращаться к нам.

Просмотр заказа: {{ order_url }}