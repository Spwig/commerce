---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
ยินดีต้อนรับกลับ! บัญชีได้รับการเปิดใช้งานอีกครั้ง

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
          🎉 บัญชีได้รับการเปิดใช้งานอีกครั้ง!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          ยินดีต้อนรับกลับ!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          บัญชีพันธมิตรของคุณได้รับการเปิดใช้งานอีกครั้ง
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
          ข่าวดี! บัญชีพันธมิตรของคุณกับ {{ shop_name }} ได้รับการเปิดใช้งานอีกครั้ง
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          คุณสามารถเริ่มต้นโปรโมตสินค้าของเราและรับรายได้ค่าคอมมิชชั่นได้ทันที
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          เข้าสู่แดชบอร์ดพันธมิตร
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          คำถาม? <a href="mailto:{{ support_email }}" style="color: #007bff;">ติดต่อฝ่ายสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ยินดีต้อนรับกลับ! บัญชีได้รับการเปิดใช้งานอีกครั้ง

สวัสดี {{ affiliate_name }},

ข่าวดี! บัญชีพันธมิตรของคุณกับ {{ shop_name }} ได้รับการเปิดใช้งานอีกครั้ง

คุณสามารถเริ่มต้นโปรโมตสินค้าของเราและรับรายได้ค่าคอมมิชชั่นได้ทันที

เข้าสู่แดชบอร์ดพันธมิตร: {{ portal_url }}

{{ shop_name }}
คำถาม? ติดต่อ {{ support_email }}