---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 지급 임계치 달성!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 지급 임계치 달성!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          훌륭한 소식!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          축하합니다! 귀하의 파트너십 잔액이 최소 지급 임계치에 도달했습니다. 이제 지급을 요청할 수 있습니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              귀하의 잔액:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>사용 가능한 잔액:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>최소 지급:</strong> {{ minimum_payout }}<br/>
              <strong>대기 중인 수수료:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          다음 단계:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 파트너십 대시보드에서 지급을 요청하세요<br/>
          • 지급은 {{ payout_schedule }}에 처리됩니다<br/>
          • 자금은 {{ payment_method }}를 통해 전송됩니다
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          지급 요청
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          대시보드 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 지급 임계치 달성!

훌륭한 소식!

안녕하세요 {{ affiliate_name }},

축하합니다! 귀하의 파트너십 잔액이 최소 지급 임계치에 도달했습니다. 이제 지급을 요청할 수 있습니다.

귀하의 잔액:
- 사용 가능한 잔액: {{ available_balance }}
- 최소 지급: {{ minimum_payout }}
- 대기 중인 수수료: {{ pending_balance }}

다음 단계:
• 파트너십 대시보드에서 지급을 요청하세요
• 지급은 {{ payout_schedule }}에 처리됩니다
• 자금은 {{ payment_method }}를 통해 전송됩니다

지급 요청: {{ request_payout_url }}
대시보드 보기: {{ portal_url }}