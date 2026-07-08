---
template_type: subscription_resumed
category: Subscriptions
---

# Email Template: subscription_resumed

## Subject
▶️ การสมัครสมาชิก {{ plan_name }} ของคุณกลับมาใช้งานอีกครั้ง - {{ shop_name }}

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
          ▶️ ยินดีต้อนรับกลับ!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          การสมัครสมาชิกของคุณกลับมาใช้งานอีกครั้ง
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resume Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#f0fdf4" padding="30px" border="2px solid {{ theme.color.success|default:'#10b981' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#14532d" align="center" padding-bottom="15px">
                รายละเอียดการสมัครสมาชิก
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>แผน:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>เริ่มใช้งานอีกครั้งเมื่อ:</strong> {{ resume_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>รอบการเรียกเก็บเงินถัดไป:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>จำนวนเงิน:</strong> {{ subscription_amount }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>วิธีการชำระเงิน:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          ขั้นตอนต่อไปคืออะไร?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.success|default:'#10b981' }}; font-size: 18px; margin-right: 8px;">✓</span>
          การสมัครสมาชิกของคุณได้รับการเปิดใช้งานแล้ว
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.success|default:'#10b981' }}; font-size: 18px; margin-right: 8px;">✓</span>
          การเข้าถึงสิทธิประโยชน์ทั้งหมดได้กลับมาเป็นปกติแล้ว
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.success|default:'#10b981' }}; font-size: 18px; margin-right: 8px;">✓</span>
          การเรียกเก็บเงินจะกลับมาเป็นปกติในวันที่ {{ next_billing_date|date:"F d, Y" }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          จัดการการสมัครสมาชิก
        </mj-button>
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
▶️ ยินดีต้อนรับกลับ!

การสมัครสมาชิกของคุณกลับมาใช้งานอีกครั้ง

รายละเอียดการสมัครสมาชิก:
แผน: {{ plan_name }}
เริ่มใช้งานอีกครั้งเมื่อ: {{ resume_date|date:"F d, Y" }}
รอบการเรียกเก็บเงินถัดไป: {{ next_billing_date|date:"F d, Y" }}
จำนวนเงิน: {{ subscription_amount }}
วิธีการชำระเงิน: {{ payment_method }}

ขั้นตอนต่อไปคืออะไร?
✓ การสมัครสมาชิกของคุณได้รับการเปิดใช้งานแล้ว
✓ การเข้าถึงสิทธิประโยชน์ทั้งหมดได้กลับมาเป็นปกติแล้ว
✓ การเรียกเก็บเงินจะกลับมาเป็นปกติในวันที่ {{ next_billing_date|date:"F d, Y" }}

จัดการการสมัครสมาชิก: {{ manage_subscription_url }}

ต้องการความช่วยเหลือ? ติดต่อเราที่ {{ support_email }}

---
Powered by Spwig - https://spwig.com