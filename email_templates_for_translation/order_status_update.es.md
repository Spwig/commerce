---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
Orden #{{ order_number }} - Actualización de estado: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actualización del estado de la orden
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
          Orden #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          El estado de su orden <strong>#{{ order_number }}</strong> ha sido actualizado.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Estado anterior:</strong> {{ old_status_display }}<br/>
              <strong>Nuevo estado:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver detalles de la orden
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Actualización del estado de la orden - Orden #{{ order_number }}

Hola {{ customer_name }},

El estado de su orden #{{ order_number }} ha sido actualizado.

Estado anterior: {{ old_status_display }}
Nuevo estado: {{ new_status_display }}

{% if order_url %}Ver detalles de la orden: {{ order_url }}{% endif %}