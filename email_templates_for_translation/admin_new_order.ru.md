---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
Получен новый заказ - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Получен новый заказ
        </mj-text>
        <mj-text>
          На ваш магазин был сделан новый заказ.
        </mj-text>
        <mj-text>
          <strong>Номер заказа:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Клиент:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Итого:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Просмотреть в админке
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Получен новый заказ

На ваш магазин был сделан новый заказ.

Номер заказа: {{ order_number }}
Клиент: {{ customer_name }}
Итого: {{ order_total }}

Просмотреть в админке: {{ admin_order_url }}