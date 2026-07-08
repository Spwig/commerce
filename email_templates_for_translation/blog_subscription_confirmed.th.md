---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
โปรดยืนยันการสมัครสมาชิกของคุณใน {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ยืนยันการสมัครสมาชิกของคุณ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          คุณ {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ขอบคุณที่สมัครสมาชิกใน {{ blog_name }}! เพื่อให้การสมัครสมาชิกของคุณสมบูรณ์และเริ่มรับการอัปเดต โปรดยืนยันที่อยู่อีเมลของคุณ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          ยืนยันการสมัครสมาชิก
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ไม่สามารถคลิกปุ่มได้? คัดลอกและวางลิงก์นี้ลงในเบราว์เซอร์ของคุณ:
              <br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">
                {{ confirmation_url }}
              </span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>ทำไมถึงต้องยืนยัน?</strong>
          <br/>
          การยืนยันอีเมลช่วยให้เราแน่ใจว่าคุณต้องการรับการอัปเดตและป้องกันการสแปม ความเป็นส่วนตัวและกล่องจดหมายของคุณมีความสำคัญต่อเรา
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ไม่ได้สมัครสมาชิก? คุณสามารถปลอดภัยใจได้โดยไม่ต้องสนใจอีเมลนี้
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ยืนยันการสมัครสมาชิกของคุณ

คุณ {{ subscriber_name }},

ขอบคุณที่สมัครสมาชิกใน {{ blog_name }}! เพื่อให้การสมัครสมาชิกของคุณสมบูรณ์และเริ่มรับการอัปเดต โปรดยืนยันที่อยู่อีเมลของคุณ

ยืนยันการสมัครสมาชิก: {{ confirmation_url }}

ทำไมถึงต้องยืนยัน?
การยืนยันอีเมลช่วยให้เราแน่ใจว่าคุณต้องการรับการอัปเดตและป้องกันการสแปม ความเป็นส่วนตัวและกล่องจดหมายของคุณมีความสำคัญต่อเรา

ไม่ได้สมัครสมาชิก? คุณสามารถปลอดภัยใจได้โดยไม่ต้องสนใจอีเมลนี้