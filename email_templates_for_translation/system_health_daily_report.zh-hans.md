---
template_type: system_health_daily_report
category: System Health
---

# Email Template: system_health_daily_report

## Subject
📊 每日系统健康报告 - {{ report_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 每日系统健康报告
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          系统健康摘要
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ report_date }} 的每日健康报告。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          总体状态：{{ overall_status }}
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
          系统指标：
        </mj-text>

        {% for metric in metrics %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ metric.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>当前：</strong>{{ metric.current_value }}<br/>
              <strong>平均（24小时）：</strong>{{ metric.average }}<br/>
              <strong>峰值：</strong>{{ metric.peak }}<br/>
              <strong>状态：</strong><span style="color: {{ metric.status_color }};">{{ metric.status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if warnings_count > 0 or critical_count > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          警报（24小时）：
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>严重：</strong><span style="color: #dc2626;">{{ critical_count }}</span><br/>
              <strong>警告：</strong><span style="color: #d97706;">{{ warnings_count }}</span><br/>
              <strong>已解决：</strong><span style="color: #059669;">{{ resolved_count }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          性能摘要：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>正常运行时间：</strong>{{ uptime_percentage }}%<br/>
              <strong>平均响应时间：</strong>{{ avg_response_time }}ms<br/>
              <strong>慢请求：</strong>{{ slow_requests_count }}<br/>
              <strong>错误（500）：</strong>{{ errors_500_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议：
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
          查看完整报告
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 每日系统健康报告

系统健康摘要

{{ report_date }} 的每日健康报告。

总体状态：{{ overall_status }}
{{ status_message }}

系统指标：
{% for metric in metrics %}
{{ metric.name }}：
- 当前：{{ metric.current_value }}
- 平均（24小时）：{{ metric.average }}
- 峰值：{{ metric.peak }}
- 状态：{{ metric.status }}

{% endfor %}

{% if warnings_count > 0 or critical_count > 0 %}
警报（24小时）：
- 严重：{{ critical_count }}
- 警告：{{ warnings_count }}
- 已解决：{{ resolved_count }}
{% endif %}

性能摘要：
- 正常运行时间：{{ uptime_percentage }}%
- 平均响应时间：{{ avg_response_time }}ms
- 慢请求：{{ slow_requests_count }}
- 错误（500）：{{ errors_500_count }}

{% if recommendations %}
建议：
{{ recommendations }}
{% endif %}

查看完整报告：{{ full_report_url }}