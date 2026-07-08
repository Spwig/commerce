---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Tu pedido ha sido enviado - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Tu pedido ha sido enviado!
        </mj-text>
        <mj-text>
          ¡Buena noticia! Tu pedido #{{ order_number }} ha sido enviado.
        </mj-text>
        <mj-text>
          <strong>Número de seguimiento:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Transportista:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Seguir envío
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Tu pedido ha sido enviado!

¡Buena noticia! Tu pedido #{{ order_number }} ha sido enviado.

Número de seguimiento: {{ tracking_number }}
Transportista: {{ carrier }}

Seguir tu envío: {{ tracking_url }}
