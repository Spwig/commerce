---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
แจ้งเตือนการระงับ - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          การแจ้งเตือนการระงับ
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
          การชำระเงินสำหรับ <strong>{{ plan_name }}</strong> ของคุณล่าช้า หากไม่ได้แก้ไขภายใน <strong>{{ grace_end_date }}</strong> ร้านค้าของคุณจะถูกตั้งค่าให้อยู่ในโหมดอ่านเท่านั้น
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          การระงับหมายถึงอะไร
        </mj-text>
        <mj-text font-size="14px">
          หากร้านค้าของคุณถูกระงับ ร้านค้าจะยังคงปรากฏให้ผู้เยี่ยมชมเห็นได้ แต่คุณจะไม่สามารถทำการเปลี่ยนแปลงใด ๆ ได้ คำสั่งซื้อใหม่จะถูกหยุดจนกว่าจะชำระยอดค้างชำระเรียบร้อย
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          กรุณาอัปเดตวิธีการชำระเงินของคุณเพื่อหลีกเลี่ยงการรบกวนใด ๆ ต่อร้านค้าของคุณ
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
แจ้งเตือนการระงับ - {{ store_name }}

สวัสดี {{ name|default:'there' }},

การชำระเงินสำหรับ {{ plan_name }} ของคุณล่าช้า หากไม่ได้แก้ไขภายใน {{ grace_end_date }}, ร้านค้าของคุณจะถูกตั้งค่าให้อยู่ในโหมดอ่านเท่านั้น

การระงับหมายถึงอะไร:
หากร้านค้าของคุณถูกระงับ ร้านค้าจะยังคงปรากฏให้ผู้เยี่ยมชมเห็นได้ แต่คุณจะไม่สามารถทำการเปลี่ยนแปลงใด ๆ ได้ คำสั่งซื้อใหม่จะถูกหยุดจนกว่าจะชำระยอดค้างชำระเรียบร้อย

กรุณาอัปเดตวิธีการชำระเงินของคุณเพื่อหลีกเลี่ยงการรบกวนใด ๆ ต่อร้านค้าของคุณ

อัปเดตวิธีการชำระเงิน: https://spwig.com/account

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}