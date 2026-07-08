---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 버려진 장바구니 보고서 - {{ abandoned_count }}개의 장바구니 ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 버려진 장바구니 보고서
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          장바구니 포기 요약
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>기간:</strong> {{ report_period }}<br/>
              <strong>버려진 장바구니:</strong> {{ abandoned_count }}<br/>
              <strong>버려진 가치:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>포기율:</strong> {{ abandonment_rate }}%<br/>
              <strong>회복율:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          주요 원인 (추적된 경우):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          세부 정보 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 버려진 장바구니 보고서

장바구니 포기 요약

METRICS:
- 기간: {{ report_period }}
- 버려진 장바구니: {{ abandoned_count }}
- 버려진 가치: {{ abandoned_value }}
- 포기율: {{ abandonment_rate }}%
- 회복율: {{ recovery_rate }}%

TOP REASONS:
{{ top_reasons }}

세부 정보 보기: {{ full_report_url }}