---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Tu pedido #{{ order_number }} está {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actualización de Envío: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ¡Buena noticia! Tu pedido ha alcanzado un hito importante en su viaje hacia ti.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del Pedido:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número de Pedido:</strong> {{ order_number }}<br/>
              <strong>Número de Seguimiento:</strong> {{ tracking_number }}<br/>
              <strong>Transportista:</strong> {{ carrier_name }}<br/>
              <strong>Ubicación Actual:</strong> {{ current_location }}<br/>
              <strong>Entrega Estimada:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear tu Paquete
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿Tienes preguntas sobre tu envío? <a href="{{ support_url }.json">Contactar Soporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Actualización de Envío: {{ milestone_status }}

Hola {{ customer_name }},

¡Buena noticia! Tu pedido ha alcanzado un hito importante en su viaje hacia ti.

📦 {{ milestone_status }}
{{ milestone_description }}

DETALLES DEL PEDIDO:
- Número de Pedido: {{ order_number }}
- Número de Seguimiento: {{ tracking_number }}
- Transportista: {{ carrier_name }}
- Ubicación Actual: {{ current_location }}
- Entrega Estimada: {{ estimated_delivery }}

Rastrear tu paquete: {{ tracking_url }}

¿Tienes preguntas sobre tu envío? Contactar Soporte: {{ support_url }}