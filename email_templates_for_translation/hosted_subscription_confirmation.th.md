---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
ยืนยันการสมัครสมาชิก - {{ store_name }}

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
          ยืนยันการสมัครสมาชิก!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          ยินดีต้อนรับสู่ Spwig
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
          ขอบคุณที่สมัครสมาชิก! แผน {{ plan_name }} สำหรับ {{ store_name }} ของคุณได้รับการยืนยันแล้ว。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          รายละเอียดแผน
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          แผน: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ช่วงเวลาการเรียกเก็บ: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          จำนวนเงิน: {{ currency }}{{ amount }}{% if intro_period %} (อัตราเริ่มต้น){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          อัตราเริ่มต้นของคุณมีผลในช่วง {{ intro_period }} หลังจากนั้น แผนของคุณจะถูกเรียกเก็บเงินที่ {{ currency }}{{ full_amount }}/{{ billing_interval }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          ร้านค้าของคุณกำลังถูกตั้งค่าในขณะนี้ และคุณจะได้รับอีเมลอีกฉบับเมื่อพร้อมใช้งาน
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ยืนยันการสมัครสมาชิก!

สวัสดี {{ name|default:'there' }},

ขอบคุณที่สมัครสมาชิก! แผน {{ plan_name }} สำหรับ {{ store_name }} ของคุณได้รับการยืนยันแล้ว。

รายละเอียดแผน:
- แผน: {{ plan_name }}
- ช่วงเวลาการเรียกเก็บ: {{ billing_interval }}
- จำนวนเงิน: {{ currency }}{{ amount }}{% if intro_period %} (อัตราเริ่มต้น){% endif %}
{% if intro_period %}
นี่คืออัตราเริ่มต้นของคุณในช่วง {{ intro_period }} หลังจากนั้น แผนของคุณจะถูกเรียกเก็บเงินที่ {{ currency }}{{ full_amount }}/{{ billing_interval }}。
{% endif %}
ร้านค้าของคุณกำลังถูกตั้งค่าในขณะนี้ และคุณจะได้รับอีเมลอีกฉบับเมื่อพร้อมใช้งาน

วันที่เรียกเก็บเงินครั้งต่อไป: {{ next_billing_date }}

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}