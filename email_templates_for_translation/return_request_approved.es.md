---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Su devolución ha sido aprobada - Orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Devolución aprobada
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
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
          Su solicitud de devolución para la orden <strong>#{{ order_number }}</strong> ha sido aprobada.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Pasos siguientes:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Descargue e imprima la etiqueta de devolución a continuación<br/>
          2. Empaque los artículos de forma segura en su empaque original si es posible<br/>
          3. Adjunte la etiqueta de devolución al exterior del paquete<br/>
          4. Deje el paquete en la ubicación de envío más cercana
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Descargar etiqueta de devolución
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Número de seguimiento de devolución:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Importante:</strong> Por favor, envíe la devolución dentro de los 7 días para garantizar el procesamiento rápido de su reembolso.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Una vez que recibamos e inspeccionemos su devolución, procesaremos su reembolso al método de pago original.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Deshabilitado - Orden #{{ order_number }}

Hola {{ customer_name }},

Su solicitud de devolución para la orden #{{ order_number }} ha sido aprobada.

Pasos siguientes:
1. Descargue e imprima la etiqueta de devolución
2. Empaque los artículos de forma segura en su empaque original si es posible
3. Adjunte la etiqueta de devolución al exterior del paquete
4. Deje el paquete en la ubicación de envío más cercana

{% if return_label_url %}Descargue su etiqueta de devolución: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Número de seguimiento de devolución: {{ return_tracking_number }}{% endif %}

Importante: Por favor, envíe la devolución dentro de los 7 días para garantizar el procesamiento rápido de su reembolso.

Una vez que recibamos e inspeccionemos su devolución, procesaremos su reembolso al método de pago original.