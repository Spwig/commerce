---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Reembolso procesado - Orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Reembolso procesado
        </mj-text>
        <mj-text>
          Se ha procesado un reembolso para la orden #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Cantidad del reembolso:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          El reembolso aparecerá en su cuenta dentro de {{ refund_days }} días hábiles.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Reembolso procesado

Se ha procesado un reembolso para la orden #{{ order_number }}.

Cantidad del reembolso: {{ refund_amount }}

El reembolso aparecerá en su cuenta dentro de {{ refund_days }} días hábiles.