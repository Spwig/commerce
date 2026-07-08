---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
환불 완료 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          환불 완료
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
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
          주문 <strong>#{{ order_number }}</strong>에 대한 반품이 검토되었으며, 환불이 완료되었습니다.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              환불 정보
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>환불 금액:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>재고 수수료:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>참고:</strong> 환불이 귀하의 계정에 나타나는 데 5~10 영업일이 소요될 수 있으며, 이는 귀하의 결제 제공업체에 따라 다를 수 있습니다.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          환불에 대해 궁금한 점이 있다면, 저희 지원팀에 문의해 주시기 바랍니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
환불 완료 - 주문 #{{ order_number }}

안녕하세요, {{ customer_name }},

주문 #{{ order_number }}에 대한 반품이 검토되었으며, 환불이 완료되었습니다.

환불 정보:
- 환불 금액: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- 재고 수수료: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

참고: 환불이 귀하의 계정에 나타나는 데 5~10 영업일이 소요될 수 있으며, 이는 귀하의 결제 제공업체에 따라 다를 수 있습니다.

환불에 대해 궁금한 점이 있다면, 저희 지원팀에 문의해 주시기 바랍니다.