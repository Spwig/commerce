---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
배송 예외 - 주문 #{{ order_number }}에 주의가 필요합니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 배송 예외
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          귀하의 배송에 예외가 발생했습니다. 이 문제를 최대한 빠르게 해결하고자 노력하고 있습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              예외 세부 정보:
            </mj-text>
            <mj-text color="#92400e">
              <strong>예외 유형:</strong> {{ exception_type }}<br/>
              <strong>설명:</strong> {{ exception_description }}<br/>
              <strong>발생 시간:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              주문 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>주문 번호:</strong> {{ order_number }}<br/>
              <strong>추적 번호:</strong> {{ tracking_number }}<br/>
              <strong>운송업체:</strong> {{ carrier_name }}<br/>
              <strong>현재 위치:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          다음으로 어떤 일이 일어날까요?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ 필요한 조치:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          주문 추적
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          지원 연락처
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 배송 예외

안녕하세요 {{ customer_name }},

귀하의 배송에 예외가 발생했습니다. 이 문제를 최대한 빠르게 해결하고자 노력하고 있습니다.

예외 세부 정보:
- 예외 유형: {{ exception_type }}
- 설명: {{ exception_description }}
- 발생 시간: {{ exception_date }}

주문 정보:
- 주문 번호: {{ order_number }}
- 추적 번호: {{ tracking_number }}
- 운송업체: {{ carrier_name }}
- 현재 위치: {{ current_location }}

다음으로 어떤 일이 일어날까요?
{{ resolution_steps }}

{% if action_required %}
⚠️ 필요한 조치:
{{ action_required_description }}
{% endif %}

주문 추적: {{ tracking_url }}
지원 연락처: {{ support_url }}