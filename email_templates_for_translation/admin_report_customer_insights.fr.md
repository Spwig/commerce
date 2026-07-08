---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 Insights client - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 Insights client
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Analytics client
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Clients:</strong> {{ total_customers }}<br/>
              <strong>Nouveaux Clients:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>Taux de Rétention:</strong> {{ retention_rate }}%<br/>
              <strong>Moyenne CLV:</strong> {{ avg_clv }}<br/>
              <strong>Taux d'Achat Répétitif:</strong> {{ repeat_purchase_rate }}%
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
          Voir le rapport complet
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 INSIGHTS CLIENT

Analytics client

MÉTRIQUES:
- Total Clients: {{ total_customers }}
- Nouveaux Clients: {{ new_customers }} ({{ new_customer_rate }}%)
- Taux de Rétention: {{ retention_rate }}%
- Moyenne CLV: {{ avg_clv }}
- Taux d'Achat Répétitif: {{ repeat_purchase_rate }}%

INSIGHTS:
{{ insights }}

Voir le rapport complet: {{ full_report_url }}