---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
결제 실패 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          결제 실패
        </mj-text>
        <mj-text>
          주문 #{{ order_number }}에 대한 결제 시도가 실패했습니다.
        </mj-text>
        <mj-text>
          <strong>고객:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>금액:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>에러:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          관리자에서 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
결제 실패

주문 #{{ order_number }}에 대한 결제 시도가 실패했습니다.

고객: {{ customer_name }}
금액: {{ order_total }}
에러: {{ error_message }}

관리자에서 보기: {{ admin_order_url }}