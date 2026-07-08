---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Actualización de la solicitud de devolución - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Actualización de la solicitud de devolución
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          Hemos revisado su solicitud de devolución para el pedido <strong>#{{ order_number }}</strong> y no podemos aprobarla en este momento.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Razón:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Si tiene preguntas sobre esta decisión o cree que ha habido un error, por favor póngase en contacto con nuestro equipo de soporte.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Actualización de la solicitud de devolución - Pedido #{{ order_number }}

Hola {{ customer_name }},

Hemos revisado su solicitud de devolución para el pedido #{{ order_number }} y no podemos aprobarla en este momento.

{% if rejection_reason %}Razón: {{ rejection_reason }}{% endif %}

Si tiene preguntas sobre esta decisión o cree que ha habido un error, por favor póngase en contacto con nuestro equipo de soporte.