---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ 비정상적인 수수료 활동이 감지되었습니다 - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 고액 수수료 경고
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          감지된 비정상 활동
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          파트너 {{ affiliate_name }}이 비정상적으로 높은 수수료를 얻었습니다. 사기 방지를 위해 검토가 필요합니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              경고 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>파트너:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>수수료 금액:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>주문 금액:</strong> {{ order_value }}<br/>
              <strong>주문 ID:</strong> {{ order_number }}<br/>
              <strong>감지 시간:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          이 경고가 지정된 이유:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 조치:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 주문 세부 정보의 정확성을 확인하세요<br/>
          • 파트너의 추천 기록을 확인하세요<br/>
          • 고객이 추천자와 관련되어 있지 않은지 확인하세요<br/>
          • 관리자 패널에서 수수료를 승인하거나 거부하세요
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          수수료 검토
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          파트너 세부 정보 보기
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          이 수수료는 검토 대기 중이며 승인될 때까지 지급되지 않습니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 고액 수수료 경고

감지된 비정상 활동

파트너 {{ affiliate_name }}이 비정상적으로 높은 수수료를 얻었습니다. 사기 방지를 위해 검토가 필요합니다.

경고 세부 정보:
- 파트너: {{ affiliate_name }} ({{ affiliate_id }})
- 수수료 금액: {{ commission_amount }}
- 주문 금액: {{ order_value }}
- 주문 ID: {{ order_number }}
- 감지 시간: {{ detected_at }}

이 경고가 지정된 이유:
{{ flag_reason }}

권장 조치:
• 주문 세부 정보의 정확성을 확인하세요
• 파트너의 추천 기록을 확인하세요
• 고객이 추천자와 관련되어 있지 않은지 확인하세요
• 관리자 패널에서 수수료를 승인하거나 거부하세요

수수료 검토: {{ review_commission_url }}
파트너 세부 정보 보기: {{ affiliate_details_url }}

이 수수료는 검토 대기 중이며 승인될 때까지 지급되지 않습니다.