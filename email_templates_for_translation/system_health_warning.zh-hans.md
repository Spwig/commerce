---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ 系统健康警告：{{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 系统健康警告
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          警告阈值已超出
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的 Spwig 安装中的一个系统健康指标已超出警告阈值。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              警告详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>指标：</strong> {{ metric_name }}<br/>
              <strong>当前值：</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>警告阈值：</strong> {{ warning_threshold }}<br/>
              <strong>严重阈值：</strong> {{ critical_threshold }}<br/>
              <strong>检测时间：</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          潜在影响：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          趋势分析：
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
              💡 需要操作：虽然目前不严重，但立即处理此警告可防止未来的服务问题。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看系统仪表板
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看详细指标
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 系统健康警告

警告阈值已超出

您的 Spwig 安装中的一个系统健康指标已超出警告阈值。

警告详情：
- 指标：{{ metric_name }}
- 当前值：{{ current_value }}
- 警告阈值：{{ warning_threshold }}
- 严重阈值：{{ critical_threshold }}
- 检测时间：{{ detected_at }}

潜在影响：
{{ impact_description }}

建议操作：
{{ recommended_actions }}

{% if trend_data %}
趋势分析：
{{ trend_data }}
{% endif %}

💡 需要操作：虽然目前不严重，但立即处理此警告可防止未来的服务问题。

查看系统仪表板：{{ dashboard_url }}
查看详细指标：{{ metrics_url }}