---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 严重警报：{{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 严重系统警报
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          需要立即关注
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          检测到您的 Spwig 安装存在严重系统健康问题。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 严重问题
            </mj-text>
            <mj-text color="#991b1b">
              <strong>指标：</strong> {{ metric_name }}<br/>
              <strong>当前值：</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>严重阈值：</strong> {{ critical_threshold }}<br/>
              <strong>检测时间：</strong> {{ detected_at }}<br/>
              <strong>严重性：</strong> 严重
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          影响：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          需要立即采取的措施：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          趋势：
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
              ⚠️ 服务降级警告
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              此问题可能导致服务中断或性能下降。请立即处理以避免对客户造成影响。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看系统仪表板
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看系统日志
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 严重系统警报

需要立即关注

检测到您的 Spwig 安装存在严重系统健康问题。

🚨 严重问题：
- 指标：{{ metric_name }}
- 当前值：{{ current_value }}
- 严重阈值：{{ critical_threshold }}
- 检测时间：{{ detected_at }}
- 严重性：严重

影响：
{{ impact_description }}

需要立即采取的措施：
{{ recommended_actions }}

{% if trend_data %}
趋势：
{{ trend_data }}
{% endif %}

⚠️ 服务降级警告：
此问题可能导致服务中断或性能下降。请立即处理以避免对客户造成影响。

查看系统仪表板：{{ dashboard_url }}
查看系统日志：{{ logs_url }}