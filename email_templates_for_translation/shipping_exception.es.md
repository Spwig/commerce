---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Excepción de envío - El pedido #{{ order_number }} requiere atención

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Excepción de envío
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Estamos escribiendo para informarle sobre una excepción con su envío. Estamos trabajando para resolver este problema lo más pronto posible.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Detalles de la excepción:
            </mj-text>
            <mj-text color="#92400e">
              <strong>Tipo de excepción:</strong> {{ exception_type }}<br/>
              <strong>Descripción:</strong> {{ exception_description }}<br/>
              <strong>Ocurrido:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Información del pedido:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número de pedido:</strong> {{ order_number }}<br/>
              <strong>Número de seguimiento:</strong> {{ tracking_number }}<br/>
              <strong>Transportista:</strong> {{ carrier_name }}<br/>
              <strong>Ubicación actual:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué sucede a continuación?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Acción requerida:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear su pedido
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contactar soporte
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ EXCEPCIÓN DE ENVÍO

Hola {{ customer_name }},

Estamos escribiendo para informarle sobre una excepción con su envío. Estamos trabajando para resolver este problema lo más pronto posible.

DETALLES DE LA EXCEPCIÓN:
- Tipo de excepción: {{ exception_type }}
- Descripción: {{ exception_description }}
- Ocurrido: {{ exception_date }}

INFORMACIÓN DEL PEDIDO:
- Número de pedido: {{ order_number }}
- Número de seguimiento: {{ tracking_number }}
- Transportista: {{ carrier_name }}
- Ubicación actual: {{ current_location }}

¿QUÉ SUCEDERÁ A CONTINUACIÓN?
{{ resolution_steps }}

{% if action_required %}
⚠️ ACCIÓN REQUERIDA:
{{ action_required_description }}
{% endif %}

Rastrear su pedido: {{ tracking_url }}
Contactar soporte: {{ support_url }}