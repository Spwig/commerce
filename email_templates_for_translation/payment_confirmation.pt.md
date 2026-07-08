---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Pagamento Confirmado - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Pagamento Confirmado
        </mj-text>
        <mj-text>
          Seu pagamento para o pedido #{{ order_number }} foi processado com sucesso.
        </mj-text>
        <mj-text>
          <strong>Valor Pago:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Método de Pagamento:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pagamento Confirmado

Seu pagamento para o pedido #{{ order_number }} foi processado com sucesso.

Valor Pago: {{ amount_paid }}
Método de Pagamento: {{ payment_method }}