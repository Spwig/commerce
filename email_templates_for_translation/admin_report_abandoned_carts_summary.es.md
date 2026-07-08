---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Informe de carritos abandonados - {{ abandoned_count }} carritos ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Informe de carritos abandonados
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumen de abandono de carritos
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Periodo:</strong> {{ report_period }}<br/>
              <strong>Carritos abandonados:</strong> {{ abandoned_count }}<br/>
              <strong>Valor abandonado:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Tasa de abandono:</strong> {{ abandonment_rate }}%<br/>
              <strong>Tasa de recuperación:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Razones principales (si se rastrean):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver detalles
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 INFORME DE CARROS ABANDONADOS

Resumen de abandono de carritos

MÉTRICAS:
- Periodo: {{ report_period }}
- Carritos abandonados: {{ abandoned_count }}
- Valor abandonado: {{ abandoned_value }}
- Tasa de abandono: {{ abandonment_rate }}%
- Tasa de recuperación: {{ recovery_rate }}%

RAZONES PRINCIPALES:
{{ top_reasons }}

Ver detalles: {{ full_report_url }}