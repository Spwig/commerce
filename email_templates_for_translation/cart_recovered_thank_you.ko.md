---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
주문 번호 #{{ order_number }} 감사합니다 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 주문 감사합니다!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          당신이 구매를 완료하게 되어 기쁩니다! 주문이 확인되었으며 배송을 위해 준비 중입니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              주문 요약
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>주문 번호:</strong> {{ order_number }}<br/>
              <strong>주문 날짜:</strong> {{ order_date }}<br/>
              <strong>총 금액:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          주문 추적
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          다음은 어떻게 진행되나요?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 주문을 준비합니다 (보통 1~2 영업일 이내)
          <br/>
          2. 배송 확인과 추적 정보를 받게 됩니다
          <br/>
          3. 주문은 다음 주소로 배송됩니다: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>알아두세요:</strong><br/>
              언제든지 계정 대시보드에서 주문을 추적할 수 있습니다.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          궁금한 점이 있습니까? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">지원 팀에 문의하세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 주문 감사합니다!

안녕하세요, {{ customer_name }},

당신이 구매를 완료하게 되어 기쁩니다! 주문이 확인되었으며 배송을 위해 준비 중입니다.

주문 요약:
- 주문 번호: {{ order_number }}
- 주문 날짜: {{ order_date }}
- 총 금액: {{ order_total }}

주문 추적: {{ order_tracking_url }}

다음은 어떻게 진행되나요?
1. 주문을 준비합니다 (보통 1~2 영업일 이내)
2. 배송 확인과 추적 정보를 받게 됩니다
3. 주문은 다음 주소로 배송됩니다: {{ shipping_address }}

💡 알아두세요:
언제든지 계정 대시보드에서 주문을 추적할 수 있습니다.

궁금한 점이 있습니까? 지원 팀에 문의하세요: {{ support_url }}

---
{{ shop_name }}에서의 주문 #{{ order_number }}