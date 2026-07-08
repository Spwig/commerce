---
template_type: system_health_daily_report
category: System Health
---

# Email Template: system_health_daily_report

## Subject
📊 รายงานสุขภาพระบบรายวัน - {{ report_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 รายงานสุขภาพระบบรายวัน
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สรุปสุขภาพระบบ
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          รายงานสุขภาพระบบประจำวันสำหรับ {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สถานะโดยรวม: {{ overall_status }}
        </mj-text>

        <mj-section background-color="{{ status_color }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#ffffff" font-weight="bold" align="center">
              {{ status_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อมูลระบบ:
        </mj-text>

        {% for metric in metrics %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ metric.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Current:</strong> {{ metric.current_value }}<br/>
              <strong>Average (24h):</strong> {{ metric.average }}<br/>
              <strong>Peak:</strong> {{ metric.peak }}<br/>
              <strong>Status:</strong> <span style="color: {{ metric.status_color }};">{{ metric.status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if warnings_count > 0 or critical_count > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การแจ้งเตือน (24 ชม.):
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Critical:</strong> <span style="color: #dc2626;">{{ critical_count }}</span><br/>
              <strong>Warnings:</strong> <span style="color: #d97706;">{{ warnings_count }}</span><br/>
              <strong>Resolved:</strong> <span style="color: #059669;">{{ resolved_count }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สรุปประสิทธิภาพ:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Uptime:</strong> {{ uptime_percentage }}%<br/>
              <strong>Avg Response Time:</strong> {{ avg_response_time }}ms<br/>
              <strong>Slow Requests:</strong> {{ slow_requests_count }}<br/>
              <strong>Errors (500):</strong> {{ errors_500_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อแนะนำ:
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
          ดูรายงานฉบับเต็ม
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 รายงานสุขภาพระบบรายวัน

สรุปสุขภาพระบบ

รายงานสุขภาพระบบประจำวันสำหรับ {{ report_date }}.

สถานะโดยรวม: {{ overall_status }}
{{ status_message }}

ข้อมูลระบบ:
{% for metric in metrics %}
{{ metric.name }}:
- Current: {{ metric.current_value }}
- Average (24h): {{ metric.average }}
- Peak: {{ metric.peak }}
- Status: {{ metric.status }}

{% endfor %}

{% if warnings_count > 0 or critical_count > 0 %}
การแจ้งเตือน (24 ชม.)
- Critical: {{ critical_count }}
- Warnings: {{ warnings_count }}
- Resolved: {{ resolved_count }}
{% endif %}

สรุปประสิทธิภาพ:
- Uptime: {{ uptime_percentage }}%
- Avg Response Time: {{ avg_response_time }}ms
- Slow Requests: {{ slow_requests_count }}
- Errors (500): {{ errors_500_count }}

{% if recommendations %}
ข้อแนะนำ:
{{ recommendations }}
{% endif %}

ดูรายงานฉบับเต็ม: {{ full_report_url }}