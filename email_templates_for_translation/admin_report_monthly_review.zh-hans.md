---
template_type: admin_report_monthly_review
category: Admin Reports
---

# Email Template: admin_report_monthly_review

## Subject
📊 月度商业回顾 - {{ month_name }} {{ year }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 月度商业回顾
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ month_name }} {{ year}} 表现
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>收入：</strong> <span style="font-size: 24px; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>增长：</strong> {{ revenue_growth }}<br/>
              <strong>订单：</strong> {{ total_orders }}<br/>
              <strong>新客户：</strong> {{ new_customers }}<br/>
              <strong>CLV：</strong> {{ customer_lifetime_value }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          关键成就：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ achievements }}
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
📊 月度商业回顾

{{ month_name }} {{ year }} 表现

财务：
- 收入：{{ total_revenue }}
- 增长：{{ revenue_growth }}
- 订单：{{ total_orders }}
- 新客户：{{ new_customers }}
- CLV：{{ customer_lifetime_value }}

关键成就：
{{ achievements }}

查看完整报告：{{ full_report_url }}