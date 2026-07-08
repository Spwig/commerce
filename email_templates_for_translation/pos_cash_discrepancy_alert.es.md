---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Alerta de discrepancia de efectivo: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Detectada discrepancia de efectivo
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alerta de Variación de Efectivo
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Se detectó una discrepancia de efectivo de {{ discrepancy_amount }} al cerrar el turno en {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles de la Discrepancia:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cajero:</strong> {{ cashier_name }}<br/>
              <strong>Fecha del Turno:</strong> {{ shift_date }}<br/>
              <strong>Duración del Turno:</strong> {{ shift_duration }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cuenta de Efectivo:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Efectivo esperado:</strong> {{ expected_cash }}<br/>
              <strong>Efectivo contado:</strong> {{ counted_cash }}<br/>
              <strong>Discrepancia:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Efectivo Inicial:</strong> {{ opening_cash }}<br/>
              <strong>Ventas en Efectivo:</strong> {{ cash_sales }}<br/>
              <strong>Reembolsos en Efectivo:</strong> {{ cash_refunds }}<br/>
              <strong>Efectivo Pagado:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nota del Cajero:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Revisar historial de transacciones en busca de errores<br/>
          2. Verificar pagos en efectivo no registrados<br/>
          3. Verificar si la cuenta de efectivo fue precisa<br/>
          4. Documentar la discrepancia en las notas del turno<br/>
          5. Seguir con el cajero si es necesario
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver informe del turno
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Revisar transacciones
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ DISCREPANCIA DE EFECTIVO DETECTADA

Alerta de Variación de Efectivo

Se detectó una discrepancia de efectivo de {{ discrepancy_amount }} al cerrar el turno en {{ terminal_name }}.

DETALLES DE LA DISCREPANCIA:
- Terminal: {{ terminal_name }}
- Cajero: {{ cashier_name }}
- Fecha del Turno: {{ shift_date }}
- Duración del Turno: {{ shift_duration }}
- Detectado: {{ detected_at }}

CUENTA DE EFECTIVO:
- Efectivo esperado: {{ expected_cash }}
- Efectivo contado: {{ counted_cash }}
- Discrepancia: {{ discrepancy_amount }}

ROMPIMIENTO:
- Efectivo Inicial: {{ opening_cash }}
- Ventas en Efectivo: {{ cash_sales }}
- Reembolsos en Efectivo: {{ cash_refunds }}
- Efectivo Pagado: {{ cash_paid_out }}

{% if cashier_note %}
NOTA DEL CAJERO:
"{{ cashier_note }}"
{% endif %}

ACCIONES RECOMENDADAS:
1. Revisar historial de transacciones en busca de errores
2. Verificar pagos en efectivo no registrados
3. Verificar si la cuenta de efectivo fue precisa
4. Documentar la discrepancia en las notas del turno
5. Seguir con el cajero si es necesario

Ver informe del turno: {{ shift_report_url }}
Revisar transacciones: {{ transaction_history_url }}