---
template_type: admin_report_revenue_forecast
category: Admin Reports
---

# Email Template: admin_report_revenue_forecast

## Subject
📈 Revenue Forecast - {{ forecast_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 Revenue Forecast
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Projected Performance
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Forecast Period:</strong> {{ forecast_period }}<br/>
              <strong>Projected Revenue:</strong> <span style="font-size: 20px; color: #059669;">{{ projected_revenue }}</span><br/>
              <strong>Current Trend:</strong> {{ trend_direction }}<br/>
              <strong>Confidence:</strong> {{ confidence_level }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Analysis:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ analysis }}
        </mj-text>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommendations:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Detailed Forecast
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📈 REVENUE FORECAST

Projected Performance

FORECAST:
- Forecast Period: {{ forecast_period }}
- Projected Revenue: {{ projected_revenue }}
- Current Trend: {{ trend_direction }}
- Confidence: {{ confidence_level }}%

ANALYSIS:
{{ analysis }}

{% if recommendations %}
RECOMMENDATIONS:
{{ recommendations }}
{% endif %}

View detailed forecast: {{ full_report_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| forecast_period | Forecast timeframe | Next 30 days |
| projected_revenue | Projected revenue | $387,500 |
| trend_direction | Trend indicator | Upward (+12% vs last period) |
| confidence_level | Forecast confidence | 85 |
| analysis | Trend analysis | Based on current trends, revenue is projected to increase 12% next month. Strong performance in Electronics and Home categories driving growth. |
| recommendations | Optional suggestions | • Increase inventory for top-performing categories\n• Launch promotional campaigns to maintain momentum |
| full_report_url | Full report page | https://shop.com/en/admin/reports/forecast |

## Notes

- Admin/merchant report
- Sent monthly
- Data-driven projections
- Strategic planning tool
- Based on historical trends
- Can be opted out
