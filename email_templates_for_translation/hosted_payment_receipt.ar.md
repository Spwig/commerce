---
template_type: hosted_payment_receipt
category: License
---

# Email Template: hosted_payment_receipt

## Subject
ใบเสร็จรับเงิน - {{ store_name }}

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
          ใบเสร็จรับเงิน
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
          การชำระเงินของคุณได้รับการยืนยันแล้ว นี่คือรายละเอียดสำหรับบันทึกของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Receipt Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          รายละเอียดใบเสร็จ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          จำนวนเงิน: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          แพ็กเกจ: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ช่วงเวลา: {{ period_start }} - {{ period_end }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}
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
ใบเสร็จรับเงิน - {{ store_name }}

สวัสดี {{ name|default:'there' }},

การชำระเงินของคุณได้รับการยืนยันแล้ว นี่คือรายละเอียดสำหรับบันทึกของคุณ

รายละเอียดใบเสร็จ:
- จำนวนเงิน: {{ currency }}{{ amount }}
- แพ็กเกจ: {{ plan_name }}
- ช่วงเวลา: {{ period_start }} - {{ period_end }}
- วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}

ไปยังร้านของคุณ: {{ admin_url }}

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}