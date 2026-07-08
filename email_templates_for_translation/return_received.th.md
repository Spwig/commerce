---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
เราได้รับการคืนสินค้าของคุณแล้ว - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          ได้รับการคืนสินค้า
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          คำสั่งซื้อ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          เราได้รับสินค้าคืนสำหรับคำสั่งซื้อ <strong>#{{ order_number }}</strong> ของคุณแล้ว
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>สิ่งที่จะเกิดขึ้นต่อไป:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. ทีมงานของเราจะตรวจสอบสินค้าที่คืนภายใน 2-3 วันทำการ<br/>
          2. เราจะตรวจสอบว่าสินค้าอยู่ในสภาพเดิม<br/>
          3. เมื่อการตรวจสอบเสร็จสิ้น เราจะดำเนินการคืนเงินให้คุณ<br/>
          4. คุณจะได้รับอีเมลยืนยันเมื่อการคืนเงินเสร็จสิ้น
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          การคืนเงินจะถูกเครดิตเข้าสู่วิธีการชำระเงินเดิมของคุณ และอาจใช้เวลา 5-10 วันทำการเพื่อปรากฏในบัญชีของคุณ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ขอบคุณสำหรับความอดทนของคุณ!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ได้รับการคืนสินค้า - คำสั่งซื้อ #{{ order_number }}

สวัสดี {{ customer_name }},

เราได้รับสินค้าคืนสำหรับคำสั่งซื้อ #{{ order_number }} ของคุณแล้ว

สิ่งที่จะเกิดขึ้นต่อไป:
1. ทีมงานของเราจะตรวจสอบสินค้าที่คืนภายใน 2-3 วันทำการ
2. เราจะตรวจสอบว่าสินค้าอยู่ในสภาพเดิม
3. เมื่อการตรวจสอบเสร็จสิ้น เราจะดำเนินการคืนเงินให้คุณ
4. คุณจะได้รับอีเมลยืนยันเมื่อการคืนเงินเสร็จสิ้น

การคืนเงินจะถูกเครดิตเข้าสู่วิธีการชำระเงินเดิมของคุณ และอาจใช้เวลา 5-10 วันทำการเพื่อปรากฏในบัญชีของคุณ

ขอบคุณสำหรับความอดทนของคุณ!