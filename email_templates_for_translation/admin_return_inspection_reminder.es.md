---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
Paquete devuelto - Se requiere inspección para la orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Se requiere inspección de devolución
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se ha recibido un paquete de devolución y requiere inspección.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Orden:</strong> #{{ order_number }}<br/>
              <strong>Recibido:</strong> {{ received_at }}<br/>
              <strong>Elementos para inspeccionar:</strong> {{ items_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if admin_url %}
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver devolución en el administrador
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Se requiere inspección de devolución

Se ha recibido un paquete de devolución y requiere inspección.

Orden: #{{ order_number }}
Recibido: {{ received_at }}
Elementos para inspeccionar: {{ items_count }}

{% if admin_url %}Ver en el administrador: {{ admin_url }}{% endif %}