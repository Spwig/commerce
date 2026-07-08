---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 Informe de cambio: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Shift Cerrado
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumen del Informe de Cambio
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Shift cerrado en {{ terminal_name }} por {{ cashier_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del Cambio:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cajero:</strong> {{ cashier_name }}<br/>
              <strong>Comenzado:</strong> {{ shift_started }}<br/>
              <strong>Terminado:</strong> {{ shift_ended }}<br/>
              <strong>Duración:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumen de Ventas:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Ventas Totales:</strong> {{ total_sales }}<br/>
              <strong>Transacciones:</strong> {{ transaction_count }}<br/>
              <strong>Artículos Vendidos:</strong> {{ items_sold }}<br/>
              <strong>Venta Promedio:</strong> {{ average_sale }}<br/>
              <strong>Impuesto Recaudado:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Desglose de Pago:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} transacciones)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Conciliación de Efectivo:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Efectivo Inicial:</strong> {{ opening_cash }}<br/>
              <strong>Ventas en Efectivo:</strong> {{ cash_sales }}<br/>
              <strong>Efectivo Esperado:</strong> {{ expected_cash }}<br/>
              <strong>Efectivo Contado:</strong> {{ counted_cash }}<br/>
              <strong>Diferencia:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Diferencia en Efectivo: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              Nota: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Informe Completo
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 CAMBIO CERRADO

Resumen del Informe de Cambio

Shift cerrado en {{ terminal_name }} por {{ cashier_name }}.

DETALLES DEL CAMBIO:
- Terminal: {{ terminal_name }}
- Cajero: {{ cashier_name }}
- Comenzado: {{ shift_started }}
- Terminado: {{ shift_ended }}
- Duración: {{ shift_duration }}

RESUMEN DE VENTAS:
- Total de ventas: {{ total_sales }}
- Transacciones: {{ transaction_count }}
- Artículos vendidos: {{ items_sold }}
- Venta promedio: {{ average_sale }}
- Impuesto recaudado: {{ tax_collected }}

DESGLOSE DE PAGO:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} transacciones)
{% endfor %}

CONCILIACIÓN DE EFECTIVO:
- Efectivo inicial: {{ opening_cash }}
- Ventas en efectivo: {{ cash_sales }}
- Efectivo esperado: {{ expected_cash }}
- Efectivo contado: {{ counted_cash }}
- Diferencia: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ DIFERENCIA EN EFECTIVO: {{ discrepancy_amount }}
{% if discrepancy_note %}Nota: {{ discrepancy_note }}{% endif %}
{% endif %}

Ver informe completo: {{ shift_report_url }}