---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
ร้านค้าของคุณพร้อมใช้งานแล้ว - {{ store_name }}

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
          ร้านค้าของคุณพร้อมใช้งานแล้ว!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} พร้อมให้คุณใช้งานแล้ว
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          สวัสดี {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          ข่าวดี! ร้านค้า Spwig ของคุณ <strong>{{ store_name }}</strong> ได้ถูกตั้งค่าและพร้อมใช้งานแล้ว คุณสามารถเริ่มตั้งค่าสินค้า แบรนด์ และวิธีการชำระเงินได้ทันที
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          รายละเอียดร้านค้าของคุณ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          URL ร้านค้า: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          แดชบอร์ดผู้ดูแล: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ภูมิภาค: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ขั้นตอนเริ่มต้น
        </mj-text>
        <mj-text font-size="14px">
          1. เข้าสู่แดชบอร์ดผู้ดูแลโดยใช้อีเมลและรหัสผ่านที่คุณตั้งไว้ตอนชำระเงิน
        </mj-text>
        <mj-text font-size="14px">
          2. เพิ่มโลโก้และแบรนด์ของร้านค้าภายใต้ Design > Theme Settings
        </mj-text>
        <mj-text font-size="14px">
          3. เพิ่มสินค้าแรกของคุณภายใต้ Catalog > Products
        </mj-text>
        <mj-text font-size="14px">
          4. ตั้งค่าผู้ให้บริการชำระเงินภายใต้ Settings > Payment Providers
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ร้านค้าของคุณพร้อมใช้งานแล้ว!

{{ store_name }} พร้อมให้คุณใช้งานแล้ว。

สวัสดี {{ name|default:'there' }},

ข่าวดี! ร้านค้า Spwig ของคุณ {{ store_name }} ได้ถูกตั้งค่าและพร้อมใช้งานแล้ว คุณสามารถเริ่มตั้งค่าสินค้า แบรนด์ และวิธีการชำระเงินได้ทันที

รายละเอียดร้านค้าของคุณ:
- URL ร้านค้า: {{ store_url }}
- แดชบอร์ดผู้ดูแล: {{ admin_url }}
- ภูมิภาค: {{ region }}

ขั้นตอนเริ่มต้น:
1. เข้าสู่แดชบอร์ดผู้ดูแลโดยใช้อีเมลและรหัสผ่านที่คุณตั้งไว้ตอนชำระเงิน
2. เพิ่มโลโก้และแบรนด์ของร้านค้าภายใต้ Design > Theme Settings
3. เพิ่มสินค้าแรกของคุณภายใต้ Catalog > Products
4. ตั้งค่าผู้ให้บริการชำระเงินภายใต้ Settings > Payment Providers

ไปที่แดชบอร์ดผู้ดูแล: {{ admin_url }}

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}