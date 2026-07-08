---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ {{ metric_name }} 已恢复正常

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 问题已解决
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          系统健康状态已恢复
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！{{ metric_name }} 的系统健康问题已得到解决。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              恢复详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>指标：</strong> {{ metric_name }}<br/>
              <strong>当前值：</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>正常阈值：</strong> {{ normal_threshold }}<br/>
              <strong>检测到问题：</strong> {{ issue_detected_at }}<br/>
              <strong>已恢复：</strong> {{ recovered_at }}<br/>
              <strong>持续时间：</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ 系统状态：正常
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }} 已恢复正常水平，并在可接受的参数范围内运行。
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          解决方案概要：
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          已采取的措施：
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
          预防措施：
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
          查看系统仪表板
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看事故报告
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 问题已解决

系统健康状态已恢复

好消息！{{ metric_name }} 的系统健康问题已得到解决。

恢复详情：
- 指标：{{ metric_name }}
- 当前值：{{ current_value }}
- 正常阈值：{{ normal_threshold }}
- 检测到问题：{{ issue_detected_at }}
- 已恢复：{{ recovered_at }}
- 持续时间：{{ issue_duration }}

✓ 系统状态：正常
{{ metric_name }} 已恢复正常水平，并在可接受的参数范围内运行。

{% if resolution_summary %}
解决方案概要：
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
已采取的措施：
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
预防措施：
{{ preventive_measures }}
{% endif %}

查看系统仪表板：{{ dashboard_url }}
{% if incident_report_url %}查看事故报告：{{ incident_report_url }}{% endif %}