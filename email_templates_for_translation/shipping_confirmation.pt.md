---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
Seu Pedido Foi Enviado - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Seu Pedido Foi Enviado!
        </mj-text>
        <mj-text>
          Boa notícia! Seu pedido #{{ order_number }} foi enviado.
        </mj-text>
        <mj-text>
          <strong>Número de Rastreamento:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>Transportadora:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Rastrear Envio
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Seu Pedido Foi Enviado!

Boa notícia! Seu pedido #{{ order_number }} foi enviado.

Número de Rastreamento: {{ tracking_number }}
Transportadora: {{ carrier }}

Rastrear seu envio: {{ tracking_url }}