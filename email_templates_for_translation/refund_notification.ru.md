---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Возврат обработан - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Возврат обработан
        </mj-text>
        <mj-text>
          Возврат был обработан для заказа #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Сумма возврата:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          Возврат появится на вашем счете в течение {{ refund_days }} рабочих дней.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Возврат обработан

Возврат был обработан для заказа #{{ order_number }}.

Сумма возврата: {{ refund_amount }}

Возврат появится на вашем счете в течение {{ refund_days }} рабочих дней.