---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
주문 #{{ order_number }} - 상태 업데이트: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          주문 상태 업데이트
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
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
          주문 <strong>#{{ order_number }}</strong> 상태가 업데이트되었습니다.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>이전 상태:</strong> {{ old_status_display }}<br/>
              <strong>새로운 상태:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          주문 상세 보기
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
주문 상태 업데이트 - 주문 #{{ order_number }}

안녕하세요 {{ customer_name }},

주문 #{{ order_number }} 상태가 업데이트되었습니다.

이전 상태: {{ old_status_display }}
새로운 상태: {{ new_status_display }}

{% if order_url %}주문 상세 보기: {{ order_url }}{% endif %}