---
template_type: hosted_payment_recovered
category: License
---

# Email Template: hosted_payment_recovered

## Subject
การชำระเงินสำเร็จ - {{ store_name }}

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
          การชำระเงินสำเร็จ
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
          ข่าวดี! การชำระเงินของคุณ <strong>{{ currency }}{{ amount }}</strong> สำหรับ <strong>{{ plan_name }}</strong> ได้รับการประมวลผลสำเร็จแล้ว สมาชิกของคุณยังคงดำเนินต่อไปโดยไม่มีการขัดข้อง
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
การชำระเงินสำเร็จ - {{ store_name }}

สวัสดี {{ name|default:'there' }},

ข่าวดี! การชำระเงินของคุณ {{ currency }}{{ amount }} สำหรับ {{ plan_name }} ได้รับการประมวลผลสำเร็จแล้ว สมาชิกของคุณยังคงดำเนินต่อไปโดยไม่มีการขัดข้อง

ไปที่ร้านของคุณ: {{ admin_url }}

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}