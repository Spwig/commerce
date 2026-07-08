---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
คำขอรีเซ็ตรหัสผ่าน

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          คำขอรีเซ็ตรหัสผ่าน
        </mj-text>
        <mj-text>
          เราได้รับคำขอในการรีเซ็ตรหัสผ่านของคุณ คลิกปุ่มด้านล่างเพื่อรีเซ็ต
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          รีเซ็ตรหัสผ่าน
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          หากคุณไม่ได้ร้องขอสิ่งนี้ คุณสามารถเพิกเฉยกับอีเมลนี้ได้อย่างปลอดภัย
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          ลิงก์นี้จะหมดอายุใน {{ expiry_hours }} ชั่วโมง
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
คำขอรีเซ็ตรหัสผ่าน

เราได้รับคำขอในการรีเซ็ตรหัสผ่านของคุณ คลิกที่ลิงก์ด้านล่างเพื่อรีเซ็ต

{{ reset_url }}

หากคุณไม่ได้ร้องขอสิ่งนี้ คุณสามารถเพิกเฉยกับอีเมลนี้ได้อย่างปลอดภัย
ลิงก์นี้จะหมดอายุใน {{ expiry_hours }} ชั่วโมง

