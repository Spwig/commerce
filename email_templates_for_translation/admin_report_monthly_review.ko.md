---
template_type: admin_report_monthly_review
category: Admin Reports
---

# Email Template: admin_report_monthly_review

## Subject
📊 월별 비즈니스 리뷰 - {{ month_name }} {{ year }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 월별 비즈니스 리뷰
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ month_name }} {{ year}} 성과
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>수익:</strong> <span style="font-size: 24px; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>성장:</strong> {{ revenue_growth }}<br/>
              <strong>주문:</strong> {{ total_orders }}<br/>
              <strong>신규 고객:</strong> {{ new_customers }}<br/>
              <strong>CLV:</strong> {{ customer_lifetime_value }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          주요 성과:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ achievements }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          전체 보고서 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 월별 비즈니스 리뷰

{{ month_name }} {{ year }} 성과

재정:
- 수익: {{ total_revenue }}
- 성장: {{ revenue_growth }}
- 주문: {{ total_orders }}
- 신규 고객: {{ new_customers }}
- CLV: {{ customer_lifetime_value }}

주요 성과:
{{ achievements }}

전체 보고서 보기: {{ full_report_url }}