---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Reporte dei carrelli abbandonati - {{ abandoned_count }} carrelli ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Reporte dei carrelli abbandonati
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Riepilogo abbandono carrello
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Periodo:</strong> {{ report_period }}<br/>
              <strong>Carrelli abbandonati:</strong> {{ abandoned_count }}<br/>
              <strong>Valore abbandonato:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Tasso di abbandono:</strong> {{ abandonment_rate }}%<br/>
              <strong>Tasso di recupero:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Motivi principali (se tracciati):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza dettagli
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 REPORT DEI CARRELLI ABANDONATI

Riepilogo abbandono carrello

METRICHE:
- Periodo: {{ report_period }}
- Carrelli abbandonati: {{ abandoned_count }}
- Valore abbandonato: {{ abandoned_value }}
- Tasso di abbandono: {{ abandonment_rate }}%
- Tasso di recupero: {{ recovery_rate }}%

MOTIVI PRINCIPALI:
{{ top_reasons }}

Visualizza dettagli: {{ full_report_url }}