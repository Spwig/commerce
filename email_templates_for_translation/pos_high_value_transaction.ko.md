---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 대규모 거래: {{ transaction_amount }}에서 {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 대규모 거래
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          대규모 거래 처리 완료
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }}에서 {{ transaction_amount }}의 거래가 처리되었습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              거래 상세 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>금액:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>단말기:</strong> {{ terminal_name }}<br/>
              <strong>직원:</strong> {{ cashier_name }}<br/>
              <strong>시간:</strong> {{ transaction_time }}<br/>
              <strong>거래 ID:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          결제 정보:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          항목 요약:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>총 항목 수:</strong> {{ item_count }}<br/>
              <strong>소계:</strong> {{ subtotal }}<br/>
              <strong>세금:</strong> {{ tax_amount }}<br/>
              <strong>총액:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          고객 정보:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              이 알림은 사기 방지 및 모니터링 목적의 {{ threshold_amount }} 이상의 모든 거래에 대해 전송됩니다.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          거래 확인
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          영수증 확인
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 대규모 거래

대규모 거래 처리 완료

{{ terminal_name }}에서 {{ transaction_amount }}의 거래가 처리되었습니다.

거래 상세 정보:
- 금액: {{ transaction_amount }}
- 단말기: {{ terminal_name }}
- 직원: {{ cashier_name }}
- 시간: {{ transaction_time }}
- 거래 ID: {{ transaction_id }}

결제 정보:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

항목 요약:
- 총 항목 수: {{ item_count }}
- 소계: {{ subtotal }}
- 세금: {{ tax_amount }}
- 총액: {{ transaction_amount }}

{% if customer_info %}
고객 정보:
{{ customer_info }}
{% endif %}

이 알림은 사기 방지 및 모니터링 목적의 {{ threshold_amount }} 이상의 모든 거래에 대해 전송됩니다.

거래 확인: {{ transaction_url }}
영수증 확인: {{ receipt_url }}