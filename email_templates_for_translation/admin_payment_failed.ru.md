---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
Ошибка оплаты - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          Ошибка оплаты
        </mj-text>
        <mj-text>
          Попытка оплаты для заказа #{{ order_number }} завершилась неудачей.
        </mj-text>
        <mj-text>
          <strong>Клиент:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Сумма:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Ошибка:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          Просмотреть в админ-панели
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ошибка оплаты

Попытка оплаты для заказа #{{ order_number }} завершилась неудачей.

Клиент: {{ customer_name }}
Сумма: {{ order_total }}
Ошибка: {{ error_message }}

Просмотреть в админ-панели: {{ admin_order_url }}