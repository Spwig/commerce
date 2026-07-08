---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
สร้างบัญชีของคุณที่ {{ site_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          คุณถูกเชิญมา!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          สร้างบัญชีของคุณที่ {{ site_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          สวัสดี {{ customer_name }},
        </mj-text>
        <mj-text>
          เราสังเกตเห็นว่าคุณได้ช้อปปิ้งกับเราในฐานะผู้ใช้ทั่วไป สร้างบัญชีเต็มรูปแบบเพื่อปลดล็อกสิทธิประโยชน์ เช่น การติดตามคำสั่งซื้อ การชำระเงินที่รวดเร็ว และข้อเสนอพิเศษ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ประวัติการช้อปปิ้งของคุณ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          จำนวนคำสั่งซื้อทั้งหมด: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ยอดใช้จ่ายทั้งหมด: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ทำไมถึงควรสร้างบัญชี?
        </mj-text>
        <mj-text font-size="14px">
          - ติดตามคำสั่งซื้อและดูประวัติการสั่งซื้อ
        </mj-text>
        <mj-text font-size="14px">
          - ชำระเงินได้รวดเร็วกับข้อมูลที่บันทึกไว้
        </mj-text>
        <mj-text font-size="14px">
          - จัดการที่อยู่และตั้งค่าความชอบของคุณ
        </mj-text>
        <mj-text font-size="14px">
          - รับข้อเสนอและโปรโมชันพิเศษ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          ลิงก์นี้จะช่วยให้คุณตั้งรหัสผ่านสำหรับบัญชีของคุณ ประวัติการสั่งซื้อที่มีอยู่จะถูกเก็บไว้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
คุณถูกเชิญมาสร้างบัญชีของคุณ!

สวัสดี {{ customer_name }},

เราสังเกตเห็นว่าคุณได้ช้อปปิ้งกับเราในฐานะผู้ใช้ทั่วไป สร้างบัญชีเต็มรูปแบบเพื่อปลดล็อกสิทธิประโยชน์ เช่น การติดตามคำสั่งซื้อ การชำระเงินที่รวดเร็ว และข้อเสนอพิเศษ

ประวัติการช้อปปิ้งของคุณ:
- จำนวนคำสั่งซื้อทั้งหมด: {{ total_orders }}
- ยอดใช้จ่ายทั้งหมด: {{ total_spent }}

ทำไมถึงควรสร้างบัญชี?
- ติดตามคำสั่งซื้อและดูประวัติการสั่งซื้อ
- ชำระเงินได้รวดเร็วกับข้อมูลที่บันทึกไว้
- จัดการที่อยู่และตั้งค่าความชอบของคุณ
- รับข้อเสนอและโปรโมชันพิเศษ

สร้างบัญชีของคุณ: {{ activation_url }}

ลิงก์นี้จะช่วยให้คุณตั้งรหัสผ่านสำหรับบัญชีของคุณ ประวัติการสั่งซื้อที่มีอยู่จะถูกเก็บไว้

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}