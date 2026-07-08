---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
ยินดีต้อนรับกลับ! {{ store_name }} กลับมาออนไลน์อีกครั้งแล้ว

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ยินดีต้อนรับกลับ!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} กลับมาออนไลน์อีกครั้งแล้ว
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          ยินดีต้อนรับ,
        </mj-text>
        <mj-text>
          ข่าวดี! ร้านค้าของคุณ <strong>{{ store_name }}</strong> ได้รับการเปิดใช้งานอีกครั้งแล้ว สมาชิก <strong>{{ plan_name }}</strong> ของคุณตอนนี้เป็นที่ใช้งานแล้ว และร้านค้าของคุณกำลังกลับมาออนไลน์อีกครั้ง
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          รายละเอียดการเปิดใช้งานอีกครั้ง
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          แผน: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          การชำระเงินที่ดำเนินการ: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          ร้านค้าของคุณกำลังกลับมาออนไลน์อีกครั้ง อาจใช้เวลาไม่กี่นาทีในการกู้คืนทุกอย่างให้สมบูรณ์ เมื่อเปิดใช้งานแล้ว ร้านค้าของคุณจะสามารถเข้าถึงได้ที่ {{ store_url }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ยินดีต้อนรับกลับ! {{ store_name }} กลับมาออนไลน์อีกครั้งแล้ว

ยินดีต้อนรับ,

ข่าวดี! ร้านค้าของคุณ {{ store_name }} ได้รับการเปิดใช้งานอีกครั้งแล้ว สมาชิก {{ plan_name }} ของคุณตอนนี้เป็นที่ใช้งานแล้ว และร้านค้าของคุณกำลังกลับมาออนไลน์อีกครั้ง

รายละเอียดการเปิดใช้งานอีกครั้ง:
- แผน: {{ plan_name }}
- การชำระเงินที่ดำเนินการ: {{ currency }}{{ amount }}
- วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}

ร้านค้าของคุณกำลังกลับมาออนไลน์อีกครั้ง อาจใช้เวลาไม่กี่นาทีในการกู้คืนทุกอย่างให้สมบูรณ์ เมื่อเปิดใช้งานแล้ว ร้านค้าของคุณจะสามารถเข้าถึงได้ที่ {{ store_url }}

ไปที่ร้านค้าของคุณ: {{ admin_url }}

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}