---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
반품이 승인되었습니다 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          반품 승인
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          주문 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          주문 <strong>#{{ order_number }}</strong>의 반품 요청이 승인되었습니다.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>다음 단계:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 아래의 반품 라벨을 다운로드하고 인쇄하세요<br/>
          2. 가능한 경우 원래 포장재에 안전하게 상품을 포장하세요<br/>
          3. 반품 라벨을 포장의 외부에 부착하세요<br/>
          4. 가장 가까운 배송 센터에 반품을 맡기세요
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          반품 라벨 다운로드
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>반품 추적 번호:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>중요:</strong> 환불이 신속하게 처리되도록 반품을 7일 이내에 발송해 주시기 바랍니다.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          우리가 반품을 수령하고 검사한 후, 원래 결제 수단으로 환불을 처리할 것입니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
반품 승인 - 주문 #{{ order_number }}

안녕하세요 {{ customer_name }},

주문 #{{ order_number }}의 반품 요청이 승인되었습니다.

다음 단계:
1. 반품 라벨을 다운로드하고 인쇄하세요
2. 가능한 경우 원래 포장재에 안전하게 상품을 포장하세요
3. 반품 라벨을 포장의 외부에 부착하세요
4. 가장 가까운 배송 센터에 반품을 맡기세요

{% if return_label_url %}반품 라벨 다운로드: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}반품 추적 번호: {{ return_tracking_number }}{% endif %}

중요: 환불이 신속하게 처리되도록 반품을 7일 이내에 발송해 주시기 바랍니다.

우리가 반품을 수령하고 검사한 후, 원래 결제 수단으로 환불을 처리할 것입니다.