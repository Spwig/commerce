---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
การอัปเดตการสมัครเป็นพันธมิตร

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
          การอัปเดตการสมัคร
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
          ขอบคุณที่สนใจในการเข้าร่วมโปรแกรมพันธมิตร {{ shop_name }}
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          หลังจากตรวจสอบการสมัครของคุณ เราได้ตัดสินใจว่าจะไม่ดำเนินการต่อไปในขณะนี้
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          ข้อนี้มีผลจากข้อกำหนดของโปรแกรมพันธมิตรของเราในปัจจุบัน และอาจไม่สะท้อนถึงคุณสมบัติหรือศักยภาพของคุณ
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          คุณยินดีที่จะสมัครใหม่ในอนาคตหากสถานการณ์ของคุณเปลี่ยนไป
        </mj-text>
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
การอัปเดตการสมัครเป็นพันธมิตร

สวัสดี {{ affiliate_name }},

ขอบคุณที่สนใจในการเข้าร่วมโปรแกรมพันธมิตร {{ shop_name }}

หลังจากตรวจสอบการสมัครของคุณ เราได้ตัดสินใจว่าจะไม่ดำเนินการต่อไปในขณะนี้

ข้อนี้มีผลจากข้อกำหนดของโปรแกรมพันธมิตรของเราในปัจจุบัน และอาจไม่สะท้อนถึงคุณสมบัติหรือศักยภาพของคุณ

คุณยินดีที่จะสมัครใหม่ในอนาคตหากสถานการณ์ของคุณเปลี่ยนไป

{{ shop_name }}
คำถาม? ติดต่อ {{ support_email }}