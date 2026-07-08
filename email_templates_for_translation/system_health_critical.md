---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 CRITICAL ALERT: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 CRITICAL SYSTEM ALERT
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Immediate Attention Required
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          A critical system health issue has been detected on your Spwig installation.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Critical Issue
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Current Value:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Critical Threshold:</strong> {{ critical_threshold }}<br/>
              <strong>Detected:</strong> {{ detected_at }}<br/>
              <strong>Severity:</strong> CRITICAL
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impact:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Immediate Actions Required:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Trend:
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Service Degradation Warning
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              This issue may cause service interruptions or performance degradation. Address immediately to prevent customer impact.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View System Dashboard
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View System Logs
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 CRITICAL SYSTEM ALERT

Immediate Attention Required

A critical system health issue has been detected on your Spwig installation.

🚨 CRITICAL ISSUE:
- Metric: {{ metric_name }}
- Current Value: {{ current_value }}
- Critical Threshold: {{ critical_threshold }}
- Detected: {{ detected_at }}
- Severity: CRITICAL

IMPACT:
{{ impact_description }}

IMMEDIATE ACTIONS REQUIRED:
{{ recommended_actions }}

{% if trend_data %}
TREND:
{{ trend_data }}
{% endif %}

⚠️ SERVICE DEGRADATION WARNING:
This issue may cause service interruptions or performance degradation. Address immediately to prevent customer impact.

View system dashboard: {{ dashboard_url }}
View system logs: {{ logs_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| metric_name | System metric name | Disk Space - Root Partition |
| current_value | Current metric value | 97% used (4.2 GB free) |
| critical_threshold | Critical threshold value | 95% |
| detected_at | When detected | February 15, 2026 at 3:45 PM |
| impact_description | What could happen | System may become unresponsive. Database writes could fail. |
| recommended_actions | What to do | • Free disk space immediately\n• Remove old logs and temp files\n• Consider upgrading storage |
| trend_data | Optional trend info | Disk usage increased 15% in last 24 hours |
| dashboard_url | System dashboard | https://shop.com/en/admin/system/health |
| logs_url | System logs page | https://shop.com/en/admin/system/logs |

## Notes

- CRITICAL admin/technical notification
- Highest priority email
- Sent when system metric exceeds critical threshold
- Examples: disk >95%, memory >90%, CPU >95%, database connections exhausted
- Immediate action required
- May indicate imminent service failure
- Always sent (cannot be opted out)
- Transactional email
