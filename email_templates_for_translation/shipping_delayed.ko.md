---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
주문 #{{ order_number }}의 업데이트 - 배송 지연

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          주문 업데이트
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }}님,
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          귀하의 주문에 대해 지연이 발생했음을 알려드립니다. 불편을 드려 죄송하며, 기다리시는 동안의 인내에 감사드립니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              주문 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>주문 번호:</strong> {{ order_number }}<br/>
              <strong>기존 예상 배송일:</strong> {{ original_delivery_date }}<br/>
              <strong>새로운 예상 배송일:</strong> {{ new_delivery_date }}<br/>
              <strong>추적 번호:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          지연의 원인:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          주문 추적
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          저희는 귀하의 주문을 최대한 빠르게 전달하기 위해 최선을 다하고 있습니다. 패키지가 출발할 때 다시 업데이트를 받으실 수 있습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          질문이 있으십니까? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">고객 지원 팀에 문의하십시오</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
주문 #{{ order_number }}의 업데이트

안녕하세요, {{ customer_name }}님,

귀하의 주문에 대해 지연이 발생했음을 알려드립니다. 불편을 드려 죄송하며, 기다리시는 동안의 인내에 감사드립니다.

주문 세부 정보:
- 주문 번호: {{ order_number }}
- 기존 예상 배송일: {{ original_delivery_date }}
- 새로운 예상 배송일: {{ new_delivery_date }}
- 추적 번호: {{ tracking_number }}

지연의 원인:
{{ delay_reason }}

주문 추적: {{ tracking_url }}

저희는 귀하의 주문을 최대한 빠르게 전달하기 위해 최선을 다하고 있습니다. 패키지가 출발할 때 다시 업데이트를 받으실 수 있습니다.

질문이 있으십니까? 고객 지원 팀에 문의하십시오: {{ support_url }}

---
이 업데이트는 {{ shop_name }}의 주문 #{{ order_number }}에 대한 것입니다.