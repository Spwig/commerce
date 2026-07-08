---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Relatório de Carts Abandonados - {{ abandoned_count }} carts ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Relatório de Carts Abandonados
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumo de Abandono de Carts
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Periodo:</strong> {{ report_period }}<br/>
              <strong>Carts Abandonados:</strong> {{ abandoned_count }}<br/>
              <strong>Valor Abandonado:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Taxa de Abandono:</strong> {{ abandonment_rate }}%<br/>
              <strong>Taxa de Recuperação:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Principais Motivos (se rastreados):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Detalhes
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 RELATÓRIO DE CARTS ABANDONADOS

Resumo de Abandono de Carts

METRÍCAS:
- Periodo: {{ report_period }}
- Carts Abandonados: {{ abandoned_count }}
- Valor Abandonado: {{ abandoned_value }}
- Taxa de Abandono: {{ abandonment_rate }}%
- Taxa de Recuperação: {{ recovery_rate }}%

PRINCIPAIS MOTIVOS:
{{ top_reasons }}

Ver detalhes: {{ full_report_url }}