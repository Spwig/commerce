---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 客户洞察 - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 客户洞察
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          客户分析
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>总客户数：</strong> {{ total_customers }}<br/>
              <strong>新客户数：</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>客户留存率：</strong> {{ retention_rate }}%<br/>
              <strong>平均客户终身价值：</strong> {{ avg_clv }}<br/>
              <strong>复购率：</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          洞察：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看完整报告
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 客户洞察

客户分析

指标：
- 总客户数：{{ total_customers }}
- 新客户数：{{ new_customers }} ({{ new_customer_rate }}%)
- 客户留存率：{{ retention_rate }}%
- 平均客户终身价值：{{ avg_clv }}
- 复购率：{{ repeat_purchase_rate }}%

洞察：
{{ insights }}

查看完整报告：{{ full_report_url }}