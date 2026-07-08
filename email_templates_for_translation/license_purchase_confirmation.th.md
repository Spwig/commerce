---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
ใบอนุญาต Spwig ของคุณ - คำสั่งซื้อ #{{ order_number }}

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
          ขอบคุณสำหรับการซื้อสินค้าของคุณ!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          คำสั่งซื้อ #{{ order_number }}
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
          การซื้อสินค้า <strong>{{ product_name }}</strong> ของคุณเสร็จสิ้นแล้ว ด้านล่างนี้คุณจะพบกับคีย์ใบอนุญาตและโทเคนติดตั้งเพื่อเริ่มต้นใช้งาน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          สรุปคำสั่งซื้อ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          สินค้า: {{ product_name }}{% if includes_pos %} (รวม POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          จำนวนเงิน: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          หมายเลขคำสั่งซื้อ: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          คีย์ใบอนุญาตของคุณ
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          โปรดเก็บคีย์นี้ไว้ - คุณจะต้องใช้มันในการติดตั้งใหม่
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          โทเคนติดตั้งของคุณ
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          โปรดใช้โทเคนนี้ในระหว่างการติดตั้งเพื่อเปิดใช้งานร้านค้าของคุณ
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
          1. โปรดติดตามคู่มือการติดตั้งของเราเพื่อติดตั้ง Spwig บนเซิร์ฟเวอร์ของคุณ
        </mj-text>
        <mj-text font-size="14px">
          2. กรอกโทเคนติดตั้งของคุณเมื่อถูกขอในระหว่างการติดตั้ง
        </mj-text>
        <mj-text font-size="14px">
          3. ร้านค้าของคุณจะถูกเปิดใช้งานโดยอัตโนมัติ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          สร้างบัญชีของคุณ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          ตั้งค่ารหัสผ่านเพื่อจัดการใบอนุญาตของคุณ ดาวน์โหลดไฟล์ และรับการอัปเดต
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          ข้อควรระวัง:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          โปรดเก็บอีเมลนี้ไว้ดีๆ - มันมีคีย์ใบอนุญาตและโทเคนติดตั้งของคุณสำหรับอ้างอิงในอนาคต อย่าแบ่งปันข้อมูลเหล่านี้กับผู้อื่น
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ขอบคุณสำหรับการซื้อสินค้าของคุณ!

คำสั่งซื้อ #{{ order_number }}

สวัสดี {{ customer_name }},

การซื้อสินค้า {{ product_name }} ของคุณเสร็จสิ้นแล้ว ด้านล่างนี้คุณจะพบกับคีย์ใบอนุญาตและโทเคนติดตั้งเพื่อเริ่มต้นใช้งาน

สรุปคำสั่งซื้อ:
- สินค้า: {{ product_name }}{% if includes_pos %} (รวม POS){% endif %}
- จำนวนเงิน: {{ price }}
- หมายเลขคำสั่งซื้อ: {{ order_number }}

คีย์ใบอนุญาตของคุณ:
{{ license_key }}
โปรดเก็บคีย์นี้ไว้ - คุณจะต้องใช้มันในการติดตั้งใหม่。

โทเคนติดตั้งของคุณ:
{{ setup_token }}
โปรดใช้โทเคนนี้ในระหว่างการติดตั้งเพื่อเปิดใช้งานร้านค้าของคุณ。

การเริ่มต้นใช้งาน:
1. โปรดติดตามคู่มือการติดตั้งของเราเพื่อติดตั้ง Spwig บนเซิร์ฟเวอร์ของคุณ
2. กรอกโทเคนติดตั้งของคุณเมื่อถูกขอในระหว่างการติดตั้ง
3. ร้านค้าของคุณจะถูกเปิดใช้งานโดยอัตโนมัติ

ดูคู่มือการติดตั้ง: {{ setup_url }}
{% if activation_url %}
สร้างบัญชีของคุณ:
ตั้งค่ารหัสผ่านเพื่อจัดการใบอนุญาตของคุณ ดาวน์โหลดไฟล์ และรับการอัปเดต。
{{ activation_url }}
{% endif %}
ข้อควรระวัง:
โปรดเก็บอีเมลนี้ไว้ดีๆ - มันมีคีย์ใบอนุญาตและโทเคนติดตั้งของคุณสำหรับอ้างอิงในอนาคต อย่าแบ่งปันข้อมูลเหล่านี้กับผู้อื่น。

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}