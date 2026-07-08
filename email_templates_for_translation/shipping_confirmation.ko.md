---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
주문이 발송되었습니다 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          주문이 발송되었습니다!
        </mj-text>
        <mj-text>
          훌륭한 소식입니다! 주문 #{{ order_number }}이(가) 발송되었습니다.
        </mj-text>
        <mj-text>
          <strong>추적 번호:</strong> {{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>운송사:</strong> {{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          배송 추적
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
주문이 발송되었습니다!

훌륭한 소식입니다! 주문 #{{ order_number }}이(가) 발송되었습니다.

추적 번호: {{ tracking_number }}
운송사: {{ carrier }}

배송을 추적하려면 여기를 클릭하세요: {{ tracking_url }}