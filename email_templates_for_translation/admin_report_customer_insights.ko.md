---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 고객 통찰력 - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 고객 통찰력
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          고객 분석
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>총 고객 수:</strong> {{ total_customers }}<br/>
              <strong>신규 고객 수:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>고객 유지율:</strong> {{ retention_rate }}%<br/>
              <strong>평균 CLV:</strong> {{ avg_clv }}<br/>
              <strong>재구매율:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          통찰력:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
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
👥 고객 통찰력

고객 분석

통계:
- 총 고객 수: {{ total_customers }}
- 신규 고객 수: {{ new_customers }} ({{ new_customer_rate }}%)
- 고객 유지율: {{ retention_rate }}%
- 평균 CLV: {{ avg_clv }}
- 재구매율: {{ repeat_purchase_rate }}%

통찰력:
{{ insights }}

전체 보고서 보기: {{ full_report_url }}