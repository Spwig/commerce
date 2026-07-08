---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
배송 완료 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          배송 완료
        </mj-text>
        <mj-text>
          주문 #{{ order_number }}이(가) 배송되었습니다!
        </mj-text>
        <mj-text>
          구매하신 상품을 즐기시길 바랍니다. 궁금한 점이나 우려 사항이 있는 경우, 언제든지 저희에게 연락 주시기 바랍니다.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          주문 확인
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
배송 완료

주문 #{{ order_number }}이(가) 배송되었습니다!

구매하신 상품을 즐기시길 바랍니다. 궁금한 점이나 우려 사항이 있는 경우, 언제든지 저희에게 연락 주시기 바랍니다.

주문 확인: {{ order_url }}

