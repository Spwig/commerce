---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
Entregada la orden - Orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Entregada la orden
        </mj-text>
        <mj-text>
          Tu orden #{{ order_number }} ha sido entregada!
        </mj-text>
        <mj-text>
          Esperamos que disfrutes tu compra. Si tienes alguna pregunta o inquietud, no dudes en contactarnos.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Ver orden
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Entregada la orden

Tu orden #{{ order_number }} ha sido entregada!

Esperamos que disfrutes tu compra. Si tienes alguna pregunta o inquietud, no dudes en contactarnos.

Ver orden: {{ order_url }}

