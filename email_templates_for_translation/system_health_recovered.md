---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ Resolved: {{ metric_name }} returned to normal

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Issue Resolved
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          System Health Recovered
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Good news! The system health issue with {{ metric_name }} has been resolved.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Recovery Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Current Value:</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Normal Threshold:</strong> {{ normal_threshold }}<br/>
              <strong>Issue Detected:</strong> {{ issue_detected_at }}<br/>
              <strong>Recovered:</strong> {{ recovered_at }}<br/>
              <strong>Duration:</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ System Status: Normal
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }} has returned to normal levels and is operating within acceptable parameters.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resolution Summary:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions Taken:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ actions_taken }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if preventive_measures %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Preventive Measures:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ preventive_measures }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View System Dashboard
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Incident Report
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ISSUE RESOLVED

System Health Recovered

Good news! The system health issue with {{ metric_name }} has been resolved.

RECOVERY DETAILS:
- Metric: {{ metric_name }}
- Current Value: {{ current_value }}
- Normal Threshold: {{ normal_threshold }}
- Issue Detected: {{ issue_detected_at }}
- Recovered: {{ recovered_at }}
- Duration: {{ issue_duration }}

✓ SYSTEM STATUS: NORMAL
{{ metric_name }} has returned to normal levels and is operating within acceptable parameters.

{% if resolution_summary %}
RESOLUTION SUMMARY:
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
ACTIONS TAKEN:
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
PREVENTIVE MEASURES:
{{ preventive_measures }}
{% endif %}

View system dashboard: {{ dashboard_url }}
{% if incident_report_url %}View incident report: {{ incident_report_url }}{% endif %}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| metric_name | System metric name | Disk Space - Root Partition |
| current_value | Current (recovered) value | 72% used |
| normal_threshold | Normal threshold value | <80% |
| issue_detected_at | When issue started | February 15, 2026 at 3:45 PM |
| recovered_at | When recovered | February 15, 2026 at 5:15 PM |
| issue_duration | How long issue lasted | 1 hour 30 minutes |
| resolution_summary | What resolved it | Disk space freed automatically by log rotation |
| actions_taken | Actions performed | • Cleared old log files\n• Removed temporary cache data\n• Enabled automatic cleanup |
| preventive_measures | Future prevention | Configured automatic log rotation and increased monitoring frequency |
| dashboard_url | System dashboard | https://shop.com/en/admin/system/health |
| incident_report_url | Incident details | https://shop.com/en/admin/system/incidents/12345 |

## Notes

- Admin/technical notification
- Sent when system metric returns to normal after alert
- Positive confirmation that issue is resolved
- May include resolution details and actions taken
- Provides closure on incident
- Links to incident report for documentation
- Transactional email
