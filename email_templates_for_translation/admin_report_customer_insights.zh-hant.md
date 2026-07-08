---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 顧客洞察 - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 顧客洞察
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          顧客分析
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>總顧客數:</strong> {{ total_customers }}<br/>
              <strong>新顧客數:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>保留率:</strong> {{ retention_rate }}%<br/>
              <strong>平均 CLV:</strong> {{ avg_clv }}<br/>
              <strong>重複購買率:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          洞察:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看完整報告
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 顧客洞察

顧客分析

METRICS:
- 總顧客數: {{ total_customers }}
- 新顧客數: {{ new_customers }} ({{ new_customer_rate }}%)
- 保留率: {{ retention_rate }}%
- 平均 CLV: {{ avg_clv }}
- 重複購買率: {{ repeat_purchase_rate }}%

INSIGHTS:
{{ insights }}

查看完整報告: {{ full_report_url }}