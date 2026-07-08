---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
การชำระเงินล้มเหลว - {{ store_name }}

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
    <mj-section background-color="#d97706" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ปัญหาการชำระเงิน
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          ต้องดำเนินการสำหรับ {{ store_name }}
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
          เราไม่สามารถดำเนินการชำระเงินของคุณสำหรับ <strong>{{ plan_name }}</strong> ได้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          รายละเอียดการชำระเงิน
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          จำนวนเงิน: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          แพ็กเกจ: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}. เพื่อหลีกเลี่ยงการหยุดชะงักของบริการ กรุณาอัปเดตวิธีการชำระเงินของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Update Payment Method" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ปัญหาการชำระเงิน - {{ store_name }}

สวัสดี {{ name|default:'there' }},

เราไม่สามารถดำเนินการชำระเงินของคุณสำหรับ {{ plan_name }} ได้

รายละเอียดการชำระเงิน:
- จำนวนเงิน: {{ currency }}{{ amount }}
- แพ็กเกจ: {{ plan_name }}

{{ retry_info }}. เพื่อหลีกเลี่ยงการหยุดชะงักของบริการ กรุณาอัปเดตวิธีการชำระเงินของคุณ

อัปเดตวิธีการชำระเงิน: https://spwig.com/account

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}