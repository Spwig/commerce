---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
Tu pedido #{{ order_number }} ha salido!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 Pedido Enviado!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          En Camino!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ¡Buena noticia! Tu pedido ha salido y está en camino hacia ti.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles de Envío:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número de Pedido:</strong> {{ order_number }}<br/>
              <strong>Número de Seguimiento:</strong> {{ tracking_number }}<br/>
              <strong>Transportista:</strong> {{ carrier_name }}<br/>
              <strong>Est. Entrega:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear tu Paquete
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 PEDIDO ENVIADO!

En Camino!

Hola {{ customer_name }},

¡Buena noticia! Tu pedido ha salido y está en camino hacia ti.

DETALLES DE ENVÍO:
- Número de Pedido: {{ order_number }}
- Número de Seguimiento: {{ tracking_number }}
- Transportista: {{ carrier_name }}
- Est. Entrega: {{ estimated_delivery }}

Rastrear tu paquete: {{ tracking_url }}