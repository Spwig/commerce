---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 Transacción de alto valor: {{ transaction_amount }} en {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 Transacción de alto valor
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Transacción procesada
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Se procesó una transacción de {{ transaction_amount }} en {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles de la transacción:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Cantidad:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cajero:</strong> {{ cashier_name }}<br/>
              <strong>Hora de registro:</strong> {{ transaction_time }}<br/>
              <strong>ID de transacción:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Información de pago:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumen de artículos:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total de artículos:</strong> {{ item_count }}<br/>
              <strong>Subtotal:</strong> {{ subtotal }}<br/>
              <strong>Impuesto:</strong> {{ tax_amount }}<br/>
              <strong>Total:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Información del cliente:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Esta notificación se envía para todas las transacciones que superan {{ threshold_amount }} con fines de prevención de fraude y monitoreo.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver transacción
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver recibo
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 TRANSACCIÓN DE ALTO VALOR

Transacción procesada

Se procesó una transacción de {{ transaction_amount }} en {{ terminal_name }}.

DETALLES DE LA TRANSACCIÓN:
- Cantidad: {{ transaction_amount }}
- Terminal: {{ terminal_name }}
- Cajero: {{ cashier_name }}
- Hora de registro: {{ transaction_time }}
- ID de transacción: {{ transaction_id }}

INFORMACIÓN DE PAGO:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

RESUMEN DE ARTÍCULOS:
- Total de artículos: {{ item_count }}
- Subtotal: {{ subtotal }}
- Impuesto: {{ tax_amount }}
- Total: {{ transaction_amount }}

{% if customer_info %}
INFORMACIÓN DEL CLIENTE:
{{ customer_info }}
{% endif %}

Esta notificación se envía para todas las transacciones que superan {{ threshold_amount }} con fines de prevención de fraude y monitoreo.

Ver transacción: {{ transaction_url }}
Ver recibo: {{ receipt_url }}