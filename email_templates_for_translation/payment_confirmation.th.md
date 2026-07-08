---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
ยืนยันการชำระเงิน - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          ยืนยันการชำระเงิน
        </mj-text>
        <mj-text>
          การชำระเงินสำหรับคำสั่งซื้อ #{{ order_number }} ของคุณได้รับการประมวลผลสำเร็จแล้ว。
        </mj-text>
        <mj-text>
          <strong>จำนวนเงินที่ชำระ:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>วิธีการชำระเงิน:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ยืนยันการชำระเงิน

การชำระเงินสำหรับคำสั่งซื้อ #{{ order_number }} ของคุณได้รับการประมวลผลสำเร็จแล้ว。

จำนวนเงินที่ชำระ: {{ amount_paid }}
วิธีการชำระเงิน: {{ payment_method }}

กรุณาตรวจสอบรายละเอียดการชำระเงินของคุณและติดต่อฝ่ายบริการลูกค้าหากคุณมีคำถามใด ๆ เกี่ยวกับการชำระเงินนี้

ขอบคุณสำหรับการใช้งาน Spwig!