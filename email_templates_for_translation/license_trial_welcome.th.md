---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
ยินดีต้อนรับสู่ Spwig - การทดลองใช้งานฟรี {{ trial_days }} วันของคุณ

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ยินดีต้อนรับสู่ Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          การทดลองใช้งานฟรีของคุณ {{ trial_days }} วันพร้อมใช้งานแล้ว
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
          ขอบคุณที่ลองใช้ <strong>{{ product_name }}</strong>! การทดลองใช้งานของคุณได้ถูกเปิดใช้งานแล้ว และคุณมี <strong>{{ trial_days }} วัน</strong> เพื่อสำรวจทุกสิ่งที่ Spwig มีให้คุณ{% if includes_pos %}, รวมถึงระบบ Point of Sale ของเรา{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          โทเคนการตั้งค่าของคุณ
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          กรุณาใช้โทเคนนี้ในระหว่างการติดตั้งเพื่อเปิดใช้งานร้านค้าทดลองของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          การเริ่มต้นใช้งาน
        </mj-text>
        <mj-text font-size="14px">
          1. โปรดติดตามคู่มือการตั้งค่าของเราเพื่อติดตั้ง Spwig บนเซิร์ฟเวอร์ของคุณ
        </mj-text>
        <mj-text font-size="14px">
          2. กรุณาใส่โทเคนการตั้งค่าของคุณเมื่อถูกขอให้ใส่ในระหว่างการติดตั้ง
        </mj-text>
        <mj-text font-size="14px">
          3. เริ่มสร้างร้านค้าออนไลน์ของคุณ!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          สิ่งที่รวมอยู่ในช่วงทดลองใช้งานของคุณ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          สามารถเข้าถึงฟีเจอร์หลักทั้งหมดได้เต็มที่เป็นเวลา {{ trial_days }} วัน
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          แคตตาล็อกสินค้า, คำสั่งซื้อ, และการจัดการลูกค้า
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          การปรับแต่งธีมและการสร้างหน้าเว็บ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          การผสานระบบผู้ให้บริการชำระเงินและจัดส่ง
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ระบบ Point of Sale (POS)
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          การทดลองใช้งานของคุณจะหมดอายุใน {{ trial_days }} วัน เมื่อคุณพร้อมแล้ว โปรดอัปเกรดเป็นใบอนุญาตเต็มรูปแบบเพื่อรักษาการดำเนินงานของร้านค้าของคุณโดยไม่มีการสูญเสียข้อมูลใดๆ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ยินดีต้อนรับสู่ Spwig!
การทดลองใช้งานฟรีของคุณ {{ trial_days }} วันพร้อมใช้งานแล้ว

สวัสดี {{ customer_name }},

ขอบคุณที่ลองใช้ {{ product_name }}! การทดลองใช้งานของคุณได้ถูกเปิดใช้งานแล้ว และคุณมี {{ trial_days }} วัน เพื่อสำรวจทุกสิ่งที่ Spwig มีให้คุณ{% if includes_pos %}, รวมถึงระบบ Point of Sale ของเรา{% endif %}.

YOUR SETUP TOKEN:
{{ setup_token }}
ใช้โทเคนนี้ในระหว่างการติดตั้งเพื่อเปิดใช้งานร้านค้าทดลองของคุณ

Getting Started:
1. โปรดติดตามคู่มือการตั้งค่าของเราเพื่อติดตั้ง Spwig บนเซิร์ฟเวอร์ของคุณ
2. กรุณาใส่โทเคนการตั้งค่าของคุณเมื่อถูกขอให้ใส่ในระหว่างการติดตั้ง
3. เริ่มสร้างร้านค้าออนไลน์ของคุณ!

View Setup Guide: {{ setup_url }}

What's Included in Your Trial:
- สามารถเข้าถึงฟีเจอร์หลักทั้งหมดได้เต็มที่เป็นเวลา {{ trial_days }} วัน
- แคตตาล็อกสินค้า, คำสั่งซื้อ, และการจัดการลูกค้า
- การปรับแต่งธีมและการสร้างหน้าเว็บ
- การผสานระบบผู้ให้บริการชำระเงินและจัดส่ง
{% if includes_pos %}- ระบบ Point of Sale (POS){% endif %}

การทดลองใช้งานของคุณจะหมดอายุใน {{ trial_days }} วัน เมื่อคุณพร้อมแล้ว โปรดอัปเกรดเป็นใบอนุญาตเต็มรูปแบบเพื่อรักษาการดำเนินงานของร้านค้าของคุณโดยไม่มีการสูญเสียข้อมูลใดๆ

Need help? Contact {{ support_email }}