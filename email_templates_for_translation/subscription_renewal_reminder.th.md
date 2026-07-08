---
template_type: subscription_renewal_reminder
category: Subscriptions
---

# Email Template: subscription_renewal_reminder

## Subject
🔔 การต่ออายุ {{ plan_name }} ภายใน {{ days_until_renewal }} วัน - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🔔 แจ้งเตือนการต่ออายุ
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          การสมัครสมาชิกของคุณกำลังจะต่ออายุเร็ว ๆ นี้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Info Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#f0f9ff" padding="30px" border="2px solid #0ea5e9" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#0c4a6e" align="center" padding-bottom="15px">
                ค่าธรรมเนียมที่จะถูกเรียกเก็บในอนาคต
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>แผน:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>จำนวนเงิน:</strong> {{ subscription_amount }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>วันที่ต่ออายุ:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>วิธีการชำระเงิน:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- Action Needed Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px" line-height="1.6" align="center">
          ไม่จำเป็นต้องดำเนินการใด ๆ การสมัครสมาชิกของคุณจะต่ออายุโดยอัตโนมัติในวันที่ {{ next_billing_date|date:"F d, Y" }}
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding="15px 20px 0 20px" line-height="1.6" align="center">
          ต้องการอัปเดตวิธีการชำระเงินหรือทำการเปลี่ยนแปลง? กรุณาเข้าสู่แดชบอร์ดบัญชีของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          จัดการการสมัครสมาชิก
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ update_payment_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            อัปเดตวิธีการชำระเงิน
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          ต้องการความช่วยเหลือ? ติดต่อเราที่ {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Powered by Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔔 แจ้งเตือนการต่ออายุ

การสมัครสมาชิกของคุณกำลังจะต่ออายุเร็ว ๆ นี้

ค่าธรรมเนียมที่จะถูกเรียกเก็บในอนาคต:
แผน: {{ plan_name }}
จำนวนเงิน: {{ subscription_amount }}
วันที่ต่ออายุ: {{ next_billing_date|date:"F d, Y" }}
วิธีการชำระเงิน: {{ payment_method }}

ไม่จำเป็นต้องดำเนินการใด ๆ การสมัครสมาชิกของคุณจะต่ออายุโดยอัตโนมัติในวันที่ {{ next_billing_date|date:"F d, Y" }}

ต้องการอัปเดตวิธีการชำระเงินหรือทำการเปลี่ยนแปลง? กรุณาเข้าสู่แดชบอร์ดบัญชีของคุณ

จัดการการสมัครสมาชิก: {{ manage_subscription_url }}
อัปเดตวิธีการชำระเงิน: {{ update_payment_url }}

ต้องการความช่วยเหลือ? ติดต่อเราที่ {{ support_email }}

---
Powered by Spwig - https://spwig.com