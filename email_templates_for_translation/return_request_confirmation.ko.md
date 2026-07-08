---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
반품 요청 수신 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          반품 요청 수신
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          주문 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          주문 <strong>#{{ order_number }}</strong>에 대한 반품 요청을 받았습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              반품 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>이유:</strong> {{ return_reason }}<br/>
              <strong>상품:</strong> {{ items_count }} 개<br/>
              <strong>상태:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          다음으로 어떤 일이 일어날까요?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 우리 팀은 24~48시간 이내에 반품 요청을 검토할 것입니다<br/>
          2. 승인되면 이메일로 반품 배송 라벨을 보내드립니다<br/>
          3. 상품을 안전하게 포장하고 반품 라벨을 부착하세요<br/>
          4. 가장 가까운 배송 센터에 패키지를 맡기세요<br/>
          5. 상품을 수령하고 검사한 후 환불이 처리됩니다
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          궁금한 점이 있다면 언제든지 저희에게 연락주세요.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
반품 요청 수신
주문 #{{ order_number }}

안녕하세요, {{ customer_name }},

주문 #{{ order_number }}에 대한 반품 요청을 받았습니다.

반품 정보:
- 이유: {{ return_reason }}
- 상품: {{ items_count }} 개
- 상태: {{ return_status }}

다음으로 어떤 일이 일어날까요?
1. 우리 팀은 24~48시간 이내에 반품 요청을 검토할 것입니다
2. 승인되면 이메일로 반품 배송 라벨을 보내드립니다
3. 상품을 안전하게 포장하고 반품 라벨을 부착하세요
4. 가장 가까운 배송 센터에 패키지를 맡기세요
5. 상품을 수령하고 검사한 후 환불이 처리됩니다

궁금한 점이 있다면 언제든지 저희에게 연락주세요.