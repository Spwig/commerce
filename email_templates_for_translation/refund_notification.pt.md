---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Reembolso Processado - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Reembolso Processado
        </mj-text>
        <mj-text>
          Um reembolso foi processado para o pedido #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Valor do Reembolso:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          O reembolso aparecerá em sua conta dentro de {{ refund_days }} dias úteis.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Reembolso Processado

Um reembolso foi processado para o pedido #{{ order_number }}.

Valor do Reembolso: {{ refund_amount }}

O reembolso aparecerá em sua conta dentro de {{ refund_days }} dias úteis.