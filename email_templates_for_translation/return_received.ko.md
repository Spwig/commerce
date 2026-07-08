---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
반품이 접수되었습니다 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          반품 접수
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          주문 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }}님,
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          주문 <strong>#{{ order_number }}</strong>에 대한 반품 상품을 받았습니다.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>다음 단계:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 팀원들이 2~3 영업일 이내로 반품 상품을 점검할 것입니다<br/>
          2. 상품이 원래 상태인지 확인할 것입니다<br/>
          3. 점검이 완료되면 환불을 처리할 것입니다<br/>
          4. 환불이 처리되면 확인 이메일을 받게 될 것입니다
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          환불은 원래 결제 수단으로 입금되며, 계좌에 반영되기까지 5~10 영업일이 소요될 수 있습니다.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          불편을 드려 죄송합니다. 감사합니다!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
반품 접수 - 주문 #{{ order_number }}

안녕하세요, {{ customer_name }}님,

주문 #{{ order_number }}에 대한 반품 상품을 받았습니다.

다음 단계:
1. 팀원들이 2~3 영업일 이내로 반품 상품을 점검할 것입니다
2. 상품이 원래 상태인지 확인할 것입니다
3. 점검이 완료되면 환불을 처리할 것입니다
4. 환불이 처리되면 확인 이메일을 받게 될 것입니다

환불은 원래 결제 수단으로 입금되며, 계좌에 반영되기까지 5~10 영업일이 소요될 수 있습니다.

불편을 드려 죄송합니다. 감사합니다!