---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ System Health Warning: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ System Health Warning
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Warning Threshold Exceeded
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          A system health metric has exceeded the warning threshold on your Spwig installation.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Warning Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Current Value:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Warning Threshold:</strong> {{ warning_threshold }}<br/>
              <strong>Critical Threshold:</strong> {{ critical_threshold }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Potential Impact:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Trend Analysis:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Action Required: While not critical yet, addressing this warning now can prevent future service issues.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View System Dashboard
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Detailed Metrics
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ SYSTEM HEALTH WARNING

Warning Threshold Exceeded

A system health metric has exceeded the warning threshold on your Spwig installation.

WARNING DETAILS:
- Metric: {{ metric_name }}
- Current Value: {{ current_value }}
- Warning Threshold: {{ warning_threshold }}
- Critical Threshold: {{ critical_threshold }}
- Detected: {{ detected_at }}

POTENTIAL IMPACT:
{{ impact_description }}

RECOMMENDED ACTIONS:
{{ recommended_actions }}

{% if trend_data %}
TREND ANALYSIS:
{{ trend_data }}
{% endif %}

💡 ACTION REQUIRED: While not critical yet, addressing this warning now can prevent future service issues.

View system dashboard: {{ dashboard_url }}
View detailed metrics: {{ metrics_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| metric_name | System metric name | Memory Usage |
| current_value | Current metric value | 82% |
| warning_threshold | Warning threshold value | 80% |
| critical_threshold | Critical threshold value | 90% |
| detected_at | When detected | February 15, 2026 at 3:45 PM |
| impact_description | What could happen | System performance may degrade if memory usage continues to increase |
| recommended_actions | What to do | • Monitor memory usage trends\n• Identify memory-intensive processes\n• Consider increasing server memory |
| trend_data | Optional trend info | Memory usage has steadily increased 5% over past week |
| dashboard_url | System dashboard | https://shop.com/en/admin/system/health |
| metrics_url | Detailed metrics page | https://shop.com/en/admin/system/metrics |

## Notes

- Admin/technical notification
- Sent when system metric exceeds warning threshold but not critical
- Examples: disk >80%, memory >75%, CPU >80%
- Preventive action recommended
- Less urgent than critical alerts
- Can be configured per-metric
- Transactional email
