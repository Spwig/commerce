---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
환불 완료 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          환불 완료
        </mj-text>
        <mj-text>
          주문 #{{ order_number }}에 대한 환불이 처리되었습니다.
        </mj-text>
        <mj-text>
          <strong>환불 금액:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          환불은 {{ refund_days }} 영업일 이내에 귀하의 계정에 나타날 예정입니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
환불 완료

주문 #{{ order_number }}에 대한 환불이 처리되었습니다.

환불 금액: {{ refund_amount }}

환불은 {{ refund_days }} 영업일 이내에 귀하의 계정에 나타날 예정입니다.