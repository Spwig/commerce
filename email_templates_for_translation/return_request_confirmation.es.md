---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Solicitud de devolución recibida - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Solicitud de devolución recibida
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          Pedido #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hemos recibido tu solicitud de devolución para el pedido <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles de la devolución:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Razón:</strong> {{ return_reason }}<br/>
              <strong>Artículos:</strong> {{ items_count }} item(s)<br/>
              <strong>Estado:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué sucede a continuación?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Nuestro equipo revisará tu solicitud de devolución dentro de 24-48 horas<br/>
          2. Una vez aprobada, te enviaremos una etiqueta de envío de devolución por correo electrónico<br/>
          3. Empaca los artículos de forma segura y adjunta la etiqueta de devolución<br/>
          4. Deja el paquete en la ubicación de envío más cercana<br/>
          5. Tu reembolso se procesará una vez que recibamos e inspeccionemos los artículos
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Si tienes alguna pregunta, no dudes en contactarnos.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
SOLICITUD DE DEVOLECIÓN RECIBIDA
Pedido #{{ order_number }}

Hola {{ customer_name }},

Hemos recibido tu solicitud de devolución para el pedido #{{ order_number }}.

DETALLES DE LA DEVOLECIÓN:
- Razón: {{ return_reason }}
- Artículos: {{ items_count }} item(s)
- Estado: {{ return_status }}

¿QUÉ SUCEDERÁ A CONTINUACIÓN?
1. Nuestro equipo revisará tu solicitud de devolución dentro de 24-48 horas
2. Una vez aprobada, te enviaremos una etiqueta de envío de devolución por correo electrónico
3. Empaca los artículos de forma segura y adjunta la etiqueta de devolución
4. Deja el paquete en la ubicación de envío más cercana
5. Tu reembolso se procesará una vez que recibamos e inspeccionemos los artículos

Si tienes alguna pregunta, no dudes en contactarnos.