---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
ยืนยันการยกเลิก - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ยืนยันการยกเลิก
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
          การสมัครสมาชิก <strong>{{ plan_name }}</strong> ของคุณถูกยกเลิกแล้ว
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          สิ่งที่จะเกิดขึ้นต่อไป
        </mj-text>
        <mj-text font-size="14px">
          คุณจะยังสามารถเข้าถึงข้อมูลได้เต็มที่จนถึง <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          หลังจากนั้น ข้อมูลร้านค้าของคุณจะถูกเก็บรักษาไว้เป็นเวลา 30 วันจนถึง <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          หากคุณต้องการส่งออกข้อมูลก่อนที่การเข้าถึงจะสิ้นสุด คุณสามารถทำได้จากแดชบอร์ดผู้ดูแลระบบ เปลี่ยนใจแล้ว? คุณสามารถเปิดใช้งานการสมัครสมาชิกได้ทุกเมื่อ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="เปิดใช้งานการสมัครสมาชิก" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ยืนยันการยกเลิก - {{ store_name }}

สวัสดี {{ name|default:'there' }},

การสมัครสมาชิก {{ plan_name }} ของคุณถูกยกเลิกแล้ว

สิ่งที่จะเกิดขึ้นต่อไป:
- คุณจะยังสามารถเข้าถึงข้อมูลได้เต็มที่จนถึง {{ access_until_date }}.
- หลังจากนั้น ข้อมูลร้านค้าของคุณจะถูกเก็บรักษาไว้เป็นเวลา 30 วันจนถึง {{ termination_date }}.

หากคุณต้องการส่งออกข้อมูลก่อนที่การเข้าถึงจะสิ้นสุด คุณสามารถทำได้จากแดชบอร์ดผู้ดูแลระบบ เปลี่ยนใจแล้ว? คุณสามารถเปิดใช้งานการสมัครสมาชิกได้ทุกเมื่อ

เปิดใช้งานการสมัครสมาชิก: https://spwig.com/account

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}