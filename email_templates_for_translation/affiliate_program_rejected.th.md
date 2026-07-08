---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
การอัปเดตการสมัครใช้งาน

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
          การอัปเดตการสมัครใช้งาน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          คุณ {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          ขอบคุณที่สมัครใช้งานเพื่อโปรโมต {{ program_name }}
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          หลังจากตรวจสอบการสมัครของคุณ เราได้ตัดสินใจไม่ให้การอนุมัติในขณะนี้
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          คุณยังสามารถโปรโมตโปรแกรมอื่น ๆ ในเครือข่ายพันธมิตรของเราได้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          ดูโปรแกรมอื่น ๆ
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
การอัปเดตการสมัครใช้งาน

คุณ {{ affiliate_name }},

ขอบคุณที่สมัครใช้งานเพื่อโปรโมต {{ program_name }}

หลังจากตรวจสอบการสมัครของคุณ เราได้ตัดสินใจไม่ให้การอนุมัติในขณะนี้

คุณยังสามารถโปรโมตโปรแกรมอื่น ๆ ในเครือข่ายพันธมิตรของเราได้

ดูโปรแกรมอื่น ๆ: {{ portal_url }}

{{ shop_name }}
คำถาม? ติดต่อ {{ support_email }}