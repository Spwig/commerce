---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
อัปเดตสถานะคอมมิชชัน - คำสั่งซื้อ #{{ order_number }}

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
          อัปเดตสถานะคอมมิชชัน
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
          เราอยากแจ้งให้คุณทราบว่าคอมมิชชันสำหรับคำสั่งซื้อ #{{ order_number }} ({{ commission_amount }}) ยังไม่ได้รับการอนุมัติ
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          สิ่งนี้มักเกิดขึ้นเมื่อคำสั่งซื้อถูกยกเลิกหรือคืนเงินก่อนที่ช่วงเวลาของคอมมิชชันจะสิ้นสุด
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          หากคุณมีคำถามเกี่ยวกับคอมมิชชันนี้ กรุณาติดต่อทีมสนับสนุนของเรา
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          ดูแดชบอร์ดผู้พันธมิตร
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          มีคำถาม? <a href="mailto:{{ support_email }}" style="color: #007bff;">ติดต่อทีมสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
อัปเดตสถานะคอมมิชชัน - คำสั่งซื้อ #{{ order_number }}

สวัสดี {{ affiliate_name }},

เราอยากแจ้งให้คุณทราบว่าคอมมิชชันสำหรับคำสั่งซื้อ #{{ order_number }} ({{ commission_amount }}) ยังไม่ได้รับการอนุมัติ

สิ่งนี้มักเกิดขึ้นเมื่อคำสั่งซื้อถูกยกเลิกหรือคืนเงินก่อนที่ช่วงเวลาของคอมมิชชันจะสิ้นสุด

หากคุณมีคำถามเกี่ยวกับคอมมิชชันนี้ กรุณาติดต่อทีมสนับสนุนของเรา

ดูแดชบอร์ดของคุณ: {{ portal_url }}

{{ shop_name }}
คำถาม? ติดต่อ {{ support_email }}
