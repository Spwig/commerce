---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
โปรดยืนยันการสมัครสมาชิกของคุณกับ {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ยืนยันการสมัครสมาชิก
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ขอบคุณที่สมัครรับข้อมูลจาก {{ store_name }}! โปรดยืนยันอีเมลของคุณเพื่อเริ่มรับข่าวสารและโปรโมชั่นของเรา
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          ยืนยันการสมัครสมาชิก
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ไม่สามารถคลิกปุ่มได้หรือไม่? คัดลอกและวางลิงก์นี้ลงในเบราว์เซอร์ของคุณ:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>เหตุผลที่ต้องยืนยัน?</strong><br/>
          การยืนยันอีเมลของคุณช่วยให้เราสามารถตรวจสอบได้ว่าคุณต้องการรับข้อมูลของเราจริง ๆ และช่วยให้กล่องขาเข้าของคุณไม่มีอีเมลขยะ
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          คุณไม่ได้สมัครหรือไม่? คุณสามารถลบอีเมลนี้ได้อย่างปลอดภัย
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ยืนยันการสมัครสมาชิกของคุณกับ {{ store_name }}

ขอบคุณที่สมัครรับข้อมูลจาก {{ store_name }}! โปรดยืนยันอีเมลของคุณเพื่อเริ่มรับข่าวสารและโปรโมชั่นของเรา

{{ confirmation_url }}

การยืนยันอีเมลของคุณช่วยให้เราสามารถตรวจสอบได้ว่าคุณต้องการรับข้อมูลของเราจริง ๆ และช่วยให้กล่องขาเข้าของคุณไม่มีอีเมลขยะ

คุณไม่ได้สมัครหรือไม่? คุณสามารถลบอีเมลนี้ได้อย่างปลอดภัย