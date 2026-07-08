---
template_type: admin_report_revenue_forecast
category: Admin Reports
---

# Email Template: admin_report_revenue_forecast

## Subject
📈 收入预测 - {{ forecast_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 收入预测
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          预测表现
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>预测时间段：</strong> {{ forecast_period }}<br/>
              <strong>预测收入：</strong> <span style="font-size: 20px; color: #059669;">{{ projected_revenue }}</span><br/>
              <strong>当前趋势：</strong> {{ trend_direction }}<br/>
              <strong>置信度：</strong> {{ confidence_level }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          分析：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ analysis }}
        </mj-text>

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
          查看详细预测
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📈 收入预测

预测表现

预测：
- 预测时间段：{{ forecast_period }}
- 预测收入：{{ projected_revenue }}
- 当前趋势：{{ trend_direction }}
- 置信度：{{ confidence_level }}%

分析：
{{ analysis }}

{% if recommendations %}
建议：
{{ recommendations }}
{% endif %}

查看详细预测：{{ full_report_url }}