---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 Kundeninsights - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 Kundeninsights
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kundenanalyse
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gesamt Kunden:</strong> {{ total_customers }}<br/>
              <strong>Neue Kunden:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>Retention Rate:</strong> {{ retention_rate }}%<br/>
              <strong>Durchschnittlicher CLV:</strong> {{ avg_clv }}<br/>
              <strong>Wiederkauf Rate:</strong> {{ repeat_purchase_rate }}%
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
          Bericht vollständig anzeigen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 KUNDENINSIGHTS

Kundenanalyse

METRICS:
- Gesamt Kunden: {{ total_customers }}
- Neue Kunden: {{ new_customers }} ({{ new_customer_rate }}%)
- Retention Rate: {{ retention_rate }}%
- Durchschnittlicher CLV: {{ avg_clv }}
- Wiederkauf Rate: {{ repeat_purchase_rate }}%

INSIGHTS:
{{ insights }}

Bericht vollständig anzeigen: {{ full_report_url }}