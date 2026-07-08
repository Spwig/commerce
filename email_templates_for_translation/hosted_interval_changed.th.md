---
template_type: hosted_interval_changed
category: License
---

# Email Template: hosted_interval_changed

## Subject
การอัปเดตการเรียกเก็บเงิน - {{ store_name }}

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
          การอัปเดตการเรียกเก็บเงิน
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
          Hi there,
        </mj-text>
        <mj-text>
          การอัปเดตช่วงเวลาการเรียกเก็บเงินสำหรับแผน {{ plan_name }} ของคุณบน {{ store_name }} ได้ถูกปรับปรุงแล้ว
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Billing Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          การเรียกเก็บเงิน
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          แผน: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ช่วงเวลาการเรียกเก็บเงินก่อนหน้า: {{ old_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ช่วงเวลาการเรียกเก็บเงินใหม่: {{ new_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          การสมัครสมาชิกของคุณยังคงเป็นปัจจุบัน คุณสามารถจัดการการตั้งค่าการเรียกเก็บเงินได้ทุกเมื่อจากบัญชีของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="จัดการการสมัครสมาชิก" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
การอัปเดตการเรียกเก็บเงิน - {{ store_name }}

Hi there,

การอัปเดตช่วงเวลาการเรียกเก็บเงินสำหรับแผน {{ plan_name }} ของคุณบน {{ store_name }} ได้ถูกปรับปรุงแล้ว

การเรียกเก็บเงิน:
- แผน: {{ plan_name }}
- ช่วงเวลาการเรียกเก็บเงินก่อนหน้า: {{ old_interval }}
- ช่วงเวลาการเรียกเก็บเงินใหม่: {{ new_interval }}
- วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}

การสมัครสมาชิกของคุณยังคงเป็นปัจจุบัน คุณสามารถจัดการการตั้งค่าการเรียกเก็บเงินได้ทุกเมื่อจากบัญชีของคุณ

จัดการการสมัครสมาชิก: https://spwig.com/account

Need help? Contact {{ support_email }}