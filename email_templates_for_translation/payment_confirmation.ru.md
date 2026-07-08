---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Оплата подтверждена - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Оплата подтверждена
        </mj-text>
        <mj-text>
          Ваша оплата за заказ #{{ order_number }} была успешно обработана.
        </mj-text>
        <mj-text>
          <strong>Сумма оплаты:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Способ оплаты:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Оплата подтверждена

Ваша оплата за заказ #{{ order_number }} была успешно обработана.

Сумма оплаты: {{ amount_paid }}
Способ оплаты: {{ payment_method }}