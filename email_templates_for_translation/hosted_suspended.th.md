---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
ร้านค้าถูกระงับ - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          บัญชีถูกระงับ
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          ร้านค้าของคุณ <strong>{{ store_name }}</strong> ถูกระงับเนื่องจากค่าบริการยังไม่ได้ชำระ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          สิ่งนี้หมายถึงอะไร
        </mj-text>
        <mj-text font-size="14px">
          ร้านค้าของคุณอยู่ในโหมดอ่านเท่านั้นขณะนี้ — ลูกค้าสามารถเข้าชมได้ แต่การสั่งซื้อถูกระงับ ข้อมูลของคุณปลอดภัย และจะถูกเก็บรักษาไว้เป็นเวลา 30 วัน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          เพื่อคืนสิทธิ์การเข้าถึงทั้งหมด กรุณาอัปเดตวิธีการชำระเงินและชำระยอดค้างชำระ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="เปิดใช้งานร้านค้าของคุณอีกครั้ง" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ร้านค้าถูกระงับ - {{ store_name }}

สวัสดี {{ name|default:'there' }},

ร้านค้าของคุณ {{ store_name }} ถูกระงับเนื่องจากค่าบริการยังไม่ได้ชำระ

สิ่งนี้หมายถึงอะไร:
ร้านค้าของคุณอยู่ในโหมดอ่านเท่านั้นขณะนี้ — ลูกค้าสามารถเข้าชมได้ แต่การสั่งซื้อถูกระงับ ข้อมูลของคุณปลอดภัย และจะถูกเก็บรักษาไว้เป็นเวลา 30 วัน

เพื่อคืนสิทธิ์การเข้าถึงทั้งหมด กรุณาอัปเดตวิธีการชำระเงินและชำระยอดค้างชำระ

เปิดใช้งานร้านค้าของคุณอีกครั้ง: https://spwig.com/account

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}