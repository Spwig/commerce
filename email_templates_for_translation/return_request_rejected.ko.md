---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
반품 요청 업데이트 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          반품 요청 업데이트
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          주문 <strong>#{{ order_number }}</strong>에 대한 반품 요청을 검토했으나, 현재 승인할 수 없습니다.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>이유:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          이 결정에 대해 궁금한 점이 있거나 오류가 발생했다고 생각하시면, 지원 팀에 연락 주시기 바랍니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
반품 요청 업데이트 - 주문 #{{ order_number }}

안녕하세요, {{ customer_name }},

주문 #{{ order_number }}에 대한 반품 요청을 검토했으나, 현재 승인할 수 없습니다.

{% if rejection_reason %}이유: {{ rejection_reason }}{% endif %}

이 결정에 대해 궁금한 점이 있거나 오류가 발생했다고 생각하시면, 지원 팀에 연락 주시기 바랍니다.