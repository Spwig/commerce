---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
결제 완료 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          결제 완료
        </mj-text>
        <mj-text>
          주문 #{{ order_number }}의 결제가 성공적으로 처리되었습니다.
        </mj-text>
        <mj-text>
          <strong>결제 금액:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>결제 방법:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
결제 완료

주문 #{{ order_number }}의 결제가 성공적으로 처리되었습니다.

결제 금액: {{ amount_paid }}
결제 방법: {{ payment_method }}

