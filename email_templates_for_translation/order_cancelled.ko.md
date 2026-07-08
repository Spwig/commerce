---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
주문 #{{ order_number }}이 취소되었습니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          주문이 취소되었습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          주문 <strong>#{{ order_number }}</strong>이 취소되었습니다.
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>이유:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          결제가 이루어졌다면, 원래 결제 방식에 따라 환불이 처리됩니다.
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          주문 상세 정보 보기
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
주문이 취소되었습니다

안녕하세요, {{ customer_name }},

주문 #{{ order_number }}이 취소되었습니다.

{% if cancellation_reason %}이유: {{ cancellation_reason }}{% endif %}

결제가 이루어졌다면, 원래 결제 방식에 따라 환불이 처리됩니다.

{% if order_url %}주문 상세 정보 보기: {{ order_url }}{% endif %}

이 취소에 대해 궁금한 점이 있습니까?
이메일: {{ support_email }}
전화: {{ support_phone }}