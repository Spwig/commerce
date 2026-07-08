---
template_type: system_health_daily_report
category: System Health
---

# Email Template: system_health_daily_report

## Subject
📊 매일 시스템 건강 보고서 - {{ report_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 매일 시스템 건강 보고서
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          시스템 건강 요약
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ report_date }}에 대한 일일 건강 보고서입니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          전체 상태: {{ overall_status }}
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
          시스템 지표:
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
          경고 (24h):
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
          성능 요약:
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
          권장 사항:
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
          전체 보고서 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 매일 시스템 건강 보고서

시스템 건강 요약

{{ report_date }}에 대한 일일 건강 보고서입니다.

전체 상태: {{ overall_status }}
{{ status_message }}

시스템 지표:
{% for metric in metrics %}
{{ metric.name }}:
- Current: {{ metric.current_value }}
- Average (24h): {{ metric.average }}
- Peak: {{ metric.peak }}
- Status: {{ metric.status }}

{% endfor %}

{% if warnings_count > 0 or critical_count > 0 %}
경고 (24H):
- Critical: {{ critical_count }}
- Warnings: {{ warnings_count }}
- Resolved: {{ resolved_count }}
{% endif %}

성능 요약:
- Uptime: {{ uptime_percentage }}%
- Avg Response Time: {{ avg_response_time }}ms
- Slow Requests: {{ slow_requests_count }}
- Errors (500): {{ errors_500_count }}

{% if recommendations %}
권장 사항:
{{ recommendations }}
{% endif %}

전체 보고서 보기: {{ full_report_url }}