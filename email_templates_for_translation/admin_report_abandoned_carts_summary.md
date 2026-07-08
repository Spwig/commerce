---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Abandoned Carts Report - {{ abandoned_count }} carts ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Abandoned Carts Report
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cart Abandonment Summary
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
📊 ABANDONED CARTS REPORT

Cart Abandonment Summary

METRICS:
- Period: {{ report_period }}
- Abandoned Carts: {{ abandoned_count }}
- Abandoned Value: {{ abandoned_value }}
- Abandonment Rate: {{ abandonment_rate }}%
- Recovery Rate: {{ recovery_rate }}%

TOP REASONS:
{{ top_reasons }}

View details: {{ full_report_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| report_period | Report period | Last 7 days |
| abandoned_count | Number of abandoned carts | 142 |
| abandoned_value | Total value abandoned | $18,247.50 |
| abandonment_rate | Percentage abandoned | 68.5 |
| recovery_rate | Recovery percentage | 12.3 |
| top_reasons | Abandonment reasons | • High shipping costs (34%)\n• Unexpected fees (28%)\n• Comparison shopping (22%) |
| full_report_url | Full report page | https://shop.com/en/admin/reports/abandoned-carts |

## Notes

- Admin/merchant report
- Sent weekly
- Identifies revenue recovery opportunities
- Actionable insights
- Can be opted out
