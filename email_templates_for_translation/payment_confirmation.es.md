---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Pago confirmado - Orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Pago confirmado
        </mj-text>
        <mj-text>
          Su pago para la orden #{{ order_number }} ha sido procesado con éxito.
        </mj-text>
        <mj-text>
          <strong>Monto Pagado:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Método de Pago:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pago confirmado

Su pago para la orden #{{ order_number }} ha sido procesado con éxito.

Monto Pagado: {{ amount_paid }}
Método de Pago: {{ payment_method }}