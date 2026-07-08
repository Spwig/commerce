---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
주문 #{{ order_number }}이 배송되었습니다!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 주문이 배송되었습니다!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          배송 중입니다!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }}님,
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          훌륭한 소식입니다! 주문이 배송되었으며, 곧 당신에게 도착할 예정입니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              배송 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>주문 번호:</strong> {{ order_number }}<br/>
              <strong>추적 번호:</strong> {{ tracking_number }}<br/>
              <strong>운송사:</strong> {{ carrier_name }}<br/>
              <strong>예상 배송일:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          패키지 추적
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 주문이 배송되었습니다!

배송 중입니다!

안녕하세요, {{ customer_name }}님,

훌륭한 소식입니다! 주문이 배송되었으며, 곧 당신에게 도착할 예정입니다.

배송 세부 정보:
- 주문 번호: {{ order_number }}
- 추적 번호: {{ tracking_number }}
- 운송사: {{ carrier_name }}
- 예상 배송일: {{ estimated_delivery }}

패키지 추적: {{ tracking_url }}