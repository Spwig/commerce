---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ 현금 차이 경고: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 현금 차이 감지됨
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          현금 변동 경고
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }}에서 근무 종료 시 현금 차이 {{ discrepancy_amount }}이 감지되었습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              차이 상세 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>단말기:</strong> {{ terminal_name }}<br/>
              <strong>직원:</strong> {{ cashier_name }}<br/>
              <strong>근무 날짜:</strong> {{ shift_date }}<br/>
              <strong>근무 기간:</strong> {{ shift_duration }}<br/>
              <strong>감지 시간:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          현금 계수:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>예상 현금:</strong> {{ expected_cash }}<br/>
              <strong>실제 계수 현금:</strong> {{ counted_cash }}<br/>
              <strong>차이:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>초기 현금:</strong> {{ opening_cash }}<br/>
              <strong>현금 판매:</strong> {{ cash_sales }}<br/>
              <strong>현금 환불:</strong> {{ cash_refunds }}<br/>
              <strong>지급 현금:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          직원 메모:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 조치:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 거래 내역을 확인하여 오류를 검토하세요<br/>
          2. 기록되지 않은 현금 결제를 확인하세요<br/>
          3. 현금 계수가 정확한지 확인하세요<br/>
          4. 근무 메모에 차이를 기록하세요<br/>
          5. 필요 시 직원과 연락하세요
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          근무 보고서 보기
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          거래 내역 확인
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 현금 차이 감지됨

현금 변동 경고

{{ terminal_name }}에서 근무 종료 시 현금 차이 {{ discrepancy_amount }}이 감지되었습니다.

차이 상세 정보:
- 단말기: {{ terminal_name }}
- 직원: {{ cashier_name }}
- 근무 날짜: {{ shift_date }}
- 근무 기간: {{ shift_duration }}
- 감지 시간: {{ detected_at }}

현금 계수:
- 예상 현금: {{ expected_cash }}
- 실제 계수 현금: {{ counted_cash }}
- 차이: {{ discrepancy_amount }}

BREAKDOWN:
- 초기 현금: {{ opening_cash }}
- 현금 판매: {{ cash_sales }}
- 현금 환불: {{ cash_refunds }}
- 지급 현금: {{ cash_paid_out }}

{% if cashier_note %}
직원 메모:
"{{ cashier_note }}"
{% endif %}

권장 조치:
1. 거래 내역을 확인하여 오류를 검토하세요
2. 기록되지 않은 현금 결제를 확인하세요
3. 현금 계수가 정확한지 확인하세요
4. 근무 메모에 차이를 기록하세요
5. 필요 시 직원과 연락하세요

근무 보고서 보기: {{ shift_report_url }}
거래 내역 확인: {{ transaction_history_url }}