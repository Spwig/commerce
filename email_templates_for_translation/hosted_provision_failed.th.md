---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
ต้องดำเนินการ - ปัญหาการตั้งค่าร้านค้าสำหรับ {{ store_name }}

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ปัญหาการตั้งค่าร้านค้า
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
          เราพบปัญหาขณะตั้งค่าร้านค้าของคุณ <strong>{{ store_name }}</strong> ทีมของเราได้รับการแจ้งและกำลังตรวจสอบปัญหาอยู่
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          เกิดอะไรขึ้น
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          จะเกิดอะไรขึ้นต่อไป?
        </mj-text>
        <mj-text font-size="14px">
          ทีมสนับสนุนของเราได้รับการแจ้งอัตโนมัติเกี่ยวกับปัญหานี้ คุณไม่จำเป็นต้องดำเนินการใด ๆ - เราจะติดต่อคุณเมื่อปัญหาได้รับการแก้ไข
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          หากคุณมีคำถามใด ๆ ในระหว่างนี้ กรุณาอย่าลังเลที่จะติดต่อเรา
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ปัญหาการตั้งค่าร้านค้า - {{ store_name }}

สวัสดี {{ name|default:'there' }},

เราพบปัญหาขณะตั้งค่าร้านค้าของคุณ {{ store_name }} ทีมของเราได้รับการแจ้งและกำลังตรวจสอบปัญหาอยู่

เกิดอะไรขึ้น:
{{ provision_error }}

จะเกิดอะไรขึ้นต่อไป?
ทีมสนับสนุนของเราได้รับการแจ้งอัตโนมัติเกี่ยวกับปัญหานี้ คุณไม่จำเป็นต้องดำเนินการใด ๆ - เราจะติดต่อคุณเมื่อปัญหาได้รับการแก้ไข

หากคุณมีคำถามใด ๆ ในระหว่างนี้ กรุณาอย่าลังเลที่จะติดต่อเรา

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}