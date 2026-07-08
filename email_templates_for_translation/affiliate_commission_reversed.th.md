---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
คืนค่าคอมมิชชัน - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          คืนค่าคอมมิชชัน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          สวัสดี {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          ค่าคอมมิชชันสำหรับคำสั่งซื้อ #{{ order_number }} ({{ commission_amount }}) ถูกคืนเนื่องจากลูกค้าได้ขอคืนเงิน
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          เมื่อลูกค้าขอคืนเงิน ค่าคอมมิชชันที่เกี่ยวข้องจะถูกคืนอัตโนมัติเพื่อให้การบัญชีเป็นไปอย่างถูกต้อง
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          นี่เป็นส่วนหนึ่งของกระบวนการพันธมิตรที่ปกติ โปรดดำเนินการส่งเสริม {{ shop_name }} เพื่อรับค่าคอมมิชชันใหม่!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          ดูแดชบอร์ดพันธมิตร
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          มีคำถาม? <a href="mailto:{{ support_email }}" style="color: #007bff;">ติดต่อฝ่ายสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
คืนค่าคอมมิชชัน - คำสั่งซื้อ #{{ order_number }}

สวัสดี {{ affiliate_name }},

ค่าคอมมิชชันสำหรับคำสั่งซื้อ #{{ order_number }} ({{ commission_amount }}) ถูกคืนเนื่องจากลูกค้าได้ขอคืนเงิน

เมื่อลูกค้าขอคืนเงิน ค่าคอมมิชชันที่เกี่ยวข้องจะถูกคืนอัตโนมัติเพื่อให้การบัญชีเป็นไปอย่างถูกต้อง

นี่เป็นส่วนหนึ่งของกระบวนการพันธมิตรที่ปกติ โปรดดำเนินการส่งเสริม {{ shop_name }} เพื่อรับค่าคอมมิชชันใหม่!

ดูแดชบอร์ดของคุณ: {{ portal_url }}

{{ shop_name }}
คำถาม? ติดต่อ {{ support_email }}