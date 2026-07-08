---
template_type: admin_report_weekly_digest
category: Admin Reports
---

# Email Template: admin_report_weekly_digest

## Subject
📈 Weekly Digest - {{ week_range }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 Weekly Digest
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Week of {{ week_range }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Revenue:</strong> <span style="font-size: 20px; color: #059669;">{{ total_revenue }}</span> ({{ revenue_change }})<br/>
              <strong>Orders:</strong> {{ total_orders }} ({{ orders_change }})<br/>
              <strong>New Customers:</strong> {{ new_customers }}<br/>
              <strong>Average Order Value:</strong> {{ avg_order_value }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Highlights:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ highlights }}
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
📈 WEEKLY DIGEST

Week of {{ week_range }}

PERFORMANCE:
- Revenue: {{ total_revenue }} ({{ revenue_change }})
- Orders: {{ total_orders }} ({{ orders_change }})
- New Customers: {{ new_customers }}
- Average Order Value: {{ avg_order_value }}

HIGHLIGHTS:
{{ highlights }}

View full report: {{ full_report_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| week_range | Week date range | February 8-14, 2026 |
| total_revenue | Weekly revenue | $87,245.50 |
| revenue_change | Change vs last week | +12.5% |
| total_orders | Weekly orders | 542 |
| orders_change | Change vs last week | +8.2% |
| new_customers | New customers | 87 |
| avg_order_value | Average order value | $160.93 |
| highlights | Key achievements | • Best sales day: Saturday ($15,247)\n• Top category: Electronics (+23%)\n• Mobile traffic up 18% |
| full_report_url | Full report page | https://shop.com/en/admin/reports/weekly/2026-W07 |

## Notes

- Admin/merchant report
- Sent weekly (e.g., Monday morning)
- Week-over-week comparisons
- Key highlights and trends
- Can be opted out
