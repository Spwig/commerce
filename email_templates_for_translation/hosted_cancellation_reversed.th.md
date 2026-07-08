---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
การยกเลิกถูกยกเลิก - {{ store_name }}

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
          การยกเลิกถูกยกเลิก
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
          สวัสดีค่ะ,
        </mj-text>
        <mj-text>
          การขอยกเลิกของคุณสำหรับ <strong>{{ store_name }}</strong> ถูกยกเลิกแล้ว สมาชิก <strong>{{ plan_name }}</strong> ของคุณจะดำเนินต่อไปตามปกติ — ไม่จำเป็นต้องมีการกระทำใดๆ จากคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          รายละเอียดการสมัครสมาชิก
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          แผน: {{ plan_name }}
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
          ร้านค้าของคุณยังคงดำเนินการตามปกติ การเรียกเก็บเงินจะดำเนินต่อไปในวันที่ระบุไว้ด้านบน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
การยกเลิกถูกยกเลิก - {{ store_name }}

สวัสดีค่ะ,

การขอยกเลิกของคุณสำหรับ {{ store_name }} ถูกยกเลิกแล้ว สมาชิก {{ plan_name }} ของคุณจะดำเนินต่อไปตามปกติ — ไม่จำเป็นต้องมีการกระทำใดๆ จากคุณ

รายละเอียดการสมัครสมาชิก:
- แผน: {{ plan_name }}
- วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}

ร้านค้าของคุณยังคงดำเนินการตามปกติ การเรียกเก็บเงินจะดำเนินต่อไปในวันที่ระบุไว้ด้านบน

{% if admin_url %}ไปที่ร้านค้าของคุณ: {{ admin_url }}

{% endif %}ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}