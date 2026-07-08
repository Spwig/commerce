---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
ดำเนินการคืนเงินแล้ว - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          ดำเนินการคืนเงินแล้ว
        </mj-text>
        <mj-text>
          ได้ดำเนินการคืนเงินสำหรับคำสั่งซื้อ #{{ order_number }} แล้ว
        </mj-text>
        <mj-text>
          <strong>จำนวนเงินคืน:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          จำนวนเงินคืนจะปรากฏในบัญชีของคุณภายใน {{ refund_days }} วันทำการ
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ดำเนินการคืนเงินแล้ว

ได้ดำเนินการคืนเงินสำหรับคำสั่งซื้อ #{{ order_number }} แล้ว

จำนวนเงินคืน: {{ refund_amount }}

จำนวนเงินคืนจะปรากฏในบัญชีของคุณภายใน {{ refund_days }} วันทำการ
