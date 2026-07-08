---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Отчет об оставленных корзинах - {{ abandoned_count }} корзин ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Отчет об оставленных корзинах
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Сводка оставления корзин
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Period:</strong> {{ report_period }}<br/>
              <strong>Abandoned Carts:</strong> {{ abandoned_count }}<br/>
              <strong>Abandoned Value:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Abandonment Rate:</strong> {{ abandonment_rate }}%<br/>
              <strong>Recovery Rate:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Top Reasons (if tracked):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Details
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 ОТЧЕТ О ОСТАВЛЕННЫХ КОРЗИНАХ

Сводка оставления корзин

METRICS:
- Period: {{ report_period }}
- Abandoned Carts: {{ abandoned_count }}
- Abandoned Value: {{ abandoned_value }}
- Abandonment Rate: {{ abandonment_rate }}%
- Recovery Rate: {{ recovery_rate }}%

TOP REASONS:
{{ top_reasons }}

View details: {{ full_report_url }}