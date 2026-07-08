---
template_type: admin_report_monthly_review
category: Admin Reports
---

# Email Template: admin_report_monthly_review

## Subject
📊 Monthly Business Review - {{ month_name }} {{ year }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Monthly Business Review
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ month_name }} {{ year}} Performance
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Revenue:</strong> <span style="font-size: 24px; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>Growth:</strong> {{ revenue_growth }}<br/>
              <strong>Orders:</strong> {{ total_orders }}<br/>
              <strong>New Customers:</strong> {{ new_customers }}<br/>
              <strong>CLV:</strong> {{ customer_lifetime_value }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Key Achievements:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ achievements }}
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
📊 MONTHLY BUSINESS REVIEW

{{ month_name }} {{ year }} Performance

FINANCIALS:
- Revenue: {{ total_revenue }}
- Growth: {{ revenue_growth }}
- Orders: {{ total_orders }}
- New Customers: {{ new_customers }}
- CLV: {{ customer_lifetime_value }}

KEY ACHIEVEMENTS:
{{ achievements }}

View full report: {{ full_report_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| month_name | Month name | February |
| year | Year | 2026 |
| total_revenue | Monthly revenue | $327,845.50 |
| revenue_growth | Growth vs last month | +15.3% |
| total_orders | Monthly orders | 2,142 |
| new_customers | New customers | 387 |
| customer_lifetime_value | Average CLV | $1,247 |
| achievements | Key wins | • Record sales week (Feb 8-14)\n• Launched 3 new product lines\n• Email campaign conversion up 22% |
| full_report_url | Full report page | https://shop.com/en/admin/reports/monthly/2026-02 |

## Notes

- Admin/merchant report
- Sent monthly (1st of next month)
- Comprehensive business review
- Growth metrics and achievements
- Can be opted out
