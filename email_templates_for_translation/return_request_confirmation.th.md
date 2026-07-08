---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
ได้รับคำขอคืนสินค้า - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          ได้รับคำขอคืนสินค้า
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
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
          เราได้รับคำขอคืนสินค้าสำหรับคำสั่งซื้อ <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการคืนสินค้า:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>เหตุผล:</strong> {{ return_reason }}<br/>
              <strong>สินค้า:</strong> {{ items_count }} รายการ<br/>
              <strong>สถานะ:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ขั้นตอนต่อไปคืออะไร?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. ทีมงานของเราจะตรวจสอบคำขอคืนสินค้าภายใน 24-48 ชั่วโมง<Br/>
          2. เมื่อได้รับการอนุมัติ เราจะส่งป้ายกำกับการคืนสินค้าให้คุณทางอีเมล<Br/>
          3. บรรจุสินค้าอย่างปลอดภัยและติดป้ายกำกับคืนสินค้า<Br/>
          4. ส่งแพ็กเกจไปยังสถานที่จัดส่งใกล้คุณที่สุด<Br/>
          5. การคืนเงินของคุณจะถูกดำเนินการเมื่อเราได้รับและตรวจสอบสินค้า
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          หากคุณมีคำถามใด ๆ กรุณาอย่าลังเลที่จะติดต่อเรา
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
คำขอคืนสินค้าได้รับการยืนยัน
คำสั่งซื้อ #{{ order_number }}

สวัสดี {{ customer_name }},

เราได้รับคำขอคืนสินค้าสำหรับคำสั่งซื้อ #{{ order_number }}.

รายละเอียดการคืนสินค้า:
- เหตุผล: {{ return_reason }}
- สินค้า: {{ items_count }} รายการ
- สถานะ: {{ return_status }}

ขั้นตอนต่อไปคืออะไร?
1. ทีมงานของเราจะตรวจสอบคำขอคืนสินค้าภายใน 24-48 ชั่วโมง
2. เมื่อได้รับการอนุมัติ เราจะส่งป้ายกำกับการคืนสินค้าให้คุณทางอีเมล
3. บรรจุสินค้าอย่างปลอดภัยและติดป้ายกำกับคืนสินค้า
4. ส่งแพ็กเกจไปยังสถานที่จัดส่งใกล้คุณที่สุด
5. การคืนเงินของคุณจะถูกดำเนินการเมื่อเราได้รับและตรวจสอบสินค้า

หากคุณมีคำถามใด ๆ กรุณาอย่าลังเลที่จะติดต่อเรา.