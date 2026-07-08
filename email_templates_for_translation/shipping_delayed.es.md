---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Actualización de su pedido #{{ order_number }} - Retraso en la entrega

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actualización de su Pedido
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Queremos informarle sobre un retraso en su pedido. Nos disculpamos por la molestia y agradecemos su paciencia.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del Pedido:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número de Pedido:</strong> {{ order_number }}<br/>
              <strong>Fecha de Entrega Original:</strong> {{ original_delivery_date }}<br/>
              <strong>Nueva Fecha de Entrega:</strong> {{ new_delivery_date }}<br/>
              <strong>Número de Seguimiento:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Motivo del Retraso:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear su Pedido
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Estamos trabajando arduamente para entregar su pedido lo más rápido posible. Recibirá otra actualización cuando su paquete esté en camino.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿Tiene preguntas? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contáctenos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Actualización de su Pedido #{{ order_number }}

Hola {{ customer_name }},

Queremos informarle sobre un retraso en su pedido. Nos disculpamos por la molestia y agradecemos su paciencia.

DETALLES DEL PEDIDO:
- Número de Pedido: {{ order_number }}
- Fecha de Entrega Original: {{ original_delivery_date }}
- Nueva Fecha de Entrega: {{ new_delivery_date }}
- Número de Seguimiento: {{ tracking_number }}

MOTIVO DEL RETRASO:
{{ delay_reason }}

Rastrear su pedido: {{ tracking_url }}

Estamos trabajando arduamente para entregar su pedido lo más rápido posible. Recibirá otra actualización cuando su paquete esté en camino.

¿Tiene preguntas? Contáctenos: {{ support_url }}

---
Esta actualización es para el pedido #{{ order_number }} en {{ shop_name }}.