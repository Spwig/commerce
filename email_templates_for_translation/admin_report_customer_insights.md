---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 Customer Insights - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 Customer Insights
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
              <strong>Total Customers:</strong> {{ total_customers }}<br/>
              <strong>New Customers:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>Retention Rate:</strong> {{ retention_rate }}%<br/>
              <strong>Avg CLV:</strong> {{ avg_clv }}<br/>
              <strong>Repeat Purchase Rate:</strong> {{ repeat_purchase_rate }}%
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
👥 CUSTOMER INSIGHTS

Customer Analytics

METRICS:
- Total Customers: {{ total_customers }}
- New Customers: {{ new_customers }} ({{ new_customer_rate }}%)
- Retention Rate: {{ retention_rate }}%
- Avg CLV: {{ avg_clv }}
- Repeat Purchase Rate: {{ repeat_purchase_rate }}%

INSIGHTS:
{{ insights }}

View full report: {{ full_report_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| report_period | Report period | Last 30 days |
| total_customers | Total customer base | 4,827 |
| new_customers | New in period | 387 |
| new_customer_rate | New customer percentage | 8.0 |
| retention_rate | Retention percentage | 73.5 |
| avg_clv | Average customer lifetime value | $1,247 |
| repeat_purchase_rate | Repeat purchase percentage | 42.3 |
| insights | Key findings | • VIP customers (top 10%) generate 45% of revenue\n• Mobile shoppers have 23% higher CLV\n• Email subscribers convert at 3.5x rate |
| full_report_url | Full report page | https://shop.com/en/admin/reports/customers |

## Notes

- Admin/merchant report
- Sent monthly
- Customer behavior analysis
- CLV and retention metrics
- Strategic insights
- Can be opted out
