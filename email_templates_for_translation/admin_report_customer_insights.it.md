---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 Insights sui clienti - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 Insights sui clienti
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Customer Analytics
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Totale clienti:</strong> {{ total_customers }}<br/>
              <strong>Nuovi clienti:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>Tasso di fidelizzazione:</strong> {{ retention_rate }}%<br/>
              <strong>CLV medio:</strong> {{ avg_clv }}<br/>
              <strong>Tasso di acquisto ripetuto:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Insights:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Full Report
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 INSIGHTS SUI CLIENTI

Customer Analytics

METRICS:
- Totale clienti: {{ total_customers }}
- Nuovi clienti: {{ new_customers }} ({{ new_customer_rate }}%)
- Tasso di fidelizzazione: {{ retention_rate }}%
- CLV medio: {{ avg_clv }}
- Tasso di acquisto ripetuto: {{ repeat_purchase_rate }}%

INSIGHTS:
{{ insights }}

View full report: {{ full_report_url }}