---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Reembolso procesado - Orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Reembolso procesado
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
          Su devolución para la orden <strong>#{{ order_number }}</strong> ha sido revisada y su reembolso ha sido procesado.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Detalles del reembolso
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Monto del reembolso:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Fee de reposición:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Nota:</strong> Puede tomar 5-10 días hábiles para que el reembolso aparezca en su cuenta, dependiendo de su proveedor de pago.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Si tiene alguna pregunta sobre su reembolso, por favor contacte a nuestro equipo de soporte.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Reembolso procesado - Orden #{{ order_number }}

Hola {{ customer_name }},

Su devolución para la orden #{{ order_number }} ha sido revisada y su reembolso ha sido procesado.

Detalles del reembolso:
- Monto del reembolso: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Fee de reposición: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Nota: Puede tomar 5-10 días hábiles para que el reembolso aparezca en su cuenta, dependiendo de su proveedor de pago.

Si tiene alguna pregunta sobre su reembolso, por favor contacte a nuestro equipo de soporte.